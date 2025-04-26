###
# MPU6050 example.
#
# License - MIT.
###

'''
SCL - GPIO6.
SDA - GPIO5.
AD0 - GND.

AD0低电平, i2c地址是0x68.
AD0高电平, i2c地址是0x69.
'''
import time
from machine import I2C, Pin

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        # 唤醒并初始化MPU6050.
        self.i2c.writeto(self.addr, bytearray([0x6B, 0x00]))  # 退出睡眠模式.

    def read_all(self):
        # 一次性读取加速度、温度、陀螺仪数据 (共14字节).
        data = self.i2c.readfrom_mem(self.addr, 0x3B, 14)

        # 解析加速度 (0x3B-0x40).
        accel = [
            self._convert(data[0], data[1]),  # X轴.
            self._convert(data[2], data[3]),  # Y轴.
            self._convert(data[4], data[5])   # Z轴.
        ]

        # 解析温度 (0x41-0x42).
        temp_raw = self._convert(data[6], data[7])
        temp = temp_raw / 340.0 + 36.53

        # 解析陀螺仪 (0x43-0x48).
        gyro = [
            self._convert(data[8], data[9]),   # X轴.
            self._convert(data[10], data[11]), # Y轴.
            self._convert(data[12], data[13])  # Z轴.
        ]

        return accel, gyro, temp

    def _convert(self, high, low):
        # 将两个字节转换为有符号整数.
        value = (high << 8) | low
        return value - 65536 if value > 32767 else value

# 初始化I2C (确保引脚正确).
i2c = I2C(0, scl=Pin(6), sda=Pin(5), freq=400000)
mpu = MPU6050(i2c)

while True:
    accel, gyro, temp = mpu.read_all()
    print(f"温度: {temp:.2f}°C, Accel: {accel}, Gyro: {gyro}")
    time.sleep(1)
