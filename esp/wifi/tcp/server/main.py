
import socket

# 创建TCP套接字
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定地址和端口
s.bind(("", 8080))

# 开始监听
s.listen(1)

print("等待客户端连接...")
conn, addr = s.accept()
print("客户端已连接:", addr)

# 接收数据
while True:
    data = conn.recv(1024)
    if not data:
        break
    print("收到数据:", data.decode())
    conn.send("Echo: " + data.decode())

# 关闭连接
conn.close()
s.close()
