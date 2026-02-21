import socket
import threading
import sys

BUFFER_SIZE = 4096

def log(message):
    print(f"[LOG] {message}")

def handle_client(client_socket):
    try:
        request = client_socket.recv(BUFFER_SIZE)
        if not request:
            client_socket.close()
            return

        first_line = request.split(b'\n')[0]
        method, path, version = first_line.split()

        # ==============================
        # MANEJO DE HTTPS (CONNECT)
        # ==============================
        if method == b'CONNECT':
            host_port = path.decode()
            host, port = host_port.split(':')
            port = int(port)

            log(f"HTTPS CONNECT a {host}:{port}")

            # Conectar al servidor destino
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((host, port))

            # Responder OK al cliente
            client_socket.send(b"HTTP/1.1 200 Connection Established\r\n\r\n")

            # Reenvío bidireccional
            threading.Thread(target=forward, args=(client_socket, remote_socket)).start()
            threading.Thread(target=forward, args=(remote_socket, client_socket)).start()
            return

        # ==============================
        # MANEJO DE HTTP NORMAL
        # ==============================
        else:
            headers = request.decode().split("\r\n")
            host = None
            port = 80

            for header in headers:
                if header.lower().startswith("host:"):
                    host = header.split(":")[1].strip()
                    break

            if not host:
                client_socket.close()
                return

            log(f"HTTP {method.decode()} -> {host}")

            # Modificar headers (ejemplo)
            request = request.replace(b"User-Agent:", b"User-Agent: ProxyServer ")

            # Conectar al servidor destino
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((host, port))

            remote_socket.send(request)

            while True:
                data = remote_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                client_socket.send(data)

            remote_socket.close()
            client_socket.close()

    except Exception as e:
        log(f"Error: {e}")
        client_socket.close()


def forward(source, destination):
    try:
        while True:
            data = source.recv(BUFFER_SIZE)
            if not data:
                break
            destination.send(data)
    except:
        pass
    finally:
        source.close()
        destination.close()


def start_proxy(host='0.0.0.0', port=8888):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(100)
    log(f"Proxy escuchando en {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        log(f"Conexión desde {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()


if __name__ == "__main__":
    start_proxy()