import re

import time

def monitor():
    with open("logs/captures.log", "r") as f:
        # Ir al final del archivo
        f.seek(0, 2)
        print("[+] Esperando nuevos eventos...")
        while True:
            linea = f.readline()
            if not linea:
                time.sleep(0.2) # Esperar un poco antes de volver a leer
                continue
            
            if ";" in linea:
                print(f"[+] ALERTA INMEDIATA: {linea.strip()}")
                analizar_honeypot()


def analizar_honeypot():
    ruta_log = "logs/captures.log"
    # El patrón busca lo que está después de 'INTENTO: '
    patron_ataque = r"INTENTO: (.*)"
    
    print("--- INFORME DE SEGURIDAD DEL HONEYPOT ---")
    
    try:
        with open(ruta_log, "r") as f:
            for linea in f:
                # Buscamos si hay comandos sospechosos como ; | &
                if any(char in linea for char in [";", "|", "&", ">"]):
                    ataque = re.search(patron_ataque, linea)
                    if ataque:
                        print(f"[ALERTA CRÍTICA] Comando detectado: {ataque.group(1)}")
    except FileNotFoundError:
        print("No se encontró el archivo de log.")

if __name__ == "__main__":
    monitor()
