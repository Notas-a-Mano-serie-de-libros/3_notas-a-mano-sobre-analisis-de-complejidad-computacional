"""Publica y verifica las implementaciones actualizadas de cada sección."""

from __future__ import annotations

import argparse
import html
import json
import re
from collections import Counter
from pathlib import Path

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

try:
    from desarrollo.scripts.example_runner import render_runner
except ModuleNotFoundError:
    from example_runner import render_runner

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "desarrollo/scripts/data/book_code.json"
START = "<!-- book-code:start -->"
END = "<!-- book-code:end -->"


def render_permutations_example() -> str:
    """Implementa el problema descrito en el libro, sin inventar un listado PDF."""
    code = '''def generar_permutaciones(lista):
    if not lista:
        yield []
        return

    for indice, valor in enumerate(lista):
        restante = lista[:indice] + lista[indice + 1:]
        for permutacion in generar_permutaciones(restante):
            yield [valor] + permutacion


lista = [1, 2, 3]

for permutacion in generar_permutaciones(lista):
    print(permutacion)
'''
    rows = []
    for line in code.splitlines():
        attrs = (' contenteditable="plaintext-only" role="textbox" aria-label="Lista de entrada" spellcheck="false" data-editable'
                 if line.startswith("lista =") else "")
        colored = highlight(line, PythonLexer(), HtmlFormatter(nowrap=True)).rstrip("\n") or " "
        rows.append(f'<span class="python-code-line" data-code-line{attrs}>{colored}</span>')
    return (
        "El ejemplo del libro consiste en generar todos los reordenamientos posibles de una lista. "
        "La siguiente implementación en Python explora las elecciones de cada posición y devuelve cada permutación.\n\n"
        '<div class="example-runner" data-example-runner><details open><summary>Ver código y editar entradas</summary>'
        '<input type="hidden" data-runner-language value="python">'
        '<p>Solo la línea de entrada resaltada es editable.</p>'
        '<div class="python-code-editor highlight" data-language="python" aria-label="Código Python · Generación de permutaciones">'
        '<pre><code>' + "".join(rows) + '</code></pre></div>'
        '<p class="runtime-credit" data-runtime-credit="python">Python se ejecuta en tu navegador con '
        '<a href="https://pyodide.org/en/stable/" target="_blank" rel="noopener">Pyodide</a>.</p>'
        '<div class="example-runner-actions"><button type="button" data-run>Ejecutar</button>'
        '<button type="button" data-stop disabled>Detener</button>'
        '<button type="button" data-reset>Reestablecer</button></div>'
        '<p data-status role="status">Listo para ejecutar.</p>'
        '<pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre>'
        '</details></div>'
    )


def format_state(state: str) -> str:
    return state if "\\(" in state else f"`{state}`"


def render(listings: list[dict], level: int = 4, detail: dict | None = None, *, include_walkthrough: bool = True, permutations_example: bool = False, minimal_example: bool = False) -> str:
    parts = [START]
    if permutations_example:
        parts.append(render_permutations_example())
    elif not listings:
        parts.append("El libro no incluye un listado de implementación para este tema.")
    for listing in listings:
        if minimal_example:
            parts.append(render_runner(listing, executable_only=True))
            continue
        algorithms = {
            247: "ordenamiento por mezcla", 262: "búsqueda secuencial",
            268: "búsqueda binaria", 273: "búsqueda binaria",
            278: "búsqueda por interpolación", 290: "búsqueda por saltos",
            298: "búsqueda exponencial", 307: "búsqueda ternaria", 312: "búsqueda ternaria",
            321: "ordenamiento burbuja básico", 323: "ordenamiento burbuja con parada anticipada",
            327: "ordenamiento por selección del máximo", 329: "ordenamiento por selección del mínimo y máximo",
            333: "ordenamiento por inserción", 341: "ordenamiento por mezcla",
            349: "ordenamiento rápido", 363: "ordenamiento radix",
        }
        algorithm = algorithms.get(listing["folio"])
        if algorithm:
            version = "recursiva" if listing["folio"] in {247, 273, 307, 341, 349} else "iterativa"
            article = "de la" if algorithm.startswith("búsqueda") else "del"
            parts.append(f"A continuación, se presenta la implementación {version} estándar {article} **{algorithm}**, aplicada sobre un arreglo de números enteros.")
        else:
            parts.append("#" * level + " " + listing["title"])
        executable_only = listing["folio"] in {247, 254, 262, 268, 273, 278, 290, 298, 307, 312, 321, 323, 327, 329, 333, 341, 349, 363, "shell"}
        parts.append(render_runner(listing, executable_only=executable_only))
        if listing.get("explanation"):
            parts.append("**Explicación:** " + listing["explanation"])
        if listing.get("note"):
            parts.append('!!! note "Explicación de la implementación"\n    ' + listing["note"])
        if not executable_only and include_walkthrough:
            example = '??? example "Ejemplo paso a paso"\n    Entrada: `' + listing["example"] + "`."
            if listing.get("desktop_trace"):
                trace = listing["desktop_trace"]
                columns = trace["columns"]
                example += "\n\n    **Prueba de escritorio**\n\n    | " + " | ".join(columns) + " |\n"
                example += "    | " + " | ".join("---" for _ in columns) + " |\n"
                example += "\n".join("    | " + " | ".join(row) + " |" for row in trace["rows"])
                example += "\n\n    " + trace["legend"]
            else:
                example += "\n\n    | Estado | Acción o resultado |\n    | --- | --- |\n"
                example += "\n".join(f"    | {format_state(state)} | {action} |" for state, action in listing["trace"])
            parts.append(example)

    parts.append(END)
    return "\n\n".join(parts)


def sync(check: bool = False) -> list[str]:
    errors = []
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    if check:
        reference = json.loads((ROOT / "desarrollo/scripts/data/book_pdf_listings.json").read_text())
        # Pygments puede serializar comillas como texto literal o como
        # entidades HTML según la versión instalada; ambas representaciones
        # producen el mismo código en el navegador.
        normalize = lambda code: re.sub(r"\s+", "", html.unescape(code))
        expected = Counter((item["page"], item["folio"], normalize(item["code"])) for item in reference["listings"])
        actual = Counter((page, item["folio"], normalize(item["code"])) for page, items in catalog["pages"].items() for item in items if item["folio"] != "shell")
        if expected != actual or reference["source_sha256"] != catalog["source_sha256"]:
            errors.append("Los algoritmos de Pages difieren de los listados del PDF actualizado.")
    for relative, listings in catalog["pages"].items():
        path = ROOT / "docs/capitulos" / relative
        source = path.read_text(encoding="utf-8")
        detail = catalog["page_details"][relative]
        expected = render(
            listings, 5 if relative.startswith("capitulo-6/") else 4, detail,
            include_walkthrough=not relative.startswith("capitulo-2/"),
            permutations_example=relative == "capitulo-2/9-complejidad-factorial.md",
            minimal_example=relative.startswith("capitulo-4/"),
        )
        marked = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
        if check:
            match = marked.search(source)
            if not match or normalize(match.group()) != normalize(expected):
                errors.append(f"{relative}: código diferente al listado del libro")
            outside = marked.sub("", source)
            if re.search(r"^\s*```(?:java|python|c|text)\s*$", outside, re.M):
                errors.append(f"{relative}: implementación adicional fuera del libro")
            for old, new in detail["patches"]:
                if old != new and old in outside and new not in outside:
                    errors.append(f"{relative}: explicación anterior incompatible con el listado")
            continue
        if marked.search(source):
            source = marked.sub(lambda _, expected=expected: expected, source)
        else:
            tabs = re.compile(r'^=== "Pseudocódigo"\n.*?(?=^#{2,6} |^<nav |\Z)', re.M | re.S)
            if not tabs.search(source):
                raise ValueError(f"No se encontró el listado en {relative}")
            source = tabs.sub(lambda _, expected=expected: expected + "\n\n", source, count=1)
        for old, new in detail["patches"]:
            if new not in source:
                source = source.replace(old, new)
        path.write_text(source, encoding="utf-8")
    return errors


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    errors = sync(args.check)
    if errors:
        raise SystemExit("\n".join(errors))
    print("Listados del libro verificados." if args.check else "Listados del libro sincronizados.")
