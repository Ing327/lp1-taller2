import socket
import json

HOST = 'localhost'
PORT = 4000

def send_request(request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(json.dumps(request).encode())
    response = s.recv(1024)
    print("Respuesta:", response.decode())
    s.close()


while True:
    command = input("Comando (set/get): ")

    if command == "set":
        key = input("Key: ")
        value = input("Value: ")
        send_request({
            "type": "set",
            "key": key,
            "value": value
        })

    elif command == "get":
        key = input("Key: ")
        send_request({
            "type": "get",
            "key": key
        })