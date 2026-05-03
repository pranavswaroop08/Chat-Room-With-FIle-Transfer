import socket
import ssl
import threading
import time

HOST = input("Enter SSL server IP: ")
PORT = 7000

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = context.wrap_socket(client, server_hostname=HOST)

client.connect((HOST, PORT))

username = input("Enter username: ")
client.send((username + "\n").encode())

latencies = []

def receive():
    while True:
        try:
            msg = client.recv(4096)
            if not msg:
                break
            print(msg.decode(), end="")
        except:
            break

def send():
    while True:
        msg = input()

        start = time.time()
        client.send((msg + "\n").encode())
        end = time.time()

        latency = (end - start) * 1000
        latencies.append(latency)
        print(f"[SSL Latency: {latency:.2f} ms]")

threading.Thread(target=receive, daemon=True).start()
threading.Thread(target=send, daemon=True).start()

while True:
    pass