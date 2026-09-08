import requests
import json
import os
import time

APIfoursquare = 'https://places-api.foursquare.com/places/search'
FOURSQUARE_KEY = 'AI4OQ2WIBAZAHWHQAHGG2EKIT2AUDABGFZPPGPFRNHYYXMDN'

HEADERS = {
    "Accept": "application/json",
    "Authorization": f"Bearer {FOURSQUARE_KEY}",
    "X-Places-Api-Version": "2025-06-17"
}

CAMPOS = "name,tel,hours,rating,menu,description,price,geocodes"


def buscar_lugares(lat, lon, categoria=None, radius=20000, limit=50, reintentos=3):
    params = {
        "ll": f"{lat},{lon}",
        "radius": radius,
        "limit": limit,
        "fields": CAMPOS
    }
    if categoria:
        params["categories"] = categoria

    for intento in range(reintentos):
        r = requests.get(APIfoursquare, headers=HEADERS, params=params)
        if r.status_code == 429:
            espera = 5 * (intento + 1)
            print(f"Rate limit alcanzado. Esperando {espera}s...")
            time.sleep(espera)
            continue
        r.raise_for_status()
        return r.json()["results"]

    raise Exception("No se pudo completar la request tras varios reintentos (429 persistente)")


def limpiar_lugares(lugares):
    limpio = []
    for l in lugares:
        geo = l.get("geocodes", {}).get("main", {})
        limpio.append({
            "nombre": l.get("name", "Sin nombre"),
            "telefono": l.get("tel", "Sin teléfono"),
            "horario": l.get("hours", {}).get("display", "Sin horario"),
            "rating": l.get("rating", "Sin rating"),
            "precio": l.get("price", "Sin precio"),
            "menu": l.get("menu", "Sin menú"),
            "descripcion": l.get("description", "Sin descripción"),
            "ubicacion": f"https://www.google.com/maps?q={geo.get('latitude')},{geo.get('longitude')}" if geo else "Sin ubicación"
        })
    return limpio


def buscar_lugares_cacheado(lat, lon, nombre_destino, carpeta_cache="datos/foursquare"):
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
    print(f"{len(lugares)} lugares guardados/cargados para Montevideo")