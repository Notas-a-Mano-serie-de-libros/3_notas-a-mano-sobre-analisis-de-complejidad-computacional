"""Editor ejecutable con las entradas de cada ejemplo del libro."""

from __future__ import annotations

import ast
import hashlib
import html
import re

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer, JavaLexer

try:
    from scripts.java_examples import java_example
    from scripts.book_code_languages import translations
except ModuleNotFoundError:
    from java_examples import java_example
    from book_code_languages import translations


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
        finish = 'print("Arreglo inicial:", arr)\n' + call + '\nprint("Arreglo ordenado:", arr)'
    elif folio in (151, 153, 158, 161, 164, 166):
        finish = call + '\nprint("Ejemplo finalizado")'
    return source + "\n\n# Entradas editables del ejemplo.\n" + setup + "\n\n" + finish + "\n"


def render_runner(listing: dict, executable_only: bool = False) -> str:
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
        colored = highlight(line, PythonLexer(), HtmlFormatter(nowrap=True)).rstrip("\n")
        attrs = (
            (f' contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea {number}" spellcheck="false" data-editable')
            if number in editable
            else ""
        )
        rows.append(f'<span class="python-code-line" data-code-line{attrs}>{colored}</span>')
    editor_html = "".join(rows)
    java_source, java_inputs, java_class = java_example(listing)
    java_rows = []
    for number, line in enumerate(java_source.splitlines(), 1):
        entry = next((item for item in java_inputs if line.strip() == item[0]), None)
        if entry:
            declaration, literal, kind, variable = entry
            start = line.rfind(literal)
            prefix, suffix = line[:start], line[start + len(literal) :]
            color = lambda text: highlight(text, JavaLexer(), HtmlFormatter(nowrap=True)).rstrip("\n")
            content = (
                color(prefix)
                + f'<span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: {variable}" spellcheck="false" data-editable data-java-input="{variable}">{color(literal)}</span>'
                + color(suffix)
            )
        else:
            content = highlight(line, JavaLexer(), HtmlFormatter(nowrap=True)).rstrip("\n")
        java_rows.append(f'<span class="python-code-line" data-code-line>{content}</span>')
    java_html = "".join(java_rows)
    title = html.escape(listing["title"], quote=True)
    intro = (
        "El navegador facilita la ejecución de código Java y Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Java ni Python; el código se ejecuta en tu navegador."
        if executable_only
        else "Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga el entorno del lenguaje elegido en el navegador."
    )
    return (
        f'<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p>'
        f"<p>{intro}</p>"
        "<details><summary>Ver código y editar entradas</summary>"
        f'<label for="language-{key}">Lenguaje del ejemplo</label><select id="language-{key}" data-runner-language><option value="java">Java</option><option value="python">Python</option></select>'
        "<p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p>"
        f'<div class="python-code-editor highlight" data-language="java" data-java-class="{java_class}" aria-label="Código Java · {title}"><pre><code>{java_html}</code></pre></div>'
        f'<div id="runner-{key}" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · {title}"><pre><code>{editor_html}</code></pre></div>'
        '<p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details>'
        '<div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button>'
        '<button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button>'
        '<button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div>'
        '<p data-status role="status">Listo para ejecutar.</p>'
        '<pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>'
    )
