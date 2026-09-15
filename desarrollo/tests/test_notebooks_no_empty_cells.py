from __future__ import annotations

import json

from desarrollo.scripts.remove_empty_notebook_cells import is_empty_cell
from desarrollo.tests.helpers import PROJECT_ROOT


def test_no_notebook_contains_empty_cells():
    notebooks = sorted(PROJECT_ROOT.glob("simulaciones/capitulo*/notebooks/**/*.ipynb"))
    assert notebooks

    for path in notebooks:
        if {".ipynb_checkpoints", ".virtual_documents"}.intersection(path.parts):
            continue
        notebook = json.loads(path.read_text(encoding="utf-8"))
        empty_indexes = [
            index
            for index, cell in enumerate(notebook.get("cells", []))
            if is_empty_cell(cell)
        ]
        assert not empty_indexes, (path, empty_indexes)

