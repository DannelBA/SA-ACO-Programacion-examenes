import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import math
import random

from cargar_datos import cargar_instancia
from funcion_objetivo import calcular_costo
from construccion_inicial import construir_solucion_aleatoria
from vecinos import generar_vecino


def enfriamiento_simulado(datos, T_inicial, alpha, T_final, iteraciones_max, semilla=None):
    if semilla is not None:
        random.seed(semilla)
    
    # Paso 1: solución inicial
    solucion_actual = construir_solucion_aleatoria(datos)
    costo_actual = calcular_costo(solucion_actual, datos)["costo_total"]

    mejor_solucion = solucion_actual
    mejor_costo = costo_actual

    T = T_inicial
    iteracion = 0

    while T > T_final and iteracion < iteraciones_max:
        # Paso 2: generar un vecino y evaluarlo
        candidato = generar_vecino(solucion_actual, datos)
        costo_candidato = calcular_costo(candidato, datos)["costo_total"]

        # Paso 3: decidir si nos movemos al vecino
        if costo_candidato < costo_actual:
            solucion_actual = candidato
            costo_actual = costo_candidato
        else:
            probabilidad = math.exp(-(costo_candidato - costo_actual) / T)
            if random.random() < probabilidad:
                solucion_actual = candidato
                costo_actual = costo_candidato

        # Paso 4: recordar la mejor solución vista hasta ahora
        if costo_actual < mejor_costo:
            mejor_solucion = solucion_actual
            mejor_costo = costo_actual

        # Paso 5: bajar la temperatura
        T = T * alpha
        iteracion += 1

    return mejor_solucion, mejor_costo, iteracion


if __name__ == "__main__":
    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")

    mejor_solucion, mejor_costo, iteracion_final = enfriamiento_simulado(
        datos, T_inicial=1000, alpha=0.995, T_final=1, iteraciones_max=2000, semilla=42
    )

    resultado = calcular_costo(mejor_solucion, datos)

    print("Iteraciones ejecutadas:", iteracion_final)
    print("Mejor costo encontrado:", mejor_costo)
    print("H:", resultado["H"], "-", resultado["detalle_H"])
    print("C_día:", resultado["C_dia"])
    print("P_libres:", resultado["P_libres"])