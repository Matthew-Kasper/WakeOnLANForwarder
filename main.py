import os
import sys

import net_wol
import status_light
from uio import StringIO

# Find log number to name the current log
log_number = len(os.listdir("/logs/"))

with open("/logs/" + f"{log_number}_log.txt", 'w') as write_file:
    try:
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
    except Exception as e:
        # Print the exception to the string buffer and write them to the log file
        exception_string = StringIO()
        sys.print_exception(e, exception_string)
        write_file.write(str(exception_string.getvalue()) + "\n")
