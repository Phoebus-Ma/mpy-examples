###
# PWM play music example.
#
# License - MIT.
###

# 使用 PWM 通过无源蜂鸣器播放音乐小星星.
import time
from machine import Pin, PWM


# 定义无源蜂鸣器 PWM 对象.
pos_buzzer = PWM(Pin(4, Pin.OUT))

# 定义音调频率列表.
tone_list = [262, 294, 330, 350, 393, 441, 495]

# 定义乐谱音符列表.
music = [
    1, 1, 5, 5, 6, 6, 5, 0,
    5, 5, 4, 4, 3, 3, 2, 0,
    5, 5, 4, 4, 3, 3, 2, 0,
    5, 5, 4, 4, 3, 3, 2, 0,
    1, 1, 5, 5, 6, 6, 5, 0,
    4, 4, 3, 3, 2, 2, 1, 0
]


# 自动播放音乐.
for i in music:
    pos_buzzer.duty(900)
    if i:
        pos_buzzer.freq(tone_list[i-1])
        time.sleep_ms(500)
        pos_buzzer.duty(0)
        time.sleep_ms(10)

# 占空比设置为 0.
pos_buzzer.duty(0)
