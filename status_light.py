import utime
from machine import Pin

status_light = Pin("LED", Pin.OUT)

# Blink Pi Pico light to indicate certain statuses
def send_blinks(blinks):
    count = 0

    for count in range(0, blinks):
        status_light.on()
        utime.sleep_ms(75)
        status_light.off()
        utime.sleep_ms(75)
