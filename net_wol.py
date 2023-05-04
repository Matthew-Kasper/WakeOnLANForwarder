import csv

def connect():
    # Open credentials.csv that stores network information
    with open("credentials.csv") as credentials:
        csv_reader = csv.reader(credentials, delimiter=',')

        # Parse network credentials from csv
        ssid = csv_reader[0][0]
        password = csv_reader[0][1]
