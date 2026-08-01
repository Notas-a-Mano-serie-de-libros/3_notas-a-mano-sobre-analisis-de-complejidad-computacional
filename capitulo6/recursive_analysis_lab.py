from __future__ import annotations

import asyncio
import html
import math
import re
from dataclasses import dataclass, field

import ipywidgets as widgets
from IPython.display import clear_output, display
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import CLexer, JavaLexer, PythonLexer


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
        events.append({"kind": "enter", "node": node_id, "stack": tuple(stack)})
        for child_value in _children(algorithm, value):
            visit(child_value, depth + 1, node_id)
        events.append({"kind": "return", "node": node_id, "stack": tuple(stack)})
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
    visible = [node for node in nodes if node.id in discovered]
    levels: dict[int, list[Node]] = {}
    for node in visible:
        levels.setdefault(node.depth, []).append(node)
    width = 720
    height = max(250, 84 + 84 * max(levels, default=0))
    positions: dict[int, tuple[float, float]] = {}
    for depth, level_nodes in levels.items():
        for index, node in enumerate(level_nodes, 1):
            positions[node.id] = (
                width * index / (len(level_nodes) + 1), 44 + depth * 84
            )
    edges = []
    circles = []
    for node in visible:
        if node.parent in positions:
            x1, y1 = positions[node.parent]
            x2, y2 = positions[node.id]
            edges.append(
                f'<line x1="{x1:.1f}" y1="{y1 + 23:.1f}" '
                f'x2="{x2:.1f}" y2="{y2 - 27:.1f}" class="lab-edge" '
                'marker-end="url(#lab-arrow-head)"/>'
            )
        x, y = positions[node.id]
        state = "base" if not node.children else "recursive"
        circles.append(
            f'<g class="lab-node {state}"><circle cx="{x:.1f}" cy="{y:.1f}" r="23"/>'
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


def _call_stack_panel(
    algorithm: str, nodes: list[Node], events: list[dict], step: int
) -> str:
    event = events[step]
    active_stack = event["stack"]
    current = event["node"]
    is_base = not nodes[current].children
    frames = []
    completed = {
        item["node"] for item in events[: step + 1] if item["kind"] == "return"
    }
    for node_id in reversed(active_stack):
        node = nodes[node_id]
        css = " current-return" if node_id == current and event["kind"] == "return" else " current-call" if node_id == current else ""
        state = (
            "Caso base · retorna"
            if node_id == current and event["kind"] == "return" and is_base
            else "Se desapila"
            if node_id == current and event["kind"] == "return"
            else "Nueva llamada"
            if node_id == current
            else "En espera"
        )
        frames.append(
            f'<div class="lab-call-frame{css}">'
            rf'<b>\({_frame_expression(algorithm, node, nodes, completed)}\)</b>'
            f'<span>{state}</span></div>'
        )
    return (
        '<div class="lab-call-stack" aria-label="Pila de llamadas">'
        + "".join(frames)
        + '<div class="lab-stack-base">Base de la pila · problema original</div></div>'
    )


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


def _code_panel(algorithm: str, language: str, is_base: bool) -> str:
    lines = CODE_SNIPPETS[language][algorithm]
    return_lines = [
        index
        for index, line in enumerate(lines)
        if line.strip().startswith(("return ", "retornar "))
    ]
    active_line = return_lines[0] if is_base else return_lines[-1]
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
.recursive-analysis-lab{box-sizing:border-box;width:100%;padding:14px 4px;background:#fff;color:#333;font-family:sans-serif}
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
.lab-controls{box-sizing:border-box!important;width:100%!important;padding:12px!important;border:0!important;background:#fff!important;margin:0!important}
.lab-controls .widget-label{color:#333;font-weight:700}
.lab-controls select{box-sizing:border-box;width:176px!important;height:32px;padding:2px 4px;border:1px solid #ccc;border-radius:3px;background:#fff!important;color:#333;font-size:13px;text-align:center;text-align-last:center;appearance:auto!important}
.lab-controls select option{background:#fff;color:#333}
.lab-controls input:not([type="range"]){box-sizing:border-box;width:176px!important;height:32px!important;padding:2px 4px!important;border:1px solid #ccc!important;border-radius:3px!important;background:#fff!important;color:#333!important;font-size:13px!important;text-align:center!important}
.lab-controls .lab-field{width:176px!important;height:32px!important}.lab-controls .lab-field input{width:176px!important;height:32px!important}
.lab-controls .lab-field.widget-disabled{opacity:1!important}.lab-controls .lab-field input:disabled{opacity:1!important;background:#f7f7f7!important;color:#333!important;cursor:default!important}
.lab-control-row{width:280px!important;min-width:280px!important;max-width:280px!important}.lab-control-row>.widget-html{flex:0 0 96px!important;width:96px!important}.lab-control-row>.widget-dropdown,.lab-control-row>.widget-text,.lab-control-row>.widget-int{flex:0 0 176px!important;width:176px!important}
.lab-controls input[type="number"]{-moz-appearance:textfield!important;appearance:textfield!important}
.lab-controls input[type="number"]::-webkit-inner-spin-button,.lab-controls input[type="number"]::-webkit-outer-spin-button{-webkit-appearance:none!important;margin:0!important}
.lab-controls .widget-readout{background:#fff!important;color:#333!important;font-family:sans-serif!important}
.lab-controls button{box-sizing:border-box;width:auto!important;height:32px;border:1px solid #bbb;border-radius:3px;background:#fff;color:#333;font-size:14px}
.lab-controls button:hover{background:#f1f1f1}
.lab-controls input[type="range"]{accent-color:#5f6368}
.lab-parameter-controls{width:100%!important;column-gap:36px!important;row-gap:12px!important}.lab-actions{box-sizing:border-box!important;width:100%!important;margin:0!important;padding-top:4px!important;justify-content:flex-end!important}
.lab-section{box-sizing:border-box;width:100%;margin:0;border:1px solid #dedede;border-bottom:0;border-radius:0;background:#fff;overflow:hidden}.lab-section:first-child{border-radius:5px 5px 0 0}.lab-section:last-child{border-bottom:1px solid #dedede;border-radius:0 0 5px 5px}
.lab-section>summary{box-sizing:border-box;width:100%;padding:9px 12px;cursor:pointer;background:#f7f7f7;color:#333;font-size:16px;font-weight:700;line-height:1.45}.lab-section[open]>summary{border-bottom:1px solid #e2e2e2}.lab-section-content{box-sizing:border-box;width:100%;background:#fff}
.lab-code-summary{display:flex!important;height:44px!important;min-height:44px!important;max-height:44px!important;align-items:center;justify-content:space-between;overflow:hidden}.lab-language-logo{display:block;flex:0 0 26px;width:26px;height:26px;object-fit:contain}
.lab-analysis-panel{margin:0;border-bottom:1px solid #dedede!important;border-radius:0 0 5px 5px!important}.lab-analysis-steps{padding:10px 18px 14px;font-size:16px;line-height:1.55}.lab-analysis-step{margin:8px 0 14px!important;line-height:1.55}.lab-analysis-step-title{font-weight:700;text-align:left}.lab-analysis-step-solution{width:100%;padding:4px 12px 0;text-align:center}.lab-analysis-result{margin:16px 0 2px!important}.lab-analysis-equation{padding:6px 0 4px;font-size:18px}
.lab-visual-sections{width:100%;margin:0}.lab-code-panel{border-radius:0!important}.lab-code-panel[open] .lab-code{height:auto;min-height:0}
.lab-state-panel{border-bottom:0!important;border-radius:0!important}
.lab-execution-grid{display:grid;width:100%;grid-template-columns:repeat(2,minmax(0,1fr));gap:0}.lab-execution-grid>.lab-section{border-radius:0}.lab-execution-grid>.lab-section:first-child{border-right:0}.lab-execution-grid>.lab-section[open]{height:470px}.lab-execution-grid>.lab-section:not([open]){height:auto}
.lab-code{height:auto;min-height:0;padding:0;overflow-x:auto;overflow-y:hidden;background:#fff;font:14px/1.55 ui-monospace,SFMono-Regular,Consolas,monospace}
.lab-code-line{display:grid;grid-template-columns:42px minmax(max-content,1fr);min-height:28px;white-space:pre-wrap}.lab-line-number{display:flex;align-items:center;justify-content:center;padding:3px 4px;border-right:1px solid #d8d8d8;background:#f2f2f2;color:#666!important;font-weight:700;user-select:none}.lab-line-source{display:block;padding:3px 10px;border-left:3px solid transparent;background:#fff}.lab-code-line.current .lab-line-number{background:#ece8d8;color:#444!important}.lab-code-line.current .lab-line-source{background:#f4e8bd;border-left-color:#a47b20}
.lab-code .k{color:#005cc5;font-weight:600}.lab-code .kt,.lab-code .nb,.lab-code .bp{color:#005cc5}.lab-code .nf{color:#6f42c1}.lab-code .n{color:#24292e}.lab-code .mi,.lab-code .mf{color:#005a8d}.lab-code .s,.lab-code .s1,.lab-code .s2{color:#22863a}.lab-code .c,.lab-code .c1,.lab-code .cm{color:#6a737d;font-style:italic}.lab-code .o{color:#d73a49}.lab-code .p{color:#24292e}
.lab-tree-scroll{height:426px;overflow:auto;background:#fff}.lab-tree{display:block;width:100%;min-width:520px;background:#fff}
.lab-edge{fill:none;stroke:#202124;stroke-width:1.7}.lab-arrow-head{fill:#202124!important;stroke:none!important}.lab-node circle{fill:#fff;stroke:#202124;stroke-width:1.7}.lab-node text{text-anchor:middle;font-family:"STIX Two Math","Cambria Math","Times New Roman",serif;font-size:15px;font-weight:400;fill:#111!important}.lab-node.base circle{fill:#e8f5e9;stroke:#202124}
.lab-call-stack{display:flex;height:426px;flex-direction:column;justify-content:flex-end;align-items:center;gap:5px;padding:14px 18px 0;overflow:auto;background:#fff}
.lab-call-frame{display:flex;width:min(100%,330px);align-items:center;justify-content:space-between;gap:12px;padding:8px 12px;border:1px solid #bbb;border-radius:3px;background:#f7f7f7}
.lab-call-frame b{font-family:"STIX Two Math","Cambria Math","Times New Roman",serif}.lab-call-frame span{font-size:12px;color:#5f6368!important}
.lab-call-frame.current-call{border:2px solid #a47b20;background:#f4e8bd}.lab-call-frame.current-return{border:2px solid #3d7d47;background:#e8f5e9}
.lab-stack-base{width:min(100%,360px);padding:6px 10px;border-top:2px solid #202124;text-align:center;color:#5f6368!important;font-size:12px}
.lab-metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:0;overflow:hidden}.lab-metric{padding:10px;text-align:center;border-right:1px solid #e2e2e2;background:#fff}.lab-metric:last-child{border-right:0}.lab-metric b{display:block;font-size:18px}
@media(max-width:760px){.lab-execution-grid{grid-template-columns:1fr}.lab-execution-grid>.lab-section:first-child{border-right:1px solid #dedede}.lab-metrics{grid-template-columns:repeat(2,1fr)}.lab-metric:nth-child(2){border-right:0}.lab-metric:nth-child(-n+2){border-bottom:1px solid #e2e2e2}}
</style>
"""


def run_app():
    algorithm = widgets.Dropdown(
        options=[(value["name"], key) for key, value in ALGORITHMS.items()],
        value="factorial",
        layout=widgets.Layout(width="176px", height="32px"),
    )
    analysis_type = widgets.Dropdown(
        options=[("Temporal", "temporal"), ("Espacial", "espacial")],
        value="temporal",
        layout=widgets.Layout(width="176px", height="32px"),
    )
    language = widgets.Dropdown(
        options=[
            ("Pseudocódigo", "pseudocode"), ("Python", "python"),
            ("Java", "java"), ("C", "c"),
        ],
        value="pseudocode",
        layout=widgets.Layout(width="176px", height="32px"),
    )
    size = widgets.BoundedIntText(
        value=5, min=1, max=12, step=1,
        disabled=True,
        layout=widgets.Layout(width="176px", height="32px"),
    )
    size.add_class("lab-field")
    previous = widgets.Button(description="Anterior", icon="step-backward")
    following = widgets.Button(description="Siguiente", icon="step-forward")
    play = widgets.Button(description="Reproducir", icon="play")
    reset = widgets.Button(description="Reiniciar", icon="refresh")
    method = widgets.HTMLMath(layout=widgets.Layout(width="100%"))
    visualization = widgets.HTMLMath(layout=widgets.Layout(width="100%"))
    state = {"nodes": [], "events": [], "step": 0, "play_task": None}

    def stop_playback():
        task = state.get("play_task")
        if task is not None and not task.done():
            task.cancel()
        state["play_task"] = None
        play.description = "Reproducir"
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
        method.value = _method_panel(algorithm.value, data, analysis_type.value)
        render()

    def render(*_):
        nodes, events = state["nodes"], state["events"]
        if not events:
            return
        step = min(state["step"], len(events) - 1)
        event = events[step]
        data = ALGORITHMS[algorithm.value]
        entered = sum(item["kind"] == "enter" for item in events[: step + 1])
        returned = sum(item["kind"] == "return" for item in events[: step + 1])
        maximum_depth = max(len(item["stack"]) for item in events[: step + 1])
        visualization.value = (
            '<div class="lab-visual-sections">'
            '<details class="lab-section lab-code-panel" open>'
            '<summary class="lab-code-summary"><span>Código activo</span>'
            + _language_logo(language.value)
            + '</summary><div class="lab-section-content">'
            + _code_panel(
                algorithm.value, language.value, not nodes[event["node"]].children
            )
            + '</div></details>'
            '<details class="lab-section lab-state-panel" open><summary>Estado de la ejecución</summary>'
            '<div class="lab-section-content lab-metrics">'
            f'<div class="lab-metric"><b>{step + 1}/{len(events)}</b>Evento</div>'
            f'<div class="lab-metric"><b>{entered}</b>Llamadas iniciadas</div>'
            f'<div class="lab-metric"><b>{returned}</b>Llamadas terminadas</div>'
            f'<div class="lab-metric"><b>{maximum_depth}</b>Profundidad máxima</div>'
            '</div></details><div class="lab-execution-grid">'
            '<details class="lab-section" open><summary>Pila de recursión</summary>'
            '<div class="lab-section-content">'
            + _call_stack_panel(algorithm.value, nodes, events, step)
            + '</div></details><details class="lab-section" open>'
            '<summary>Árbol de recursión</summary><div class="lab-section-content">'
            + _tree_svg(nodes, events, step)
            + "</div></details></div></div>"
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
        method.value = _method_panel(
            algorithm.value, ALGORITHMS[algorithm.value], change["new"]
        )
        render()

    analysis_type.observe(select_analysis, names="value")
    language.observe(render, names="value")

    def move_step(delta):
        if not state["events"]:
            return
        state["step"] = min(
            max(0, state["step"] + delta), len(state["events"]) - 1
        )
        render()

    async def play_process():
        try:
            while state["step"] < len(state["events"]) - 1:
                await asyncio.sleep(0.65)
                move_step(1)
        except asyncio.CancelledError:
            return
        finally:
            state["play_task"] = None
            play.description = "Reproducir"
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
        state["play_task"] = asyncio.get_running_loop().create_task(play_process())

    previous.on_click(lambda _: (stop_playback(), move_step(-1)))
    following.on_click(lambda _: (stop_playback(), move_step(1)))
    play.on_click(toggle_playback)
    reset.on_click(lambda _: (stop_playback(), state.update(step=0), render()))

    def labeled(label, control):
        label_widget = widgets.HTML(
            value=f'<b>{html.escape(label)}</b>',
            layout=widgets.Layout(width="96px"),
        )
        row = widgets.HBox(
            [label_widget, control],
            layout=widgets.Layout(width="280px", align_items="center", gap="8px"),
        )
        row.add_class("lab-control-row")
        return row

    analysis_controls = widgets.VBox(
        [
            labeled("Algoritmo", algorithm),
            labeled("Análisis", analysis_type),
        ],
        layout=widgets.Layout(width="280px", gap="8px"),
    )
    input_controls = widgets.VBox(
        [
            labeled("Lenguaje", language),
            labeled("Entrada n", size),
        ],
        layout=widgets.Layout(width="280px", gap="8px"),
    )
    parameter_controls = widgets.HBox(
        [analysis_controls, input_controls],
        layout=widgets.Layout(flex_flow="row wrap", gap="36px", align_items="flex-start"),
    )
    parameter_controls.add_class("lab-parameter-controls")
    action_controls = widgets.HBox(
        [previous, following, play, reset],
        layout=widgets.Layout(gap="6px", justify_content="flex-end"),
    )
    action_controls.add_class("lab-actions")
    controls = widgets.VBox(
        [parameter_controls, action_controls],
        layout=widgets.Layout(
            width="100%", align_items="stretch", gap="12px"
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
        layout=widgets.Layout(width="100%", gap="0"),
    )
    configuration_panel.add_class("lab-configuration-panel")
    styles = widgets.HTML(
        STYLES,
        layout=widgets.Layout(height="0px", min_height="0px", overflow="hidden"),
    )
    app = widgets.VBox([
        styles,
        configuration_panel,
        visualization,
        method,
    ], layout=widgets.Layout(width="100%", gap="0"))
    app.add_class("recursive-analysis-lab")
    rebuild()
    clear_output(wait=True)
    display(app)


if __name__ == "__main__":
    run_app()
