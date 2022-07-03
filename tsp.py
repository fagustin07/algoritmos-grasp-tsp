import math
import random
import numpy as np

# propósito: encontrar un camino con un costo relativamente bajo que pase por todas las ciudades.
# precondición: no hay ciudades aisladas.
# ciudades: lista de ciudades
# distancia: matriz entre ciudades donde distancia[i,j] = distancia desde la ciudad i
# hasta la ciudad j y distancia[j,i] = distancia[i,j]
def tsp(ciudades, distancia, ciudad_origen):
    dicc_ciudades = {ciudad: False for ciudad in ciudades}
    distancias_completas = floyd_warshall(ciudades, distancia.copy())

    recorrido, costo = heuristica_nearest_neighbor(dicc_ciudades.copy(), distancias_completas, ciudad_origen)
    solucion = (recorrido.copy(), costo)
    mejor_recorrido, mejor_costo = busqueda_local(solucion, distancias_completas)

    print("solución heurística:")
    print(recorrido)
    print(costo)
    print()
    print("solución búsqueda local:")
    print(mejor_recorrido)
    print(mejor_costo)

    return (mejor_recorrido, mejor_costo)

# propósito: encontrar un camino con un costo relativamente bajo que pase 
# por todas las ciudades.
# precondición: existen caminos entre todo par de ciudades y las conexiones 
# entre ciudades valen igual tanto para la ida y la vuelta.
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
def busqueda_local(solucion, distancia):
    mejor_recorrido = solucion[0]
    mejor_costo = solucion[1]
    sigo_buscando = True

    while sigo_buscando:
        recorrido_vecino, costo_vecino = buscar_vecino((mejor_recorrido.copy(), mejor_costo), distancia)

        if costo_vecino < mejor_costo:
            mejor_recorrido = recorrido_vecino
            mejor_costo = costo_vecino
        else:
            sigo_buscando = costo_vecino != mejor_costo

    return (mejor_recorrido, mejor_costo)

def buscar_vecino(solucion, distancia):
    recorrido = solucion[0]
    costo = solucion[1]
    N = len(recorrido)
    mejor_cambio_local = math.inf

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

    return (recorrido, costo)

# propósito: retorna una matriz completa de distancias entre ciudades.
# precondición: no hay ciudades aisladas.
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
def cantidad_mejores(n):
    top_N = math.ceil( n * 0.05)

    if top_N >= 3:
        return top_N
    # Para casos en donde haya menos de un top 3, lo obligo a que tome los mejores tres
    elif n >= 3:
        return 3
    # si tiene menos de 3 posibilidades, lo obligo a ir por la mejor
    else:
        1

# Encontré por internet esta forma de crear la matriz de distancias.
# No sé si servirá pero me ayuda a empezar a ver resultados.
N = 20
ciudades = [i for i in range(N)]
aristas = [(i,j) for i in range(N) for j in range(N)]

np.random.seed(0)
x = np.random.rand(N)*1000
y = np.random.rand(N)*1000

# si bien acá genero una matriz de distancias completa, dentro de mi algoritmo
# esto no está asegurado y además quiero las distancias mínimas,
#  es por eso que igualmente aplico floyd-warshall
distancia = {(i,j): np.hypot(x[i] - x[j], y[i] - y[j]) for i,j in aristas }

tsp(ciudades, distancia, 0)