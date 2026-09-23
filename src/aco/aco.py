import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import random

from cargar_datos import cargar_instancia
from funcion_objetivo import calcular_costo
from candidatos import construir_candidatos
from feromona import inicializar_feromona, evaporar_feromona, depositar_feromona
from hormiga import construir_solucion_hormiga


def colonia_hormigas(datos, num_hormigas, generaciones, alpha, beta, rho, Q, semilla=None):
    if semilla is not None:
        random.seed(semilla)

    candidatos = construir_candidatos(datos)
    feromona = inicializar_feromona(candidatos)

    mejor_solucion = None
    mejor_costo = float("inf")

    for generacion in range(generaciones):
        soluciones_de_la_ronda = []

        # Paso 1: cada hormiga construye su solución
        for _ in range(num_hormigas):
            solucion = construir_solucion_hormiga(datos, candidatos, feromona, alpha, beta)
            costo = calcular_costo(solucion, datos)["costo_total"]
            soluciones_de_la_ronda.append((solucion, costo))

            if costo < mejor_costo:
                mejor_solucion = solucion
                mejor_costo = costo

        # Paso 2: evaporar
        evaporar_feromona(feromona, rho)

        # Paso 3: depositar, según lo que hizo cada hormiga de esta ronda
        for solucion, costo in soluciones_de_la_ronda:
            depositar_feromona(feromona, solucion, costo, Q)

    return mejor_solucion, mejor_costo


if __name__ == "__main__":
    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")

    mejor_solucion, mejor_costo = colonia_hormigas(
        datos, num_hormigas=10, generaciones=30,
        alpha=1.0, beta=2.0, rho=0.9, Q=10, semilla=42
    )

    resultado = calcular_costo(mejor_solucion, datos)
    print("Mejor costo:", mejor_costo)
    print("H:", resultado["H"], "-", resultado["detalle_H"])
    print("C_día:", resultado["C_dia"])