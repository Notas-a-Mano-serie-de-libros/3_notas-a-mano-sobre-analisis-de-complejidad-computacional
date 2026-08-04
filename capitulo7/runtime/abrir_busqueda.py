from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path


NOTEBOOKS = {
    "comparacion": "0_comparacion_busquedas.ipynb",
    "secuencial": "1_busqueda_secuencial.ipynb",
    "binaria": "2_busqueda_binaria.ipynb",
    "interpolacion": "3_busqueda_interpolacion.ipynb",
    "saltos": "4_busqueda_saltos.ipynb",
    "exponencial": "5_busqueda_exponencial.ipynb",
    "ternaria": "6_busqueda_ternaria.ipynb",
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Abre una simulación del capítulo 7 en Voilà, con el código oculto.",
    )
    parser.add_argument(
        "busqueda",
        choices=NOTEBOOKS,
        help="Simulación que se abrirá.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8866,
        help="Puerto local para Voilà.",
    )
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Inicia Voilà sin abrir el navegador automáticamente.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    project_dir = Path(__file__).resolve().parent
    notebook = project_dir / "notebooks" / NOTEBOOKS[args.busqueda]

    if not notebook.exists():
        print(f"No se encontró la libreta: {notebook}", file=sys.stderr)
        return 1

    if importlib.util.find_spec("voila") is None:
        print(
            "Voilà no está instalado. Ejecute: python3 -m pip install voila ipywidgets",
            file=sys.stderr,
        )
        return 1

    command = [
        sys.executable,
        "-m",
        "voila",
        str(notebook),
        "--VoilaConfiguration.strip_sources=True",
        f"--port={args.port}",
    ]

    if args.no_browser:
        command.append("--no-browser")

    return subprocess.call(command, cwd=project_dir.parent)


if __name__ == "__main__":
    raise SystemExit(main())
