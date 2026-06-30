from __future__ import annotations

import re
import time
from html import escape


def set_disabled(controls, disabled):
    for control in controls:
        control.disabled = disabled


def pause(seconds, colab_output=None):
    if colab_output is not None:
        colab_output.eval_js(f"new Promise(resolve => setTimeout(resolve, {int(seconds * 1000)}))")
        return
    time.sleep(seconds)


class OutputCache:
    def __init__(self):
        self.formula = object()
        self.html = object()
        self.formula_html = {}

    def render_formula_html(self, formula):
        if formula in self.formula_html:
            return self.formula_html[formula]

        lines = _formula_lines(formula)
        rows = "".join(f'<div class="formula-line">{_math_html(line)}</div>' for line in lines)
        html = (
            '<div class="formula-renderer">'
            "<style>"
            ".formula-renderer{width:100%;box-sizing:border-box;overflow:visible;"
            "font-family:'Scheherazade New','Times New Roman',serif;"
            "font-size:28px;font-weight:600;line-height:1.45;"
            "color:#111111;}"
            "@media (prefers-color-scheme:dark){.formula-renderer{color:#f2f2f2;}}"
            ".formula-line{display:flex;align-items:center;gap:8px;min-height:38px;white-space:nowrap;}"
            ".formula-frac{display:inline-flex;flex-direction:column;align-items:center;"
            "vertical-align:middle;line-height:1.05;margin:0 4px;}"
            ".formula-num{border-bottom:2px solid currentColor;padding:0 6px 3px;}"
            ".formula-den{padding:3px 6px 0;}"
            ".formula-floor{display:inline-flex;align-items:center;gap:2px;}"
            ".formula-root{display:inline-flex;align-items:center;gap:3px;}"
            ".formula-sub{font-size:.62em;vertical-align:sub;line-height:0;}"
            ".formula-sup{font-size:.62em;vertical-align:super;line-height:0;}"
            "</style>"
            f"{rows}"
            "</div>"
        )
        self.formula_html[formula] = html
        return html

    def update_formula(self, widget, formula):
        if formula == self.formula:
            return False
        widget.value = self.render_formula_html(formula) if formula else ""
        self.formula = formula
        return True

    def update_html(self, widget, html):
        if html == self.html:
            return False
        widget.value = html
        self.html = html
        return True


__all__ = [
    "OutputCache",
    "pause",
    "set_disabled",
]


def _formula_lines(formula):
    text = formula.strip()
    text = text.replace(r"\displaystyle", "")
    text = re.sub(r"\\begin\{(?:array|aligned)\}(?:\{[^{}]*\})?", "", text)
    text = re.sub(r"\\end\{(?:array|aligned)\}", "", text)
    text = re.sub(r"\\\\(?:\[[^\]]+\])?", "\n", text)
    return [line.strip() for line in text.splitlines() if line.strip()]


def _math_html(expression):
    parser = _FormulaParser(expression)
    return parser.parse()


class _FormulaParser:
    COMMANDS = {
        "approx": "≈",
        "cdot": "·",
        "times": "×",
        "leq": "≤",
        "geq": "≥",
        "neq": "≠",
        "in": "∈",
        "quad": "  ",
        "min": "min",
        "max": "max",
        "log": "log",
        "bmod": "mod",
    }

    def __init__(self, text):
        self.text = text
        self.index = 0

    def parse(self, stop=None):
        parts = []
        while self.index < len(self.text):
            char = self.text[self.index]
            if stop and char == stop:
                break
            if char == "\\":
                parts.append(self.command())
            elif char in "_^":
                parts.append(self.script(char))
            elif char == "{":
                self.index += 1
                parts.append(self.parse("}"))
                if self.index < len(self.text) and self.text[self.index] == "}":
                    self.index += 1
            elif char == "}":
                if stop == "}":
                    break
                self.index += 1
                parts.append(escape(char))
            elif char == "&":
                self.index += 1
            else:
                parts.append(escape(char))
                self.index += 1
        return "".join(parts)

    def command(self):
        self.index += 1
        start = self.index
        while self.index < len(self.text) and self.text[self.index].isalpha():
            self.index += 1
        name = self.text[start:self.index]
        if not name and self.index < len(self.text):
            char = self.text[self.index]
            self.index += 1
            return escape(char)

        if name in {"left", "right"}:
            return ""
        if name in {"text", "mathrm"}:
            return self.group_text()
        if name == "frac":
            numerator = self.group_math()
            denominator = self.group_math()
            return (
                '<span class="formula-frac">'
                f'<span class="formula-num">{numerator}</span>'
                f'<span class="formula-den">{denominator}</span>'
                "</span>"
            )
        if name == "sqrt":
            content = self.group_math()
            return f'<span class="formula-root">√<span>{content}</span></span>'
        if name == "lfloor":
            return "⌊"
        if name == "rfloor":
            return "⌋"
        if name in self.COMMANDS:
            return self.COMMANDS[name]
        if name:
            return escape(name)
        return ""

    def script(self, marker):
        self.index += 1
        css_class = "formula-sub" if marker == "_" else "formula-sup"
        content = self.group_math() if self.peek() == "{" else self.next_text()
        return f'<span class="{css_class}">{content}</span>'

    def group_math(self):
        if self.peek() != "{":
            return self.next_text()
        self.index += 1
        content = self.parse("}")
        if self.peek() == "}":
            self.index += 1
        return content

    def group_text(self):
        if self.peek() != "{":
            return ""
        self.index += 1
        start = self.index
        depth = 1
        while self.index < len(self.text) and depth:
            char = self.text[self.index]
            if char == "{":
                depth += 1
            elif char == "}":
                depth -= 1
            self.index += 1
        return escape(self.text[start:self.index - 1])

    def next_text(self):
        if self.index >= len(self.text):
            return ""
        char = self.text[self.index]
        self.index += 1
        return escape(char)

    def peek(self):
        return self.text[self.index] if self.index < len(self.text) else ""
