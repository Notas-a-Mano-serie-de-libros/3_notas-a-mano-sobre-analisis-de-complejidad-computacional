from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source(relative_path):
    return (ROOT / relative_path).read_text(encoding="utf-8")


def test_shared_widget_control_grids_wrap_at_natural_width():
    controls = source("common/widget_controls.py")
    charts = source("common/chart_runtime.py")
    for module_source in (controls, charts):
        assert "widgets.Box(" in module_source
        assert 'width="auto"' in module_source
        assert 'display="flex"' in module_source
        assert 'flex_flow="row wrap"' in module_source
    assert 'layout=widgets.Layout(width=width, flex=f"0 0 {width}"' in controls


def test_chapters_two_and_four_parameter_panels_use_aligned_columns():
    paths = (
        "capitulo2/analisis_complejidad_temporal_experimental/experimental_animation.py",
        "capitulo4/experiment_ui.py",
    )
    for path in paths:
        module_source = source(path)
        assert "widgets.Box(" in module_source
        assert 'width="auto"' in module_source
        assert 'flex_flow="column nowrap"' in module_source
        assert "flex-flow: column nowrap !important" in module_source
        assert "width: 346px !important" in module_source

    polynomial_source = source(
        "capitulo2/analisis_complejidad_temporal_experimental/polynomial_animation.py"
    )
    assert 'flex_flow="row wrap"' in polynomial_source


def test_chapter_three_control_sections_use_flex_wrap():
    module_source = source("capitulo3/asymptotic_animation.py")
    controls_rule = module_source.split("#bo-wrap .controls-grid{", 1)[1].split("}", 1)[0]
    assert "display:flex" in controls_rule
    assert "flex-flow:row wrap" in controls_rule
    assert "grid-template-columns" not in controls_rule


def test_search_and_sort_control_families_wrap_without_fixed_grids():
    paths = (
        "capitulo7/domain/search_common.py",
        "capitulo7/domain/0_comparacion_busquedas_app.py",
        "capitulo8/domain/sort_common.py",
        "capitulo8/domain/0_comparacion_ordenamientos_app.py",
        "capitulo8/domain/4_ordenamiento_shell_app.py",
    )
    for path in paths:
        module_source = source(path)
        assert 'flex_flow="row wrap"' in module_source or "flex-flow:row wrap" in module_source
