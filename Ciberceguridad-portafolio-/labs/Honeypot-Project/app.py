from flask import Flask, request, render_template
import os
import re
from datetime import datetime

app = Flask(__name__)

def registrar_ataque(ip_cliente, intento):
    # Ruta al archivo que creamos en la estructura de carpetas
    ruta_log = "logs/captures.log"
    tiempo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(ruta_log, "a") as f:
        f.write(f"[{tiempo}] IP_ORIGEN: {ip_cliente} | INTENTO: {intento}\n")

@app.route('/')
def index():
    ip = request.args.get('ip')
    salida_comando = ""

    if ip:
        patron = r"^([0-9]{1,3}\.){3}[0-9]{1,3}$"
        if re.match(patron, ip):
            comando = f"ping -c 2 {ip}"
            salida_comando = os.popen(comando).read()
        else:
            registrar_ataque(request.remote_addr, ip)
            salida_comando = "Intento de intrusión registrado. Tu IP ha sido reportada."

    return render_template("index.html", salida=salida_comando)

if __name__ == '__main__':
    # Corremos en el puerto 8080 de tu localhost (Termux)
    app.run(host='127.0.0.1', port=8080)
