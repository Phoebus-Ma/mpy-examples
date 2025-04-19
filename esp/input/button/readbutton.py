###
# Read button value.
#
# License - MIT.
###

import time
from machine import Pin


# 初始化按键引脚 (使用内部上拉电阻).
button = Pin(0, Pin.IN, Pin.PULL_UP)

def read_button():
    # 读取按键状态 (按下时返回False，因为上拉到高电平).
    return not button.value()

# 简单去抖动函数.
def debounce(button_state):
    time.sleep_ms(50)  # 等待抖动消失.
    return read_button() == button_state

while True:
    if read_button():
        print("Button pressed!")
        # 等待按键释放 (带防抖).
        while debounce(True):
            pass
    else:
        # 添加适当延时防止CPU过载.
        time.sleep_ms(100)
