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
