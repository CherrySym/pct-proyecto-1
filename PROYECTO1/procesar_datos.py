#PROYECTO 1 - MATIAS FADEL, ERIK DAMIRES, GABRIEL MEDEROS, NICOLAS GOBBO

import requests
import time
import os
import datetime

def filtrar_datos_clima():
    """
    leer las fechas de los findes de 'datos/procesados/findelargos_2026.txt'
    leer el json clima historico 'datos/raw/
    buscar cómo estuvo el clima esos mismos días exactos en los 10 años
    extraer la temperatura máxima y la lluvia de esas dias supongo
    guardar un nuevo archivo 'datos/procesados/clima_findes_largos.json'
    """

    return
def filtrar_lugares_de_interes():
    """
    no me entere que trae foursquare
    """
    return

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

