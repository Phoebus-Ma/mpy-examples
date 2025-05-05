###
# Touch screen ft6336u i2c example.
#
# License - MIT.
###

import time
from machine import Pin, I2C, Timer

# 硬件初始化
i2c = I2C(0, sda=Pin(6), scl=Pin(7), freq=400_000)
int_pin = Pin(5, Pin.IN, Pin.PULL_UP)
rst_pin = Pin(4, Pin.OUT)

# FT6336U 配置
FT6336U_ADDR = 0x38
FT6336U_REG_DEVICE_MODE = 0x00
FT6336U_REG_TOUCHES = 0x02
FT6336U_REG_TOUCH1_XH = 0x03

def ft6336u_init():
    i2c.writeto_mem(FT6336U_ADDR, FT6336U_REG_DEVICE_MODE, b'\x00')
    time.sleep_ms(50)

def read_touch():
    data = i2c.readfrom_mem(FT6336U_ADDR, FT6336U_REG_TOUCH1_XH, 4)
    x = ((data[0] & 0x0F) << 8) | data[1]
    y = ((data[2] & 0x0F) << 8) | data[3]
    event = (data[0] >> 6) & 0x03
    return x, y, event

def touch_interrupt(pin):
    if int_pin.value() == 0:
        x, y, event = read_touch()
        if event in [1, 3]:
            print(f"Touch: X={x}, Y={y}, Event={'Down' if event==1 else 'Move'}")
        elif event == 2:
            print("Touch Up")

# 启动
rst_pin.value(0)
time.sleep_ms(6)
rst_pin.value(1)

ft6336u_init()
int_pin.irq(trigger=Pin.IRQ_FALLING, handler=touch_interrupt)

# 保持主程序运行
while True:
    time.sleep(1)
