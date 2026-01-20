import base64
import json
import sys

def clean_padding(data):
    """Añade el padding '=' necesario para base64 si falta."""
    return data + '=' * (-len(data) % 4)

def decode_jwt(token):
    try:
        parts = token.split('.')
        if len(parts) != 3:
            print("[-] Error: El formato del token no es válido (debe tener 3 partes).")
            return

        sections = ['Header', 'Payload', 'Signature (Hex)']
        
        for i in range(2):
            # Decodificar Base64URL a JSON
            decoded = base64.urlsafe_b64decode(clean_padding(parts[i]))
            print(f"\n[+] {sections[i]}:")
            print(json.dumps(json.loads(decoded), indent=4))
        
        print(f"\n[+] {sections[2]}:")
        print(parts[2])

    except Exception as e:
        print(f"[-] Error al decodificar: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python inspect_jwt.py <TU_TOKEN_JWT>")
    else:
        decode_jwt(sys.argv[1])
