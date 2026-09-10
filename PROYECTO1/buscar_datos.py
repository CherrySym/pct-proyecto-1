def datos_feriados(URL, archivo_salida='PROYECTO1/datos/raw/feriados_2026.txt'):
    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0:
        return
    else:
        r = requests.get(URL)
        dias = [feriado['date'] for feriado in r.json()]
        with open(archivo_salida, 'w') as feriados:
            for dia in dias:
                feriados.write(dia + '\n')

def findes_largos_candidatos(URL, archivo_salida = 'PROYECTO1/datos/raw/findelargos_2026.txt', archivo_entrada = 'PROYECTO1/datos/raw/feriados_2026.txt'):
    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0:
        return
    else:
        with open(archivo_entrada, 'r') as feriados, open(archivo_salida, 'w') as findelargo:
            for feriado in feriados:
                fecha = datetime.datetime.strptime(feriado.strip(), "%Y-%m-%d")
                if fecha.weekday() == 0 or fecha.weekday() == 4:
                    findelargo.write(feriado.strip() + '\n')

def datos_destinos():

    return

def datos_clima():

    return

def lugares_de_interes():
    # en el archivo pruebaapi.py por ahora
    return

