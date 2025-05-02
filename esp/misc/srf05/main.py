###
# HY-SRF05 ultrasonic wave module example.
#
# License - MIT.
###

import time
from machine import Pin, time_pulse_us

class SRF05:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger = Pin(trigger_pin, Pin.OUT)
        self.echo = Pin(echo_pin, Pin.IN)
        self.trigger.value(0)  # 初始化触发引脚为低电平.

    def get_distance_cm(self, max_cm=400):
        """
        获取距离 (厘米).
        :param max_cm: 最大测量距离 (超过此值返回0).
        :return: 距离值 (厘米)或0 (超时).
        """
        # 发送触发脉冲 (至少10us高电平).
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)

        # 测量回波脉冲宽度 (微秒).
        pulse_width = time_pulse_us(self.echo, 1, max_cm * 58 * 2)

        # 计算距离 (时间 * 声速 / 2 (往返)).
        # 声速在空气中约343m/s → 34300cm/s → 1cm需要约29.157us .
        # 因此距离 = (时间 / 2) / 29.157 ≈ 时间 / 58.314 .
        if pulse_width > 0:
            distance = (pulse_width / 2) / 29.157
            return round(distance, 2) if distance <= max_cm else 0
        return 0  # 超时返回0.

# 使用示例
if __name__ == "__main__":
    # 初始化传感器 (根据实际接线修改引脚号).
    srf = SRF05(trigger_pin=6, echo_pin=5)

    while True:
        distance = srf.get_distance_cm()

        if distance > 0 and distance < 400:
            print("Distance:", distance, "cm")
            
        time.sleep(1)
