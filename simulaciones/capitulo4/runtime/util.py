from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import ticker

try:
    from common.graphics import graphics_dir
except ModuleNotFoundError:
    def graphics_dir(chapter, *parts):
        root = next(
            (
                base for base in (Path.cwd(), *Path.cwd().parents)
                if (base / chapter).is_dir()
            ),
            Path.cwd(),
        )
        return root / Path("recursos/imagenes") / chapter / "generadas" / Path(*parts)

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
GRAPH_DIR = graphics_dir('capitulo4', 'referencias')
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
