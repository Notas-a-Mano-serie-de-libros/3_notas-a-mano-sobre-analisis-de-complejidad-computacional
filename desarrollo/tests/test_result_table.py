import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


class ResultTableTests(unittest.TestCase):
    def test_table_does_not_require_pandas(self):
        source = (ROOT / "common" / "chart_runtime.py").read_text(encoding="utf-8")
        self.assertNotIn("pandas", source.replace("sin depender de pandas", ""))

    def test_table_renders_head_and_full_html(self):
        from common.chart_runtime import make_single_table

        table = make_single_table(list(range(1, 8)), [1.0] * 7, [2] * 7, 1e-6, [0.001] * 7)
        self.assertEqual(len(table), 7)
        self.assertEqual(len(table.head(5)), 5)
        html = table.head(5)._repr_html_()
        self.assertIn('class="dataframe"', html)
        self.assertEqual(html.count("<tr>"), 6)
        self.assertIn("Operaciones obtenidas", html)


if __name__ == "__main__":
    unittest.main()
