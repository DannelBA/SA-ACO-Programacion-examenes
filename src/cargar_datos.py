import openpyxl


def cargar_examenes(hoja):
    """
    Lee la hoja 'Examenes' y devuelve un diccionario así:
    {
        'E01': {'estudiantes': 11, 'duracion': 120, 'franjas_permitidas': ['F1','F2','F6','F7']},
        ...
    }
    """
    examenes = {}
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        codigo, num_estudiantes, duracion, franjas_texto = fila
        examenes[codigo] = {
            "estudiantes": num_estudiantes,
            "duracion": duracion,
            "franjas_permitidas": franjas_texto.split(","),
        }
    return examenes

def cargar_franjas(hoja):
    """
    Lee la hoja 'Franjas' y devuelve un diccionario así:
    {
        'F1': {'dia': 'Lunes', 'horario': '08:00-10:00'},
        ...
    }
    """
    franjas = {}
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        codigo, dia, horario = fila
        franjas[codigo] = {"dia": dia, "horario": horario}
    return franjas

def cargar_aulas(hoja):
    """
    Lee la hoja 'Aulas' y devuelve un diccionario así:
    {
        'A101': {'capacidad': 15, 'franjas_disponibles': ['F1','F2',...]},
        ...
    }
    """
    aulas = {}
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        codigo, capacidad, franjas_texto = fila
        aulas[codigo] = {
            "capacidad": capacidad,
            "franjas_disponibles": franjas_texto.split(","),
        }
    return aulas

def cargar_matriculas(hoja):
    """
    Lee la hoja 'Matriculas' y devuelve una lista de parejas:
    [('EST001', 'E35'), ('EST001', 'E12'), ...]
    """
    matriculas = []
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        estudiante, examen = fila
        matriculas.append((estudiante, examen))
    return matriculas

def agrupar_examenes_por_estudiante(matriculas):
    """
    Convierte la lista de matrículas [('EST001','E35'), ('EST001','E22'), ...]
    en un diccionario: {'EST001': ['E35', 'E22', ...], ...}
    """
    resultado = {}
    for estudiante, examen in matriculas:
        if estudiante not in resultado:
            resultado[estudiante] = []
        resultado[estudiante].append(examen)
    return resultado

def cargar_instancia(ruta_excel):
    """
    Abre el Excel y devuelve TODO junto en un solo diccionario:
    {
        'examenes': {...},
        'franjas': {...},
        'aulas': {...},
        'matriculas': [...]
    }
    """
    libro = openpyxl.load_workbook(ruta_excel, data_only=True)
    matriculas = cargar_matriculas(libro["Matriculas"])
    return {
        "examenes": cargar_examenes(libro["Examenes"]),
        "franjas": cargar_franjas(libro["Franjas"]),
        "aulas": cargar_aulas(libro["Aulas"]),
        "matriculas": matriculas,
        "examenes_por_estudiante": agrupar_examenes_por_estudiante(matriculas),
    }

if __name__ == "__main__":
    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")

    print("Exámenes:", len(datos["examenes"]))
    print("Franjas:", len(datos["franjas"]))
    print("Aulas:", len(datos["aulas"]))
    print("Matrículas:", len(datos["matriculas"]))