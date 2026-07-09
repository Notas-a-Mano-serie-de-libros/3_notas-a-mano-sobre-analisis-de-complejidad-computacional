from __future__ import annotations

from common.visual_roles import SORT_ROLE_STYLES


DEFAULT_SIZE = 10
DEFAULT_BAR_SIZE = 32
MAX_SIZE = 64
FONT_FAMILY = "Scheherazade New"
FORMULA_OUTPUT_HEIGHT = "76px"
ROLE_STYLES = SORT_ROLE_STYLES

VIEW_OPTIONS = (("Barras", "barras"), ("Cajas", "cajas"))
TREE_VIEW_OPTIONS = (("Barras", "barras"), ("Cajas", "cajas"), ("Árbol", "arbol"))
ORDER_OPTIONS = (("Ascendente", False), ("Descendente", True))
PIVOT_OPTIONS = (("Fin", "end"), ("Inicio", "start"), ("Medio", "middle"), ("Aleatorio", "random"))
PARTITION_OPTIONS = (("Hoare", "hoare"), ("Lomuto", "lomuto"))
GAP_SEQUENCE_OPTIONS = (
    ("Shell", "shell"),
    ("Hibbard", "hibbard"),
    ("Sedgewick", "sedgewick"),
    ("Pratt", "pratt"),
)
