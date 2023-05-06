import socket

import network
import utime

import credentials_cache
import device_manager
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

# Generates html page to be sent.
def page(is_enabled, runtime):

    if(runtime == -1):
        # Do not display runtime
        status = str(is_enabled)
    else:
        # Display runtime
        formatted_time = utime.localtime(runtime)
        status = f"{str(is_enabled)} for {int(formatted_time[3])} hours, {int(formatted_time[4])} minutes, and {int(formatted_time[5])} seconds."


    html = f"""
            <!DOCTYPE html>
            <html>
            <body>
            <h2>Wake on LAN Forwarder.</h2>
            <form action="./On">
            <input type="submit" value="       On       " style="height:100px;font-size:14pt;float:left;" />
            </form>
            <form action="./Off">
            <input type="submit" value="       Off       " style="height:100px;font-size:14pt;" />
            </form>
            <p>Device is currently {status}.</p>
            </body>
            </html>
            """
    return html

# Opens socket to listen for http requests
def listen(ip):

    # Format address
    address = (ip, 80)

    # Bind and listen on port for http requests
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)

    return(connection)

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

            html = page("on", device_runtime)

            # Reset first_enable status when enabled for first time
            first_enable = False
        else:
            html = page("off", -1)

            # Reset first_enable status when device powers off
            first_enable = True

        client.send(html)
        client.close()

        # Send status that request was fulfilled
        status_light.send_blinks(3)