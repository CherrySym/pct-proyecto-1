#PROYECTO 1 - MATIAS FADEL, ERIK DAMIRES, GABRIEL MEDEROS, NICOLAS GOBBO

"""
Interfaz de consola para interactuar con evaluar_destino.py
"""

from evaluar_destino import (
    cargar_clima_findes,
    decidir_mejor_destino,
    decidir_mejor_destino_para_finde,
    decidir_mejor_finde,
)


def listar_destinos(findes_largos):
    destinos = set()
    for finde in findes_largos:
        destinos.update(finde['clima'].keys())
    return sorted(destinos)


def elegir_de_lista(opciones, titulo):
    print(f"\n{titulo}")
    for i, opcion in enumerate(opciones):
        print(f"{i + 1}. {opcion}")

    while True:
        eleccion = input("Elegí un número: ").strip()
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(opciones):
            return int(eleccion) - 1
        print("Opción inválida, intentá de nuevo.")


def menu_mejor_finde_para_destino(findes_largos):
    destinos = listar_destinos(findes_largos)
    indice = elegir_de_lista(destinos, "Destinos disponibles:")
    decidir_mejor_destino(destinos[indice])


def menu_mejor_destino_para_finde(findes_largos):
    opciones = [f"{f['finde'][0]} a {f['finde'][-1]}" for f in findes_largos]
    indice = elegir_de_lista(opciones, "Fines de semana largos disponibles:")
    decidir_mejor_destino_para_finde(indice)


def main():
    findes_largos = cargar_clima_findes()

    opciones_menu = {
        "1": ("Mejor finde para un destino", menu_mejor_finde_para_destino),
        "2": ("Mejor destino para un finde", menu_mejor_destino_para_finde),
        "3": ("Mejor finde general (con su mejor destino)", lambda _: decidir_mejor_finde()),
    }

    while True:
        print("\n--- Evaluador de destinos ---")
        for clave, (descripcion, _) in opciones_menu.items():
            print(f"{clave}. {descripcion}")
        print("0. Salir")

        eleccion = input("Elegí una opción: ").strip()
        if eleccion == "0":
            break

        opcion = opciones_menu.get(eleccion)
        if opcion is None:
            print("Opción inválida, intentá de nuevo.")
            continue

        _, funcion = opcion
        funcion(findes_largos)


if __name__ == "__main__":
    main()
