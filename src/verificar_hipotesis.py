import random

from cargar_datos import cargar_instancia
from funcion_objetivo import calcular_costo
from aco.candidatos import construir_candidatos
from aco.feromona import inicializar_feromona, evaporar_feromona, depositar_feromona
from aco.hormiga import construir_solucion_hormiga


def colonia_hormigas_con_log(datos, num_hormigas, generaciones, alpha, beta, rho, Q, semilla):
    """
    Igual que colonia_hormigas, pero además devuelve la lista del mejor
    costo visto DESPUÉS de cada generación (para poder inspeccionar
    cuándo aparece por primera vez cada mejora).
    """
    random.seed(semilla)

    candidatos = construir_candidatos(datos)
    feromona = inicializar_feromona(candidatos)

    mejor_costo = float("inf")
    historial_mejor_por_generacion = []

    for generacion in range(generaciones):
        soluciones_de_la_ronda = []

        for _ in range(num_hormigas):
            solucion = construir_solucion_hormiga(datos, candidatos, feromona, alpha, beta)
            costo = calcular_costo(solucion, datos)["costo_total"]
            soluciones_de_la_ronda.append((solucion, costo))

            if costo < mejor_costo:
                mejor_costo = costo

        historial_mejor_por_generacion.append(mejor_costo)

        evaporar_feromona(feromona, rho)
        for solucion, costo in soluciones_de_la_ronda:
            depositar_feromona(feromona, solucion, costo, Q)

    return historial_mejor_por_generacion


datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")

print("--- Con rho=0.70, Q=1,000,000 ---")
historial_1 = colonia_hormigas_con_log(datos, num_hormigas=10, generaciones=30,
                                         alpha=1.0, beta=2.0, rho=0.70, Q=1_000_000, semilla=6)
print("Historial completo:", historial_1)

print("\n--- Con rho=0.85, Q=1,000,000 ---")
historial_2 = colonia_hormigas_con_log(datos, num_hormigas=10, generaciones=30,
                                         alpha=1.0, beta=2.0, rho=0.85, Q=1_000_000, semilla=6)
print("Historial completo:", historial_2)