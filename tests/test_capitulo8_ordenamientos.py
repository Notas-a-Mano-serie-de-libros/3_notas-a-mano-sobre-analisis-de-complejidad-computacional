from __future__ import annotations

import json
import sys
import unittest

from tests.helpers import PROJECT_ROOT, load_module_from_path


DOMAIN_DIR = PROJECT_ROOT / "capitulo8" / "domain"
NOTEBOOK_DIR = PROJECT_ROOT / "capitulo8" / "notebooks"
if str(DOMAIN_DIR) not in sys.path:
    sys.path.insert(0, str(DOMAIN_DIR))

SORT_CASES = [
    [9, 3, 7, 1, 8, 2, 6, 4],
    [5, 1, 4, 2, 8, 0, 3, 7],
    [10, 20, 5, 15, 0, 25, 30, 12],
    [6, 5, 4, 3, 2, 1, 0, 7],
]

SORT_MODULES = {
    "burbuja": ("1_ordenamiento_burbuja_app.py", "step_bubble_sort", [5, 1, 4, 2, 8]),
    "seleccion": ("2_ordenamiento_seleccion_app.py", "step_selection_sort", [64, 25, 12, 22, 11]),
    "insercion": ("3_ordenamiento_insercion_app.py", "step_insertion_sort", [5, 2, 4, 6, 1, 3]),
    "mezcla": ("4_ordenamiento_mezcla_app.py", "step_merge_sort", [38, 27, 43, 3, 9, 82, 10]),
    "rapido": ("5_ordenamiento_rapido_app.py", "step_quick_sort", [10, 7, 8, 9, 1, 5]),
    "radix": ("6_ordenamiento_radix_app.py", "step_radix_sort", [170, 45, 75, 90, 802, 24, 2, 66]),
}


class TestCapitulo8Ordenamientos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modules = {
            name: load_module_from_path(f"capitulo8_{name}", DOMAIN_DIR / path)
            for name, (path, _step, _book) in SORT_MODULES.items()
        }
        cls.common = load_module_from_path("capitulo8_sort_common", DOMAIN_DIR / "sort_common.py")
        cls.config = load_module_from_path("capitulo8_sort_config", DOMAIN_DIR / "sort_config.py")
        cls.algorithms = load_module_from_path("capitulo8_sort_algorithms", DOMAIN_DIR / "sort_algorithms.py")
        cls.launchers = load_module_from_path("capitulo8_launchers", NOTEBOOK_DIR / "launchers.py")

    def run_until_complete(self, module, step_name, state):
        step = getattr(module, step_name)
        for _ in range(5000):
            if state["sorting_complete"]:
                return
            step(state)
        raise AssertionError("El algoritmo excedió el máximo de pasos")

    def test_algorithms_sort_in_both_directions_and_views(self):
        for name, module in self.modules.items():
            step_name = SORT_MODULES[name][1]
            for values in SORT_CASES:
                for descending in (False, True):
                    for view in ("cajas", "barras"):
                        with self.subTest(name=name, values=values, descending=descending, view=view):
                            state = module.create_state(size=len(values), descending=descending, values=values, view=view)
                            self.assertEqual(state["view"], view)
                            self.run_until_complete(module, step_name, state)
                            expected = sorted(values, reverse=descending)
                            self.assertEqual(state["arr"], expected)
                            self.assertTrue(state["sorting_complete"])
                            self.assertIn("Finaliza", state["message"])

    def test_first_step_prepares_visible_work_without_finishing(self):
        for name, module in self.modules.items():
            step_name = SORT_MODULES[name][1]
            values = SORT_MODULES[name][2]
            with self.subTest(name=name):
                state = module.create_state(size=len(values), values=values, view="barras")
                initial_values = list(state["arr"])
                getattr(module, step_name)(state)

                self.assertEqual(len(state["arr"]), len(initial_values))
                self.assertEqual(state["step_index"], 1)
                self.assertFalse(state["sorting_complete"])
                self.assertTrue(state["sorting_active"])
                has_visible_work = (
                    any(role != "default" for role in state["roles"])
                    or bool(state.get("merge_tree_nodes"))
                    or bool(state.get("quick_tree_nodes"))
                )
                self.assertTrue(has_visible_work)
                self.assertNotEqual(state["message"], "Presiona Paso siguiente para iniciar.")

    def test_book_arrays_are_preserved_from_original_notebooks(self):
        for name, module in self.modules.items():
            with self.subTest(name=name):
                self.assertEqual(module.BOOK_ARRAY, SORT_MODULES[name][2])

    def test_common_generates_random_values(self):
        values = self.common.generate_values(8)

        self.assertEqual(len(values), 8)
        self.assertEqual(len(set(values)), 8)
        self.assertTrue(all(value >= 10 for value in values))

    def test_trace_events_are_copied_without_deepcopy(self):
        source = (DOMAIN_DIR / "sort_common.py").read_text(encoding="utf-8")
        event = {
            "arr": [3, 1],
            "roles": ["default", "current"],
            "labels": ["", "i"],
            "merge_tree_nodes": [{"start": 0, "end": 1, "values": [3, 1], "roles": ["default", "current"]}],
            "message": "evento",
        }

        copied = self.common.copy_event(event)
        copied["arr"][0] = 99
        copied["merge_tree_nodes"][0]["values"][0] = 99

        self.assertNotIn("deepcopy", source)
        self.assertEqual(event["arr"], [3, 1])
        self.assertEqual(event["merge_tree_nodes"][0]["values"], [3, 1])

    def test_sort_traces_are_lazy_until_first_step(self):
        source = (DOMAIN_DIR / "sort_common.py").read_text(encoding="utf-8")
        self.assertIn("class LazyTrace", source)
        self.assertIn("def next_event", source)

        state = self.common.create_state("burbuja", size=5, values=[5, 1, 4, 2, 8])
        self.assertFalse(state["trace"].materialized)
        self.assertEqual(state["message"], "Presiona Paso siguiente para iniciar el ordenamiento burbuja.")

        self.common.step_sort(state)
        self.assertTrue(state["trace"].materialized)
        self.assertEqual(state["step_index"], 1)

    def test_controls_use_dropdowns_for_view_and_order(self):
        source = (DOMAIN_DIR / "sort_common.py").read_text(encoding="utf-8")
        config_source = (DOMAIN_DIR / "sort_config.py").read_text(encoding="utf-8")

        self.assertIn("VIEW_OPTIONS", config_source)
        self.assertIn("TREE_VIEW_OPTIONS", config_source)
        self.assertIn("ORDER_OPTIONS", config_source)
        self.assertIn('description="Vista"', source)
        self.assertIn('description="Orden"', source)
        self.assertIn("widgets.Dropdown", source)
        self.assertNotIn("Orden descendente", source)
        self.assertNotIn("widgets.Checkbox", source)
        self.assertIn('description="Finalizar"', source)
        self.assertIn("def finish_without_animation", source)

    def test_buttons_keep_chapter7_color_conventions(self):
        source = (DOMAIN_DIR / "sort_common.py").read_text(encoding="utf-8")

        self.assertIn('button_style="info"', source)
        self.assertIn('button_style="success"', source)
        self.assertIn('button_style="warning"', source)
        self.assertIn('button_style="primary"', source)

    def test_default_view_is_bars_and_controls_have_tree_where_needed(self):
        source = (DOMAIN_DIR / "sort_common.py").read_text(encoding="utf-8")
        config_source = (DOMAIN_DIR / "sort_config.py").read_text(encoding="utf-8")

        self.assertIn("DEFAULT_BAR_SIZE = 32", config_source)
        self.assertIn('value="barras"', source)
        self.assertIn('value=default_size_for_view("barras")', source)
        self.assertIn("TREE_VIEW_OPTIONS if has_tree else VIEW_OPTIONS", source)
        self.assertIn('margin="10px 0 0 0"', source)
        for name, module in self.modules.items():
            with self.subTest(name=name):
                state = module.create_state(size=5, values=[5, 1, 4, 2, 8])
                self.assertEqual(state["view"], "barras")

    def test_bars_default_to_twenty_items_only_for_that_view(self):
        for name, module in self.modules.items():
            with self.subTest(name=name):
                bar_state = module.create_state()
                box_state = module.create_state(view="cajas")

                self.assertEqual(bar_state["view"], "barras")
                self.assertEqual(len(bar_state["arr"]), 32)
                self.assertEqual(len(box_state["arr"]), 10)

    def test_common_is_decoupled_from_sorting_algorithms(self):
        common_source = (DOMAIN_DIR / "sort_common.py").read_text(encoding="utf-8")
        algorithms_source = (DOMAIN_DIR / "sort_algorithms.py").read_text(encoding="utf-8")
        tree_source = (DOMAIN_DIR / "sort_tree.py").read_text(encoding="utf-8")

        self.assertIn("from sort_algorithms import TRACE_BUILDERS", common_source)
        self.assertIn("from sort_tree import", common_source)
        self.assertIn("def bubble_trace", algorithms_source)
        self.assertIn("def quick_trace", algorithms_source)
        self.assertIn("def quick_tree", tree_source)
        self.assertIn('"common/animation_runtime.py"', (NOTEBOOK_DIR / "colab_bootstrap.py").read_text(encoding="utf-8"))
        self.assertIn('"capitulo8/domain/sort_tree.py"', (NOTEBOOK_DIR / "colab_bootstrap.py").read_text(encoding="utf-8"))
        self.assertIn("project_root", (NOTEBOOK_DIR / "colab_bootstrap.py").read_text(encoding="utf-8"))
        self.assertNotIn("def bubble_trace", common_source)
        self.assertNotIn("def quick_trace", common_source)
        self.assertNotIn("def quick_tree", common_source)
        self.assertNotIn('"bubble_trace"', self.common.__all__)
        self.assertIn("copy_event", self.common.__all__)

    def test_equations_are_rendered_above_animation(self):
        source = (DOMAIN_DIR / "sort_common.py").read_text(encoding="utf-8")

        self.assertIn("formula_output", source)
        self.assertIn("from common.animation_runtime import OutputCache, pause, set_disabled", source)
        self.assertIn("render_cache = OutputCache()", source)
        self.assertIn('formula = state["formula"]', source)
        self.assertIn("formula_output = widgets.HTML", source)
        self.assertNotIn("widgets.HTMLMath", source)
        self.assertIn("render_cache.update_formula(formula_output, formula)", source)
        self.assertIn("render_cache.update_html(html_output, render_state_html(state, include_styles=False))", source)
        self.assertNotIn("async def run_async", source)
        self.assertNotIn("schedule(", source)
        self.assertIn('controls["auto"].on_click(run_auto)', source)
        self.assertIn("colab_output.enable_custom_widget_manager()", source)
        self.assertNotIn("AUTO_RENDER_EVERY", source)
        self.assertIn('FORMULA_OUTPUT_HEIGHT = "76px"', (DOMAIN_DIR / "sort_config.py").read_text(encoding="utf-8"))
        self.assertIn("min_height=FORMULA_OUTPUT_HEIGHT", source)
        self.assertIn("css_widget = widgets.HTML(sort_styles())", source)
        self.assertIn("render_state_html(state, include_styles=False)", source)
        self.assertIn("widgets.VBox([controls_layout, formula_output, css_widget, html_output]", source)
        for module in self.modules.values():
            state = module.create_state(size=5, values=[5, 1, 4, 2, 8])
            getattr(module, SORT_MODULES[state["algorithm"]][1])(state)
            self.assertTrue(state["formula"])
            self.assertIn("=", state["formula"])

    def test_render_supports_boxes_and_bars_without_order_label(self):
        module = self.modules["burbuja"]
        box_state = module.create_state(size=5, values=[5, 1, 4, 2, 8], view="cajas")
        bar_state = module.create_state(size=5, values=[5, 1, 4, 2, 8], view="barras")

        box_html = module.render_state_html(box_state)
        bar_html = module.render_state_html(bar_state)

        self.assertIn("sort-items boxes", box_html)
        self.assertIn("sort-app-bars", bar_html)
        self.assertIn("bar-panel", bar_html)
        self.assertIn("bar-nodes", bar_html)
        self.assertIn("min-height:", bar_html)
        self.assertNotIn("Tipo de orden", box_html)
        self.assertNotIn("Tipo de orden", bar_html)

    def test_merge_and_quick_render_tree_view(self):
        merge = self.modules["mezcla"].create_state(size=7, values=[38, 27, 43, 3, 9, 82, 10], view="arbol")
        quick = self.modules["rapido"].create_state(size=6, values=[10, 7, 8, 9, 1, 5], view="arbol")

        merge_html = self.modules["mezcla"].render_state_html(merge)
        quick_html = self.modules["rapido"].render_state_html(quick)

        self.assertIn("merge-tree-shell", merge_html)
        self.assertIn("merge-row-tree", merge_html)
        self.assertIn("[0, 6]", merge_html)
        self.assertIn("quick-tree-shell", quick_html)
        self.assertIn("quick-row", quick_html)
        self.assertIn("[0, 5]", quick_html)

    def test_merge_tree_view_follows_active_division_path(self):
        module = self.modules["mezcla"]
        state = module.create_state(size=8, values=[95, 131, 111, 57, 158, 16, 25, 98], view="arbol")

        module.step_merge_sort(state)
        module.step_merge_sort(state)
        first_html = module.render_state_html(state)
        self.assertIn("[0, 7]", first_html)
        self.assertIn("[0, 3]", first_html)
        self.assertIn("[4, 7]", first_html)
        self.assertNotIn("[0, 1]", first_html)
        self.assertIn("#dae8fc", first_html)

        module.step_merge_sort(state)
        second_html = module.render_state_html(state)
        self.assertIn("[0, 1]", second_html)
        self.assertIn("[2, 3]", second_html)
        self.assertIn("#f2f6f7", second_html)
        self.assertIn("#dae8fc", second_html)

    def test_merge_tree_preserves_base_merge_and_hide_behavior(self):
        module = self.modules["mezcla"]
        state = module.create_state(size=8, values=[95, 131, 111, 57, 158, 16, 25, 98], view="arbol")

        for _ in range(5):
            module.step_merge_sort(state)
        base_html = module.render_state_html(state)
        self.assertIn("[0, 0]", base_html)
        self.assertIn("#e8fce9", base_html)

        module.step_merge_sort(state)
        module.step_merge_sort(state)
        empty_merge_html = module.render_state_html(state)
        self.assertIn("[0, 1]", empty_merge_html)
        self.assertIn("#fff2cc", empty_merge_html)

        module.step_merge_sort(state)
        compare_html = module.render_state_html(state)
        self.assertIn("#dae8fc", compare_html)
        self.assertIn("#f8cecc", compare_html)

        module.step_merge_sort(state)
        module.step_merge_sort(state)
        sorted_parent_html = module.render_state_html(state)
        self.assertIn("[0, 1]", sorted_parent_html)
        self.assertNotIn("[0, 0]", sorted_parent_html)
        self.assertNotIn("[1, 1]", sorted_parent_html)
        self.assertIn("#e8fce9", sorted_parent_html)

    def test_merge_tree_does_not_update_parent_when_child_finishes(self):
        trace = self.algorithms.merge_trace([95, 131, 111, 57, 158, 16, 25, 98])
        event = trace[17]
        nodes = {(node["start"], node["end"]): node for node in event["merge_tree_nodes"]}

        self.assertEqual(nodes[(2, 3)]["values"], [57, 111])
        self.assertEqual(nodes[(0, 3)]["values"], [95, 131, 111, 57])

    def test_simulation_height_is_stable_across_merge_tree_steps(self):
        module = self.modules["mezcla"]
        state = module.create_state(size=8, values=[95, 131, 111, 57, 158, 16, 25, 98], view="arbol")
        initial_height = self.common.simulation_min_height(state)

        for _ in range(12):
            module.step_merge_sort(state)
            self.assertEqual(self.common.simulation_min_height(state), initial_height)
            self.assertIn(f"min-height:{initial_height}px", module.render_state_html(state))

    def test_simulation_height_is_cached_by_view_algorithm_and_size(self):
        module = self.modules["mezcla"]
        state = module.create_state(size=8, values=[95, 131, 111, 57, 158, 16, 25, 98], view="arbol")
        self.common._SIMULATION_HEIGHT_CACHE.clear()

        first = self.common.simulation_min_height(state)
        second = self.common.simulation_min_height(state)

        self.assertEqual(first, second)
        self.assertIn(("arbol", "mezcla", 8), self.common._SIMULATION_HEIGHT_CACHE)

    def test_sort_item_html_is_cached_per_state(self):
        module = self.modules["burbuja"]
        state = module.create_state(size=8, values=[8, 7, 6, 5, 4, 3, 2, 1], view="barras")

        first = module.render_state_html(state)
        second = module.render_state_html(state)

        self.assertEqual(first, second)
        self.assertIn("_item_html_cache", state)

    def test_sort_tree_html_is_cached_per_state(self):
        module = self.modules["mezcla"]
        state = module.create_state(size=8, values=[95, 131, 111, 57, 158, 16, 25, 98], view="arbol")

        module.step_merge_sort(state)
        first = module.render_state_html(state)
        cache_size = len(state.get("_tree_html_cache", {}))
        second = module.render_state_html(state)

        self.assertEqual(first, second)
        self.assertIn("_tree_html_cache", state)
        self.assertGreater(cache_size, 0)
        self.assertEqual(cache_size, len(state["_tree_html_cache"]))

    def test_quick_tree_uses_snapshots_and_stable_height(self):
        module = self.modules["rapido"]
        state = module.create_state(size=6, values=[10, 7, 8, 9, 1, 5], view="arbol")
        initial_height = self.common.simulation_min_height(state)

        for _ in range(8):
            module.step_quick_sort(state)
            self.assertIn("quick_tree_nodes", state)
            self.assertEqual(self.common.simulation_min_height(state), initial_height)
            self.assertIn(f"min-height:{initial_height}px", module.render_state_html(state))

        self.assertTrue(any(role == "pivot" for role in state["roles"]))
        self.assertIn("quick-tree-shell", module.render_state_html(state))

    def test_quick_tree_reveals_partition_children(self):
        trace = self.algorithms.quick_trace([10, 7, 8, 9, 1, 5])
        event = next(item for item in trace if len(item.get("quick_tree_nodes", [])) > 1)
        ranges = {(node["start"], node["end"]) for node in event["quick_tree_nodes"]}

        self.assertIn((0, 5), ranges)
        self.assertTrue(any(start > 0 or end < 5 for start, end in ranges))

    def test_bar_view_preserves_original_visual_style(self):
        module = self.modules["seleccion"]
        state = module.create_state(size=5, values=[64, 25, 12, 22, 11], view="barras")
        html = module.render_state_html(state)

        self.assertIn("background: #000000", html)
        self.assertIn("border-radius: 0;", html)
        self.assertIn('<div class="bar-value">64</div>', html)
        self.assertIn('<div class="bar-index">0</div>', html)
        first_bar = html.index('<div class="bar-wrap"')
        value_position = html.index("bar-value", first_bar)
        bar_position = html.index('<div class="bar"', value_position + 1)
        index_position = html.index("bar-index", bar_position)
        self.assertLess(value_position, bar_position)
        self.assertLess(bar_position, index_position)

    def test_bar_view_keeps_yellow_highlight_roles(self):
        highlighted_modules = 0
        for name, module in self.modules.items():
            with self.subTest(name=name):
                state = module.create_state(size=5, values=[5, 1, 4, 2, 8], view="barras")
                yellow_event = next((
                    event for event in state["trace"]
                    if any(role in {"boundary", "write", "pivot"} for role in event["roles"])
                ), None)
                if yellow_event is None:
                    continue
                highlighted_modules += 1
                state.update(yellow_event)
                html = module.render_state_html(state)
                self.assertIn("#fff2cc", html)
        self.assertGreater(highlighted_modules, 0)

    def test_bubble_marks_pass_limit_i_as_yellow_boundary(self):
        module = self.modules["burbuja"]
        state = module.create_state(size=5, values=[5, 1, 4, 2, 8], view="barras")
        module.step_bubble_sort(state)

        self.assertEqual(state["roles"][4], "boundary")
        self.assertEqual(state["labels"][4], "i")
        self.assertEqual(state["roles"][0], "current")
        self.assertEqual(state["roles"][1], "compare")
        self.assertEqual(state["labels"][0], "j")
        self.assertEqual(state["labels"][1], "j + 1")
        html = module.render_state_html(state)
        self.assertIn("#fff2cc", html)

    def test_selection_uses_original_candidate_labels_and_yellow_boundary(self):
        module = self.modules["seleccion"]
        ascending = module.create_state(size=5, values=[64, 25, 12, 22, 11], view="barras")
        descending = module.create_state(size=5, descending=True, values=[64, 25, 12, 22, 11], view="barras")

        module.step_selection_sort(ascending)
        module.step_selection_sort(descending)

        self.assertEqual(ascending["roles"][4], "boundary")
        self.assertEqual(ascending["labels"][4], "i")
        self.assertEqual(ascending["roles"][0], "current")
        self.assertEqual(ascending["labels"][0], "máximo")
        self.assertIn(r"\text{máximo}", ascending["formula"])

        self.assertEqual(descending["roles"][4], "boundary")
        self.assertEqual(descending["labels"][4], "i")
        self.assertEqual(descending["roles"][0], "current")
        self.assertEqual(descending["labels"][0], "mínimo")
        self.assertIn(r"\text{mínimo}", descending["formula"])

    def test_insertion_moves_red_marker_without_yellow_bars(self):
        module = self.modules["insercion"]
        state = module.create_state(size=3, values=[5, 2, 4], view="barras")

        for event in state["trace"]:
            self.assertFalse(any(role in {"boundary", "write", "pivot"} for role in event["roles"]))

        module.step_insertion_sort(state)
        module.step_insertion_sort(state)
        self.assertEqual(state["roles"][1], "compare")
        self.assertEqual(state["labels"][1], "i")

        module.step_insertion_sort(state)
        self.assertEqual(state["roles"][0], "current")
        self.assertEqual(state["roles"][1], "compare")

        module.step_insertion_sort(state)
        self.assertEqual(state["arr"], [2, 5, 4])
        self.assertEqual(state["roles"][0], "compare")
        self.assertEqual(state["labels"][0], "i")
        self.assertEqual(state["roles"][1], "current")
        self.assertNotIn("#fff2cc", module.render_state_html(state))

    def test_every_trace_step_can_render(self):
        for name, module in self.modules.items():
            views = ("cajas", "barras", "arbol") if name in {"mezcla", "rapido"} else ("cajas", "barras")
            for view in views:
                with self.subTest(name=name, view=view):
                    state = module.create_state(size=5, values=[5, 1, 4, 2, 8], view=view)
                    for event in state["trace"]:
                        state.update(event)
                        html = module.render_state_html(state)
                        self.assertIn("sort-app", html)

    def test_launchers_load_all_modules(self):
        expected = {
            "run_comparacion": "0_comparacion_ordenamientos_app.py",
            "run_burbuja": "1_ordenamiento_burbuja_app.py",
            "run_seleccion": "2_ordenamiento_seleccion_app.py",
            "run_insercion": "3_ordenamiento_insercion_app.py",
            "run_mezcla": "4_ordenamiento_mezcla_app.py",
            "run_rapido": "5_ordenamiento_rapido_app.py",
            "run_radix": "6_ordenamiento_radix_app.py",
        }
        for launcher_name, relative_path in expected.items():
            with self.subTest(launcher_name=launcher_name):
                self.assertTrue(hasattr(self.launchers, launcher_name))
                module = self.launchers._load_module(relative_path, f"test_{launcher_name}")
                self.assertTrue(hasattr(module, "run_app"))

    def test_radix_notebook_is_individual_only(self):
        notebook = NOTEBOOK_DIR / "6_ordenamiento_radix.ipynb"
        nb = json.loads(notebook.read_text(encoding="utf-8"))
        code_cells = [cell for cell in nb["cells"] if cell["cell_type"] == "code"]
        bootstrap = (NOTEBOOK_DIR / "colab_bootstrap.py").read_text(encoding="utf-8")
        launchers = (NOTEBOOK_DIR / "launchers.py").read_text(encoding="utf-8")
        comparison = (NOTEBOOK_DIR / "0_comparacion_ordenamientos.ipynb").read_text(encoding="utf-8")
        chart_source = (DOMAIN_DIR / "ordenamientos_chart.py").read_text(encoding="utf-8")

        self.assertEqual(len(code_cells), 2)
        self.assertIn('SIMULATION_NAME = "radix"', "".join(code_cells[0]["source"]))
        self.assertIn('run_single_chart("Radix")', "".join(code_cells[1]["source"]))
        for cell in code_cells:
            self.assertEqual(cell.get("outputs"), [])
            self.assertIsNone(cell.get("execution_count"))
            self.assertTrue(cell["metadata"]["jupyter"]["source_hidden"])

        self.assertIn("6_ordenamiento_radix_app.py", bootstrap)
        self.assertIn('"radix": "run_radix"', bootstrap)
        self.assertIn("def run_radix", launchers)
        self.assertNotIn("Ordenamiento radix", comparison)
        self.assertIn('("Radix", "radix"', chart_source)
        self.assertNotIn('("Radix", "radix"', chart_source.split("_SINGLE_CONFIGS", 1)[0])

    def test_notebooks_are_clean_invocations(self):
        comparison_notebook = NOTEBOOK_DIR / "0_comparacion_ordenamientos.ipynb"
        comparison_nb = json.loads(comparison_notebook.read_text(encoding="utf-8"))
        comparison_source = "".join(comparison_nb["cells"][1]["source"])
        self.assertIn('SIMULATION_NAME = "comparacion"', comparison_source)
        self.assertEqual(comparison_nb["cells"][1]["outputs"], [])
        self.assertIsNone(comparison_nb["cells"][1]["execution_count"])
        self.assertTrue(comparison_nb["cells"][1]["metadata"]["jupyter"]["source_hidden"])

        for index, name in enumerate(("burbuja", "seleccion", "insercion", "mezcla", "rapido"), start=1):
            with self.subTest(name=name):
                notebook = NOTEBOOK_DIR / f"{index}_ordenamiento_{name}.ipynb"
                nb = json.loads(notebook.read_text(encoding="utf-8"))
                source = "".join(nb["cells"][1]["source"])
                self.assertIn(f'SIMULATION_NAME = "{name}"', source)
                self.assertEqual(nb["cells"][1]["outputs"], [])
                self.assertIsNone(nb["cells"][1]["execution_count"])
                self.assertTrue(nb["cells"][1]["metadata"]["jupyter"]["source_hidden"])

    def test_comparison_bootstrap_and_render_bars(self):
        bootstrap = (NOTEBOOK_DIR / "colab_bootstrap.py").read_text(encoding="utf-8")
        module = self.launchers._load_module(
            "0_comparacion_ordenamientos_app.py",
            "capitulo8_comparacion_test_app",
        )
        source = (DOMAIN_DIR / "0_comparacion_ordenamientos_app.py").read_text(encoding="utf-8")
        notebook_source = (NOTEBOOK_DIR / "0_comparacion_ordenamientos.ipynb").read_text(encoding="utf-8")
        values = [5, 1, 4, 2, 8, 3]
        state = module.create_comparison_state(size=len(values), values=values)

        self.assertIn("0_comparacion_ordenamientos_app.py", bootstrap)
        self.assertIn('"comparacion": "run_comparacion"', bootstrap)
        self.assertIn('description="Ordenar"', source)
        self.assertIn('description="Finalizar"', source)
        self.assertIn("disabled=True", source)
        self.assertIn("def set_running_buttons", source)
        self.assertIn("finish_button.disabled = False", source)
        self.assertIn("finish_button.disabled = True", source)
        self.assertIn('execution_state["finish_requested"] = True', source)
        self.assertIn("def finish_comparison", source)
        self.assertIn("while not all_sorts_complete(state):", source)
        self.assertNotIn('description="Buscar"', source)
        self.assertNotIn("AUTO_RENDER_EVERY", source)
        self.assertNotIn("Complejidad temporal", notebook_source)
        self.assertNotIn("Complejidad espacial", notebook_source)
        self.assertEqual(notebook_source.count("Mejor caso"), 1)
        self.assertEqual(notebook_source.count("Caso promedio"), 1)
        self.assertEqual(notebook_source.count("Peor caso"), 1)
        self.assertNotIn('description="Paso siguiente"', source)
        self.assertNotIn('description="Ejecución automática"', source)
        self.assertEqual(len(state["algorithms"]), 5)
        for item in state["algorithms"]:
            self.assertEqual(item["state"]["initial_values"], values)
            self.assertEqual(item["state"]["view"], "barras")

        module.step_all_sorts(state)
        self.assertTrue(all(item["steps"] == 1 for item in state["algorithms"]))
        html = module.render_comparison_html(state)

        self.assertIn("Algoritmo", html)
        self.assertIn("Pasos", html)
        self.assertIn("Arreglo", html)
        self.assertIn("background: #000000;", html)
        self.assertIn("overflow-x: hidden;", html)
        self.assertIn("gap: 0;", source)
        self.assertIn("padding-bottom: 0;", source)
        self.assertIn("body_output = widgets.HTML", source)
        self.assertIn("render_comparison_body_html(state)", source)
        self.assertIn("render_comparison_rows_html(state)", source)
        self.assertNotIn("header_output = widgets.HTML", source)
        self.assertNotIn("rows_output = widgets.HTML", source)
        self.assertNotIn("row_outputs = []", source)
        self.assertIn("Ordenamiento<br>burbuja", html)
        self.assertIn("font-weight: 700;", html)
        self.assertEqual(html.count('<div class="comparison-index">'), len(values))
        self.assertNotIn("Generar arreglo del libro", (DOMAIN_DIR / "0_comparacion_ordenamientos_app.py").read_text(encoding="utf-8"))

        self.assertIn('value="Algoritmos activos"', source)
        self.assertIn("widgets.Checkbox", source)
        self.assertIn("widgets.GridBox", source)
        self.assertIn("ALGORITHM_COLUMN_WIDTHS = (118, 138, 122)", source)
        self.assertIn("ALGORITHM_GROUP_GAP = 2", source)
        self.assertIn("ALGORITHM_FIELD_WIDTH = sum(ALGORITHM_COLUMN_WIDTHS)", source)
        self.assertIn('grid_template_columns=" ".join', source)
        self.assertIn("overflow=\"visible\"", source)
        self.assertIn('margin="0 0 0 32px"', source)
        self.assertIn('border="1px solid #767676"', source)
        self.assertIn('background_color="#ffffff"', source)
        self.assertIn("algorithms_group", source)
        self.assertNotIn("widgets.Accordion", source)
        self.assertNotIn("widgets.SelectMultiple", source)

    def test_comparison_can_filter_visible_algorithms(self):
        module = self.launchers._load_module(
            "0_comparacion_ordenamientos_app.py",
            "capitulo8_comparacion_filter_test_app",
        )
        state = module.create_comparison_state(
            size=5,
            values=[5, 1, 4, 2, 8],
            selected_algorithms=("burbuja", "rapido"),
        )
        html = module.render_comparison_html(state)

        self.assertEqual([item["key"] for item in state["algorithms"]], ["rapido", "burbuja"])
        self.assertIn("Ordenamiento<br>burbuja", html)
        self.assertIn("Ordenamiento<br>rápido", html)
        self.assertNotIn("Ordenamiento<br>selección", html)

    def test_comparison_reads_selected_checkboxes(self):
        module = self.launchers._load_module(
            "0_comparacion_ordenamientos_app.py",
            "capitulo8_comparacion_checkbox_test_app",
        )

        class Check:
            def __init__(self, value):
                self.value = value

        selected = module.selected_from_checks({
            "burbuja": Check(True),
            "seleccion": Check(False),
            "rapido": Check(True),
        })

        self.assertEqual(selected, ("burbuja", "rapido"))


class TestCapitulo8IndividualNotebooks(unittest.TestCase):
    def test_individual_notebooks_keep_only_minimal_invocation_code(self):
        expected = {
            "1_ordenamiento_burbuja.ipynb": "burbuja",
            "2_ordenamiento_seleccion.ipynb": "seleccion",
            "3_ordenamiento_insercion.ipynb": "insercion",
            "4_ordenamiento_mezcla.ipynb": "mezcla",
            "5_ordenamiento_rapido.ipynb": "rapido",
        }

        chart_names = {
            "1_ordenamiento_burbuja.ipynb": "Burbuja",
            "2_ordenamiento_seleccion.ipynb": "Selección",
            "3_ordenamiento_insercion.ipynb": "Inserción",
            "4_ordenamiento_mezcla.ipynb": "Mezcla",
            "5_ordenamiento_rapido.ipynb": "Rápido",
        }

        for notebook_name, simulation_name in expected.items():
            with self.subTest(notebook=notebook_name):
                notebook = json.loads((NOTEBOOK_DIR / notebook_name).read_text())
                code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
                self.assertEqual(len(code_cells), 2)

                # Cell 0: simulation bootstrap
                source = "".join(code_cells[0]["source"])
                code_lines = [line for line in source.splitlines() if line.strip()]
                self.assertLessEqual(len(code_lines), 17)
                self.assertIn(f'SIMULATION_NAME = "{simulation_name}"', source)
                self.assertIn("BOOTSTRAP_CANDIDATES = (", source)
                self.assertIn("bootstrap_code = (", source)
                self.assertIn("colab_bootstrap.py", source)
                self.assertIn("exec(", source)
                self.assertNotIn("def ", source)
                self.assertNotIn("step_", source)
                self.assertNotIn("create_state", source)
                self.assertEqual(code_cells[0].get("outputs"), [])
                self.assertIsNone(code_cells[0].get("execution_count"))

                # Cell 1: run_single_chart invocation
                chart_source = "".join(code_cells[1]["source"])
                self.assertIn("run_single_chart", chart_source)
                self.assertIn("ordenamientos_chart", chart_source)
                self.assertNotIn("from ordenamientos_chart import", chart_source)
                self.assertIn("sort_metrics.py", chart_source)
                self.assertIn(f'run_single_chart("{chart_names[notebook_name]}")', chart_source)
                self.assertEqual(code_cells[1].get("outputs"), [])
                self.assertIsNone(code_cells[1].get("execution_count"))


if __name__ == "__main__":
    unittest.main()
