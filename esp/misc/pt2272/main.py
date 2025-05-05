###
# PT2272 example.
#
# License - MIT.
###

# ESP32 PT2272 遥控解码示例
# 硬件说明：
# - PT2272-M4 模块 (4位数据输出).
# - VT引脚 → ESP32 GPIO4 (解码有效标志, 也可以只接这一根引脚, 解码成功变高电平).
# - D0-D3 → ESP32 GPIO10、11、2、3 (数据输出).
# - 需共地连接 (GND).
from machine import Pin
import time

# 硬件配置 (根据实际接线修改).
class PT2272_Config:
    VT_PIN = 4       # 解码有效信号引脚.
    DATA_PINS = [10, 11, 2, 3]  # 数据引脚 (D0-D3).
    DEBOUNCE_MS = 20 # 信号去抖时间.

class PT2272_Decoder:
    def __init__(self, config):
        self.config = config

        # 初始化VT引脚 (上升沿中断).
        self.vt_pin = Pin(self.config.VT_PIN, Pin.IN, Pin.PULL_UP)
        self.vt_pin.irq(
            trigger=Pin.IRQ_RISING,
            handler=self._vt_irq_handler
        )

        # 初始化数据引脚.
        self.data_pins = [
            Pin(p, Pin.IN, Pin.PULL_UP)
            for p in self.config.DATA_PINS
        ]

        # 状态变量.
        self.data_ready = False
        self.last_data = [0]*len(self.data_pins)

    def _vt_irq_handler(self, pin):
        """VT引脚中断处理"""
        # 添加简单防抖.
        if pin.value() == 1:
            time.sleep_ms(self.config.DEBOUNCE_MS)
            if pin.value() == 1:
                self.data_ready = True

    def read_data(self):
        """读取解码数据"""
        if not self.data_ready:
            return None

        # 读取数据引脚状态.
        current_data = [
            int(p.value())
            for p in self.data_pins
        ]

        # 验证数据稳定性 (可选).
        if current_data != self.last_data:
            self.last_data = current_data.copy()
            return None

        # 反转数据 (根据实际接线调整).
        # current_data = [1 - d for d in current_data]

        self.data_ready = False
        return current_data

# 使用示例.
if __name__ == "__main__":
    # 初始化解码器.
    decoder = PT2272_Decoder(PT2272_Config())
    print("PT2272 解码器已启动")
    print("等待遥控信号...")

    # 地址码匹配示例 (根据实际地址设置).
    # 注意：PT2272地址码通过A0-A7引脚设置，需与发射端匹配.
    # 此处示例为默认地址 (悬空).

    while True:
        # 读取解码数据.
        data = decoder.read_data()
        if data is not None:
            # 转换为十六进制显示.
            data_hex = hex(int(''.join(map(str, data)), 2))
            print(f"接收数据: {data} (0x{data_hex[2:].upper()})")

            # 在此处添加业务逻辑.
            # 示例：控制LED.
            # if data == [1,0,1,0]:
            #     machine.Pin(2, machine.Pin.OUT).value(1)

        time.sleep(0.01)
