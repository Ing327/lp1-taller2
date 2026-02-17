#!/usr/bin/env python3
"""
Problema 4: Servidor HTTP básico - Cliente
Objetivo: Crear un cliente HTTP que realice una petición GET a un servidor web local
"""
import socket
import http.client


HOST = 'localhost'
PORT = 9000

# : Definir la dirección y puerto del servidor HTTP

cliente = http.client.HTTPConnection(HOST, PORT)
cliente.request('GET', '/')

respuesta = cliente.getresponse()
datos = respuesta.read().decode()

print(datos)

cliente.close()
# : Crear una conexión HTTP con el servidor
# HTTPConnection permite establecer conexiones HTTP con servidores

# : Realizar una petición GET al path raíz ('/')
# request() envía la petición HTTP al servidor
# Primer parámetro: método HTTP (GET, POST, etc.)
# Segundo parámetro: path del recurso solicitado

# : Obtener la respuesta del servidor
# getresponse() devuelve un objeto HTTPResponse con los datos de la respuesta

# : Leer el contenido de la respuesta
# read() devuelve el cuerpo de la respuesta en bytes

# : Decodificar los datos de bytes a string e imprimirlos
# decode() convierte los bytes a string usando UTF-8 por defecto

# : Cerrar la conexión con el servidor

