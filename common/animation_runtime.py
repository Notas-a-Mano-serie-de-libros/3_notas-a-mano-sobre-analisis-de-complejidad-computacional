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
            "@font-face{font-family:'KaTeX_Main';src:url('https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/fonts/KaTeX_Main-Regular.woff2') format('woff2');font-weight:400;font-style:normal;}"
            "@font-face{font-family:'KaTeX_Main';src:url('https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/fonts/KaTeX_Main-Bold.woff2') format('woff2');font-weight:700;font-style:normal;}"
            "@font-face{font-family:'KaTeX_Math';src:url('https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/fonts/KaTeX_Math-Italic.woff2') format('woff2');font-weight:400;font-style:italic;}"
            ".formula-renderer{width:100%;box-sizing:border-box;overflow:visible;"
            "font-family:'KaTeX_Main','Latin Modern Roman','Computer Modern Serif','STIX Two Text','STIXGeneral',serif;"
            "font-size:16px;font-weight:400;line-height:1.25;"
            "color:#111111;}"
            "@media (prefers-color-scheme:dark){.formula-renderer{color:#f2f2f2;}}"
            ".formula-line{display:flex;align-items:center;gap:4px;min-height:24px;white-space:nowrap;}"
            ".formula-frac{display:inline-flex;flex-direction:column;align-items:center;"
            "vertical-align:middle;line-height:1.02;margin:0 2px;font-size:.96em;}"
            ".formula-num{border-bottom:1px solid currentColor;padding:0 3px 1px;}"
            ".formula-den{padding:1px 3px 0;}"
            ".formula-floor{display:inline-flex;align-items:center;gap:1px;}"
            ".formula-root{display:inline-flex;align-items:center;gap:2px;}"
            ".formula-sub{font-size:.68em;vertical-align:sub;line-height:0;}"
            ".formula-sup{font-size:.68em;vertical-align:super;line-height:0;}"
            ".formula-var{font-family:'KaTeX_Math','STIX Two Math','STIXGeneral',serif;font-style:italic;}"
            ".formula-op,.formula-text{font-family:'KaTeX_Main','STIX Two Text','STIXGeneral',serif;font-style:normal;}"
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
    line_break = "\uE000"
    text = re.sub(r"\\\\(?:\[[^\]]+\])?", line_break, text)
    text = re.sub(r"\s+", " ", text)
    return [line.strip() for line in text.split(line_break) if line.strip()]


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
        "min": '<span class="formula-op">min</span>',
        "max": '<span class="formula-op">max</span>',
        "log": '<span class="formula-op">log</span>',
        "bmod": '<span class="formula-op">mod</span>',
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
            elif char.isalpha():
                parts.append(self.variable())
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
        return f'<span class="formula-text">{escape(self.text[start:self.index - 1])}</span>'

    def variable(self):
        start = self.index
        while self.index < len(self.text) and self.text[self.index].isalpha():
            self.index += 1
        return f'<span class="formula-var">{escape(self.text[start:self.index])}</span>'

    def next_text(self):
        if self.index >= len(self.text):
            return ""
        char = self.text[self.index]
        self.index += 1
        return escape(char)

    def peek(self):
        return self.text[self.index] if self.index < len(self.text) else ""
