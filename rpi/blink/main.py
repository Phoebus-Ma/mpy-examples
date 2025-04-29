###
# Blink for led on and off.
#
# License - MIT.
###

import time
from machine import Pin


# GPIO25 是板载LED灯.
led = Pin(25, Pin.OUT)  

while True:
    led.value(1)
    time.sleep(0.5)
    led.value(0)
    time.sleep(0.5)
