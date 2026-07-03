from __future__ import annotations

import json
import unittest
from pathlib import Path

from tests.helpers import PROJECT_ROOT


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


if __name__ == "__main__":
    unittest.main()
