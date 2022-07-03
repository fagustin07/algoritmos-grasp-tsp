import sys
import time
import grasp
import numpy as np
import graficadora

def exec_tsp_grasp(ciudades, matriz_distancias, ciudad_inicial):
    start_time = time.time()
    resultados = grasp.exec(ciudades, matriz_distancias, ciudad_inicial)
    N = len(ciudades)
    print(f"TSP GRASP terminado para {N} ciudades en {time.time() - start_time} segundos")
    graficadora.dibujar(N, resultados)

if __name__ == '__main__':
    N = int(sys.argv[1])
    if N is None:
        N = 20
    ciudad_inicial = int(sys.argv[2])
    if ciudad_inicial is None:
        ciudad_inicial = 0
    ciudades = [i for i in range(N)]
    aristas = [(i,j) for i in range(N) for j in range(N)]

    np.random.seed(0)
    x = np.random.rand(N)*1000
    y = np.random.rand(N)*1000
    distancia = {(i,j): np.hypot(x[i] - x[j], y[i] - y[j]) for i,j in aristas }

    exec_tsp_grasp(ciudades, distancia, ciudad_inicial)