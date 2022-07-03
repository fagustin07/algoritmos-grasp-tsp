import matplotlib.pyplot as plt

def dibujar(N, resultados):
    plt.title(f"resultados de búsqueda local para {N} ciudades")
    plt.xlabel("cantidad de iteraciones en búsqueda local")
    plt.ylabel("puntaje")

    for i, res in enumerate(resultados):
        puntajes = [sol[1] for sol in res]
        plt.plot(list(range(0, len(res))), puntajes, label=f"GRASP {i}")

    plt.xlim(0, max([len(res) for res in resultados]) + 1)
    plt.ylim(0, max([sol[1] for res in resultados for sol in res]) + 300)
    plt.legend()
    plt.show()