import socket

HOST = 'localhost'
PORT = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

while True:
    message = client.recv(1024).decode()
    print(message)

    data = input()
    client.sendall(data.encode())