import device_manager
import net_wol
import status_light

# Connect to network
ip = net_wol.connect()

# Successfully connected to network
status_light.send_blinks(1)

# Open a socket on port 80 for http requests
connection = net_wol.listen(ip)

# Successfully opened the port
status_light.send_blinks(2)

# Accept client requests
net_wol.serve(connection, device_manager.get_target_ip())