import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from cargar_datos import cargar_instancia
from candidatos import construir_candidatos


def inicializar_feromona(candidatos, valor_inicial=1.0):
    """
    Crea el diccionario de feromona: una entrada por cada combinación
    posible (examen, franja, aula), todas arrancando en el mismo valor.
    """
    feromona = {}
    for examen, lista_candidatos in candidatos.items():
        for (franja, aula) in lista_candidatos:
            feromona[(examen, franja, aula)] = valor_inicial
    return feromona

def evaporar_feromona(feromona, rho):
    """
    Reduce toda la feromona un poco, simulando que se va 'olvidando'
    con el tiempo. rho es qué tanto se CONSERVA (por ejemplo 0.9
    significa que queda el 90%, se evapora el 10%).
    """
    for clave in feromona:
        feromona[clave] = feromona[clave] * rho


def depositar_feromona(feromona, solucion, costo_total, Q):
    """
    Refuerza la feromona de las combinaciones (examen, franja, aula)
    que usó esta solución. Cuanto mejor (más bajo) el costo, mayor
    el refuerzo.
    """
    aporte = Q / costo_total

    for examen, (franja, aula) in solucion.items():
        clave = (examen, franja, aula)
        feromona[clave] = feromona[clave] + aporte


if __name__ == "__main__":
    feromona_prueba = {
        ("E01", "F1", "A101"): 1.0,
        ("E01", "F2", "A102"): 1.0,
    }

    print("Antes:", feromona_prueba)

    evaporar_feromona(feromona_prueba, rho=0.9)
    print("Después de evaporar (rho=0.9):", feromona_prueba)

    solucion_prueba = {"E01": ("F1", "A101")}
    depositar_feromona(feromona_prueba, solucion_prueba, costo_total=100, Q=10)
    print("Después de depositar:", feromona_prueba)