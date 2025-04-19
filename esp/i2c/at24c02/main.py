###
# AT24C02 eeprom i2c example.
#
# License - MIT.
###

from machine import I2C, Pin
import time


class AT24C02:
# {
    def __init__(self, i2c, i2c_addr=0x50):
        self.i2c = i2c
        self.addr = i2c_addr
        self.page_size = 8  # AT24C02 的页大小为8字节.
        
    def write_byte(self, mem_addr, data):
        # 写入单个字节.
        self.i2c.writeto_mem(self.addr, mem_addr, bytes([data]))
        time.sleep_ms(5)  # 等待写入完成.
        
    def read_byte(self, mem_addr):
        # 读取单个字节.
        return self.i2c.readfrom_mem(self.addr, mem_addr, 1)[0]
    
    def write_page(self, mem_addr, data):
        # 写入一页数据 (最多8字节).
        if len(data) > self.page_size:
            raise ValueError("Page size exceeded")
            
        self.i2c.writeto_mem(self.addr, mem_addr, data)
        time.sleep_ms(5)  # 等待写入完成.
        
    def write(self, mem_addr, data):
        # 通用写入函数 (自动处理分页).
        remaining = len(data)
        offset = 0
        
        while remaining > 0:
            # 计算当前页剩余空间.
            page_offset = mem_addr % self.page_size
            chunk_size = min(remaining, self.page_size - page_offset)
            
            self.write_page(mem_addr, data[offset:offset+chunk_size])
            
            mem_addr += chunk_size
            offset += chunk_size
            remaining -= chunk_size
            
    def read(self, mem_addr, length):
        # 读取数据.
        return self.i2c.readfrom_mem(self.addr, mem_addr, length)
# }

# 初始化I2C (ESP32默认引脚：SDA=21, SCL=22).
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# 扫描I2C设备 (验证连接).
devices = i2c.scan()
print("I2C设备地址:", [hex(addr) for addr in devices])

# 创建AT24C02实例.
eeprom = AT24C02(i2c)

# 测试写入和读取.
test_addr = 0x00  # 测试地址.
test_data = b"Hello AT24C02!"

# 写入数据.
print("写入数据:", test_data)
eeprom.write(test_addr, test_data)

# 读取数据.
read_data = eeprom.read(test_addr, len(test_data))
print("读取数据:", read_data)

# 验证数据.
if read_data == test_data:
    print("数据验证成功!")
else:
    print("数据验证失败!")
