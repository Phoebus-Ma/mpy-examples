###
# SSD1315 oled i2c example.
#
# License - MIT.
###

# PS2摇杆，有两个adc (x轴和y轴)，和一个按键.
# vrx    - GPIO4.
# vry    - GPIO5.
# Button - GPIO15.
from machine import Pin, ADC
import time


# 定义PS2摇杆的引脚.
vrx = ADC(Pin(4))  # X轴连接到ADC引脚32.
vry = ADC(Pin(5))  # Y轴连接到ADC引脚33.
btn = Pin(15, Pin.IN, Pin.PULL_UP)  # 按键连接到数字引脚15.

# 配置ADC的衰减比和宽度.
vrx.atten(ADC.ATTN_11DB)    # 衰减比为11dB，测量范围为0-3.3V.
vry.atten(ADC.ATTN_11DB)
vrx.width(ADC.WIDTH_12BIT)  # 宽度为12位，对应的范围0-4095.
vry.width(ADC.WIDTH_12BIT)

while True:
    # 读取X轴和Y轴的值.
    x_value = vrx.read()
    y_value = vry.read()

    # 检测按键状态.
    button_pressed = not btn.value()  # 按键按下时为True.

    # 打印摇杆值和按键状态.
    print(f'X轴值: {x_value}, Y轴值: {y_value}, 按键状态: {button_pressed}')

    # 根据摇杆值执行操作 (示例：控制电机或舵机).
    # 例如：控制舵机角度.
    # angle = int((x_value / 4095) * 180)   # 将X轴值映射到0-180度.
    # pwm_duty = int((angle / 180) * 1023)  # 将角度映射到PWM占空比0-1023.
    # servo.duty(pwm_duty)

    # 等待100毫秒.
    time.sleep(0.1)
