#!/bin/bash

# Colores
VERDE='\e[32m'
ROJO='\e[31m'
RESET='\e[0m'

# Verificación de argumentos
if [ -z "$1" ]; then
    echo -e "${ROJO}[!] Uso: $0 <url> [archivo_reporte]${RESET}"
    exit 1
fi

echo "--- Analizando headers para: $1 ---"

# 1. Lista completa y bien cerrada
whitelist=("Strict-Transport-Security" "Content-Security-Policy" "X-Frame-Options" "X-Content-Type-Options" "Referrer-Policy" "Permissions-Policy")

# 2. Captura de headers
headers=$(curl -I -s "$1")

for i in "${whitelist[@]}"; do
    if echo "$headers" | grep -iq "$i"; then
        mensaje="${VERDE}[+] Detectado: $i${RESET}"
        echo -e "$mensaje"
        # Si existe el segundo argumento ($2), guardamos (sin colores para que el txt sea legible)
        [ -n "$2" ] && echo "[+] Detectado: $i" >> "$2"
    else
        mensaje="${ROJO}[-] Faltante:  $i${RESET}"
        echo -e "$mensaje"
        [ -n "$2" ] && echo "[-] Faltante:  $i" >> "$2"
    fi
done
