#PROYECTO 1 - MATIAS FADEL, ERIK DAMIRES, GABRIEL MEDEROS, NICOLAS GOBBO

import requests
import time
import os
import datetime

def filtrar_datos_clima():

    return
def filtrar_lugares_de_interes():

    return

def encontrar_finde_largo(archivo_entrada='datos/raw/feriados_2026.txt', archivo_salida='datos/procesados/findelargos_2026.txt'):
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

