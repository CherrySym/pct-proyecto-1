#PROYECTO 1 - MATIAS FADEL, ERIK DAMIRES, GABRIEL MEDEROS, NICOLAS GOBBO

import time
import requests
import os
import datetime

APIferiados = 'https://nagerholidays.com//api/v4/Holidays/uy/2026'
APIclima = 'https://open-meteo.com'
APIcoords = 'https://nominatim.openstreetmap.org/search'
APIrandom = 'x'

def datos_feriados(url=APIferiados, archivo_salida='datos/raw/feriados_2026.txt'):
    directorio = os.path.dirname(archivo_salida)
    if directorio:
        os.makedirs(directorio, exist_ok=True)

    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0:
        return
    else:
        r = requests.get(url)
        r.raise_for_status()
        dias = [feriado['date'] for feriado in r.json()]
        with open(archivo_salida, 'w', encoding='utf-8') as feriados:
            for dia in dias:
                feriados.write(dia + '\n')

def datos_destinos():

    return

def datos_clima():

    return

def lugares_de_interes():
    # en el archivo pruebaapi.py por ahora
    return

def datos_coords(archivo_salida='datos/raw/coords_2026.txt', archivo_entrada='datos/raw/direcciones_2026.txt', actualizado=False):
    directorio = os.path.dirname(archivo_salida)
    if directorio:
        os.makedirs(directorio, exist_ok=True)

    HEADERS = {'User-Agent': 'proyecto1-geocoder'}

    if actualizado:
        print("Ya está actualizado, no se hicieron cambios en el archivo de salida.")
        return

    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0:
        return

    if not os.path.exists(archivo_entrada):
        print(f"El archivo de entrada {archivo_entrada} no existe.")
        return

    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        direcciones = [line.strip() for line in f.readlines() if line.strip()]

    with open(archivo_salida, 'w', encoding='utf-8') as coordenadas:
        for direccion in direcciones:
            params = {'q': direccion, 'format': 'json', 'limit': 1}
            r = requests.get(APIcoords, params=params, headers=HEADERS)
            data = r.json()

            if not data:
                print(f"No se encontraron coordenadas para: {direccion}")
                continue

            lat = data[0]['lat']
            lon = data[0]['lon']
            coordenadas.write(f"{direccion};{lat},{lon}\n")
            time.sleep(1)

    print("Coordenadas actualizadas correctamente")

if __name__ == "__main__":
    datos_feriados()
    datos_coords()