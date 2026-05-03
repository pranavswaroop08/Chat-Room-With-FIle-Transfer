import socket
import threading

HOST = "0.0.0.0"
PORT = 6000

rooms = {}

def handle_client(conn, addr):
    room = conn.recv(1024).decode().strip()
    username = conn.recv(1024).decode().strip()

    if room not in rooms:
        rooms[room] = []

    rooms[room].append(conn)
    print(f"{username} joined {room}")

    while True:
        try:
            data = conn.recv(4096)
            if not data:
                break

            if data.startswith(b"FILE"):
                filename = conn.recv(1024).decode().strip()
                filesize = int(conn.recv(1024).decode().strip())

                with open("server_" + filename, "wb") as f:
                    remaining = filesize
                    while remaining > 0:
                        chunk = conn.recv(min(4096, remaining))
                        if not chunk:
                            break
                        f.write(chunk)
                        remaining -= len(chunk)

                msg = f"[{username}] sent file: {filename}\n"

            else:
                msg = f"[{username}] {data.decode().strip()}\n"

            for client in rooms[room]:
                try:
                    client.send(msg.encode())
                except:
                    pass

        except:
            break

    rooms[room].remove(conn)
    conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("Server running on port 6000...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

start_server()