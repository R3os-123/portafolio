#!/bin/bash

# ============================================
# Script: csrf-token-extractor.sh
# Descripción: Extrae tokens CSRF de formularios web
# Uso: ./csrf-token-extractor.sh https://ejemplo.com
# ============================================

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 1. Verificar que se proporcionó URL
if [ -z "$1" ]; then
    echo -e "${RED}[!] ERROR: Debes proporcionar una URL${NC}"
    echo -e "${YELLOW}Uso: $0 https://ejemplo.com${NC}"
    exit 1
fi

URL="$1"
COOKIE_FILE="cookies.txt"

echo -e "${BLUE}[*] Conectando a: $URL${NC}"

# 2. Realizar petición y guardar cookies (sin verbose)
#    -s: silent (sin progress bar)
#    -L: seguir redirects
#    -c: guardar cookies
RESPONSE=$(curl -s -L -c "$COOKIE_FILE" "$URL")

# 3. Verificar si curl tuvo éxito
if [ $? -ne 0 ]; then
    echo -e "${RED}[!] ERROR: No se pudo conectar a $URL${NC}"
    exit 1
fi

# 4. Buscar token CSRF en múltiples formatos comunes
#    - grep -o: solo muestra la parte que coincide
#    - Primero intentamos con comillas dobles
CSRF=$(echo "$RESPONSE" | grep -o 'name="csrf"[^>]*value="[^"]*"' | sed 's/.*value="\([^"]*\)".*/\1/')

# 5. Si no encontró, intentar con comillas simples
if [ -z "$CSRF" ]; then
    CSRF=$(echo "$RESPONSE" | grep -o "name='csrf'[^>]*value='[^']*'" | sed "s/.*value='\([^']*\)'.*/\1/")
fi

# 6. Si aún no encontró, buscar por input type="hidden"
if [ -z "$CSRF" ]; then
    CSRF=$(echo "$RESPONSE" | grep -o '<input[^>]*type="hidden"[^>]*name="csrf"[^>]*>' | sed 's/.*value="\([^"]*\)".*/\1/')
fi

# 7. Si aún no encontró, buscar cualquier input con name que contenga "csrf"
if [ -z "$CSRF" ]; then
    CSRF=$(echo "$RESPONSE" | grep -i 'name="[^"]*csrf[^"]*"' | sed 's/.*value="\([^"]*\)".*/\1/' | head -1)
fi

# 8. Mostrar resultados
if [ -z "$CSRF" ]; then
    echo -e "${RED}[!] No se encontró ningún token CSRF${NC}"
    echo -e "${YELLOW}[*] Posibles causas:${NC}"
    echo -e "    - El sitio no usa CSRF"
    echo -e "    - El token tiene otro nombre (ej: _token, authenticity_token)"
    echo -e "    - Necesitas autenticarte primero"
    echo -e "${YELLOW}[*] Cookies guardadas en: $COOKIE_FILE${NC}"
    
    # Mostrar nombres de cookies capturadas
    if [ -f "$COOKIE_FILE" ] && [ -s "$COOKIE_FILE" ]; then
        echo -e "${BLUE}[*] Cookies encontradas:${NC}"
        awk '!/^#/ {print $6 "=" $7}' "$COOKIE_FILE"
    fi
else
    echo -e "${GREEN}[+] TOKEN CSRF ENCONTRADO: $CSRF${NC}"
    echo -e "${BLUE}[*] Cookies guardadas en: $COOKIE_FILE${NC}"
    echo ""
    echo -e "${YELLOW}================================================${NC}"
    echo -e "Ya puedes usar el token en tu ataque:"
    echo -e "  Variable: \$${GREEN}CSRF${NC}"
    echo -e "  Valor: ${GREEN}$CSRF${NC}"
    echo -e "${YELLOW}================================================${NC}"
    
    # Mostrar ejemplo de uso con curl
    echo -e "\n${BLUE}[*] Ejemplo de uso con curl:${NC}"
    echo -e "curl -b $COOKIE_FILE -d \"csrf=$CSRF&username=admin&password=test\" $URL/login"
fi

# 9. Opcional: Buscar otros tokens comunes
echo -e "\n${BLUE}[*] Buscando otros tokens posibles...${NC}"
OTHER_TOKENS=$(echo "$RESPONSE" | grep -Eo 'name="[^"]*(token|Token|TOKEN)[^"]*"[^>]*value="[^"]*"' | sed 's/name="\([^"]*\)".*value="\([^"]*\)"/\1=\2/')

if [ ! -z "$OTHER_TOKENS" ]; then
    echo -e "${YELLOW}[*] Otros tokens encontrados:${NC}"
    echo "$OTHER_TOKENS"
fi
