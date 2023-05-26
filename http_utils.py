import credentials_cache
import device_manager


def parse_post(request, wol_socket, override_post_check):
    # Initialize a status to send
    send_status = ""

    # Initialize post body found flag
    post_body_found = True

    # Find and cache the device_status
    device_on = device_manager.get_status(credentials_cache.get_target_ip())

    try:
        if (request.find("b'POST") != -1) or override_post_check:
            # If request is a post request

            # Set default password
            password = ""

            # Find password
            password_index_start = request.find("password=")

            # Initialize index end in case it never gets set
            password_index_end = -1

            # If start of password exists, find ending position
            if (password_index_start != -1):
                # Try and find end of password data starting from the password starting position
                password_index_end = request[password_index_start:].find(r"\r\n") + password_index_start

            # Check to see if password start and end markers exist
            if password_index_start != -1 and password_index_end != -1:
                password = request[password_index_start + len("password="):password_index_end]
            else:
                post_body_found = False

            # Check if password is correct
            if password == credentials_cache.get_operation_password():
                if request.find("Wake") != -1 and not device_on:
                    # If button On was pressed
                    device_manager.wake(wol_socket)
                    send_status = "Successfully sent Wake-On-Lan packet to device."
                else:
                    send_status = "Can not wake when device is already on."
                    pass
            else:
                send_status = "Incorrect Password."
                pass

        else:
            # It is a get request
            pass
    except IndexError:
        pass

    return send_status, post_body_found
