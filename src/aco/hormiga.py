import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import random

from cargar_datos import cargar_instancia
from candidatos import construir_candidatos
from heuristica import calcular_eta


def elegir_para_examen(examen, candidatos_examen, solucion_parcial, datos, feromona, alpha, beta):
    """
    Elige UN candidato (franja, aula) para este examen, combinando
    feromona (experiencia acumulada) y eta (heurística del momento).
    """
    pesos = []
    for (franja, aula) in candidatos_examen:
        f = feromona[(examen, franja, aula)]
        eta = calcular_eta(examen, franja, aula, solucion_parcial, datos)
        pesos.append((f ** alpha) * (eta ** beta))

    elegido = random.choices(candidatos_examen, weights=pesos, k=1)[0]
    return elegido

def construir_solucion_hormiga(datos, candidatos, feromona, alpha, beta):
    """
    Una hormiga construye una solución completa: recorre todos los
    exámenes, uno por uno, y para cada uno elige su (franja, aula)
    considerando lo que ya lleva puesto hasta el momento.
    """
    solucion = {}

    solucion = {}
    for examen in datos["examenes"]:
        candidatos_examen = candidatos[examen]
        elegido = elegir_para_examen(examen, candidatos_examen, solucion, datos, feromona, alpha, beta)
        solucion[examen] = elegido
    return solucion

def construir_varias_hormigas(datos, candidatos, feromona, alpha, beta, num_hormigas):
    """
    Construye 'num_hormigas' soluciones independientes y devuelve
    la lista de (solucion, costo_total) de cada una.
    """
    from funcion_objetivo import calcular_costo

    resultados = []
    for _ in range(num_hormigas):
        solucion = construir_solucion_hormiga(datos, candidatos, feromona, alpha, beta)
        costo = calcular_costo(solucion, datos)["costo_total"]
        resultados.append((solucion, costo))

    return resultados

if __name__ == "__main__":
    from feromona import inicializar_feromona

    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")
    candidatos = construir_candidatos(datos)
    feromona = inicializar_feromona(candidatos)

    resultados = construir_varias_hormigas(datos, candidatos, feromona, alpha=1.0, beta=2.0, num_hormigas=10)

    costos = [costo for (solucion, costo) in resultados]
    print("Costos de las 10 hormigas:", costos)
    print("Mejor costo:", min(costos))