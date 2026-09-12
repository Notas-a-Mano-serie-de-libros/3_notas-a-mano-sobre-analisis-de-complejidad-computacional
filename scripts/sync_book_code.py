"""Publica y verifica las implementaciones actualizadas de cada sección."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    from scripts.book_code_languages import language_tabs
    from scripts.example_runner import render_runner
except ModuleNotFoundError:
    from book_code_languages import language_tabs
    from example_runner import render_runner

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "scripts/data/book_code.json"
START = "<!-- book-code:start -->"
END = "<!-- book-code:end -->"


def format_state(state: str) -> str:
    return state if "\\(" in state else f"`{state}`"


def render(listings: list[dict], level: int = 4, detail: dict | None = None) -> str:
    parts = [START]
    if not listings:
        parts.append("El libro no incluye un listado de implementación para este tema.")
    for listing in listings:
        parts.append("#" * level + " " + listing["title"])
        if listing["folio"] == "shell":
            parts.append("Implementación de ampliación del sitio (Java); no es un listado del PDF.")
        else:
            parts.append(f"Implementación basada en el libro, página {listing['folio']} (Java).")
        parts.append(language_tabs(listing))
        parts.append(
            "Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`."
        )
        if listing["folio"] in (151, 262, 290, 298, 321, 323, 327, 329, 333, 363, "shell"):
            parts.append("En C, `n` indica la longitud del arreglo y se recibe como parámetro.")
        if listing["folio"] in (153, 156, 177):
            parts.append(
                "En C, las dimensiones se reciben como parámetros; las matrices de salida las reserva el llamador. La reserva de memoria se analiza por separado de los ciclos mostrados."
            )
        if listing["folio"] == 167:
            parts.append(
                "La versión C requiere GMP (`gmp.h` y enlace con `-lgmp`) para conservar la precisión arbitraria de `BigInteger`. El llamador inicializa y libera el resultado con `mpz_init` y `mpz_clear`."
            )
        parts.append(
            "| Parámetro o variable | Significado |\n| --- | --- |\n"
            + "\n".join(f"| `{name}` | {meaning} |" for name, meaning in listing["parameters"].items())
        )
        parts.append("**Precondiciones:** " + listing["preconditions"])
        parts.append("**Resultado:** " + listing["result"])
        if listing.get("explanation"):
            parts.append("**Explicación:** " + listing["explanation"])
        if listing.get("note"):
            parts.append('!!! note "Explicación de la implementación"\n    ' + listing["note"])
        executable_only = listing["folio"] in {247, 254, 262, 268, 273, 278, 290, 298, 307, 312, 321, 323, 327, 329, 333, 341, 349, 363, "shell"}
        if not executable_only:
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
        parts.append(render_runner(listing, executable_only=executable_only))

    if detail:
        parts.append("#" * level + " Laboratorio y medición")
        parts.extend(detail["relation"])
        url = "https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/" + detail["source"]
        parts.append(f"[Consultar la adaptación y sus mediciones]({url}).")
    parts.append(END)
    return "\n\n".join(parts)


def sync(check: bool = False) -> list[str]:
    errors = []
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    for relative, listings in catalog["pages"].items():
        path = ROOT / "docs/capitulos" / relative
        source = path.read_text(encoding="utf-8")
        detail = catalog["page_details"][relative]
        expected = render(listings, 5 if relative.startswith("capitulo-6/") else 4, detail)
        marked = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
        if check:
            match = marked.search(source)
            if not match or match.group() != expected:
                errors.append(f"{relative}: código diferente al listado del libro")
            outside = marked.sub("", source)
            if re.search(r"^\s*```(?:java|python|c|text)\s*$", outside, re.M):
                errors.append(f"{relative}: implementación adicional fuera del libro")
            for old, new in detail["patches"]:
                if old != new and old in outside and new not in outside:
                    errors.append(f"{relative}: explicación anterior incompatible con el listado")
            continue
        if marked.search(source):
            source = marked.sub(lambda _: expected, source)
        else:
            tabs = re.compile(r'^=== "Pseudocódigo"\n.*?(?=^#{2,6} |^<nav |\Z)', re.M | re.S)
            if not tabs.search(source):
                raise ValueError(f"No se encontró el listado en {relative}")
            source = tabs.sub(lambda _: expected + "\n\n", source, count=1)
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
