import net_wol
import status_light

# Retry initialization if failed
while True:
    # Connect to network
    ip = net_wol.connect()

    # Successfully connected to network
    status_light.send_blinks(1)

    # Open a socket on port 80 for http requests and establish wol socket
    connection = net_wol.listen(ip)
    wol_socket = net_wol.establish_wol_socket()

    # Successfully opened the port
    status_light.send_blinks(2)

    # Accept client requests
    net_wol.serve(connection, wol_socket)
