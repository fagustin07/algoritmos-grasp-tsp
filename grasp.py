import math
import random
import numpy as np

# propósito: encontrar un camino con un costo relativamente bajo que pase por todas las ciudades.
# precondición: no hay ciudades aisladas.
# ciudades: lista de ciudades
# distancia: matriz entre ciudades donde distancia[i,j] = distancia desde la ciudad i
# hasta la ciudad j y distancia[j,i] = distancia[i,j]
# complejidad: O(N^3) que viene de aplicar floyd-warshall.
# comentario: Ejecuté una instancia de 1000 ciudades con floyd-warshall y tardó
# más de 5 min y lo corté porque no terminaba de aplicar el algoritmo. Luego probé
# correrlo de nuevo pero sin FW y tardó 13s. Es por eso que en la complejidad de BL
# menciono que para mí la complejidad de BL es más bien O(N^2) y que el while
# representa un k fijo y no hace que la complejidad llegue a O(N^3) sino
# más bien O(k * N^2) siendo k < N.
def grasp(ciudades, distancia, ciudad_origen):
    dicc_ciudades = {ciudad: False for ciudad in ciudades}
    # distancias_completas = floyd_warshall(ciudades, distancia.copy())
    distancias_completas = distancia

    recorrido, costo = heuristica_nearest_neighbor(dicc_ciudades.copy(), distancias_completas, ciudad_origen)
    solucion_heuristica = (recorrido.copy(), costo)
    sol_local = busqueda_local(solucion_heuristica, distancias_completas)

    print("solución heurística:")
    print(costo)
    print()
    print("solución búsqueda local:")
    print(sol_local[1])

    return sol_local[1]

# propósito: encontrar un camino con un costo relativamente bajo que pase 
# por todas las ciudades.
# precondición: existen caminos entre todo par de ciudades y las conexiones 
# entre ciudades valen igual tanto para la ida y la vuelta.
# complejidad: O(N*N) = O(N^2) siendo N la cantidad de ciudades multiplicado
# por las posibles ciudades a las que puede ir cada ciudad.
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
# complejidad: O(N^3). Siendo N^2 el costo de explorar un vecindario multiplicado
# por N en el caso que siempre encuentre un vecino con costos mejorados mayores al 10% del anterior.
# Esto en la teoría, pero la verdad es que al optimizar la BL siento que el costo 
# es mas bien O(k * N^2) => O(N^2).
def busqueda_local(solucion, distancia):
    print("comienza busqueda local:")
    mejor_recorrido = solucion[0]
    mejor_costo = solucion[1]
    sigo_buscando = True
    limite_tolerancia = calcular_tolerancia(len(mejor_recorrido))

    while sigo_buscando and limite_tolerancia > 0:
        recorrido_vecino, costo_vecino, mejora_vecino = buscar_vecino((mejor_recorrido.copy(), mejor_costo), distancia)

        if costo_vecino < mejor_costo:
            mejora_minima_apreciable = mejor_costo * 0.03
            print("costo actual: {}, costo vecino: {}, mejora minima apreciable: {}, mejora: {}".format(mejor_costo, costo_vecino, mejora_minima_apreciable, mejora_vecino))
            if mejora_vecino < mejora_minima_apreciable:
                limite_tolerancia -= 1
            mejor_recorrido = recorrido_vecino
            mejor_costo = costo_vecino
        else:
            sigo_buscando = mejora_vecino != 0

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

            if diferencia_costo < 0 and diferencia_costo < mejor_cambio_local:
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
    top_N = math.ceil( n * 0.05)

    if top_N >= 3:
        return top_N
    # Para casos en donde haya menos de un top 3, lo obligo a que tome los mejores tres
    elif n >= 3:
        return 3
    # si tiene menos de 3 posibilidades, lo obligo a ir por la mejor
    else:
        1

# propósito: retorna un entero que limitará la poca mejora al explorar vecindarios/
# complejidad: O(1) ya que son cálculos.
# comentario: llegué a este número luego de probar varias combinaciones de 
# corte mencionadas en clase. Ejecutando el algoritmo varias 
# veces con diferentes cantidades de instancias(20, 50, 100 y 200), saqué el 
# minimo apreciable, que podría ser mayor pero no lo vi necesario para 
# las pruebas que realicé ya que les cuesta llegar a vecinos apreciables con
# la cantidad que fijé (3%).
def calcular_tolerancia(n):
    return int(np.ceil(np.log2(n)))

# Encontré por internet esta forma de crear la matriz de distancias.
# No sé si servirá pero me ayuda a empezar a ver resultados.
N = 1000
ciudades = [i for i in range(N)]
aristas = [(i,j) for i in range(N) for j in range(N)]

np.random.seed(0)
x = np.random.rand(N)*1000
y = np.random.rand(N)*1000

# si bien acá genero una matriz de distancias completa, dentro de mi algoritmo
# esto no está asegurado y además quiero las distancias mínimas,
#  es por eso que igualmente aplico floyd-warshall
distancia = {(i,j): np.hypot(x[i] - x[j], y[i] - y[j]) for i,j in aristas }

grasp(ciudades, distancia, 0)