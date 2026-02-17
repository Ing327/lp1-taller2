#!/usr/bin/env python3
"""
Problema 3: Chat simple con múltiples clientes - Cliente
Objetivo: Crear un cliente de chat que se conecte a un servidor y permita enviar/recibir mensajes en tiempo real
"""

import socket
import threading

HOST = 'localhost'
PORT = 9000

def recibir_mensajes():
    """
    Función ejecutada en un hilo separado para recibir mensajes del servidor
    de forma continua sin bloquear el hilo principal.
    """
    while True:
        # : Recibir mensajes del servidor (hasta 1024 bytes) y decodificarlos
         mensaje = cliente.recv(1024).decode()
        # Imprimir el mensaje recibido
         print(mensaje)
        

# Solicitar nombre de usuario al cliente
nombre = input("Cual es tu nombre:")

# : Crear un socket TCP/IP
# AF_INET: socket de familia IPv4
# SOCK_STREAM: socket de tipo TCP (orientado a conexión)

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))
cliente.send(nombre.encode())



# : Conectar el socket al servidor en la dirección y puerto especificados

# : Enviar el nombre del cliente al servidor (codificado a bytes)

# Crear y iniciar un hilo para recibir mensajes del servidor
# target: función que se ejecutará en el hilo
hilo_recibir = threading.Thread(target=recibir_mensajes)
hilo_recibir.start()

# Bucle principal en el hilo principal para enviar mensajes al servidor
while True:
    # Solicitar mensaje al usuario por consola
    mensaje = input("Mensaje: ")
    # : Codificar el mensaje a bytes y enviarlo al servidor
    cliente.send(mensaje.encode())
    

