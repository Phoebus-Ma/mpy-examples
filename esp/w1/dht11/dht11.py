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
