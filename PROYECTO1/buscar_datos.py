#PROYECTO 1 - MATIAS FADEL, ERIK DAMIRES, GABRIEL MEDEROS, NICOLAS GOBBO

from dotenv import load_dotenv
load_dotenv()

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
APIfoursquare = 'https://places-api.foursquare.com/places/search'

FOURSQUARE_KEY = os.environ.get("FOURSQUARE_KEY")

HEADERS_FOURSQUARE = {
    "Accept": "application/json",
    "Authorization": f"Bearer {FOURSQUARE_KEY}",
    "X-Places-Api-Version": "2025-06-17"
}

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

    if not os.path.exists(archivo_entrada):
        print(f"El archivo de entrada {archivo_entrada} no existe.")
        return

    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        direcciones = [line.strip() for line in f.readlines() if line.strip()]

    # cargamos lo que ya está geocodificado para no volver a pedirlo, y para
    # detectar qué direcciones faltan (agregadas nuevas, o que quedaron
    # incompletas por un corte a mitad de camino)
    coords_existentes = {}
    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0:
        with open(archivo_salida, 'r', encoding='utf-8') as f:
            for linea in f:
                if ';' in linea:
                    nombre, coords = linea.strip().split(';', 1)
                    coords_existentes[nombre] = coords

    faltantes = [d for d in direcciones if d not in coords_existentes]
    if not faltantes:
        return

    for direccion in faltantes:
        params = {'q': direccion, 'format': 'json', 'limit': 1}
        data = None

        for intento in range(3):
            try:
                r = requests.get(APIcoords, params=params, headers=HEADERS, timeout=15)
            except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
                espera = 3 * (intento + 1)
                print(f"Error de conexión geocodificando '{direccion}'. Reintentando en {espera}s...")
                time.sleep(espera)
                continue

            if r.status_code == 429:
                espera = 5 * (intento + 1)
                print(f"Rate limit de Nominatim. Esperando {espera}s...")
                time.sleep(espera)
                continue

            r.raise_for_status()
            data = r.json()
            break

        if not data:
            print(f"No se encontraron coordenadas para: {direccion}")
            continue

        lat = data[0]['lat']
        lon = data[0]['lon']
        coords_existentes[direccion] = f"{lat},{lon}"
        time.sleep(1)

    with open(archivo_salida, 'w', encoding='utf-8') as coordenadas:
        for direccion in direcciones:
            if direccion in coords_existentes:
                coordenadas.write(f"{direccion};{coords_existentes[direccion]}\n")

    print("Coordenadas actualizadas correctamente")

"""
CONSEGUIR CLIMA (OPEN-METEO)
"""

def datos_clima(archivo_coords=None, archivo_salida=None, inicio='2016-01-01', fin='2025-12-31'):
    _dir = os.path.dirname(os.path.abspath(__file__))
    if archivo_coords is None:
        archivo_coords = os.path.join(_dir, 'datos', 'raw', 'coords_2026.txt')
    if archivo_salida is None:
        archivo_salida = os.path.join(_dir, 'datos', 'raw', 'clima_historico.json')

    directorio = os.path.dirname(archivo_salida)
    if directorio:
        os.makedirs(directorio, exist_ok=True)

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

    # solo descargamos lo que falte: destinos nuevos, o que no se hayan
    # podido bajar en una corrida anterior (quedaron afuera del json)
    resultados_existentes = {}
    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0:
        with open(archivo_salida, 'r', encoding='utf-8') as f:
            resultados_existentes = json.load(f)

    faltantes = [(n, lat, lon) for n, lat, lon in destinos_coords if n not in resultados_existentes]
    if not faltantes:
        return

    async def descargar_un_destino(sem, session, nombre, lat, lon):
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
        sem = asyncio.Semaphore(2)
        async with aiohttp.ClientSession() as session:
            tareas = [descargar_un_destino(sem, session, n, lat, lon) for n, lat, lon in faltantes]
            return await asyncio.gather(*tareas)

    print(f"Descargando datos climáticos de forma asíncrona para {len(faltantes)} destino(s)...")
    tiempo_inicio = time.time()
    resultados_lista = asyncio.run(descargar_todos())
    nuevos = {nombre: datos for nombre, datos in resultados_lista if datos}
    tiempo_total = time.time() - tiempo_inicio
    print(f"Descarga asíncrona completada en {tiempo_total:.2f} segundos.")

    resultados_existentes.update(nuevos)

    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(resultados_existentes, f, ensure_ascii=False, indent=2)



"""
CONSEGUIR LUGARES DE INTERES (FOURSQUARE)
"""

def buscar_lugares(lat, lon, categoria=None, radius=20000, limit=50, reintentos=3):
    params = {
        "ll": f"{lat},{lon}",
        "radius": radius,
        "limit": limit
    }

    if categoria:
        params["categories"] = categoria

    for intento in range(reintentos):
        try:
            r = requests.get(APIfoursquare, headers=HEADERS_FOURSQUARE, params=params, timeout=15)
        except (requests.exceptions.ChunkedEncodingError, requests.exceptions.ConnectionError):
            espera = 3 * (intento + 1)
            print(f"Error de conexión. Reintentando en {espera}s...")
            time.sleep(espera)
            continue

        if r.status_code == 429:
            espera = 5 * (intento + 1)
            print(f"Rate limit alcanzado. Esperando {espera}s...")
            time.sleep(espera)
            continue

        r.raise_for_status()
        return r.json()["results"]

    raise Exception("No se pudo completar la request tras varios reintentos")


def filtrar_lugares(lugares):
    filtrados = []

    for lugar in lugares:
        categorias = [c.get("name", "").lower() for c in lugar.get("categories", [])]

        es_restaurante = any("restaurant" in categoria for categoria in categorias)
        es_playa = any("beach" in categoria for categoria in categorias)

        if es_restaurante or es_playa:
            filtrados.append(lugar)

    return filtrados


def limpiar_lugares(lugares):
    limpio = []

    for l in lugares:
        limpio.append({
            "nombre": l.get("name", "Sin nombre"),
            "categorias": [c.get("name") for c in l.get("categories", [])],
            "direccion": l.get("location", {}).get("formatted_address", "Sin dirección"),
        })

    return limpio


def buscar_lugares_cacheado(lat, lon, nombre_destino, carpeta_cache=None):
    if carpeta_cache is None:
        carpeta_cache = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'foursquare')

    os.makedirs(carpeta_cache, exist_ok=True)

    ruta = os.path.join(carpeta_cache, f"{nombre_destino}.json")

    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)

    resultados_crudos = buscar_lugares(lat, lon)
    resultados_filtrados = filtrar_lugares(resultados_crudos)
    resultados_limpios = limpiar_lugares(resultados_filtrados)

    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(resultados_limpios, f, ensure_ascii=False, indent=2)

    return resultados_limpios


def datos_lugares(archivo_coords=None):
    _dir = os.path.dirname(os.path.abspath(__file__))
    if archivo_coords is None:
        archivo_coords = os.path.join(_dir, 'datos', 'raw', 'coords_2026.txt')

    if not os.path.exists(archivo_coords):
        raise FileNotFoundError(f"No se encontró el archivo: {archivo_coords}")

    with open(archivo_coords, 'r', encoding='utf-8') as archivo:
        for linea in archivo:
            linea = linea.strip()

            if not linea:
                continue

            nombre_destino, coordenadas = linea.split(";")
            lat, lon = coordenadas.split(",")
            lat = float(lat)
            lon = float(lon)

            nombre_archivo = nombre_destino.split(",")[0].strip()

            lugares = buscar_lugares_cacheado(lat, lon, nombre_archivo)

            print(f"{len(lugares)} lugares guardados para {nombre_archivo}")


if __name__ == "__main__":
    datos_feriados()
    datos_destinos()
    datos_coords()
    datos_clima()
    datos_lugares()