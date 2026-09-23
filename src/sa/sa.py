import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import math
import random
import time

from cargar_datos import cargar_instancia
from funcion_objetivo import calcular_costo
from construccion_inicial import construir_solucion_aleatoria
from vecinos import generar_vecino


def enfriamiento_simulado(datos, T_inicial, alpha, T_final, iteraciones_max, semilla=None):
    if semilla is not None:
        random.seed(semilla)
    
    inicio = time.perf_counter()  # Marca el tiempo de inicio
    
    # Paso 1: solución inicial
    solucion_actual = construir_solucion_aleatoria(datos)
    costo_actual = calcular_costo(solucion_actual, datos)["costo_total"]

    mejor_solucion = solucion_actual
    mejor_costo = costo_actual
    iteracion_mejor = 0  # En qué iteración se encontró la mejor

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
            iteracion_mejor = iteracion  # Actualiza el récord

        # Paso 5: bajar la temperatura
        T = T * alpha
        iteracion += 1

    tiempo_ejecucion = time.perf_counter() - inicio 
        
    return {
        "mejor_solucion": mejor_solucion,
        "mejor_costo": mejor_costo,
        "iteraciones_totales": iteracion,
        "iteracion_mejor": iteracion_mejor,
        "tiempo_ejecucion": tiempo_ejecucion,
    }


if __name__ == "__main__":
    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")

    resultado = enfriamiento_simulado(
        datos, T_inicial=1000, alpha=0.995, T_final=1, iteraciones_max=2000, semilla=42
    )

    detalle_costo = calcular_costo(resultado["mejor_solucion"], datos)

    print("Mejor costo:", resultado["mejor_costo"])
    print("Iteración donde se encontró:", resultado["iteracion_mejor"])
    print("Iteraciones totales:", resultado["iteraciones_totales"])
    print("Tiempo (s):", resultado["tiempo_ejecucion"])
    print("H:", detalle_costo["H"])