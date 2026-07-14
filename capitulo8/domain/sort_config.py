from __future__ import annotations

from common.visual_roles import SORT_ROLE_STYLES
from common.visual_roles import (
    SORT_ROLE_ACTIVE,
    SORT_ROLE_BOUNDARY,
    SORT_ROLE_COMPARE,
    SORT_ROLE_CURRENT,
    SORT_ROLE_DEFAULT,
    SORT_ROLE_DESCRIPTIONS,
    SORT_ROLE_EXCLUDED,
    SORT_ROLE_NAMES,
    SORT_ROLE_PIVOT,
    SORT_ROLE_SORTED,
    SORT_ROLE_SWAP,
    SORT_ROLE_WRITE,
)


DEFAULT_SIZE = 10
DEFAULT_BAR_SIZE = 32
MAX_SIZE = 64
FONT_FAMILY = "Scheherazade New"
FORMULA_OUTPUT_HEIGHT = "0px"
FORMULA_OUTPUT_PADDING = "30px 0 0 0"
ROLE_STYLES = SORT_ROLE_STYLES
ROLE_NAMES = SORT_ROLE_NAMES
ROLE_DESCRIPTIONS = SORT_ROLE_DESCRIPTIONS
ROLE_DEFAULT = SORT_ROLE_DEFAULT
ROLE_ACTIVE = SORT_ROLE_ACTIVE
ROLE_CURRENT = SORT_ROLE_CURRENT
ROLE_COMPARE = SORT_ROLE_COMPARE
ROLE_SWAP = SORT_ROLE_SWAP
ROLE_BOUNDARY = SORT_ROLE_BOUNDARY
ROLE_WRITE = SORT_ROLE_WRITE
ROLE_PIVOT = SORT_ROLE_PIVOT
ROLE_SORTED = SORT_ROLE_SORTED
ROLE_EXCLUDED = SORT_ROLE_EXCLUDED

VIEW_OPTIONS = (("Barras", "barras"), ("Cajas", "cajas"))
TREE_VIEW_OPTIONS = (("Barras", "barras"), ("Cajas", "cajas"), ("Árbol", "arbol"))
ORDER_OPTIONS = (("Ascendente", False), ("Descendente", True))
PIVOT_OPTIONS = (
    ("Fin", "end"),
    ("Inicio", "start"),
    ("Medio", "middle"),
    ("Aleatorio", "random"),
    ("Mediana de tres", "median_three"),
    ("Mediana de medianas", "median_medians"),
)
PARTITION_OPTIONS = (("Hoare", "hoare"), ("Lomuto", "lomuto"))
GAP_SEQUENCE_OPTIONS = (
    ("Shell", "shell"),
    ("Hibbard", "hibbard"),
    ("Sedgewick", "sedgewick"),
    ("Pratt", "pratt"),
)
