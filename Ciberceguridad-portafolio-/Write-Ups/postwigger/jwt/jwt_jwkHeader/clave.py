import base64

with open("modulus.hex", "r") as f:
    hex_n = f.read().strip()

# Convertir hex a bytes y luego a Base64URL
bytes_n = bytes.fromhex(hex_n)
b64_n = base64.urlsafe_b64encode(bytes_n).decode().replace("=", "")
print(f"VALOR N: {b64_n}")
