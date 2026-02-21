import socket
import threading
import json
import sys
import time

HOST = 'localhost'
PORT = int(sys.argv[1])  # puerto pasado por parámetro

# Otros servidores backend para replicación
OTHER_SERVERS = [
    ('localhost', 5001),
    ('localhost', 5002),
    ('localhost', 5003)
]

data_store = {}
lock = threading.Lock()


def replicate_to_others(key, value):
    for host, port in OTHER_SERVERS:
        if port != PORT:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((host, port))
                message = json.dumps({
                    "type": "replicate",
                    "key": key,
                    "value": value
                })
                s.send(message.encode())
                s.close()
            except:
                pass


def handle_client(conn):
    global data_store
    try:
        data = conn.recv(1024).decode()
        request = json.loads(data)

        if request["type"] == "set":
            key = request["key"]
            value = request["value"]

            with lock:
                data_store[key] = value

            replicate_to_others(key, value)

            conn.send(b"OK")

        elif request["type"] == "get":
            key = request["key"]
            value = data_store.get(key, None)
            conn.send(json.dumps(value).encode())

        elif request["type"] == "replicate":
            with lock:
                data_store[request["key"]] = request["value"]

        elif request["type"] == "health":
            conn.send(b"ALIVE")

    except:
        pass

    conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Backend iniciado en puerto {PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()


if __name__ == "__main__":
    start_server()