###
# Button irq example.
#
# License - MIT.
###

# 按键下降沿中断，按下按键，触发中断，切换LED状态.
# Button - GPIO7.
# LED    - GPIO8.
import time
from machine import Pin


# 初始化LED和按钮引脚.
led    = Pin(8, Pin.OUT)  # LED连接到GPIO8.
button = Pin(7, Pin.IN, Pin.PULL_UP)  # 按钮连接到GPIO7，启用上拉电阻.

# 中断标志变量.
interrupt_flag = False

# 中断处理函数.
def button_handler(pin):
    global interrupt_flag
    interrupt_flag = True  # 设置中断标志.

# 配置按钮中断 (下降沿触发).
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)

while True:
    if interrupt_flag:
        interrupt_flag = False  # 重置中断标志.
        print("按键按下!")
        led.value(not led.value())  # 切换LED状态.
        # 简单防抖：延时检测电平状态.
        time.sleep_ms(20)
        if not button.value():
            print("确认按键按下")

    # 降低CPU占用.
    time.sleep_ms(10)
