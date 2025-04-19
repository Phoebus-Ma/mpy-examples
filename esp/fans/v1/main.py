###
# Control fans web server.
#
# License - MIT.
###

# 功能如下:
# 1. 通过高低电平控制场效应管开关风扇;
# 2. 是一个WiFi STA模式的TCP服务器;
# 3. 有开和关两种状态, 且可以定义不同状态的持续时间;
# 4. 有一个json文件用于保存开关状态时长的配置;
# 5. 需要在全局变量中填入wifi名和密码;
# 6. 浏览器输入本服务器的ip地址, 就可以配置和运行;
# 7. 开机默认关闭风扇，需要通过步骤6开启.

import network
import socket
import time
import ujson
from machine import Pin, Timer

# 硬件配置.
LED_PIN = 2        # LED连接的GPIO引脚.
FAN_PIN = 15       # FAN连接的GPIO引脚.
CONFIG_FILE = "led_config.json"  # 配置文件路径.

# 初始化LED和Wi-Fi.
led = Pin(LED_PIN, Pin.OUT)
fan = Pin(FAN_PIN, Pin.OUT)
sta_if = network.WLAN(network.STA_IF)

# 全局变量.
current_mode = "control"  # 初始模式.
led_enabled = False       # LED循环状态.
blink_on_time = 1         # 默认亮的时间(秒).
blink_off_time = 1        # 默认灭的时间(秒).

wifi_name = ''            # WiFi名(改成实际的).
wifi_pw = ''              # WiFi密码(改成实际的).

#
# 文件系统操作.
#
def save_config():
    """保存配置到文件"""
    config = {
        "on_time": blink_on_time,
        "off_time": blink_off_time
    }
    with open(CONFIG_FILE, "w") as f:
        ujson.dump(config, f)

def load_config():
    """从文件加载配置"""
    global blink_on_time, blink_off_time
    try:
        with open(CONFIG_FILE, "r") as f:
            config = ujson.load(f)
            blink_on_time = config.get("on_time", 1)
            blink_off_time = config.get("off_time", 1)
    except:
        # print("使用默认配置")
        pass

#
# LED控制逻辑.
#
def led_blink(timer):
    """LED闪烁定时器回调"""
    global led, fan, blink_on_time, blink_off_time
    led.value(1)
    fan.value(1)
    time.sleep(blink_on_time)
    fan.value(0)
    led.value(0)
    time.sleep(blink_off_time)

# 创建硬件定时器.
blink_timer = Timer(0)
load_config()  # 启动时加载配置.

#
# Web服务器逻辑.
#
def generate_html():
    """生成动态HTML内容"""
    html = """<html>
<head>
    <title>ESP32 LED Control</title>
    <style>
        .mode-switch { margin: 20px; }
        .config-box { border: 1px solid #ccc; padding: 20px; margin: 10px; }
    </style>
</head>
<body>
    <div class="mode-switch">
        <a href="/?mode=control"><button>Control Model</button></a>
        <a href="/?mode=config"><button>Config Model</button></a>
    </div>"""

    if current_mode == "control":
        html += f"""
    <div class="config-box">
        <h2>Control Model</h2>
        <p>Current status: <strong>{'Running' if led_enabled else 'Stoped'}</strong></p>
        <p><a href="/?action=start"><button>Start</button></a></p>
        <p><a href="/?action=stop"><button>Stop</button></a></p>
    </div>"""
    else:
        html += f"""
    <div class="config-box">
        <h2>Config Model</h2>
        <form action="/?mode=config" method="post">
            <label>On time(s): 
                <input type="number" name="on_time" value="{blink_on_time}" step="0.1" min="0.1">
            </label><br>
            <label>Off time(s): 
                <input type="number" name="off_time" value="{blink_off_time}" step="0.1" min="0.1">
            </label><br>
            <input type="submit" value="Save">
        </form>
    </div>"""

    html += "</body></html>"
    return html

def handle_request(request):
    """处理HTTP请求"""
    global current_mode, led_enabled, blink_on_time, blink_off_time
    
    # 模式切换处理.
    if "mode=control" in request:
        current_mode = "control"
    elif "mode=config" in request:
        current_mode = "config"

    # 控制模式操作.
    if "action=start" in request:
        blink_timer.deinit()
        period = int((blink_on_time + blink_off_time) * 1000)
        blink_timer.init(period=period, mode=Timer.PERIODIC, callback=led_blink)
        led_enabled = True
    elif "action=stop" in request:
        blink_timer.deinit()
        fan.value(0)
        led.value(0)
        led_enabled = False

    # 配置模式操作.
    if request.startswith("POST") and "on_time" in request:
        params = request.split("\r\n\r\n")[1]
        pairs = params.split("&")
        config = {p.split("=")[0]: float(p.split("=")[1]) for p in pairs}
        blink_on_time = config.get("on_time", blink_on_time)
        blink_off_time = config.get("off_time", blink_off_time)
        save_config()  # 保存新配置.

#
# 主程序.
#
def main():
    # 连接Wi-Fi
    sta_if.active(True)
    sta_if.connect(wifi_name, wifi_pw)
    while not sta_if.isconnected():
        pass
    # print("IP地址:", sta_if.ifconfig()[0])

    # 创建TCP服务器.
    s = socket.socket()
    s.bind(("0.0.0.0", 80))
    s.listen(5)

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024).decode()
        
        if request:  # 过滤空请求.
            handle_request(request)
            
        # 发送响应.
        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: text/html\n")
        conn.send("Connection: close\n\n")
        conn.send(generate_html())
        conn.close()

if __name__ == "__main__":
    main()
