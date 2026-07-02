from __future__ import annotations

import json
import unittest

from tests.helpers import PROJECT_ROOT, load_module_from_path


LAUNCHERS_PATH = PROJECT_ROOT / "capitulo7" / "notebooks" / "launchers.py"
LOCAL_APP_PATH = PROJECT_ROOT / "capitulo7" / "abrir_busqueda.py"

SEARCH_CASES = [
    ([3, 8, 12, 20, 31, 44, 55, 68], 20, True),
    ([3, 8, 12, 20, 31, 44, 55, 68], 21, False),
    ([0, 4, 7, 15, 19, 23, 42, 77], 0, True),
    ([0, 4, 7, 15, 19, 23, 42, 77], 99, False),
    ([2, 5, 9, 14, 18, 27, 33, 40], 40, True),
    ([2, 5, 9, 14, 18, 27, 33, 40], -1, False),
    ([1, 6, 11, 16, 21, 26, 31, 36], 26, True),
    ([1, 6, 11, 16, 21, 26, 31, 36], 17, False),
    ([10, 20, 30, 40, 50, 60, 70, 80], 70, True),
    ([10, 20, 30, 40, 50, 60, 70, 80], 35, False),
]

SEARCH_MODULES = {
    "secuencial": ("1_busqueda_secuencial_app.py", "step_linear_search", "run_secuencial"),
    "binaria": ("2_busqueda_binaria_app.py", "step_binary_search", "run_binaria"),
    "interpolacion": ("3_busqueda_interpolacion_app.py", "step_interpolation_search", "run_interpolacion"),
    "saltos": ("4_busqueda_saltos_app.py", "step_jump_search", "run_saltos"),
}


class TestCapitulo7BusquedaTernaria(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.launchers = load_module_from_path("capitulo7_launchers", LAUNCHERS_PATH)
        cls.module = cls.launchers._load_module(
            "6_busqueda_ternaria_app.py",
            "capitulo7_ternaria_test_app",
        )

    def test_launchers_load_ternary_module(self):
        self.assertTrue(hasattr(self.module, "run_app"))
        self.assertTrue(hasattr(self.module, "create_state"))
        self.assertTrue(hasattr(self.module, "step_ternary_search"))
        self.assertTrue(hasattr(self.module, "build_formula"))
        self.assertEqual(self.module.BOOK_ARRAY, [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(self.module.BOOK_TARGET, 8)

    def test_local_launcher_forces_fresh_module_load(self):
        source = LAUNCHERS_PATH.read_text(encoding="utf-8")

        self.assertIn("importlib.invalidate_caches()", source)
        self.assertIn("module_path.stat().st_mtime_ns", source)
        self.assertIn('sys.modules.pop("search_common", None)', source)

    def test_bootstrap_clears_previous_widget_output(self):
        source = (PROJECT_ROOT / "capitulo7" / "notebooks" / "colab_bootstrap.py").read_text(encoding="utf-8")

        self.assertIn("clear_output(wait=False)", source)
        self.assertIn("clear_output(wait=True)", source)

    def test_bootstrap_resolves_only_chapter7_launcher(self):
        source = (PROJECT_ROOT / "capitulo7" / "notebooks" / "colab_bootstrap.py").read_text(encoding="utf-8")

        self.assertIn('"capitulo7" / "notebooks" / "launchers.py"', source)
        self.assertIn("No se pudo localizar capitulo7/notebooks/launchers.py", source)
        self.assertIn("project_root", source)
        self.assertIn("launcher_path.parent.parent.parent.resolve()", source)
        self.assertNotIn('base / "notebooks"', source)

    def test_original_visual_convention_after_select_step(self):
        state = self.module.create_state(size=8, target=8, values=[1, 2, 3, 4, 5, 6, 7, 8])
        self.module.step_ternary_search(state)

        self.assertEqual(self.module.ROLE_STYLES["target"], ("#fff2cc", "#d6b656", "#111111"))
        self.assertEqual(self.module.ROLE_STYLES["range"], ("#ffffff", "#111111", "#111111"))
        self.assertEqual(self.module.ROLE_STYLES["probe"], ("#dae8fc", "#6c8ebf", "#111111"))
        self.assertEqual(state["arr"][state["a"]]["role"], "default")
        self.assertEqual(state["arr"][state["b"]]["role"], "default")
        self.assertEqual(state["arr"][state["m1"]]["role"], "current")
        self.assertEqual(state["arr"][state["m2"]]["role"], "current")

    def test_existing_target_starts_highlighted(self):
        state = self.module.create_state(size=8, target=6, values=[1, 2, 3, 4, 5, 6, 7, 8])
        missing_state = self.module.create_state(size=8, target=9, values=[1, 2, 3, 4, 5, 6, 7, 8])
        html = self.module.render_state_html(state)

        self.assertEqual(state["arr"][5]["role"], "target")
        self.assertTrue(state["arr"][5]["is_target"])
        self.assertNotIn("target", [node["role"] for node in missing_state["arr"]])
        self.assertIn("background:#fff2cc", html)
        state["arr"][5]["role"] = "current"
        self.assertIn("background:#dae8fc", self.module.render_state_html(state))
        state["arr"][5]["role"] = "found"
        self.assertIn("background:#e8fce9", self.module.render_state_html(state))

    def test_original_ui_features_are_present(self):
        source = (PROJECT_ROOT / "capitulo7" / "domain" / "6_busqueda_ternaria_app.py").read_text()
        common_source = (PROJECT_ROOT / "capitulo7" / "domain" / "search_common.py").read_text()
        self.assertIn('description="Generar arreglo del libro"', common_source)
        self.assertIn('description="Elemento"', common_source)
        self.assertIn('description="Posición"', common_source)
        self.assertIn('description="Objetivo"', common_source)
        self.assertIn("target_readout = widgets.BoundedIntText", common_source)
        self.assertIn("disabled=True", common_source)
        self.assertIn('controls.append(target_readout)', common_source)
        self.assertIn("def update_target_readout", common_source)
        self.assertIn('target_readout.value = target', common_source)
        self.assertIn("def current_values", common_source)
        self.assertIn("state = build_state(values=current_values())", common_source)
        self.assertLess(common_source.index("display(layout)"), common_source.rindex("state = build_state()"))
        self.assertIn("def on_target_position_change", common_source)
        self.assertIn("def enforce_target_membership", common_source)
        self.assertIn("target = enforce_target_membership", common_source)
        self.assertIn("def update_target_position_visibility", common_source)
        self.assertIn('target_position_input.layout.display = None if target_mode_input.value == TARGET_EXISTS else "none"', common_source)
        self.assertIn("ui_state[\"first_row\"].children = tuple(first_row_controls())", common_source)
        self.assertNotIn("Objetivo automático", source)
        self.assertNotIn("auto_target_checkbox", source)
        self.assertIn("from common.animation_runtime import OutputCache, formula_iframe_height, pause, set_disabled", common_source)
        self.assertIn("render_cache = OutputCache()", common_source)
        self.assertIn('formula = state.get("formula")', common_source)
        self.assertIn("formula_output = widgets.HTML", common_source)
        self.assertNotIn("widgets.HTMLMath", common_source)
        self.assertIn('render_cache.update_formula(formula_output, formula, state.get("formula_reserved_height"))', common_source)
        self.assertIn("render_cache.update_html(html_output, render_html(state))", common_source)
        self.assertNotIn("async def run_async", common_source)
        self.assertNotIn("schedule(", common_source)
        self.assertIn("auto_button.on_click(run_auto)", common_source)
        self.assertNotIn("AUTO_RENDER_EVERY", common_source)
        self.assertIn("formula_output", common_source)
        self.assertIn("def range_formula_rows(state):", source)
        self.assertIn("{range_formula_rows(state)}", source)
        self.assertNotIn("search-status", source)
        self.assertNotIn("status-equation", source)
        self.assertIn("LABEL_HTML", source)
        self.assertIn("m<sub>1</sub>", source)
        self.assertIn("m<sub>2</sub>", source)
        self.assertIn("math_inline", common_source)
        self.assertIn("font-size: 20px;", common_source)
        self.assertIn("margin-top: 8px;", common_source)

    def test_array_labels_render_as_math_html(self):
        state = self.module.create_state(size=8, target=8, values=[1, 2, 3, 4, 5, 6, 7, 8])
        self.module.step_ternary_search(state)
        html = self.module.render_state_html(state)

        self.assertIn('<span class="math-label">a</span>', html)
        self.assertIn('<span class="math-label">b</span>', html)
        self.assertIn('<span class="math-label">m<sub>1</sub></span>', html)
        self.assertIn('<span class="math-label">m<sub>2</sub></span>', html)

    def test_multiple_array_labels_share_one_line(self):
        state = self.module.create_state(size=1, target=8, values=[8])
        state["arr"][0]["label"] = "a\nb\nm1\nm2"
        html = self.module.render_state_html(state)

        self.assertIn('<span class="label-separator">, </span>', html)
        self.assertNotIn("<br>", html)
        self.assertIn(
            '<span class="math-label">a</span><span class="label-separator">, </span><span class="math-label">b</span>',
            html,
        )

    def test_range_values_share_one_formula_row(self):
        state = self.module.create_state(size=8, target=8, values=[1, 2, 3, 4, 5, 6, 7, 8])
        formula = self.module.range_formula_rows(state)

        self.assertIn("a\n&=\n0,\\;\\; b = 7", formula)
        self.assertNotIn("\\quad", formula)
        self.assertEqual(formula.count("\\\\[14pt]"), 1)
        self.assertNotIn("\\\\[8pt]", formula)

    def test_messages_render_equations_as_math_html(self):
        self.assertIn(
            '<span class="math-inline">m<sub>1</sub> = 2</span>',
            self.module.message_html("Compara contra m1 = 2 y m2 = 5."),
        )
        self.assertIn(
            '<span class="math-inline">m<sub>2</sub> = 5</span>',
            self.module.message_html("Compara contra m1 = 2 y m2 = 5."),
        )
        self.assertIn(
            '<span class="math-inline">8 &lt; 20</span>',
            self.module.message_html("8 es menor que 20; descarta desde m1 hacia la derecha."),
        )
        self.assertIn(
            '<span class="math-inline">30 &gt; 20</span>',
            self.module.message_html("30 es mayor que 20; descarta desde m2 hacia la izquierda."),
        )
        self.assertIn(
            '<span class="math-inline">20 &lt; 25 &lt; 30</span>',
            self.module.message_html("25 está entre 20 y 30; descarta los extremos."),
        )

    def test_ternaria(self):
        for values, target, should_find in SEARCH_CASES:
            with self.subTest(values=values, target=target):
                state = self.module.create_state(size=len(values), target=target, values=values)

                for _ in range(32):
                    if state["search_complete"]:
                        break
                    self.module.step_ternary_search(state)

                self.assertTrue(state["search_complete"])
                found_nodes = [node for node in state["arr"] if node["role"] == "found"]

                if should_find:
                    self.assertEqual(state["general_message"], self.module.FOUND_MESSAGE)
                    self.assertEqual(len(found_nodes), 1)
                    self.assertEqual(found_nodes[0]["value"], target)
                else:
                    self.assertEqual(state["general_message"], self.module.NOT_FOUND_MESSAGE)
                    self.assertEqual(found_nodes, [])


class TestCapitulo7LocalVoilaLauncher(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module_from_path("capitulo7_abrir_busqueda", LOCAL_APP_PATH)

    def test_local_launcher_registers_all_search_notebooks(self):
        self.assertEqual(
            self.module.NOTEBOOKS,
            {
                "comparacion": "0_comparacion_busquedas.ipynb",
                "secuencial": "1_busqueda_secuencial.ipynb",
                "binaria": "2_busqueda_binaria.ipynb",
                "interpolacion": "3_busqueda_interpolacion.ipynb",
                "saltos": "4_busqueda_saltos.ipynb",
                "exponencial": "5_busqueda_exponencial.ipynb",
                "ternaria": "6_busqueda_ternaria.ipynb",
            },
        )

    def test_local_launcher_hides_notebook_sources_with_voila(self):
        source = LOCAL_APP_PATH.read_text(encoding="utf-8")

        self.assertIn('"-m"', source)
        self.assertIn('"voila"', source)
        self.assertIn("--VoilaConfiguration.strip_sources=True", source)
        self.assertIn("python3 -m pip install voila ipywidgets", source)


class TestCapitulo7IndividualNotebooks(unittest.TestCase):
    def test_individual_notebooks_keep_only_minimal_invocation_code(self):
        expected = {
            "1_busqueda_secuencial.ipynb": "secuencial",
            "2_busqueda_binaria.ipynb": "binaria",
            "3_busqueda_interpolacion.ipynb": "interpolacion",
            "4_busqueda_saltos.ipynb": "saltos",
            "5_busqueda_exponencial.ipynb": "exponencial",
            "6_busqueda_ternaria.ipynb": "ternaria",
        }

        chart_names = {
            "1_busqueda_secuencial.ipynb": "Secuencial",
            "2_busqueda_binaria.ipynb": "Binaria",
            "3_busqueda_interpolacion.ipynb": "Interpolación",
            "4_busqueda_saltos.ipynb": "Saltos",
            "5_busqueda_exponencial.ipynb": "Exponencial",
            "6_busqueda_ternaria.ipynb": "Ternaria",
        }

        for notebook_name, simulation_name in expected.items():
            with self.subTest(notebook=notebook_name):
                notebook = json.loads((PROJECT_ROOT / "capitulo7" / "notebooks" / notebook_name).read_text())
                code_cells = [cell for cell in notebook["cells"] if cell["cell_type"] == "code"]
                if notebook_name == "3_busqueda_interpolacion.ipynb":
                    sources = ["".join(cell["source"]) for cell in code_cells]
                    self.assertTrue(any(f'SIMULATION_NAME = "{simulation_name}"' in source for source in sources))
                    self.assertTrue(any('run_single_chart("Interpolación")' in source for source in sources))
                    self.assertTrue(any("run_general_formula_visual" in source for source in sources))
                    self.assertTrue(any("run_interpolation_visual" in source for source in sources))
                    self.assertTrue(any("def interpolation_search" in source for source in sources))
                    self.assertTrue(any("def fit_function" in source for source in sources))
                    for cell in code_cells:
                        self.assertEqual(cell.get("outputs"), [])
                        self.assertIsNone(cell.get("execution_count"))
                    continue

                expected_code_cells = 3 if notebook_name == "6_busqueda_ternaria.ipynb" else 2
                self.assertEqual(len(code_cells), expected_code_cells)

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
                self.assertIn("busquedas_chart", chart_source)
                self.assertNotIn("from busquedas_chart import", chart_source)
                self.assertIn("search_metrics.py", chart_source)
                self.assertIn(f'run_single_chart("{chart_names[notebook_name]}")', chart_source)
                self.assertEqual(code_cells[1].get("outputs"), [])
                self.assertIsNone(code_cells[1].get("execution_count"))

                if notebook_name == "6_busqueda_ternaria.ipynb":
                    asymptotic_source = "".join(code_cells[2]["source"])
                    self.assertIn("log2_n", asymptotic_source)
                    self.assertIn("log3_n", asymptotic_source)
                    self.assertIn("two_log3_n", asymptotic_source)
                    self.assertIn('"figure.dpi": 500', asymptotic_source)
                    self.assertIn('"savefig.dpi": 500', asymptotic_source)
                    self.assertEqual(code_cells[2].get("outputs"), [])
                    self.assertIsNone(code_cells[2].get("execution_count"))


class TestCapitulo7BusquedaExponencial(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.launchers = load_module_from_path("capitulo7_launchers_exponencial", LAUNCHERS_PATH)
        cls.module = cls.launchers._load_module(
            "5_busqueda_exponencial_app.py",
            "capitulo7_exponencial_test_app",
        )

    def test_launchers_load_exponential_module(self):
        self.assertTrue(hasattr(self.launchers, "run_exponencial"))
        self.assertTrue(hasattr(self.module, "run_app"))
        self.assertTrue(hasattr(self.module, "create_state"))
        self.assertTrue(hasattr(self.module, "step_exponential_search"))
        self.assertTrue(hasattr(self.module, "build_range_formula"))
        self.assertEqual(self.module.BOOK_ARRAY, [1, 2, 3, 4, 5, 6, 7, 8])
        self.assertEqual(self.module.BOOK_TARGET, 6)

    def test_original_exponential_visual_conventions_are_preserved(self):
        self.assertEqual(self.module.ROLE_STYLES["target"], ("#fff2cc", "#d6b656", "#111111"))
        self.assertEqual(self.module.ROLE_STYLES["range"], ("#dae8fc", "#6c8ebf", "#111111"))
        self.assertEqual(self.module.ROLE_STYLES["probe"], ("#f8cecc", "#b85450", "#111111"))
        self.assertEqual(self.module.ROLE_STYLES["current"], ("#dae8fc", "#6c8ebf", "#111111"))

    def test_existing_target_starts_highlighted(self):
        state = self.module.create_state(size=8, target=6, values=[1, 2, 3, 4, 5, 6, 7, 8])
        missing_state = self.module.create_state(size=8, target=9, values=[1, 2, 3, 4, 5, 6, 7, 8])
        html = self.module.render_state_html(state)

        self.assertEqual(state["arr"][5]["role"], "target")
        self.assertTrue(state["arr"][5]["is_target"])
        self.assertNotIn("target", [node["role"] for node in missing_state["arr"]])
        self.assertIn("background:#fff2cc", html)
        state["arr"][5]["role"] = "current"
        self.assertIn("background:#dae8fc", self.module.render_state_html(state))
        state["arr"][5]["role"] = "found"
        self.assertIn("background:#e8fce9", self.module.render_state_html(state))

    def test_exponential_ui_features_are_present(self):
        source = (PROJECT_ROOT / "capitulo7" / "domain" / "5_busqueda_exponencial_app.py").read_text()
        common_source = (PROJECT_ROOT / "capitulo7" / "domain" / "search_common.py").read_text()
        bootstrap = (PROJECT_ROOT / "capitulo7" / "notebooks" / "colab_bootstrap.py").read_text()
        notebook = (PROJECT_ROOT / "capitulo7" / "notebooks" / "5_busqueda_exponencial.ipynb").read_text()

        self.assertIn('description="Generar arreglo del libro"', common_source)
        self.assertNotIn("Objetivo automático", source)
        self.assertNotIn("auto_target_checkbox", source)
        self.assertIn("render_cache = OutputCache()", common_source)
        self.assertIn('formula = state.get("formula")', common_source)
        self.assertIn("formula_output = widgets.HTML", common_source)
        self.assertNotIn("widgets.HTMLMath", common_source)
        self.assertIn('render_cache.update_formula(formula_output, formula, state.get("formula_reserved_height"))', common_source)
        self.assertIn("render_cache.update_html(html_output, render_html(state))", common_source)
        self.assertIn("formula_output", common_source)
        self.assertIn("LABEL_HTML", source)
        self.assertIn("math_inline", common_source)
        self.assertIn("margin-top: 8px;", common_source)
        self.assertIn('"common/animation_runtime.py"', bootstrap)
        self.assertIn("5_busqueda_exponencial_app.py", bootstrap)
        self.assertIn('"SIMULATION_NAME = \\"exponencial\\"\\n"', notebook)

    def test_exponential_labels_render_as_math_html(self):
        state = self.module.create_state(size=8, target=6, values=[1, 2, 3, 4, 5, 6, 7, 8])

        while state["phase"] != "range_show":
            self.module.step_exponential_search(state)

        html = self.module.render_state_html(state)
        self.assertIn('<span class="math-label">a</span>', html)
        self.assertIn('<span class="math-label">b</span>', html)
        self.assertNotIn("inicio", html)
        self.assertNotIn("fin", html)

        self.module.step_exponential_search(state)
        self.module.step_exponential_search(state)
        html = self.module.render_state_html(state)
        self.assertIn('<span class="math-label">m</span>', html)
        self.assertNotIn("medio", html)

    def test_exponential_messages_render_equations_as_math_html(self):
        self.assertIn(
            '<span class="math-inline">i = 4</span>',
            self.module.message_html("5 no coincide; actualiza i a 4."),
        )
        self.assertIn(
            '<span class="math-inline">8 &gt; 6</span>',
            self.module.message_html("8 es mayor que 6; rango calculado [2, 4]."),
        )
        self.assertIn(
            '<span class="math-inline">[2, 4]</span>',
            self.module.message_html("Aplica búsqueda binaria en el rango [2, 4]."),
        )
        self.assertIn(
            "Búsqueda binaria:",
            self.module.message_html("Búsqueda binaria: evalúa m en la posición 3."),
        )

    def test_exponential_formula_always_shows_all_equations_in_single_rows(self):
        state = self.module.create_state(size=8, target=6, values=[1, 2, 3, 4, 5, 6, 7, 8])
        initial_formula = state["formula"]

        self.assertIn("\\text{Fase exponencial (en ejecución)}", initial_formula)
        self.assertIn("\\text{Búsqueda binaria (inactiva)}", initial_formula)
        self.assertIn("i &= 2 \\cdot i", initial_formula)
        self.assertIn("\\mathrm{rango} &= \\left[\\frac{i}{2}, \\min(i, n - 1)\\right]", initial_formula)
        self.assertIn("m &= a + \\left\\lfloor\\frac{b - a}{2}\\right\\rfloor", initial_formula)
        self.assertNotIn("inicio", initial_formula)
        self.assertNotIn("fin", initial_formula)
        self.assertNotIn("medio", initial_formula)

        self.module.step_exponential_search(state)
        show_formula = state["formula"]
        self.assertEqual([node["label"] for node in state["arr"]], ["i", "", "", "", "", "", "", ""])
        self.assertFalse(state["arr"][0]["reviewed"])
        self.assertIn("i &= 2 \\cdot i", show_formula)
        self.assertNotIn("2 \\cdot 0 = 1", show_formula)

        self.module.step_exponential_search(state)
        next_formula = state["formula"]
        self.assertIn("i &= 2 \\cdot i = 2 \\cdot 0 = 1", next_formula)
        self.assertIn("\\mathrm{rango} &=", next_formula)
        self.assertIn("m &=", next_formula)

        while state["phase"] != "range_show":
            self.module.step_exponential_search(state)
        range_formula = state["formula"]
        self.assertIn("\\text{Fase exponencial (terminado)}", range_formula)
        self.assertIn("\\text{Búsqueda binaria (inactiva)}", range_formula)
        self.assertIn("\\mathrm{rango} &= \\left[\\frac{i}{2}, \\min(i, n - 1)\\right] = ", range_formula)
        self.assertIn(" = [4, 7]", range_formula)
        self.assertIn("m &=", range_formula)

        self.module.step_exponential_search(state)
        self.module.step_exponential_search(state)
        mid_formula = state["formula"]
        self.assertIn("\\text{Fase exponencial (terminado)}", mid_formula)
        self.assertIn("\\text{Búsqueda binaria (en ejecución)}", mid_formula)
        self.assertIn("i &= 2 \\cdot i = 2 \\cdot 4 = 8", mid_formula)
        self.assertIn("m &= a + \\left\\lfloor\\frac{b - a}{2}\\right\\rfloor = ", mid_formula)
        self.assertIn(" = 5", mid_formula)
        self.assertNotIn("inicio", mid_formula)
        self.assertNotIn("fin", mid_formula)
        self.assertNotIn("medio", mid_formula)

    def test_exponential_search(self):
        cases = [
            ([1, 2, 3, 4, 5, 6, 7, 8], 6, True),
            ([1, 2, 3, 4, 5, 6, 7, 8], 9, False),
            ([2, 5, 9, 14, 18, 27, 33, 40], 2, True),
            ([2, 5, 9, 14, 18, 27, 33, 40], 17, False),
        ]

        for values, target, should_find in cases:
            with self.subTest(values=values, target=target):
                state = self.module.create_state(size=len(values), target=target, values=values)

                for _ in range(64):
                    if state["search_complete"]:
                        break
                    self.module.step_exponential_search(state)

                self.assertTrue(state["search_complete"])
                found_nodes = [node for node in state["arr"] if node["role"] == "found"]

                if should_find:
                    self.assertEqual(state["general_message"], self.module.FOUND_MESSAGE)
                    self.assertEqual(len(found_nodes), 1)
                    self.assertEqual(found_nodes[0]["value"], target)
                else:
                    self.assertEqual(state["general_message"], self.module.NOT_FOUND_MESSAGE)
                    self.assertEqual(found_nodes, [])


class TestCapitulo7BusquedasRestantes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.launchers = load_module_from_path("capitulo7_launchers_restantes", LAUNCHERS_PATH)
        cls.modules = {
            name: cls.launchers._load_module(path, f"capitulo7_{name}_test_app")
            for name, (path, _step, _launcher) in SEARCH_MODULES.items()
        }

    def test_launchers_and_bootstrap_include_all_remaining_searches(self):
        bootstrap = (PROJECT_ROOT / "capitulo7" / "notebooks" / "colab_bootstrap.py").read_text(encoding="utf-8")

        self.assertTrue(hasattr(self.launchers, "run_comparacion"))
        self.assertIn("0_comparacion_busquedas_app.py", bootstrap)
        self.assertIn('"comparacion": "run_comparacion"', bootstrap)

        for name, (path, _step, launcher_name) in SEARCH_MODULES.items():
            with self.subTest(name=name):
                self.assertTrue(hasattr(self.launchers, launcher_name))
                self.assertIn(path, bootstrap)
                self.assertIn(f'"{name}": "{launcher_name}"', bootstrap)

    def test_notebooks_are_clean_invocations(self):
        comparison_notebook = PROJECT_ROOT / "capitulo7" / "notebooks" / "0_comparacion_busquedas.ipynb"
        comparison_nb = json.loads(comparison_notebook.read_text(encoding="utf-8"))
        comparison_source = "".join(comparison_nb["cells"][1]["source"])
        self.assertIn('SIMULATION_NAME = "comparacion"', comparison_source)
        self.assertEqual(comparison_nb["cells"][1]["outputs"], [])
        self.assertIsNone(comparison_nb["cells"][1]["execution_count"])
        self.assertTrue(comparison_nb["cells"][1]["metadata"]["jupyter"]["source_hidden"])

        for index, name in enumerate(("secuencial", "binaria", "interpolacion", "saltos"), start=1):
            with self.subTest(name=name):
                notebook = PROJECT_ROOT / "capitulo7" / "notebooks" / f"{index}_busqueda_{name}.ipynb"
                nb = json.loads(notebook.read_text(encoding="utf-8"))
                source = next(
                    "".join(cell["source"])
                    for cell in nb["cells"]
                    if cell["cell_type"] == "code" and f'SIMULATION_NAME = "{name}"' in "".join(cell["source"])
                )
                self.assertIn(f'SIMULATION_NAME = "{name}"', source)
                for cell in nb["cells"]:
                    if cell["cell_type"] == "code":
                        self.assertEqual(cell["outputs"], [])
                        self.assertIsNone(cell["execution_count"])

    def test_visual_conventions_and_labels_are_preserved(self):
        expected = {
            "secuencial": {
                "range": ("#fff2cc", "#d6b656", "#111111"),
                "probe": ("#f8cecc", "#b85450", "#111111"),
            },
            "binaria": {
                "range": ("#ffffff", "#111111", "#111111"),
                "probe": ("#f8cecc", "#b85450", "#111111"),
            },
            "interpolacion": {
                "range": ("#ffffff", "#111111", "#111111"),
                "probe": ("#f8cecc", "#b85450", "#111111"),
            },
            "saltos": {
                "range": ("#ffffff", "#111111", "#111111"),
                "probe": ("#f8cecc", "#b85450", "#111111"),
            },
        }

        common_source = (PROJECT_ROOT / "capitulo7" / "domain" / "search_common.py").read_text(encoding="utf-8")
        for name, module in self.modules.items():
            with self.subTest(name=name):
                self.assertEqual(module.ROLE_STYLES["range"], expected[name]["range"])
                self.assertEqual(module.ROLE_STYLES["probe"], expected[name]["probe"])
                self.assertEqual(module.ROLE_STYLES["default"][0], "#ffffff")
                self.assertEqual(module.ROLE_STYLES["target"], ("#fff2cc", "#d6b656", "#111111"))
                html = module.render_state_html(module.create_state(size=8, target=6, values=[1, 2, 3, 4, 5, 6, 7, 8]))
                self.assertNotIn("search-status", html)
                self.assertIn("background:#fff2cc", html)
                self.assertNotIn("border-color:", html)
                self.assertIn("font-size: 20px;", common_source)
                self.assertIn("margin-top: 8px;", common_source)

    def test_existing_target_starts_highlighted_in_all_remaining_searches(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8]

        for name, module in self.modules.items():
            with self.subTest(name=name):
                kwargs = {"uniform": False} if name == "interpolacion" else {}
                state = module.create_state(size=len(values), target=6, values=values, **kwargs)
                missing_state = module.create_state(size=len(values), target=9, values=values, **kwargs)
                html = module.render_state_html(state)

                self.assertEqual(state["arr"][5]["role"], "target")
                self.assertTrue(state["arr"][5]["is_target"])
                self.assertNotIn("target", [node["role"] for node in missing_state["arr"]])
                self.assertIn("background:#fff2cc", html)
                state["arr"][5]["role"] = "current"
                self.assertIn("background:#dae8fc", module.render_state_html(state))
                state["arr"][5]["role"] = "found"
                self.assertIn("background:#e8fce9", module.render_state_html(state))

    def test_binary_and_interpolation_use_symbol_labels(self):
        binary = self.modules["binaria"]
        binary_state = binary.create_state(size=8, target=6, values=[1, 2, 3, 4, 5, 6, 7, 8])
        binary.step_binary_search(binary_state)
        binary_html = binary.render_state_html(binary_state)

        self.assertIn('<span class="math-label">a</span>', binary_html)
        self.assertIn('<span class="math-label">m</span>', binary_html)
        self.assertIn('<span class="math-label">b</span>', binary_html)
        self.assertIn(r"m =", binary_state["formula"])
        self.assertIn(r"a + \left\lfloor", binary_state["formula"])
        self.assertIn(r"\frac{b - a}{2}", binary_state["formula"])
        self.assertNotIn("medio =", binary_state["formula"])
        self.assertNotIn("inicio + fin", binary_state["formula"])

        interpolation = self.modules["interpolacion"]
        interpolation_state = interpolation.create_state(size=8, target=6, values=[1, 2, 3, 4, 5, 6, 7, 8])
        interpolation.step_interpolation_search(interpolation_state)
        interpolation_html = interpolation.render_state_html(interpolation_state)

        self.assertIn('<span class="math-label">a</span>', interpolation_html)
        self.assertIn('<span class="math-label">p</span>', interpolation_html)
        self.assertIn('<span class="math-label">b</span>', interpolation_html)
        self.assertIn(r"p =", interpolation_state["formula"])
        self.assertIn(r"(b - a)(x - arr[a])", interpolation_state["formula"])
        self.assertNotIn("pos =", interpolation_state["formula"])
        self.assertNotIn("elemento", interpolation_state["formula"])

    def test_no_remaining_search_uses_automatic_target_checkbox(self):
        for name, (path, _step, _launcher) in SEARCH_MODULES.items():
            with self.subTest(name=name):
                source = (PROJECT_ROOT / "capitulo7" / "domain" / path).read_text(encoding="utf-8")
                self.assertNotIn("Objetivo automático", source)
                self.assertNotIn("auto_target_checkbox", source)

    def test_individual_searches_share_default_size(self):
        expected_default_size = "DEFAULT_SIZE = 10"
        for path in sorted((PROJECT_ROOT / "capitulo7" / "domain").glob("*_busqueda_*_app.py")):
            with self.subTest(path=path.name):
                source = path.read_text(encoding="utf-8")
                self.assertIn(expected_default_size, source)

    def test_search_apps_use_common_runner(self):
        common_source = (PROJECT_ROOT / "capitulo7" / "domain" / "search_common.py").read_text(encoding="utf-8")

        self.assertIn("def run_search_app", common_source)
        self.assertIn('description="Paso siguiente"', common_source)
        self.assertIn('description="Ejecución automática"', common_source)
        self.assertIn('description="Generar nuevo arreglo"', common_source)
        self.assertIn('description="Generar arreglo del libro"', common_source)
        self.assertIn('"capitulo7/domain/search_common.py"', (PROJECT_ROOT / "capitulo7" / "notebooks" / "colab_bootstrap.py").read_text(encoding="utf-8"))

        for path in sorted((PROJECT_ROOT / "capitulo7" / "domain").glob("*_busqueda_*_app.py")):
            with self.subTest(path=path.name):
                source = path.read_text(encoding="utf-8")
                self.assertIn("from search_common import (", source)
                self.assertIn("run_search_app", source)
                self.assertIn("render_state_html as render_search_state_html", source)
                self.assertIn("run_search_app(", source)

    def test_interpolation_imports_extra_widget_dependency(self):
        source = (PROJECT_ROOT / "capitulo7" / "domain" / "3_busqueda_interpolacion_app.py").read_text(encoding="utf-8")

        self.assertIn("import ipywidgets as widgets", source)
        self.assertIn("widgets.Checkbox", source)

    def test_formula_output_reserves_stable_space(self):
        common_source = (PROJECT_ROOT / "capitulo7" / "domain" / "search_common.py").read_text(encoding="utf-8")
        runtime_source = (PROJECT_ROOT / "common" / "animation_runtime.py").read_text(encoding="utf-8")

        self.assertIn('min_height="0px"', common_source)
        self.assertIn('padding="30px 0 0 0"', common_source)
        self.assertIn('margin="0"', common_source)
        self.assertIn('overflow="visible"', common_source)
        self.assertIn("widget.layout.min_height", runtime_source)
        self.assertIn("formula_iframe_height(formula)", runtime_source)
        self.assertIn("calculate_formula_reserved_height(state, step_search)", common_source)
        self.assertIn('state["formula_reserved_height"]', common_source)
        self.assertIn('state.get("formula_reserved_height")', common_source)
        self.assertIn("self.max_formula_height", runtime_source)
        self.assertIn("align-items:flex-end", runtime_source)
        self.assertIn("justify-content:flex-start", runtime_source)
        self.assertIn("text-align:left", runtime_source)
        self.assertNotIn("frameElement.style.height", runtime_source)

        for constant in (
            'PHASE_RUNNING = "en ejecución"',
            'PHASE_DONE = "terminado"',
            'PHASE_INACTIVE = "inactiva"',
        ):
            self.assertIn(constant, common_source)
        for filename in ("4_busqueda_saltos_app.py", "5_busqueda_exponencial_app.py"):
            with self.subTest(filename=filename):
                source = (PROJECT_ROOT / "capitulo7" / "domain" / filename).read_text(encoding="utf-8")
                self.assertIn(r"\begin{{array}}{{l}}", source)
                self.assertNotIn(r"\begin{{gathered}}", source)

    def test_exponential_formula_space_is_reserved_before_binary_phase(self):
        module = self.launchers._load_module("5_busqueda_exponencial_app.py", "capitulo7_exponential_reserved_height_test")
        common = self.launchers._load_module("search_common.py", "capitulo7_search_common_reserved_height_test")
        state = module.create_state(size=8, target=6, values=[1, 2, 3, 4, 5, 6, 7, 8])
        reserved = common.calculate_formula_reserved_height(state, module.step_exponential_search)
        initial_height = common.formula_iframe_height(state["formula"])

        self.assertGreater(reserved, initial_height)

        heights = []
        for _ in range(32):
            heights.append(common.formula_iframe_height(state["formula"]))
            if state["search_complete"]:
                break
            module.step_exponential_search(state)

        self.assertEqual(reserved, max(heights))

    def test_search_math_text_uses_same_font_as_array_values(self):
        common_source = (PROJECT_ROOT / "capitulo7" / "domain" / "search_common.py").read_text(encoding="utf-8")
        self.assertIn("font-family: '{FONT_FAMILY}', serif;", common_source)

        for path in sorted((PROJECT_ROOT / "capitulo7" / "domain").glob("*_busqueda_*_app.py")):
            with self.subTest(path=path.name):
                source = path.read_text(encoding="utf-8")
                self.assertIn("FONT_FAMILY = \"Scheherazade New\"", source)
                self.assertNotIn("font-family: '{FONT_FAMILY}', serif;", source)
                self.assertNotIn("Times New Roman", source)
                self.assertNotIn("Cambria Math", source)
                self.assertNotIn("FORMULA_FONT_CSS", source)
                self.assertNotIn("mjx-container", source)
                self.assertNotIn("display(HTML(", source)

    def test_search_nodes_reserve_compact_label_height(self):
        common_source = (PROJECT_ROOT / "capitulo7" / "domain" / "search_common.py").read_text(encoding="utf-8")

        self.assertIn("SEARCH_NODES_PER_ROW = 10", common_source)
        self.assertIn("SEARCH_NODE_WIDTH = 54", common_source)
        self.assertIn("SEARCH_NODE_HEIGHT = 116", common_source)
        self.assertIn("SEARCH_NODE_GAP = 0", common_source)
        self.assertIn("SEARCH_LABEL_HEIGHT = 28", common_source)
        self.assertIn("SEARCH_MESSAGE_HEIGHT = 44", common_source)
        self.assertIn("SEARCH_RESULT_WIDTH = 42", common_source)
        self.assertIn("def calculate_search_dimensions(state):", common_source)
        self.assertIn('min-height: {dimensions["app_height"]}px;', common_source)
        self.assertIn('min-height: {dimensions["nodes_height"]}px;', common_source)
        self.assertIn('height: {SEARCH_MESSAGE_HEIGHT}px;', common_source)
        self.assertIn("search-array-line", common_source)
        self.assertIn("search-result-symbol", common_source)
        self.assertIn("def render_result_symbol(state):", common_source)
        self.assertIn('width: min(100%, {dimensions["nodes_width"]}px);', common_source)
        self.assertIn("height: {SEARCH_NODE_HEIGHT}px;", common_source)
        self.assertIn("flex: 0 0 {SEARCH_NODE_WIDTH}px;", common_source)
        self.assertIn("flex: 0 0 54px;", common_source)
        self.assertIn("gap: {SEARCH_NODE_GAP}px;", common_source)
        self.assertIn("border: 2px solid #111111;", common_source)
        self.assertIn("border-left-width: 0;", common_source)
        self.assertIn(".node-wrap:nth-child({SEARCH_NODES_PER_ROW}n + 1) .node", common_source)
        self.assertIn("border-radius: 0;", common_source)
        self.assertIn("box-shadow: none;", common_source)
        self.assertIn("box-sizing: border-box;", common_source)
        self.assertIn("height: 24px;", common_source)
        self.assertIn("flex: 0 0 24px;", common_source)
        self.assertIn("line-height: 24px;", common_source)
        self.assertIn("height: {SEARCH_LABEL_HEIGHT}px;", common_source)
        self.assertIn("min-height: {SEARCH_LABEL_HEIGHT}px;", common_source)
        self.assertIn("overflow: visible;", common_source)
        self.assertIn("white-space: nowrap;", common_source)
        self.assertIn("label-separator", common_source)

        for path in sorted((PROJECT_ROOT / "capitulo7" / "domain").glob("*_busqueda_*_app.py")):
            with self.subTest(path=path.name):
                source = path.read_text(encoding="utf-8")
                self.assertIn("render_search_state_html(state, ROLE_STYLES, LABEL_HTML)", source)
                self.assertNotIn("SEARCH_NODE_HEIGHT", source)
                self.assertNotIn("SEARCH_NODE_WIDTH", source)
                self.assertNotIn("def node_html", source)
                self.assertNotIn("def label_html", source)
                self.assertNotIn("def message_html", source)
                self.assertNotIn("def math_inline", source)

    def test_search_dimensions_are_cached_by_size(self):
        common = self.launchers._load_module("search_common.py", "capitulo7_search_common_cache_test")
        common._SEARCH_DIMENSION_CACHE.clear()
        first = common.calculate_search_dimensions({"arr": [{"value": index} for index in range(12)]})
        second = common.calculate_search_dimensions({"arr": [{"value": index} for index in range(12)]})

        self.assertIs(first, second)
        self.assertIn(12, common._SEARCH_DIMENSION_CACHE)

    def test_search_node_html_is_cached_per_state(self):
        module = self.modules["binaria"]
        state = module.create_state(size=8, target=6, values=[1, 2, 3, 4, 5, 6, 7, 8])

        first = module.render_state_html(state)
        second = module.render_state_html(state)

        self.assertEqual(first, second)
        self.assertIn("_node_html_cache", state)

    def test_search_result_symbol_appears_only_after_completion(self):
        module = self.modules["binaria"]
        state = module.create_state(size=8, target=6, values=[1, 2, 3, 4, 5, 6, 7, 8])

        self.assertIn("search-result", module.render_state_html(state))
        self.assertNotIn("search-result-symbol", module.render_state_html(state))
        while not state["search_complete"]:
            module.step_binary_search(state)
        found_html = module.render_state_html(state)
        self.assertIn('search-result-symbol found', found_html)
        self.assertIn(">✓</span>", found_html)
        self.assertNotIn(r"$\checkmark$", found_html)

        missing = module.create_state(size=8, target=99, values=[1, 2, 3, 4, 5, 6, 7, 8])
        while not missing["search_complete"]:
            module.step_binary_search(missing)
        missing_html = module.render_state_html(missing)
        self.assertIn('search-result-symbol missing', missing_html)
        self.assertIn(">×</span>", missing_html)
        self.assertNotIn(r"$\times$", missing_html)

    def test_search_auto_execution_stays_disabled_after_completion(self):
        common_source = (PROJECT_ROOT / "capitulo7" / "domain" / "search_common.py").read_text(encoding="utf-8")

        self.assertIn("def sync_execution_buttons():", common_source)
        self.assertIn('complete = state["search_complete"]', common_source)
        self.assertIn("step_button.disabled = complete", common_source)
        self.assertIn("auto_button.disabled = complete", common_source)
        self.assertIn("finish_button.disabled = complete", common_source)
        self.assertIn("def finish_without_animation", common_source)
        self.assertIn("def enable_controls_for_new_array():", common_source)
        self.assertIn("reset_button.disabled = False", common_source)
        self.assertIn("book_button.disabled = False", common_source)
        self.assertIn("sync_execution_buttons()", common_source)
        self.assertIn("enable_controls_for_new_array()", common_source)

    def test_sequential_book_array_is_available(self):
        module = self.modules["secuencial"]

        self.assertEqual(module.BOOK_ARRAY, [0, 1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(module.BOOK_TARGET, 6)
        source = (PROJECT_ROOT / "capitulo7" / "domain" / "search_common.py").read_text(encoding="utf-8")
        self.assertIn('description="Generar arreglo del libro"', source)

    def test_sequential_search_labels_current_index(self):
        module = self.modules["secuencial"]
        state = module.create_state(size=4, target=3, values=[1, 2, 3, 4])

        self.assertIn("i &= 0", state["formula"])
        module.step_linear_search(state)
        html = module.render_state_html(state)
        self.assertIn('<span class="math-label">i</span>', html)
        self.assertEqual([node["label"] for node in state["arr"]], ["i", "", "", ""])
        self.assertFalse(state["arr"][0]["reviewed"])
        self.assertIn("i &= 0", state["formula"])

        module.step_linear_search(state)
        labels = [node["label"] for node in state["arr"]]
        self.assertEqual(labels, ["", "", "", ""])
        self.assertEqual(state["phase"], "show_current")
        self.assertIn("i &= 1", state["formula"])

        module.step_linear_search(state)
        labels = [node["label"] for node in state["arr"]]
        self.assertEqual(labels, ["", "i", "", ""])
        self.assertEqual(state["phase"], "compare_current")

    def test_searches_expose_first_step_before_comparison(self):
        cases = (
            ("binaria", "step_binary_search", "m", "compare"),
            ("interpolacion", "step_interpolation_search", "p", "compare"),
            ("ternaria", "step_ternary_search", "m1", "compare"),
            ("exponencial", "step_exponential_search", "i", "exponential_compare"),
        )

        for module_name, step_name, expected_label, expected_phase in cases:
            with self.subTest(module=module_name):
                module = self.modules.get(module_name)
                if module is None:
                    path = "6_busqueda_ternaria_app.py" if module_name == "ternaria" else "5_busqueda_exponencial_app.py"
                    module = self.launchers._load_module(path, f"capitulo7_{module_name}_first_step_test_app")
                state = module.create_state(size=8, target=6, values=[1, 2, 3, 4, 5, 6, 7, 8])
                getattr(module, step_name)(state)

                labels = "\n".join(node["label"] for node in state["arr"])
                self.assertIn(expected_label, labels)
                self.assertEqual(state["phase"], expected_phase)
                self.assertFalse(state["search_complete"])

    def test_jump_search_uses_phase_titles_and_only_i_label(self):
        module = self.modules["saltos"]
        state = module.create_state(size=8, target=6, values=[1, 2, 3, 4, 5, 6, 7, 8])

        self.assertIn("\\text{Fase de saltos (en ejecución)}", state["formula"])
        self.assertNotIn("\\mathrm{rango}", state["formula"])
        self.assertIn("\\text{Fase lineal (inactiva)}", state["formula"])
        self.assertIn("i &= -", state["formula"])

        module.step_jump_search(state)
        html = module.render_state_html(state)
        self.assertIn("Fase de saltos", html)
        self.assertNotIn("inicio bloque", html)
        self.assertNotIn("fin bloque", html)
        self.assertIn("\\text{Fase de saltos (en ejecución)}", state["formula"])

        while state["phase"] != "linear_show":
            module.step_jump_search(state)
        self.assertIn("\\text{Fase de saltos (terminado)}", state["formula"])
        self.assertIn("\\text{Fase lineal (en ejecución)}", state["formula"])
        self.assertIn("i &= 4", state["formula"])
        module.step_jump_search(state)
        html = module.render_state_html(state)
        self.assertIn("Búsqueda secuencial", html)
        self.assertIn('<span class="math-label">i</span>', html)
        self.assertNotIn("inicio bloque", html)
        self.assertNotIn("fin bloque", html)

    def test_comparison_runs_all_searches_on_same_array(self):
        module = self.launchers._load_module(
            "0_comparacion_busquedas_app.py",
            "capitulo7_comparacion_test_app",
        )
        source = (PROJECT_ROOT / "capitulo7" / "domain" / "0_comparacion_busquedas_app.py").read_text(encoding="utf-8")
        notebook_source = (PROJECT_ROOT / "capitulo7" / "notebooks" / "0_comparacion_busquedas.ipynb").read_text(encoding="utf-8")
        values = [1, 2, 3, 4, 5, 6, 7, 8]
        state = module.create_comparison_state(size=len(values), target=6, values=values)

        self.assertEqual(module.DEFAULT_SIZE, 10)
        self.assertIn('description="Buscar"', source)
        self.assertIn('description="Finalizar"', source)
        self.assertIn("disabled=True", source)
        self.assertIn("def set_running_buttons", source)
        self.assertIn("finish_button.disabled = False", source)
        self.assertIn("finish_button.disabled = True", source)
        self.assertIn('execution_state["finish_requested"] = True', source)
        self.assertIn("def finish_comparison", source)
        self.assertIn("while not all_searches_complete(state):", source)
        self.assertIn("def comparison_delta(item):", source)
        self.assertIn('phase == "compare_current"', source)
        self.assertIn('phase in {"decide_block", "linear_compare"}', source)
        self.assertIn('phase == "binary_compare"', source)
        self.assertNotIn("AUTO_RENDER_EVERY", source)
        self.assertNotIn("Complejidad temporal", notebook_source)
        self.assertNotIn("Complejidad espacial", notebook_source)
        self.assertEqual(notebook_source.count("Mejor caso"), 1)
        self.assertEqual(notebook_source.count("Caso promedio"), 1)
        self.assertEqual(notebook_source.count("Peor caso"), 1)
        self.assertNotIn('description="Paso siguiente"', source)
        self.assertNotIn('description="Ejecución automática"', source)
        self.assertEqual(len(state["algorithms"]), 6)
        for item in state["algorithms"]:
            self.assertEqual([node["value"] for node in item["state"]["arr"]], values)
            self.assertEqual(item["state"]["target"], 6)

        module.step_all_searches(state)

        self.assertTrue(all(item["steps"] == 0 for item in state["algorithms"]))
        html = module.render_comparison_html(state)
        self.assertIn("comparison-table", html)
        self.assertIn("Algoritmo", html)
        self.assertIn("Pasos", html)
        self.assertIn("Arreglo", html)
        self.assertIn("font-weight: 700;", html)
        self.assertIn("background: #ffffff;", html)
        self.assertIn("comparison-array-head", html)
        self.assertIn("comparison-result", html)
        self.assertIn("COMPARISON_NODE_WIDTH = 54", source)
        self.assertIn("array_width = len(state[\"values\"]) * COMPARISON_NODE_WIDTH", source)
        self.assertIn("grid-template-columns: minmax(180px, 240px) 96px {array_width}px 42px;", source)
        self.assertIn("gap: 0;", source)
        self.assertIn("rows_output = widgets.HTML", source)
        self.assertIn("render_comparison_rows_html(state)", source)
        self.assertNotIn("row_outputs = []", source)
        self.assertIn("comparison-result-symbol", source)
        self.assertIn('symbol = "✓" if found else "×"', source)
        self.assertIn("border: 2px solid #111111;", source)
        self.assertNotIn("border-color:", html)
        self.assertEqual(html.count('<div class="comparison-index">'), len(values))
        self.assertNotIn(r"$\checkmark$", html)
        self.assertNotIn(r"$\times$", html)
        self.assertIn("grid-template-columns: minmax(180px, 240px) 96px 432px 42px;", html)
        self.assertIn("width: 432px;", html)
        self.assertNotIn("Arreglo:</strong>", html)
        self.assertNotIn("Objetivo:</strong>", html)
        self.assertNotIn("pasos:", html)
        self.assertNotIn("comparison-card", html)
        self.assertNotIn("search-message", html)
        self.assertNotIn("node-label", html)
        for title in (
            "Búsqueda secuencial",
            "Búsqueda binaria",
            "Búsqueda por interpolación",
            "Búsqueda por saltos",
            "Búsqueda exponencial",
            "Búsqueda ternaria",
        ):
            self.assertIn(title, html)

        while not module.all_searches_complete(state):
            module.step_all_searches(state)
        completed_html = module.render_comparison_html(state)
        metrics = self.launchers._load_module("search_metrics.py", "capitulo7_search_metrics_for_comparison_test")
        expected_steps = {
            "Búsqueda binaria": metrics.count_search_steps("Binaria", values, 6),
            "Búsqueda ternaria": metrics.count_search_steps("Ternaria", values, 6),
            "Búsqueda exponencial": metrics.count_search_steps("Exponencial", values, 6),
            "Búsqueda por interpolación": metrics.count_search_steps("Interpolación", values, 6),
            "Búsqueda por saltos": metrics.count_search_steps("Saltos", values, 6),
            "Búsqueda secuencial": metrics.count_search_steps("Secuencial", values, 6),
        }
        self.assertEqual({item["title"]: item["steps"] for item in state["algorithms"]}, expected_steps)
        self.assertEqual(completed_html.count('comparison-result-symbol found'), len(state["algorithms"]))
        self.assertEqual(completed_html.count(">✓</span>"), len(state["algorithms"]))
        self.assertNotIn(r"$\checkmark$", completed_html)
        self.assertNotIn(r"$\times$", completed_html)
        self.assertNotIn('comparison-result-symbol missing', completed_html)

        missing_state = module.create_comparison_state(
            size=len(values),
            target=99,
            values=values,
            target_mode=module.TARGET_MISSING,
        )
        while not module.all_searches_complete(missing_state):
            module.step_all_searches(missing_state)
        missing_html = module.render_comparison_html(missing_state)
        self.assertEqual(missing_html.count('comparison-result-symbol missing'), len(missing_state["algorithms"]))
        self.assertEqual(missing_html.count(">×</span>"), len(missing_state["algorithms"]))
        self.assertNotIn(r"$\checkmark$", missing_html)
        self.assertNotIn(r"$\times$", missing_html)
        self.assertNotIn('comparison-result-symbol found', missing_html)

        source = (PROJECT_ROOT / "capitulo7" / "domain" / "0_comparacion_busquedas_app.py").read_text(encoding="utf-8")
        self.assertNotIn("Generar arreglo del libro", source)
        self.assertNotIn("book_button", source)

    def test_comparison_reuses_loaded_modules_by_mtime(self):
        module = self.launchers._load_module(
            "0_comparacion_busquedas_app.py",
            "capitulo7_comparacion_cache_test_app",
        )
        module._MODULE_CACHE.clear()

        first = module.load_algorithm(module.ALGORITHMS[0])
        second = module.load_algorithm(module.ALGORITHMS[0])

        self.assertIs(first, second)
        self.assertEqual(len(module._MODULE_CACHE), 1)

    def test_comparison_target_mode_controls_membership(self):
        module = self.launchers._load_module(
            "0_comparacion_busquedas_app.py",
            "capitulo7_comparacion_target_mode_test_app",
        )
        source = (PROJECT_ROOT / "capitulo7" / "domain" / "0_comparacion_busquedas_app.py").read_text(encoding="utf-8")
        values = [1, 2, 3, 4, 5, 6, 7, 8]

        exists_state = module.create_comparison_state(
            size=len(values),
            values=values,
            target_mode=module.TARGET_EXISTS,
        )
        missing_state = module.create_comparison_state(
            size=len(values),
            values=values,
            target_mode=module.TARGET_MISSING,
        )

        self.assertIn(exists_state["target"], values)
        self.assertNotIn(missing_state["target"], values)
        self.assertIn("target_readout = widgets.BoundedIntText", source)
        self.assertIn("disabled=True", source)
        self.assertIn('controls.append(target_readout)', source)
        self.assertIn("def update_target_readout", source)
        self.assertIn('target_readout.value = target', source)
        self.assertIn("def current_values", source)
        self.assertIn("state = build_state(values=current_values())", source)
        self.assertLess(source.index("display(controls)"), source.rindex("state = build_state()"))
        self.assertIn("def on_target_position_change", source)
        self.assertIn("enforce_target_membership", source)
        self.assertIn("def update_target_position_visibility", source)
        self.assertIn('target_position_input.layout.display = None if target_mode_input.value == TARGET_EXISTS else "none"', source)
        self.assertIn("ui_state[\"first_row\"].children = tuple(first_row_controls())", source)

    def test_target_position_selects_existing_value_location(self):
        module = self.launchers._load_module(
            "0_comparacion_busquedas_app.py",
            "capitulo7_comparacion_target_position_test_app",
        )
        common = self.launchers._load_module(
            "search_common.py",
            "capitulo7_search_common_target_position_test",
        )
        values = [1, 2, 3, 4, 5, 6, 7, 8]

        self.assertEqual(
            common.choose_target(values, common.TARGET_EXISTS, common.TARGET_POSITION_START),
            1,
        )
        self.assertEqual(
            common.choose_target(values, common.TARGET_EXISTS, common.TARGET_POSITION_END),
            8,
        )
        self.assertEqual(
            common.choose_target(values, common.TARGET_EXISTS, common.TARGET_POSITION_MIDDLE),
            5,
        )

        state = module.create_comparison_state(
            size=len(values),
            values=values,
            target_mode=module.TARGET_EXISTS,
            target_position=module.TARGET_POSITION_END,
        )

        self.assertEqual(state["target"], 8)
        self.assertEqual(state["target_position"], module.TARGET_POSITION_END)
        self.assertEqual(state["values"], values)

        middle_state = module.create_comparison_state(
            size=len(values),
            values=state["values"],
            target_mode=module.TARGET_EXISTS,
            target_position=module.TARGET_POSITION_MIDDLE,
        )

        self.assertEqual(middle_state["values"], values)
        self.assertEqual(middle_state["target"], 5)

    def test_target_membership_is_enforced_after_array_generation(self):
        module = self.launchers._load_module(
            "0_comparacion_busquedas_app.py",
            "capitulo7_comparacion_membership_enforced_test_app",
        )
        common = self.launchers._load_module(
            "search_common.py",
            "capitulo7_search_common_membership_enforced_test",
        )
        values = [0, 4, 9, 12, 30, 45, 70, 100]

        for position in (
            common.TARGET_POSITION_START,
            common.TARGET_POSITION_END,
            common.TARGET_POSITION_MIDDLE,
            common.TARGET_POSITION_RANDOM,
        ):
            for _ in range(50):
                target = common.choose_target(values, common.TARGET_EXISTS, position)
                self.assertIn(target, values)
                state = module.create_comparison_state(
                    size=len(values),
                    values=values,
                    target_mode=module.TARGET_EXISTS,
                    target_position=position,
                )
                self.assertIn(state["target"], state["values"])

        for _ in range(50):
            target = common.choose_target(values, common.TARGET_MISSING)
            self.assertNotIn(target, values)
            state = module.create_comparison_state(
                size=len(values),
                values=values,
                target_mode=module.TARGET_MISSING,
            )
            self.assertNotIn(state["target"], state["values"])

        self.assertEqual(common.enforce_target_membership(values, 999, common.TARGET_EXISTS), values[0])
        self.assertNotIn(common.enforce_target_membership(values, values[0], common.TARGET_MISSING), values)

    def test_remaining_search_algorithms_find_and_miss(self):
        cases = [
            ([1, 2, 3, 4, 5, 6, 7, 8], 6, True),
            ([1, 2, 3, 4, 5, 6, 7, 8], 9, False),
            ([2, 5, 9, 14, 18, 27, 33, 40], 2, True),
            ([2, 5, 9, 14, 18, 27, 33, 40], 17, False),
        ]

        for name, module in self.modules.items():
            step_name = SEARCH_MODULES[name][1]
            step = getattr(module, step_name)
            for values, target, should_find in cases:
                with self.subTest(name=name, values=values, target=target):
                    kwargs = {"uniform": False} if name == "interpolacion" else {}
                    state = module.create_state(size=len(values), target=target, values=values, **kwargs)

                    for _ in range(96):
                        if state["search_complete"]:
                            break
                        step(state)

                    self.assertTrue(state["search_complete"])
                    found_nodes = [node for node in state["arr"] if node["role"] == "found"]

                    if should_find:
                        self.assertEqual(state["general_message"], module.FOUND_MESSAGE)
                        self.assertEqual(len(found_nodes), 1)
                        self.assertEqual(found_nodes[0]["value"], target)
                    else:
                        self.assertTrue(state["general_message"].startswith(module.NOT_FOUND_MESSAGE))
                        self.assertEqual(found_nodes, [])

    def test_ternary_space_complexity_is_logarithmic_in_notebooks(self):
        comparison = json.loads(
            (PROJECT_ROOT / "capitulo7" / "notebooks" / "0_comparacion_busquedas.ipynb").read_text(encoding="utf-8")
        )
        ternary = json.loads(
            (PROJECT_ROOT / "capitulo7" / "notebooks" / "6_busqueda_ternaria.ipynb").read_text(encoding="utf-8")
        )
        exercises = json.loads(
            (PROJECT_ROOT / "capitulo7" / "ejercicios_propuestos.ipynb").read_text(encoding="utf-8")
        )

        comparison_source = "\n".join("".join(cell.get("source", [])) for cell in comparison["cells"])
        ternary_source = "\n".join("".join(cell.get("source", [])) for cell in ternary["cells"])
        exercises_source = "\n".join("".join(cell.get("source", [])) for cell in exercises["cells"])

        self.assertIn("Búsqueda ternaria</td><td>Ω(1)</td><td>Θ(log n)</td><td>O(log n)</td>", comparison_source)
        self.assertNotIn("Complejidad espacial", comparison_source)
        self.assertIn('<tr><td>Caso promedio</td><td>$\\Theta(\\log_3 n)$</td><td>$\\Theta(\\log_3 n)$</td></tr>', ternary_source)
        self.assertIn('<tr><td>Peor caso</td><td>$O(\\log_3 n)$</td><td>$O(\\log_3 n)$</td></tr>', ternary_source)
        self.assertIn('<tr><td>Caso promedio</td><td>$\\Theta(\\log_3 n)$</td><td>$\\Theta(\\log_3 n)$</td></tr>', exercises_source)
        self.assertIn('<tr><td>Peor caso</td><td>$O(\\log_3 n)$</td><td>$O(\\log_3 n)$</td></tr>', exercises_source)


if __name__ == "__main__":
    unittest.main()
