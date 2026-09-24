from cargar_datos import cargar_instancia
from experimento_linea_base import (
    correr_experimento_sa,
    resumir_resultados,
    guardar_resultados_csv,
)


# Las 10 combinaciones del Bloque 1 (ver justificación en la sustentación:
# 9 combinaciones cruzando T_inicial x alpha, más 1 que aísla T_final)
COMBINACIONES_BLOQUE1 = [
    {"nombre": "combo_01", "T_inicial": 1000, "alpha": 0.995, "T_final": 0.1, "iteraciones_max": 20000},
    {"nombre": "combo_02", "T_inicial": 1000, "alpha": 0.998, "T_final": 0.1, "iteraciones_max": 20000},
    {"nombre": "combo_03", "T_inicial": 1000, "alpha": 0.999, "T_final": 0.1, "iteraciones_max": 20000},
    {"nombre": "combo_04", "T_inicial": 2000, "alpha": 0.995, "T_final": 0.1, "iteraciones_max": 20000},
    {"nombre": "combo_05", "T_inicial": 2000, "alpha": 0.998, "T_final": 0.1, "iteraciones_max": 20000},
    {"nombre": "combo_06", "T_inicial": 2000, "alpha": 0.999, "T_final": 0.1, "iteraciones_max": 20000},
    {"nombre": "combo_07", "T_inicial": 5000, "alpha": 0.995, "T_final": 0.1, "iteraciones_max": 20000},
    {"nombre": "combo_08", "T_inicial": 5000, "alpha": 0.998, "T_final": 0.1, "iteraciones_max": 20000},
    {"nombre": "combo_09", "T_inicial": 5000, "alpha": 0.999, "T_final": 0.1, "iteraciones_max": 20000},
    {"nombre": "combo_10", "T_inicial": 5000, "alpha": 0.999, "T_final": 0.01, "iteraciones_max": 20000},
]


if __name__ == "__main__":
    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")

    resumenes = []

    for combinacion in COMBINACIONES_BLOQUE1:
        nombre = combinacion["nombre"]
        print(f"\n=== Corriendo {nombre}: {combinacion} ===")

        resultados = correr_experimento_sa(datos, combinacion, num_corridas=30)
        resumen = resumir_resultados(resultados)
        resumen["nombre"] = nombre
        resumenes.append(resumen)

        guardar_resultados_csv(resultados, f"resultados/bloque1_sa_{nombre}.csv")
        print(f"Resumen {nombre}: costo_promedio={resumen['costo_promedio']:.0f}, "
              f"factibilidad={resumen['porcentaje_factible']:.0f}%")

    # Guardamos también un CSV con el resumen de las 10 combinaciones, para comparar de un vistazo
    guardar_resultados_csv(resumenes, "resultados/bloque1_sa_resumen.csv")
    print("\nListo. Revisa resultados/bloque1_sa_resumen.csv para comparar las 10 combinaciones.")