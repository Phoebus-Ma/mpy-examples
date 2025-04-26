###
# Read i2c address example.
#
# License - MIT.
###

# 读取i2c从设备的地址, 适合在不知道设备地址等情况.
from machine import I2C, Pin


# 初始化I2C总线，使用默认的SCL和SDA引脚.
i2c = I2C(scl=Pin(6), sda=Pin(5))

# 扫描I2C总线以检测连接的设备.
devices = i2c.scan()

# 打印检测到的设备地址.
if devices:
    print("Detect i2c address:")
    for device in devices:
        print(hex(device))
else:
    print("Not found i2c device.")
