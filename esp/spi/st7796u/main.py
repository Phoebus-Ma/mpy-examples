###
# ST7796U LCD spi example.
#
# License - MIT.
###

# ESP32-C6 ST7796U 完整驱动示例 (SPI接口).
# 分辨率: 320x480.
# 测试环境: ESP32-C6 MicroPython v1.20+.

import machine
import time
from machine import Pin, SPI

# 硬件连接配置 (根据实际接线修改).
class ST7796U_Config:
    SPI_HOST = 1       # 使用VSPI (HSPI=0, VSPI=1).
    SPI_FREQ = 40_000_000  # 最大40MHz.
    
    # 引脚定义 (ESP32-C6 DevKitC)
    PIN_SCK  = 18      # GPIO18 (VSPI SCK).
    PIN_SDA  = 23      # GPIO23 (VSPI MOSI).
    PIN_DC   = 6      # GPIO16 (Data/Command).
    PIN_RST  = 7      # GPIO17 (Reset).
    PIN_CS   = 5       # GPIO5  (Chip Select).
    PIN_BL   = 4       # GPIO4  (Backlight - 可选).

# 颜色定义 (RGB565格式).
class Color:
    RED     = 0xF800
    GREEN   = 0x07E0
    BLUE    = 0x001F
    WHITE   = 0xFFFF
    BLACK   = 0x0000
    YELLOW  = 0xFFE0
    CYAN    = 0x07FF
    MAGENTA = 0xF81F

class ST7796U_Driver:
    def __init__(self, config):
        self.config = config
        self.width = 320
        self.height = 480
        
        # 初始化SPI总线.
        self.spi = SPI(
            self.config.SPI_HOST,
            baudrate=self.config.SPI_FREQ,
            sck=Pin(self.config.PIN_SCK),
            mosi=Pin(self.config.PIN_SDA),
            miso=None,
            polarity=0,
            phase=0
        )
        
        # 初始化控制引脚.
        self.cs   = Pin(self.config.PIN_CS,   Pin.OUT, value=1)
        self.dc   = Pin(self.config.PIN_DC,   Pin.OUT, value=0)
        self.rst  = Pin(self.config.PIN_RST,  Pin.OUT, value=0)
        self.bl   = Pin(self.config.PIN_BL,   Pin.OUT, value=1) if hasattr(self.config, 'PIN_BL') else None
        
        # 硬件复位.
        self.reset()
        
        # 执行完整初始化序列.
        self._init_sequence()

    def reset(self):
        """执行硬件复位"""
        self.rst(1)
        time.sleep_ms(50)
        self.rst(0)
        time.sleep_ms(150)
        self.rst(1)
        time.sleep_ms(150)

    def _write_cmd(self, cmd):
        """发送命令"""
        self.cs(0)
        self.dc(0)
        self.spi.write(bytes([cmd]))
        self.cs(1)

    def _write_data(self, data):
        """发送数据"""
        self.cs(0)
        self.dc(1)
        self.spi.write(data)
        self.cs(1)

    def _init_sequence(self):
        """ST7796U完整初始化序列 (根据官方数据手册)"""
        init_commands = [
            # Power Setting.
            (0xB2, b'\x0C\x0C\x00\x33\x33', 1),   # PORCH设置.
            (0xB7, b'\x35', 1),                   # 电源控制1.
            (0xBB, b'\x19', 1),                   # VCOM设置.
            (0xC0, b'\x2C', 1),                   # LCM驱动.
            (0xC2, b'\x01', 1),                   # VDV/VRH使能.
            (0xC3, b'\x13', 1),                   # VDV设置.
            (0xC4, b'\x20', 1),                   # VRH设置.
            (0xC6, b'\x0F', 1),                   # 帧速率控制.
            (0xD0, b'\xA4\xA1', 1),               # 电源优化.
            (0xE0, b'\xD0\x04\x0D\x11\x13\x2B\x3F\x54\x4C\x08\x0E\x09\x27\x2A', 2),  # 正极伽马.
            (0xE1, b'\xF0\x09\x0B\x06\x08\x0A\x3F\x38\x4F\x0A\x0F\x05\x32\x35', 2),  # 负极伽马.
            
            # Display Setting.
            (0x36, b'\x08', 1),   # 内存访问控制 (RGB顺序).
            (0x3A, b'\x55', 1),   # 接口像素格式 (16bit/pixel).
            
            # Sleep Out & Display On.
            (0x11, None, 120),    # 退出睡眠模式.
            (0x29, None, 100)     # 开启显示.
        ]

        for cmd, data, delay in init_commands:
            self._write_cmd(cmd)
            if data:
                self._write_data(data)
            if delay:
                time.sleep_ms(delay)

    def set_window(self, x0, y0, x1, y1):
        """设置绘制窗口"""
        self._write_cmd(0x2A)  # Column Address Set.
        self._write_data(bytes([x0 >> 8, x0 & 0xFF, x1 >> 8, x1 & 0xFF]))
        self._write_cmd(0x2B)  # Row Address Set.
        self._write_data(bytes([y0 >> 8, y0 & 0xFF, y1 >> 8, y1 & 0xFF]))
        self._write_cmd(0x2C)  # Memory Write.

    '''
    在MicroPython下, ESP32-C6的RAM空间不够一次发送一帧完整数据, 此处分段发送数据.
    '''
    def fill_rect(self, x, y, w, h, color, chunk_size=4092):
        """优化版矩形填充 (支持大尺寸绘制)"""
        x1 = x + w - 1
        y1 = y + h - 1
        self.set_window(x, y, x1, y1)
        
        # 创建单像素颜色模板 (2字节).
        color_data = bytes([color >> 8, color & 0xFF])
        
        # 计算每行像素数和总行数.
        pixels_per_row = w
        total_rows = h
        
        # 分块发送数据.
        for row in range(total_rows):
            # 计算当前行数据偏移.
            offset = row * pixels_per_row * 2
            
            # 分块发送 (每次发送chunk_size字节).
            for i in range(0, pixels_per_row * 2, chunk_size):
                # 计算当前块大小 (不能超过剩余数据).
                current_chunk = min(chunk_size, pixels_per_row * 2 - i)
                
                # 发送数据块 (自动重复颜色数据).
                self._write_data(color_data * (current_chunk // 2))

    def draw_pixel(self, x, y, color):
        """绘制单个像素"""
        self.set_window(x, y, x, y)
        self._write_data(bytes([color >> 8, color & 0xFF]))

    def fill_screen(self, color):
        """全屏填充"""
        self.fill_rect(0, 0, self.width, self.height, color)

# 使用示例.
if __name__ == "__main__":
    display = ST7796U_Driver(ST7796U_Config())
    
    # 测试大尺寸填充 (320x480全屏).
    display.fill_screen(Color.BLACK)
    display.fill_rect(0, 0, 320, 480, Color.BLUE)
    
    # 绘制测试图案 (不再需要注释掉).
    display.fill_rect(50, 50, 220, 100, Color.RED)
    display.fill_rect(50, 200, 220, 100, Color.GREEN)
    
    # 保持显示.
    while True:
        time.sleep(1)
