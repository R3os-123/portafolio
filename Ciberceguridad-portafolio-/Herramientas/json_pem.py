# Crea un archivo llamado 'get_pub.py'
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Pon aquí los valores 'n' y 'e' que sacaste del /jwks.json
n_str = "2a0lPs7kCr5TzUJWNNisugW97xdkiUoAUgK4YZ2sMn1fSIdpvPZJ4P7uw1w7dBeNQnxCU4MePr9kWXIWI__6z-6rURGqw1dK7gOoWQ2Fal8QupCUlw8oYueAxAJyJizlnwDna9GbMkkXji0x5AnZDbSsw4inRY_OlDnklCADxIfw3GXZnc1rCIQFO__rOQ7fDZeCELO06ceTD_JVedtwMAnKAAGtRpaUleOLd3axMkENrtQoYebNyaetRiN79nmrBKQit4ZySccmNt16ETBJhn_uOht23iRItM5sb1BukRHjQqvpngMWRTOLZ3QtgrcEHM5arA595AN47Xr9KnwNbw"
e_str = "AQAB"

def b64_to_int(s):
    # Añadir padding si es necesario
    s += '=' * (4 - len(s) % 4)
    return int.from_bytes(base64.urlsafe_b64decode(s), 'big')

n = b64_to_int(n_str)
e = b64_to_int(e_str)

# Construir la llave
public_key = rsa.RSAPublicNumbers(e, n).public_key()
pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print(pem.decode())
