#!/usr/bin/env python3
"""
Problema 3: Chat simple con múltiples clientes - Servidor
Objetivo: Crear un servidor de chat que maneje múltiples clientes simultáneamente usando threads
"""

import socket
import threading

# : Definir la dirección y puerto del servidor

HOST = "localhost"
PORT = 9000

# Lista para mantener todos los sockets de clientes conectados
clientes = []

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()
print("Servidor 'chat' esta a la espera de conexiones ...")



def atender_cliente(cliente, nombre):
    """
    Maneja la comunicación con un cliente específico en un hilo separado.
    
    Args:
        client_socket: Socket del cliente
        client_name: Nombre del cliente
    """
    while True:
        try:
            # : Recibir datos del cliente (hasta 1024 bytes)
            mensaje = cliente.recv(1024)
            if not mensaje:
                break
            # Si no se reciben datos, el cliente se desconectó
            
                
            # Formatear el mensaje con el nombre del cliente
            print(f"{nombre}: {mensaje.decode()}")
            broadcast(mensaje.decode(), cliente)
            
            # Imprimir el mensaje en el servidor
           
            
            # : Retransmitir el mensaje a todos los clientes excepto al remitente

            
        except ConnectionResetError:
            # Manejar desconexión inesperada del cliente
            clientes.remove(cliente)
            cliente.close()
            break

def broadcast(mensaje, emisor):
    
    """
    Envía un mensaje a todos los clientes conectados excepto al remitente.
    
    Args:
        message: Mensaje a enviar (string)
        sender_socket: Socket del cliente que envió el mensaje original
    """
    for cliente in clientes:
        if cliente != emisor:
            cliente.send(mensaje.encode())
            # : Enviar el mensaje codificado a bytes a cada cliente


# : Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)

# : Enlazar el socket a la dirección y puerto especificados

# : Poner el socket en modo escucha
# El parámetro define el número máximo de conexiones en cola

print("Servidor chat a la espera de conexiones ...")

# Bucle principal para aceptar conexiones entrantes
while True:
    # : Aceptar una conexión entrante
    # client: nuevo socket para comunicarse con el cliente
    # addr: dirección y puerto del cliente
    
    cliente, direccion = servidor.accept()
    
    print(f"Conexión realizada desde la IP {direccion}")
    
    nombre = cliente.recv(1024).decode()
    clientes.append(cliente)
    
    # : Recibir el nombre del cliente (hasta 1024 bytes) y decodificarlo
    
    # : Agregar el socket del cliente a la lista de clientes conectados
    
    # Enviar mensaje de confirmación de conexión al cliente
    cliente.send("ya estás conectado!".encode())
    
    # Notificar a todos los clientes que un nuevo usuario se unió al chat
    broadcast(f"{nombre} se ha unido al 'Chat'", cliente)
    hilo_cliente =threading.Thread(target=atender_cliente, args=(cliente, nombre))
    hilo_cliente.start()
    # : Crear e iniciar un hilo para manejar la comunicación con este cliente
    # target: función que se ejecutará en el hilo
    # args: argumentos que se pasarán a la función
    
    

