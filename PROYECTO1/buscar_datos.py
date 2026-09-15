#PROYECTO 1 - MATIAS FADEL, ERIK DAMIRES, GABRIEL MEDEROS, NICOLAS GOBBO

import time
import requests
import os
import datetime
import json
import asyncio
import aiohttp

APIferiados = 'https://nagerholidays.com//api/v4/Holidays/uy/2026'
APIclima = 'https://open-meteo.com'
APIcoords = 'https://nominatim.openstreetmap.org/search'
APIrandom = 'x'

"""
CONSEGUIR FERIADOS (NAGER HOLIDAYS)
"""

def datos_feriados(url=APIferiados, archivo_salida=None):
    if archivo_salida is None:
        archivo_salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datos', 'raw', 'feriados_2026.txt')

    directorio = os.path.dirname(archivo_salida)
    if directorio:
        os.makedirs(directorio, exist_ok=True)

    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0: #Si el archivo SI existe, NO hacer nada
        return
    else: #Si el archivo NO existe escribir los feriados.
        r = requests.get(url)
        r.raise_for_status()
        dias = [feriado['date'] for feriado in r.json()]
        with open(archivo_salida, 'w', encoding='utf-8') as feriados:
            for dia in dias:
                feriados.write(dia + '\n')

"""
ESTABLECER DESTINOS
"""

def datos_destinos(archivo_salida=None):
    if archivo_salida is None:
        archivo_salida = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datos', 'raw', 'direcciones_2026.txt')

    directorio = os.path.dirname(archivo_salida)
    if directorio:
        os.makedirs(directorio, exist_ok=True)

    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0:
        return

    destinos = [
        "Montevideo, Uruguay",
        "Punta del Este, Maldonado, Uruguay",
        "Colonia del Sacramento, Colonia, Uruguay",
        "Salto, Uruguay",
        "Piriápolis, Maldonado, Uruguay",
        "Cabo Polonio, Rocha, Uruguay",
        "La Paloma, Rocha, Uruguay",
        "Villa Serrana, Lavalleja, Uruguay",
        "Minas, Lavalleja, Uruguay",
        "Carmelo, Colonia, Uruguay",
        "Tacuarembó, Uruguay",
        "Rivera, Uruguay",
        "Mercedes, Soriano, Uruguay",
        "Chuy, Rocha, Uruguay",
        "Termas del Daymán, Salto, Uruguay"
    ]

    with open(archivo_salida, 'w', encoding='utf-8') as f:
        for destino in destinos:
            f.write(destino + '\n')

"""
CONSEGUIR COORDENADAS (NOMINATIM)
"""

def datos_coords(archivo_salida=None, archivo_entrada=None, actualizado=False):
    _dir = os.path.dirname(os.path.abspath(__file__))
    if archivo_salida is None:
        archivo_salida = os.path.join(_dir, 'datos', 'raw', 'coords_2026.txt')
    if archivo_entrada is None:
        archivo_entrada = os.path.join(_dir, 'datos', 'raw', 'direcciones_2026.txt')

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

"""
CONSEGUIR CLIMA (OPEN-METEO)
"""

def datos_clima_asincrono(archivo_coords=None, archivo_salida=None, inicio='2016-01-01', fin='2025-12-31'):
    _dir = os.path.dirname(os.path.abspath(__file__))
    if archivo_coords is None:
        archivo_coords = os.path.join(_dir, 'datos', 'raw', 'coords_2026.txt')
    if archivo_salida is None:
        archivo_salida = os.path.join(_dir, 'datos', 'raw', 'clima_historico.json')

    directorio = os.path.dirname(archivo_salida)
    if directorio:
        os.makedirs(directorio, exist_ok=True)

    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0:
        return

    if not os.path.exists(archivo_coords):
        print(f"El archivo de coordenadas {archivo_coords} no existe.")
        return

    destinos_coords = []
    with open(archivo_coords, 'r', encoding='utf-8') as f:
        for linea in f:
            if ';' in linea:
                nombre, coords = linea.strip().split(';')
                lat, lon = coords.split(',')
                destinos_coords.append((nombre, float(lat), float(lon)))

    sem = asyncio.Semaphore(2)

    async def descargar_un_destino(session, nombre, lat, lon):
        async with sem:
            url_archive = 'https://archive-api.open-meteo.com/v1/archive'
            params = {
                'latitude': str(lat),
                'longitude': str(lon),
                'start_date': inicio,
                'end_date': fin,
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
                'timezone': 'America/Montevideo'
            }
            for intento in range(3):
                async with session.get(url_archive, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return nombre, data.get('daily', {})
                    elif resp.status in [429, 502, 503]:
                        await asyncio.sleep(1.5)
                    else:
                        print(f"Error {resp.status} al descargar clima para {nombre}")
                        break
                await asyncio.sleep(0.3)
            return nombre, {}

    async def descargar_todos():
        async with aiohttp.ClientSession() as session:
            tareas = [descargar_un_destino(session, n, lat, lon) for n, lat, lon in destinos_coords]
            return await asyncio.gather(*tareas)

    print("Descargando datos climáticos de forma asíncrona...")
    tiempo_inicio = time.time()
    resultados_lista = asyncio.run(descargar_todos())
    resultados = {nombre: datos for nombre, datos in resultados_lista if datos}
    tiempo_total = time.time() - tiempo_inicio
    print(f"Descarga asíncrona completada en {tiempo_total:.2f} segundos.")

    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

def datos_clima():
    datos_clima_asincrono()

def lugares_de_interes():
    # en el archivo reclectar_foursquare.py
    return

if __name__ == "__main__":
    datos_feriados()
    datos_destinos()
    datos_coords()
    datos_clima()