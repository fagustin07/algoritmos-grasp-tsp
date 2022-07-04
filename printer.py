import matplotlib.pyplot as plt

def graficar(archivo, N, resultados, path):
    plt.title(f"Resultados de búsqueda local para {archivo} con {N} ciudades")
    plt.xlabel("cantidad de iteraciones en búsqueda local")
    plt.ylabel("puntaje")

    for i, res in enumerate(resultados):
        puntajes = [sol[1] for sol in res]
        plt.plot(list(range(0, len(res))), puntajes, label=f"GRASP {i}")

    plt.xlim(0, max([len(res) for res in resultados]) + 1)
    plt.ylim(0, max([sol[1] for res in resultados for sol in res]) + 300)
    plt.legend()
    plt.savefig(path)
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