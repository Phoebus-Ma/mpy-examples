###
# EC11 example.
#
# License - MIT.
###

# EC11旋转编码器.
# CLK - GPIO4.
# DT  - GPIO5.
# SW  - GPIO6.
import time
from machine import Pin, Timer


# 配置EC11引脚 (根据实际连接修改).
CLK_PIN = 4   # A相.
DT_PIN  = 5   # B相.
SW_PIN  = 6   # 按键.

# 初始化全局变量.
counter     = 0
clk_last    = 0
clk_current = 0
sw_pressed  = False

# 初始化引脚.
clk = Pin(CLK_PIN, Pin.IN, Pin.PULL_UP)
dt  = Pin(DT_PIN, Pin.IN, Pin.PULL_UP)
sw  = Pin(SW_PIN, Pin.IN, Pin.PULL_UP)

# 旋转编码器中断处理函数.
def handle_encoder(pin):
    global clk_last, counter
    clk_current = clk.value()
    
    # CLK状态变化.
    if clk_current != clk_last:
        dt_value = dt.value()

        # 顺时针旋转.
        if dt_value != clk_current:
            counter += 1
        # 逆时针旋转.
        else:
            counter -= 1
    clk_last = clk_current

# 按键中断处理函数 (带简单防抖).
def handle_sw(pin):
    global sw_pressed
    # 简单防抖.
    time.sleep_ms(20)
    if sw.value() == 0:
        sw_pressed = True

# 配置中断.
clk.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=handle_encoder)
sw.irq(trigger=Pin.IRQ_FALLING, handler=handle_sw)

# 主循环.
while True:
    if sw_pressed:
        print("Button pressed! Counter reset.")
        counter = 0
        sw_pressed = False
        
    # 显示当前计数值 (可根据需要修改输出方式).
    print("Counter:", counter)

    # 控制刷新频率.
    time.sleep(0.1)
