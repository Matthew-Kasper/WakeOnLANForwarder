import utime
from machine import Pin

status_light = Pin("LED", Pin.OUT)

# Blink Pi Pico light to indicate certain statuses
def(blinks):
    count = 1

    for count in range(1, blinks):
        status_light.on()
        utime.sleep_ms(5)
        status_light.off()
