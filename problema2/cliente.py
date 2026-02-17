#!/usr/bin/env python3
"""
Problema 2: Comunicación bidireccional - Cliente
Objetivo: Crear un cliente TCP que envíe un mensaje al servidor y reciba la misma respuesta
"""

import socket

# : Definir la dirección y puerto del servidor

HOST = "localhost"
PORT = 9000

# Solicitar mensaje al usuario por consola
mensaje = input("Digite tu Mensaje: ")

# : Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

cliente.sendall(mensaje.encode())

# : Conectar el socket al servidor en la dirección y puerto especificados

# Mostrar mensaje que se va a enviar
print(f"Mensaje enviados: '{mensaje}'")

respuesta = cliente.recv(1024)
print(f"Respuesta del 'Echo': '{respuesta.decode()}'")

cliente.close()



# : Codificar el mensaje a bytes y enviarlo al servidor
# sendall() asegura que todos los datos sean enviados
# : Recibir datos del servidor (hasta 1024 bytes)
# Decodificar e imprimir los datos recibidos
# : Cerrar la conexión con el servidor