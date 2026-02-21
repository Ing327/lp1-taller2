# Problema 9: Sistema Distribuido (Coordinación entre servidores)

**Conceptos clave**:

- Múltiples servidores coordinados
- Balanceador de carga simple
- Replicación de datos
- Tolerancia a fallos básica

**Requerimientos**:

- Registro de servidores backend
- Health checks entre servidores
- Distribución de clientes
- Sincronización de datos







Sistema Distribuido en Python
Descripción

Este proyecto implementa un sistema distribuido básico en Python que incluye:

Múltiples servidores backend coordinados

Balanceador de carga simple (Round Robin)

Replicación de datos entre servidores

Health checks automáticos

Tolerancia básica a fallos

El sistema permite distribuir clientes entre varios servidores y mantener los datos sincronizados entre ellos.

Componentes del sistema

El proyecto está compuesto por tres archivos principales:

backend_server.py
Servidor que almacena datos en memoria y replica la información a los otros servidores.

load_balancer.py
Distribuye las solicitudes de los clientes entre los servidores activos.

client.py
Cliente de prueba para enviar solicitudes al sistema.

Arquitectura

Cliente → Load Balancer → Servidores Backend (5001, 5002, 5003)

El cliente se conecta al balanceador de carga (puerto 4000).
El balanceador redirige la solicitud a uno de los servidores backend disponibles.
Los servidores replican los datos entre ellos.

Cómo ejecutar el sistema
1. Abrir el proyecto

Abrir la carpeta del proyecto en Visual Studio Code.

2. Abrir cinco terminales

Ir a Terminal → New Terminal y abrir cinco terminales.

3. Iniciar los servidores backend

En cada terminal ejecutar:

Terminal 1:

python backend_server.py 5001

Terminal 2:

python backend_server.py 5002

Terminal 3:

python backend_server.py 5003

Cada uno mostrará:

Backend iniciado en puerto XXXX
4. Iniciar el Load Balancer

En otra terminal:

python load_balancer.py

Mostrará:

Load Balancer iniciado en puerto 4000
5. Iniciar el Cliente

En la última terminal:

python client.py
Uso del sistema
Guardar un valor

Escribir:

set

Luego ingresar:

Key: nombre
Value: Gustavo

El sistema responderá:

OK
Consultar un valor

Escribir:

get

Luego:

Key: nombre

El sistema devolverá el valor almacenado.



Funcionamiento interno

El balanceador utiliza Round Robin para distribuir las solicitudes.

Cada vez que se ejecuta un set, el servidor replica el dato a los demás backends.

El balanceador realiza verificaciones periódicas (health checks).

Si un servidor se detiene, el sistema continúa funcionando con los servidores activos.

Prueba de tolerancia a fallos

Ejecutar todo el sistema.

Detener uno de los servidores backend (Ctrl + C).

El cliente seguirá funcionando.

El balanceador dejará de enviar tráfico al servidor detenido.