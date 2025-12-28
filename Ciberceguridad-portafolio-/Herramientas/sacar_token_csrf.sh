
# 1. Configura aquí la URL base de tu lab
URL="https://0a570061049ba1f1804f58f800c60096.web-security-academy.net/feedback" 

echo -e "\e[1;34m[*] Conectando a ctOS Central...\e[0m"

# 2. Extraer el CSRF y guardar la sesión en cookies.txt
# Buscamos la línea que contiene 'name="csrf"' y extraemos el valor entre comillas
CSRF=$(curl -s -c cookies.txt "$URL/feedback" | grep 'name="csrf"' | sed -E 's/.*value="([^"]+)".*/\1/')

if [ -z "$CSRF" ]; then
    echo -e "\e[1;31m[!] ERROR: No se pudo encontrar el token CSRF.\e[0m"
else
    echo -e "\e[1;32m[+] TOKEN CAPTURADO: $CSRF\e[0m"
    echo -e "\e[1;34m[*] SESIÓN GUARDADA: cookies.txt\e[0m"
    echo ""
    echo -e "\e[1;37mYa puedes ejecutar tu ataque usando la variable \e[1;32m\$CSRF\e[0m"
    echo "------------------------------------------------------------"
fi
