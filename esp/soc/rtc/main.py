###
# ESP MCU internal rtc example.
#
# License - MIT.
###

# ESP MCU内部rtc.
import time
from machine import RTC

# 初始化RTC对象.
rtc = RTC()

# 设置时间 (首次使用需要设置).
# rtc.datetime((2025, 3, 1, 12, 34, 56, 0, None)).

def get_rtc_time():
    # 读取RTC时间 (返回元组：(年, 月, 日, 时, 分, 秒, 毫秒, 周几)).
    return rtc.datetime()

# 格式化时间输出.
def format_time(dt):
    return "{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}.{:03d}".format(
        dt[0], dt[1], dt[2], dt[3], dt[4], dt[5], dt[6]
    )

# 主循环示例.
while True:
    current_time = get_rtc_time()
    print("RTC时间:", format_time(current_time))
    time.sleep(1)
