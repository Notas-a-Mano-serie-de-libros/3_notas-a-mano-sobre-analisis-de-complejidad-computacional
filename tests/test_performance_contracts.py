from __future__ import annotations

import json
import subprocess
import sys
import unittest

from tests.helpers import PROJECT_ROOT, load_module_from_path


class TestPerformanceContracts(unittest.TestCase):
    def test_benchmark_script_runs_in_quick_mode(self):
        script = PROJECT_ROOT / "scripts" / "benchmark_animations.py"
        result = subprocess.run(
            [sys.executable, str(script), "--repeats", "1", "--json"],
            check=True,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        payload = json.loads(result.stdout)
        labels = {item["label"] for item in payload["benchmarks"]}

        self.assertEqual(payload["repeats"], 1)
        self.assertGreaterEqual(len(payload["benchmarks"]), 34)
        self.assertTrue(all(item["avg_ms"] >= 0 for item in payload["benchmarks"]))
        self.assertIn("capitulo7.ternaria.steps", labels)
        self.assertIn("capitulo7.interpolacion.render", labels)
        self.assertIn("capitulo8.mezcla.arbol.render", labels)
        self.assertIn("capitulo8.rapido.steps", labels)

    def test_clean_notebooks_check_mode_passes_on_clean_tree(self):
        script = PROJECT_ROOT / "scripts" / "clean_notebooks.py"
        result = subprocess.run(
            [sys.executable, str(script), "--check"],
            check=True,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )

        self.assertEqual(result.stdout.strip(), "")

    def test_runtime_output_cache_skips_repeated_html_assignments(self):
        runtime = load_module_from_path(
            "common_animation_runtime_test",
            PROJECT_ROOT / "common" / "animation_runtime.py",
        )

        class Widget:
            value = ""

        cache = runtime.OutputCache()
        widget = Widget()

        self.assertTrue(cache.update_html(widget, "\n  <div>uno</div>\n"))
        self.assertEqual(widget.value, "\n  <div>uno</div>\n")
        self.assertFalse(cache.update_html(widget, "\n  <div>uno</div>\n"))
        self.assertTrue(cache.update_formula(widget, r"x = 1"))
        self.assertIn("formula-renderer", widget.value)
        self.assertFalse(cache.update_formula(widget, r"x = 1"))

    def test_runtime_uses_original_synchronous_pause_for_colab(self):
        source = (PROJECT_ROOT / "common" / "animation_runtime.py").read_text(encoding="utf-8")

        self.assertIn("def pause(seconds, colab_output=None):", source)
        self.assertIn("colab_output.eval_js", source)
        self.assertIn("time.sleep(seconds)", source)
        self.assertIn("def update_formula(self, widget, formula):", source)
        self.assertIn("def render_formula_html(self, formula):", source)
        self.assertIn("class _FormulaParser:", source)
        self.assertIn("formula-frac", source)
        self.assertIn("widget.value = self.render_formula_html(formula) if formula else \"\"", source)
        self.assertNotIn('from IPython.display import Math, display', source)
        self.assertNotIn("display(Math(formula))", source)
        self.assertNotIn('widget.value = f"$${formula}$$" if formula else ""', source)
        self.assertNotIn("MathJax.typesetPromise", source)
        self.assertNotIn("async def async_pause", source)
        self.assertNotIn("def schedule", source)
        self.assertNotIn("threading", source)
        self.assertNotIn("_SCHEDULED_TASKS", source)

    def test_visual_contracts_keep_stable_dimensions_and_separated_css(self):
        search_common = (PROJECT_ROOT / "capitulo7" / "domain" / "search_common.py").read_text(encoding="utf-8")
        sort_common = (PROJECT_ROOT / "capitulo8" / "domain" / "sort_common.py").read_text(encoding="utf-8")

        self.assertIn("_SEARCH_CSS = _build_search_css()", search_common)
        self.assertIn("css_widget = widgets.HTML(_SEARCH_CSS)", search_common)
        self.assertIn("css_widget = widgets.HTML(sort_styles())", sort_common)
        self.assertIn("render_state_html(state, include_styles=False)", sort_common)
        self.assertIn("_tree_html_cache", sort_common)
        self.assertIn("_item_html_cache", sort_common)
        self.assertTrue((PROJECT_ROOT / "common" / "plot_style.py").exists())


if __name__ == "__main__":
    unittest.main()
