# client_socket.py
import socket
import time

HOST = "101.126.89.14"
PORT = 8002

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("✅ Connected to server, sending message...")
    s.sendall(b"Hello from local client!")
    time.sleep(0.5)  # 👈 给服务端一点时间进入 recv
    data = s.recv(1024)
    print(f"✅ Received from server: {data.decode()}")