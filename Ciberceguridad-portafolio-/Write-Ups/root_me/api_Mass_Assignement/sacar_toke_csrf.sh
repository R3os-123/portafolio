#!/bin/bash

URL=$1

# 1. Obtener token CSRF
CSRF_TOKEN=$(curl -s "$URL/login" -c cookies.txt | grep -o 'csrf" value="[^"]*' | cut -d'"' -f3)

echo "Token CSRF obtenido: $CSRF_TOKEN"

# 2. Hacer login
curl -d "username=wiener" \
     -d "password=peter" \
     -d "csrf=$CSRF_TOKEN" \
     "$URL/login" \
     -b cookies.txt \
     -c cookies.txt \
     -L \
     -v
