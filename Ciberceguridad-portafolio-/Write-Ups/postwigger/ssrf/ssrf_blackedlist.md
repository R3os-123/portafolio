Nombre del Lab: SSRF with blacklist-based input filter
Tema: SSRF (Server-Side Request Forgery)

Dificultad: Media

Herramientas: curl

1. Reconocimiento
Se realiza una inspección del formulario de stock para identificar cómo se comunican el frontend y el backend.

Comando: curl -v [URL]

Observación: La aplicación utiliza el parámetro stockApi para realizar peticiones de stock a una API interna. Se identifica que existe una lista negra (blacklist) que bloquea palabras clave como 127.0.0.1, localhost y la cadena admin.

2. Identificación de la Vulnerabilidad
El servidor web no valida correctamente las redirecciones internas o las variaciones de codificación de los parámetros prohibidos.

Punto de inyección: Parámetro stockApi en el endpoint /product/stock.

Tipo de vulnerabilidad: SSRF con bypass de filtros mediante representación alternativa de IP y doble encoding.

3. Explotación
Para evadir la lista negra, se aplican dos técnicas de ofuscación:

IP abreviada: Se utiliza 127.1 en lugar de 127.0.0.1 para apuntar al localhost.

Doble URL Encoding: Se codifica la letra "a" de "admin" como %2561. El servidor decodifica una vez, obtiene %61dmin (pasando el filtro), y la función interna lo decodifica por segunda vez para ejecutar la ruta real.

Ejecución final (Eliminación de usuario):

Bash

curl -X POST -d "stockApi=http://127.1/%2561dmin/delete?username=wiener" \
"https://0a8a00e50455730d83a29c9c0050006f.web-security-academy.net/product/stock"
4. Resultado / Prueba de Concepto (PoC)
Acción final: Acceso exitoso al panel administrativo y eliminación del usuario wiener mediante una petición forjada desde el servidor.

Estado: Resuelto
