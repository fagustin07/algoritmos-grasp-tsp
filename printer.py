import matplotlib.pyplot as plt

def graficar(archivo, N, resultados_grasp, resultados_bl, path_bl, path_grasp, guardar = False):
    plt.figure(1)
    plt.title(f"Resultados de búsqueda local para {archivo} con {N} ciudades")
    plt.xlabel("# iteraciones")
    plt.ylabel("puntaje")

    for res in resultados_bl:
        puntajes = [sol for sol in res]
        plt.plot(list(range(0, len(res))), puntajes)

    plt.xlim(0, max([len(res) for res in resultados_bl]) + 1)
    plt.ylim(0, max([sol for res in resultados_bl for sol in res]) + 300)
    plt.legend()
    if guardar:
        plt.savefig(path_bl)

    plt.figure(2)
    plt.title(f"Resultados de GRASP para {archivo} con {N} ciudades")
    plt.xlabel("# iteraciones")
    plt.ylabel("puntaje")

    puntajes = []
    for res in resultados_grasp:
        puntajes.append(res)

    plt.plot(list(range(0, len(resultados_grasp))), puntajes)
    plt.xlim(0, len(resultados_grasp) + 10)
    plt.ylim(0, max(res for res in resultados_grasp) + 300)
    plt.legend()
    if guardar:
        plt.savefig(path_grasp)
    
    plt.show()

def dibujar(solucion, path):
    with open(path, 'w') as f:
        f.write(f"[DISTANCIA TOTAL] => {solucion[1]}\n\n")
        f.write(f"[CIRCUITO] \n")
        for i,ciudad in enumerate(solucion[0]):
            if i < len(solucion[0]) - 1:
               f.write(f"-> {ciudad} ->\n")
            else:
               f.write(f"-> {ciudad}\n")