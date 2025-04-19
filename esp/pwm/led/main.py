###
# DS1302 rtc i2c example.
#
# License - MIT.
###

# 呼吸灯，GPIO0 接LED正极.
import time
from machine import Pin, PWM


# 创建 LED 控制对象.
led = PWM(Pin(0), freq=1000)

while True:
    # 渐亮.
    for i in range(0, 1024):
        led.duty(i)
        time.sleep_ms(1)
    
    # 渐暗.
    for i in range(1023, 0, -1):
        led.duty(i)
        time.sleep_ms(1)
