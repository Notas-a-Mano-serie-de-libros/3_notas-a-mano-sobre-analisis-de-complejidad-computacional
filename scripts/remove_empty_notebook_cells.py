#!/usr/bin/env python3
"""Elimina celdas completamente vacías de todos los notebooks del proyecto."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source_text(cell: dict) -> str:
    source = cell.get("source", [])
    return "".join(source) if isinstance(source, list) else str(source)


def is_empty_cell(cell: dict) -> bool:
    """Una celda con salidas o adjuntos se conserva aunque no tenga fuente."""
    return (
        not source_text(cell).strip()
        and not cell.get("outputs")
        and not cell.get("attachments")
    )


def clean_notebook(path: Path) -> int:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    cells = notebook.get("cells", [])
    retained = [cell for cell in cells if not is_empty_cell(cell)]
    removed = len(cells) - len(retained)
    if removed:
        notebook["cells"] = retained
        path.write_text(
            json.dumps(notebook, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8",
        )
    return removed


def main() -> None:
    notebooks_changed = 0
    cells_removed = 0
    for path in sorted(ROOT.glob("capitulo*/notebooks/**/*.ipynb")):
        removed = clean_notebook(path)
        if removed:
            notebooks_changed += 1
            cells_removed += removed
            print(f"{path.relative_to(ROOT)}: {removed} celda(s) eliminada(s)")
    print(
        f"Total: {cells_removed} celda(s) vacía(s) eliminada(s) "
        f"en {notebooks_changed} notebook(s)."
    )


if __name__ == "__main__":
    main()
