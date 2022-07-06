import sys
import time
import datetime
import grasp
import printer
import xml_parser as parser

RECURSOS_DIR = "./recursos"
OUTPUT_DIR = "./output"

def mejor_solucion(resultados):
    mejor_sol = resultados[0][-1]

    for res in resultados:
        act_sol = res[-1]
        if mejor_sol[1] > act_sol[1]:
            mejor_sol = act_sol

    return mejor_sol

if __name__ == '__main__':
    archivo = sys.argv[1]
    ciudad_inicial = int(sys.argv[2])
    tiempo = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    nombre_archivo = f'tsp-circuito-{archivo}-{tiempo}.txt'
    nombre_grafico_grasp = f'tsp-grasp-{archivo}-{tiempo}.png'
    nombre_grafico_bl = f'tsp-busqueda-local-{archivo}-{tiempo}.png'

    V, X = parser.crear_grafo_desde(f'{RECURSOS_DIR}/{archivo}.xml')
    N = len(V)
    start_time = time.time()
    res_grasp, res_bl, mejor_sol = grasp.exec(V, X, ciudad_inicial)

    print(f"TSP GRASP terminado para {N} ciudades en {time.time() - start_time} segundos")
    print(f'mejor circuito conseguido: {mejor_sol}')
    
    guardar_graficos = False

    printer.dibujar(mejor_sol, f'{OUTPUT_DIR}/{nombre_archivo}')
    printer.graficar(archivo, N, res_grasp, res_bl, f'{OUTPUT_DIR}/{nombre_grafico_grasp}', f'{OUTPUT_DIR}/{nombre_grafico_bl}', guardar_graficos)
