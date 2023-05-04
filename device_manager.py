import os

import uping


def get_target_ip():
    # Open credentials.csv that stores target_ip information
    credentials = open("credentials.txt", "r")
    lines = credentials.readlines()

    # Take target device ip from third line
    target_ip = lines[2].strip()

    return target_ip

def get_status(ip):
    response = uping.ping(ip, count=2, timeout=500, quiet=True)

    # Return on if all packets arrived successfully
    if(response[0] == response[1]):
        return "on"
    else:
        return "off"

def wake(ip):

def kill(ip):