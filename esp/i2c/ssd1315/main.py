###
# SSD1315 oled i2c example.
#
# License - MIT.
###

# I2C OLED, 芯片使用ssd1315, 分辨率128x64..
# i2c地址0x3C.
# SCL - GPIO22.
# SDA - GPIO21.
from machine import I2C, Pin
import ssd1306


# 初始化I2C总线.
i2c = I2C(scl=Pin(22), sda=Pin(21))

# 初始化SSD1315显示屏.
width  = 128
height = 64
i2c_addr = 0x3C  # SSD1315的常见I2C地址.
oled = ssd1306.SSD1306_I2C(width, height, i2c, addr=i2c_addr)

# 清屏.
oled.fill(0)

# 在屏幕上显示"Hello World".
oled.text("Hello World", 0, 0)

# 更新显示.
oled.show()
