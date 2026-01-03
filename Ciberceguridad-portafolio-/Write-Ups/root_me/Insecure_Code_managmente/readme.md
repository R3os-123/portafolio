
# Root-me Write-up: Insecure Code Management (.git Exposure)

## 1. Fase de Reconocimiento y Descubrimiento

El reto comenzó con un **fuzzing de directorios** para identificar archivos o carpetas ocultas. Se detectó la existencia del directorio `.git/`, lo cual es una vulnerabilidad crítica de **Information Exposure**.

## 2. Exfiltración del Repositorio

Para reconstruir el historial de desarrollo en local, se utilizó `wget`. Este comando permite "clonar" el repositorio descargando los objetos de Git directamente desde el servidor web.

```bash
wget -r -np -nH --cut-dirs=3 -R "index.html*" http://challenge01.root-me.org/web-serveur/ch61/.git/

```

### Análisis de banderas `wget`:

* **`-r` (recursive):** Descarga todo el árbol de directorios de la carpeta `.git`.
* **`-np` (no-parent):** Asegura que la descarga no suba a directorios superiores fuera del reto.
* **`-nH` (no-host-directories):** Evita la creación de carpetas con el nombre del dominio del reto.
* **`--cut-dirs=3`:** Elimina los niveles de directorios innecesarios (`web-serveur/ch61/`) para guardar el contenido directamente en la carpeta actual.
* **`-R "index.html*"`:** Rechaza los archivos `index.html` autogenerados por el servidor para el listado de directorios, manteniendo la integridad de los objetos de Git.

## 3. Análisis Forense del Historial (Git Logs)

Una vez descargado, inspeccionamos el historial cronológico de cambios utilizando el log de Git:

```bash
git log --oneline

```

**Salida obtenida:**

```text
c0b4661 (HEAD -> master) blue team want sha256!!!!!!!!!
550880c renamed app name  <-- COMMIT DE INTERÉS
a8673b2 changed password  <-- PUNTO DE INFLEXIÓN
1572c85 secure auth with md5
5e0e146 Initial commit for the new HR database access

```

### Interpretación de los Commits:

El historial revela una narrativa de seguridad fallida. John (el desarrollador) intentó securizar la aplicación en el commit `1572c85` usando MD5, y luego cambió la contraseña en `a8673b2`. Sin embargo, los cambios en Git son **inmutables**; los datos antiguos permanecen en la base de datos de objetos.

## 4. Recuperación de la Flag (Inspección de Objetos)

Para obtener la contraseña, consultamos el estado del archivo `config.php` en el commit `550880c` (justo después del cambio de password).

```bash
git show 550880c40814a9d0c39ad3485f7620b1dbce0de8:config.php

```

### Análisis del comando `git show`:

* **`git show`:** Este comando reconstruye un objeto de la base de datos de Git y lo muestra por pantalla.
* **`550880c...`:** Es el hash SHA-1 del commit. Indica el punto exacto en el tiempo que queremos ver.
* **`:` (separador):** Indica que queremos ver un archivo específico dentro de ese commit.
* **`config.php`:** El archivo de configuración que contenía las credenciales.

**Contenido recuperado:**

```php
<?php
    $username = "admin";
    $password = "s3cureP@ssw0rd"; // FLAG ENCONTRADA

```

## 5. Mitigación y Buenas Prácticas

1. **Bloqueo de archivos ocultos:** Configurar el servidor (Nginx/Apache) para denegar el acceso a cualquier archivo o carpeta que comience con un punto (`.*`).
2. **Higiene de Secretos:** Nunca incluir contraseñas, tokens o llaves API en el control de versiones. Se deben usar variables de entorno o gestores de secretos.
3. **Limpieza de Historial:** Si se sube un secreto por error, se debe rotar la credencial inmediatamente y purgar el historial de Git usando herramientas como `git-filter-repo` o `BFG Repo-Cleaner`.
