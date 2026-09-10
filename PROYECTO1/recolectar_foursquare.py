import requests
import json
import os
import time
import pathlib

APIfoursquare = 'https://places-api.foursquare.com/places/search'
FOURSQUARE_KEY = os.environ.get("FOURSQUARE_KEY", "LET0YMDHISQQGEEMBICVWFBJ4R3NYL34VGLWBCF0ASWQ3DHE")

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {FOURSQUARE_KEY}",
    "X-Places-Api-Version": "2025-06-17"
}

CARPETA_CACHE = pathlib.Path(__file__).resolve().parent / "foursquare"

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
            r = requests.get(APIfoursquare, headers=HEADERS, params=params, timeout=15)
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


def limpiar_lugares(lugares):
    limpio = []
    for l in lugares:
        limpio.append({
            "nombre": l.get("name", "Sin nombre"),
            "categorias": [c.get("name") for c in l.get("categories", [])],
            "direccion": l.get("location", {}).get("formatted_address", "Sin dirección")
        })
    return limpio


def buscar_lugares_cacheado(lat, lon, nombre_destino, carpeta_cache=CARPETA_CACHE):
    os.makedirs(carpeta_cache, exist_ok=True)
    ruta = os.path.join(carpeta_cache, f"{nombre_destino}.json")

    if os.path.exists(ruta):
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)

    resultados_crudos = buscar_lugares(lat, lon)
    resultados_limpios = limpiar_lugares(resultados_crudos)

    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(resultados_limpios, f, ensure_ascii=False, indent=2)

    return resultados_limpios


if __name__ == "__main__":
    lugares = buscar_lugares_cacheado(-34.9011, -56.1645, "montevideo")
    print(f"{len(lugares)} lugares guardados para Montevideo")