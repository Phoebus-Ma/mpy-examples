###
# Ky-035 hall sensor example.
#
# License - MIT.
###

# 能够检测磁性和相对强度.
# 初始值是输入电压的一半,
# 磁性材料不同极性靠近会输出更高或更低的电压,
# 靠近的距离也会导致输出电压增加或减小的值.
import time
from machine import Pin, ADC


# 初始化引脚
analog_pin = ADC(Pin(4))         # KY-035 模拟输出接 GPIO4

# 配置 ADC 参数（量程 0-3.3V，11dB 衰减）
analog_pin.atten(ADC.ATTN_11DB)   # 设置量程为 0-3.3V
analog_pin.width(ADC.WIDTH_12BIT) # 12位分辨率（0-4095）

# 校准传感器基准值（无磁场时）
def calibrate_sensor(samples=100):
    baseline = 0
    for _ in range(samples):
        baseline += analog_pin.read()
        time.sleep_ms(10)
    return baseline // samples

baseline = calibrate_sensor()
print("Baseline value:", baseline)

# 主循环：检测磁场变化
while True:
    analog_value = analog_pin.read()
    
    # 判断磁场强度（阈值可根据实测调整）
    if abs(analog_value - baseline) > 500:  # 模拟阈值
        print("Magnetic field detected! Analog:", analog_value)
    
    time.sleep(1)
