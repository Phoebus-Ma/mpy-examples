###
# IR1838 example.
#
# License - MIT.
###

# IR1838红外传感器，红外遥控采用NEC编码.
# ir1838 - GPIO5.
import time
from machine import Pin


# 初始化红外接收引脚.
ir_pin    = Pin(5, Pin.IN, Pin.PULL_UP)
last_time = 0
pulses    = []

def ir_handler(pin):
    global last_time, pulses
    current_time = time.ticks_us()
    if last_time > 0:
        pulse_duration = time.ticks_diff(current_time, last_time)
        pulses.append(pulse_duration)
    last_time = current_time

ir_pin.irq(trigger=Pin.IRQ_FALLING, handler=ir_handler)

def decode_nec(pulses):
    if len(pulses) < 2 or pulses[0] < 9000 or pulses[1] < 4500:
        return None
    data = 0
    for i in range(2, len(pulses)):
        if i % 2 == 0 and pulses[i] > 1600:
            data |= (1 << ((i//2) - 1))
    return hex(data)

while True:
    if len(pulses) > 32:
        code = decode_nec(pulses)
        if code:
            print("IR Code:", code)
        pulses.clear()
        last_time = 0
    time.sleep_ms(100)
