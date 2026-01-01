vistos = set()

with open("repeated.txt", "r") as archivo:
    for linea in archivo:
        # .strip() elimina espacios y saltos de línea (\n, \r, etc.)
        limpia = linea.strip()
        
        # Saltamos líneas vacías si las hay
        if not limpia:
            continue
            
        if limpia in vistos:
            print(f"--- CONTRASEÑA ENCONTRADA ---")
            print(f"'{limpia}'") 
            break
        
        vistos.add(limpia)
