###
# Read adc value example.
#
# License - MIT.
###

import machine
import time


# 初始化ADC通道，假设使用GPIO引脚32 (ADC通道0).
adc_channel = machine.ADC(machine.Pin(0))

# 配置ADC衰减级别.
# ADC.ATTN_0DB   : 0dB衰减，输入电压范围 0~1.1V;
# ADC.ATTN_2_5DB : 2.5dB衰减，输入电压范围 0~1.5V;
# ADC.ATTN_6DB   : 6dB衰减，输入电压范围 0~2.2V;
# ADC.ATTN_11DB  : 11dB衰减，输入电压范围 0~3.3V .
adc_channel.atten(machine.ADC.ATTN_11DB)

while True:
    # 读取ADC值
    adc_value = adc_channel.read()
    print("ADC值:", adc_value)
    time.sleep(1)  # 等待1秒
