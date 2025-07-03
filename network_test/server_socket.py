# server_socket.py
import socket

HOST = "0.0.0.0"
PORT = 8002

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"✅ Listening on {HOST}:{PORT}...")

    conn, addr = s.accept()
    with conn:
        print(f"🔌 Connection from {addr}")
        data = conn.recv(1024)
        if not data:
            print("⚠️ Received empty data! Client may have closed the connection.")
        else:
            print(f"📩 Received: {data.decode()}")
            conn.sendall(b"Hello from server!")
            print("📤 Response sent.")