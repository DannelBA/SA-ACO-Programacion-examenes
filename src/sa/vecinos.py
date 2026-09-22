import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import random
from cargar_datos import cargar_instancia
from construccion_inicial import construir_solucion_aleatoria


def cambiar_franja(solucion, datos):
    """
    Toma la solución actual, elige un examen al azar, y le asigna
    una franja distinta (de las permitidas para ese examen).
    Devuelve una solución NUEVA (no modifica la original).
    """
    vecino = dict(solucion)  # copia la solución, para no dañar la original

    examenes = list(datos["examenes"].keys())
    examen_elegido = random.choice(examenes)

    franja_actual, aula_actual = vecino[examen_elegido]
    franjas_permitidas = datos["examenes"][examen_elegido]["franjas_permitidas"]
    nueva_franja = random.choice(franjas_permitidas)

    vecino[examen_elegido] = (nueva_franja, aula_actual)

    return vecino

def cambiar_aula(solucion, datos):
    """
    Toma la solución actual, elige un examen al azar, y le asigna
    un aula distinta (dejando su franja igual).
    """
    vecino = dict(solucion)

    examenes = list(datos["examenes"].keys())
    examen_elegido = random.choice(examenes)

    franja_actual, aula_actual = vecino[examen_elegido]
    aulas_disponibles = list(datos["aulas"].keys())
    nueva_aula = random.choice(aulas_disponibles)

    vecino[examen_elegido] = (franja_actual, nueva_aula)

    return vecino

def intercambiar(solucion, datos):
    """
    Elige dos exámenes al azar y les intercambia su franja y aula.
    """
    vecino = dict(solucion)

    examenes = list(datos["examenes"].keys())
    examen_1, examen_2 = random.sample(examenes, 2)  # dos exámenes distintos, sin repetir

    vecino[examen_1], vecino[examen_2] = vecino[examen_2], vecino[examen_1]

    return vecino

def generar_vecino(solucion, datos):
    """
    Elige al azar uno de los 3 movimientos y lo aplica sobre la solución.
    Esta es la función que va a usar el algoritmo SA en cada paso.
    """
    movimiento = random.choice([cambiar_franja, cambiar_aula, intercambiar])
    return movimiento(solucion, datos)


if __name__ == "__main__":
    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")
    solucion = construir_solucion_aleatoria(datos)

    vecino = cambiar_franja(solucion, datos)

    for examen in solucion:
        if solucion[examen] != vecino[examen]:
            print("Examen que cambió:", examen)
            print("Antes:", solucion[examen])
            print("Después:", vecino[examen])
    
    vecino2 = cambiar_aula(solucion, datos)
    for examen in solucion:
        if solucion[examen] != vecino2[examen]:
            print("\nExamen que cambió (aula):", examen)
            print("Antes:", solucion[examen])
            print("Después:", vecino2[examen])
            
    vecino3 = intercambiar(solucion, datos)
    for examen in solucion:
        if solucion[examen] != vecino3[examen]:
            print("\nExamen que cambió (intercambio):", examen, solucion[examen], "->", vecino3[examen])
            
    print("\n--- Probando generar_vecino (varias veces) ---")
    for _ in range(5):
        vecino_random = generar_vecino(solucion, datos)
        cambios = [e for e in solucion if solucion[e] != vecino_random[e]]
        print("Exámenes que cambiaron:", cambios)