Pirate - Machine Readme (HTB)
Nombre: Pirate

Dificultad: Easy

Sistema Operativo: Linux (Ubuntu)

1. Fase de Reconocimiento (Enumeración)
Puertos Abiertos:

21/TCP: FTP (vsftpd 3.0.3)

22/TCP: SSH (OpenSSH 8.2p1)

80/TCP: HTTP (Gunicorn - Python Web Server)

Hallazgo Clave: El servidor web corre sobre Gunicorn, lo que indica que la aplicación está escrita en Python.

2. Explotación de la Vulnerabilidad Web (IDOR / LFI)
La página permitía descargar archivos .pcap basados en un ID de usuario (parámetro vulnerable).

Técnica: Al cambiar el ID a 0 (Insecure Direct Object Reference - IDOR), se obtuvo acceso a una captura de tráfico privilegiada que no estaba destinada al usuario guest.

3. Análisis Forense (Tráfico de Red)
Archivo: archivo.pcap

Herramienta: termshark / tcpdump.

Descubrimiento: El tráfico capturaba una sesión de FTP en texto plano. Se interceptaron los comandos USER y PASS, revelando credenciales válidas.

4. Acceso Inicial (Footprinting)
Uso de las credenciales obtenidas para entrar vía SSH. Esto proporciona una shell estable como usuario de bajos privilegios.

5. Escalada de Privilegios (Privesc)
Enumeración Interna: Ejecución de linpeas.sh.

Vulnerabilidad: Se detectó que el binario de /usr/bin/python3 tenía el bit SUID activado (o Capabilities específicas como cap_setuid+ep).

Explotación: Inyección de código Python para manipular el ID de usuario del proceso (UID).

Python

import os
os.setuid(0)  # Cambia a root
os.system("/bin/bash") # Ejecuta shell como root
🏁 Flag Final
Ruta: /root/root.txt

💡 Lección aprendida:
Nunca se debe dar permisos SUID a lenguajes de programación o editores de texto (como Python, Perl, Vim o Nano), ya que permiten ejecutar comandos del sistema o manipular el UID, lo que equivale a entregar las llaves maestras del servidor.
