#Función objetivo: f = 100000 * H + 100 * C_día + P_libres

# Calculo de variable H

def contar_capacidad_insuficiente(solucion, datos):
    """
    Cuenta en cuántos exámenes el aula asignada es más pequeña
    que la cantidad de estudiantes de ese examen.
    """
    examenes = datos["examenes"]
    aulas = datos["aulas"]

    violaciones = 0
    for examen, (franja, aula) in solucion.items():
        capacidad_aula = aulas[aula]["capacidad"]
        estudiantes_examen = examenes[examen]["estudiantes"]
        if capacidad_aula < estudiantes_examen:
            violaciones += 1

    return violaciones

def contar_choque_aula(solucion, datos):
    """
    Cuenta cuántas veces un aula quedó ocupada por más de un examen
    en la misma franja.
    """
    ocupacion = {}  # (aula, franja) -> cuántos exámenes hay ahí

    for examen, (franja, aula) in solucion.items():
        clave = (aula, franja)
        ocupacion[clave] = ocupacion.get(clave, 0) + 1

    violaciones = 0
    for cantidad in ocupacion.values():
        if cantidad > 1:
            violaciones += cantidad - 1  # si hay 3 exámenes ahí, cuenta 2 choques

    return violaciones

def contar_choque_estudiante(solucion, datos):
    """
    Cuenta cuántas veces un mismo estudiante quedó con dos (o más)
    exámenes en la misma franja.
    """
    examenes_por_estudiante = datos["examenes_por_estudiante"]

    violaciones = 0
    for estudiante, lista_examenes in examenes_por_estudiante.items():
        franjas_ocupadas = {}
        for examen in lista_examenes:
            if examen not in solucion:
                continue
            franja, aula = solucion[examen]
            franjas_ocupadas[franja] = franjas_ocupadas.get(franja, 0) + 1

        for cantidad in franjas_ocupadas.values():
            if cantidad > 1:
                violaciones += cantidad - 1

    return violaciones

def contar_franja_no_permitida(solucion, datos):
    """
    Cuenta cuántos exámenes quedaron en una franja que NO está
    en su lista de franjas permitidas.
    """
    examenes = datos["examenes"]

    violaciones = 0
    for examen, (franja, aula) in solucion.items():
        franjas_permitidas = examenes[examen]["franjas_permitidas"]
        if franja not in franjas_permitidas:
            violaciones += 1

    return violaciones

def contar_aula_no_disponible(solucion, datos):
    """
    Cuenta cuántos exámenes quedaron en un aula que NO está
    disponible en la franja asignada.
    """
    aulas = datos["aulas"]

    violaciones = 0
    for examen, (franja, aula) in solucion.items():
        franjas_disponibles = aulas[aula]["franjas_disponibles"]
        if franja not in franjas_disponibles:
            violaciones += 1

    return violaciones

def contar_examen_no_programado(solucion, datos):
    """
    Cuenta cuántos exámenes de la instancia NO aparecen en la solución.
    """
    examenes = datos["examenes"]

    violaciones = 0
    for examen in examenes:
        if examen not in solucion:
            violaciones += 1

    return violaciones

def calcular_H(solucion, datos):
    """
    Suma las 6 restricciones duras y devuelve el total (H),
    junto con el detalle de cada una por separado.
    """
    detalle = {
        "examen_no_programado": contar_examen_no_programado(solucion, datos),
        "franja_no_permitida": contar_franja_no_permitida(solucion, datos),
        "aula_no_disponible": contar_aula_no_disponible(solucion, datos),
        "capacidad_insuficiente": contar_capacidad_insuficiente(solucion, datos),
        "choque_aula": contar_choque_aula(solucion, datos),
        "choque_estudiante": contar_choque_estudiante(solucion, datos),
    }
    H = sum(detalle.values())
    return H, detalle

# Calculo de variable C_dia

def calcular_C_dia(solucion, datos):
    """
    Cuenta los 'casos estudiante-día': por cada estudiante, y por cada
    día en que ese estudiante tiene 2 o más exámenes, se suma 1 caso.
    """
    examenes_por_estudiante = datos["examenes_por_estudiante"]
    franjas = datos["franjas"]

    casos = 0
    for estudiante, lista_examenes in examenes_por_estudiante.items():
        dias_ocupados = {}
        for examen in lista_examenes:
            if examen not in solucion:
                continue
            franja, aula = solucion[examen]
            dia = franjas[franja]["dia"]
            dias_ocupados[dia] = dias_ocupados.get(dia, 0) + 1

        for cantidad_examenes_ese_dia in dias_ocupados.values():
            if cantidad_examenes_ese_dia >= 2:
                casos += 1  # OJO: aquí sumamos 1, no "cantidad - 1"

    return casos

# Calcular variable P_libres

def calcular_P_libres(solucion, datos):
    """
    Suma, para cada examen programado, la diferencia entre la
    capacidad del aula asignada y el número de estudiantes del examen.
    """
    examenes = datos["examenes"]
    aulas = datos["aulas"]

    total = 0
    for examen, (franja, aula) in solucion.items():
        capacidad_aula = aulas[aula]["capacidad"]
        estudiantes_examen = examenes[examen]["estudiantes"]
        total += capacidad_aula - estudiantes_examen

    return total

# Callcular costo f

def calcular_costo(solucion, datos):
    """
    Calcula el costo total de una solución, según la fórmula:
    f = 100000*H + 100*C_dia + P_libres

    Devuelve un diccionario con el total y el detalle de cada parte,
    para poder revisar de dónde viene el costo.
    """
    H, detalle_H = calcular_H(solucion, datos)
    C_dia = calcular_C_dia(solucion, datos)
    P_libres = calcular_P_libres(solucion, datos)

    costo_total = 100000 * H + 100 * C_dia + P_libres

    return {
        "costo_total": costo_total,
        "H": H,
        "C_dia": C_dia,
        "P_libres": P_libres,
        "detalle_H": detalle_H,
    }