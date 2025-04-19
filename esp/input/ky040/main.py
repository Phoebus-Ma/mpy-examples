###
# Ky040 (EC11) example.
#
# License - MIT.
###

# EC11旋转编码器.
# CLK - GPIO4.
# DT  - GPIO5.
# SW  - GPIO6.
import time
from machine import Pin


# 定义旋转编码器引脚.
clk = Pin(4, Pin.IN, Pin.PULL_UP)
dt  = Pin(5, Pin.IN, Pin.PULL_UP)
sw  = Pin(6, Pin.IN, Pin.PULL_UP)

counter = 0
last_state = (clk.value(), dt.value())

while True:
    current_state = (clk.value(), dt.value())
    
    # 检测旋转方向.
    if current_state != last_state:
        if (current_state == (0, 1) and last_state == (1, 1)) or \
           (current_state == (1, 0) and last_state == (0, 0)):
            counter += 1
            print("顺时针旋转，计数器：", counter)
        elif (current_state == (1, 0) and last_state == (1, 1)) or \
             (current_state == (0, 1) and last_state == (0, 0)):
            counter -= 1
            print("逆时针旋转，计数器：", counter)
        last_state = current_state
    
    # 检测开关按下.
    if not sw.value():
        print("开关按下，计数器复位为0")
        counter = 0
    
    time.sleep(0.01)
