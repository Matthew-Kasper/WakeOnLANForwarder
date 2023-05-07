import utime

# Opens html file and stores it in a string
html_file = open("index.html", "r")
html_base = html_file.read()


# Generates html page to be sent.
def get_html(is_enabled, runtime, send_status):
    if (runtime == -1):
        # Do not display runtime
        device_status = str(is_enabled)
    else:
        # Display runtime
        formatted_time = utime.localtime(runtime)
        device_status = f"{str(is_enabled)} for {int(formatted_time[3])} hours, {int(formatted_time[4])} minutes, and {int(formatted_time[5])} seconds."

    html = html_base.format(send_status, device_status)
    return f"HTTP/1.1 200\r\nContent-Type: text/html\r\n\r\n{html}\n"
