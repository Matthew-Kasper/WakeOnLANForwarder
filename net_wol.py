import socket

import network
import utime

import credentials_cache
import device_manager
import html_cache
import status_light


# Connects to local network, returns IPv4 of device
def connect():
    # Takes first and second line of credentials file and takes the ssid and password from them
    ssid = credentials_cache.get_ssid()
    password = credentials_cache.get_inet_password()

    # Connect to the network using ssid and password
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(str(ssid), str(password))

    return str(wlan.ifconfig()[0])


# Opens socket to listen for http requests
def listen(ip):
    # Format address
    address = (ip, 80)

    # Bind and listen on port for http requests
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)

    return (connection)


# Creates broadcast socket to be used for sending wake-on-lan packets
def establish_wol_socket():
    wol_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    return wol_socket


# Checks if an html form button was pressed and updates the html page
def serve(connection, target_ip, wol_socket):
    # Initialize system timer variables
    first_enable = True
    first_enable_timestamp = -1

    while True:
        # Accept client connection and reads request
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)

        try:
            # Isolate part of request with form information
            request = request.split()[1]
        except IndexError:
            pass

        # Check for what button was pressed and if the server can be turned on/off
        if request == '/On?' and not device_manager.get_status(target_ip):
            device_manager.wake(wol_socket)
        elif request == '/Off?' and device_manager.get_status(target_ip):
            device_manager.kill("stub")

        # Generate and send new html page
        if device_manager.get_status(target_ip):
            if first_enable:
                # Reset time of first enable
                first_enable_timestamp = utime.time()

            # Find device runtime
            device_runtime = utime.time() - first_enable_timestamp

            html = html_cache.get_html("on", device_runtime)

            # Reset first_enable status when enabled for first time
            first_enable = False
        else:
            html = html_cache.get_html("off", -1)

            # Reset first_enable status when device powers off
            first_enable = True

        client.send(html)
        client.close()

        # Send status that request was fulfilled
        status_light.send_blinks(3)
