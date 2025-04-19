###
# Matrix button example.
#
# License - MIT.
###

import time
from machine import Pin


# 行引脚设置为输入.
row_pins = [
    Pin(15, Pin.IN, Pin.PULL_UP),
    Pin(23, Pin.IN, Pin.PULL_UP),
    Pin(22, Pin.IN, Pin.PULL_UP),
    Pin(21, Pin.IN, Pin.PULL_UP)
]

# 列引脚设置为输出.
col_pins = [
    Pin(20, Pin.OUT),
    Pin(19, Pin.OUT),
    Pin(18, Pin.OUT),
    Pin(9,  Pin.OUT)
]


def read_keypad():
# {
    keys = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']
    ]

    for j, col_pin in enumerate(col_pins):
        # 将当前列设置为低电平.
        col_pin.value(0)

        for i, row_pin in enumerate(row_pins):
            # 检测行引脚的状态.
            if row_pin.value() == 0:
                # 将当前列恢复为高电平.
                col_pin.value(1)	
                # 返回按下的按键.
                return keys[i][j]
        
        # 将当前列恢复为高电平.
        col_pin.value(1)

    # 没有按键被按下.
    return None 
# }

# 循环读取键盘状态.
while True:
    key = read_keypad()
    if key is not None:
        print("按下的按键:", key)
    time.sleep(0.1)  # 短暂延迟.
