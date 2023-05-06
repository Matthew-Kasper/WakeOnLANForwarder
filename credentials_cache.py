credentials = open("credentials.txt", "r")
lines = credentials.readlines()

ssid = lines[0].strip()
inet_password = lines[1].strip()
target_ip = lines[2].strip()
broadcast_ip = lines[3].strip()
target_mac = lines[4].strip()
operation_password = lines[5].strip()

def get_ssid():
    return ssid

def get_inet_password():
    return inet_password

def get_target_ip():
    return target_ip

def get_broadcast_ip():
    return broadcast_ip

def get_target_mac():
    return target_mac

def get_operation_password():
    return operation_password
