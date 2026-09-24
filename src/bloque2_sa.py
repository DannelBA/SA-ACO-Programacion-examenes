from cargar_datos import cargar_instancia
from experimento_linea_base import (
    correr_experimento_sa,
    resumir_resultados,
    guardar_resultados_csv,
)


# Bloque 2: profundizamos en alpha y T_final (los que más importaron en el
# Bloque 1), con T_inicial fijo en 5000 (en el Bloque 1 no mostró efecto
# relevante). La combinación 10 aísla el efecto de "cortar antes de tiempo"
# con un iteraciones_max reducido a propósito.
COMBINACIONES_BLOQUE2 = [
    {"nombre": "combo_01", "T_inicial": 5000, "alpha": 0.999,  "T_final": 0.05,  "iteraciones_max": 60000},
    {"nombre": "combo_02", "T_inicial": 5000, "alpha": 0.999,  "T_final": 0.01,  "iteraciones_max": 60000},
    {"nombre": "combo_03", "T_inicial": 5000, "alpha": 0.999,  "T_final": 0.005, "iteraciones_max": 60000},
    {"nombre": "combo_04", "T_inicial": 5000, "alpha": 0.9993, "T_final": 0.05,  "iteraciones_max": 60000},
    {"nombre": "combo_05", "T_inicial": 5000, "alpha": 0.9993, "T_final": 0.01,  "iteraciones_max": 60000},
    {"nombre": "combo_06", "T_inicial": 5000, "alpha": 0.9993, "T_final": 0.005, "iteraciones_max": 60000},
    {"nombre": "combo_07", "T_inicial": 5000, "alpha": 0.9995, "T_final": 0.05,  "iteraciones_max": 60000},
    {"nombre": "combo_08", "T_inicial": 5000, "alpha": 0.9995, "T_final": 0.01,  "iteraciones_max": 60000},
    {"nombre": "combo_09", "T_inicial": 5000, "alpha": 0.9995, "T_final": 0.005, "iteraciones_max": 60000},
    # combo_10: mismos T_inicial/alpha/T_final que combo_06, pero con tope
    # de iteraciones reducido a la mitad -> aísla el efecto de "cortar antes"
    {"nombre": "combo_10", "T_inicial": 5000, "alpha": 0.9993, "T_final": 0.005, "iteraciones_max": 10000},
]


if __name__ == "__main__":
    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")

    resumenes = []

    for combinacion in COMBINACIONES_BLOQUE2:
        nombre = combinacion["nombre"]
        print(f"\n=== Corriendo {nombre}: {combinacion} ===")

        resultados = correr_experimento_sa(datos, combinacion, num_corridas=30)
        resumen = resumir_resultados(resultados)
        resumen["nombre"] = nombre
        resumenes.append(resumen)

        guardar_resultados_csv(resultados, f"resultados/bloque2_sa_{nombre}.csv")
        print(f"Resumen {nombre}: costo_promedio={resumen['costo_promedio']:.0f}, "
              f"factibilidad={resumen['porcentaje_factible']:.0f}%")

    guardar_resultados_csv(resumenes, "resultados/bloque2_sa_resumen.csv")
    print("\nListo. Revisa resultados/bloque2_sa_resumen.csv para comparar las 10 combinaciones.")