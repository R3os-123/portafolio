¡Excelente! Vamos a redactar este reporte con un nivel de detalle que demuestre no solo que sabes usar la herramienta, sino que comprendes la arquitectura de servidores. Este es el tipo de documentación que destaca en un proceso de selección o en una comunidad de hacking.

---

# Informe de Explotación: SSRF vía Nginx ProxyPass Misconfiguration

**Plataforma:** Root-Me

**Vulnerabilidad:** Server-Side Request Forgery (SSRF)

**Técnica:** Host Injection & DNS Wildcard Bypass

**Flag:** `RM{SSRF_v1a_Ng1nX_:o}`

---

### 1. Análisis de la Configuración (Vectores de Ataque)

Al analizar el archivo `nginx.conf`, se identificaron dos puntos críticos:

* **Acceso Restringido:** El directorio `/uploads/` cuenta con una directiva `allow 127.0.0.1; deny all;`. Esto significa que el contenido (incluyendo la flag) solo es accesible si la petición se origina desde el propio servidor.
* **Proxy Dinámico Inseguro:** La directiva `location ~ /dir_enum(.*)` utiliza una expresión regular para capturar la entrada del usuario (`$1`) y la concatena directamente en un `proxy_pass`.

### 2. Identificación del Fallo

El fallo principal es la **confianza ciega en la concatenación de cadenas**. Al no validar que `$1` sea un recurso local del servidor de destino, el atacante puede inyectar caracteres especiales de una URL para cambiar el destino de la petición saliente del proxy.

### 3. Estrategia de Explotación: URL UserInfo Injection

El estándar de URLs permite definir credenciales antes del host: `http://user:pass@host.com`. Aprovechamos esto para "neutralizar" el host legítimo del proxy:

1. **Payload:** `/dir_enum@app.127.0.0.1.nip.io/uploads/`
2. **Construcción interna en Nginx:**
`http://web-serveur-ch94-apache` + `@app.127.0.0.1.nip.io/uploads/`
3. **Interpretación del Servidor:**
Nginx interpreta que `web-serveur-ch94-apache` es el nombre de usuario y el host real al que debe conectarse es **`app.127.0.0.1.nip.io`**.

### 4. Bypass del Resolver mediante DNS Wildcard

Para evitar problemas con el resolvedor DNS interno y listas negras de IPs, se utilizó **nip.io**. Este servicio resuelve cualquier subdominio que contenga una IP hacia esa misma IP.

* `app.127.0.0.1.nip.io` resuelve a `127.0.0.1`.

Esto obliga a Nginx a realizar una petición interna hacia sí mismo, lo que permite saltar la restricción de IP de la carpeta `/uploads/`, ya que para el sistema de archivos, la petición ahora proviene de `localhost`.

### 5. Ejecución (PoC)

Utilizando `curl` desde la terminal para obtener el listado de archivos y posteriormente la flag:

```bash
# Paso 1: Listar directorio para localizar la flag
curl -i "http://challenge01.root-me.org:59094/dir_enum@app.127.0.0.1.nip.io/uploads/"

# Paso 2: Leer la flag (asumiendo que se llama flag.txt)
curl -i "http://challenge01.root-me.org:59094/dir_enum@app.127.0.0.1.nip.io/uploads/flag.txt"

```

### 6. Conclusión y Mitigación

La vulnerabilidad se resuelve evitando el uso de variables del usuario directamente en la directiva `proxy_pass`. Se recomienda usar rutas estáticas o validaciones estrictas (whitelisting) antes de procesar la redirección del proxy
