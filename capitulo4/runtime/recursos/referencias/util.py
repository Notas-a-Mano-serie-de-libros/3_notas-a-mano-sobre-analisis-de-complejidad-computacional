import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from pathlib import Path
from common.graphics import graphics_dir

plt.style.use('default')
plt.rcParams['figure.dpi'] = 500
plt.rcParams['savefig.dpi'] = 500
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['savefig.facecolor'] = 'white'
plt.rcParams['savefig.edgecolor'] = 'white'
plt.rcParams['font.family'] = 'STIXGeneral'
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.formatter.use_mathtext'] = True
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
GRAPH_DIR = graphics_dir("capitulo4", "referencias")
GRAPH_DIR.mkdir(parents=True, exist_ok=True)
ORIGINAL_FIGSIZE = (8, 3)


def _axis_label(text):
    labels = {
        'Cantidad de datos de entrada (n)': r'$\mathrm{Tamaño\ de\ la\ entrada}\ (n)$',
        'Cantidad de datos de entrada ($m \\cdot n$)': (
            r'$\mathrm{Cantidad\ de\ datos\ de\ entrada}\ (m\cdot n)$'
        ),
        'Número de ejecuciones': r'$\mathrm{Número\ de\ ejecuciones}$',
        'Tiempo de ejecución [s]': r'$\mathrm{Tiempo\ de\ ejecución}\ [s]$',
        'Consumo de memoria [bytes]': r'$\mathrm{Consumo\ de\ memoria}\ [bytes]$',
    }
    return labels.get(text, text)


def _title(text):
    if text == 'Complejidad teórica vs experimental':
        return 'Complejidad teórica vs. experimental'
    return text


def _format_axis_text(ax):
    for axis in (ax.xaxis, ax.yaxis):
        formatter = ticker.ScalarFormatter(useMathText=True)
        formatter.set_scientific(True)
        formatter.set_powerlimits((-2, 2))
        axis.set_major_formatter(formatter)
        axis.get_offset_text().set_fontfamily('STIXGeneral')
    ax.ticklabel_format(axis='both', style='sci', scilimits=(-2, 2))
    ax.tick_params(axis='both', labelsize=10)
    for label in (*ax.get_xticklabels(), *ax.get_yticklabels()):
        label.set_fontfamily('STIXGeneral')


def graficar_complejidad(x, y_experimental, y_teorico, nombre_archivo, ylabel, funcion,
                         titulo='Complejidad teórica vs experimental',
                         xlabel='Cantidad de datos de entrada (n)',
                         path=GRAPH_DIR,
                         legend_loc='best',
                         y_headroom=0.08):
    fig, ax = plt.subplots(figsize=ORIGINAL_FIGSIZE)
    ax.plot(
        x,
        y_experimental,
        label=rf'${funcion}\ \mathrm{{experimental}}$',
        color='#1f77b4',
        linewidth=1.5,
    )
    ax.plot(
        x,
        y_teorico,
        ':',
        label=rf'${funcion}\ \mathrm{{teórica}}$',
        color='red',
        linewidth=1.5,
    )
    ax.set_xlabel(_axis_label(xlabel))
    ax.set_ylabel(_axis_label(ylabel))
    ax.set_title(_title(titulo))
    y_min, y_max = ax.get_ylim()
    y_span = max(y_max - y_min, abs(y_max) * 0.05, 1e-12)
    ax.set_ylim(y_min, y_max + y_span * max(0, y_headroom))

    _format_axis_text(ax)

    ax.legend(
        loc=legend_loc,
        frameon=True,
        framealpha=0.9,
        facecolor='white',
        edgecolor='#E0E0E0',
    )
    ax.grid(True, color='#CFD8DC', linestyle='-', linewidth=0.6, alpha=0.55)
    for spine in ax.spines.values():
        spine.set_color('#000000')
        spine.set_linewidth(0.8)
    fig.savefig(Path(path) / nombre_archivo, dpi=500, bbox_inches="tight", pad_inches=0.05)
    plt.show()


def modelo_cuadratico(n, a, b, c):
    return a * n**2 + b * n + c

def modelo_lineal(n, a, b):
    return a * n + b

def modelo_constante(n, c):
    return c * np.ones_like(n)
