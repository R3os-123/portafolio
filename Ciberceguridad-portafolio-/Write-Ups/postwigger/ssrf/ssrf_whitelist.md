
---

# Nombre del Lab: SSRF with whitelist-based input filter

**Tema:** SSRF (Server-Side Request Forgery) / Bypass de Whitelist

**Dificultad:** Alta

**Herramientas:** curl

---

### 1. Reconocimiento

Se analiza el parámetro `stockApi` y se descubre que, a diferencia de labs anteriores, este solo acepta URLs que apunten al dominio permitido: `stock.weliketoshop.net`. Cualquier intento de usar una IP directa o `localhost` es rechazado por una **Whitelist** (Lista blanca).

* **Comando inicial:** `curl -v [URL]`
* **Observación:** El servidor valida que el hostname de la URL proporcionada sea el oficial.

### 2. Identificación de la Vulnerabilidad

La vulnerabilidad reside en una discrepancia entre cómo el componente de seguridad (filtro) y el componente de red (librería de peticiones) procesan la URL. Se aprovecha el soporte de **credenciales embebidas** y el manejo de **fragmentos (#)**.

* **Punto de inyección:** Parámetro `stockApi`.
* **Concepto de Bypass:** Uso de `@` para simular credenciales y `#` para truncar la URL de cara al servidor interno, pero manteniendo el dominio permitido para el filtro de seguridad.

### 3. Explotación

Para engañar al servidor, se construye una URL compleja que utiliza **Double URL Encoding** para proteger el carácter especial `#`:

1. **Credenciales:** `http://localhost@stock.weliketoshop.net` (El filtro ve el dominio permitido).
2. **Fragmento:** Se inserta un `#` entre el objetivo y el dominio permitido: `http://localhost#@stock.weliketoshop.net`.
3. **Doble Encoding:** El carácter `#` se convierte en `%23` (simple) y luego en `%2523` (doble) para evitar que el servidor frontal lo decodifique prematuramente.

**Ejecución final (Eliminación de usuario):**

```bash
curl -X POST -d "stockApi=http://localhost:80%2523@stock.weliketoshop.net/admin/delete?username=carlos" \
"https://[LAB-ID].web-security-academy.net/product/stock"

```

### 4. Resultado / Prueba de Concepto (PoC)

* **Acción final:** El servidor interno decodifica el `%2523` como `#`, interpretando que la conexión debe hacerse a `localhost` y que el resto (`@stock.weliketoshop.net`) es solo un fragmento a ignorar. Esto permite acceder al panel `/admin` y eliminar al usuario `carlos`.
* **Estado:** Resuelto.

