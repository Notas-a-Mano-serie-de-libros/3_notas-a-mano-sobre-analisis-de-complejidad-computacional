"""Prueba de escritorio: pseudocódigo resaltado y traza paso a paso.

El módulo no depende de ``ipywidgets``: recibe filas ya calculadas y devuelve
HTML. Las búsquedas generan sus filas con :func:`search_desk_row` y los
ordenamientos las derivan de la traza de eventos con :func:`sort_desk_rows`.
"""

from __future__ import annotations

import re
from html import escape

DESK_ROW_LIMIT = 40
DESK_TITLE = "Prueba de escritorio"
_INITIAL_HINT = "Presione Paso siguiente o Ejecución automática para iniciar la prueba de escritorio."

# Cada línea es (clave, texto). La clave identifica el paso que la ejecuta;
# ``None`` marca líneas que sólo estructuran el pseudocódigo. Los marcadores
# {gt}, {lt}, {le}, {ge} y {order} se adaptan al orden ascendente/descendente.
PSEUDOCODE = {
    "secuencial": (
        (None, "procedimiento busquedaSecuencial(A, n, x)"),
        ("loop", "  para i ← 0 hasta n - 1 hacer"),
        ("compare", "    si A[i] = x entonces"),
        ("found", "      retornar i"),
        ("not_found", "  retornar -1"),
    ),
    "binaria": (
        (None, "procedimiento busquedaBinaria(A, n, x)"),
        ("init", "  a ← 0;  b ← n - 1"),
        ("while", "  mientras a ≤ b hacer"),
        ("mid", "    m ← a + ⌊(b - a) / 2⌋"),
        ("found", "    si A[m] = x entonces retornar m"),
        ("go_right", "    sino si A[m] < x entonces a ← m + 1"),
        ("go_left", "    sino b ← m - 1"),
        ("not_found", "  retornar -1"),
    ),
    "interpolacion": (
        (None, "procedimiento busquedaInterpolacion(A, n, x)"),
        ("init", "  a ← 0;  b ← n - 1"),
        ("while", "  mientras a ≤ b y A[a] ≤ x ≤ A[b] hacer"),
        ("probe", "    p ← a + ⌊(b - a) · (x - A[a]) / (A[b] - A[a])⌋"),
        ("found", "    si A[p] = x entonces retornar p"),
        ("go_right", "    sino si A[p] < x entonces a ← p + 1"),
        ("go_left", "    sino b ← p - 1"),
        ("not_found", "  retornar -1"),
    ),
    "saltos": (
        (None, "procedimiento busquedaSaltos(A, n, x)"),
        ("init", "  salto ← ⌊√n⌋;  inicio ← 0"),
        ("block_loop", "  mientras inicio < n hacer"),
        (None, "    fin ← min(inicio + salto, n)"),
        ("decide", "    si A[fin - 1] ≥ x entonces"),
        ("linear", "      para i ← inicio hasta fin - 1 hacer"),
        ("compare", "        si A[i] = x entonces"),
        ("found", "          retornar i"),
        (None, "      retornar -1"),
        ("next_block", "    inicio ← fin"),
        ("not_found", "  retornar -1"),
    ),
    "exponencial": (
        (None, "procedimiento busquedaExponencial(A, n, x)"),
        ("init", "  i ← 0"),
        ("exp_while", "  mientras i < n y A[i] < x hacer"),
        ("exp_next", "    i ← (i = 0) ? 1 : 2 · i"),
        ("range", "  a ← ⌊i / 2⌋;  b ← min(i, n - 1)"),
        ("bin_while", "  mientras a ≤ b hacer           // búsqueda binaria"),
        ("mid", "    m ← a + ⌊(b - a) / 2⌋"),
        ("found", "    si A[m] = x entonces retornar m"),
        ("go_right", "    sino si A[m] < x entonces a ← m + 1"),
        ("go_left", "    sino b ← m - 1"),
        ("not_found", "  retornar -1"),
    ),
    "ternaria": (
        (None, "procedimiento busquedaTernaria(A, n, x)"),
        ("init", "  a ← 0;  b ← n - 1"),
        ("while", "  mientras a ≤ b hacer"),
        ("points", "    m1 ← ⌊a + (b - a) / 3⌋;  m2 ← ⌊b - (b - a) / 3⌋"),
        ("found", "    si A[m1] = x o A[m2] = x entonces retornar ese índice"),
        ("go_left", "    si x < A[m1] entonces b ← m1 - 1"),
        ("go_right", "    sino si x > A[m2] entonces a ← m2 + 1"),
        ("go_middle", "    sino a ← m1 + 1;  b ← m2 - 1"),
        ("not_found", "  retornar -1"),
    ),
    "burbuja": (
        (None, "procedimiento burbuja(A, n)"),
        ("outer", "  para i ← 0 hasta n - 2 hacer"),
        (None, "    intercambiado ← falso"),
        ("bound", "    b ← n - 1 - i"),
        ("inner", "    para j ← 0 hasta b - 1 hacer"),
        ("compare", "      si A[j] {gt} A[j + 1] entonces"),
        ("swap", "        intercambiar A[j] con A[j + 1];  intercambiado ← verdadero"),
        ("fix", "    A[b] queda en su posición final"),
        ("early", "    si no intercambiado entonces terminar"),
        ("end", "  retornar A"),
    ),
    "seleccion": (
        (None, "procedimiento seleccion(A, n)"),
        ("outer", "  para i ← n - 1 hasta 1 (decreciendo) hacer"),
        ("init", "    m ← 0"),
        ("inner", "    para j ← 1 hasta i hacer"),
        ("compare", "      si A[j] {gt} A[m] entonces"),
        ("update", "        m ← j"),
        ("keep", "    si m ≠ i entonces"),
        ("swap", "      intercambiar A[m] con A[i]"),
        ("end", "  retornar A"),
    ),
    "insercion": (
        (None, "procedimiento insercion(A, n)"),
        ("outer", "  para i ← 1 hasta n - 1 hacer"),
        ("pick", "    x ← A[i];  j ← i - 1"),
        ("while", "    mientras j ≥ 0 y A[j] {gt} x hacer"),
        ("shift", "      A[j + 1] ← A[j];  j ← j - 1"),
        ("insert", "    A[j + 1] ← x"),
        ("end", "  retornar A"),
    ),
    "insercion_binaria": (
        (None, "procedimiento insercionBinaria(A, n)"),
        ("outer", "  para i ← 1 hasta n - 1 hacer"),
        ("pick", "    x ← A[i];  a ← 0;  b ← i"),
        ("while", "    mientras a < b hacer"),
        ("mid", "      m ← a + ⌊(b - a) / 2⌋"),
        ("range", "      si A[m] {le} x entonces a ← m + 1  sino b ← m"),
        ("pos", "    pos ← a"),
        ("shift", "    para j ← i hasta pos + 1 (decreciendo): A[j] ← A[j - 1]"),
        ("insert", "    A[pos] ← x"),
        ("end", "  retornar A"),
    ),
    "shell": (
        (None, "procedimiento shell(A, n)"),
        ("gap", "  para cada salto h de la secuencia (de mayor a menor) hacer"),
        ("outer", "    para k ← h hasta n - 1 hacer"),
        ("pick", "      j ← k"),
        ("while", "      mientras j ≥ h hacer"),
        ("compare", "        si A[j - h] {gt} A[j] entonces"),
        ("swap", "          intercambiar A[j - h] con A[j];  j ← j - h"),
        (None, "        sino salir del ciclo"),
        ("place", "      el elemento queda ubicado en su subarreglo"),
        ("end", "  retornar A"),
    ),
    "mezcla": (
        ("call", "// llamada inicial: mezcla(A, 0, n - 1)"),
        (None, "procedimiento mezcla(A, inicio, fin)"),
        ("base", "  si inicio ≥ fin entonces retornar"),
        ("divide", "  medio ← ⌊(inicio + fin) / 2⌋"),
        (None, "  mezcla(A, inicio, medio);  mezcla(A, medio + 1, fin)"),
        (None, "  intercalar(A, inicio, medio, fin)"),
        (None, ""),
        (None, "procedimiento intercalar(A, inicio, medio, fin)"),
        ("merge_init", "  i ← inicio;  j ← medio + 1;  k ← inicio"),
        (None, "  mientras k ≤ fin hacer"),
        ("merge_loop", "    si j > fin o (i ≤ medio y A[i] {le} A[j]) entonces"),
        (None, "      B[k] ← A[i];  i ← i + 1"),
        (None, "    sino  B[k] ← A[j];  j ← j + 1"),
        (None, "    k ← k + 1"),
        ("merge_done", "  copiar B[inicio..fin] en A[inicio..fin]"),
        ("end", "// A queda ordenado"),
    ),
    "rapido_lomuto": (
        ("work", "procedimiento rapido(A, inicio, fin)"),
        ("base", "  si inicio ≥ fin entonces retornar"),
        ("pivot", "  elegir el pivote según la estrategia"),
        ("move", "  llevar el pivote a la posición fin"),
        (None, "  i ← inicio"),
        (None, "  para j ← inicio hasta fin - 1 hacer"),
        ("compare", "    si A[j] {le} pivote entonces"),
        ("apply", "      intercambiar A[i] con A[j];  i ← i + 1"),
        ("place", "  intercambiar A[i] con A[fin]"),
        ("recurse", "  rapido(A, inicio, i - 1);  rapido(A, i + 1, fin)"),
        ("end", "// A queda ordenado"),
    ),
    "rapido_hoare": (
        ("work", "procedimiento rapido(A, inicio, fin)"),
        ("base", "  si inicio ≥ fin entonces retornar"),
        ("pivot", "  elegir el pivote (permanece en su posición p)"),
        (None, "  i ← inicio;  j ← fin"),
        (None, "  repetir"),
        ("scan_i", "    mientras A[i] {le} pivote hacer  i ← i + 1"),
        ("scan_j", "    mientras A[j] {ge} pivote hacer  j ← j - 1"),
        ("cross", "    si i ≥ j entonces salir del ciclo"),
        ("swap", "    intercambiar A[i] con A[j];  i ← i + 1;  j ← j - 1"),
        ("place", "  colocar el pivote en su posición final p"),
        ("recurse", "  rapido(A, inicio, p - 1);  rapido(A, p + 1, fin)"),
        ("end", "// A queda ordenado"),
    ),
    "radix": (
        (None, "procedimiento radix(A, n, base)"),
        ("passes", "  p ← cantidad de dígitos de la clave máxima"),
        (None, "  para i ← 1 hasta p hacer"),
        (None, "    crear las cubetas C[0 .. base - 1] vacías"),
        ("distribute", "    para cada x en A (de izquierda a derecha) hacer"),
        (None, "      d ← ⌊x / base^(i - 1)⌋ mod base;  agregar x a C[d]"),
        (None, "    k ← 0"),
        ("collect", "    para cada cubeta C[d] en orden {order} hacer"),
        (None, "      para cada x en C[d]: A[k] ← x;  k ← k + 1"),
        ("pass_end", "    // pasada i terminada"),
        ("end", "  retornar A"),
    ),
}

_ORDER_TOKENS = {
    False: {"{gt}": ">", "{lt}": "<", "{le}": "≤", "{ge}": "≥", "{order}": "ascendente"},
    True: {"{gt}": "<", "{lt}": ">", "{le}": "≥", "{ge}": "≤", "{order}": "descendente"},
}

_STYLES = """<style>
.desk-check { display: flex; flex-wrap: wrap; gap: 16px; align-items: flex-start; color: inherit; font-family: inherit; }
.desk-check__code { flex: 1 1 340px; min-width: 260px; max-width: 100%; border: 1px solid rgba(128,128,128,.4); padding: 8px 0; overflow-x: auto; }
.desk-check__line { display: flex; border-left: 4px solid transparent; font: 13px/1.65 SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; white-space: pre; padding: 0 12px 0 0; }
.desk-check__num { flex: 0 0 34px; text-align: right; padding-right: 12px; opacity: .55; user-select: none; }
.desk-check__line--active { background: rgba(139,75,50,.20); border-left-color: #8b4b32; font-weight: 700; }
.desk-check__line--active .desk-check__num { opacity: 1; color: #8b4b32; }
.desk-check__trace { flex: 2 1 460px; min-width: 280px; max-height: 340px; overflow: auto; border: 1px solid rgba(128,128,128,.4); }
.desk-check__table { width: 100%; border-collapse: collapse; font-size: 13px; line-height: 1.45; }
.desk-check__table th, .desk-check__table td { border-bottom: 1px solid rgba(128,128,128,.3); padding: 5px 9px; text-align: left; vertical-align: top; }
.desk-check__table th { position: sticky; top: 0; background: rgba(128,128,128,.18); backdrop-filter: blur(6px); z-index: 1; }
.desk-check__table tr:last-child td { font-weight: 600; background: rgba(139,75,50,.12); }
.desk-check__table td.desk-check__step { text-align: right; white-space: nowrap; }
.desk-check__table td.desk-check__mono { font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; font-size: 12px; }
.desk-check__note { font-size: 12px; opacity: .75; margin: 6px 9px; }
.desk-check__empty { font-size: 13px; opacity: .8; padding: 12px; }
</style>"""


def pseudocode_for(algorithm, descending=False):
    """Devuelve las líneas (clave, texto) del algoritmo con el orden aplicado."""

    tokens = _ORDER_TOKENS[bool(descending)]
    lines = []
    for key, text in PSEUDOCODE.get(algorithm, ()):
        for token, value in tokens.items():
            text = text.replace(token, value)
        lines.append((key, text))
    return lines


def pseudocode_algorithm_key(state):
    """Clave de pseudocódigo para el estado de una simulación de ordenamiento."""

    algorithm = state.get("algorithm")
    if algorithm == "rapido":
        return "rapido_lomuto" if state.get("partition_scheme") == "lomuto" else "rapido_hoare"
    return algorithm


_LATEX_STEPS = (
    (re.compile(r"\\begin\{array\}\{l\}|\\end\{array\}|\\displaystyle"), ""),
    (re.compile(r"\\\\\[\d+pt\]"), "; "),
    (re.compile(r",\s*\\q?quad\s*"), ", "),
    (re.compile(r"\\q?quad\s*|\\ "), " "),
    (re.compile(r"\\leftrightarrow"), "↔"),
    (re.compile(r"\\leftarrow"), "←"),
    (re.compile(r"\\left|\\right"), ""),
    (re.compile(r"\\lfloor"), "⌊"),
    (re.compile(r"\\rfloor"), "⌋"),
    (re.compile(r"\\leq?\b"), "≤"),
    (re.compile(r"\\geq?\b"), "≥"),
    (re.compile(r"\\cdot"), "·"),
    (re.compile(r"\\bmod"), "mod"),
    (re.compile(r"\\(?:text|operatorname)\{([^{}]*)\}"), r"\1"),
)
_FRACTION = re.compile(r"\\frac\{([^{}]*)\}\{([^{}]*)\}")
_SUBSCRIPT_BRACES = re.compile(r"([A-Za-z])_\{([^{}]*)\}")
_SUBSCRIPT_CHAR = re.compile(r"([A-Za-z])_([A-Za-z0-9])")
_SUPERSCRIPT = re.compile(r"\^\{([^{}]*)\}")


def latex_to_text(formula):
    """Convierte las fórmulas LaTeX de la traza en texto plano legible."""

    text = str(formula or "")
    for pattern, replacement in _LATEX_STEPS:
        text = pattern.sub(replacement, text)
    for _ in range(3):
        text = _FRACTION.sub(r"(\1)/(\2)", text)
    text = _SUBSCRIPT_BRACES.sub(r"\1[\2]", text)
    text = _SUBSCRIPT_CHAR.sub(r"\1[\2]", text)
    text = _SUPERSCRIPT.sub(r"^\1", text)
    text = text.replace("{", "").replace("}", "")
    text = re.sub(r"\s+", " ", text).strip(" ;,")
    if text.lower().startswith("arreglo ordenado"):
        return ""
    return text


def desk_row(step, line, variables, action, array=None):
    return {
        "step": step,
        "line": line,
        "vars": variables or "",
        "action": action or "",
        "array": None if array is None else list(array),
    }


def _node_value(state, index):
    nodes = state.get("arr", [])
    if index is None or not 0 <= index < len(nodes):
        return None
    return nodes[index]["value"]


def _found_index(state):
    for index, node in enumerate(state.get("arr", [])):
        if node.get("role") == "found":
            return index
    return None


def _search_line_and_variables(algorithm, before, after):
    target = after.get("target")
    phase = before.get("phase")
    complete = bool(after.get("search_complete"))
    found_index = _found_index(after) if complete else None
    found = found_index is not None

    if algorithm == "secuencial":
        index = before.get("current_index", 0)
        if found:
            return "found", f"i = {found_index}, A[i] = {target} = x"
        if complete:
            return "not_found", f"i = {len(after['arr'])}, x = {target}"
        if phase == "show_current":
            return "loop", f"i = {index}, x = {target}"
        return "compare", f"i = {index}, A[i] = {_node_value(before, index)}, x = {target}"

    if algorithm == "binaria":
        low, high, mid = after["low"], after["high"], after["mid"]
        if found:
            return "found", f"m = {found_index}, A[m] = {target} = x"
        if complete:
            return "not_found", f"a = {low}, b = {high} (a > b)"
        if phase == "select":
            return "mid", f"a = {low}, b = {high}, m = {mid}, A[m] = {_node_value(after, mid)}"
        direction = "go_right" if _node_value(before, before["mid"]) < target else "go_left"
        return direction, f"a = {low}, b = {high}, x = {target}"

    if algorithm == "interpolacion":
        low, high, pos = after["low"], after["high"], after["pos"]
        if found:
            return "found", f"p = {found_index}, A[p] = {target} = x"
        if complete:
            return "not_found", f"a = {low}, b = {high}, x = {target}"
        if phase == "probe":
            return "probe", f"a = {low}, b = {high}, p = {pos}, A[p] = {_node_value(after, pos)}"
        direction = "go_right" if _node_value(before, before["pos"]) < target else "go_left"
        return direction, f"a = {low}, b = {high}, x = {target}"

    if algorithm == "saltos":
        jump, start, end = after["jump_size"], after["block_start"], after["block_end"]
        linear = after.get("linear_index")
        if found:
            return "found", f"i = {found_index}, A[i] = {target} = x"
        if complete:
            return "not_found", f"salto = {jump}, x = {target}"
        if phase == "show_block":
            return "block_loop", f"salto = {jump}, inicio = {start}, fin = {end}"
        if phase == "decide_block":
            last = _node_value(before, before["block_end"] - 1)
            if after.get("phase") == "linear_show":
                return "decide", f"fin = {before['block_end']}, A[fin - 1] = {last} ≥ x = {target}"
            return "next_block", f"A[fin - 1] = {last} < x = {target}; inicio = {start}, fin = {end}"
        if phase == "linear_show":
            return "linear", f"i = {linear}"
        index = before.get("linear_index")
        return "compare", f"i = {index}, A[i] = {_node_value(before, index)}, x = {target}"

    if algorithm == "exponencial":
        index = before.get("current_index")
        if found:
            mid = after.get("mid")
            if mid is not None and str(phase).startswith("binary"):
                return "found", f"m = {found_index}, A[m] = {target} = x"
            return "found", f"i = {found_index}, A[i] = {target} = x"
        if complete:
            return "not_found", f"a = {after.get('low')}, b = {after.get('high')}"
        if phase == "exponential_show":
            if after.get("phase") == "range_show":
                return "range", f"i = {index}, a = {after['low']}, b = {after['high']}"
            return "exp_while", f"i = {index}, A[i] = {_node_value(before, index)}, x = {target}"
        if phase == "exponential_compare":
            if after.get("phase") == "range_show":
                return "range", f"i = {index}, a = {after['low']}, b = {after['high']}"
            return "exp_next", f"A[i] = {_node_value(before, index)} < x = {target}; i = {after['current_index']}"
        if phase == "range_show":
            return "bin_while", f"a = {after['low']}, b = {after['high']}"
        if phase == "binary_select":
            mid = after["mid"]
            return "mid", f"a = {after['low']}, b = {after['high']}, m = {mid}, A[m] = {_node_value(after, mid)}"
        direction = "go_right" if _node_value(before, before["mid"]) < target else "go_left"
        return direction, f"a = {after['low']}, b = {after['high']}, x = {target}"

    if algorithm == "ternaria":
        low, high = after["a"], after["b"]
        if found:
            return "found", f"A[{found_index}] = {target} = x"
        if complete:
            return "not_found", f"a = {low}, b = {high}, x = {target}"
        if phase == "select":
            return "points", f"a = {low}, b = {high}, m1 = {after['m1']}, m2 = {after['m2']}"
        first = _node_value(before, before["m1"])
        second = _node_value(before, before["m2"])
        if target < first:
            line = "go_left"
        elif target > second:
            line = "go_right"
        else:
            line = "go_middle"
        return line, f"a = {low}, b = {high}, A[m1] = {first}, A[m2] = {second}, x = {target}"

    return None, ""


def search_desk_row(algorithm, before, after, step):
    """Fila de la prueba de escritorio para un paso de búsqueda."""

    line, variables = _search_line_and_variables(algorithm, before, after)
    return desk_row(step, line, variables, after.get("general_message"))


def sort_infer_line(algorithm_key, event):
    """Infiere la línea de pseudocódigo a partir del evento si no viene etiquetado."""
    line = event.get("desk_line")
    if line:
        return line
    msg = str(event.get("message", "")).lower()
    formula = str(event.get("formula", "")).lower()
    comp = bool(event.get("sorting_complete"))

    if comp:
        return "end"

    if algorithm_key == "burbuja":
        if "compara" in msg:
            return "compare"
        if "intercambia" in msg:
            return "swap"
        if "fija" in msg:
            return "fix"
        if "termina" in msg or "finaliza" in msg:
            return "end"

    elif algorithm_key == "seleccion":
        if "comienza" in msg:
            return "init"
        if "compara" in msg:
            return "compare"
        if "es el nuevo" in msg:
            return "update"
        if "intercambia" in msg:
            return "swap"
        if "ya está" in msg:
            return "keep"

    elif algorithm_key == "insercion":
        if "comienza" in msg:
            return "outer"
        if "marca" in msg:
            return "pick"
        if "compara" in msg:
            return "while"
        if "mueve" in msg:
            return "shift"
        if "insertado" in msg or "inserta" in msg:
            return "insert"

    elif algorithm_key == "insercion_binaria":
        if "busca" in msg:
            return "pick"
        if "compara" in msg:
            return "mid"
        if "actualiza" in msg:
            return "range"
        if "posición de inserción" in msg:
            return "pos"
        if "desplaza" in msg:
            return "shift"
        if "inserta" in msg:
            return "insert"

    elif algorithm_key == "shell":
        if "pasada" in msg:
            return "gap"
        if "compara" in msg:
            return "compare"
        if "intercambia" in msg:
            return "swap"
        if "ubicado" in msg:
            return "place"

    elif algorithm_key == "mezcla":
        if "comienza" in msg:
            return "call"
        if "divide" in msg:
            return "divide"
        if "ordenado" in msg or "caso base" in formula:
            return "base"
        if "mezcla" in msg:
            return "merge_init"
        if "compara" in msg or "inserta" in msg:
            return "merge_loop"
        if "termina" in msg:
            return "merge_done"

    elif algorithm_key == "rapido_lomuto":
        if "comienza" in msg:
            return "work"
        if "trabaja" in msg or "ordenado" in msg:
            return "base"
        if "selecciona" in msg:
            return "pivot"
        if "mueve el pivote" in msg:
            return "move"
        if "compara" in msg or "permanece" in msg:
            return "compare"
        if "intercambia" in msg:
            return "apply"
        if "coloca" in msg or "posición final" in msg:
            return "place"

    elif algorithm_key == "rapido_hoare":
        if "comienza" in msg:
            return "work"
        if "ordenado" in msg:
            return "base"
        if "selecciona" in msg:
            return "pivot"
        if "avanza" in msg:
            return "scan_i"
        if "retrocede" in msg:
            return "scan_j"
        if "cruzan" in msg:
            return "cross"
        if "intercambia" in msg:
            return "swap"
        if "queda ordenado" in msg or "posición" in msg:
            return "place"

    elif algorithm_key == "radix":
        if "cantidad de pasadas" in msg or "calcula" in msg:
            return "passes"
        if "dígito" in msg and "bucket" in msg:
            return "distribute"
        if "escribe" in msg:
            return "collect"
        if "pasada" in msg:
            return "pass_end"

    return None


def sort_desk_rows(state, limit=DESK_ROW_LIMIT):
    """Filas derivadas de los eventos ya ejecutados de un ordenamiento."""

    trace = state.get("trace")
    step = int(state.get("step_index", 0) or 0)
    if trace is None or step <= 0:
        return []
    events = trace.materialize() if hasattr(trace, "materialize") else trace
    last = min(step, len(events) - 1)
    algo_key = pseudocode_algorithm_key(state)
    rows = []
    for index in range(max(1, last - limit + 1), last + 1):
        event = events[index]
        variables = event.get("desk_vars")
        if variables is None:
            variables = latex_to_text(event.get("formula", ""))
        line = sort_infer_line(algo_key, event)
        rows.append(desk_row(index, line, variables, event.get("message"), event.get("arr")))
    return rows


def _format_array(values):
    return "[" + ", ".join("—" if value is None else str(value) for value in values) + "]"


def render_desk_check(algorithm, rows, *, descending=False, total_steps=None, show_array=False, limit=DESK_ROW_LIMIT):
    """HTML del panel: pseudocódigo con la línea activa y tabla de seguimiento."""

    lines = pseudocode_for(algorithm, descending)
    if not lines:
        return ""
    rows = list(rows or ())
    visible = rows[-limit:]
    active = visible[-1]["line"] if visible else None

    code_html = []
    for number, (key, text) in enumerate(lines, start=1):
        is_active = key is not None and key == active
        css = "desk-check__line desk-check__line--active" if is_active else "desk-check__line"
        current = ' aria-current="step"' if is_active else ""
        code_html.append(
            f'<div class="{css}"{current}><span class="desk-check__num">{number}</span>'
            f'<span>{escape(text) or " "}</span></div>'
        )
    line_numbers = {key: number for number, (key, _text) in enumerate(lines, start=1) if key}

    if visible:
        body = []
        for row in visible:
            number = line_numbers.get(row["line"])
            line_cell = str(number) if number is not None else "—"
            array_cell = f'<td class="desk-check__mono">{escape(_format_array(row["array"]))}</td>' if show_array and row["array"] is not None else ("<td></td>" if show_array else "")
            body.append(
                f'<tr><td class="desk-check__step">{row["step"]}</td><td class="desk-check__step">{line_cell}</td>'
                f'<td class="desk-check__mono">{escape(row["vars"]) or "—"}</td>{array_cell}'
                f'<td>{escape(row["action"])}</td></tr>'
            )
        array_head = "<th>Arreglo</th>" if show_array else ""
        hidden = (rows[0]["step"] > 1) if rows else False
        note = ""
        if len(rows) > limit or hidden:
            note = f'<p class="desk-check__note">Se muestran los últimos {len(visible)} pasos' + (f" de {total_steps}" if total_steps else "") + ".</p>"
        trace_html = (
            f'{note}<table class="desk-check__table"><thead><tr><th>Paso</th><th>Línea</th><th>Variables</th>{array_head}<th>Acción</th></tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table>'
        )
    else:
        trace_html = f'<div class="desk-check__empty">{escape(_INITIAL_HINT)}</div>'

    return (
        f'{_STYLES}<div class="desk-check" role="region" aria-label="{DESK_TITLE}" aria-live="polite">'
        f'<div class="desk-check__code">{"".join(code_html)}</div>'
        f'<div class="desk-check__trace">{trace_html}</div></div>'
    )


__all__ = [
    "DESK_ROW_LIMIT",
    "DESK_TITLE",
    "PSEUDOCODE",
    "desk_row",
    "latex_to_text",
    "pseudocode_algorithm_key",
    "pseudocode_for",
    "render_desk_check",
    "search_desk_row",
    "sort_desk_rows",
]
