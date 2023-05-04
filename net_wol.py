import csv

import network


def connect():
    # Open credentials.csv that stores network information
    with open("credentials.csv") as credentials:
        csv_reader = csv.reader(credentials, delimiter=',')

        # Parse network credentials from csv
        ssid = csv_reader[0][0]
        password = csv_reader[0][1]

        # Establish connection to router
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(str(ssid), str(password))