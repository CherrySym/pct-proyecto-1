#PROYECTO 1 - MATIAS FADEL, ERIC DAMIRES, GABRIEL MEDEROS, NICOLAS GOBBO

def filtrar_datos_clima():

    return
def filtrar_lugares_de_interes():

    return

def encontrar_finde_largo(URL, archivo_salida = 'PROYECTO1/findelargos_2026.txt', archivo_entrada = 'PROYECTO1/feriados_2026.txt'):
    if os.path.exists(archivo_salida) and os.path.getsize(archivo_salida) > 0:
        return
    else:
        with open(archivo_entrada, 'r') as feriados, open(archivo_salida, 'w') as findelargo:
            for feriado in feriados:
                fecha = datetime.datetime.strptime(feriado.strip(), "%Y-%m-%d")
                if fecha.weekday() == 0:
                    # Lunes: el finde largo arranca el sabado anterior
                    sabado = fecha - datetime.timedelta(days=2)
                    domingo = fecha - datetime.timedelta(days=1)
                    dias_finde = [sabado, domingo, fecha]
                elif fecha.weekday() == 4:
                    # Viernes: el finde largo sigue con sabado y domingo
                    sabado = fecha + datetime.timedelta(days=1)
                    domingo = fecha + datetime.timedelta(days=2)
                    dias_finde = [fecha, sabado, domingo]
                else:
                    continue
                linea = ', '.join(dia.strftime("%Y-%m-%d") for dia in dias_finde)
                findelargo.write(linea + '\n')

encontrar_finde_largo(APIferiados)

