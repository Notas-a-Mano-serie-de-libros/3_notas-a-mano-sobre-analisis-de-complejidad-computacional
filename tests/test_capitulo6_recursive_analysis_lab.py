from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "capitulo6"
    / "recursive_analysis_lab.py"
).read_text(encoding="utf-8")


def test_recursive_lab_supports_requested_analysis_examples():
    from capitulo6.recursive_analysis_lab import ALGORITHMS

    assert set(ALGORITHMS) == {
        "factorial", "fibonacci", "power_simple", "power_fast"
    }


def test_fibonacci_trace_distinguishes_total_calls_from_stack_depth():
    from capitulo6.recursive_analysis_lab import build_trace

    nodes, events = build_trace("fibonacci", 5)
    maximum_depth = max(len(event["stack"]) for event in events)

    assert len(nodes) == 15
    assert maximum_depth == 5
    assert len(nodes) > maximum_depth


def test_fast_power_halves_the_argument_until_base_case():
    from capitulo6.recursive_analysis_lab import build_trace

    nodes, _ = build_trace("power_fast", 16)

    assert [node.n for node in nodes] == [16, 8, 4, 2, 1, 0]


def test_call_stack_places_original_problem_at_the_base_and_returns_in_reverse():
    from capitulo6.recursive_analysis_lab import _call_stack_panel, build_trace

    nodes, events = build_trace("factorial", 3)
    base_return_step = next(
        index
        for index, event in enumerate(events)
        if event["kind"] == "return" and nodes[event["node"]].n == 1
    )
    markup = _call_stack_panel("factorial", nodes, events, base_return_step)

    assert markup.index("f(1)=1") < markup.index(r"f(2)=2\cdot 1")
    assert markup.index(r"f(2)=2\cdot 1") < markup.index("f(3)=3")
    assert "Caso base · retorna" in markup
    assert "Orden de desapilado" not in markup


def test_lab_explains_temporal_and_spatial_recurrences():
    assert 'symbol = "T" if analysis_type == "temporal" else "S"' in SOURCE
    assert 'data[\'space\']' in SOURCE
    assert "Expresión de complejidad por casos" in SOURCE
    assert "Pila de llamadas" in SOURCE
    assert "Orden de desapilado" not in SOURCE


def test_cost_expression_uses_base_and_recursive_cases():
    from capitulo6.recursive_analysis_lab import _cost_expression

    factorial = _cost_expression("factorial", "temporal")
    fibonacci_space = _cost_expression("fibonacci", "espacial")

    assert r"T(n)=\begin{cases}" in factorial
    assert r"\text{si } n\leq 1" in factorial
    assert r"T(n-1)+\Theta(1)" in factorial
    assert r"S(n)=\begin{cases}" in fibonacci_space
    assert r"\max\{S(n-1),S(n-2)\}+\Theta(1)" in fibonacci_space


def test_lab_uses_editable_input_right_aligned_actions_and_collapsible_panels():
    assert "widgets.BoundedIntText" in SOURCE
    assert 'description="Paso:"' not in SOURCE
    assert 'add_class("lab-actions")' in SOURCE
    assert '<details class="lab-section' in SOURCE
    assert "lab-analysis-step" in SOURCE
    assert '("Temporal", "temporal")' in SOURCE
    assert '("Espacial", "espacial")' in SOURCE
    assert 'labeled("Algoritmo", algorithm)' in SOURCE
    assert 'labeled("Análisis", analysis_type)' in SOURCE
    assert 'labeled("Lenguaje", language)' in SOURCE
    assert SOURCE.count('layout=widgets.Layout(width="176px", height="32px")') == 4
    assert "Resultado del análisis" not in SOURCE
    assert 'description="Configuración"' in SOURCE
    assert 'add_class("lab-configuration-summary")' in SOURCE
    assert "Laboratorio de análisis recursivo" not in SOURCE
    assert '<div class="lab-analysis-step">' in SOURCE
    assert "lab-analysis-step-title" in SOURCE
    assert "lab-analysis-step-solution" in SOURCE
    assert "disabled=True" in SOURCE
    assert 'description="Reproducir"' in SOURCE
    assert "async def play_process" in SOURCE
    assert "[analysis_controls, input_controls]" in SOURCE
    assert ".recursive-analysis-lab .widget-box," not in SOURCE
    assert 'controls = widgets.VBox(' in SOURCE
    assert 'add_class("lab-parameter-controls")' in SOURCE
    assert "justify-content:flex-end!important" in SOURCE


def test_lab_provides_four_syntax_highlighted_languages():
    from capitulo6.recursive_analysis_lab import CODE_SNIPPETS, _highlight_code_line

    assert set(CODE_SNIPPETS) == {"pseudocode", "python", "java", "c"}
    assert '<span class="k">' in _highlight_code_line("def factorial(n):", "python")
    assert '<span class="k">' in _highlight_code_line("si n ≤ 1: retornar 1", "pseudocode")


def test_code_snippets_use_standard_multiline_indentation():
    from capitulo6.recursive_analysis_lab import CODE_SNIPPETS

    for language in CODE_SNIPPETS.values():
        for lines in language.values():
            assert all("if " not in line or "return " not in line for line in lines)
            assert any(line.startswith("    ") for line in lines[1:])
            assert any(line.startswith("        ") for line in lines[1:])


def test_code_panel_uses_content_driven_height_without_vertical_scroll():
    assert ".lab-code-panel[open] .lab-code{height:auto;min-height:0}" in SOURCE
    assert "overflow-x:auto;overflow-y:hidden" in SOURCE
    assert ".lab-code{height:244px" not in SOURCE


def test_recursion_tree_uses_arrows_and_only_marks_base_cases():
    from capitulo6.recursive_analysis_lab import _tree_svg, build_trace

    nodes, events = build_trace("factorial", 3)
    base_enter = next(
        index for index, event in enumerate(events)
        if event["kind"] == "enter" and nodes[event["node"]].n == 1
    )
    base_return = base_enter + 1

    entering_markup = _tree_svg(nodes, events, base_enter)
    returning_markup = _tree_svg(nodes, events, base_return)

    assert 'marker-end="url(#lab-arrow-head)"' in entering_markup
    assert 'class="lab-node base"' in entering_markup
    assert "lab-node active" not in entering_markup
    assert entering_markup == returning_markup


def test_execution_state_precedes_stack_and_tree_panels():
    assert SOURCE.index("Estado de la ejecución") < SOURCE.index("Pila de recursión")


def test_code_panel_identifies_the_selected_language_with_a_logo():
    from capitulo6.recursive_analysis_lab import LANGUAGE_LOGOS, _language_logo

    assert set(LANGUAGE_LOGOS) == {"python", "java", "c"}
    assert "python-original.svg" in _language_logo("python")
    assert "java-original.svg" in _language_logo("java")
    assert "C1stEdition.svg" in _language_logo("c")
    assert _language_logo("pseudocode") == ""
    assert 'class="lab-code-summary"' in SOURCE


def test_code_panel_uses_white_background_and_numbered_gutter():
    from capitulo6.recursive_analysis_lab import _code_panel

    markup = _code_panel("factorial", "python", False)

    assert 'class="lab-line-number">1</span>' in markup
    assert 'class="lab-line-number">4</span>' in markup
    assert "grid-template-columns:42px" in SOURCE
    assert ".lab-code{height:auto;min-height:0;padding:0" in SOURCE
    assert "justify-content:center" in SOURCE
    assert "font-weight:700;user-select:none" in SOURCE
    assert "lab-code-python" not in markup
    assert "background:rgb(20%,60%,35%)" not in SOURCE


def test_code_panel_header_has_fixed_height_for_every_logo():
    assert "height:44px!important;min-height:44px!important;max-height:44px!important" in SOURCE


def test_chapter_six_reference_notebooks_are_separated():
    root = Path(__file__).resolve().parents[1] / "capitulo6"

    assert not (root / "ejemplo_recursion.ipynb").exists()
    assert not (root / "comparacion_fibonacci.ipynb").exists()
    assert (root / "referencias" / "ejemplo_recursion.ipynb").exists()
    assert (root / "referencias" / "comparacion_fibonacci.ipynb").exists()
