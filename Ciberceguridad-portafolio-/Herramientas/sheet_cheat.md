#[obtener token csrf]

-------------------

URL=https://0a8d00d3046c7bb2845b2c58000c00f8.web-security-academy.net
# 1. Obtener página y guardar cookies EN LA MISMA sesión
curl -s "$URL/login" -c cookies.txt -o temp.html

# 2. Extraer CSRF token DEL MISMO HTML obtenido
CSRF_TOKEN=$(grep -o 'csrf" value="[^"]*' temp.html | cut -d'"' -f3)
echo "CSRF Token actual: $CSRF_TOKEN"

# 3. Hacer login con las cookies y token correctos
curl -v \
  -b cookies.txt \
  -c cookies.txt \
  -d "csrf=$CSRF_TOKEN" \
  -d "username=wiener" \
  -d "password=peter" \
  -L \
  "$URL/login"

# Limpiar
rm -f temp.html

-------------------
