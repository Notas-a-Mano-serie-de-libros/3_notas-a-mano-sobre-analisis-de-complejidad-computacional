"""Normalización editorial de productos explícitos en expresiones LaTeX."""

from __future__ import annotations

import re
from pathlib import Path


MATH_EXPRESSION = re.compile(r"(\\\[.*?\\\]|\\\(.*?\\\))", re.DOTALL)


def normalize_expression(expression: str) -> str:
    """Añade ``\cdot`` solo en formas inequívocas de multiplicación."""
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


def normalize_file(path: Path) -> bool:
    source = path.read_text(encoding="utf-8")
    normalized = normalize_math_products(source)
    if normalized == source:
        return False
    path.write_text(normalized, encoding="utf-8")
    return True


__all__ = [
    "implicit_product_issues",
    "normalize_expression",
    "normalize_file",
    "normalize_math_products",
]
