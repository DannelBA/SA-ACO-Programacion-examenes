from cargar_datos import cargar_instancia
from funcion_objetivo import contar_examen_no_programado, contar_aula_no_disponible, contar_capacidad_insuficiente, contar_choque_aula, contar_choque_estudiante, contar_franja_no_permitida
from funcion_objetivo import calcular_H, calcular_C_dia, calcular_P_libres, calcular_costo
datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")

# Armamos una solución muy simple a mano, solo para los primeros 3 exámenes,
# poniendo a todos en la misma franja y la misma aula (a propósito, para
# que veamos violaciones de restricciones cuando calculemos el costo).
solucion_de_prueba = {
    "E01": ("F1", "A101"),
    "E02": ("F1", "A101"),
    "E03": ("F1", "A101"),
}

print(solucion_de_prueba)

H, detalle = calcular_H(solucion_de_prueba, datos)
print("\nH total:", H)
print("Detalle:", detalle)

C_dia = calcular_C_dia(solucion_de_prueba, datos)
print("\nC_día:", C_dia)

P_libres = calcular_P_libres(solucion_de_prueba, datos)
print("P_libres:", P_libres)

resultado = calcular_costo(solucion_de_prueba, datos)
print("\n=== Resultado final ===")
print(resultado)