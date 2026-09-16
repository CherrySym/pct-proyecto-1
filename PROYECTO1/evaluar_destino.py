#PROYECTO 1 - MATIAS FADEL, ERIK DAMIRES, GABRIEL MEDEROS, NICOLAS GOBBO

"""

SISTEMA DE PUNTACION
Sistema de puntaje sobre 100
Generar un ranking

cuando:
largo del finde
clima en el finde

donde:
- Clima (open-meteo): x puntos
- POI (foursquare): x puntos
    (cantidad)

"""

import os
import json

_dir = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_CLIMA_FINDES = os.path.join(_dir, 'datos', 'procesados', 'clima_findes_largos.json')
CARPETA_FOURSQUARE = os.path.join(_dir, 'foursquare')


def cargar_clima_findes(archivo=ARCHIVO_CLIMA_FINDES):
    with open(archivo, 'r', encoding='utf-8') as f:
        return json.load(f)


def contar_lugares_interes(destino, carpeta=CARPETA_FOURSQUARE):
    """
    cuenta cuántos lugares de interés (foursquare) tiene un destino,
    buscando el archivo cacheado sin importar mayúsculas/minúsculas
    """
    nombre_corto = destino.split(",")[0].strip().lower()

    for nombre_archivo in os.listdir(carpeta):
        if nombre_archivo.lower() == f"{nombre_corto}.json":
            with open(os.path.join(carpeta, nombre_archivo), 'r', encoding='utf-8') as f:
                return len(json.load(f))

    return None


def clima_finde_para_destino(finde, destino):
    """
    promedia, entre los días que componen un finde largo, el promedio histórico
    (10 años) de temperatura máxima y lluvia de un destino puntual
    """
    dias = finde['clima'].get(destino)
    if not dias:
        return None

    temps = [d['promedio']['temp_max'] for d in dias.values() if d['promedio']['temp_max'] is not None]
    lluvias = [d['promedio']['lluvia'] for d in dias.values() if d['promedio']['lluvia'] is not None]

    if not temps or not lluvias:
        return None

    return {
        "finde": finde['finde'],
        "temp_prom": round(sum(temps) / len(temps), 1),
        "lluvia_prom": round(sum(lluvias) / len(lluvias), 1),
    }


def normalizar(valores, invertir=False):
    """
    escala una lista de valores a puntajes 0-100 (min-max).
    invertir=True cuando un valor más bajo debería dar más puntaje (ej. lluvia)
    """
    minimo, maximo = min(valores), max(valores)
    if maximo == minimo:
        return [100.0 for _ in valores]

    escalados = [(v - minimo) / (maximo - minimo) * 100 for v in valores]
    return [100 - e for e in escalados] if invertir else escalados


def mejor_finde_para_destino(destino, w_temp=0.5, w_lluvia=0.5, archivo=ARCHIVO_CLIMA_FINDES):
    """
    para un destino fijo, ordena sus findes largos disponibles de mejor a peor
    según temperatura (más alta = mejor) y lluvia (menos lluvia = mejor),
    normalizadas 0-100 entre esos mismos findes
    """
    findes_largos = cargar_clima_findes(archivo)

    candidatos = [clima_finde_para_destino(finde, destino) for finde in findes_largos]
    candidatos = [c for c in candidatos if c is not None]

    if not candidatos:
        print(f"No hay datos climáticos para '{destino}'.")
        return []

    temp_scores = normalizar([c['temp_prom'] for c in candidatos])
    lluvia_scores = normalizar([c['lluvia_prom'] for c in candidatos], invertir=True)

    for candidato, temp_score, lluvia_score in zip(candidatos, temp_scores, lluvia_scores):
        candidato['score_temp'] = round(temp_score, 1)
        candidato['score_lluvia'] = round(lluvia_score, 1)
        candidato['score'] = round(w_temp * temp_score + w_lluvia * lluvia_score, 1)

    return sorted(candidatos, key=lambda c: c['score'], reverse=True)


def decidir_mejor_destino(destino, w_temp=0.5, w_lluvia=0.5):
    ranking = mejor_finde_para_destino(destino, w_temp, w_lluvia)

    print(f"\nRanking de findes largos para ir a {destino}:")
    for puesto, c in enumerate(ranking, start=1):
        print(
            f"{puesto}. {c['finde'][0]} a {c['finde'][-1]}  |  "
            f"temp prom: {c['temp_prom']}°C (score {c['score_temp']})  |  "
            f"lluvia prom: {c['lluvia_prom']}mm (score {c['score_lluvia']})  |  "
            f"score total: {c['score']}"
        )

    return ranking[0] if ranking else None


def mejor_destino_para_finde(indice_finde, w_temp=1/3, w_lluvia=1/3, w_lugares=1/3, archivo=ARCHIVO_CLIMA_FINDES):
    """
    para un finde largo fijo, ordena los destinos disponibles de mejor a peor
    según temperatura, lluvia y cantidad de lugares de interés, normalizadas
    0-100 entre esos mismos destinos
    """
    findes_largos = cargar_clima_findes(archivo)
    finde = findes_largos[indice_finde]

    candidatos = []
    for destino in finde['clima']:
        clima = clima_finde_para_destino(finde, destino)
        lugares = contar_lugares_interes(destino)
        if clima is None or lugares is None:
            continue
        clima['destino'] = destino
        clima['lugares'] = lugares
        candidatos.append(clima)

    if not candidatos:
        print(f"No hay datos suficientes para el finde {finde['finde']}.")
        return []

    temp_scores = normalizar([c['temp_prom'] for c in candidatos])
    lluvia_scores = normalizar([c['lluvia_prom'] for c in candidatos], invertir=True)
    lugares_scores = normalizar([c['lugares'] for c in candidatos])

    for candidato, temp_score, lluvia_score, lugares_score in zip(candidatos, temp_scores, lluvia_scores, lugares_scores):
        candidato['score_temp'] = round(temp_score, 1)
        candidato['score_lluvia'] = round(lluvia_score, 1)
        candidato['score_lugares'] = round(lugares_score, 1)
        candidato['score'] = round(
            w_temp * temp_score + w_lluvia * lluvia_score + w_lugares * lugares_score, 1
        )

    return sorted(candidatos, key=lambda c: c['score'], reverse=True)


def decidir_mejor_destino_para_finde(indice_finde, w_temp=1/3, w_lluvia=1/3, w_lugares=1/3):
    ranking = mejor_destino_para_finde(indice_finde, w_temp, w_lluvia, w_lugares)

    if not ranking:
        return None

    print(f"\nRanking de destinos para el finde {ranking[0]['finde'][0]} a {ranking[0]['finde'][-1]}:")
    for puesto, c in enumerate(ranking, start=1):
        print(
            f"{puesto}. {c['destino']}  |  "
            f"temp prom: {c['temp_prom']}°C (score {c['score_temp']})  |  "
            f"lluvia prom: {c['lluvia_prom']}mm (score {c['score_lluvia']})  |  "
            f"lugares: {c['lugares']} (score {c['score_lugares']})  |  "
            f"score total: {c['score']}"
        )

    return ranking[0]


def rankear_findes(w_temp=1/3, w_lluvia=1/3, w_lugares=1/3, archivo=ARCHIVO_CLIMA_FINDES):
    """
    para cada finde largo disponible calcula su mejor destino posible
    (mismos criterios que mejor_destino_para_finde) y arma un ranking de
    fines de semana ordenado por el score de ese mejor destino
    """
    findes_largos = cargar_clima_findes(archivo)

    resultados = []
    for indice in range(len(findes_largos)):
        ranking_destinos = mejor_destino_para_finde(indice, w_temp, w_lluvia, w_lugares, archivo)
        if not ranking_destinos:
            continue

        mejor = ranking_destinos[0]
        resultados.append({
            "finde": mejor['finde'],
            "mejor_destino": mejor['destino'],
            "temp_prom": mejor['temp_prom'],
            "lluvia_prom": mejor['lluvia_prom'],
            "lugares": mejor['lugares'],
            "score": mejor['score'],
            "ranking_destinos": ranking_destinos,
        })

    return sorted(resultados, key=lambda r: r['score'], reverse=True)


def decidir_mejor_finde(w_temp=1/3, w_lluvia=1/3, w_lugares=1/3):
    ranking = rankear_findes(w_temp, w_lluvia, w_lugares)

    if not ranking:
        print("No hay datos suficientes para rankear los fines de semana largos.")
        return None

    print("\nRanking de fines de semana largos (con su mejor destino):")
    for puesto, r in enumerate(ranking, start=1):
        print(
            f"{puesto}. {r['finde'][0]} a {r['finde'][-1]}  ->  {r['mejor_destino']}  |  "
            f"temp prom: {r['temp_prom']}°C  |  lluvia prom: {r['lluvia_prom']}mm  |  "
            f"lugares: {r['lugares']}  |  score: {r['score']}"
        )

    return ranking[0]


if __name__ == "__main__":
    decidir_mejor_destino("Punta del Este, Maldonado, Uruguay")
    decidir_mejor_destino("Cabo Polonio, Rocha, Uruguay")
    decidir_mejor_destino_para_finde(0)
    decidir_mejor_finde()
