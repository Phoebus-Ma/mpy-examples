from machine import Pin
import time

class DS1302:
    def __init__(self, clk, dio, cs):
        self.clk = clk
        self.dio = dio
        self.cs = cs
        self.clk.init(Pin.OUT)
        self.cs.init(Pin.OUT)

    def _dec2hex(self, dat):
        return (dat // 10) * 16 + (dat % 10)

    def _hex2dec(self, dat):
        return (dat // 16) * 10 + (dat % 16)

    def _write_byte(self, dat):
        self.dio.init(Pin.OUT)
        for i in range(8):
            self.dio.value((dat >> i) & 1)
            self.clk.value(1)
            self.clk.value(0)

    def _read_byte(self):
        d = 0
        self.dio.init(Pin.IN)
        for i in range(8):
            d = d | (self.dio.value() << i)
            self.clk.value(1)
            self.clk.value(0)
        return d

    def _get_reg(self, reg):
        self.cs.value(1)
        self._write_byte(reg)
        t = self._read_byte()
        self.cs.value(0)
        return t

    def _set_reg(self, reg, dat):
        self.cs.value(1)
        self._write_byte(reg)
        self._write_byte(dat)
        self.cs.value(0)

    def _wr(self, reg, dat):
        self._set_reg(0x8E, 0)
        self._set_reg(reg, dat)
        self._set_reg(0x8E, 0x80)

    def start(self):
        t = self._get_reg(0x80 + 1)
        self._wr(0x80, t & 0x7F)

    def stop(self):
        t = self._get_reg(0x80 + 1)
        self._wr(0x80, t | 0x80)

    def second(self, second=None):
        if second is None:
            return self._hex2dec(self._get_reg(0x80 + 1)) % 60
        else:
            self._wr(0x80, self._dec2hex(second % 60))

    def minute(self, minute=None):
        if minute is None:
            return self._hex2dec(self._get_reg(0x82 + 1))
        else:
            self._wr(0x82, self._dec2hex(minute % 60))

    def hour(self, hour=None):
        if hour is None:
            return self._hex2dec(self._get_reg(0x84 + 1))
        else:
            self._wr(0x84, self._dec2hex(hour % 24))

    def day(self, day=None):
        if day is None:
            return self._hex2dec(self._get_reg(0x86 + 1))
        else:
            self._wr(0x86, self._dec2hex(day % 32))

    def month(self, month=None):
        if month is None:
            return self._hex2dec(self._get_reg(0x88 + 1))
        else:
            self._wr(0x88, self._dec2hex(month % 13))

    def year(self, year=None):
        if year is None:
            return self._hex2dec(self._get_reg(0x8C + 1))
        else:
            self._wr(0x8C, self._dec2hex(year % 100))

    def weekday(self, weekday=None):
        if weekday is None:
            return self._hex2dec(self._get_reg(0x8A + 1)) % 8
        else:
            self._wr(0x8A, self._dec2hex(weekday % 8))

# 初始化DS1302对象
ds1302 = DS1302(clk=Pin(7), dio=Pin(6), cs=Pin(15))

# 设置时间（年，月，日，时，分，秒，星期）
ds1302.year(2025)    # 年（23表示2023年）
ds1302.month(3)    # 月
ds1302.day(1)      # 日
ds1302.hour(10)     # 时（24小时制）
ds1302.minute(0)    # 分
ds1302.second(0)    # 秒
ds1302.weekday(3)   # 星期（1-7，3表示星期三）

# 启动DS1302
ds1302.start()

# 主循环
while True:
    year = ds1302.year()
    mon  = ds1302.month()
    day  = ds1302.day()
    hour = ds1302.hour()
    mins = ds1302.minute()
    sec  = ds1302.second()
    week = ds1302.weekday()
    
    print(f'{year}-{mon}-{day} {hour}:{mins}:{sec} {week}')
    time.sleep(1)
