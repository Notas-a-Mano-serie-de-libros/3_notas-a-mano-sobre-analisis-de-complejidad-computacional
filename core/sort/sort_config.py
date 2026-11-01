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
SORT_THEME_CSS = """
      :root {
        --sort-bg: #ffffff;
        --sort-panel-bg: #f7f7f7;
        --sort-text: #111827;
        --sort-text-secondary: #4b5563;
        --sort-border: #9ca3af;
        --sort-border-strong: #6b7280;
        --sort-grid: #e5e7eb;
        --sort-focus: #2563eb;
        --sort-focus-bg: #eff6ff;
        --sort-muted-opacity: 0.42;
        --sort-title-size: 19px;
        --sort-message-size: 22px;
        --sort-value-size: 16px;
        --sort-index-size: 16px;
      }
      .sort-comparison-legend {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        gap: 8px 14px;
        width: 100%;
        max-width: none;
        min-height: 34px;
        margin: 0 0 24px;
        padding: 7px 10px;
        border: 1px solid var(--sort-grid);
        border-top: 0;
        border-radius: 0;
        background: #f9fafb;
        color: var(--sort-text);
        font-size: 15px;
        line-height: 18px;
      }
      .sort-comparison-legend-item {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        white-space: nowrap;
      }
      .sort-comparison-legend-swatch {
        width: 14px;
        height: 14px;
        border: 1px solid var(--sort-border);
        box-sizing: border-box;
      }
      .variant-app > .sort-comparison-legend,
      .insertion-comparison-table > .sort-comparison-legend,
      .shell-comparison-table > .sort-comparison-legend {
        margin: 0 -14px 24px;
        width: calc(100% + 28px);
        border-left: 0;
        border-right: 0;
        border-radius: 0;
      }
"""
FORMULA_OUTPUT_HEIGHT = "0px"
FORMULA_OUTPUT_PADDING = "30px 12px 12px 12px"
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
RADIX_DATA_TYPE_OPTIONS = (
    ("Número", "numero"),
    ("Carácter", "caracter"),
    ("Cadena de caracteres", "cadena"),
    ("Fecha", "fecha"),
)
RADIX_NUMBER_MODE_OPTIONS = (
    ("Positivos", "positive"),
    ("Negativos", "negative"),
    ("Mixto", "mixed"),
    ("Punto flotante", "float"),
)
RADIX_BASE_OPTIONS = (
    ("Binario (2)", 2),
    ("Octal (8)", 8),
    ("Decimal (10)", 10),
    ("Hexadecimal (16)", 16),
)
