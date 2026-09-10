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

