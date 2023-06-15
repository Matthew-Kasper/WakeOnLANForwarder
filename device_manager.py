import credentials_cache
import uping


def get_status(ip):
    response = uping.ping(ip, count=4, timeout=1000, quiet=True)

    # Return true if all packets arrived successfully
    return response[0] == response[1]


def wake(wol_socket):
    # Converts mac_address into a list of bytes
    mac_address = credentials_cache.get_target_mac()
    mac_address_bytes = bytearray.fromhex(str(mac_address))
    mac_address_bytes_list = [mac_address_bytes[0], mac_address_bytes[1], mac_address_bytes[2], mac_address_bytes[3],
                              mac_address_bytes[4], mac_address_bytes[5]]

    # Prepares payload
    broadcast_address = credentials_cache.get_broadcast_ip()
    payload = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF] + (mac_address_bytes_list * 16)

    wol_socket.sendto(bytes(payload), (str(broadcast_address), 9))


def kill(kol_socket):
    # Stub
    print("kill")
