import socket
import ssl
import threading

HOST = "0.0.0.0"
PORT = 7000

clients = []

def handle_client(conn):
    username = conn.recv(1024).decode().strip()
    clients.append(conn)

    while True:
        try:
            msg = conn.recv(4096)
            if not msg:
                break

            full_msg = f"[{username}] {msg.decode()}"

            for client in clients:
                try:
                    client.send(full_msg.encode())
                except:
                    pass

        except:
            break

    clients.remove(conn)
    conn.close()

def start_ssl_server():
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print("SSL Server running on port 7000...")

    while True:
        client_socket, addr = server.accept()
        conn = context.wrap_socket(client_socket, server_side=True)
        threading.Thread(target=handle_client, args=(conn,)).start()

start_ssl_server()