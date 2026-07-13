from __future__ import annotations


WHITE = ("#ffffff", "#111111", "#111111")
TARGET = ("#fff2cc", "#d6b656", "#111111")
BLUE = ("#dae8fc", "#6c8ebf", "#111111")
GREEN = ("#e8fce9", "#97d077", "#111111")
RED = ("#f8cecc", "#b85450", "#111111")
GRAY = ("#f2f6f7", "#d3d9db", "#8a8f94")

SEARCH_ROLE_STYLES = {
    "default": WHITE,
    "target": TARGET,
    "current": BLUE,
    "found": GREEN,
    "excluded": GRAY,
    "range": WHITE,
    "probe": RED,
}

SEARCH_RANGE_HIGHLIGHT_STYLES = {
    **SEARCH_ROLE_STYLES,
    "range": BLUE,
}

SEARCH_SEQUENTIAL_STYLES = {
    **SEARCH_ROLE_STYLES,
    "range": TARGET,
}

SEARCH_EXPONENTIAL_STYLES = {
    **SEARCH_ROLE_STYLES,
    "range": BLUE,
}

SEARCH_TERNARY_STYLES = {
    **SEARCH_ROLE_STYLES,
    "probe": BLUE,
}

SORT_ROLE_STYLES = {
    "default": WHITE,
    "active": WHITE,
    "current": BLUE,
    "compare": RED,
    "swap": BLUE,
    "boundary": TARGET,
    "write": TARGET,
    "pivot": TARGET,
    "sorted": GREEN,
    "excluded": GRAY,
}

SORT_ROLE_DEFAULT = "default"
SORT_ROLE_ACTIVE = "active"
SORT_ROLE_CURRENT = "current"
SORT_ROLE_COMPARE = "compare"
SORT_ROLE_SWAP = "swap"
SORT_ROLE_BOUNDARY = "boundary"
SORT_ROLE_WRITE = "write"
SORT_ROLE_PIVOT = "pivot"
SORT_ROLE_SORTED = "sorted"
SORT_ROLE_EXCLUDED = "excluded"

SORT_ROLE_NAMES = frozenset(SORT_ROLE_STYLES)
SORT_ROLE_DESCRIPTIONS = {
    SORT_ROLE_DEFAULT: "Elemento sin énfasis visual.",
    SORT_ROLE_ACTIVE: "Elemento dentro de una región activa sin comparación directa.",
    SORT_ROLE_CURRENT: "Elemento o índice principal del paso actual.",
    SORT_ROLE_COMPARE: "Elemento comparado contra el índice principal.",
    SORT_ROLE_SWAP: "Elemento que participa en un intercambio.",
    SORT_ROLE_BOUNDARY: "Límite, pivote calculado, hito o índice de referencia.",
    SORT_ROLE_WRITE: "Posición donde se escribe o reconstruye un valor.",
    SORT_ROLE_PIVOT: "Pivote seleccionado por quicksort.",
    SORT_ROLE_SORTED: "Elemento que ya quedó en su posición final.",
    SORT_ROLE_EXCLUDED: "Elemento fuera de la región activa.",
}


def validate_sort_roles(roles):
    unknown = sorted(set(roles) - SORT_ROLE_NAMES)
    if unknown:
        raise ValueError(f"Roles visuales de ordenamiento no registrados: {unknown}")
