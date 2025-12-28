

#Nombre del Lab: [Nombre aquí]

**Tema:** [Ej: SSRF / SQLi / LFI]

**Dificultad:** [Baja / Media / Alta]

**Herramientas:** [Ej: curl, python, sqlmap]

---

### 1. Reconocimiento

Se realiza un análisis inicial para identificar puntos de entrada y el comportamiento de la aplicación.

* **Comando:** `curl -v [URL]`
* **Observación:** [Ej: Se detecta un parámetro `X` que realiza peticiones a una API interna].

### 2. Identificación de la Vulnerabilidad

Descripción del fallo encontrado y por qué ocurre.

* **Punto de inyección:** [Ej: Parámetro `stockApi` en `/product/stock`]
* **Tipo de vulnerabilidad:** [Ej: SSRF mediante manipulación de URL en el backend]

### 3. Explotación

Pasos realizados para confirmar y explotar la vulnerabilidad.

1. **Construcción del payload:** [Ej: Se cambia el destino a `http://localhost/admin`]
2. **Ejecución:**
```bash
[Pega aquí el comando curl o script de python]

```



### 4. Resultado / Prueba de Concepto (PoC)

* **Acción final:** [Ej: Eliminación del usuario `carlos` / Acceso a archivos internos]
* **Estado:** Resuelto / Explotado.

---

### ¿Cómo usarla eficientemente?

* **Sección de Reconocimiento:** Anota siempre qué te llamó la atención (un código de estado `302`, una cabecera `Server` específica, etc.).
* **Bloques de código:** Usa las comillas triples (```) para que los comandos se vean limpios.
* **Comentarios:** Si el lab tiene un truco específico (como saltar un filtro), añádelo en la sección de Explotación.

¿Te gustaría que la adaptara más para algún tipo de vulnerabilidad específica, como solo para ataques de red o escalada de privilegios?
