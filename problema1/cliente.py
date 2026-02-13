#!/usr/bin/env python3
"""
Problema 1: Sockets básicos - Cliente
Objetivo: Crear un cliente TCP que se conecte a un servidor e intercambie mensajes básicos
"""

import socket

HOST = "localhost"
PORT = 9000

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

cliente.sendall(b"Mundo!")
respuesta = cliente.recv(1024)
print(f"Respuesta: {respuesta}")

cliente.close()



# : Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)

# : Conectar el socket al servidor en la dirección y puerto especificados

# : Enviar datos al servidor (convertidos a bytes)
# sendall() asegura que todos los datos sean enviados

# : Recibir datos del servidor (hasta 1024 bytes)

# : Decodificar e imprimir los datos recibidos

# : Cerrar la conexión con el servidor

