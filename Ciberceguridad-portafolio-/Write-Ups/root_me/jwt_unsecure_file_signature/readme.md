Root-Me CTF: JWT - Public Key / Path Traversal
Flag
RM{Uns3cUr3_f1l3_H4ndl1nG!!}

 Descripción del Reto
El reto consistía en obtener privilegios de administrador accediendo al endpoint /admin. Se identificó que la aplicación gestiona la autenticación mediante JSON Web Tokens (JWT) y presenta una vulnerabilidad de Insecure File Handling al procesar el parámetro kid (Key ID).

🛠️ Herramientas Utilizadas
Navegador / Curl: Para interceptar y enviar peticiones.

JWT.io: Para la decodificación, manipulación y firma manual del token.

 Proceso de Explotación
1. Identificación del Vector de Ataque
Al analizar el token de sesión, se observó que el encabezado incluía un campo kid:

JSON

{
  "alg": "HS256",
  "kid": "b901bb24-700b-4cc6-a71a-cb207ab61313",
  "typ": "JWT"
}
Se descubrió que el servidor utilizaba este valor como una ruta relativa para cargar la clave secreta desde el sistema de archivos. Al introducir caracteres de control, el servidor reveló que intentaba abrir archivos dentro de una carpeta llamada keys/.

2. Bypass de Path Traversal
Se localizó un recurso estático público en el servidor: /static/challs/htmllecture.html.

Para obligar al servidor a usar este archivo como clave de firma, se utilizó un payload de Path Traversal avanzado: ....//. Este payload permitió evadir filtros de seguridad comunes que bloquean el clásico ../, logrando retroceder directorios hasta alcanzar la carpeta de archivos estáticos.

3. Firma Manual con JWT.io
Para generar el token malicioso, se siguieron estos pasos en JWT.io:

Header: Se cambió el kid por ....//static/challs/htmllecture.html.

Payload: Se modificó el campo "user" a "admin".

Verify Signature: * Se copió el contenido íntegro del archivo htmllecture.html.

Se pegó en el campo "secret" de JWT.io (asegurando que el algoritmo fuera HS256).

Esto generó una firma válida basada en un "secreto" que el servidor posee localmente y nosotros conocemos públicamente.

4. Ejecución
Se envió el token resultante mediante la cookie session:

Bash

curl -v http://challenge01.root-me.org:59081/admin \
     -b "session=eyJhbGciOiJIUzI1NiIsImtpZCI6Ii4uLi4vL3N0YXRpYy9jaGFsbHMvaHRtbGxlY3R1cmUuaHRtbCIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYWRtaW4iLCJpYXQiOjE3Njc5OTYwNjl9.PfX2_BlS0M-FhJIlRB34d1QnYWzeGCS7eiuRchu4kzc"
El servidor, al recibir el token, leyó su propio archivo htmllecture.html, generó el hash y, al coincidir con nuestra firma, concedió acceso de administrador.

 Conclusión
Este ataque demuestra que la seguridad de JWT no solo reside en la complejidad de la clave, sino en la integridad del proceso de recuperación de la misma. El uso de KID Manipulation permite a un atacante definir su propia "fuente de verdad" para la autenticación.
