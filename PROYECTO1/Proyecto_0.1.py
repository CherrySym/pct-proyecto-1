#PROYECTO 1 - MATIAS FADEL, ERIC DAMIRES, GABRIEL MEDEROS, NICOLAS GOBBO

# - nager.date (sacar los feriados y findes)
# - open-meteo (sacar los datos climaticos historicos)
# - nominatim (sacar las coordenadas)
# - otra api mas (con clave maybe)

import requests
import time
import os

APIferiados = 'https://nagerholidays.com//api/v4/Holidays/uy/2026'
APIclima = 'https://open-meteo.com'
APIcoords = 'https://nominatim.openstreetmap.org/search'
APIrandom = 'x'

def consumir_datos_feriados(URL, archivo_salida='PROYECTO1/feriados_2026.txt'):
    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0:
        return
    else:
        r = requests.get(URL)
        dias = [feriado['date'] for feriado in r.json()]
        with open(archivo_salida, 'w') as feriados:
            for dia in dias:
                feriados.write(dia + '\n')

def encontrar_finde_largo(URL, archivo_salida = 'PROYECTO1/findelargos_2026.txt', archivo_entrada = 'PROYECTO1/feriados_2026.txt'):
    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0:
        return
    else:
        with open(archivo_entrada, 'r') as feriados, open(archivo_salida, 'w') as findelargo:
            for feriado in feriados:
                fecha = datetime.datetime.strptime(feriado.strip(), "%Y-%m-%d")
                if fecha.weekday() == 0 or fecha.weekday() == 4:
                    findelargo.write(feriado.strip() + '\n')




