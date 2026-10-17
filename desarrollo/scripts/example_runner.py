"""Editor ejecutable con las entradas de cada ejemplo del libro."""

from __future__ import annotations

import ast
import hashlib
import html
import re

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import CLexer, JavaLexer, PythonLexer

try:
    from desarrollo.scripts.book_code_languages import translations
    from desarrollo.scripts.c_examples import c_example
    from desarrollo.scripts.java_examples import java_example
except ModuleNotFoundError:
    from book_code_languages import translations
    from c_examples import c_example
    from java_examples import java_example


def highlighted_line(source: str, lexer) -> str:
    """Mantiene estable el HTML entre versiones de Pygments."""
    rendered = highlight(source, lexer, HtmlFormatter(nowrap=True)).rstrip("\n")
    return "".join(
        fragment if fragment.startswith("<") else fragment.replace('"', "&quot;")
        for fragment in re.split(r"(<[^>]+>)", rendered)
    )


def runnable_example(listing: dict) -> str:
    source = translations(listing)["Python"]
    folio = listing["folio"]
    inputs = []
    for match in re.finditer(r"(\w+) = (\[\[.*?\]\]|\[.*?\]|-?\d+)", listing["example"]):
        inputs.append(match.group(0))
    setup = "\n".join(inputs)
    functions = [node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef)]
    if folio == 148:
        return setup + "\nm = [[1, 2], [3, 4]]\nj = 1\n\n" + source + '\nprint("arr[i]:", arr[i])\nprint("m[i][j]:", m[i][j])\n'
    if folio == 254:
        setup = """from types import SimpleNamespace

raiz = SimpleNamespace(dato=5, izquierdo=SimpleNamespace(
    dato=3, izquierdo=None, derecho=None), derecho=None)
valor = 3"""
    if folio in (170, 171, 172, 173):
        setup = """n = 3
var = False

# Valores de los predicados para esta prueba de escritorio.
def g(n):
    return False


def h(n):
    return True


def r(n):
    print("Se ejecuta la alternativa r(n)")


def s(n):
    print("Se ejecuta la alternativa s(n)")"""
        source += '\nprint("Evaluación de condiciones completada")'
        return setup + "\n\n" + source
    if folio in (161, 166):
        setup += """\n
# Estas auxiliares dependen del problema y no están definidas en el libro.
def foo1():
    raise NotImplementedError("El libro no define foo1; depende del problema analizado.")


def foo2():
    raise NotImplementedError("El libro no define foo2; depende del problema analizado.")


def foo(n):
    raise NotImplementedError("El libro no define foo; depende del problema analizado.")"""
    fn = functions[0]
    args = ", ".join(arg.arg for arg in fn.args.args)
    call = fn.name + "(" + args + ")"
    finish = "resultado = " + call + '\nprint("Resultado:", resultado)'
    if fn.name == "ordenar":
        finish = call + '\nprint("Arreglo ordenado:", arr)'
    elif folio in (151, 153, 158, 161, 164, 166):
        finish = call + '\nprint("Ejemplo finalizado")'
    return source + "\n\n# Entradas editables del ejemplo.\n" + setup + "\n\n" + finish + "\n"


def render_runner(listing: dict, executable_only: bool = False, *, include_pseudocode: bool = False) -> str:
    # Pages inicia con el mismo arreglo que carga el botón «Generar arreglo
    # del libro» de cada notebook de búsqueda u ordenamiento.
    book_arrays = {
        262: [0, 1, 2, 3, 4, 5, 6, 7],
        268: [2, 3, 5, 9, 10, 11, 21, 43],
        273: [2, 3, 5, 9, 10, 11, 21, 43],
        278: [0, 10, 20, 30, 40, 60, 80, 90],
        290: [1, 2, 3, 4, 5, 6, 7, 8],
        298: [1, 2, 3, 4, 5, 6, 7, 8],
        307: [1, 2, 3, 4, 5, 6, 7, 8],
        312: [1, 2, 3, 4, 5, 6, 7, 8],
        321: [5, 1, 4, 2, 8],
        323: [5, 1, 4, 2, 8],
        327: [64, 25, 12, 22, 11],
        329: [64, 25, 12, 22, 11],
        333: [5, 2, 4, 6, 1, 3],
        341: [38, 27, 43, 3, 9, 82, 10],
        349: [10, 7, 8, 9, 1, 5],
        363: [170, 45, 75, 90, 802, 24, 2, 66],
    }
    if listing["folio"] in book_arrays:
        listing = dict(listing)
        values = book_arrays[listing["folio"]]
        listing["example"] = re.sub(
            r"arr\s*=\s*\[[^\]]*\]",
            "arr = " + repr(values),
            listing["example"],
            count=1,
        )
        if listing["folio"] in {268, 273, 278, 307, 312, 341, 349}:
            listing["example"] = re.sub(r"\bb\s*=\s*\d+", f"b = {len(values) - 1}", listing["example"], count=1)
    key = hashlib.sha256((str(listing["folio"]) + listing["code"]).encode()).hexdigest()[:12]
    source = runnable_example(listing)
    editable = set()
    implementation = translations(listing)["Python"]
    implementation_start = source.find(implementation)
    implementation_end = implementation_start + len(implementation)
    offsets = [0]
    for line in source.splitlines(keepends=True):
        offsets.append(offsets[-1] + len(line))
    for node in ast.parse(source).body:
        if (
            isinstance(node, ast.Assign)
            and not any(isinstance(target, ast.Name) and target.id == "resultado" for target in node.targets)
            and not implementation_start <= offsets[node.lineno - 1] < implementation_end
        ):
            editable.update(range(node.lineno, node.end_lineno + 1))
    rows = []
    for number, line in enumerate(source.splitlines(), 1):
        colored = highlighted_line(line, PythonLexer())
        attrs = (
            (f' contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea {number}" spellcheck="false" data-editable')
            if number in editable
            else ""
        )
        colored = colored or " "
        rows.append(f'<span class="python-code-line" data-code-line{attrs}>{colored}</span>')
    editor_html = "".join(rows)
    java_source, java_inputs, java_class = java_example(listing)
    java_rows = []
    for _number, line in enumerate(java_source.splitlines(), 1):
        entry = next((item for item in java_inputs if line.strip() == item[0]), None)
        if entry:
            declaration, literal, kind, variable = entry
            start = line.rfind(literal)
            prefix, suffix = line[:start], line[start + len(literal) :]
            color = lambda text: highlighted_line(text, JavaLexer())
            content = (
                color(prefix)
                + f'<span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: {variable}" spellcheck="false" data-editable data-java-input="{variable}">{color(literal)}</span>'
                + color(suffix)
            )
        else:
            content = highlighted_line(line, JavaLexer())
        content = content or " "
        row_attrs = " data-editable-row" if entry else ""
        java_rows.append(f'<span class="python-code-line" data-code-line{row_attrs}>{content}</span>')
    java_html = "".join(java_rows)
    c_source, c_inputs, c_key = c_example(listing)
    c_rows = []
    for line in c_source.splitlines():
        entry = next((item for item in c_inputs if line.strip() == item[0]), None)
        color = lambda text: highlighted_line(text, CLexer())
        if entry:
            _, literal, _, variable = entry
            start = line.rfind(literal)
            content = color(line[:start]) + f'<span contenteditable="plaintext-only" role="textbox" aria-label="Entrada C: {variable}" spellcheck="false" data-editable data-c-input="{variable}">{color(literal)}</span>' + color(line[start + len(literal):])
        else:
            content = color(line) or " "
        attrs = " data-editable-row" if entry else ""
        c_rows.append(f'<span class="python-code-line" data-code-line{attrs}>{content}</span>')
    c_html = "".join(c_rows)
    title = html.escape(listing["title"], quote=True)
    pseudocode_html = "".join(
        f'<span class="python-code-line" data-code-line>{html.escape(line) or " "}</span>'
        for line in translations(listing)["Pseudocódigo"].splitlines()
    ) if include_pseudocode else ""
    pseudocode_tab = (
        f'<button type="button" role="tab" id="pseudocode-tab-{key}" aria-controls="pseudocode-code-{key}" '
        'aria-selected="true" data-language-tab="pseudocode">Pseudocódigo</button>'
    ) if include_pseudocode else ""
    pseudocode_panel = (
        f'<div id="pseudocode-code-{key}" role="tabpanel" aria-labelledby="pseudocode-tab-{key}" '
        f'class="python-code-editor highlight" data-language="pseudocode" '
        f'aria-label="Pseudocódigo · {title}"><pre><code>{pseudocode_html}</code></pre></div>'
    ) if include_pseudocode else ""
    pseudocode_note = (
        '<p data-runner-note="pseudocode">El pseudocódigo es una representación general del algoritmo y no se puede ejecutar.</p>'
    ) if include_pseudocode else ""
    editable_note = (
        '<p data-runner-note="editable" hidden>Solo las líneas de entrada resaltadas son editables. '
        'La implementación y la llamada al algoritmo son de solo lectura.</p>'
        if include_pseudocode
        else "<p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p>"
    )
    initial_language = "pseudocode" if include_pseudocode else "java"
    java_selected = "false" if include_pseudocode else "true"
    java_inactive = ' tabindex="-1"' if include_pseudocode else ""
    java_hidden = " hidden" if include_pseudocode else ""
    pseudocode_disabled = " disabled" if include_pseudocode else ""
    execution_attribute = " data-execution-ui hidden" if include_pseudocode else ""
    return (
        '<div class="example-runner" data-example-runner>'
        "<details open><summary>Ver código y editar entradas</summary>"
        f'<input type="hidden" data-runner-language value="{initial_language}">'
        '<div class="runner-language-tabs" role="tablist" aria-label="Lenguaje del ejemplo">'
        f'{pseudocode_tab}'
        f'<button type="button" role="tab" id="java-tab-{key}" aria-controls="java-code-{key}" aria-selected="{java_selected}"{java_inactive} data-language-tab="java">Java</button>'
        f'<button type="button" role="tab" id="python-tab-{key}" aria-controls="runner-{key}" aria-selected="false" tabindex="-1" data-language-tab="python">Python</button>'
        f'<button type="button" role="tab" id="c-tab-{key}" aria-controls="c-code-{key}" aria-selected="false" tabindex="-1" data-language-tab="c">C</button></div>'
        f'{editable_note}'
        f'{pseudocode_panel}'
        f'{pseudocode_note}'
        f'<div id="java-code-{key}" role="tabpanel" aria-labelledby="java-tab-{key}" class="python-code-editor highlight" data-language="java" data-java-class="{java_class}"{java_hidden} aria-label="Código Java · {title}"><pre><code>{java_html}</code></pre></div>'
        f'<div id="runner-{key}" role="tabpanel" aria-labelledby="python-tab-{key}" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · {title}"><pre><code>{editor_html}</code></pre></div>'
        f'<div id="c-code-{key}" role="tabpanel" aria-labelledby="c-tab-{key}" class="python-code-editor highlight" data-language="c" data-c-key="{c_key}" hidden aria-label="Código C · {title}"><pre><code>{c_html}</code></pre></div>'
        f'<p class="java-runtime-credit runtime-credit" data-runtime-credit="java"{java_hidden}>Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>.</p>'
        '<p class="runtime-credit" data-runtime-credit="python" hidden>Python se ejecuta en tu navegador con <a href="https://pyodide.org/en/stable/" target="_blank" rel="noopener">Pyodide</a>.</p>'
        '<p class="runtime-credit" data-runtime-credit="c" hidden>C se ejecuta en tu navegador mediante <a href="https://webassembly.org/" target="_blank" rel="noopener">WebAssembly</a>.</p>'
        f'<div class="example-runner-actions"><button type="button" data-run{pseudocode_disabled}><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button>'
        '<button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button>'
        f'<button type="button" data-reset{pseudocode_disabled}><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Reestablecer</span></button></div>'
        f'<p data-status{execution_attribute} role="status">Listo para ejecutar.</p>'
        f'<pre data-output{execution_attribute} aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></details></div>'
    )
