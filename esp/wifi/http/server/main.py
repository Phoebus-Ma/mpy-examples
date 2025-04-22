###
# Http Server example.
#
# License - MIT.
###

# Http 服务器，浏览器输入: 127.0.0.1:80
import socket

# 创建TCP套接字.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定地址和端口.
s.bind(("", 80))

# 开始监听.
s.listen(1)

print("等待客户端连接...")
conn, addr = s.accept()
print("客户端已连接:", addr)

# 发送HTTP响应.
conn.send(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hello from ESP32!</h1>")

# 关闭连接.
conn.close()
s.close()
