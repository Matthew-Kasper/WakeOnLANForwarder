import network

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