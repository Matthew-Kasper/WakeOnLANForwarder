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

    # Return true if all packets arrived successfully
    return response[0] == response[1]

def wake(ip):
    # Stub
    print("wake")
def kill(ip):
    # Stub
    print("kill")