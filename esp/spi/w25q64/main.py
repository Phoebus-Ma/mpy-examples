###
# W25Q64 spi example.
#
# License - MIT.
###

# W25Q64是一个有64Mbit，即8MB容量的Flash，SPI接口.
# SCK  - GPIO18.
# MOSI - GPIO23.
# MISO - GPIO19.
# CS   - GPIO5.
from machine import Pin, SPI
import w25q64


# 初始化SPI总线.
spi = SPI(1, sck = Pin(18), mosi = Pin(23), miso = Pin(19))

# 初始化W25Q64的CS引脚.
cs = Pin(5, Pin.OUT)

# 创建W25Q64对象.
w25q64_obj = w25q64.W25Q64(spi, cs)

# 读取W25Q64的ID.
jedec_id = w25q64_obj.read_id()
print("W25Q64 ID:", jedec_id)

# 写入数据到W25Q64.
write_address = 0x000000
write_data    = b"Hello, W25Q64!"
w25q64_obj.page_program(write_address, write_data)
print("数据写入完成")

# 从W25Q64读取数据.
read_address = write_address
read_length  = len(write_data)
read_data    = w25q64_obj.read_data(read_address, read_length)
print("读取的数据:", read_data.decode('utf-8'))
