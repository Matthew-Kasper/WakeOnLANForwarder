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

    # Make sure that it gets connected to the network
    while not wlan.isconnected():
        utime.sleep(1)
        status_light.send_blinks(1)

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
        request = str(client.recv(1024))

        # Initialize a status to send
        send_status = ""

        # Find and cache the device_status
        device_on = device_manager.get_status(target_ip)

        try:
            # Isolate part of request with form information
            request_list = request.split()

            if request_list[0] == "b'POST":
                # Set default password
                password = ""

                raw_form_data = request_list[len(request_list) - 1]
                # Find password
                password_index_start = raw_form_data.find("password=")
                password_index_end = raw_form_data.find("&")

                # Check to see if password start and end markers exist
                if password_index_start != -1 and password_index_end != -1:
                    password = raw_form_data[password_index_start + len("password="):password_index_end]

                # Check if password is correct
                if password == credentials_cache.get_operation_password():
                    if raw_form_data.find("On") != -1 and not device_on:
                        # If button On was pressed
                        device_manager.wake(wol_socket)
                        send_status = "Successfully sent Wake-On-Lan packet to device."
                    elif raw_form_data.find("Off") != -1 and device_on:
                        # If button Off was pressed
                        device_manager.kill("Stub")
                        send_status = "Successfully sent Kill-On-Lan packet to device."
                    else:
                        send_status = "Can not wake/kill when device is already in that state."
                else:
                    send_status = "Incorrect Password."
            else:
                # It is a get request
                pass
        except IndexError:
            pass

        # Generate and send new html page
        if device_on:
            if first_enable:
                # Reset time of first enable
                first_enable_timestamp = utime.time()

            # Find device runtime
            device_runtime = utime.time() - first_enable_timestamp

            html = html_cache.get_html("on", device_runtime, send_status)

            # Reset first_enable status when enabled for first time
            first_enable = False
        else:
            html = html_cache.get_html("off", -1, send_status)

            # Reset first_enable status when device powers off
            first_enable = True

        client.send(html)
        client.close()

        # Send status that request was fulfilled
        status_light.send_blinks(3)
