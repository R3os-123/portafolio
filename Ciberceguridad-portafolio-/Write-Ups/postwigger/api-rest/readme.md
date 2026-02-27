

## Vulnerabilidad: REST Path Pollution

La aplicación es vulnerable a la inyección de secuencias de navegación de directorios (`../`) y caracteres de truncado (`#`) en el parámetro `username`. Esto permite redirigir las peticiones internas del backend hacia endpoints no autorizados.

---

##  Proceso de Explotación

### 1. Identificación del Vector (Path Traversal)

Se confirmó que el backend construye rutas dinámicas basadas en el input. Al inyectar `administrator/../carlos`, el servidor devolvió el perfil de Carlos, validando que el input se concatena directamente en la URL de la API interna.

### 2. Bypass de Restricciones (API Versioning)

Al intentar extraer el token en la versión actual (v2) mediante `administrator/field/passwordResetToken%23`, el servidor respondió con un error de seguridad:

> *"This version of API only supports the email field for security reasons"*

Se aplicó un **Versioning Attack** retrocediendo en la estructura de directorios para forzar el uso de la **v1**, la cual carece de esta protección.

### 3. Extracción del Token (Exfiltración)

Para obtener un token válido, se disparó primero una solicitud legítima de reset para `administrator` y luego se ejecutó el payload de extracción:

```bash
# Payload maestro de extracción en Termux
curl -b cookies.txt \
  -d "csrf=[TOKEN]&username=../../v1/users/administrator/field/passwordResetToken%23" \
  "https://[LAB_ID].web-security-academy.net/forgot-password"

```

**Respuesta obtenida:**

```json
{
  "type": "passwordResetToken",
  "result": "l3nzvfcdv78jt04ybfw97fdj4hqjkzcx"
}

```

---

## 🏁 Post-Explotación

1. **Acceso:** Se utilizó el token robado directamente en el parámetro identificado en el JS: `?passwordResetToken=l3nzvfcdv78jt04ybfw97fdj4hqjkzcx`.
2. **Acción:** Cambio de contraseña de `administrator`.
3. **Objetivo:** Acceso al Admin Panel y eliminación del usuario `carlos`.

---

##  Notas Técnicas para el Futuro

* **Truncado:** El uso de `%23` (`#`) es vital para ignorar el resto de la ruta que el backend intenta añadir (ej. `/reset-password`).
* **API Discovery:** Siempre que una API mencione "esta versión", es obligatorio buscar `/v1/`, `/v0/` o `/beta/`.
* **Secuencia de Disparo:** Los tokens son volátiles; si el resultado es `null`, hay que solicitar un reset justo antes de lanzar el exploit.

---


