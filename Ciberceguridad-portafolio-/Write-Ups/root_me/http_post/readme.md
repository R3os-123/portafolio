🚩 Write-up: HTTP POST - RootMe

CTF: RootMe

Categoría: Web

Dificultad: Fácil

Fecha Resuelto: 30 de Diciembre, 2025

Herramientas: curl (Termux en Android)

Flag: H7tp_h4s_N0_s3Cr37S_F0r_y0U

🎯 Descripción del Reto

URL: http://challenge01.root-me.org/web-serveur/ch56/

Un juego llamado "RandGame: Human vs. Machine" donde debes generar un score mayor a 999,999 para ganar. El formulario web genera un score aleatorio entre 0 y 1,000,000 usando JavaScript.

Objetivo: Derrotar al sistema y obtener la flag.

🔍 Reconocimiento y Análisis

1. Inspección del Código HTML/JavaScript

```html
<form action="" method="post" onsubmit="document.getElementsByName('score')[0].value = Math.floor(Math.random() * 1000001)">
    <input type="hidden" name="score" value="-1" />
    <input type="submit" name="generate" value="Give a try!">
</form>
```

Observaciones clave:

· El formulario usa método POST
· El campo score está oculto (type="hidden")
· El valor de score se establece mediante JavaScript en el evento onsubmit
· JavaScript genera un número aleatorio: Math.floor(Math.random() * 1000001)
· Rango máximo: 0 a 1,000,000 (1,000,001 posibles valores)

2. Lógica del Juego

· Score a vencer: 999,999
· Score máximo posible vía JavaScript: 1,000,000
· Teóricamente, hay una probabilidad muy baja (1/1,000,001) de ganar

🧠 Identificación de la Vulnerabilidad

Problema de Seguridad

Validación solo del lado del cliente:

· El servidor confía en el valor que recibe del parámetro score
· No hay validación en el servidor para verificar si el score fue generado legítimamente
· El JavaScript se ejecuta en el navegador del usuario, por lo que puede ser omitido o manipulado

Vector de Ataque

Podemos enviar directamente una petición POST con un valor de score arbitrario, evitando completamente la validación JavaScript.

🚀 Explotación (Paso a Paso)

Paso 1: Entender la Estructura del POST

Los parámetros requeridos son:

· score: El valor numérico del puntaje
· generate: El valor del botón submit ("Give a try!")

Paso 2: Enviar Petición POST Manipulada

```bash
curl -X POST -d "score=10000000" -d "generate=Give a try!" "http://challenge01.root-me.org/web-serveur/ch56/"
```

Parámetros enviados:

· score=10000000: 10 millones (muy por encima del objetivo de 999,999)
· generate=Give a try!: Simula el click del botón

Paso 3: Resultado - ¡Éxito!

```html
<p>Wow, 10000000! How did you do that? :o</p>
<p>Flag to validate the challenge: <strong>H7tp_h4s_N0_s3Cr37S_F0r_y0U</strong></p>
```

💡 Explicación Técnica

¿Por qué funciona?

1. Arquitectura cliente-servidor defectuosa: La lógica del juego se implementa completamente en JavaScript del lado del cliente
2. Falta de validación del servidor: El servidor acepta cualquier valor de score sin verificar su autenticidad
3. Manipulación de peticiones HTTP: Al usar herramientas como curl, podemos enviar datos arbitrarios directamente al servidor, omitiendo las restricciones del frontend

Conceptos de Seguridad Aprendidos

· Never trust client-side validation: Las validaciones en JavaScript pueden ser fácilmente omitidas
· Input validation on server-side: Siempre validar datos en el servidor, independientemente de las validaciones del cliente
· Parameter tampering: Ataque básico pero efectivo que modifica parámetros HTTP

📚 Herramientas y Comandos

· curl: Para enviar peticiones HTTP personalizadas
· -X POST: Especifica el método HTTP POST
· -d "param=value": Envía datos en el cuerpo de la petición POST

🔐 Solución Alternativa

También podrías haber usado otros métodos:

Opción 1: Usar un proxy como Burp Suite (si estuviera disponible)

1. Interceptar la petición POST normal
2. Modificar el valor de score en el proxy
3. Reenviar la petición modificada

Opción 2: Deshabilitar JavaScript en el navegador

1. Desactivar JavaScript
2. Cambiar manualmente el valor del campo oculto score
3. Enviar el formulario

🏁 Flag

H7tp_h4s_N0_s3Cr37S_F0r_y0U

📝 Notas para Termux/Android

· Este reto demuestra que no necesitas herramientas complejas para vulnerabilidades web básicas
· curl es suficiente para la mayoría de ataques de manipulación de parámetros
· La simplicidad de Termux no es una limitación para retos web fundamentales

---

Write-up realizado completamente desde Termux en Android
