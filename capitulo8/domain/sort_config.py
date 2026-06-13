from __future__ import annotations


DEFAULT_SIZE = 10
DEFAULT_BAR_SIZE = 32
MAX_SIZE = 64
FONT_FAMILY = "Scheherazade New"
FORMULA_OUTPUT_HEIGHT = "76px"

ROLE_STYLES = {
    "default": ("#ffffff", "#111111", "#111111"),
    "active": ("#ffffff", "#111111", "#111111"),
    "current": ("#dae8fc", "#6c8ebf", "#111111"),
    "compare": ("#f8cecc", "#b85450", "#111111"),
    "swap": ("#dae8fc", "#6c8ebf", "#111111"),
    "boundary": ("#fff2cc", "#d6b656", "#111111"),
    "write": ("#fff2cc", "#d6b656", "#111111"),
    "pivot": ("#fff2cc", "#d6b656", "#111111"),
    "sorted": ("#e8fce9", "#97d077", "#111111"),
    "excluded": ("#f2f6f7", "#d3d9db", "#8a8f94"),
}

VIEW_OPTIONS = (("Barras", "barras"), ("Cajas", "cajas"))
TREE_VIEW_OPTIONS = (("Barras", "barras"), ("Cajas", "cajas"), ("Árbol", "arbol"))
ORDER_OPTIONS = (("Ascendente", False), ("Descendente", True))
PIVOT_OPTIONS = (("Fin", "end"), ("Inicio", "start"), ("Medio", "middle"), ("Aleatorio", "random"))
