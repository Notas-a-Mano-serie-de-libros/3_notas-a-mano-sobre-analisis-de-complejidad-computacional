"""Traducciones de los listados Java publicados en cada sección."""

from __future__ import annotations

import json
import re
from pathlib import Path

DATA = json.loads((Path(__file__).parent / "data/book_translations.json").read_text())


def condition_python(code: str) -> str:
    """Conserva el orden de los fragmentos condicionales del libro."""
    lines = []
    for raw in code.splitlines():
        s = raw.strip()
        if s == "}":
            continue
        if s.startswith("//"):
            lines.append("    pass  # " + s[2:].strip())
        elif s.startswith("if (") or s.startswith("} else if ("):
            prefix = "if " if s.startswith("if") else "elif "
            expr = s[s.index("(") + 1 : s.rfind(")")]
            expr = expr.replace("!", "not ").replace("&&", "and").replace("||", "or")
            lines.append(prefix + expr + ":")
        elif s.startswith("} else"):
            lines.append("else:")
        else:
            statement = s.split("//")[0].strip().rstrip(";")
            lines.append("    " + statement)
    return "\n".join(lines)


def pseudocode(python: str) -> str:
    """Notación estructurada; rango(inicio, fin, paso) excluye fin."""
    lines = []
    for raw in python.splitlines():
        indent = raw[: len(raw) - len(raw.lstrip())]
        s = raw.strip()
        if s.startswith("from "):
            continue
        s = re.sub(r"^def (.*):$", r"función \1", s)
        s = re.sub(r"^elif (.*):$", r"si no, si \1 entonces", s)
        s = re.sub(r"^if (.*):$", r"si \1 entonces", s)
        s = re.sub(r"^while (.*):$", r"mientras \1", s)
        s = re.sub(r"^for (\w+) in (.*):$", r"para \1 en \2", s)
        s = s.replace("else:", "si no").replace("return", "retornar")
        s = s.replace("raise ", "error ").replace("pass", "sin operaciones")
        s = s.replace("True", "verdadero").replace("False", "falso").replace("None", "nulo")
        s = s.replace(" and ", " y ").replace(" or ", " o ").replace("not ", "no ")
        s = s.replace("range(", "rango(").replace("len(", "longitud(").replace("print(", "imprimir(")
        s = s.replace("isqrt(", "raízEntera(").replace(" // ", " div ")
        s = re.sub(r"(?<![<>=!]) = (?!=)", " ← ", s)
        lines.append(indent + s)
    return "\n".join(lines).strip()


def translations(listing: dict) -> dict[str, str]:
    folio = str(listing["folio"])
    if folio in ("170", "171", "172", "173"):
        python = condition_python(listing["code"])
        c = listing["code"]
    else:
        python = DATA["python_by_folio"][folio]
        c = DATA["c_by_folio"][folio]
    return {"Java": listing["code"], "Pseudocódigo": pseudocode(python), "Python": python, "C": c}


def language_tabs(listing: dict) -> str:
    try:
        from scripts.java_examples import java_example
    except ModuleNotFoundError:
        from java_examples import java_example
    names = {"Java": "java", "Pseudocódigo": "text", "Python": "python", "C": "c"}
    result = []
    for label, code in translations(listing).items():
        if label == "Java":
            code = java_example(listing)[0]
        lines = "\n".join("    " + line if line else "" for line in code.splitlines())
        result.append(f'=== "{label}"\n\n    ```{names[label]}\n{lines}\n    ```')
    return "\n\n".join(result)
