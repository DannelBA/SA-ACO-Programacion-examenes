import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from cargar_datos import cargar_instancia


def construir_candidatos(datos):
    """
    Para cada examen, arma la lista de parejas (franja, aula) que
    respetan:
      - la franja está permitida para ese examen
      - el aula está disponible en esa franja
    Devuelve: {examen: [(franja, aula), (franja, aula), ...]}
    """
    examenes = datos["examenes"]
    aulas = datos["aulas"]

    candidatos = {}
    for examen, info_examen in examenes.items():
        pares = []
        for franja in info_examen["franjas_permitidas"]:
            for aula, info_aula in aulas.items():
                if franja in info_aula["franjas_disponibles"]:
                    pares.append((franja, aula))
        candidatos[examen] = pares

    return candidatos


if __name__ == "__main__":
    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")
    candidatos = construir_candidatos(datos)

    print("Candidatos para E01:", candidatos["E01"])
    print("Cantidad de candidatos para E01:", len(candidatos["E01"]))