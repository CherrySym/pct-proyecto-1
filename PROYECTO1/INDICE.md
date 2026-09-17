# El Índice de Escapada

## La fórmula

Para cada par (finde largo, destino) calculamos tres sub-puntajes normalizados 0-100 por min-max, comparando siempre entre los destinos candidatos de ese mismo finde:

- **`score_temp`** — temperatura máxima promedio de esos días específicos (mismo mes/día), promediando los 10 años de histórico 2016-2025 (Open-Meteo). Más alta = más puntaje.
- **`score_lluvia`** — precipitación promedio de esos mismos días y años. Más baja = más puntaje (escala invertida).
- **`score_lugares`** — cantidad de lugares de interés (restaurantes y playas, Foursquare) en 20km a la redonda del destino. Más lugares = más puntaje.

```
score = w_temp · score_temp + w_lluvia · score_lluvia + w_lugares · score_lugares
```

Implementado en `evaluar_destino.mejor_destino_para_finde()` (rankea destinos para un finde fijo) y `evaluar_destino.rankear_findes()` (rankea findes, usando el mejor destino de cada uno). Los tres pesos son parámetros de esas funciones, no están hardcodeados.

## Los pesos, y por qué

Usamos **w_temp = w_lluvia = w_lugares = 1/3**.

No es un default por pereza: decidimos no imponer una jerarquía turística nuestra (por ejemplo, asumir que el clima le importa a todo el mundo más que tener dónde comer o qué hacer). Con pesos iguales, ningún factor domina el resultado por diseño de la fórmula — el que domine en cada caso lo decide el dato, no el peso. Esa misma neutralidad es la que expone la conclusión de abajo: el ranking es tan sensible al criterio que ni siquiera hace falta cambiar de finde para que cambie el ganador, alcanza con cambiar el peso.

## Conclusión no obvia

**1. El ganador de un finde no depende del finde, depende de qué se pondera.**
Para el finde de Carnaval (14 al 17/02/2026), con pesos iguales gana **Carmelo** (score 72.4 — 28.6°C, 1.9mm de lluvia, 12 lugares). Pero:
- Si el criterio fuera 100% temperatura, ganan **Salto y Termas del Daymán** (29.6°C, empatados en el tope) y Carmelo cae al **4º puesto**.
- Si el criterio fuera 100% cantidad de lugares, gana **Piriápolis** (28 lugares, el máximo) — que bajo un criterio puramente climático es el **14º de 15** destinos posibles para ese mismo finde (score 17.7 sobre 100, casi el peor de la lista).

Tres fórmulas razonables, tres ganadores de regiones del país completamente distintas, para el mismo finde y los mismos datos.

**2. El finde más lluvioso del año no es de verano — es de primavera.**
Cruzando los 8 findes largos de 2026 contra los 3.653 días de histórico por destino (2016-2025), el finde de fin de octubre (31/10 al 02/11) tiene **38.0%** de probabilidad histórica de lluvia >1mm, más alto que el de Carnaval (**34.5%**) y que cualquier otro finde largo del año — pese a que la primavera suele asumirse más estable que el verano. El segundo finde de octubre (10 al 12/10) tampoco se queda atrás, con **36.7%**.

*(Ambas conclusiones se pueden reproducir corriendo `evaluar_destino.mejor_destino_para_finde(0, w_temp, w_lluvia, w_lugares)` con distintos pesos, y cruzando `datos/raw/clima_historico.json` contra `datos/procesados/findelargos_2026.txt`.)*
