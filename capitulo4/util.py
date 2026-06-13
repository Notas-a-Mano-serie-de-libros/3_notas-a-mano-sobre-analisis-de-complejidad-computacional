import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
import os

plt.style.use('default')
plt.rcParams['figure.dpi'] = 500
plt.rcParams['savefig.dpi'] = 500
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['savefig.edgecolor'] = 'white'
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
os.makedirs('graficas', exist_ok=True)

def graficar_complejidad(x, y_experimental, y_teorico, nombre_archivo, ylabel, funcion,
                         titulo='Complejidad teórica vs experimental',
                         xlabel='Cantidad de datos de entrada (n)',
                         path='graficas/'):
    plt.figure(figsize=(8, 3))
    plt.plot(x, y_experimental, label=f"{funcion} experimental")
    plt.plot(x, y_teorico, '--', label=f"{funcion} teórica", color='red')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(titulo)

    formatter = ticker.ScalarFormatter(useMathText=True)
    formatter.set_scientific(True)
    formatter.set_powerlimits((-2, 2))
    plt.gca().xaxis.set_major_formatter(formatter)
    plt.gca().yaxis.set_major_formatter(formatter)
    plt.ticklabel_format(axis='both', style='sci', scilimits=(-2, 2))

    plt.legend()
    plt.grid(True)
    plt.savefig(f"{path}{nombre_archivo}", dpi=500, bbox_inches="tight", pad_inches=0.05)
    plt.show()


def modelo_cuadratico(n, a, b, c):
    return a * n**2 + b * n + c

def modelo_lineal(n, a, b):
    return a * n + b

def modelo_constante(n, c):
    return c * np.ones_like(n)
