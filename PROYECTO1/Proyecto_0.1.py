#PROYECTO 1 - MATIAS FADEL, ERIC DAMIRES, GABRIEL MEDEROS

# - nager.date (sacar los feriados y findes)
# - open-meteo (sacar los datos climaticos historicos)
# - nominatim (sacar las coordenadas)
# - otra api mas (con clave maybe)

import requests

APIferiados = 'https://nagerholidays.com//api/v4/Holidays/uy/2026'
APIclima = 'https://open-meteo.com'
APIcoords = 'https://nominatim.org'
APIrandom = 'x' 

def consumir_datos(URL):
    r = requests.get(URL)
    dias = [feriado['date'] for feriado in r.json()]
    with open (r'PROYECTO 1/feriados_2026.txt', 'w') as feriados:
        for dia in dias:
            feriados.write(dia + '\n')
    return feriados



print(consumir_datos(APIferiados))