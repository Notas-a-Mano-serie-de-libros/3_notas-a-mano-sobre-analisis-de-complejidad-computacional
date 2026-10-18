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
        (None, "función buscar(arr, x)"),
        ("loop", "    para i en rango(longitud(arr))"),
        ("compare", "        si arr[i] == x entonces"),
        ("found", "            retornar verdadero"),
        (None, ""),
        ("not_found", "    retornar falso"),
    ),
    "binaria": (
        (None, "función buscar(arr, a, b, x)"),
        ("while", "    mientras a <= b"),
        ("mid", "        m ← a + (b - a) div 2"),
        ("compare", "        si arr[m] == x entonces"),
        ("found", "            retornar verdadero"),
        ("go_right", "        si x > arr[m] entonces"),
        (None, "            a ← m + 1"),
        ("go_left", "        si no"),
        (None, "            b ← m - 1"),
        (None, ""),
        ("not_found", "    retornar falso"),
    ),
    "interpolacion": (
        (None, "función buscar(arr, a, b, x)"),
        ("while", "    mientras a <= b y x >= arr[a] y x <= arr[b]"),
        (None, "        num ← (b - a) * (x - arr[a])"),
        (None, "        den ← arr[b] - arr[a]"),
        (None, "        si den == 0 entonces"),
        (None, "            retornar arr[a] == x"),
        (None, ""),
        ("probe", "        p ← a + num div den"),
        ("compare", "        si arr[p] == x entonces"),
        ("found", "            retornar verdadero"),
        ("go_right", "        si x > arr[p] entonces"),
        (None, "            a ← p + 1"),
        ("go_left", "        si no"),
        (None, "            b ← p - 1"),
        (None, ""),
        ("not_found", "    retornar falso"),
    ),
    "saltos": (
        (None, "función buscar(arr, x)"),
        (None, "    n ← longitud(arr)"),
        (None, "    si n == 0 entonces"),
        (None, "        retornar falso"),
        (None, ""),
        ("init", "    paso ← raízEntera(n)"),
        (None, "    anterior ← 0"),
        (None, "    delta ← paso"),
        (None, ""),
        ("decide", "    mientras arr[min(delta, n) - 1] < x"),
        ("next_block", "        anterior ← delta"),
        (None, "        delta += paso"),
        (None, "        si anterior >= n entonces"),
        (None, "            retornar falso"),
        (None, ""),
        ("linear", "    para i en rango(anterior, min(delta, n))"),
        ("compare", "        si arr[i] == x entonces"),
        ("found", "            retornar verdadero"),
        (None, ""),
        ("not_found", "    retornar falso"),
    ),
    "exponencial": (
        (None, "función buscar(arr, x)"),
        (None, "    n ← longitud(arr)"),
        (None, "    si n == 0 entonces"),
        (None, "        retornar falso"),
        (None, "    si arr[0] == x entonces"),
        (None, "        retornar verdadero"),
        (None, ""),
        ("init", "    i ← 1"),
        ("exp_while", "    mientras i < n y arr[i] <= x"),
        ("exp_next", "        i *= 2"),
        (None, ""),
        ("range", "    a ← i div 2"),
        (None, "    b ← min(i, n - 1)"),
        (None, "    retornar busquedaBinaria(arr, a, b, x)"),
        (None, ""),
        (None, "función busquedaBinaria(arr, a, b, x)"),
        ("bin_while", "    mientras a <= b"),
        ("mid", "        m ← a + (b - a) div 2"),
        ("compare", "        si arr[m] == x entonces"),
        ("found", "            retornar verdadero"),
        ("go_right", "        si x > arr[m] entonces"),
        (None, "            a ← m + 1"),
        ("go_left", "        si no"),
        (None, "            b ← m - 1"),
        (None, ""),
        ("not_found", "    retornar falso"),
    ),
    "ternaria": (
        (None, "función buscar(arr, a, b, x)"),
        ("while", "    mientras a <= b"),
        ("points", "        m1 ← a + (b - a) div 3"),
        (None, "        m2 ← b - (b - a + 2) div 3"),
        (None, ""),
        ("compare", "        si arr[m1] == x o arr[m2] == x entonces"),
        ("found", "            retornar verdadero"),
        ("go_left", "        si x < arr[m1] entonces"),
        (None, "            b ← m1 - 1"),
        ("go_right", "        si no, si x > arr[m2] entonces"),
        (None, "            a ← m2 + 1"),
        ("go_middle", "        si no"),
        (None, "            a ← m1 + 1"),
        (None, "            b ← m2 - 1"),
        (None, ""),
        ("not_found", "    retornar falso"),
    ),
    "burbuja": (
        (None, "función ordenar(arr)"),
        ("outer", "    para i en rango(longitud(arr) - 1, 0, -1)"),
        (None, "        intercambiado ← falso"),
        (None, ""),
        ("inner", "        para j en rango(i)"),
        ("compare", "            si arr[j] {gt} arr[j + 1] entonces"),
        (None, "                temp ← arr[j]"),
        ("swap", "                arr[j] ← arr[j + 1]"),
        (None, "                arr[j + 1] ← temp"),
        (None, "                intercambiado ← verdadero"),
        (None, ""),
        ("fix", "        si no intercambiado entonces"),
        ("end", "            break"),
    ),
    "seleccion": (
        (None, "función ordenar(arr)"),
        ("outer", "    para i en rango(longitud(arr) - 1)"),
        ("init", "        max ← 0"),
        (None, ""),
        ("inner", "        para j en rango(1, longitud(arr) - i)"),
        ("compare", "            si arr[j] {gt} arr[max] entonces"),
        ("update", "                max ← j"),
        (None, ""),
        ("keep", "        temp ← arr[max]"),
        ("swap", "        arr[max] ← arr[longitud(arr) - 1 - i]"),
        ("end", "        arr[longitud(arr) - 1 - i] ← temp"),
    ),
    "insercion": (
        (None, "función ordenar(arr)"),
        ("outer", "    para i en rango(1, longitud(arr))"),
        ("pick", "        clave ← arr[i]"),
        (None, "        j ← i - 1"),
        (None, ""),
        ("while", "        mientras j >= 0 y arr[j] {gt} clave"),
        ("shift", "            arr[j + 1] ← arr[j]"),
        (None, "            j -= 1"),
        (None, ""),
        ("insert", "        arr[j + 1] ← clave"),
    ),
    "insercion_binaria": (
        (None, "función ordenar(arr)"),
        ("outer", "    para i en rango(1, longitud(arr))"),
        ("pick", "        clave ← arr[i]; a ← 0; b ← i"),
        (None, ""),
        ("while", "        mientras a < b"),
        ("mid", "            m ← a + (b - a) div 2"),
        ("range", "            si arr[m] {le} clave entonces a ← m + 1  si no b ← m"),
        (None, ""),
        ("pos", "        pos ← a"),
        ("shift", "        para j en rango(i, pos, -1): arr[j] ← arr[j - 1]"),
        ("insert", "        arr[pos] ← clave"),
    ),
    "shell": (
        (None, "función ordenar(arr)"),
        ("gap", "    para cada salto h de la secuencia decreciente"),
        ("outer", "        para k en rango(h, longitud(arr))"),
        ("pick", "            j ← k"),
        (None, ""),
        ("while", "            mientras j >= h y arr[j - h] {gt} arr[j]"),
        ("swap", "                intercambiar arr[j - h] con arr[j]"),
        ("place", "                j -= h"),
        (None, ""),
        ("end", "    retornar arr"),
    ),
    "mezcla": (
        (None, "función ordenar(arr, a, b)"),
        ("base", "    si a >= b entonces retornar"),
        ("divide", "    m ← a + (b - a) div 2"),
        (None, "    ordenar(arr, a, m)"),
        (None, "    ordenar(arr, m + 1, b)"),
        ("call", "    combinar(arr, a, m, b)"),
        (None, ""),
        (None, "función combinar(arr, a, m, b)"),
        (None, "    izquierda ← arr[a:m + 1]"),
        (None, "    derecha ← arr[m + 1:b + 1]"),
        ("merge_init", "    i ← 0; j ← 0; k ← a"),
        (None, ""),
        ("merge_loop", "    mientras i < longitud(izquierda) y j < longitud(derecha)"),
        (None, "        si izquierda[i] {le} derecha[j] entonces arr[k] ← izquierda[i]; i += 1"),
        (None, "        si no arr[k] ← derecha[j]; j += 1"),
        (None, "        k += 1"),
        (None, ""),
        (None, "    mientras i < longitud(izquierda): arr[k] ← izquierda[i]; i += 1; k += 1"),
        (None, "    mientras j < longitud(derecha): arr[k] ← derecha[j]; j += 1; k += 1"),
        (None, ""),
        ("merge_done", "    // subarreglo combinado"),
        ("end", "// ordenamiento finalizado"),
    ),
    "rapido_lomuto": (
        (None, "función ordenar(arr, a, b)"),
        ("base", "    si a >= b entonces retornar"),
        ("work", "    p ← particionar(arr, a, b)"),
        (None, "    ordenar(arr, a, p - 1)"),
        (None, "    ordenar(arr, p + 1, b)"),
        (None, ""),
        (None, "función particionar(arr, a, b)"),
        ("pivot", "    pivote ← arr[b]"),
        (None, "    i ← a"),
        (None, ""),
        (None, "    para j en rango(a, b)"),
        ("compare", "        si arr[j] {le} pivote entonces"),
        ("apply", "            intercambiar arr[i] con arr[j]; i += 1"),
        (None, ""),
        ("place", "    intercambiar arr[i] con arr[b]"),
        (None, "    retornar i"),
        ("end", "// partición completada"),
    ),
    "rapido_hoare": (
        (None, "función ordenar(arr, a, b)"),
        ("base", "    si a >= b entonces retornar"),
        ("work", "    p ← particionar(arr, a, b)"),
        (None, "    ordenar(arr, a, p - 1)"),
        (None, "    ordenar(arr, p + 1, b)"),
        (None, ""),
        (None, "función particionar(arr, a, b)"),
        ("pivot", "    pivote ← arr[a]"),
        (None, "    i ← a + 1; j ← b"),
        (None, ""),
        ("cross", "    mientras i <= j"),
        ("scan_i", "        mientras i <= j y arr[i] < pivote: i += 1"),
        ("scan_j", "        mientras i <= j y arr[j] > pivote: j -= 1"),
        ("swap", "        si i <= j entonces intercambiar arr[i] con arr[j]; i += 1; j -= 1"),
        (None, ""),
        ("place", "    intercambiar arr[a] con arr[j]"),
        (None, "    retornar j"),
        ("end", "// partición completada"),
    ),
    "radix": (
        (None, "función ordenar(arr)"),
        ("passes", "    maximo ← max(arr); d ← floor(log10(maximo)) + 1"),
        (None, "    para i en rango(1, d + 1)"),
        (None, "        ordenarPorDigito(arr, i)"),
        (None, ""),
        (None, "función ordenarPorDigito(arr, i)"),
        (None, "    n ← longitud(arr); exp ← 10 ** (i - 1)"),
        (None, "    conteo ← [0] * 10; salida ← [0] * n"),
        (None, ""),
        ("distribute", "    para valor en arr: conteo[(valor div exp) % 10] += 1"),
        (None, "    para j en rango(1, 10): conteo[j] += conteo[j - 1]"),
        (None, ""),
        ("collect", "    para j en rango(n - 1, -1, -1)"),
        (None, "        d ← (arr[j] div exp) % 10; salida[conteo[d] - 1] ← arr[j]; conteo[d] -= 1"),
        (None, ""),
        ("pass_end", "    arr[:] ← salida"),
        ("end", "// arreglo ordenado"),
    ),
}

_ORDER_TOKENS = {
    False: {"{gt}": ">", "{lt}": "<", "{le}": "<=", "{ge}": ">=", "{order}": "ascendente"},
    True: {"{gt}": "<", "{lt}": ">", "{le}": ">=", "{ge}": "<=", "{order}": "descendente"},
}

_STYLES = """<style>
.desk-check { display: flex; flex-wrap: wrap; gap: 16px; align-items: stretch; color: #111111; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 13px; }
.desk-check__code { flex: 1 1 360px; min-width: 280px; max-width: 100%; border: 1px solid var(--md-default-fg-color--lighter, rgba(128,128,128,.35)); border-radius: 4px; padding: 0; overflow-x: auto; overflow-y: hidden; background: var(--md-code-bg-color, rgba(128,128,128,.04)); box-sizing: border-box; height: calc(var(--desk-code-lines, 20) * 1.65em + 2px); }
.desk-check__code-inner { display: inline-block; min-width: 100%; padding-right: 28px; box-sizing: border-box; }
.desk-check__line { display: flex; align-items: stretch; width: 100%; font: 13px/1.65 SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; white-space: pre; min-height: 1.65em; box-sizing: border-box; }
.desk-check__line:first-child .desk-check__num { border-top-left-radius: 3px; }
.desk-check__line:last-child .desk-check__num { border-bottom-left-radius: 3px; }
.desk-check__num { flex: 0 0 38px; width: 38px; min-width: 38px; display: flex; align-items: center; justify-content: center; text-align: center; background: rgba(128,128,128,.10); border-right: 1px solid var(--md-default-fg-color--lighter, rgba(128,128,128,.35)); margin-right: 12px; color: var(--md-default-fg-color--light, inherit); opacity: .75; user-select: none; box-sizing: border-box; }
.desk-check__line--active { background: rgba(139,75,50,.18); font-weight: 700; }
.desk-check__line--active .desk-check__num { background: rgba(139,75,50,.30); border-right-color: #8b4b32; color: #8b4b32; opacity: 1; font-weight: 700; }
.desk-check__trace { flex: 2 1 480px; min-width: 300px; border: 1px solid var(--md-default-fg-color--lighter, rgba(128,128,128,.35)); border-radius: 4px; display: flex; flex-direction: column; overflow: hidden; background: var(--md-default-bg-color, #ffffff); box-sizing: border-box; height: calc(var(--desk-code-lines, 20) * 1.65em + 2px); max-height: calc(var(--desk-code-lines, 20) * 1.65em + 2px); min-height: 0; }
.desk-check__table-wrap { width: 100%; flex: 1 1 auto; overflow-y: auto; overflow-x: auto; position: relative; min-height: 0; }
.desk-check__table { width: 100%; border-collapse: separate; border-spacing: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 13px; line-height: 1.45; }
.desk-check__table th, .desk-check__table td { border-bottom: 1px solid rgba(128,128,128,.25); padding: 5px 8px; text-align: left; vertical-align: middle; }
.desk-check__table th { position: sticky; top: 0; background: var(--md-default-bg-color, #ffffff); background-color: rgba(246, 245, 243, 0.98); backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px); z-index: 10; box-shadow: 0 1px 0 rgba(128,128,128,.35); font-weight: 600; text-align: center; }
.desk-check__table tr:last-child td { font-weight: 600; background: rgba(139,75,50,.10); }
.desk-check__table td.desk-check__step, .desk-check__table th.desk-check__step { width: 1%; text-align: center; white-space: nowrap; font-variant-numeric: tabular-nums; padding: 5px 6px; }
.desk-check__table td.desk-check__mono { font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; font-size: 12px; }
.desk-check__table td.desk-check__var, .desk-check__table th.desk-check__var { font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; font-size: 12px; text-align: center; white-space: nowrap; padding: 5px 8px; }
.desk-check__table tbody tr:hover td { background: rgba(139,75,50,.07) !important; cursor: default; }
.desk-check__note { font-size: 12px; opacity: .75; margin: 4px 8px; flex: 0 0 auto; }
.desk-check__empty { font-size: 13px; opacity: .8; padding: 14px; flex: 1 1 auto; display: flex; align-items: center; }
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
    text = re.sub(r"\b[Aa]\[", "arr[", text)
    text = re.sub(r"\s+", " ", text).strip(" ;,")
    if text.lower().startswith("arreglo ordenado"):
        return ""
    return text


def parse_desk_vars(variables):
    """Extrae un diccionario {nombre_variable: valor} a partir del texto de variables."""

    if isinstance(variables, dict):
        return {
            re.sub(r"\b[Aa]\[", "arr[", str(k)): str(v)
            for k, v in variables.items()
        }
    text = str(variables or "").strip()
    if not text:
        return {}
    parts = re.split(r"[,;]\s*", text)
    result = {}
    for part in parts:
        part = part.strip()
        if not part or "↔" in part or "valores de h" in part:
            continue
        if "<" in part and "=" in part and ("A[" in part or "a[" in part or "arr[" in part):
            subparts = re.split(r"\s*[<>]+\s*", part)
            for sp in subparts:
                if "=" in sp:
                    k, v = sp.split("=", 1)
                    k_clean = re.sub(r"\b[Aa]\[", "arr[", k.strip())
                    result[k_clean] = v.strip()
            continue
        m = re.match(r"^([a-zA-Z_áéíóúÁÉÍÓÚ][a-zA-Z0-9_áéíóúÁÉÍÓÚ\[\]\s+-]*?)\s*(?:=|←)\s*(.+)$", part)
        if m:
            var_name = m.group(1).strip()
            var_name = re.sub(r"\b[Aa]\[", "arr[", var_name)
            rest = m.group(2).strip()
            if "=" in rest:
                eqs = [e.strip() for e in rest.split("=")]
                val = eqs[-1] if not (eqs[-1].isalpha() and len(eqs[-1]) == 1 and eqs[0].isdigit()) else eqs[0]
            else:
                val = rest
            val = re.split(r"\s*[<>≤≥]\s*", val)[0].strip()
            if var_name:
                result[var_name] = val
    return result


def simplify_desk_action(action):
    """Simplifica la frase de acción para la prueba de escritorio: (condición); acción corta."""
    if not action:
        return ""
    text = str(action).strip()
    text = re.sub(r"^(?:Búsqueda (?:lineal|binaria|secuencial)|Fase de saltos|Fase exponencial):\s*", "", text)

    m = re.match(r"^(-?\d+)\s+es menor que\s+(-?\d+);\s*(.+?)\.?$", text, re.IGNORECASE)
    if m:
        outcome = m.group(3).replace("la mitad ", "mitad ")
        return f"{m.group(1)} < {m.group(2)}; {outcome}"

    m = re.match(r"^(-?\d+)\s+es mayor que\s+(-?\d+);\s*(.+?)\.?$", text, re.IGNORECASE)
    if m:
        outcome = m.group(3).replace("la mitad ", "mitad ")
        return f"{m.group(1)} > {m.group(2)}; {outcome}"

    m = re.match(r"^(-?\d+)\s+es mayor o igual que\s+(-?\d+);\s*(.+?)\.?$", text, re.IGNORECASE)
    if m:
        outcome = re.sub(r"comienza la búsqueda secuencial en este bloque", "inicia búsqueda secuencial", m.group(3), flags=re.IGNORECASE)
        return f"{m.group(1)} ≥ {m.group(2)}; {outcome}"

    m = re.match(r"^(-?\d+)\s+no coincide;\s*(.+?)\.?$", text, re.IGNORECASE)
    if m:
        outcome = re.sub(r"avanza al siguiente elemento", "avanza siguiente", m.group(2), flags=re.IGNORECASE)
        outcome = re.sub(r"avanza dentro del bloque", "avanza en bloque", outcome, flags=re.IGNORECASE)
        return f"{m.group(1)} ≠ x; {outcome}"

    m = re.match(r"^(-?\d+)\s+está entre\s+(-?\d+)\s+y\s+(-?\d+);\s*(.+?)\.?$", text, re.IGNORECASE)
    if m:
        return f"{m.group(2)} < {m.group(1)} < {m.group(3)}; {m.group(4)}"

    m = re.match(r"^[Ee]valúa\s+([a-zA-Z0-9_]+)\s+en la posición\s+(-?\d+)\.?$", text)
    if m:
        return f"Evalúa {m.group(1)} = {m.group(2)}"

    m = re.match(r"^[Ee]stima\s+([a-zA-Z0-9_]+)\s+en la posición\s+(-?\d+).*$", text)
    if m:
        return f"Estima {m.group(1)} = {m.group(2)}"

    m = re.match(r"^[Cc]ompara contra\s+(.+?)\.?$", text)
    if m:
        c = m.group(1).replace(" y ", ", ")
        return f"Compara {c}"

    m = re.match(r"^[Mm]uestra el bloque\s+(\[[^\]]+\])\.?$", text)
    if m:
        return f"Bloque {m.group(1)}"

    m = re.match(r"^[Cc]ompara la posición\s+(-?\d+).*$", text)
    if m:
        return f"Compara pos {m.group(1)}"

    m = re.match(r"^[Cc]omienza en la posición\s+(-?\d+)\.?$", text)
    if m:
        return f"Inicia en pos {m.group(1)}"

    m = re.match(r"^[Cc]ompara las posiciones\s+(-?\d+)\s+y\s+(-?\d+)\.?$", text)
    if m:
        return f"Compara pos {m.group(1)} y {m.group(2)}"

    m = re.match(r"^[Ii]ntercambia las posiciones\s+(-?\d+)\s+y\s+(-?\d+)\.?$", text)
    if m:
        return f"Intercambia pos {m.group(1)} y {m.group(2)}"

    return text.rstrip(".")


def desk_row(step, line, variables, action, array=None):
    var_dict = parse_desk_vars(variables)
    short_action = simplify_desk_action(action)
    return {
        "step": step,
        "line": line,
        "vars": variables or "",
        "var_dict": var_dict,
        "action": short_action,
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
            return "found", f"i = {found_index}, arr[i] = {target} = x"
        if complete:
            return "not_found", f"i = {len(after['arr'])}, x = {target}"
        if phase == "show_current":
            return "loop", f"i = {index}, x = {target}"
        return "compare", f"i = {index}, arr[i] = {_node_value(before, index)}, x = {target}"

    if algorithm == "binaria":
        low, high, mid = after["low"], after["high"], after["mid"]
        if found:
            return "found", f"m = {found_index}, arr[m] = {target} = x"
        if complete:
            return "not_found", f"a = {low}, b = {high} (a > b)"
        if phase == "select":
            return "mid", f"a = {low}, b = {high}, m = {mid}, arr[m] = {_node_value(after, mid)}"
        direction = "go_right" if _node_value(before, before["mid"]) < target else "go_left"
        return direction, f"a = {low}, b = {high}, x = {target}"

    if algorithm == "interpolacion":
        low, high, pos = after["low"], after["high"], after["pos"]
        if found:
            return "found", f"p = {found_index}, arr[p] = {target} = x"
        if complete:
            return "not_found", f"a = {low}, b = {high}, x = {target}"
        if phase == "probe":
            return "probe", f"a = {low}, b = {high}, p = {pos}, arr[p] = {_node_value(after, pos)}"
        direction = "go_right" if _node_value(before, before["pos"]) < target else "go_left"
        return direction, f"a = {low}, b = {high}, x = {target}"

    if algorithm == "saltos":
        jump, start, end = after["jump_size"], after["block_start"], after["block_end"]
        linear = after.get("linear_index")
        if found:
            return "found", f"i = {found_index}, arr[i] = {target} = x"
        if complete:
            return "not_found", f"salto = {jump}, x = {target}"
        if phase == "show_block":
            return "decide", f"salto = {jump}, inicio = {start}, fin = {end}"
        if phase == "decide_block":
            last = _node_value(before, before["block_end"] - 1)
            if after.get("phase") == "linear_show":
                return "decide", f"fin = {before['block_end']}, arr[fin - 1] = {last} ≥ x = {target}"
            return "next_block", f"arr[fin - 1] = {last} < x = {target}; inicio = {start}, fin = {end}"
        if phase == "linear_show":
            return "linear", f"i = {linear}"
        index = before.get("linear_index")
        return "compare", f"i = {index}, arr[i] = {_node_value(before, index)}, x = {target}"

    if algorithm == "exponencial":
        index = before.get("current_index")
        if found:
            mid = after.get("mid")
            if mid is not None and str(phase).startswith("binary"):
                return "found", f"m = {found_index}, arr[m] = {target} = x"
            return "found", f"i = {found_index}, arr[i] = {target} = x"
        if complete:
            return "not_found", f"a = {after.get('low')}, b = {after.get('high')}"
        if phase == "exponential_show":
            if after.get("phase") == "range_show":
                return "range", f"i = {index}, a = {after['low']}, b = {after['high']}"
            return "exp_while", f"i = {index}, arr[i] = {_node_value(before, index)}, x = {target}"
        if phase == "exponential_compare":
            if after.get("phase") == "range_show":
                return "range", f"i = {index}, a = {after['low']}, b = {after['high']}"
            return "exp_next", f"arr[i] = {_node_value(before, index)} < x = {target}; i = {after['current_index']}"
        if phase == "range_show":
            return "bin_while", f"a = {after['low']}, b = {after['high']}"
        if phase == "binary_select":
            mid = after["mid"]
            return "mid", f"a = {after['low']}, b = {after['high']}, m = {mid}, arr[m] = {_node_value(after, mid)}"
        direction = "go_right" if _node_value(before, before["mid"]) < target else "go_left"
        return direction, f"a = {after['low']}, b = {after['high']}, x = {target}"

    if algorithm == "ternaria":
        low, high = after["a"], after["b"]
        if found:
            return "found", f"arr[{found_index}] = {target} = x"
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
        return line, f"a = {low}, b = {high}, arr[m1] = {first}, arr[m2] = {second}, x = {target}"

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
    cache = state.setdefault("_desk_row_cache", {})
    rows = []
    for index in range(max(1, last - limit + 1), last + 1):
        if index in cache:
            rows.append(cache[index])
            continue
        event = events[index]
        variables = event.get("desk_vars")
        if variables is None:
            variables = latex_to_text(event.get("formula", ""))
        line = sort_infer_line(algo_key, event)
        row = desk_row(index, line, variables, event.get("message"), event.get("arr"))
        cache[index] = row
        rows.append(row)
    return rows


def _format_array(values):
    return "[" + ", ".join("—" if value is None else str(value) for value in values) + "]"


def _collect_variable_columns(rows):
    """Obtiene el conjunto ordenado de nombres de variables presentes en las filas."""
    columns = []
    for row in rows:
        var_dict = row.get("var_dict")
        if not var_dict and row.get("vars"):
            var_dict = parse_desk_vars(row["vars"])
        if var_dict:
            for key in var_dict.keys():
                if key not in columns:
                    columns.append(key)
    return columns


def render_desk_check(algorithm, rows, *, descending=False, total_steps=None, show_array=False, limit=DESK_ROW_LIMIT):
    """HTML del panel: pseudocódigo con la línea activa y tabla de seguimiento."""

    lines = pseudocode_for(algorithm, descending)
    if not lines:
        return ""
    rows = list(rows or ())
    visible = rows[-limit:]
    active = visible[-1]["line"] if visible else None

    code_html = []
    line_numbers = {}
    for number, (key, text) in enumerate(lines, start=1):
        if key:
            line_numbers[key] = number
        is_active = key is not None and key == active
        css = "desk-check__line desk-check__line--active" if is_active else "desk-check__line"
        current = ' aria-current="step"' if is_active else ""
        line_content = escape(text) if text.strip() else "&nbsp;"
        code_html.append(
            f'<div class="{css}"{current}><span class="desk-check__num">{number}</span>'
            f'<span>{line_content}</span></div>'
        )

    if visible:
        var_cols = _collect_variable_columns(visible)
        body = []
        for row in visible:
            number = line_numbers.get(row["line"])
            line_cell = str(number) if number is not None else "—"
            row_vars = row.get("var_dict")
            if not row_vars and row.get("vars"):
                row_vars = parse_desk_vars(row["vars"])
            row_vars = row_vars or {}

            if var_cols:
                var_cells = "".join(
                    f'<td class="desk-check__var">{escape(str(row_vars.get(col, "—")))}</td>'
                    for col in var_cols
                )
            else:
                var_cells = f'<td class="desk-check__mono">{escape(row["vars"]) or "—"}</td>'

            array_cell = f'<td class="desk-check__mono">{escape(_format_array(row["array"]))}</td>' if show_array and row["array"] is not None else ("<td></td>" if show_array else "")
            body.append(
                f'<tr><td class="desk-check__step">{row["step"]}</td><td class="desk-check__step">{line_cell}</td>'
                f'{var_cells}{array_cell}</tr>'
            )

        if var_cols:
            var_headers = "".join(f'<th class="desk-check__var">{escape(col)}</th>' for col in var_cols)
        else:
            var_headers = '<th class="desk-check__var">Variables</th>'

        array_head = "<th>Arreglo</th>" if show_array else ""
        hidden = (rows[0]["step"] > 1) if rows else False
        note = ""
        if len(rows) > limit or hidden:
            note = f'<p class="desk-check__note">Se muestran los últimos {len(visible)} pasos' + (f" de {total_steps}" if total_steps else "") + ".</p>"
        scroll_trigger = (
            '<img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" style="display:none;" '
            'onload="var w=this.closest(\'.desk-check\')?.querySelector(\'.desk-check__table-wrap\');if(w)w.scrollTop=w.scrollHeight;" '
            'onerror="var w=this.closest(\'.desk-check\')?.querySelector(\'.desk-check__table-wrap\');if(w)w.scrollTop=w.scrollHeight;">'
        )
        trace_html = (
            f'<div class="desk-check__table-wrap"><table class="desk-check__table"><thead><tr>'
            f'<th class="desk-check__step">Paso</th><th class="desk-check__step">Línea</th>'
            f'{var_headers}{array_head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table>{scroll_trigger}</div>{note}'
        )
    else:
        trace_html = f'<div class="desk-check__empty">{escape(_INITIAL_HINT)}</div>'

    return (
        f'{_STYLES}<div class="desk-check" style="--desk-code-lines: {len(lines)};" role="region" aria-label="{DESK_TITLE}" aria-live="polite">'
        f'<div class="desk-check__code"><div class="desk-check__code-inner">{"".join(code_html)}</div></div>'
        f'<div class="desk-check__trace">{trace_html}</div></div>'
    )


__all__ = [
    "DESK_ROW_LIMIT",
    "DESK_TITLE",
    "PSEUDOCODE",
    "desk_row",
    "latex_to_text",
    "parse_desk_vars",
    "pseudocode_algorithm_key",
    "pseudocode_for",
    "render_desk_check",
    "search_desk_row",
    "sort_desk_rows",
]
