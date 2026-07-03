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
        self.assertGreaterEqual(len(payload["benchmarks"]), 45)
        self.assertTrue(all(item["avg_ms"] >= 0 for item in payload["benchmarks"]))
        self.assertIn("capitulo7.ternaria.steps", labels)
        self.assertIn("capitulo7.ternaria.lazy_render_steps", labels)
        self.assertIn("capitulo7.interpolacion.render", labels)
        self.assertIn("capitulo8.mezcla.arbol.render", labels)
        self.assertIn("capitulo8.rapido.steps", labels)
        self.assertIn("capitulo8.rapido.lazy_render_steps", labels)

    def test_benchmark_supports_thresholds_and_json_output_file(self):
        module = load_module_from_path(
            "benchmark_animations_threshold_test",
            PROJECT_ROOT / "scripts" / "benchmark_animations.py",
        )
        payload = {
            "benchmarks": [
                {"label": "fast", "avg_ms": 1.0},
                {"label": "slow", "avg_ms": 20.0},
            ]
        }

        self.assertEqual(module.benchmark_failures(payload, max_ms=None), [])
        self.assertEqual([item["label"] for item in module.benchmark_failures(payload, max_ms=5)], ["slow"])

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

    def test_colab_validation_scripts_pass(self):
        for script_name in ("validate_colab_bootstrap.py", "validate_colab_links.py"):
            with self.subTest(script=script_name):
                result = subprocess.run(
                    [sys.executable, str(PROJECT_ROOT / "scripts" / script_name)],
                    check=True,
                    capture_output=True,
                    text=True,
                    cwd=PROJECT_ROOT,
                )

                self.assertNotEqual(result.stdout.strip(), "")

    def test_ci_workflow_has_robust_update_checks(self):
        workflow = (PROJECT_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

        self.assertIn("permissions:", workflow)
        self.assertIn("contents: read", workflow)
        self.assertIn("concurrency:", workflow)
        for job in ("notebooks-clean:", "lint-python:", "colab-sanity:", "tests:", "benchmark:", "security:"):
            self.assertIn(job, workflow)
        for version in ('"3.10"', '"3.11"', '"3.12"'):
            self.assertIn(version, workflow)
        self.assertIn("python scripts/clean_notebooks.py --check --diagnose", workflow)
        self.assertIn("ruff check capitulo7 capitulo8 common scripts tests", workflow)
        self.assertIn("python scripts/validate_colab_bootstrap.py", workflow)
        self.assertIn("python scripts/validate_colab_links.py", workflow)
        self.assertIn("python scripts/benchmark_animations.py --repeats 3 --max-ms 1500", workflow)
        self.assertIn("pip-audit --local --progress-spinner off --format json", workflow)
        self.assertIn("actions/upload-artifact@v4", workflow)

    def test_runtime_output_cache_skips_repeated_html_assignments(self):
        runtime = load_module_from_path(
            "common_animation_runtime_test",
            PROJECT_ROOT / "common" / "animation_runtime.py",
        )

        class Widget:
            value = ""
            class layout:
                min_height = ""

        cache = runtime.OutputCache()
        widget = Widget()

        self.assertTrue(cache.update_html(widget, "\n  <div>uno</div>\n"))
        self.assertEqual(widget.value, "\n  <div>uno</div>\n")
        self.assertFalse(cache.update_html(widget, "\n  <div>uno</div>\n"))
        self.assertTrue(cache.update_formula(widget, r"x = 1"))
        self.assertIn("formula-mathjax-frame", widget.value)
        self.assertIn("srcdoc=", widget.value)
        self.assertIn("tex-svg.js", widget.value)
        self.assertIn("visibility:hidden", widget.value)
        self.assertNotIn("formula-fallback", widget.value)
        self.assertIn('id=&quot;formula&quot; style=&quot;visibility:hidden&quot;', widget.value)
        self.assertIn("style.visibility = &#x27;visible&#x27;", widget.value)
        self.assertIn("previousElementSibling", widget.value)
        self.assertIn("math-ready", widget.value)
        self.assertIn("align-items:flex-end", widget.value)
        self.assertIn("justify-content:flex-start", widget.value)
        self.assertIn("text-align:left", widget.value)
        first_height = widget.layout.min_height
        tall_formula = r"x = \frac{1}{2}\\[18pt]y = \frac{3}{4}"
        self.assertTrue(cache.update_formula(widget, tall_formula, 420))
        self.assertEqual(widget.layout.min_height, "420px")
        self.assertIn("formula-frame-stack", widget.value)
        self.assertIn("visibility:hidden", widget.value)
        self.assertGreaterEqual(int(widget.layout.min_height.removesuffix("px")), int(first_height.removesuffix("px")))
        self.assertFalse(cache.update_formula(widget, tall_formula))
        html_widget = Widget()
        self.assertTrue(cache.update_outputs(widget, html_widget, r"z = 3", "<div>dos</div>", 420))
        self.assertEqual(html_widget.value, "<div>dos</div>")
        self.assertFalse(cache.update_outputs(widget, html_widget, r"z = 3", "<div>dos</div>", 420))

    def test_runtime_uses_original_synchronous_pause_for_colab(self):
        source = (PROJECT_ROOT / "common" / "animation_runtime.py").read_text(encoding="utf-8")

        self.assertIn("def pause(seconds, colab_output=None):", source)
        self.assertIn("colab_output.eval_js", source)
        self.assertIn("time.sleep(seconds)", source)
        self.assertIn("def update_formula(self, widget, formula, reserved_height=None):", source)
        self.assertIn("def update_outputs(self, formula_widget, html_widget, formula, html, reserved_height=None):", source)
        self.assertIn("def render_formula_html(self, formula, height):", source)
        self.assertIn("def render_formula_iframe(self, formula, height, hidden=False):", source)
        self.assertIn("def mathjax_srcdoc(formula):", source)
        self.assertIn("def formula_iframe_height(formula):", source)
        self.assertIn("tex-svg.js", source)
        self.assertIn("visibility:hidden", source)
        self.assertIn("formula-frame-stack", source)
        self.assertIn("previousElementSibling", source)
        self.assertNotIn("formula-fallback", source)
        self.assertIn('id="formula" style="visibility:hidden"', source)
        self.assertIn("style.visibility = 'visible'", source)
        self.assertIn("math-ready", source)
        self.assertIn("align-items:flex-end", source)
        self.assertIn("justify-content:flex-start", source)
        self.assertIn("text-align:left", source)
        self.assertIn("widget.layout.min_height", source)
        self.assertIn("self.max_formula_height", source)
        self.assertNotIn("frameElement.style.height", source)
        self.assertIn("widget.value = self.render_formula_html(formula, self.max_formula_height) if formula else \"\"", source)
        self.assertNotIn("class _FormulaParser:", source)
        self.assertNotIn("KaTeX_Main", source)
        self.assertNotIn('from IPython.display import Math, display', source)
        self.assertNotIn("display(Math(formula))", source)
        self.assertNotIn('widget.value = f"$${formula}$$" if formula else ""', source)
        self.assertNotIn("async def async_pause", source)
        self.assertNotIn("def schedule", source)
        self.assertNotIn("threading", source)
        self.assertNotIn("_SCHEDULED_TASKS", source)

    def test_formula_transition_keeps_previous_rendered_formula_visible(self):
        runtime = load_module_from_path(
            "common_animation_runtime_transition_test",
            PROJECT_ROOT / "common" / "animation_runtime.py",
        )
        cache = runtime.OutputCache()
        first = cache.render_formula_html(r"x = 1", 80)
        second = cache.render_formula_html(r"y = 2", 80)

        self.assertIn("formula-mathjax-frame", first)
        self.assertNotIn("formula-frame-stack", first)
        self.assertIn("formula-frame-stack", second)
        self.assertIn(first, second)
        self.assertIn("visibility:hidden", second)
        self.assertNotIn("formula-fallback", second)

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
