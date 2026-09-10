import time
import requests
import os

APIferiados = 'https://nagerholidays.com//api/v4/Holidays/uy/2026'
APIclima = 'https://open-meteo.com'
APIcoords = 'https://nominatim.openstreetmap.org/search'
APIrandom = 'x'

def datos_feriados(URL, archivo_salida='PROYECTO1/datos/raw/feriados_2026.txt'):
    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0:
        return
    else:
        r = requests.get(URL)
        dias = [feriado['date'] for feriado in r.json()]
        with open(archivo_salida, 'w') as feriados:
            for dia in dias:
                feriados.write(dia + '\n')

def datos_destinos():

    return

def datos_clima():

    return

def lugares_de_interes():
    # en el archivo pruebaapi.py por ahora
    return

def consumir_datos_coords(archivo_salida='PROYECTO1/datos/raw/coords_2026.txt', actualizado=False):
    archivo_entrada = 'PROYECTO1/datos/procesados/direcciones_2026.txt'
    HEADERS = {'User-Agent': 'proyecto1-geocoder'}

    if actualizado:
        print("Ya está actualizado, no se hicieron cambios en el archivo de salida.")
        return

    with open(archivo_entrada, 'r') as f:
        direcciones = [line.strip() for line in f.readlines() if line.strip()]

    with open(archivo_salida, 'w') as coordenadas:
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

consumir_datos_coords(archivo_salida='PROYECTO1/datos/raw/coords_2026.txt', actualizado=False)

