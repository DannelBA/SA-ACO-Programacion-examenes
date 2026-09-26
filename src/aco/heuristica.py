import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from cargar_datos import cargar_instancia


def contar_problemas(examen, franja, aula, solucion_parcial, datos):
    """
    Para un candidato (franja, aula) de un examen, cuenta cuántos
    problemas tendría SI se asignara ahí, comparado con lo que la
    hormiga ya lleva puesto hasta el momento (solucion_parcial).
    """
    problemas = 0

    # 1) ¿El aula ya está ocupada en esa franja por otro examen?
    for otro_examen, (f, a) in solucion_parcial.items():
        if f == franja and a == aula:
            problemas += 1

    # 2) ¿Algún estudiante de este examen ya tiene otro examen en esa franja?
    estudiantes_examen = datos["estudiantes_por_examen"][examen]
    for estudiante in estudiantes_examen:
        for otro_examen in datos["examenes_por_estudiante"].get(estudiante, []):
            if otro_examen in solucion_parcial:
                franja_otro, _ = solucion_parcial[otro_examen]
                if franja_otro == franja:
                    problemas += 1
                    break  # con uno que choque ya basta, no seguimos revisando ese estudiante

    # 3) ¿El aula alcanza para los estudiantes del examen?
    capacidad_aula = datos["aulas"][aula]["capacidad"]
    num_estudiantes = datos["examenes"][examen]["estudiantes"]
    if capacidad_aula < num_estudiantes:
        problemas += 1

    return problemas

def calcular_eta(examen, franja, aula, solucion_parcial, datos):
    """
    Convierte la cantidad de problemas en un valor de 'atractivo'.
    Entre menos problemas, más alto el valor (más atractivo).
    """
    problemas = contar_problemas(examen, franja, aula, solucion_parcial, datos)
    return 1.0 / (1.0 + problemas)


if __name__ == "__main__":
    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")

    # Armamos una solución parcial a mano, como si una hormiga ya
    # hubiera puesto estos 2 exámenes:
    solucion_parcial = {
        "E01": ("F1", "A101"),
        "E02": ("F2", "A102"),
    }

    # Probemos con un candidato que debería chocar de aula con E01:
    problemas = contar_problemas("E05", "F1", "A101", solucion_parcial, datos)
    print("Problemas de poner E05 en (F1, A101):", problemas)

    # Y uno que no debería chocar con nada (franja/aula libres):
    problemas2 = contar_problemas("E05", "F3", "B201", solucion_parcial, datos)
    print("Problemas de poner E05 en (F3, B201):", problemas2)
    
    print(datos["aulas"]["B201"])
    print(datos["examenes"]["E05"])
    
    eta1 = calcular_eta("E05", "F1", "A101", solucion_parcial, datos)
    eta2 = calcular_eta("E05", "F3", "B201", solucion_parcial, datos)
    print("\nEta candidato con 2 problemas:", eta1)
    print("Eta candidato con 1 problema:", eta2)