import socket
import threading
import json
import os

HOST = '0.0.0.0'
PORT = 9000
ROOMS_FILE = 'rooms.json'

clients = {}          # socket -> {"username": str, "room": str}
rooms = {}            # room_name -> set(socket)
lock = threading.Lock()


# ---------------- PERSISTENCIA ----------------

def load_rooms():
    global rooms
    if os.path.exists(ROOMS_FILE):
        with open(ROOMS_FILE, 'r') as f:
            data = json.load(f)
            for room in data:
                rooms[room] = set()
    else:
        rooms["general"] = set()


def save_rooms():
    with open(ROOMS_FILE, 'w') as f:
        json.dump(list(rooms.keys()), f)


# ---------------- UTILIDADES ----------------

def broadcast(room, message, exclude_client=None):
    for client in rooms.get(room, []):
        if client != exclude_client:
            try:
                client.sendall(message.encode())
            except:
                pass


def list_rooms():
    return ", ".join(rooms.keys())


def list_users(room):
    return ", ".join([clients[c]["username"] for c in rooms[room]])


# ---------------- MANEJO CLIENTE ----------------

def handle_client(client):
    try:
        client.sendall("Ingrese su nombre de usuario: ".encode())
        username = client.recv(1024).decode().strip()

        with lock:
            clients[client] = {"username": username, "room": "general"}
            rooms["general"].add(client)

        client.sendall(f"Bienvenido {username}! Sala actual: general\n".encode())
        broadcast("general", f"{username} se ha unido a la sala\n", client)

        while True:
            msg = client.recv(1024).decode().strip()
            if not msg:
                break

            if msg.startswith("/"):
                handle_command(client, msg)
            else:
                with lock:
                    room = clients[client]["room"]
                    broadcast(room, f"{username}: {msg}\n", client)

    except:
        pass
    finally:
        disconnect(client)


def handle_command(client, msg):
    parts = msg.split()
    command = parts[0].lower()

    with lock:
        username = clients[client]["username"]
        current_room = clients[client]["room"]

        if command == "/create" and len(parts) > 1:
            room_name = parts[1]
            if room_name not in rooms:
                rooms[room_name] = set()
                save_rooms()
                client.sendall(f"Sala '{room_name}' creada.\n".encode())
            else:
                client.sendall("La sala ya existe.\n".encode())

        elif command == "/join" and len(parts) > 1:
            room_name = parts[1]
            if room_name in rooms:
                rooms[current_room].remove(client)
                broadcast(current_room, f"{username} salió de la sala\n")

                rooms[room_name].add(client)
                clients[client]["room"] = room_name

                client.sendall(f"Te uniste a '{room_name}'\n".encode())
                broadcast(room_name, f"{username} se unió a la sala\n", client)
            else:
                client.sendall("La sala no existe.\n".encode())

        elif command == "/leave":
            if current_room != "general":
                rooms[current_room].remove(client)
                rooms["general"].add(client)
                clients[client]["room"] = "general"
                client.sendall("Volviste a la sala general\n".encode())
            else:
                client.sendall("Ya estás en general.\n".encode())

        elif command == "/rooms":
            client.sendall(f"Salas disponibles: {list_rooms()}\n".encode())

        elif command == "/users":
            client.sendall(f"Usuarios en sala: {list_users(current_room)}\n".encode())

        elif command == "/msg" and len(parts) >= 3:
            target_user = parts[1]
            private_msg = " ".join(parts[2:])
            for c in clients:
                if clients[c]["username"] == target_user:
                    c.sendall(f"[Privado] {username}: {private_msg}\n".encode())
                    return
            client.sendall("Usuario no encontrado.\n".encode())

        else:
            client.sendall("Comando no válido.\n".encode())


def disconnect(client):
    with lock:
        if client in clients:
            username = clients[client]["username"]
            room = clients[client]["room"]
            rooms[room].remove(client)
            broadcast(room, f"{username} se desconectó\n", client)
            del clients[client]

    client.close()


# ---------------- MAIN ----------------

def main():
    load_rooms()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor iniciado en puerto {PORT}")

    while True:
        client, addr = server.accept()
        print(f"Conexión desde {addr}")
        threading.Thread(target=handle_client, args=(client,), daemon=True).start()


if __name__ == "__main__":
    main()
