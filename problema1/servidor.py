#!/usr/bin/env python3
"""
Problema 1: Sockets básicos - Servidor
Objetivo: Crear un servidor TCP que acepte una conexión y intercambie mensajes básicos
"""

import socket

#: Definir la dirección y puerto del servidor
HOST = "localhost"
PORT = 9000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORT))
servidor.listen()
print("el servidor esta a la espera de conexiones ...")

cliente, direccion =servidor.accept()
print(f"un cliente se conecto desde la direccion {direccion}")

datos = cliente.recv(1024)
cliente.sendall(b"Hola! " + datos) # ojo! debe ser binario, no cadena
cliente.close()

#: Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)

# : Enlazar el socket a la dirección y puerto especificados

# : Poner el socket en modo escucha
# El parámetro define el número máximo de conexiones en cola



# : Aceptar una conexión entrante
# accept() bloquea hasta que llega una conexión
# conn: nuevo socket para comunicarse con el cliente
# addr: dirección y puerto del cliente



# : Recibir datos del cliente (hasta 1024 bytes)
 
# : Enviar respuesta al cliente (convertida a bytes)
# sendall() asegura que todos los datos sean enviados

# : Cerrar la conexión con el cliente

