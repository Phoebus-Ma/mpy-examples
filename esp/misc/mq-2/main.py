###
# MQ-2 sensor example.
#
# License - MIT.
###

import time
import machine
from math import log


# 初始化 ADC 和 GPIO (根据实际接线调整引脚)
adc = machine.ADC(machine.Pin(6))  # 模拟输入
adc.atten(machine.ADC.ATTN_11DB)    # 设置 ADC 衰减为 11dB (量程 0-3.3V)
digital_pin = machine.Pin(5, machine.Pin.IN)  # 数字输入

# 校准参数（需根据实际环境调整）
CLEAN_AIR_RO = 9.83  # 洁净空气中的传感器电阻（单位：kΩ）
RL = 5.0             # 模块上的负载电阻（单位：kΩ）
THRESHOLD = 1000     # 报警阈值（ADC 原始值）

def read_mq2():
    # 读取 ADC 值（取10次平均值滤波）
    adc_value = 0
    for _ in range(10):
        adc_value += adc.read()
        time.sleep_ms(10)
    adc_value = adc_value / 10
    
    # 计算电压和传感器电阻
    voltage = (adc_value / 4095) * 3.3  # ESP32 ADC 为 12位 (0-4095)
    rs = (3.3 - voltage) / voltage * RL  # 传感器电阻（kΩ）
    
    # 计算气体浓度比例（简化模型）
    ratio = rs / CLEAN_AIR_RO
    return adc_value, ratio

def check_alarm(adc_value):
    # 检查数字输出或模拟阈值
    if adc_value > THRESHOLD or digital_pin.value() == 0:
        print("警报！检测到可燃气体或烟雾！")
        # 触发其他操作（如点亮LED、发送网络请求等）

# 预热传感器（MQ-2需要约1-2分钟预热）
print("预热传感器中...请等待 20 秒.")
time.sleep(20)

while True:
    adc_val, ratio = read_mq2()
    print("ADC值:", adc_val, "| 电阻比:", ratio)
    check_alarm(adc_val)
    time.sleep(1)
