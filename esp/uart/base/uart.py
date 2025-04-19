
import machine
import utime

# 初始化UART对象
# 使用UART2，波特率为115200，数据位为8，停止位为1，无校验位
# TX引脚为GPIO12，RX引脚为GPIO13
uart = machine.UART(2, baudrate=115200, bits=8, parity=None, stop=1, tx=5, rx=4)

# 发送数据函数
def send_data(data):
    uart.write(data + '\n')  # 发送数据并添加换行符
    print("Sent:", data)

# 接收数据函数
def receive_data():
    if uart.any():  # 检查是否有数据可读
        data = uart.readline()  # 读取一行数据
        print("Received:", data.decode().strip())  # 解码并去除换行符后打印

# 主循环
while True:
    send_data("Hello, UART!")  # 发送数据
    receive_data()  # 接收数据
    utime.sleep(1)  # 等待1秒
