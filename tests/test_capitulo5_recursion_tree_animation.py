from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[1]
    / "capitulo5"
    / "recursion_tree_animation.py"
).read_text(encoding="utf-8")


def test_bootstrap_loads_the_shared_widget_engine_in_local_and_colab_runs():
    bootstrap = (
        Path(__file__).resolve().parents[1] / "capitulo5" / "colab_bootstrap.py"
    ).read_text(encoding="utf-8")

    assert "sys.path.insert(0, project_root)" in bootstrap
    assert 'common/widget_controls.py' in bootstrap


def test_general_expression_always_keeps_symbolic_external_cost():
    from capitulo5.recursion_tree_animation import _equation_markup

    quadratic = _equation_markup(
        "division", 2, 2, "quadratic", 4, (2,), (0.5,)
    )
    zero = _equation_markup(
        "reduction", 1, 1, "zero", 4, (1,), (1,)
    )

    for markup in (quadratic, zero):
        assert "Expresión general" in markup
        assert "+f(n)" in markup
        assert r"\sum_{i=1}^{m}" in markup
        assert r"\(\displaystyle C(n)=" in markup
    assert "+n^2" not in quadratic


def test_result_expression_formats_exact_division_factors_as_fractions():
    from capitulo5.recursion_tree_animation import _expanded_equation_markup

    markup = _expanded_equation_markup(
        "division", (2, 1), (0.5, 0.75), "linear", 4
    )

    assert r"2C\left(\dfrac{n}{2}\right)" in markup
    assert r"C\left(\dfrac{3}{4}\cdot n\right)" in markup
    assert r"\(\displaystyle C(n)=\begin{cases}" in markup
    assert r"1 & \text{si } n=1" in markup
    assert r"0.5\cdot n" not in markup
    assert r"0.75\cdot n" not in markup


def test_result_expression_adds_reduction_base_case():
    from capitulo5.recursion_tree_animation import _expanded_equation_markup

    markup = _expanded_equation_markup(
        "reduction", (1, 1), (1, 2), "constant", 4
    )

    assert r"C(n)=\begin{cases}" in markup
    assert r"\text{si } n>2" in markup
    assert r"1 & \text{si } 1\leq n\leq 2" in markup


def test_result_expression_uses_selected_base_case():
    from capitulo5.recursion_tree_animation import _expanded_equation_markup

    markup = _expanded_equation_markup(
        "division", (2,), (0.5,), "linear", 4, base_value=7
    )

    assert r"7 & \text{si } n=1" in markup


def test_controls_wrap_without_horizontal_scroll():
    assert ".recursion-tree-controls{box-sizing:border-box!important;display:flex!important" in SOURCE
    assert "flex-flow:row wrap!important" in SOURCE
    assert 'width="auto", display="flex", flex_flow="row wrap"' in SOURCE
    assert 'layout=widgets.Layout(width="auto")' in SOURCE
    assert "grid_template_columns=" not in SOURCE


def test_playback_buttons_wrap_without_horizontal_scroll():
    playback_rule = SOURCE.split(".recursion-playback{", 1)[1].split("}", 1)[0]
    assert "flex-flow:row wrap!important" in playback_rule
    assert "height:auto!important" in playback_rule
    assert "overflow:visible!important" in playback_rule
    assert 'action_layout = widgets.Layout(width="auto", flex="0 0 auto")' in SOURCE


def test_level_table_rows_select_their_tree_nodes():
    assert "const row = event.target.closest('.recursion-level-table tr[data-level]')" in SOURCE
    assert '`.tree-node[data-level="${row.dataset.level}"]`' in SOURCE
    assert "row.classList.add('is-selected')" in SOURCE


def test_builder_filters_methods_by_relation_type():
    division_block = SOURCE.split("division_methods = [", 1)[1].split("]", 1)[0]
    reduction_block = SOURCE.split("reduction_methods = [", 1)[1].split("]", 1)[0]

    assert '"master"' in division_block
    assert '"characteristic"' not in division_block
    assert '"characteristic"' in reduction_block
    assert '"master"' not in reduction_block
    assert "update_method_options()" in SOURCE


def test_original_animation_uses_requested_panel_order():
    assert (
        "else [equation, configuration_panel, expanded_equation, tree_panel, level_table]"
        in SOURCE
    )
    assert "else (controls, playback)" in SOURCE
    assert "[plot_container, note] if not builder_only else []" in SOURCE
    assert "Árbol de recursión:</button>" in SOURCE


def test_all_collapsible_panel_titles_share_style_and_icon():
    assert (
        ".recursion-info-section>summary,.recursion-tree-panel-summary{" in SOURCE
    )
    assert (
        '.recursion-info-section>summary::before,.recursion-tree-panel-summary::before{'
        in SOURCE
    )
    assert 'content:"▶"' in SOURCE
    assert '<span class="recursion-panel-marker">' not in SOURCE
    assert 'aria-expanded="true">Configuración</button>' in SOURCE


def test_builder_limits_term_count_to_supported_methods():
    assert 'if not builder_only:' in SOURCE
    assert 'method.value == "characteristic"' in SOURCE
    assert 'master_flavor.value == "generalized"' in SOURCE
    assert 'control.disabled = not allows_multiple_terms' in SOURCE
    assert 'parameter_state["m"] = 1' in SOURCE
    assert 'term_count.add_class("recursion-control-disabled")' in SOURCE
    assert ".recursion-control-disabled{opacity:.5!important}" in SOURCE


def test_method_fields_leave_standard_gap_after_wider_labels():
    assert "def labeled(label, control, label_width=52, row_width=252):" in SOURCE
    assert 'min_width=f"{label_width}px"' in SOURCE
    assert 'max_width=f"{label_width}px"' in SOURCE
    assert 'min_width=f"{row_width}px"' in SOURCE
    assert 'max_width=f"{row_width}px"' in SOURCE
    assert 'row.add_class("recursion-labeled-control")' in SOURCE
    assert '"<b>Método</b>", method, label_width=96, row_width=296' in SOURCE
    assert '"<b>Versión</b>", master_flavor, label_width=96, row_width=296' in SOURCE


def test_term_count_stepper_visually_matches_parameter_text_width():
    assert 'term_count.add_class("recursion-term-count-control")' in SOURCE
    assert 'r"\\(\\boldsymbol{m}\\)", term_count, row_width=256' in SOURCE
    assert ".recursion-term-count-control{" in SOURCE
    assert "width:188px!important" in SOURCE
    assert "width:120px!important" in SOURCE
    assert ".recursion-stepper{" in SOURCE
    assert "gap:0!important" in SOURCE
    assert SOURCE.count('layout=widgets.Layout(width="188px", align_items="center", grid_gap="0px")') == 2
    assert SOURCE.count('margin="0", flex="0 0 34px"') == 4
    assert SOURCE.count('margin="0", flex="0 0 120px"') == 2
    assert "border-radius:0!important" in SOURCE
    assert "font-family:sans-serif!important;font-size:13px!important" in SOURCE
    assert "font-weight:700!important;line-height:1.1!important" in SOURCE
    assert 'term_a_input.add_class("recursion-term-value-control")' in SOURCE
    assert 'term_b_input.add_class("recursion-term-value-control")' in SOURCE
    assert ".recursion-tree-root .recursion-term-value-control{" in SOURCE


def test_polynomial_and_polylogarithmic_controls_share_parameter_width():
    assert 'polynomial_degree.add_class("recursion-parameter-value-control")' in SOURCE
    assert 'logarithmic_power.add_class("recursion-parameter-value-control")' in SOURCE
    assert 'logarithmic_base.add_class("recursion-parameter-value-control")' in SOURCE
    assert ".recursion-parameter-value-control{" in SOURCE
    assert 'r"\\(\\boldsymbol{k}\\)", polynomial_degree, row_width=256' in SOURCE


def test_polylogarithmic_function_exposes_k_p_and_ell_after_b_i():
    option = '("polylogarithmic", r"n^k\\cdot\\log_\\ell^p(n)")'
    parameter_block = SOURCE.split(
        "parameter_controls = widgets.VBox(", 1
    )[1].split("term_validation,", 1)[0]

    assert option in SOURCE
    assert parameter_block.index("term_b_control") < parameter_block.index(
        "degree_control"
    )
    assert parameter_block.index("degree_control") < parameter_block.index(
        "logarithmic_power_control"
    )
    assert parameter_block.index("logarithmic_power_control") < parameter_block.index(
        "logarithmic_base_control"
    )
    assert 'function_type.value == "polylogarithmic"' in SOURCE


def test_polylogarithmic_expression_uses_selected_parameters():
    from capitulo5.recursion_tree_animation import _expanded_equation_markup

    markup = _expanded_equation_markup(
        "division", (2,), (0.5,), "polylogarithmic", (3, 2, 5)
    )

    assert r"+n^{3}\cdot\log_{5}^{2}(n)" in markup


def test_base_case_field_is_below_function_selector():
    recurrence_controls = SOURCE.split(
        '"Relación de recurrencia:"', 1
    )[1].split("parameters_section", 1)[0]

    assert "base_case_control" in recurrence_controls
    assert 'base_case_input = widgets.Text(' in SOURCE
    assert '"<b>Tipo</b>", relation_type, label_width=96, row_width=296' in SOURCE
    assert "function_control" in recurrence_controls


def test_all_chapter_five_buttons_use_the_shared_visual_style():
    assert ".recursion-tree-root .widget-button{" in SOURCE
    assert "background:#f7f7f7!important;color:#333!important;" in SOURCE
    assert "border:1px solid #ccc!important;border-radius:0!important;" in SOURCE
    assert "box-shadow:none!important;font-family:sans-serif!important" in SOURCE
    assert ".recursion-tree-root .widget-button:hover{" in SOURCE
    assert "background:#eee!important;color:#333!important" in SOURCE


def test_master_variant_selection_does_not_import_symbolic_solver():
    variant_update = SOURCE.split(
        "def update_master_variant_options", 1
    )[1].split("def update", 1)[0]

    assert "recurrence_solution_methods" not in variant_update
    assert 'variants.append(("Básico", "basic"))' in variant_update


def test_master_function_selector_excludes_unsupported_growth_functions():
    selector_handler = SOURCE.split(
        "def select_function(delta):", 1
    )[1].split("def update_function_readout", 1)[0]
    guard_handler = SOURCE.split(
        "def prevent_unsupported_function_for_master", 1
    )[1].split("def update_term_count_availability", 1)[0]
    unsupported = '{"zero", "exponential", "factorial"}'

    assert unsupported in selector_handler
    assert unsupported in guard_handler
    assert "function_type.value = \"constant\"" in guard_handler
