import socket
import os
import hashlib

HOST = 'localhost'
PORT = 9001
BUFFER_SIZE = 4096


def calculate_checksum(path):
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(BUFFER_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()


def read_line(sock):
    data = b""
    while not data.endswith(b"\n"):
        chunk = sock.recv(1)
        if not chunk:
            break
        data += chunk
    return data.decode().strip()


def upload(filepath):
    if not os.path.exists(filepath):
        print("Archivo no encontrado")
        return

    filesize = os.path.getsize(filepath)
    filename = os.path.basename(filepath)
    checksum = calculate_checksum(filepath)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        s.sendall(f"UPLOAD {filename} {filesize}\n".encode())

        with open(filepath, 'rb') as f:
            while chunk := f.read(BUFFER_SIZE):
                s.sendall(chunk)

        s.sendall(f"CHECKSUM {checksum}\n".encode())

        response = read_line(s)
        print(response)


def download(filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        s.sendall(f"DOWNLOAD {filename}\n".encode())

        response = read_line(s)

        if response.startswith("ERROR"):
            print(response)
            return

        _, filesize = response.split()
        filesize = int(filesize)

        with open(filename, 'wb') as f:
            received = 0
            while received < filesize:
                chunk = s.recv(min(BUFFER_SIZE, filesize - received))
                if not chunk:
                    break
                f.write(chunk)
                received += len(chunk)

        checksum_line = read_line(s)
        _, server_checksum = checksum_line.split()

        local_checksum = calculate_checksum(filename)

        if local_checksum == server_checksum:
            print("Descarga correcta")
        else:
            print("Error de integridad")


def list_files():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"LIST\n")

        while True:
            line = read_line(s)
            print(line)
            if line == "END":
                break


if __name__ == "__main__":
    while True:
        cmd = input("Comando (upload/download/list/exit): ").strip()

        if cmd == "upload":
            path = input("Ruta del archivo: ")
            upload(path)

        elif cmd == "download":
            name = input("Nombre del archivo: ")
            download(name)

        elif cmd == "list":
            list_files()

        elif cmd == "exit":
            break
