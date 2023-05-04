import net_wol
import status_light

# Connect to network
net_wol.connect()

# Successfully connected to network
status_light.send_blinks(1)