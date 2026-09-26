from cargar_datos import cargar_instancia
from experimento_linea_base import (
    correr_experimento_aco,
    resumir_resultados,
    guardar_resultados_csv,
)


# Bloque 2 de ACO: profundizamos en generaciones y rho (zona 0.75-0.85,
# donde el Bloque 1 mostró los mejores resultados), num_hormigas fijo en 10.
# La combinación 10 aísla el efecto de duplicar num_hormigas sobre la mejor
# combinación de las 9 primeras (200 generaciones, rho=0.85).
COMBINACIONES_BLOQUE2_ACO = [
    {"nombre": "combo_01", "num_hormigas": 10, "generaciones": 100, "rho": 0.75, "alpha": 1.0, "beta": 2.0, "Q": 1_000_000},
    {"nombre": "combo_02", "num_hormigas": 10, "generaciones": 100, "rho": 0.80, "alpha": 1.0, "beta": 2.0, "Q": 1_000_000},
    {"nombre": "combo_03", "num_hormigas": 10, "generaciones": 100, "rho": 0.85, "alpha": 1.0, "beta": 2.0, "Q": 1_000_000},
    {"nombre": "combo_04", "num_hormigas": 10, "generaciones": 150, "rho": 0.75, "alpha": 1.0, "beta": 2.0, "Q": 1_000_000},
    {"nombre": "combo_05", "num_hormigas": 10, "generaciones": 150, "rho": 0.80, "alpha": 1.0, "beta": 2.0, "Q": 1_000_000},
    {"nombre": "combo_06", "num_hormigas": 10, "generaciones": 150, "rho": 0.85, "alpha": 1.0, "beta": 2.0, "Q": 1_000_000},
    {"nombre": "combo_07", "num_hormigas": 10, "generaciones": 200, "rho": 0.75, "alpha": 1.0, "beta": 2.0, "Q": 1_000_000},
    {"nombre": "combo_08", "num_hormigas": 10, "generaciones": 200, "rho": 0.80, "alpha": 1.0, "beta": 2.0, "Q": 1_000_000},
    {"nombre": "combo_09", "num_hormigas": 10, "generaciones": 200, "rho": 0.85, "alpha": 1.0, "beta": 2.0, "Q": 1_000_000},
    {"nombre": "combo_10", "num_hormigas": 20, "generaciones": 200, "rho": 0.85, "alpha": 1.0, "beta": 2.0, "Q": 1_000_000},
]


if __name__ == "__main__":
    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")

    resumenes = []

    for combinacion in COMBINACIONES_BLOQUE2_ACO:
        nombre = combinacion["nombre"]
        print(f"\n=== Corriendo {nombre}: {combinacion} ===")

        resultados = correr_experimento_aco(datos, combinacion, num_corridas=30)
        resumen = resumir_resultados(resultados)
        resumen["nombre"] = nombre
        resumenes.append(resumen)

        guardar_resultados_csv(resultados, f"resultados/bloque2_aco_{nombre}.csv")
        print(f"Resumen {nombre}: costo_promedio={resumen['costo_promedio']:.0f}, "
              f"factibilidad={resumen['porcentaje_factible']:.0f}%")

    guardar_resultados_csv(resumenes, "resultados/bloque2_aco_resumen.csv")
    print("\nListo. Revisa resultados/bloque2_aco_resumen.csv para comparar las 10 combinaciones.")