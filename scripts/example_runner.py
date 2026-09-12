"""Editor ejecutable con las entradas de cada ejemplo del libro."""

from __future__ import annotations

import ast
import hashlib
import html
import re

try:
    from scripts.book_code_languages import translations
except ModuleNotFoundError:
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
# Completa estas auxiliares según el problema que estés analizando.
def foo1():
    raise NotImplementedError("Completa foo1 en el editor")


def foo2():
    raise NotImplementedError("Completa foo2 en el editor")


def foo(n):
    raise NotImplementedError("Completa foo en el editor")"""
    fn = functions[0]
    args = ", ".join(arg.arg for arg in fn.args.args)
    call = fn.name + "(" + args + ")"
    finish = "resultado = " + call + '\nprint("Resultado:", resultado)'
    if fn.name == "ordenar":
        finish = 'print("Arreglo inicial:", arr)\n' + call + '\nprint("Arreglo ordenado:", arr)'
    elif folio in (151, 153, 158, 161, 164, 166):
        finish = call + '\nprint("Ejemplo finalizado")'
    return source + "\n\n# Entradas editables del ejemplo.\n" + setup + "\n\n" + finish + "\n"


def render_runner(listing: dict) -> str:
    key = hashlib.sha256((str(listing["folio"]) + listing["code"]).encode()).hexdigest()[:12]
    code = html.escape(runnable_example(listing))
    title = html.escape(listing["title"], quote=True)
    return (
        f'<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p>'
        "<p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p>"
        f'<details><summary>Editar código y entradas</summary><label for="runner-{key}">Código Python · {title}</label>'
        f'<textarea id="runner-{key}" spellcheck="false" wrap="off" rows="14">{code}</textarea></details>'
        '<div class="example-runner-actions"><button type="button" data-run>Ejecutar</button>'
        '<button type="button" data-stop disabled>Detener</button>'
        '<button type="button" data-reset>Restablecer ejemplo</button></div>'
        '<p data-status role="status">Listo para ejecutar.</p>'
        '<pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>'
    )
