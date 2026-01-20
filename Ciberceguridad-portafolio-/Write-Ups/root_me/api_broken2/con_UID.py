# Crea este archivo como 'gen.py'
import datetime

admin_fecha_str = "2026-01-14 03:11:42.704147"
suffix = "-8a22-0242ac100027" 
drift = -180000000012 

def int_to_uuid_prefix(t_int):
    low = t_int & 0xffffffff
    mid = (t_int >> 32) & 0xffff
    hi = (t_int >> 48) & 0x0fff
    return f"{low:08x}-{mid:04x}-1{hi:03x}"

dt = datetime.datetime.strptime(admin_fecha_str, '%Y-%m-%d %H:%M:%S.%f')
base_ticks = int((dt.timestamp() + 12219292800) * 10**7) + drift

with open("lista_admin.txt", "w") as f:
    for i in range(-50, 50): # Rango de 100 microsegundos
        f.write(int_to_uuid_prefix(base_ticks + i) + suffix + "\n")
