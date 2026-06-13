from __future__ import annotations

import sys
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch

from tests.helpers import PROJECT_ROOT, load_module_from_path


class TestChartCaching(unittest.TestCase):
    def test_search_metrics_are_available_without_chart_runtime(self):
        module = load_module_from_path(
            "capitulo7_search_metrics_test",
            PROJECT_ROOT / "capitulo7" / "domain" / "search_metrics.py",
        )

        values = [1, 3, 5, 7, 9]
        self.assertEqual(module.count_search_steps("Secuencial", values, 7), 4)
        self.assertEqual(module.count_search_steps("Binaria", values, 7), 2)
        self.assertIn("Ternaria", module.STEP_COUNTERS)

    def test_sort_metrics_are_available_without_chart_runtime(self):
        module = load_module_from_path(
            "capitulo8_sort_metrics_test",
            PROJECT_ROOT / "capitulo8" / "domain" / "sort_metrics.py",
        )

        self.assertGreater(module.count_sort_operations("burbuja", [3, 2, 1]), 0)
        self.assertGreater(module.count_sort_operations("rapido", [3, 2, 1]), 0)
        self.assertIn("radix", module.OPERATION_COUNTERS)

    def test_search_chart_caches_computed_series_by_profile(self):
        module = load_module_from_path(
            "capitulo7_busquedas_chart_test",
            PROJECT_ROOT / "capitulo7" / "domain" / "busquedas_chart.py",
        )
        source = (PROJECT_ROOT / "capitulo7" / "domain" / "busquedas_chart.py").read_text(encoding="utf-8")

        self.assertIn("from search_metrics import count_search_steps", source)
        self.assertIn("from common.plot_style import apply_plot_style", source)
        self.assertIn("apply_plot_style(matplotlib)", source)
        self.assertNotIn("def _count_binary", source)
        module._CACHE.clear()
        calls = []

        def fake_simulate(algorithms, emp_n, trials):
            calls.append((len(emp_n), trials))
            return {"Binaria": [1.0, 2.0]}

        module._simulate = fake_simulate
        module._profile = lambda fast=False: ([2, 4], [4, 8], 4, 3)
        algorithms = [("Binaria", object(), "step", {}, "#000000")]

        first = module._compute_series(algorithms)
        second = module._compute_series(algorithms)

        self.assertIs(first, second)
        self.assertEqual(calls, [(2, 3)])
        self.assertIn("an_avg", first)
        self.assertIn("theory", first)

    def test_search_chart_downloads_metrics_when_missing_next_to_runtime_file(self):
        chart_source = (PROJECT_ROOT / "capitulo7" / "domain" / "busquedas_chart.py").read_text(encoding="utf-8")
        metrics_source = (PROJECT_ROOT / "capitulo7" / "domain" / "search_metrics.py").read_text(encoding="utf-8")

        with tempfile.TemporaryDirectory() as tmpdir:
            runtime_dir = Path(tmpdir)
            chart_path = runtime_dir / "busquedas_chart.py"
            chart_path.write_text(chart_source, encoding="utf-8")

            sys.modules.pop("search_metrics", None)
            with patch("urllib.request.urlopen", lambda _url: type("Response", (), {"read": lambda self: metrics_source.encode("utf-8")})()):
                module = load_module_from_path(
                    "capitulo7_busquedas_chart_missing_metrics_test",
                    chart_path,
                )

            self.assertTrue((runtime_dir / "search_metrics.py").exists())
            self.assertEqual(module.count_search_steps("Secuencial", [1, 2, 3], 3), 3)

    def test_sort_chart_caches_computed_series_by_profile(self):
        domain_dir = PROJECT_ROOT / "capitulo8" / "domain"
        sys.path.insert(0, str(domain_dir))
        try:
            module = load_module_from_path(
                "capitulo8_ordenamientos_chart_test",
                domain_dir / "ordenamientos_chart.py",
            )
        finally:
            sys.path.remove(str(domain_dir))

        module._CACHE.clear()
        source = (domain_dir / "ordenamientos_chart.py").read_text(encoding="utf-8")

        self.assertIn("from sort_metrics import count_sort_operations", source)
        self.assertIn("from common.plot_style import apply_plot_style", source)
        self.assertIn("apply_plot_style(matplotlib)", source)
        self.assertNotIn("def _count_bubble", source)
        calls = []

        def fake_simulate(emp_n, trials):
            calls.append((len(emp_n), trials))
            return {name: [1.0, 2.0] for name, *_ in module._CONFIGS}

        module._simulate = fake_simulate
        module._profile = lambda fast=False: ([2, 4], [4, 8], 4, 3)

        first = module._compute_series()
        second = module._compute_series()

        self.assertIs(first, second)
        self.assertEqual(calls, [(2, 3)])
        self.assertIn("an_avg", first)
        self.assertIn("theory", first)

    def test_sort_chart_downloads_metrics_when_missing_next_to_runtime_file(self):
        domain_dir = PROJECT_ROOT / "capitulo8" / "domain"
        chart_source = (domain_dir / "ordenamientos_chart.py").read_text(encoding="utf-8")
        metrics_source = (domain_dir / "sort_metrics.py").read_text(encoding="utf-8")

        with tempfile.TemporaryDirectory() as tmpdir:
            runtime_dir = Path(tmpdir)
            chart_path = runtime_dir / "ordenamientos_chart.py"
            chart_path.write_text(chart_source, encoding="utf-8")
            sys.path.insert(0, str(domain_dir))
            try:
                sys.modules.pop("sort_metrics", None)
                with patch("urllib.request.urlopen", lambda _url: type("Response", (), {"read": lambda self: metrics_source.encode("utf-8")})()):
                    module = load_module_from_path(
                        "capitulo8_ordenamientos_chart_missing_metrics_test",
                        chart_path,
                    )
            finally:
                sys.path.remove(str(domain_dir))

            self.assertTrue((runtime_dir / "sort_metrics.py").exists())
            self.assertGreater(module.count_sort_operations("burbuja", [3, 2, 1]), 0)


if __name__ == "__main__":
    unittest.main()
