import utime

# Opens html file and stores it in a string
html_file = open("index.html", "r")
html_base = html_file.read()


# Generates html page to be sent.
def get_html(is_enabled, runtime):
    if (runtime == -1):
        # Do not display runtime
        status = str(is_enabled)
    else:
        # Display runtime
        formatted_time = utime.localtime(runtime)
        status = f"{str(is_enabled)} for {int(formatted_time[3])} hours, {int(formatted_time[4])} minutes, and {int(formatted_time[5])} seconds."

    html = html_base.format(status)
    return html
