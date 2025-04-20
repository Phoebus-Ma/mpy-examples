###
# WiFi Router (AP) example.
#
# License - MIT.
###

import network


AP_SSID = 'ESP32_AP'
AP_PW   = '12345678'

# 初始化WiFi接口
ap = network.WLAN(network.AP_IF)

# 配置AP
ap.config(essid=AP_SSID, password=AP_PW)

# 激活AP
ap.active(True)

print("AP Started, IP address: ", ap.ifconfig()[0])
