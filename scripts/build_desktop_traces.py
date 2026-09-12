"""Construye pruebas de escritorio de búsquedas y ordenamientos con sus ejemplos."""

from __future__ import annotations

import ast
import copy
import inspect
import json
import re
import sys
from pathlib import Path

try:
    from scripts.book_code_languages import translations
except ModuleNotFoundError:
    from book_code_languages import translations

CATALOG = Path(__file__).parent / "data/book_code.json"


def desktop_trace(listing: dict, search: bool) -> dict:
    source = translations(listing)["Python"]
    filename = "<desktop-example>"
    env: dict = {}
    exec(compile(source, filename, "exec"), env)
    example = listing["example"]
    arr = ast.literal_eval(re.search(r"arr = (\[[^\]]*\])", example)[1])
    original = arr.copy()
    fn = env["buscar" if search else "ordenar"]
    args = {"arr": arr}
    for name in inspect.signature(fn).parameters:
        if name != "arr":
            args[name] = int(re.search(r"\b" + name + r" = (-?\d+)", example)[1])
    events = []
    pending = {}
    lines = source.splitlines()

    def record(frame, action, result=None):
        level = 0
        parent = frame.f_back
        while parent:
            if parent.f_code.co_filename == filename:
                level += 1
            parent = parent.f_back
        local = copy.deepcopy(dict(frame.f_locals))
        # Python avoids shadowing its min/max functions in Radix.
        local = {{"minimo": "min", "maximo": "max"}.get(k, k): value for k, value in local.items()}
        events.append((frame.f_code.co_name, level, local, action, result))

    def trace(frame, event, arg):
        if frame.f_code.co_filename != filename:
            return trace
        key = id(frame)
        if event == "call":
            record(frame, "Entrada a la llamada.")
        elif event == "line":
            if key in pending:
                record(frame, "`" + lines[pending[key] - 1].strip() + "`")
            pending[key] = frame.f_lineno
        elif event == "return":
            line = pending.pop(key, None)
            action = ("`" + lines[line - 1].strip() + "`; " if line else "") + "Termina la llamada."
            record(frame, action, "true" if arg is True else "false" if arg is False else "sin valor" if arg is None else str(arg))
        return trace

    previous = sys.gettrace()
    try:
        sys.settrace(trace)
        result = fn(**args)
    finally:
        sys.settrace(previous)
    if search:
        assert result == (args["x"] in original)
    else:
        assert arr == sorted(original)
    names = []
    for _, _, values, _, _ in events:
        for name in values:
            if name not in names:
                names.append(name)
    rows = []
    for i, (method, level, values, action, result) in enumerate(events, 1):

        def cell(value):
            if isinstance(value, bool):
                return "true" if value else "false"
            return str(value)

        rows.append([str(i), method, str(level), *[cell(values[n]) if n in values else "—" for n in names], action, result or "—"])
    return {
        "columns": ["Paso", "Método", "Profundidad", *names, "Operación ejecutada", "Retorno"],
        "rows": rows,
        "legend": "Cada fila muestra el estado después de la operación indicada de la traducción Python de esta variante. «—» indica una variable aún no declarada en esa llamada o un retorno todavía pendiente. La profundidad inicial es 0; cada llamada anidada la incrementa en 1.",
    }


def main():
    catalog = json.loads(CATALOG.read_text())
    count = 0
    for page, listings in catalog["pages"].items():
        if not page.startswith(("capitulo-7/", "capitulo-8/")):
            continue
        for listing in listings:
            if listing["folio"] != 278:  # Conserva la traza manual con las ecuaciones.
                listing["desktop_trace"] = desktop_trace(listing, page.startswith("capitulo-7/"))
            count += 1
    traces = {
        listing["folio"]: listing["desktop_trace"]
        for page, listings in catalog["pages"].items()
        if page.startswith(("capitulo-7/", "capitulo-8/"))
        for listing in listings
    }
    traces[247] = traces[341]
    for listings in catalog["pages"].values():
        for listing in listings:
            if listing["folio"] in traces:
                listing["desktop_trace"] = copy.deepcopy(traces[listing["folio"]])
    CATALOG.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n")
    print(f"{count} pruebas de escritorio de búsquedas y ordenamientos verificadas.")


if __name__ == "__main__":
    main()
