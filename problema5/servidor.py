import socket
import os
import hashlib
import threading

HOST = '0.0.0.0'
PORT = 9001
BUFFER_SIZE = 4096
BASE_DIR = "storage"

os.makedirs(BASE_DIR, exist_ok=True)


def safe_path(filename):
    return os.path.abspath(os.path.join(BASE_DIR, os.path.basename(filename)))


def calculate_checksum(path):
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(BUFFER_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()


def read_line(conn):
    data = b""
    while not data.endswith(b"\n"):
        chunk = conn.recv(1)
        if not chunk:
            break
        data += chunk
    return data.decode().strip()


def handle_client(conn, addr):
    print(f"Conexion desde {addr}")
    try:
        command_line = read_line(conn)
        parts = command_line.split()

        if not parts:
            return

        command = parts[0]

        # ================= UPLOAD =================
        if command == "UPLOAD":
            filename = parts[1]
            filesize = int(parts[2])
            filepath = safe_path(filename)

            with open(filepath, 'wb') as f:
                received = 0
                while received < filesize:
                    chunk = conn.recv(min(BUFFER_SIZE, filesize - received))
                    if not chunk:
                        break
                    f.write(chunk)
                    received += len(chunk)

            checksum_line = read_line(conn)
            _, client_checksum = checksum_line.split()

            server_checksum = calculate_checksum(filepath)

            if client_checksum == server_checksum:
                conn.sendall(b"OK\n")
            else:
                conn.sendall(b"ERROR Checksum mismatch\n")

        # ================= DOWNLOAD =================
        elif command == "DOWNLOAD":
            filename = parts[1]
            filepath = safe_path(filename)

            if not os.path.exists(filepath):
                conn.sendall(b"ERROR File not found\n")
                return

            filesize = os.path.getsize(filepath)
            conn.sendall(f"OK {filesize}\n".encode())

            with open(filepath, 'rb') as f:
                while chunk := f.read(BUFFER_SIZE):
                    conn.sendall(chunk)

            checksum = calculate_checksum(filepath)
            conn.sendall(f"CHECKSUM {checksum}\n".encode())

        # ================= LIST =================
        elif command == "LIST":
            conn.sendall(b"OK\n")
            for file in os.listdir(BASE_DIR):
                conn.sendall(f"{file}\n".encode())
            conn.sendall(b"END\n")

        else:
            conn.sendall(b"ERROR Unknown command\n")

    except Exception as e:
        print("Error:", e)

    finally:
        conn.close()


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}")

        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()


if __name__ == "__main__":
    start_server()
