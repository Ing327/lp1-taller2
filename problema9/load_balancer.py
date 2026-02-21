import socket
import threading
import json
import time

HOST = 'localhost'
PORT = 4000

BACKENDS = [
    ('localhost', 5001),
    ('localhost', 5002),
    ('localhost', 5003)
]

active_servers = BACKENDS.copy()
index = 0
lock = threading.Lock()


def health_check():
    global active_servers
    while True:
        new_active = []
        for host, port in BACKENDS:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((host, port))
                s.send(json.dumps({"type": "health"}).encode())
                response = s.recv(1024)
                if response == b"ALIVE":
                    new_active.append((host, port))
                s.close()
            except:
                pass

        with lock:
            active_servers = new_active

        time.sleep(3)


def get_next_server():
    global index
    with lock:
        if not active_servers:
            return None
        server = active_servers[index % len(active_servers)]
        index += 1
        return server


def handle_client(conn):
    server = get_next_server()
    if not server:
        conn.send(b"No hay servidores disponibles")
        conn.close()
        return

    try:
        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect(server)

        data = conn.recv(1024)
        backend_socket.send(data)

        response = backend_socket.recv(1024)
        conn.send(response)

        backend_socket.close()

    except:
        conn.send(b"Error en backend")

    conn.close()


def start_load_balancer():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("Load Balancer iniciado en puerto 4000")

    threading.Thread(target=health_check, daemon=True).start()

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()


if __name__ == "__main__":
    start_load_balancer()