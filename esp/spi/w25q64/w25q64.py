
# w25q64.py
from machine import SPI, Pin
from micropython import const

# 指令定义
W25X_WriteEnable = const(0x06)
W25X_ReadStatusReg = const(0x05)
W25X_PageProgram = const(0x02)
W25X_SectorErase = const(0x20)
W25X_ReadData = const(0x03)

class W25Q64:
    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self.read_id()  # 读取芯片ID以确认连接

    def read_id(self):
        self.cs.off()
        self.spi.write(bytearray([W25X_ReadStatusReg]))
        id = list(self.spi.read(1))[0]
        self.cs.on()
        return id

    def write_enable(self):
        self.cs.off()
        self.spi.write(bytearray([W25X_WriteEnable]))
        self.cs.on()

    def page_program(self, address, data):
        self.write_enable()
        self.cs.off()
        self.spi.write(bytearray([W25X_PageProgram]))
        self.spi.write(bytearray([ (address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF ]))
        self.spi.write(data)
        self.cs.on()
        self.wait_busy()

    def sector_erase(self, address):
        self.write_enable()
        self.cs.off()
        self.spi.write(bytearray([W25X_SectorErase]))
        self.spi.write(bytearray([ (address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF ]))
        self.cs.on()
        self.wait_busy()

    def read_data(self, address, length):
        self.cs.off()
        self.spi.write(bytearray([W25X_ReadData]))
        self.spi.write(bytearray([ (address >> 16) & 0xFF, (address >> 8) & 0xFF, address & 0xFF ]))
        data = self.spi.read(length)
        self.cs.on()
        return data

    def wait_busy(self):
        while True:
            self.cs.off()
            self.spi.write(bytearray([W25X_ReadStatusReg]))
            status = list(self.spi.read(1))[0]
            self.cs.on()
            if (status & 0x01) == 0:
                break
