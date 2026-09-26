from cargar_datos import cargar_instancia
from experimento_linea_base import (
    correr_experimento_aco,
    resumir_resultados,
    guardar_resultados_csv,
)


# Bloque 1 de ACO: cuadrícula generaciones x rho (los que más se esperan
# que influyan, según el diagnóstico de la línea base), con num_hormigas,
# alpha y beta fijos. La combinación 10 aísla el efecto de duplicar
# num_hormigas sobre la mejor combinación de las 9 primeras.
COMBINACIONES_BLOQUE1_ACO = [
    {"nombre": "combo_01", "num_hormigas": 10, "generaciones": 30,  "rho": 0.70, "alpha": 1.0, "beta": 2.0, "Q": 1000000},
    {"nombre": "combo_02", "num_hormigas": 10, "generaciones": 30,  "rho": 0.85, "alpha": 1.0, "beta": 2.0, "Q": 1000000},
    {"nombre": "combo_03", "num_hormigas": 10, "generaciones": 30,  "rho": 0.95, "alpha": 1.0, "beta": 2.0, "Q": 1000000},
    {"nombre": "combo_04", "num_hormigas": 10, "generaciones": 60,  "rho": 0.70, "alpha": 1.0, "beta": 2.0, "Q": 1000000},
    {"nombre": "combo_05", "num_hormigas": 10, "generaciones": 60,  "rho": 0.85, "alpha": 1.0, "beta": 2.0, "Q": 1000000},
    {"nombre": "combo_06", "num_hormigas": 10, "generaciones": 60,  "rho": 0.95, "alpha": 1.0, "beta": 2.0, "Q": 1000000},
    {"nombre": "combo_07", "num_hormigas": 10, "generaciones": 100, "rho": 0.70, "alpha": 1.0, "beta": 2.0, "Q": 1000000},
    {"nombre": "combo_08", "num_hormigas": 10, "generaciones": 100, "rho": 0.85, "alpha": 1.0, "beta": 2.0, "Q": 1000000},
    {"nombre": "combo_09", "num_hormigas": 10, "generaciones": 100, "rho": 0.95, "alpha": 1.0, "beta": 2.0, "Q": 1000000},
    {"nombre": "combo_10", "num_hormigas": 20, "generaciones": 100, "rho": 0.85, "alpha": 1.0, "beta": 2.0, "Q": 1000000},
]


if __name__ == "__main__":
    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")

    resumenes = []

    for combinacion in COMBINACIONES_BLOQUE1_ACO:
        nombre = combinacion["nombre"]
        print(f"\n=== Corriendo {nombre}: {combinacion} ===")

        resultados = correr_experimento_aco(datos, combinacion, num_corridas=30)
        resumen = resumir_resultados(resultados)
        resumen["nombre"] = nombre
        resumenes.append(resumen)

        guardar_resultados_csv(resultados, f"resultados/bloque1_aco_{nombre}.csv")
        print(f"Resumen {nombre}: costo_promedio={resumen['costo_promedio']:.0f}, "
              f"factibilidad={resumen['porcentaje_factible']:.0f}%")

    guardar_resultados_csv(resumenes, "resultados/bloque1_aco_resumen.csv")
    print("\nListo. Revisa resultados/bloque1_aco_resumen.csv para comparar las 10 combinaciones.")