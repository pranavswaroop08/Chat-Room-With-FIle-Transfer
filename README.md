# Chat-Room-With-FIle-Transfer
Multi-Protocol Chat & File Transfer
System
A comprehensive collection of Python scripts for TCP, SSL/TLS, and SSH
communications.

Overview
This project implements a modular communication system featuring two primary
architectures: a standard TCP-based room chat with file transfer capabilities, and a
secure SSL-encrypted chat system with latency tracking. It also includes utility scripts
for SSH-based file transfers and security certificate management.
Project Structure
server.py - Standard TCP
A multi-threaded TCP server that supports chat rooms and direct file uploads. Files
are saved locally with a server_ prefix.
client.py - Standard TCP + SSH

A client supporting room-based chat, standard file transfer (via /file ), and SSH-
based secure file transfer (via /sshfile using Paramiko).

ssl_server.py - SSL/TLS
A secure server utilizing Python's ssl module. It loads cert.pem and key.pem to
establish an encrypted TLS channel on port 7000.
ssl_client.py - SSL/TLS
An encrypted client that connects to the SSL server. It includes built-in latency
monitoring for every message sent.
cert.pem & key.pem - Security
Self-signed X.509 certificate and private key used for the SSL/TLS server.

Installation & Prerequisites
Ensure you have Python 3.x installed. The following libraries are required for the SSH
functionality:
pip install paramiko

Usage Guide
1. Standard TCP Chat (with File Transfer)
Start the server: python server.py
Start the client: python client.py
Enter the Server IP, Room Name, and Username.
Commands:
Type normal messages to chat in the room.
/file <path> : Upload a file to the server.
/sshfile <path> : Upload a file to a remote server using SSH/SFTP.

2. Secure SSL Chat
Start the SSL server: python ssl_server.py (Ensure cert.pem and
key.pem are in the same directory).
Start the SSL client: python ssl_client.py
The client will display the RTT (Round Trip Time) for each message sent in
milliseconds.

Security Configuration

Note: The provided ssl_client.py uses ssl.CERT_NONE and
check_hostname = False for development purposes. For production
environments, ensure proper certificate validation.
Certificate Details
The included cert.pem is configured for localhost and was issued in Bangalore,
Karnataka, India by "CNProject".
