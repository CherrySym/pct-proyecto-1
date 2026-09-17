#PROYECTO 1 - MATIAS FADEL, ERIK DAMIRES, GABRIEL MEDEROS, NICOLAS GOBBO

import requests
import time
import os
import datetime
import json

def filtrar_datos_clima(archivo_findes=None, archivo_clima=None, archivo_salida=None):
    """
    leer las fechas de los findes de 'datos/procesados/findelargos_2026.txt'
    leer el json clima historico 'datos/raw/clima_historico.json'
    buscar cómo estuvo el clima esos mismos días exactos (mismo mes y día) en los 10 años
    extraer la temperatura máxima y la lluvia de esos días para cada lugar
    guardar un nuevo archivo 'datos/procesados/clima_findes_largos.json'
    """
    _dir = os.path.dirname(os.path.abspath(__file__))
    if archivo_findes is None:
        archivo_findes = os.path.join(_dir, 'datos', 'procesados', 'findelargos_2026.txt')
    if archivo_clima is None:
        archivo_clima = os.path.join(_dir, 'datos', 'raw', 'clima_historico.json')
    if archivo_salida is None:
        archivo_salida = os.path.join(_dir, 'datos', 'procesados', 'clima_findes_largos.json')

    directorio = os.path.dirname(archivo_salida)
    if directorio:
        os.makedirs(directorio, exist_ok=True)

    if not os.path.exists(archivo_findes) or os.path.getsize(archivo_findes) == 0:
        return
    if not os.path.exists(archivo_clima) or os.path.getsize(archivo_clima) == 0:
        return
    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0:
        # si el archivo de salida es más nuevo que sus fuentes, la caché sigue siendo válida
        entradas_mas_nuevas = os.path.getmtime(archivo_findes) > os.path.getmtime(archivo_salida) \
            or os.path.getmtime(archivo_clima) > os.path.getmtime(archivo_salida)
        if not entradas_mas_nuevas:
            return

    with open(archivo_findes, 'r', encoding='utf-8') as f:
        findes_largos = [
            [datetime.datetime.strptime(fecha.strip(), "%Y-%m-%d").date() for fecha in linea.split(',')]
            for linea in f if linea.strip()
        ]

    with open(archivo_clima, 'r', encoding='utf-8') as f:
        clima_historico = json.load(f)

    indice_por_lugar = {}
    for lugar, datos in clima_historico.items():
        indice_dia = {}
        for fecha_str, temp_max, lluvia in zip(datos['time'], datos['temperature_2m_max'], datos['precipitation_sum']):
            fecha = datetime.datetime.strptime(fecha_str, "%Y-%m-%d").date()
            dia_mes = fecha.strftime("%m-%d") #buscamos por dia y mes, ignorando el año, es decir, devolvemos todos los 02-14, 02-15, etc.
            indice_dia.setdefault(dia_mes, []).append({
                "anio": fecha.year,
                "temp_max": temp_max,
                "lluvia": lluvia,
            })
        indice_por_lugar[lugar] = indice_dia

    def promedio(registros, clave):
        valores = [registro[clave] for registro in registros if registro[clave] is not None]
        return round(sum(valores) / len(valores), 1) if valores else None

    # para cada finde largo armamos, por lugar y por día del finde, la lista de registros
    # históricos (uno por cada uno de los 10 años) de ese mismo mes-día, junto con el
    # promedio de temperatura máxima y lluvia de esos 10 años
    clima_findes_largos = []
    for fechas_finde in findes_largos:
        clima_findes_largos.append({
            "finde": [fecha.strftime("%Y-%m-%d") for fecha in fechas_finde],
            "clima": {
                lugar: {
                    fecha.strftime("%m-%d"): {
                        "registros": indice_dia.get(fecha.strftime("%m-%d"), []),
                        "promedio": {
                            "temp_max": promedio(indice_dia.get(fecha.strftime("%m-%d"), []), "temp_max"),
                            "lluvia": promedio(indice_dia.get(fecha.strftime("%m-%d"), []), "lluvia"),
                        },
                    }
                    for fecha in fechas_finde
                }
                for lugar, indice_dia in indice_por_lugar.items()
            },
        })

    with open(archivo_salida, 'w', encoding='utf-8') as f:
        json.dump(clima_findes_largos, f, ensure_ascii=False, indent=2)

    print(f"Se procesó el clima histórico de {len(clima_findes_largos)} findes largos y se guardó en {archivo_salida}")


def encontrar_finde_largo(archivo_entrada=None, archivo_salida=None):
    _dir = os.path.dirname(os.path.abspath(__file__))
    if archivo_entrada is None:
        archivo_entrada = os.path.join(_dir, 'datos', 'raw', 'feriados_2026.txt')
    if archivo_salida is None:
        archivo_salida = os.path.join(_dir, 'datos', 'procesados', 'findelargos_2026.txt')
    
    directorio = os.path.dirname(archivo_salida)
    if directorio:
        os.makedirs(directorio, exist_ok=True)

    if not os.path.exists(archivo_entrada) or os.path.getsize(archivo_entrada) == 0:
        print(f"El archivo de entrada {archivo_entrada} no existe o está vacío.")
        return
    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0:
        print(f"El archivo {archivo_salida} ya existe.")
        return

    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        lista_feriados = [datetime.datetime.strptime(linea.strip(), "%Y-%m-%d") for linea in f if linea.strip()]

    findes_largos = []

    for fecha in lista_feriados:
        dias_finde = []

        if fecha.weekday() == 0:  # Si es Lunes
            sabado = fecha - datetime.timedelta(days=2)
            domingo = fecha - datetime.timedelta(days=1)
            martes = fecha + datetime.timedelta(days=1)

            if martes in lista_feriados:
                dias_finde = [sabado, domingo, fecha, martes]
            else:
                dias_finde = [sabado, domingo, fecha]

        elif fecha.weekday() == 4:  # Si es Viernes
            jueves = fecha - datetime.timedelta(days=1)
            sabado = fecha + datetime.timedelta(days=1)
            domingo = fecha + datetime.timedelta(days=2)

            if jueves in lista_feriados:
                dias_finde = [jueves, fecha, sabado, domingo]
            else:
                dias_finde = [fecha, sabado, domingo]

        if dias_finde and dias_finde not in findes_largos:
            findes_largos.append(dias_finde)
    with open(archivo_salida, 'w', encoding='utf-8') as findelargo:
        for dias in findes_largos:
            linea = ', '.join(dia.strftime("%Y-%m-%d") for dia in dias)
            findelargo.write(linea + '\n')
    print(f"Se encontraron {len(findes_largos)} findes largos y se guardaron en {archivo_salida}")

if __name__ == "__main__":
    encontrar_finde_largo()
    filtrar_datos_clima()

