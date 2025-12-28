
import argparse
import zipfile
passwd_list ="rockyou.txt"
zip = "protected.zip"
#colores
VERDE = "\033[0;32m"
ROJO = "\033[0;31m"
RESET = "\033[0m"
CYAN = "\033[0;36m"
print(f"{CYAN}=========cracker de zips==========")


# 1. Configuración de Argparse
parser = argparse.ArgumentParser(description='cracker de zips')
parser.add_argument("-d",'--diccionario', type=str, help='Ruta del diccionario')
parser.add_argument('-z','--zip', type=str, help='Ruta del zip ')
#try:
args = parser.parse_args()
#except:
#    pass
contador = 0
with open(args.diccionario ,"rb") as diccionario:
    total_passwords = sum(1 for linea in diccionario)
    diccionario.seek(0)
    with zipfile.ZipFile(args.zip, mode="r") as archive:
        for i in diccionario:
            contador += 1

            if contador % 1000 == 0:
                porcentaje = (contador / total_passwords) * 100
                # Dibujamos la barra: \r para volver al inicio, end="" para no saltar de linea
                print(f"\r{CYAN}Progreso: [{contador}/{total_passwords}] {porcentaje:.2f}%{RESET}", end="")
            
            try:
                archive.extractall(pwd=i.strip())
                print(f'\n{VERDE}[¥] OK contraseña encontrada: {RESET}{i.decode().strip()}{RESET}')
                break
            except:
                pass
