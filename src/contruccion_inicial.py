import random

from cargar_datos import cargar_instancia
from funcion_objetivo import calcular_costo


def construir_solucion_aleatoria(datos):
    """
    Para cada examen de la instancia, elige al azar una franja
    (entre las permitidas para ese examen) y un aula (entre todas
    las aulas, sin filtrar por ahora).
    Devuelve la solución completa: {examen: (franja, aula)}
    """
    examenes = datos["examenes"]
    aulas_disponibles = list(datos["aulas"].keys())

    solucion = {}
    for examen, info_examen in examenes.items():
        franja = random.choice(info_examen["franjas_permitidas"])
        aula = random.choice(aulas_disponibles)
        solucion[examen] = (franja, aula)

    return solucion


if __name__ == "__main__":
    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")
    solucion = construir_solucion_aleatoria(datos)

    print("Cantidad de exámenes en la solución:", len(solucion))
    print("Ejemplo E01:", solucion["E01"])
    print("Ejemplo E20:", solucion["E20"])
    
    # prueba de costo f
    resultado = calcular_costo(solucion, datos)
    print("\n=== Costo de la solución aleatoria ===")
    print("Costo total:", resultado["costo_total"])
    print("H:", resultado["H"], "-", resultado["detalle_H"])
    print("C_día:", resultado["C_dia"])
    print("P_libres:", resultado["P_libres"])