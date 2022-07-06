import math
import random
import numpy as np

# propósito: encontrar un camino con un costo relativamente bajo que pase por todas las ciudades.
# precondición: no hay ciudades aisladas.
# ciudades: lista de ciudades
# distancia: matriz entre ciudades donde distancia[i,j] = distancia desde la ciudad i
# hasta la ciudad j y distancia[j,i] = distancia[i,j]
# complejidad: O(N^4) siendo N la cantidad de ciudades.
def exec(ciudades, distancia, ciudad_origen):
    N = len(ciudades)
    dicc_ciudades = {ciudad: False for ciudad in ciudades}
    distancias_completas = floyd_warshall(ciudades, distancia.copy()) # O(N^3)
    max_iteraciones = limite_grasp(N)
    max_it_bl = limite_bl(N)
    resultados_grasp = []
    resultados_bl = []
    res_iteracion = []

    if (N < 2):
        resultados_grasp.append([(ciudades, 0)])
        return resultados_grasp

    mejor_resultado = ([], math.inf)

    while max_iteraciones > 0: # O(N)
        # solución greedy # O(log N * N^2)
        recorrido, costo = heuristica_nearest_neighbor(dicc_ciudades.copy(), distancias_completas, ciudad_origen)
        sol_greedy = (recorrido.copy(), costo)
        print(f"\n[#{max_iteraciones}] puntaje greedy: {costo}")
        res_iteracion.append(sol_greedy[1])
        # solución búsqueda local # O(N^3)
        sol_local = busqueda_local(sol_greedy, distancias_completas, res_iteracion, max_it_bl)
        print(f"[#{max_iteraciones}] puntaje búsqueda local: {sol_local[1]}")
        if sol_local[1] < mejor_resultado[1]:
          mejor_resultado = sol_local
        resultados_bl.append(res_iteracion)
        resultados_grasp.append(mejor_resultado[1])
        print(f"[#{max_iteraciones}] iteraciones en búsqueda local: {len(res_iteracion)-1}")
        res_iteracion = []
        max_iteraciones -= 1
    resultados_grasp.append(mejor_resultado[1])

    return (resultados_grasp, resultados_bl, mejor_resultado)

# propósito: encontrar un camino con un costo relativamente bajo que pase 
# por todas las ciudades.
# precondición: existen caminos entre todo par de ciudades y las conexiones 
# entre ciudades valen igual tanto para la ida y la vuelta.
# complejidad: O(N * N * log N) =  O(log N * N^2) siendo N la cantidad de ciudades.
def heuristica_nearest_neighbor(ciudades, distancia, ciudad_inicial):
    recorrido = [ciudad_inicial]
    ciudades[ciudad_inicial] = True
    costo = 0

    while len(recorrido) < len(ciudades):
        actual = recorrido[-1]
        posibles = {key: distancia[actual, key] for key in ciudades if key != actual and not ciudades[key]}
        top_N_caminos = cantidad_mejores(len(posibles))
        posibles_ordenados = dict(sorted(posibles.items(), key=lambda item: item[1])[:top_N_caminos])

        destino = random.choice(list(posibles_ordenados.keys()))
        recorrido.append(destino)
        ciudades[destino] = True
        costo += posibles_ordenados[destino]

    costo += distancia[recorrido[-1], ciudad_inicial]
    recorrido.append(ciudad_inicial)

    return (recorrido, costo)
    
# propósito: retorna una mejor solucion vecina de la dada si existe, sino retorna la misma solucion.
# precondición: la distancia es una matriz completa de distancias.
# complejidad: O(N^3). Siendo N la cantidad de ciudades.
def busqueda_local(solucion, distancia, res_iteraciones, limite_corte):
    mejor_recorrido = solucion[0]
    mejor_costo = solucion[1]
    sigo_buscando = True

    while sigo_buscando and limite_corte > 0:
        recorrido_vecino, costo_vecino, mejora_vecino = buscar_vecino((mejor_recorrido.copy(), mejor_costo), distancia)

        if costo_vecino < mejor_costo:
            mejora_minima_apreciable = mejor_costo * 0.01
            if limite_corte % 5 == 0 and mejora_vecino < mejora_minima_apreciable:
                limite_corte -= 1
            # print("costo actual: {}, costo vecino: {}, mejora minima apreciable: {}, mejora: {}".format(mejor_costo, costo_vecino, mejora_minima_apreciable, mejora_vecino))
            mejor_recorrido = recorrido_vecino
            mejor_costo = costo_vecino
        else:
            # cuando se cumpla que costo_vecino == mejor_costo 
            # significa que el mejor vecino encontrado era mi solución actual, entonces encontré al mejor del vecindario.
            sigo_buscando = costo_vecino != mejor_costo
        res_iteraciones.append(mejor_costo)
    return (mejor_recorrido, mejor_costo)

# propósito: explora el vecindario de una solución actual y retorna
# la mejor solucion de dicho vecindario.
# precondición: distancia es una matriz completa.
# complejidad: O(N^2) siendo N la cantidad de ciudades.
def buscar_vecino(solucion, distancia):
    recorrido = solucion[0]
    costo = solucion[1]
    N = len(recorrido)
    mejor_cambio_local = 0

    for i in range(N-2):
        for j in range(i+2, N-1):
            # costo de aristas de la solucion actual
            costo_x = distancia[recorrido[i],recorrido[i+1]] + distancia[recorrido[j],recorrido[j+1]]
            # costo de aristas de la solucion vecina
            costo_y = distancia[recorrido[i],recorrido[j]] + distancia[recorrido[i+1],recorrido[j+1]]

            diferencia_costo = costo_y - costo_x

            if diferencia_costo < mejor_cambio_local:
                mejor_cambio_local = diferencia_costo
                mejor_i = i
                mejor_j = j

    if mejor_cambio_local < 0:
        recorrido[mejor_i+1:mejor_j+1:] = recorrido[mejor_i+1:mejor_j+1][::-1]
        costo = costo + mejor_cambio_local

    return (recorrido, costo, np.abs(mejor_cambio_local))

# propósito: retorna una matriz completa de distancias entre ciudades.
# precondición: no hay ciudades aisladas.
# complejidad: O(N^3) siendo N la cantidad de ciudades.
def floyd_warshall(V, E):
    distancia = E
    N = len(V)

    for i in range(N):
        for j in range(N):
            for k in range(N):
                if(i!=j and j != k and k != i):
                    distancia[i,j] = min(distancia[i,j], distancia[i,k] + distancia[k,j])

    return distancia

# propósito: retorna un entero que limitará los posibles n destinos que tiene una ciudad.
# complejidad: O(1) ya que son cálculos.
def cantidad_mejores(n):
    top_N = int(np.ceil(n * 0.05))

    if top_N >= 3:
        return top_N
    # Para casos en donde haya menos de un top 3, lo obligo a que tome los mejores tres
    elif n >= 3:
        return 3
    # si tiene menos de 3 posibilidades, lo obligo a ir por la mejor
    else:
        1

# propósito: retorna un entero que limitará la cantidad de iteraciones de grasp.
# complejidad: O(1) ya que son cálculos.
# comentario: tomé esta condición basándome en la experimentación con GRASP.
def limite_grasp(n):
    return int(np.ceil(n * 0.6))

# propósito: retorna un entero que limitará la poca mejora al explorar vecindarios.
# complejidad: O(1) ya que son cálculos.
# comentario: tomé esta condición a través de experimentación con BL.
def limite_bl(n):
    return int(np.ceil(n * 0.5))
