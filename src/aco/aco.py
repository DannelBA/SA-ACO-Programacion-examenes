import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import random
import time

from cargar_datos import cargar_instancia
from funcion_objetivo import calcular_costo
from candidatos import construir_candidatos
from feromona import inicializar_feromona, evaporar_feromona, depositar_feromona
from hormiga import construir_solucion_hormiga


def colonia_hormigas(datos, num_hormigas, generaciones, alpha, beta, rho, Q, semilla=None):
    if semilla is not None:
        random.seed(semilla)
        
    inicio = time.perf_counter()

    candidatos = construir_candidatos(datos)
    feromona = inicializar_feromona(candidatos)

    mejor_solucion = None
    mejor_costo = float("inf")
    generacion_mejor = 0

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
                generacion_mejor = generacion

        # Paso 2: evaporar
        evaporar_feromona(feromona, rho)

        # Paso 3: depositar, según lo que hizo cada hormiga de esta ronda
        for solucion, costo in soluciones_de_la_ronda:
            depositar_feromona(feromona, solucion, costo, Q)

    tiempo_ejecucion = time.perf_counter() - inicio  # NUEVO

    return {
        "mejor_solucion": mejor_solucion,
        "mejor_costo": mejor_costo,
        "generacion_mejor": generacion_mejor,
        "tiempo_ejecucion": tiempo_ejecucion,
    }


if __name__ == "__main__":
    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")

    resultado = colonia_hormigas(
        datos, num_hormigas=10, generaciones=30,
        alpha=1.0, beta=2.0, rho=0.9, Q=10, semilla=42
    )

    detalle_costo = calcular_costo(resultado["mejor_solucion"], datos)

    print("Mejor costo:", resultado["mejor_costo"])
    print("Generación donde se encontró:", resultado["generacion_mejor"])
    print("Tiempo (s):", resultado["tiempo_ejecucion"])
    print("H:", detalle_costo["H"])