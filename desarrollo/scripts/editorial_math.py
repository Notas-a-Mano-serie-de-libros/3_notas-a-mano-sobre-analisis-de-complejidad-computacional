"""Normalización editorial de productos explícitos en expresiones LaTeX."""

from __future__ import annotations

import re
from pathlib import Path

MATH_EXPRESSION = re.compile(r"(\\\[.*?\\\]|\\\(.*?\\\))", re.DOTALL)

# Expresiones que suelen aparecer en prosa sin los delimitadores que necesita
# MathJax. Se mantienen deliberadamente acotadas para no tocar código, enlaces
# ni nombres de funciones.
PLAIN_COMPLEXITY = re.compile(
    # Mantener cada alternativa sin cuantificadores anidados evita el
    # retroceso exponencial señalado por CodeQL para textos adversariales.
    r"(?<![\\w\\])O\s*\(n\s+log\s*\(n\)\)|"
    r"(?<![\\w\\])(?:O|Ω|Theta|Omega|log)\s*\([^()\n]*\)|"
    r"(?<![\\w\\])O\s*\([^()\n]*√n[^()\n]*\)|"
    r"(?<![\\w\\])(?:√n|n²|n³)"
)


def _format_plain_complexity(match: re.Match[str]) -> str:
    value = match.group(0)
    # Unicode habitual en los apuntes -> sintaxis LaTeX equivalente.
    value = value.replace("√n", r"\sqrt{n}")
    value = value.replace("n²", r"n^2").replace("n³", r"n^3")
    value = re.sub(r"\bO\s*\(\s*n\s+log\s*\(\s*n\s*\)\s*\)", lambda _: r"O(n \cdot \log(n))", value)
    value = re.sub(r"\bO\s*\(\s*n²\s*\)", lambda _: r"O(n^2)", value)
    value = re.sub(r"\bO\s*\(\s*n³\s*\)", lambda _: r"O(n^3)", value)
    value = re.sub(r"\bO\s*\(\s*√n\s*\)", lambda _: r"O(\sqrt{n})", value)
    return rf"\({value}\)"


def normalize_plain_math(document: str) -> str:
    """Delimita fórmulas de complejidad escritas accidentalmente como texto."""
    lines: list[str] = []
    in_fence = False
    in_display = False
    for line in document.splitlines(keepends=True):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            lines.append(line)
            continue
        if line.strip() == r"\[":
            in_display = True
            lines.append(line)
            continue
        if line.strip() == r"\]":
            in_display = False
            lines.append(line)
            continue
        if in_fence or in_display or "<" in line or "`" in line or r"\(" in line or "$" in line:
            lines.append(line)
            continue
        stripped = line.strip()
        # Una ecuación aislada se presenta como bloque, conservando su puntuación.
        if re.match(r"^(?:T|S|C)\([^)]*\)\s*=", stripped) or re.match(r"^(?:T|S|C)\([^)]*\)\\in", stripped):
            ending = ""
            if stripped.endswith("."):
                stripped, ending = stripped[:-1], "."
            stripped = re.sub(r"(?<![A-Za-z])c(?=\s*(?:n|2\^))", r"c \\cdot ", stripped)
            lines.append(f"\\[\n{stripped}\n\\]{ending}\n")
            continue
        lines.append(PLAIN_COMPLEXITY.sub(_format_plain_complexity, line))
    return "".join(lines)


def normalize_expression(expression: str) -> str:
    r"""Añade ``\cdot`` solo en formas inequívocas de multiplicación."""
    expression = re.sub(
        r"(?<![\\\w.^])(\d+(?:\.\d+)?)(?=(?:[A-Za-z]|\\(?:log|sqrt)))",
        r"\1 \\cdot ",
        expression,
    )
    expression = re.sub(
        r"(?<![\\\w])([A-Za-z](?:\^\{[^{}]+\}|\^[A-Za-z0-9]+)?)\s*(?=\\log)",
        r"\1 \\cdot ",
        expression,
    )
    expression = re.sub(
        r"\b([a-z])([A-Z])(?=\s*(?:\\!\s*)?(?:\\left)?\()",
        r"\1 \\cdot \2",
        expression,
    )
    expression = re.sub(r"\)\s*(?=\()", r") \\cdot ", expression)
    expression = re.sub(r"\b([ndk])\s*(?=\()", r"\1 \\cdot ", expression)
    expression = re.sub(
        r"\b(nd|mn|kn)\b",
        lambda match: rf"{match.group(1)[0]} \cdot {match.group(1)[1]}",
        expression,
    )
    expression = re.sub(r"\b([ck])\\,\s*(?=[gn]\b)", r"\1 \\cdot ", expression)
    expression = re.sub(r"\)\s*\\,\s*(?=[A-Za-z]\s*\()", r") \\cdot ", expression)
    expression = re.sub(
        r"(n(?:\^\{[^{}]+\}|\^[A-Za-z0-9]+))\s+(?=\d+\^)",
        r"\1 \\cdot ",
        expression,
    )
    return expression


def normalize_math_products(document: str) -> str:
    return MATH_EXPRESSION.sub(lambda match: normalize_expression(match.group(0)), document)


def implicit_product_issues(document: str) -> list[str]:
    """Retorna expresiones que cambiarían al aplicar la normalización."""
    issues = []
    for match in MATH_EXPRESSION.finditer(document):
        expression = match.group(0)
        if normalize_expression(expression) != expression:
            issues.append(expression)
    return issues


def plain_math_issues(document: str) -> list[str]:
    """Detecta fórmulas de complejidad que quedaron fuera de MathJax."""
    issues: list[str] = []
    in_fence = False
    in_display = False
    for line in document.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if line.strip() == r"\[":
            in_display = True
            continue
        if line.strip() == r"\]":
            in_display = False
            continue
        if in_fence or in_display or "<" in line or "`" in line:
            continue
        plain = MATH_EXPRESSION.sub("", line)
        if PLAIN_COMPLEXITY.search(plain) or re.search(r"\b(?:T|S|C)\([^)]*\)\s*=", plain):
            issues.append(line.strip())
    return issues


def normalize_file(path: Path) -> bool:
    source = path.read_text(encoding="utf-8")
    normalized = normalize_plain_math(normalize_math_products(source))
    if normalized == source:
        return False
    path.write_text(normalized, encoding="utf-8")
    return True


__all__ = [
    "implicit_product_issues",
    "plain_math_issues",
    "normalize_expression",
    "normalize_file",
    "normalize_math_products",
    "normalize_plain_math",
]
