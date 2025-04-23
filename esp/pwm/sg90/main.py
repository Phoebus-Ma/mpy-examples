###
# SG90 micro Servo example.
#
# License - MIT.
###

import time
from machine import Pin
from servo import Servo


# 定义舵机控制对象
my_servo = Servo(Pin(4), max_us=2500)


# 程序入口
if __name__ == '__main__':
    while True:
        my_servo.write_angle(0)
        time.sleep(1)
        my_servo.write_angle(45)
        time.sleep(1)
        my_servo.write_angle(90)
        time.sleep(1)
        my_servo.write_angle(135)
        time.sleep(1)
        my_servo.write_angle(180)
        time.sleep(1)
