import socket
import threading
import os
import paramiko

HOST = input("Enter server IP: ")
PORT = 6000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

room = input("Enter room name: ")
username = input("Enter username: ")

client.send((room + "\n").encode())
client.send((username + "\n").encode())

def receive():
    while True:
        try:
            msg = client.recv(4096)
            if not msg:
                break
            print(msg.decode(), end="")
        except:
            break

def send_file_ssh(filepath):
    if not os.path.exists(filepath):
        print("File not found")
        return

    host = input("SSH Server IP: ")
    username = input("SSH Username: ")
    password = input("SSH Password: ")

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(hostname=host, username=username, password=password)

        sftp = ssh.open_sftp()

        filename = os.path.basename(filepath)
        sftp.put(filepath, filename)

        print(f"[SSH] File sent: {filename}")

        sftp.close()
        ssh.close()

    except Exception as e:
        print(f"[SSH ERROR] {e}")

def send():
    while True:
        msg = input()

        if msg.startswith("/file"):
            try:
                _, filepath = msg.split(" ", 1)
            except:
                print("Usage: /file <path>")
                continue

            if os.path.exists(filepath):
                filename = os.path.basename(filepath)
                filesize = os.path.getsize(filepath)

                client.send(b"FILE\n")
                client.send((filename + "\n").encode())
                client.send((str(filesize) + "\n").encode())

                with open(filepath, "rb") as f:
                    while True:
                        chunk = f.read(4096)
                        if not chunk:
                            break
                        client.send(chunk)

                print("File sent!")
            else:
                print("File not found")

        elif msg.startswith("/sshfile"):
            try:
                _, filepath = msg.split(" ", 1)
                send_file_ssh(filepath)
            except:
                print("Usage: /sshfile <path>")

        else:
            client.send((msg + "\n").encode())

threading.Thread(target=receive, daemon=True).start()
threading.Thread(target=send, daemon=True).start()

while True:
    pass