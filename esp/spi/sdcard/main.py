###
# SPI sdcard example.
#
# License - MIT.
###

import os
import sdcard
from machine import Pin, SPI

# 配置 SPI 引脚 (根据硬件调整)
spi = SPI(1, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
cs = Pin(5, Pin.OUT)

# 初始化 SD 卡
sd = sdcard.SDCard(spi, cs)

# 挂载文件系统
os.mount(sd, '/sd')

# 测试写入和读取
with open('/sd/hello.txt', 'w') as f:
    f.write('hello world.')

with open('/sd/hello.txt', 'r') as f:
    print(f.read())

# 卸载
os.umount('/sd')
