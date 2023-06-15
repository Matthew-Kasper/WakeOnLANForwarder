import socket

import network
import utime

import credentials_cache
import device_manager
import html_cache
import http_utils
import status_light


# Connects to local network, returns IPv4 of device
def connect():
    # Takes first and second line of credentials file and takes the ssid and password from them
    ssid = credentials_cache.get_ssid()
    password = credentials_cache.get_inet_password()

    # Connect to the network using ssid and password
    wlan = network.WLAN(network.STA_IF)

    # Disable power save
    wlan.config(pm=0xa11140)

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

    # Make sure that a connection can not block
    connection.settimeout(30)

    connection.bind(address)
    connection.listen(1)

    return (connection)


# Creates broadcast socket to be used for sending wake-on-lan packets
def establish_wol_socket():
    wol_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    return wol_socket


# Checks if an html form button was pressed and updates the html page
def serve(connection, wol_socket):
    # Initialize reference to network interface to check if connected to network
    wlan = network.WLAN(network.STA_IF)

    # Initialize system timer variables
    first_enable = True
    first_enable_timestamp = -1

    while wlan.isconnected():
        # Check every refresh loop if the device has been enabled and log start-time
        device_on = device_manager.get_status(credentials_cache.get_target_ip())

        if (device_on):
            if first_enable:
                first_enable_timestamp = utime.time()
            first_enable = False
        else:
            first_enable = True

        try:
            # Accept client connection and reads request
            client = connection.accept()[0]
        except OSError:
            # Refreshes the listener on the timeout interval to clear invalid requests

            # Update device up-timer between listening refreshes
            device_manager.get_status(credentials_cache.get_target_ip())
            status_light.send_blinks(1)
            continue

        try:
            request = str(client.recv(1024))
        except OSError:
            # If request could not be parsed, close connection and continue from top
            status_light.send_blinks(2)
            client.close()
            continue

        send_status, post_body_found = http_utils.parse_post(request, wol_socket, override_post_check=False)

        # If password fields could not be found, body was not send along with the header, need to receive again
        if not post_body_found:
            status_light.send_blinks(1)
            # Receive body
            request = str(client.recv(1024))

            # Retry process, but if it fails do not try again
            send_status = http_utils.parse_post(request, wol_socket, override_post_check=True)[0]

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

        # Wait for html to be finished sending
        utime.sleep(1)

        client.close()

        # Send status that request was fulfilled
        status_light.send_blinks(3)
