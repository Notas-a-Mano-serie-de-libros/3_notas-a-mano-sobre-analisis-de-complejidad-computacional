#!/usr/bin/env python3
"""
Abre un notebook del proyecto en el entorno correcto.

Si el archivo existe localmente, lo abre con Jupyter Lab (capítulos 2–6)
o con Voilà con el código oculto (capítulos 7–8, animaciones interactivas).
Si no existe localmente o se pasa --colab, lo abre en Google Colab.

Uso
---
    python3 abrir.py ALIAS
    python3 abrir.py --lista
    python3 abrir.py --colab ALIAS

Ejemplos
--------
    python3 abrir.py 2/constante
    python3 abrir.py 3/big-o
    python3 abrir.py 4/ejemplo3
    python3 abrir.py 7/secuencial
    python3 abrir.py 8/mezcla
    python3 abrir.py --colab 3/theta
    python3 abrir.py --lista
"""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
import webbrowser
from pathlib import Path

# ---------------------------------------------------------------------------
# Constantes del repositorio
# ---------------------------------------------------------------------------

_REPO = (
    "Notas-a-Mano-serie-de-libros"
    "/3_notas-a-mano-sobre-analisis-de-complejidad-computacional"
)
_COLAB_BASE = f"https://githubtocolab.com/{_REPO}/blob/main/"

# Capítulos que usan Voilà (animaciones interactivas con código oculto)
_VOILA_CAPS = {"7", "8"}

# ---------------------------------------------------------------------------
# Catálogo de notebooks  alias → ruta relativa desde la raíz del proyecto
# ---------------------------------------------------------------------------

NOTEBOOKS: dict[str, str] = {
    # ------------------------------------------------------------------
    # Capítulo 2 – Fundamentos del análisis de algoritmos
    # ------------------------------------------------------------------
    "2/constante":      "simulaciones/capitulo2/notebooks/1_complejidad_constante.ipynb",
    "2/logaritmica":    "simulaciones/capitulo2/notebooks/2_complejidad_logaritmica.ipynb",
    "2/lineal":         "simulaciones/capitulo2/notebooks/3_complejidad_lineal.ipynb",
    "2/log-lineal":     "simulaciones/capitulo2/notebooks/4_complejidad_log_lineal.ipynb",
    "2/cuadratica":     "simulaciones/capitulo2/notebooks/5_complejidad_cuadratica.ipynb",
    "2/cubica":         "simulaciones/capitulo2/notebooks/6_complejidad_cubica.ipynb",
    "2/polinomial-general": "simulaciones/capitulo2/notebooks/7_complejidad_polinomial_general.ipynb",
    "2/exponencial":    "simulaciones/capitulo2/notebooks/8_complejidad_exponencial.ipynb",
    "2/factorial":      "simulaciones/capitulo2/notebooks/9_complejidad_factorial.ipynb",
    "2/alta-temporal":  "recursos/graficas/capitulo2/analisis_alta_complejidad_temporal.ipynb",
    "2/alta-espacial":  "recursos/graficas/capitulo2/analisis_alta_complejidad_espacial.ipynb",
    "2/comparacion":    "recursos/graficas/capitulo2/comparacion_complejidades_teoricas.ipynb",
    "2/polinomica":     "recursos/graficas/capitulo2/complejidad_polinomica.ipynb",
    # ------------------------------------------------------------------
    # Capítulo 3 – Notación asintótica
    # ------------------------------------------------------------------
    "3/big-o":          "simulaciones/capitulo3/notebooks/1_notacion_big_o.ipynb",
    "3/little-o":       "simulaciones/capitulo3/notebooks/2_notacion_little_o.ipynb",
    "3/big-omega":      "simulaciones/capitulo3/notebooks/3_notacion_big_omega.ipynb",
    "3/little-omega":   "simulaciones/capitulo3/notebooks/4_notacion_little_omega.ipynb",
    "3/theta":          "simulaciones/capitulo3/notebooks/5_notacion_theta.ipynb",
    "3/representacion": "simulaciones/capitulo3/notebooks/notacion_asintotica_representacion_generica.ipynb",
    # ------------------------------------------------------------------
    # Capítulo 4 – Análisis de algoritmos estructurados
    # ------------------------------------------------------------------
    "4/ejemplo1":       "simulaciones/capitulo4/notebooks/ejemplo1_(sumar_numeros).ipynb",
    "4/ejemplo2":       "simulaciones/capitulo4/notebooks/ejemplo2_(imprimir_elementos_arreglo).ipynb",
    "4/ejemplo3":       "simulaciones/capitulo4/notebooks/ejemplo3_(imprimir_elementos_matriz).ipynb",
    "4/ejemplo4":       "simulaciones/capitulo4/notebooks/ejemplo4_(inicializar_matriz_variable).ipynb",
    "4/ejemplo5":       "simulaciones/capitulo4/notebooks/ejemplo5_(ciclos_incremento_no_lineal).ipynb",
    "4/ejemplo7":       "simulaciones/capitulo4/notebooks/ejemplo7_(ciclo_sin_dependencia).ipynb",
    "4/ejemplo9":       "simulaciones/capitulo4/notebooks/ejemplo9_(complejidad_oculta).ipynb",
    # ------------------------------------------------------------------
    # Capítulo 6 – Análisis de algoritmos recursivos
    # ------------------------------------------------------------------
    "6/fibonacci":      "simulaciones/capitulo6/notebooks/comparacion_fibonacci.ipynb",
    "6/recursion":      "simulaciones/capitulo6/notebooks/ejemplo_recursion.ipynb",
    # ------------------------------------------------------------------
    # Capítulo 7 – Algoritmos de búsqueda  (Voilà)
    # ------------------------------------------------------------------
    "7/comparacion":    "simulaciones/capitulo7/notebooks/0_comparacion_busquedas.ipynb",
    "7/secuencial":     "simulaciones/capitulo7/notebooks/1_busqueda_secuencial.ipynb",
    "7/binaria":        "simulaciones/capitulo7/notebooks/2_busqueda_binaria.ipynb",
    "7/interpolacion":  "simulaciones/capitulo7/notebooks/3_busqueda_interpolacion.ipynb",
    "7/saltos":         "simulaciones/capitulo7/notebooks/4_busqueda_saltos.ipynb",
    "7/exponencial":    "simulaciones/capitulo7/notebooks/5_busqueda_exponencial.ipynb",
    "7/ternaria":       "simulaciones/capitulo7/notebooks/6_busqueda_ternaria.ipynb",
    # ------------------------------------------------------------------
    # Capítulo 8 – Algoritmos de ordenamiento  (Voilà)
    # ------------------------------------------------------------------
    "8/comparacion":    "simulaciones/capitulo8/notebooks/0_comparacion_ordenamientos.ipynb",
    "8/burbuja":        "simulaciones/capitulo8/notebooks/1_ordenamiento_burbuja.ipynb",
    "8/seleccion":      "simulaciones/capitulo8/notebooks/2_ordenamiento_seleccion.ipynb",
    "8/insercion":      "simulaciones/capitulo8/notebooks/3_ordenamiento_insercion.ipynb",
    "8/shell":          "simulaciones/capitulo8/notebooks/4_ordenamiento_shell.ipynb",
    "8/mezcla":         "simulaciones/capitulo8/notebooks/5_ordenamiento_mezcla.ipynb",
    "8/rapido":         "simulaciones/capitulo8/notebooks/6_ordenamiento_rapido.ipynb",
    "8/radix":          "simulaciones/capitulo8/notebooks/7_ordenamiento_radix.ipynb",
}

# ---------------------------------------------------------------------------
# Lógica de apertura
# ---------------------------------------------------------------------------

_ROOT = Path(__file__).resolve().parent


def _capitulo(alias: str) -> str:
    return alias.split("/")[0]


def _usar_voila(alias: str) -> bool:
    return _capitulo(alias) in _VOILA_CAPS


def _abrir_local(alias: str, notebook: Path, port: int) -> int:
    if _usar_voila(alias):
        if importlib.util.find_spec("voila") is None:
            print(
                "Voilà no está instalado.\n"
                "Instálelo con:  pip install voila ipywidgets",
                file=sys.stderr,
            )
            return 1
        return subprocess.call(
            [
                sys.executable,
                "-m",
                "voila",
                str(notebook),
                "--VoilaConfiguration.strip_sources=True",
                f"--port={port}",
            ],
            cwd=_ROOT,
        )

    # Para los demás capítulos abre Jupyter Lab; si no está disponible,
    # intenta con Jupyter Notebook clásico. Pages usa Colab como ruta web.
    for mod, flag in [("jupyterlab", "lab"), ("notebook", "notebook")]:
        if importlib.util.find_spec(mod) is not None:
            return subprocess.call(
                [sys.executable, "-m", "jupyter", flag, str(notebook)],
                cwd=_ROOT,
            )

    print(
        "Jupyter Lab no está instalado.\n"
        "Instálelo con:  pip install jupyterlab",
        file=sys.stderr,
    )
    return 1


def _abrir_colab(alias: str, rel_path: str) -> int:
    url = _COLAB_BASE + rel_path
    print(f"Abriendo en Google Colab:\n  {url}")
    webbrowser.open(url)
    return 0


def _listar() -> None:
    """Imprime el catálogo de alias disponibles."""
    cap_prev = ""
    for alias, ruta in sorted(NOTEBOOKS.items()):
        cap = _capitulo(alias)
        if cap != cap_prev:
            print(f"\n  Capítulo {cap}:")
            cap_prev = cap
        existe = "✓" if (_ROOT / ruta).exists() else " "
        print(f"    [{existe}] {alias:<22}  →  {ruta}")
    print(
        "\n  [✓] = disponible localmente   [ ] = solo disponible en Colab\n"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="abrir.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "alias",
        nargs="?",
        metavar="ALIAS",
        help=(
            "Alias del notebook que se desea abrir "
            "(p. ej. '3/big-o', '7/secuencial'). "
            "Ejecute --lista para ver todos los disponibles."
        ),
    )
    parser.add_argument(
        "--colab",
        action="store_true",
        help=(
            "Fuerza la apertura en Google Colab aunque el archivo "
            "exista localmente."
        ),
    )
    parser.add_argument(
        "--lista",
        action="store_true",
        help="Muestra todos los notebooks disponibles con su alias.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8866,
        metavar="PUERTO",
        help="Puerto local para Voilà (capítulos 7 y 8). Por defecto: 8866.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.lista:
        _listar()
        return 0

    if not args.alias:
        _build_parser().print_help()
        return 1

    if args.alias not in NOTEBOOKS:
        print(
            f"Error: alias '{args.alias}' no encontrado.\n"
            "Ejecute  python3 abrir.py --lista  para ver los disponibles.",
            file=sys.stderr,
        )
        return 1

    rel_path = NOTEBOOKS[args.alias]
    local_path = _ROOT / rel_path

    if not args.colab and local_path.exists():
        print(f"Abriendo localmente: {local_path.relative_to(_ROOT)}")
        return _abrir_local(args.alias, local_path, args.port)

    if not local_path.exists() and not args.colab:
        print(f"Archivo no encontrado localmente: {rel_path}")

    return _abrir_colab(args.alias, rel_path)


if __name__ == "__main__":
    raise SystemExit(main())
