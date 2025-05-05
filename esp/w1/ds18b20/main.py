from machine import Pin
import onewire, ds18x20
import time

# 初始化单总线（GPIO8）
ow = onewire.OneWire(Pin(5))
ds = ds18x20.DS18X20(ow)

# 扫描总线上的 DS18B20 设备
roms = ds.scan()
print("Found DS18B20 devices:", [hex(int.from_bytes(rom, 'little')) for rom in roms])

# 温度采集函数
def read_temperature(index=0):
    try:
        ds.convert_temp()          # 启动温度转换
        time.sleep_ms(750)         # 等待转换完成（12-bit精度）
        return ds.read_temp(roms[index])  # 读取指定传感器温度
    except:
        return None

# 主循环
while True:
    for i, rom in enumerate(roms):
        temp = read_temperature(i)
        if temp is not None:
            print(f"Sensor {i}: {temp:.2f}°C")
        else:
            print(f"Sensor {i} read error")
    time.sleep(5)  # 每5秒采集一次
