Write-up: HTTP - Open Redirect (Root-Me)
1. 📝 Descripción
Este reto consiste en una página de "Redes Sociales" que redirige al usuario a sitios externos (Facebook, Twitter, Slack) mediante el paso de una URL por parámetro. Sin embargo, el sistema intenta proteger esta funcionalidad mediante una firma criptográfica (parámetro h).

2. 🔍 Fase de Reconocimiento
Al inspeccionar los enlaces de la página principal, observamos la siguiente estructura de URL: ?url=https://facebook.com&h=a023cfbf5f1c39bdf8407f28b60cd134

Análisis de los parámetros:
url: El destino de la redirección.

h: Una cadena de 32 caracteres hexadecimales.

Al intentar modificar el parámetro url por otro sitio (ej. google.com), el servidor responde con el mensaje: Incorrect hash!

3. 🛠️ Análisis de la Vulnerabilidad
El uso de una cadena hexadecimal de 32 caracteres sugiere fuertemente el uso del algoritmo MD5. Para verificar si existe un "Salt" (clave secreta) o si es un MD5 plano, realizamos una prueba en la terminal:

Bash

echo -n "https://facebook.com" | md5sum
# Resultado: a023cfbf5f1c39bdf8407f28b60cd134
Conclusión: El servidor es vulnerable porque el mecanismo de integridad es predecible. No utiliza una clave secreta para firmar las URLs; simplemente calcula el MD5 del texto plano del parámetro url.

4. 🚀 Explotación (Exploit)
Para superar el reto, debemos forzar una redirección a un dominio que no esté en la lista original. Aunque el servidor usa JavaScript para la redirección final, el flag se revela cuando el sistema detecta un "Open Redirect" exitoso.

Paso 1: Elegir una URL y generar el Hash
Elegimos, por ejemplo, https://www.google.com.

Bash

echo -n "https://www.google.com" | md5sum
# Resultado: ed076287532e86365e841e92bfc50d8c
Paso 2: Construir la URL de ataque
Combinamos nuestra URL con su respectivo hash generado: http://challenge01.root-me.org/web-serveur/ch52/?url=https://www.google.com&h=ed076287532e86365e841e92bfc50d8c

Paso 3: Ejecución y obtención del Flag
Al acceder a la URL, el servidor valida que el hash coincide con la URL proporcionada. En lugar de simplemente redirigir, el sistema de Root-Me detecta la manipulación y entrega el flag en el código fuente de la página:

HTML

<p>Well done! The flag is: R3d1r3ct_M3_If_U_C4n</p>
<script>document.location = 'https://www.google.com';</script>
5. 🛡️ Mitigación
Para prevenir ataques de Open Redirect, se recomienda:

Implementar una Lista Blanca (Allowlist): Solo permitir redirecciones a dominios internos o socios de confianza previamente definidos.

Redirección por Índices: Usar identificadores (ej. ?id=1) que apunten a una base de datos de URLs en el servidor, evitando que el usuario controle el destino directamente.

Firmas con Salt: Si se usa hashing para integridad, añadir una clave secreta en el servidor para que los atacantes no puedan generar firmas válidas: md5($secret_salt . $url).
