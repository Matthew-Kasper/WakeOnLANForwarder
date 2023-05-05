import socket

import network

import device_manager
import status_light


# Connects to local network, returns IPv4 of device
def connect():
    # Open credentials.csv that stores network information
    credentials = open("credentials.txt", "r")
    lines = credentials.readlines()

    # Takes first and second line of credentials file and takes the ssid and password from them
    ssid = lines[0].strip()
    password = lines[1].strip()

    # Connect to the network using ssid and password
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(str(ssid), str(password))

    return str(wlan.ifconfig()[0])

# Generates html page to be sent
def page(status):
    html = f"""
            <!DOCTYPE html>
            <html>
            <body>
            <p>Wake on LAN Forwarder.</p>
            <form action="./On">
            <input type="submit" value="On " />
            </form>
            <form action="./Off">
            <input type="submit" value="Off" />
            </form>
            <p>Device is currently {str(status)}.</p>
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

# Checks if an html form button was pressed and updates the html page
def serve(connection, target_ip):
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
            device_manager.wake(target_ip)
        elif request == '/Off?' and device_manager.get_status(target_ip):
            device_manager.kill(target_ip)

        # Generate and send new html page
        if device_manager.get_status(target_ip):
            html = page("on")
        else:
            html = page("off")

        client.send(html)
        client.close()

        # Send status that request was fulfilled
        status_light.send_blinks(3)