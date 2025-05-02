###
# WiFi Client (STA) example.
#
# License - MIT.
###

import network


wifi_ssid = 'your_wifi_ssid'
wifi_pw   = 'your_wifi_password'

# 初始化WiFi接口
wlan = network.WLAN(network.STA_IF)

# 激活接口
wlan.active(True)

# 连接到WiFi网络
wlan.connect(wifi_ssid, wifi_pw)

# 等待连接成功
while not wlan.isconnected():
    pass

print("IP地址:", wlan.ifconfig()[0])
