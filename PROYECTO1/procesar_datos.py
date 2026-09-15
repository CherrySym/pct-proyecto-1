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
        return
    else:
        with open(archivo_entrada, 'r', encoding='utf-8') as feriados, open(archivo_salida, 'w', encoding='utf-8') as findelargo:
            for feriado in feriados:
                fecha = datetime.datetime.strptime(feriado.strip(), "%Y-%m-%d")
                if fecha.weekday() == 0:
                    # Lunes: el finde largo arranca el sábado anterior
                    sabado = fecha - datetime.timedelta(days=2)
                    domingo = fecha - datetime.timedelta(days=1)
                    dias_finde = [sabado, domingo, fecha]
                elif fecha.weekday() == 4:
                    # Viernes: el finde largo sigue con sábado y domingo
                    sabado = fecha + datetime.timedelta(days=1)
                    domingo = fecha + datetime.timedelta(days=2)
                    dias_finde = [fecha, sabado, domingo]
                else:
                    continue
                linea = ', '.join(dia.strftime("%Y-%m-%d") for dia in dias_finde)
                findelargo.write(linea + '\n')

if __name__ == "__main__":
    encontrar_finde_largo()

