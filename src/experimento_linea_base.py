from cargar_datos import cargar_instancia
from funcion_objetivo import calcular_costo
from sa.sa import enfriamiento_simulado
from aco.aco import colonia_hormigas
import statistics
import csv


def correr_experimento_sa(datos, parametros, num_corridas=30):
    """
    Corre SA 'num_corridas' veces con los hiperparámetros dados en
    'parametros' (un diccionario), cada una con una semilla distinta.
    """
    resultados = []

    for i in range(num_corridas):
        semilla = i

        resultado = enfriamiento_simulado(
            datos,
            T_inicial=parametros["T_inicial"],
            alpha=parametros["alpha"],
            T_final=parametros["T_final"],
            iteraciones_max=parametros["iteraciones_max"],
            semilla=semilla,
        )

        detalle_costo = calcular_costo(resultado["mejor_solucion"], datos)

        resultados.append({
            "corrida": i,
            "costo": resultado["mejor_costo"],
            "H": detalle_costo["H"],
            "es_factible": detalle_costo["H"] == 0,
            "iteracion_mejor": resultado["iteracion_mejor"],
            "tiempo": resultado["tiempo_ejecucion"],
        })

        print(f"Corrida {i}: costo={resultado['mejor_costo']}, H={detalle_costo['H']}")

    return resultados

def correr_experimento_aco(datos, parametros, num_corridas=30):
    """
    Corre ACO 'num_corridas' veces con los hiperparámetros dados,
    cada una con una semilla distinta.
    """
    resultados = []

    for i in range(num_corridas):
        semilla = i

        resultado = colonia_hormigas(
            datos,
            num_hormigas=parametros["num_hormigas"],
            generaciones=parametros["generaciones"],
            alpha=parametros["alpha"],
            beta=parametros["beta"],
            rho=parametros["rho"],
            Q=parametros["Q"],
            semilla=semilla,
        )

        detalle_costo = calcular_costo(resultado["mejor_solucion"], datos)

        resultados.append({
            "corrida": i,
            "costo": resultado["mejor_costo"],
            "H": detalle_costo["H"],
            "es_factible": detalle_costo["H"] == 0,
            "iteracion_mejor": resultado["generacion_mejor"],  # misma clave que usa SA, para reusar resumir_resultados
            "tiempo": resultado["tiempo_ejecucion"],
        })

        print(f"Corrida {i}: costo={resultado['mejor_costo']}, H={detalle_costo['H']}")

    return resultados

def resumir_resultados(resultados):
    """
    Calcula las métricas resumen a partir de la lista de resultados
    de todas las corridas.
    """
    costos = [r["costo"] for r in resultados]
    tiempos = [r["tiempo"] for r in resultados]
    iteraciones_convergencia = [r["iteracion_mejor"] for r in resultados]
    factibles = [r["es_factible"] for r in resultados]

    costo_promedio = statistics.mean(costos)
    desviacion_estandar = statistics.stdev(costos)  # requiere al menos 2 datos
    coeficiente_variacion = desviacion_estandar / costo_promedio

    return {
        "costo_promedio": costo_promedio,
        "mejor_costo": min(costos),
        "peor_costo": max(costos),
        "desviacion_estandar": desviacion_estandar,
        "coeficiente_variacion": coeficiente_variacion,
        "porcentaje_factible": sum(factibles) / len(factibles) * 100,
        "tiempo_promedio": statistics.mean(tiempos),
        "iteracion_convergencia_promedio": statistics.mean(iteraciones_convergencia),
    }
    
def guardar_resultados_csv(resultados, ruta):
    """
    Guarda la lista de resultados (uno por corrida) en un archivo CSV,
    con una columna por cada dato (costo, H, tiempo, etc.).
    """
    columnas = list(resultados[0].keys())  # toma los nombres de columna del primer resultado

    with open(ruta, mode="w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=columnas)
        escritor.writeheader()
        escritor.writerows(resultados)


if __name__ == "__main__":
    datos = cargar_instancia("datos/instancia_examenes_tema02.xlsx")

    parametros_linea_base = {
        "T_inicial": 1000,
        "alpha": 0.995,
        "T_final": 1,
        "iteraciones_max": 2000,
    }

    resultados = correr_experimento_sa(datos, parametros_linea_base, num_corridas=30)
    resumen = resumir_resultados(resultados)
    print("\n=== Resumen ===")
    for clave, valor in resumen.items():
        print(f"{clave}: {valor}")
        
        parametros_linea_base_aco = {
        "num_hormigas": 10,
        "generaciones": 30,
        "alpha": 1.0,
        "beta": 2.0,
        "rho": 0.9,
        "Q": 10,
    }

    print("\n\n=== ACO - Línea base ===")
    resultados_aco = correr_experimento_aco(datos, parametros_linea_base_aco, num_corridas=30)
    resumen_aco = resumir_resultados(resultados_aco)
    print("\n=== Resumen ACO ===")
    for clave, valor in resumen_aco.items():
        print(f"{clave}: {valor}")
        
    guardar_resultados_csv(resultados, "resultados/linea_base_sa.csv")
    guardar_resultados_csv(resultados_aco, "resultados/linea_base_aco.csv")
    print("\nArchivos CSV guardados en la carpeta resultados/")
    