###
# IR333 ir transfer example.
#
# License - MIT.
###

# 红外发射管，发送nec编码.
import machine
import utime

class IRSender:
    def __init__(self, pin):
        """
        初始化红外发射器.
        :param pin: GPIO引脚号 (需支持PWM输出).
        """
        self.ir_pin = machine.Pin(pin, machine.Pin.OUT)
        # 配置38KHz PWM (ESP32的PWM频率范围支持38KHz).
        self.pwm = machine.PWM(self.ir_pin, freq=38000, duty=512)  # 10位分辨率，50%占空比.
        self.pwm.duty(0)  # 初始关闭输出.

    def _pulse(self, duration_us):
        """
        生成指定时长的38KHz脉冲.
        :param duration_us: 脉冲持续时间 (微秒).
        """
        self.pwm.duty(512)  # 开启PWM.
        utime.sleep_us(duration_us)
        self.pwm.duty(0)    # 关闭PWM.

    def send_nec(self, address, command):
        """
        发送NEC协议红外信号.
        :param address: 8位地址码 (0x00-0xFF).
        :param command: 8位命令码 (0x00-0xFF).
        """
        # 发送引导码 (9ms脉冲 + 4.5ms间隔).
        self._pulse(9000)
        utime.sleep_us(4500)

        # 发送地址码及其反码.
        self._send_byte(address)
        self._send_byte(~address & 0xFF)

        # 发送命令码及其反码.
        self._send_byte(command)
        self._send_byte(~command & 0xFF)

        # 结束脉冲 (560us，可选).
        self._pulse(560)

    def _send_byte(self, byte):
        """
        发送8位数据 (含NEC协议格式).
        :param byte: 要发送的字节数据.
        """
        for i in range(8):
            bit = (byte >> (7 - i)) & 0x01  # 从高位到低位发送.
            # 发送560us脉冲.
            self._pulse(560)
            # 根据bit值发送不同间隔.
            if bit:
                utime.sleep_us(1690)  # 逻辑1：560us脉冲 + 1690us间隔.
            else:
                utime.sleep_us(560)   # 逻辑0：560us脉冲 + 560us间隔.

# 使用示例.
if __name__ == "__main__":
    ir = IRSender(5)  # 使用GPIO4作为红外发射引脚.
    
    while True:
        # 示例：发送地址0x00，命令0xFF.
        ir.send_nec(0x00, 0xFF)
        utime.sleep(1)  # 每秒发送一次.
        
        # 示例：发送地址0xFF，命令0x00.
        ir.send_nec(0xFF, 0x00)
        utime.sleep(1)
