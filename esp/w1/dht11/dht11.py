###
# DHT11 1-wire example.
#
# License - MIT.
###

# DHT11是一个温湿度传感器，采用1根线进行通信.
# 使用GPIO4端口进行通信.
import time
import dht
import machine


d = dht.DHT11(machine.Pin(4))

while True:
    d.measure()
    temp = d.temperature()
    humi = d.humidity()

    print(f'{temp}℃, {humi}%.')
    time.sleep(3)
