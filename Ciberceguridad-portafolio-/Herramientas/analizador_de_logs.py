import argparse
import re
from collections import Counter

# 1. Configuración de Argparse
parser = argparse.ArgumentParser(description='Busca IPs y usuarios en un archivo de logs.')
parser.add_argument('archivo', type=str, help='Ruta del archivo de logs')

try:
    args = parser.parse_args()
    
    ip_list = []
    usuarios = []
    validador = False

    # 2. Procesamiento del archivo
    with open(args.archivo, 'r') as f:
        patron_ip = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
        patron_usuario = r"user\s+([^\s]+)"
        
        for linea in f:
            if "Failed" in linea:
                encontrados = re.findall(patron_ip, linea)
                usr_encontrados = re.findall(patron_usuario, linea)
                
                if encontrados:
                    ip_list.append(encontrados[0])
                if usr_encontrados:
                    usuarios.append(usr_encontrados[0])

    conteo_ips = Counter(ip_list)
    conteo_usrs = Counter(usuarios)

    # 3. Generación del Reporte
    print("\n--- RESULTADOS DEL ANÁLISIS ---")
    
    with open('salida.txt', 'w') as f_salida:
        f_salida.write("--- REPORTE DE INCIDENTES SOC ---\n\n")

        f_salida.write("[>] RESUMEN DE IPs:\n")
        for ip, total in conteo_ips.items():
            txt = f"IP: {ip} | Intentos: {total}\n"
            f_salida.write(txt)
            print(txt.strip())

        f_salida.write("\n[>] RESUMEN DE USUARIOS:\n")
        for usr, total in conteo_usrs.items():
            txt = f"Usuario: {usr} | Intentos: {total}\n"
            f_salida.write(txt)
            print(txt.strip())
            
        validador = True

    if validador:
        print("\n[+] Reporte generado con éxito en 'salida.txt'")

except FileNotFoundError:
    print(f"Error: El archivo '{args.archivo}' no existe.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
