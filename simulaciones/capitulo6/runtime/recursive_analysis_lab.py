from __future__ import annotations

import asyncio
import html
import math
import re
import time
from dataclasses import dataclass, field

import ipywidgets as widgets
from IPython.display import clear_output, display
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import CLexer, JavaLexer, PythonLexer

from common.simulation_views import action_button, actions, standard_view_styles
from common.widget_controls import (
    STANDARD_CONTROL_COLUMN_GAP,
    STANDARD_CONTROL_ROW_GAP,
    STANDARD_LABEL_CONTROL_GAP,
)

try:
    from google.colab import output as _colab_output  # type: ignore
except (ImportError, ModuleNotFoundError):
    _colab_output = None


RUNNING_IN_COLAB = _colab_output is not None


@dataclass
class Node:
    id: int
    n: int
    label: str
    depth: int
    parent: int | None
    children: list[int] = field(default_factory=list)


ALGORITHMS = {
    "factorial": {
        "name": "Factorial",
        "maximum": 12,
        "default": 5,
        "case": "El costo depende únicamente de n; los tres casos coinciden.",
        "base": r"n\leq 1\quad\Rightarrow\quad \Theta(1)",
        "calls": r"1\text{ llamada: }T(n-1)",
        "work": r"f(n)=\Theta(1)",
        "time": r"T(n)=T(n-1)+\Theta(1)\in\Theta(n)",
        "space": r"S(n)=S(n-1)+\Theta(1)\in\Theta(n)",
        "code": (
            "factorial(n):",
            "  si n ≤ 1: retornar 1",
            "  retornar n × factorial(n-1)",
        ),
    },
    "fibonacci": {
        "name": "Fibonacci ingenuo",
        "maximum": 8,
        "default": 5,
        "case": "El costo depende únicamente de n; los tres casos coinciden.",
        "base": r"n\leq 1\quad\Rightarrow\quad \Theta(1)",
        "calls": r"2\text{ llamadas: }T(n-1)+T(n-2)",
        "work": r"f(n)=\Theta(1)",
        "time": r"T(n)=T(n-1)+T(n-2)+\Theta(1)\in\Theta(\varphi^n)",
        "space": r"S(n)=\max\{S(n-1),S(n-2)\}+\Theta(1)\in\Theta(n)",
        "code": (
            "fibonacci(n):",
            "  si n ≤ 1: retornar n",
            "  retornar fibonacci(n-1) + fibonacci(n-2)",
        ),
    },
    "power_simple": {
        "name": "Potencia simple",
        "maximum": 12,
        "default": 6,
        "case": "El costo depende únicamente del exponente n.",
        "base": r"n=0\quad\Rightarrow\quad \Theta(1)",
        "calls": r"1\text{ llamada: }T(n-1)",
        "work": r"f(n)=\Theta(1)",
        "time": r"T(n)=T(n-1)+\Theta(1)\in\Theta(n)",
        "space": r"S(n)=S(n-1)+\Theta(1)\in\Theta(n)",
        "code": (
            "potencia(x, n):",
            "  si n = 0: retornar 1",
            "  retornar x × potencia(x, n-1)",
        ),
    },
    "power_fast": {
        "name": "Exponenciación rápida",
        "maximum": 64,
        "default": 16,
        "case": "El costo depende únicamente del exponente n.",
        "base": r"n=0\quad\Rightarrow\quad \Theta(1)",
        "calls": r"1\text{ llamada: }T(\lfloor n/2\rfloor)",
        "work": r"f(n)=\Theta(1)",
        "time": r"T(n)=T(\lfloor n/2\rfloor)+\Theta(1)\in\Theta(\log n)",
        "space": r"S(n)=S(\lfloor n/2\rfloor)+\Theta(1)\in\Theta(\log n)",
        "code": (
            "potenciaRapida(x, n):",
            "  si n = 0: retornar 1",
            "  mitad = potenciaRapida(x, ⌊n/2⌋)",
            "  retornar mitad² (× x si n es impar)",
        ),
    },
}


CODE_SNIPPETS = {
    "pseudocode": {
        "factorial": ("factorial(n):", "    si n ≤ 1:", "        retornar 1", "    retornar n × factorial(n - 1)"),
        "fibonacci": ("fibonacci(n):", "    si n ≤ 1:", "        retornar n", "    retornar fibonacci(n - 1) + fibonacci(n - 2)"),
        "power_simple": ("potencia(x, n):", "    si n = 0:", "        retornar 1", "    retornar x × potencia(x, n - 1)"),
        "power_fast": ("potenciaRapida(x, n):", "    si n = 0:", "        retornar 1", "    mitad = potenciaRapida(x, ⌊n / 2⌋)", "    si n es impar:", "        retornar mitad × mitad × x", "    retornar mitad × mitad"),
    },
    "python": {
        "factorial": ("def factorial(n):", "    if n <= 1:", "        return 1", "    return n * factorial(n - 1)"),
        "fibonacci": ("def fibonacci(n):", "    if n <= 1:", "        return n", "    return fibonacci(n - 1) + fibonacci(n - 2)"),
        "power_simple": ("def potencia(x, n):", "    if n == 0:", "        return 1", "    return x * potencia(x, n - 1)"),
        "power_fast": ("def potencia_rapida(x, n):", "    if n == 0:", "        return 1", "    mitad = potencia_rapida(x, n // 2)", "    if n % 2 == 1:", "        return mitad * mitad * x", "    return mitad * mitad"),
    },
    "java": {
        "factorial": ("static long factorial(int n) {", "    if (n <= 1) {", "        return 1;", "    }", "    return n * factorial(n - 1);", "}"),
        "fibonacci": ("static long fibonacci(int n) {", "    if (n <= 1) {", "        return n;", "    }", "    return fibonacci(n - 1) + fibonacci(n - 2);", "}"),
        "power_simple": ("static double potencia(double x, int n) {", "    if (n == 0) {", "        return 1;", "    }", "    return x * potencia(x, n - 1);", "}"),
        "power_fast": ("static double potenciaRapida(double x, int n) {", "    if (n == 0) {", "        return 1;", "    }", "    double mitad = potenciaRapida(x, n / 2);", "    if (n % 2 == 1) {", "        return mitad * mitad * x;", "    }", "    return mitad * mitad;", "}"),
    },
    "c": {
        "factorial": ("long factorial(int n) {", "    if (n <= 1) {", "        return 1;", "    }", "    return n * factorial(n - 1);", "}"),
        "fibonacci": ("long fibonacci(int n) {", "    if (n <= 1) {", "        return n;", "    }", "    return fibonacci(n - 1) + fibonacci(n - 2);", "}"),
        "power_simple": ("double potencia(double x, int n) {", "    if (n == 0) {", "        return 1;", "    }", "    return x * potencia(x, n - 1);", "}"),
        "power_fast": ("double potencia_rapida(double x, int n) {", "    if (n == 0) {", "        return 1;", "    }", "    double mitad = potencia_rapida(x, n / 2);", "    if (n % 2 == 1) {", "        return mitad * mitad * x;", "    }", "    return mitad * mitad;", "}"),
    },
}


LANGUAGE_LOGOS = {
    "python": (
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
        "Python",
    ),
    "java": (
        "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg",
        "Java",
    ),
    "c": (
        "https://upload.wikimedia.org/wikipedia/commons/7/72/C1stEdition.svg",
        "C",
    ),
}


def _language_logo(language: str) -> str:
    if language == "pseudocode":
        return ""
    source, label = LANGUAGE_LOGOS[language]
    return (
        f'<img class="lab-language-logo" src="{source}" '
        f'alt="Logotipo de {label}" title="{label}">'
    )


def _children(algorithm: str, n: int) -> list[int]:
    if algorithm == "fibonacci":
        return [] if n <= 1 else [n - 1, n - 2]
    if algorithm == "power_fast":
        return [] if n == 0 else [n // 2]
    limit = 1 if algorithm == "factorial" else 0
    return [] if n <= limit else [n - 1]


def build_trace(algorithm: str, n: int):
    nodes: list[Node] = []
    events: list[dict] = []
    stack: list[int] = []

    def visit(value: int, depth: int, parent: int | None):
        node_id = len(nodes)
        node = Node(node_id, value, f"{value}", depth, parent)
        nodes.append(node)
        if parent is not None:
            nodes[parent].children.append(node_id)
        stack.append(node_id)

        def add_event(kind: str, line: int):
            events.append(
                {"kind": kind, "line": line, "node": node_id, "stack": tuple(stack)}
            )

        add_event("enter", 0)
        add_event("line", 1)
        children = _children(algorithm, value)
        if not children:
            add_event("return", 2)
        elif algorithm == "power_fast":
            add_event("line", 3)
            visit(children[0], depth + 1, node_id)
            add_event("resume", 3)
            add_event("line", 4)
            add_event("return", 5 if value % 2 else 6)
        else:
            for child_value in children:
                add_event("line", 3)
                visit(child_value, depth + 1, node_id)
                add_event("resume", 3)
            add_event("return", 3)
        stack.pop()

    visit(n, 0, None)
    return nodes, events


def _node_value(algorithm: str, n: int):
    if algorithm == "factorial":
        return math.factorial(n)
    if algorithm == "fibonacci":
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
    if n == 0:
        return 1
    return rf"x^{{{n}}}"


def _frame_expression(
    algorithm: str, node: Node, nodes: list[Node], completed: set[int]
) -> str:
    value = node.n
    if not node.children:
        result = _node_value(algorithm, value)
        return rf"f({value})={result}"

    child_terms = []
    for child_id in node.children:
        child = nodes[child_id]
        child_terms.append(
            str(_node_value(algorithm, child.n))
            if child_id in completed
            else rf"f({child.n})"
        )
    if algorithm == "factorial":
        body = rf"{value}\cdot {child_terms[0]}"
    elif algorithm == "fibonacci":
        body = "+".join(child_terms)
    elif algorithm == "power_simple":
        body = rf"x\cdot {child_terms[0]}"
    else:
        factor = r"\cdot x" if value % 2 else ""
        body = rf"\left({child_terms[0]}\right)^2{factor}"
    if all(child_id in completed for child_id in node.children):
        body += rf"={_node_value(algorithm, value)}"
    return rf"f({value})={body}"


def _tree_svg(nodes: list[Node], events: list[dict], step: int) -> str:
    discovered = {
        event["node"] for event in events[: step + 1] if event["kind"] == "enter"
    }
    levels: dict[int, list[Node]] = {}
    for node in nodes:
        levels.setdefault(node.depth, []).append(node)
    width = 720
    height = _execution_height(nodes)
    maximum_depth = max((node.depth for node in nodes), default=0)
    top_padding = 38
    usable_height = height - 2 * top_padding
    positions: dict[int, tuple[float, float]] = {}
    for depth, level_nodes in levels.items():
        for index, node in enumerate(level_nodes, 1):
            positions[node.id] = (
                width * index / (len(level_nodes) + 1),
                top_padding
                if maximum_depth == 0
                else top_padding + usable_height * depth / maximum_depth,
            )
    edges = []
    circles = []
    for node in nodes:
        is_visible = node.id in discovered
        if is_visible and node.parent in discovered:
            x1, y1 = positions[node.parent]
            x2, y2 = positions[node.id]
            edges.append(
                f'<line x1="{x1:.1f}" y1="{y1 + 23:.1f}" '
                f'x2="{x2:.1f}" y2="{y2 - 27:.1f}" class="lab-edge" '
                'marker-end="url(#lab-arrow-head)"/>'
            )
        x, y = positions[node.id]
        state = "base" if not node.children else "recursive"
        visibility = "" if is_visible else " undiscovered"
        hidden = "" if is_visible else ' aria-hidden="true"'
        circles.append(
            f'<g class="lab-node {state}{visibility}"{hidden}>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="23"/>'
            f'<text x="{x:.1f}" y="{y + 5:.1f}">{node.n}</text></g>'
        )
    return (
        f'<div class="lab-tree-scroll"><svg class="lab-tree" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="Árbol de recursión">'
        '<defs><marker id="lab-arrow-head" markerWidth="8" markerHeight="8" '
        'refX="7" refY="4" orient="auto" markerUnits="strokeWidth">'
        '<path d="M0,0 L8,4 L0,8 Z" class="lab-arrow-head"/></marker></defs>'
        f'{"".join(edges)}{"".join(circles)}</svg></div>'
    )


def _execution_height(nodes: list[Node]) -> int:
    """Reserva una altura estable y proporcional a la profundidad real."""

    maximum_depth = max((node.depth for node in nodes), default=0)
    return min(426, max(180, 76 + maximum_depth * 82))


def _inline_math_html(expression: str) -> str:
    """Compone MathML nativo sin recargar MathJax durante la animación."""

    accessible = expression.replace(r"\left", "").replace(r"\right", "")
    accessible = re.sub(r"\s*\\cdot\s*", " por ", accessible)
    accessible = re.sub(r"\^\{([^{}]+)\}", r" elevado a \1", accessible)
    accessible = re.sub(r"\^([0-9]+)", r" elevado a \1", accessible)
    accessible = accessible.replace("{", "").replace("}", "")
    accessible = " ".join(accessible.split())

    normalized = expression.replace(r"\left", "").replace(r"\right", "")
    normalized = re.sub(r"\s*\\cdot\s*", "·", normalized)

    def sequence(position: int, closing: str | None = None):
        output = []
        while position < len(normalized):
            character = normalized[position]
            if closing and character == closing:
                return "".join(output), position + 1
            if character.isspace():
                position += 1
                continue
            if character == "(":
                inner, position = sequence(position + 1, ")")
                atom = (
                    '<mrow><mo fence="true">(</mo>'
                    f'{inner}<mo fence="true">)</mo></mrow>'
                )
            elif character.isdigit():
                end = position + 1
                while end < len(normalized) and normalized[end].isdigit():
                    end += 1
                atom = f"<mn>{normalized[position:end]}</mn>"
                position = end
            elif character.isalpha():
                end = position + 1
                while end < len(normalized) and normalized[end].isalpha():
                    end += 1
                atom = f"<mi>{html.escape(normalized[position:end])}</mi>"
                position = end
            elif character in "=+-·×":
                output.append(f"<mo>{html.escape(character)}</mo>")
                position += 1
                continue
            else:
                output.append(f"<mtext>{html.escape(character)}</mtext>")
                position += 1
                continue

            if position < len(normalized) and normalized[position] == "^":
                position += 1
                if position < len(normalized) and normalized[position] == "{":
                    exponent, position = sequence(position + 1, "}")
                else:
                    start = position
                    while position < len(normalized) and normalized[position].isalnum():
                        position += 1
                    value = normalized[start:position]
                    tag = "mn" if value.isdigit() else "mi"
                    exponent = f"<{tag}>{html.escape(value)}</{tag}>"
                atom = f"<msup>{atom}<mrow>{exponent}</mrow></msup>"
            output.append(atom)
        return "".join(output), position

    rendered, _ = sequence(0)
    return (
        '<math class="lab-math-expression" '
        f'aria-label="{html.escape(accessible, quote=True)}"><mrow>{rendered}</mrow></math>'
    )


def _call_stack_panel(
    algorithm: str, nodes: list[Node], events: list[dict], step: int
) -> str:
    event = events[step]
    active_stack = event["stack"]
    current = event["node"]
    is_base = not nodes[current].children
    finished = step == len(events) - 1
    frames = []
    completed = {
        item["node"] for item in events[: step + 1] if item["kind"] == "return"
    }
    for node_id in reversed(active_stack):
        node = nodes[node_id]
        if node_id == current and event["kind"] == "return" and finished:
            css = " current-return completed"
        elif node_id == current and event["kind"] == "return":
            css = " current-return frame-pop"
        elif node_id == current and event["kind"] == "enter":
            css = " current-call frame-push"
        elif node_id == current and event["kind"] == "resume":
            css = " current-call frame-resume"
        elif node_id == current:
            css = " current-call"
        else:
            css = " waiting"
        state = (
            ""
            if node_id == current and finished
            else "Caso base · retorna"
            if node_id == current and event["kind"] == "return" and is_base
            else "Se desapila"
            if node_id == current and event["kind"] == "return"
            else "Nueva llamada"
            if node_id == current and event["kind"] == "enter"
            else "Recibe el resultado"
            if node_id == current and event["kind"] == "resume"
            else "En ejecución"
            if node_id == current
            else "En espera"
        )
        state_markup = f"<span>{state}</span>" if state else ""
        frame_markup = (
            f'<div class="lab-call-frame{css}">'
            f'<b>{_inline_math_html(_frame_expression(algorithm, node, nodes, completed))}</b>'
            f'{state_markup}</div>'
        )
        if node_id == current and finished:
            frame_markup = (
                '<div class="lab-completed-row">'
                + frame_markup
                + '<span class="lab-finish-check" role="img" title="Completado" '
                'aria-label="Completado">✓</span></div>'
            )
        frames.append(frame_markup)
    return (
        '<div class="lab-call-stack" aria-label="Pila de llamadas">'
        + "".join(frames)
        + '<div class="lab-stack-base">Base de la pila · problema original</div></div>'
    )


def _desk_check_table(
    algorithm: str, nodes: list[Node], events: list[dict], step: int
) -> str:
    """Construye la traza acumulada con el contrato de búsquedas y ordenamientos."""

    rows = []
    first = max(0, step - 39)
    for index, event in enumerate(events[first : step + 1], start=first):
        node = nodes[event["node"]]
        stack_values = " → ".join(str(nodes[node_id].n) for node_id in event["stack"])
        result = (
            str(_node_value(algorithm, node.n))
            if event["kind"] == "return"
            else "—"
        )
        rows.append(
            '<tr>'
            f'<td>{index + 1}</td>'
            f'<td>{event["line"] + 1}</td>'
            f'<td class="lab-desk-mono">{node.n}</td>'
            f'<td class="lab-desk-mono">{stack_values}</td>'
            f'<td class="lab-desk-mono">{result}</td>'
            "</tr>"
        )
    note = (
        f'<p class="lab-desk-note">Se muestran los últimos {len(rows)} pasos.</p>'
        if first
        else ""
    )
    scroll_trigger = (
        '<img class="lab-desk-scroll-trigger" '
        'src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" '
        'alt="" onload="var w=this.closest(\'.lab-desk-check\')?.querySelector(\'.lab-desk-table-wrap\');'
        'if(w)w.scrollTop=w.scrollHeight;">'
    )
    return (
        '<div class="lab-desk-check" role="region" aria-label="Prueba de escritorio" aria-live="polite">'
        '<div class="lab-desk-table-wrap">'
        '<table class="lab-desk-table">'
        '<thead><tr><th>Paso</th><th>Línea</th><th>n</th><th>Pila activa</th><th>Resultado</th></tr></thead>'
        '<tbody>' + "".join(rows) + f"</tbody></table>{scroll_trigger}</div>{note}</div>"
    )


def _event_delay(event: dict, nodes: list[Node]) -> float:
    if event["kind"] == "enter":
        return 0.55
    if event["kind"] == "resume":
        return 0.3
    if event["kind"] == "return":
        return 0.75 if not nodes[event["node"]].children else 0.6
    return 0.32


def _cost_expression(algorithm: str, analysis_type: str) -> str:
    symbol = "T" if analysis_type == "temporal" else "S"
    base_condition = r"n\leq 1" if algorithm in {"factorial", "fibonacci"} else "n=0"
    if algorithm == "fibonacci":
        recursive_cost = (
            r"T(n-1)+T(n-2)+\Theta(1)"
            if analysis_type == "temporal"
            else r"\max\{S(n-1),S(n-2)\}+\Theta(1)"
        )
    elif algorithm == "power_fast":
        recursive_cost = rf"{symbol}(\lfloor n/2\rfloor)+\Theta(1)"
    else:
        recursive_cost = rf"{symbol}(n-1)+\Theta(1)"
    recursive_condition = "n>1" if algorithm in {"factorial", "fibonacci"} else "n>0"
    return (
        rf"{symbol}(n)=\begin{{cases}}"
        rf"\Theta(1), & \text{{si }} {base_condition},\\"
        rf"{recursive_cost}, & \text{{si }} {recursive_condition}"
        r"\end{cases}"
    )


def _method_panel(algorithm: str, data: dict, analysis_type: str) -> str:
    is_temporal = analysis_type == "temporal"
    stages = (
        ("1", "Caso de análisis", data["case"]),
        ("2", "Caso base", rf"\({data['base']}\)"),
        (
            "3",
            "Costo de las llamadas recursivas" if is_temporal else "Profundidad de la pila",
            rf"\({data['calls']}\)"
            if is_temporal
            else rf"La pila conserva únicamente la rama activa más profunda: \({data['space']}\)",
        ),
        (
            "4",
            "Trabajo por llamada" if is_temporal else "Espacio por marco",
            rf"\({data['work']}\)"
            if is_temporal
            else r"Cada llamada mantiene sus parámetros y variables locales: \(\Theta(1)\) por marco",
        ),
    )
    steps = "".join(
        '<div class="lab-analysis-step">'
        f'<div class="lab-analysis-step-title"><b>{number}. {title}.</b></div>'
        f'<div class="lab-analysis-step-solution">{body}</div></div>'
        for number, title, body in stages
    )
    result = _cost_expression(algorithm, analysis_type)
    return (
        '<details class="lab-section lab-analysis-panel" open>'
        f'<summary>Análisis {"temporal" if is_temporal else "espacial"}</summary>'
        f'<div class="lab-section-content lab-analysis-steps">{steps}'
        '<div class="lab-analysis-step lab-analysis-result">'
        '<div class="lab-analysis-step-title"><b>5. Expresión de complejidad por casos.</b></div>'
        rf'<div class="lab-analysis-step-solution lab-analysis-equation">\({result}\)</div>'
        '</div></div></details>'
    )


def _highlight_code_line(line: str, language: str) -> str:
    if language == "pseudocode":
        rendered = html.escape(line)
        rendered = re.sub(
            r"\b(si|retornar|en otro caso|es impar)\b",
            r'<span class="k">\1</span>', rendered,
        )
        rendered = re.sub(r"\b(\d+)\b", r'<span class="mi">\1</span>', rendered)
        rendered = re.sub(
            r"\b([A-Za-zÁ-ÿ_][A-Za-zÁ-ÿ_0-9]*)(?=\()",
            r'<span class="nf">\1</span>', rendered,
        )
        return rendered
    lexer = {"python": PythonLexer(), "java": JavaLexer(), "c": CLexer()}[language]
    return highlight(line, lexer, HtmlFormatter(nowrap=True)).rstrip("\n")


def _language_line(algorithm: str, language: str, trace_line: int) -> int:
    if language not in {"java", "c"}:
        return trace_line
    if algorithm == "power_fast":
        return {0: 0, 1: 1, 2: 2, 3: 4, 4: 5, 5: 6, 6: 8}[trace_line]
    return 4 if trace_line == 3 else trace_line


def _code_panel(algorithm: str, language: str, active_line: int) -> str:
    lines = CODE_SNIPPETS[language][algorithm]
    active_line = _language_line(algorithm, language, active_line)
    rows = []
    for index, line in enumerate(lines):
        css = " current" if index == active_line else ""
        rows.append(
            f'<div class="lab-code-line{css}">'
            f'<span class="lab-line-number">{index + 1}</span>'
            f'<span class="lab-line-source">{_highlight_code_line(line, language)}</span>'
            '</div>'
        )
    return '<div class="lab-code">' + "".join(rows) + "</div>"


STYLES = """
<style>
.recursive-analysis-lab{box-sizing:border-box;width:100%;max-width:100%;min-width:0;padding:14px 4px;background:#fff;color:#333;font-family:sans-serif;overflow-x:hidden!important;overflow-y:visible!important}
.recursive-analysis-lab *{box-sizing:border-box}
.recursive-analysis-lab>.widget-box,
.recursive-analysis-lab .widget-html-content,
.recursive-analysis-lab .widget-htmlmath-content{box-sizing:border-box;width:100%!important;max-width:none!important;background:#fff;color:#333;font-family:sans-serif}
.recursive-analysis-lab>.widget-html,.recursive-analysis-lab>.widget-htmlmath{box-sizing:border-box;width:100%!important;max-width:none!important;margin:0!important}
.recursive-analysis-lab .widget-label,
.recursive-analysis-lab label,
.recursive-analysis-lab p,
.recursive-analysis-lab b,
.recursive-analysis-lab i,
.recursive-analysis-lab span,
.recursive-analysis-lab div{color:#333}
.recursive-analysis-lab mjx-container,
.recursive-analysis-lab mjx-container *{color:#333!important}
.recursive-analysis-lab mjx-container svg,
.recursive-analysis-lab mjx-container svg *{fill:#333!important;color:#333!important}
.lab-configuration-panel{box-sizing:border-box!important;width:100%!important;max-width:none!important;margin:0!important;border:1px solid #dedede!important;border-bottom:0!important;border-radius:5px 5px 0 0!important;background:#fff!important;overflow:hidden!important}
.lab-configuration-summary{box-sizing:border-box!important;width:100%!important;height:44px!important;min-height:44px!important;margin:0!important;padding:10px 14px!important;border:0!important;border-bottom:1px solid #e2e2e2!important;border-radius:0!important;background:#f7f7f7!important;color:#333!important;font-family:sans-serif!important;font-size:16px!important;font-weight:700!important;line-height:24px!important;text-align:left!important}.lab-configuration-summary:hover{background:#f7f7f7!important}.lab-configuration-summary .fa{color:#333!important}
.lab-controls{box-sizing:border-box!important;width:100%!important;max-width:100%!important;min-width:0!important;padding:12px!important;border:0!important;background:#fff!important;margin:0!important;overflow-x:hidden!important}
.lab-controls .widget-label{color:#333;font-family:sans-serif;font-size:13px;font-weight:700;line-height:1.1}
.lab-control-label{display:flex!important;align-items:center!important;justify-content:center!important;height:32px!important;min-height:32px!important;color:#333!important;font-family:sans-serif!important;font-size:13px!important;font-weight:700!important;line-height:1.1!important;text-align:center!important}.lab-control-label .widget-htmlmath-content{display:flex!important;align-items:center!important;justify-content:center!important;width:100%!important;height:32px!important;color:#333!important;font-family:sans-serif!important;font-size:13px!important;font-weight:700!important;line-height:1.1!important}.lab-control-label mjx-container,.lab-control-label mjx-container *{color:#333!important;font-size:100%!important;font-weight:700!important}
.lab-controls select{box-sizing:border-box;width:188px!important;height:32px;padding:2px 4px;border:1px solid #ccc;border-radius:3px;background:#fff!important;color:#333;font-size:13px;text-align:center;text-align-last:center;appearance:auto!important}
.lab-controls select option{background:#fff;color:#333}
.lab-controls input:not([type="range"]){box-sizing:border-box;width:188px!important;height:32px!important;padding:2px 4px!important;border:1px solid #ccc!important;border-radius:3px!important;background:#fff!important;color:#333!important;font-size:13px!important;text-align:center!important}
.lab-controls .lab-field{width:188px!important;height:32px!important}.lab-controls .lab-field input{width:188px!important;height:32px!important}
.lab-controls .lab-field.widget-disabled{opacity:1!important}.lab-controls .lab-field input:disabled{opacity:1!important;background:#f7f7f7!important;color:#333!important;cursor:default!important}
.lab-control-row{box-sizing:border-box!important;width:292px!important;min-width:0!important;max-width:100%!important;overflow-x:hidden!important}.lab-control-row>.widget-html,.lab-control-row>.widget-htmlmath{flex:0 0 96px!important;width:96px!important;min-width:96px!important;max-width:96px!important}.lab-control-row>.widget-dropdown,.lab-control-row>.widget-text,.lab-control-row>.widget-int{flex:0 0 188px!important;width:188px!important;min-width:188px!important;max-width:188px!important}
.lab-controls input[type="number"]{-moz-appearance:textfield!important;appearance:textfield!important}
.lab-controls input[type="number"]::-webkit-inner-spin-button,.lab-controls input[type="number"]::-webkit-outer-spin-button{-webkit-appearance:none!important;margin:0!important}
.lab-controls .widget-readout{background:#fff!important;color:#333!important;font-family:sans-serif!important}
.lab-controls .lab-configuration-summary{height:44px!important;min-height:44px!important}
.lab-controls input[type="range"]{accent-color:#5f6368}
.lab-parameter-controls{box-sizing:border-box!important;width:100%!important;max-width:100%!important;min-width:0!important;column-gap:36px!important;row-gap:12px!important;overflow-x:hidden!important}
.lab-section{box-sizing:border-box;width:100%;margin:0;border:1px solid #dedede;border-bottom:0;border-radius:0;background:#fff;overflow:hidden}.lab-section:first-child{border-radius:5px 5px 0 0}.lab-section:last-child{border-bottom:1px solid #dedede;border-radius:0 0 5px 5px}
.lab-section>summary{box-sizing:border-box;width:100%;padding:9px 12px;cursor:pointer;background:#f7f7f7;color:#333;font-size:16px;font-weight:700;line-height:1.45}.lab-section[open]>summary{border-bottom:1px solid #e2e2e2}.lab-section-content{box-sizing:border-box;width:100%;background:#fff}
.lab-code-summary{position:relative;display:flex!important;height:44px!important;min-height:44px!important;max-height:44px!important;padding-left:32px!important;align-items:center;justify-content:space-between;overflow:hidden}.lab-code-summary::before{position:absolute;left:12px;top:50%;content:"▾";font-size:13px;line-height:1;transform:translateY(-50%)}.lab-code-panel:not([open])>.lab-code-summary::before{content:"▸"}.lab-language-logo{display:block;flex:0 0 26px;width:26px;height:26px;object-fit:contain}
.lab-analysis-panel{margin:0;border-bottom:1px solid #dedede!important;border-radius:0 0 5px 5px!important}.lab-analysis-steps{padding:10px 18px 14px;font-size:16px;line-height:1.55}.lab-analysis-step{margin:8px 0 14px!important;line-height:1.55}.lab-analysis-step-title{font-weight:700;text-align:left}.lab-analysis-step-solution{width:100%;padding:4px 12px 0;text-align:center}.lab-analysis-result{margin:16px 0 2px!important}.lab-analysis-equation{padding:6px 0 4px;font-size:18px}
.lab-visual-sections{width:100%;margin:0}.lab-code-panel{border-radius:0!important}.lab-code-panel[open] .lab-code{height:auto;min-height:0}
.lab-code{height:auto;min-height:0;padding:0;overflow-x:auto;overflow-y:hidden;background:#fff;font:14px/1.55 ui-monospace,SFMono-Regular,Consolas,monospace}
.lab-code-line{display:grid;grid-template-columns:42px minmax(max-content,1fr);min-height:28px;white-space:pre-wrap}.lab-line-number{display:flex;align-items:center;justify-content:center;padding:3px 4px;border-right:1px solid #d8d8d8;background:#f2f2f2;color:#666!important;font-weight:700;user-select:none}.lab-line-source{display:block;padding:3px 10px;border-left:3px solid transparent;background:#fff}.lab-code-line.current .lab-line-number{background:#ece8d8;color:#444!important}.lab-code-line.current .lab-line-source{background:#f4e8bd;border-left-color:#a47b20}
.lab-code .k{color:#005cc5;font-weight:600}.lab-code .kt,.lab-code .nb,.lab-code .bp{color:#005cc5}.lab-code .nf{color:#6f42c1}.lab-code .n{color:#24292e}.lab-code .mi,.lab-code .mf{color:#005a8d}.lab-code .s,.lab-code .s1,.lab-code .s2{color:#22863a}.lab-code .c,.lab-code .c1,.lab-code .cm{color:#6a737d;font-style:italic}.lab-code .o{color:#d73a49}.lab-code .p{color:#24292e}
.lab-tree-scroll{height:100%;overflow:auto;background:#fff}.lab-tree{display:block;width:100%;height:100%;min-width:520px;background:#fff}
.lab-edge{fill:none;stroke:#202124;stroke-width:1.7}.lab-arrow-head{fill:#202124!important;stroke:none!important}.lab-node circle{fill:#fff;stroke:#202124;stroke-width:1.7}.lab-node text{text-anchor:middle;font-family:"STIX Two Math","Cambria Math","Times New Roman",serif;font-size:15px;font-weight:400;fill:#111!important}.lab-node.base circle{fill:#e8f5e9;stroke:#202124}
.lab-node.undiscovered{opacity:0;pointer-events:none}.lab-call-stack{display:flex;height:100%;flex-direction:column;justify-content:flex-end;align-items:center;gap:0;padding:14px 18px 0;overflow:auto;background:#fff}
.lab-call-frame{display:flex;width:min(100%,330px);align-items:center;justify-content:space-between;gap:12px;padding:8px 12px;border:1px solid #202124;border-radius:0;background:#f7f7f7;transition:background-color .2s ease,opacity .2s ease,transform .2s ease}
.lab-call-frame+.lab-call-frame{border-top:0}
.lab-call-frame b{font-family:"STIX Two Math","Cambria Math","Times New Roman",serif;font-weight:400}.lab-call-frame span{font-size:12px;color:#5f6368!important}.lab-call-frame .lab-math-expression{display:inline-block;margin:0;font-family:"STIX Two Math","Cambria Math","Times New Roman",serif;font-size:18px;color:#202124!important;white-space:nowrap}.lab-call-frame .lab-math-expression *{color:#202124!important}
.lab-call-frame.waiting{opacity:.62}.lab-call-frame.current-call{background:#f4e8bd;opacity:1}.lab-call-frame.current-return{background:#e8f5e9;opacity:1}.lab-call-frame.completed{transform:none;opacity:1}
.lab-completed-row{position:relative;width:min(100%,330px)}.lab-completed-row .lab-call-frame{width:100%}
.lab-finish-check{position:absolute;left:calc(100% + 8px);top:50%;display:inline-block!important;width:28px;font-family:serif;font-size:28px;line-height:1;font-weight:700;color:#2d7d32!important;text-align:center;transform:translateY(-50%)}
.lab-call-frame.frame-push{animation:lab-frame-push .22s ease-out}.lab-call-frame.frame-resume{animation:lab-frame-resume .24s ease-out}.lab-call-frame.frame-pop{animation:lab-frame-pop .28s ease-in-out}
@keyframes lab-frame-push{from{opacity:0;transform:translateY(-9px)}to{opacity:1;transform:translateY(0)}}@keyframes lab-frame-resume{0%{transform:scale(.985)}55%{transform:scale(1.012)}100%{transform:scale(1)}}@keyframes lab-frame-pop{0%{opacity:1;transform:translateY(0)}65%{opacity:1;transform:translateY(-2px)}100%{opacity:.38;transform:translateY(-9px)}}
.lab-stack-base{width:min(100%,360px);margin-top:5px;padding:6px 10px;border-top:2px solid #202124;text-align:center;color:#5f6368!important;font-size:12px}
.lab-desk-check{display:flex;width:100%;height:100%;min-height:0;flex-direction:column;overflow:hidden;background:#fff;color:#111;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:13px}.lab-desk-table-wrap{position:relative;width:100%;min-height:0;flex:1 1 auto;overflow:auto}.lab-desk-table{width:max-content;min-width:100%;border-collapse:separate;border-spacing:0;font-size:13px;line-height:1.45}.lab-desk-table th,.lab-desk-table td{width:1%;padding:5px 10px;border-bottom:1px solid rgba(128,128,128,.25);text-align:center;vertical-align:middle;white-space:nowrap}.lab-desk-table th{position:sticky;top:0;z-index:10;background:rgba(246,245,243,.98);box-shadow:0 1px 0 rgba(128,128,128,.35);font-weight:600}.lab-desk-table tr:last-child td{background:rgba(139,75,50,.10);font-weight:600}.lab-desk-table tbody tr:hover td{background:rgba(139,75,50,.07)!important}.lab-desk-mono{font-family:SFMono-Regular,Consolas,"Liberation Mono",Menlo,monospace;font-size:12px}.lab-desk-note{flex:0 0 auto;margin:4px 8px;font-size:12px;opacity:.75}.lab-desk-scroll-trigger{display:none}.lab-widget-panels{box-sizing:border-box!important;width:100%!important;margin:0!important;gap:0!important;overflow:visible!important}.lab-widget-panel{box-sizing:border-box!important;width:100%!important;min-width:0!important;margin:0!important;gap:0!important;border:1px solid #dedede!important;background:#fff!important;overflow:hidden!important}.lab-widget-header{box-sizing:border-box!important;width:100%!important;height:44px!important;min-height:44px!important;gap:0!important;border-bottom:1px solid #e2e2e2!important;background:#f7f7f7!important;overflow:hidden!important}.lab-widget-summary{flex:1 1 auto!important;width:auto!important;min-width:0!important;height:44px!important;min-height:44px!important;max-height:44px!important;margin:0!important;padding:10px 14px!important;border:0!important;border-radius:0!important;background:#f7f7f7!important;color:#333!important;box-shadow:none!important;font-family:sans-serif!important;font-size:16px!important;font-weight:700!important;line-height:24px!important;text-align:left!important}.lab-widget-summary:hover{background:#f7f7f7!important}.lab-widget-logo{position:relative!important;z-index:1!important;flex:0 0 42px!important;width:42px!important;height:44px!important;margin:0!important;padding:9px 12px 9px 4px!important;background:transparent!important;overflow:hidden!important}.lab-widget-logo .widget-html-content{display:flex!important;align-items:center!important;justify-content:flex-end!important;width:100%!important;height:100%!important;margin:0!important;padding:0!important;background:transparent!important}.lab-widget-logo .lab-language-logo{margin:0!important;background:transparent!important}.lab-widget-content{box-sizing:border-box!important;width:100%!important;min-width:0!important;margin:0!important;background:#fff!important;overflow:hidden!important}.lab-widget-overview,.lab-widget-execution{display:flex!important;width:100%!important;min-width:0!important;align-items:flex-start!important;gap:0!important;overflow:hidden!important}.lab-widget-overview>.lab-widget-panel,.lab-widget-execution>.lab-widget-panel{flex:0 0 50%!important;width:50%!important;min-width:0!important}.lab-widget-overview>.lab-widget-panel:first-child,.lab-widget-execution>.lab-widget-panel:first-child{border-right:0!important}.lab-widget-overview>.lab-widget-panel,.lab-widget-execution>.lab-widget-panel{border-top:0!important}.lab-widget-overview .lab-widget-content,.lab-widget-execution .lab-widget-content{overflow:hidden!important}.lab-widget-panel.lab-collapsed .lab-widget-content{height:0!important;min-height:0!important;max-height:0!important}.lab-widget-panel.lab-collapsed{height:44px!important}
@media(max-width:760px){.lab-widget-overview,.lab-widget-execution{display:block!important}.lab-widget-overview>.lab-widget-panel,.lab-widget-execution>.lab-widget-panel{width:100%!important;flex:0 0 100%!important}.lab-widget-overview>.lab-widget-panel:first-child,.lab-widget-execution>.lab-widget-panel:first-child{border-right:1px solid #dedede!important}.lab-widget-overview>.lab-widget-panel+.lab-widget-panel,.lab-widget-execution>.lab-widget-panel+.lab-widget-panel{border-top:0!important}}
</style>
"""


def _mathjax_frame(content: str, height: int) -> str:
    """Renderiza fórmulas de forma estable en Jupyter local y Google Colab."""

    srcdoc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
html,body{{box-sizing:border-box;width:100%;height:100%;margin:0;padding:0;background:#fff;color:#333;font-family:sans-serif;overflow:auto;}}
*,*::before,*::after{{box-sizing:border-box;}}
#content{{width:100%;visibility:hidden;}}
body.math-ready #content{{visibility:visible;}}
.lab-section{{width:100%;margin:0;border:0;background:#fff;}}
.lab-section>summary{{box-sizing:border-box;width:100%;padding:9px 12px;background:#f7f7f7;border-bottom:1px solid #e2e2e2;color:#333;font-size:16px;font-weight:700;line-height:1.45;cursor:pointer;}}
.lab-section-content{{width:100%;background:#fff;}}
.lab-analysis-steps{{padding:10px 18px 14px;font-size:16px;line-height:1.55;}}
.lab-analysis-step{{margin:8px 0 14px;line-height:1.55;}}
.lab-analysis-step-title{{font-weight:700;text-align:left;}}
.lab-analysis-step-solution{{width:100%;padding:4px 12px 0;text-align:center;}}
.lab-analysis-result{{margin:16px 0 2px;}}
.lab-analysis-equation{{padding:6px 0 4px;font-size:18px;}}
.lab-call-stack{{display:flex;height:100%;min-height:400px;flex-direction:column;justify-content:flex-end;align-items:center;gap:0;padding:14px 18px 0;overflow:auto;background:#fff;}}
.lab-call-frame{{display:flex;width:min(100%,330px);align-items:center;justify-content:space-between;gap:12px;padding:8px 12px;border:1px solid #202124;background:#f7f7f7;}}
.lab-call-frame+.lab-call-frame{{border-top:0;}}
.lab-call-frame b{{font-family:"STIX Two Math","Cambria Math","Times New Roman",serif;}}
.lab-call-frame span{{font-size:12px;color:#5f6368;}}
.lab-call-frame.waiting{{opacity:.62;}}.lab-call-frame.current-call{{background:#f4e8bd;opacity:1;}}.lab-call-frame.current-return{{background:#e8f5e9;opacity:1;}}.lab-call-frame.completed{{opacity:1;}}
.lab-completed-row{{position:relative;width:min(100%,330px);}}.lab-completed-row .lab-call-frame{{width:100%;}}
.lab-finish-check{{position:absolute;left:calc(100% + 8px);top:50%;width:28px;font-family:serif;font-size:28px;font-weight:700;color:#2d7d32;text-align:center;transform:translateY(-50%);}}
.lab-stack-base{{width:min(100%,360px);margin-top:5px;padding:6px 10px;border-top:2px solid #202124;text-align:center;color:#5f6368;font-size:12px;}}
mjx-container{{color:#333!important;}}
</style>
<script>
window.MathJax={{tex:{{inlineMath:[['\\\\(','\\\\)']],processEscapes:true}},svg:{{fontCache:'none'}},startup:{{typeset:false}}}};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js" integrity="sha256-1CldwzdEg2k1wTmf7s5RWVd7NMXI/7nxxjJM2C4DqII=" crossorigin="anonymous"></script>
</head>
<body><div id="content">{content}</div>
<script>
window.addEventListener('load',function(){{
  if(window.MathJax&&MathJax.typesetPromise){{MathJax.typesetPromise([document.getElementById('content')]).then(function(){{document.body.classList.add('math-ready');}});}}
  else{{document.body.classList.add('math-ready');}}
}});
</script></body></html>"""
    return (
        '<iframe class="lab-mathjax-frame" '
        f'srcdoc="{html.escape(srcdoc, quote=True)}" '
        f'style="display:block;width:100%;height:{height}px;border:0;overflow:hidden;background:#fff;" '
        'scrolling="no"></iframe>'
    )


def run_app():
    algorithm = widgets.Dropdown(
        options=[(value["name"], key) for key, value in ALGORITHMS.items()],
        value="factorial",
        layout=widgets.Layout(width="188px", height="32px"),
    )
    analysis_type = widgets.Dropdown(
        options=[("Temporal", "temporal"), ("Espacial", "espacial")],
        value="temporal",
        layout=widgets.Layout(width="188px", height="32px"),
    )
    language = widgets.Dropdown(
        options=[
            ("Pseudocódigo", "pseudocode"), ("Python", "python"),
            ("Java", "java"), ("C", "c"),
        ],
        value="pseudocode",
        layout=widgets.Layout(width="188px", height="32px"),
    )
    size = widgets.BoundedIntText(
        value=5, min=1, max=12, step=1,
        disabled=True,
        layout=widgets.Layout(width="188px", height="32px"),
    )
    size.add_class("lab-field")
    previous = action_button("step_back")
    following = action_button("step")
    play = action_button("play")
    reset = action_button("restart")
    method = widgets.HTML(layout=widgets.Layout(width="100%"))
    code_content = widgets.HTML(layout=widgets.Layout(width="100%"))
    state_content = widgets.HTML(layout=widgets.Layout(width="100%"))
    stack_content = widgets.HTML(layout=widgets.Layout(width="100%"))
    tree_content = widgets.HTML(layout=widgets.Layout(width="100%"))
    language_logo = widgets.HTML(layout=widgets.Layout(width="42px", height="44px"))
    language_logo.add_class("lab-widget-logo")
    state = {
        "nodes": [], "events": [], "step": 0, "play_task": None,
        "render_cache": {},
    }

    def collapsible_panel(title, content, extra=None):
        summary = widgets.Button(
            description=title, icon="caret-down",
            layout=widgets.Layout(width="100%", height="44px"),
        )
        summary.add_class("lab-widget-summary")
        summary.add_class("lab-subpanel-title")
        header_children = [summary] + ([extra] if extra is not None else [])
        header = widgets.HBox(header_children, layout=widgets.Layout(width="100%", grid_gap="0"))
        header.add_class("lab-widget-header")
        content.add_class("lab-widget-content")

        def toggle(_):
            collapsed = content.layout.display != "none"
            content.layout.display = "none" if collapsed else "block"
            summary.icon = "caret-right" if collapsed else "caret-down"
            if collapsed:
                panel.add_class("lab-collapsed")
            else:
                panel.remove_class("lab-collapsed")

        summary.on_click(toggle)
        panel = widgets.VBox([header, content], layout=widgets.Layout(width="100%", grid_gap="0"))
        panel.add_class("lab-widget-panel")
        return panel

    code_panel = collapsible_panel("Algoritmo", code_content, language_logo)
    state_panel = collapsible_panel("Prueba de escritorio", state_content)
    stack_panel = collapsible_panel("Pila de recursión", stack_content)
    tree_panel = collapsible_panel("Árbol de recursión", tree_content)
    overview_panels = widgets.HBox(
        [code_panel, state_panel], layout=widgets.Layout(width="100%", grid_gap="0")
    )
    overview_panels.add_class("lab-widget-overview")
    execution_panels = widgets.HBox(
        [stack_panel, tree_panel], layout=widgets.Layout(width="100%", grid_gap="0")
    )
    execution_panels.add_class("lab-widget-execution")
    visualization = widgets.VBox(
        [overview_panels, execution_panels],
        layout=widgets.Layout(width="100%", grid_gap="0"),
    )
    visualization.add_class("lab-widget-panels")

    def stop_playback():
        task = state.get("play_task")
        if task is not None and not task.done():
            task.cancel()
        state["play_task"] = None
        play.description = "Ejecución automática"
        play.icon = "play"

    def rebuild(*_):
        stop_playback()
        data = ALGORITHMS[algorithm.value]
        size.max = data["maximum"]
        if size.value > size.max:
            size.value = data["default"]
        nodes, events = build_trace(algorithm.value, size.value)
        state["nodes"], state["events"] = nodes, events
        state["step"] = 0
        state["render_cache"].clear()
        language_logo.value = _language_logo(language.value)
        overview_height = max(112, len(CODE_SNIPPETS[language.value][algorithm.value]) * 28)
        execution_height = _execution_height(nodes)
        code_content.layout.height = f"{overview_height}px"
        state_content.layout.height = f"{overview_height}px"
        stack_content.layout.height = f"{execution_height}px"
        tree_content.layout.height = f"{execution_height}px"
        method.value = _mathjax_frame(
            _method_panel(algorithm.value, data, analysis_type.value), 550
        )
        render()

    def update_content(widget, cache_key, value):
        if state["render_cache"].get(cache_key) == value:
            return
        state["render_cache"][cache_key] = value
        widget.value = value

    def render(*_):
        nodes, events = state["nodes"], state["events"]
        if not events:
            return
        step = min(state["step"], len(events) - 1)
        event = events[step]
        update_content(
            code_content,
            "code",
            _code_panel(algorithm.value, language.value, event["line"]),
        )
        update_content(
            state_content,
            "desk",
            _desk_check_table(algorithm.value, nodes, events, step),
        )
        update_content(
            stack_content,
            "stack",
            _call_stack_panel(algorithm.value, nodes, events, step),
        )
        update_content(
            tree_content, "tree", _tree_svg(nodes, events, step)
        )

    def select_algorithm(change):
        if change.get("name") != "value":
            return
        data = ALGORITHMS[change["new"]]
        size.max = data["maximum"]
        size.value = data["default"]
        rebuild()

    algorithm.observe(select_algorithm, names="value")
    size.observe(rebuild, names="value")

    def select_analysis(change):
        if change.get("name") != "value":
            return
        method.value = _mathjax_frame(
            _method_panel(
                algorithm.value, ALGORITHMS[algorithm.value], change["new"]
            ),
            550,
        )

    analysis_type.observe(select_analysis, names="value")

    def select_language(change):
        if change.get("name") != "value":
            return
        state["render_cache"].pop("code", None)
        language_logo.value = _language_logo(change["new"])
        overview_height = max(112, len(CODE_SNIPPETS[change["new"]][algorithm.value]) * 28)
        code_content.layout.height = f"{overview_height}px"
        state_content.layout.height = f"{overview_height}px"
        render()

    language.observe(select_language, names="value")

    def move_step(delta):
        if not state["events"]:
            return
        state["step"] = min(
            max(0, state["step"] + delta), len(state["events"]) - 1
        )
        render()

    async def play_process_async():
        try:
            while state["step"] < len(state["events"]) - 1:
                next_event = state["events"][state["step"] + 1]
                await asyncio.sleep(_event_delay(next_event, state["nodes"]))
                move_step(1)
        except asyncio.CancelledError:
            return
        finally:
            state["play_task"] = None
            play.description = "Ejecución automática"
            play.icon = "play"

    def play_process_sync():
        try:
            while state["step"] < len(state["events"]) - 1:
                next_event = state["events"][state["step"] + 1]
                time.sleep(_event_delay(next_event, state["nodes"]))
                move_step(1)
        finally:
            state["play_task"] = None
            play.description = "Ejecución automática"
            play.icon = "play"

    def toggle_playback(_):
        task = state.get("play_task")
        if task is not None and not task.done():
            stop_playback()
            return
        if state["step"] >= len(state["events"]) - 1:
            state["step"] = 0
            render()
        play.description = "Pausar"
        play.icon = "pause"
        if RUNNING_IN_COLAB:
            play_process_sync()
            return
        state["play_task"] = asyncio.get_running_loop().create_task(play_process_async())

    previous.on_click(lambda _: (stop_playback(), move_step(-1)))
    following.on_click(lambda _: (stop_playback(), move_step(1)))
    play.on_click(toggle_playback)
    reset.on_click(lambda _: (stop_playback(), state.update(step=0), render()))

    def labeled(label, control):
        control.layout.margin = "0"
        label_markup = "<i>n</i>" if label == "n" else html.escape(label)
        label_widget = widgets.HTML(
            value=f'<span class="compact-control-label">{label_markup}</span>',
            layout=widgets.Layout(width="96px", margin="0"),
        )
        label_widget.add_class("lab-control-label")
        row = widgets.HBox(
            [label_widget, control],
            layout=widgets.Layout(
                width="292px", align_items="center",
                grid_gap=f"{STANDARD_LABEL_CONTROL_GAP}px",
                overflow="hidden",
            ),
        )
        row.add_class("lab-control-row")
        return row

    analysis_controls = widgets.VBox(
        [
            labeled("Algoritmo", algorithm),
            labeled("Análisis", analysis_type),
        ],
        layout=widgets.Layout(width="292px", grid_gap=f"{STANDARD_CONTROL_ROW_GAP}px"),
    )
    input_controls = widgets.VBox(
        [
            labeled("Lenguaje", language),
            labeled("n", size),
        ],
        layout=widgets.Layout(width="292px", grid_gap=f"{STANDARD_CONTROL_ROW_GAP}px"),
    )
    parameter_controls = widgets.HBox(
        [analysis_controls, input_controls],
        layout=widgets.Layout(
            flex_flow="row wrap", grid_gap=f"{STANDARD_CONTROL_COLUMN_GAP}px",
            align_items="flex-start",
        ),
    )
    parameter_controls.add_class("lab-parameter-controls")
    action_controls = actions([previous, following, play, reset])
    action_controls.add_class("lab-actions")
    controls = widgets.VBox(
        [parameter_controls, action_controls],
        layout=widgets.Layout(
            width="100%", align_items="stretch", grid_gap=f"{STANDARD_CONTROL_ROW_GAP}px"
        ),
    )
    controls.add_class("lab-controls")
    configuration_summary = widgets.Button(
        description="Configuración",
        icon="caret-down",
        layout=widgets.Layout(width="100%", height="44px"),
    )
    configuration_summary.add_class("lab-configuration-summary")

    def toggle_configuration(_):
        collapsed = controls.layout.display != "none"
        controls.layout.display = "none" if collapsed else "flex"
        configuration_summary.icon = "caret-right" if collapsed else "caret-down"

    configuration_summary.on_click(toggle_configuration)
    configuration_panel = widgets.VBox(
        [configuration_summary, controls],
        layout=widgets.Layout(width="100%", grid_gap="0"),
    )
    configuration_panel.add_class("lab-configuration-panel")
    styles = widgets.HTML(
        STYLES + standard_view_styles(".recursive-analysis-lab"),
        layout=widgets.Layout(height="0px", min_height="0px", overflow="hidden"),
    )
    app = widgets.VBox([
        styles,
        configuration_panel,
        visualization,
        method,
    ], layout=widgets.Layout(width="100%", grid_gap="0"))
    app.add_class("recursive-analysis-lab")
    rebuild()
    clear_output(wait=True)
    display(app)


if __name__ == "__main__":
    run_app()
