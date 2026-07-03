from __future__ import annotations

import json
import unittest
from pathlib import Path

from tests.helpers import PROJECT_ROOT, load_module_from_path


class TestNotebooksAreClean(unittest.TestCase):
    def test_notebooks_do_not_store_execution_outputs(self):
        notebooks = sorted(PROJECT_ROOT.rglob("*.ipynb"))

        for notebook_path in notebooks:
            if ".ipynb_checkpoints" in notebook_path.parts:
                continue

            with self.subTest(notebook=notebook_path.relative_to(PROJECT_ROOT)):
                notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
                for index, cell in enumerate(notebook.get("cells", [])):
                    if cell.get("cell_type") != "code":
                        continue
                    self.assertEqual(cell.get("outputs", []), [], f"celda {index}")
                    self.assertIsNone(cell.get("execution_count"), f"celda {index}")
                    metadata = cell.get("metadata", {})
                    self.assertNotIn("ExecuteTime", metadata, f"celda {index}")
                    self.assertNotIn("execution", metadata, f"celda {index}")

    def test_notebooks_are_protected_by_git_filter(self):
        attributes = (PROJECT_ROOT / ".gitattributes").read_text(encoding="utf-8")
        filter_script = PROJECT_ROOT / "scripts" / "clean_notebook_filter.py"

        self.assertIn("*.ipynb filter=strip-notebook-output", attributes)
        self.assertTrue(filter_script.exists())

    def test_clean_notebooks_reports_diagnostic_issues(self):
        cleaner = load_module_from_path(
            "clean_notebooks_diagnostic_test",
            PROJECT_ROOT / "scripts" / "clean_notebooks.py",
        )
        notebook = {
            "cells": [
                {"cell_type": "markdown", "source": ["texto"]},
                {
                    "cell_type": "code",
                    "metadata": {"ExecuteTime": {}, "execution": {}},
                    "outputs": [{"name": "stdout", "text": "hola"}],
                    "execution_count": 3,
                    "source": ["print('hola')"],
                },
            ]
        }

        self.assertEqual(
            cleaner.notebook_issues(notebook),
            [
                "celda 2: metadata.ExecuteTime",
                "celda 2: metadata.execution",
                "celda 2: outputs",
                "celda 2: execution_count",
            ],
        )
        self.assertTrue(cleaner.clean_notebook_data(notebook))
        cell = notebook["cells"][1]
        self.assertEqual(cell["outputs"], [])
        self.assertIsNone(cell["execution_count"])
        self.assertNotIn("ExecuteTime", cell["metadata"])
        self.assertNotIn("execution", cell["metadata"])


if __name__ == "__main__":
    unittest.main()
