# El Índice de Escapada

## La fórmula

Para cada fin de semana largo y destino calculamos tres puntajes del 0-100 comparando entre los destinos elegidos 
por cada finde.

- **`score_temp`** — temperatura máxima promedio de esos días específicos (mismo mes/día), utilizando los registros del periodo 2016-2025.
- **`score_lluvia`** — precipitación promedio de esos mismos días y años. Más baja = más puntaje (escala invertida).
- **`score_lugares`** — cantidad de lugares de interés (restaurantes y playas, Foursquare) en 20km a la redonda del destino. Más lugares = más puntaje.

**`score`** = (peso_temp · score_temp) + (peso_lluvia · score_lluvia) + (peso_lugares · score_lugares)

En`evaluar_destino.mejor_destino_para_finde()` se rankean destinos para un finde y `evaluar_destino.rankear_findes()` donde se rankean findes, usando el mejor destino de cada uno.

## Los pesos, y por qué

Usamos **peso_temp/peso_lluvia/peso_lugares = 1/3**.

Parece algo básico y no tan pensado a fondo, pero para nosotros realmente que son todos factores que afectan de igual manera al puntaje final. Al final del día, quien va a querer salir a un restaurante si hace frio, o quien va a ir a la playa si llueve; y los puntos de interes definen si tan siquiera vale la pena ir al lugar. Por muy buen clima que haya, si no hay nada que hacer no nos resulta interesante ir.

## Conclusión no obvia

**1. El ganador de un finde no depende del finde, depende de qué se pondera.**

Para el finde de Carnaval (14 al 17/02/2026), con pesos iguales gana **Carmelo** (score 72.4 — 28.6°C, 1.9mm de lluvia, 12 lugares). Pero:
- Si el criterio fuera 100% temperatura, ganan **Salto y Termas del Daymán** (29.6°C, empatados en el tope) y Carmelo cae al **4º puesto**.
- Si el criterio fuera 100% cantidad de lugares, gana **Piriápolis** (28 lugares, el máximo) — que bajo un criterio puramente climático es el **14º de 15** destinos posibles para ese mismo finde (score 17.7 sobre 100, casi el peor de la lista).

Tres fórmulas razonables, tres ganadores de regiones del país completamente distintas, para el mismo finde y los mismos datos.

**El mejor fin de semana largo del año es:**

**`2026-10-10 a 2026-10-12:`**

**`Salto, Uruguay | temp prom: 23.8°C | lluvia prom: 2.6mm |lugares: 10 | score: 78.6`**




