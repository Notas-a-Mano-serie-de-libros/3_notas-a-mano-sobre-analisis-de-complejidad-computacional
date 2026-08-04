import ast
from pathlib import Path

import numpy as np

from common.experimental_simulation import (
    DEFAULT_SAMPLING_POINTS,
    SimulationConfig,
    build_experiment_sizes,
    next_order_of_magnitude,
    previous_order_of_magnitude,
)
from common.widget_controls import magnitude_stepper
from common.widget_controls import (
    STANDARD_CONTROL_COLUMN_GAP,
    STANDARD_CONTROL_ROW_GAP,
    STANDARD_FIELD_WIDTH,
    STANDARD_LABEL_CONTROL_GAP,
    compact_labeled_control,
)
import ipywidgets as widgets


def test_puntos_de_muestreo_predeterminados_son_mil():
    assert DEFAULT_SAMPLING_POINTS == 1_000
    assert SimulationConfig(100).sampling_points == 1_000


def test_configuracion_normaliza_valores_fuera_de_rango():
    config = SimulationConfig(0, sampling_points=50_000, executions=0).normalized()

    assert config.maximum_n == 1
    assert config.sampling_points == 1_000
    assert config.executions == 1


def test_intervalos_pequenos_siempre_producen_muestras_validas():
    sizes, checkpoints = build_experiment_sizes(3, 3, points=30)

    np.testing.assert_array_equal(sizes, [1, 2, 3])
    assert checkpoints.size == 0


def test_muestras_son_unicas_ordenadas_y_conservan_hitos_decimales():
    sizes, checkpoints = build_experiment_sizes(1_000, 75, points=30)

    assert np.all(np.diff(sizes) > 0)
    np.testing.assert_array_equal(checkpoints, [10, 100, 1_000])
    assert 10 in sizes
    assert int(sizes[-1]) == 75
    assert np.all(sizes <= 75)


def test_navegacion_por_ordenes_de_magnitud_admite_edicion_manual():
    assert previous_order_of_magnitude(75) == 10
    assert next_order_of_magnitude(75) == 100


def test_control_visual_tiene_medidas_uniformes_y_etiquetas_accesibles():
    control = magnitude_stepper(value=30, accessible_name="Puntos de muestreo")

    assert control.container.layout.width == "188px"
    assert control.value.layout.width == "120px"
    assert control.value.layout.min_width == control.value.layout.max_width == "120px"
    assert control.value.layout.margin == "0"
    assert control.value.layout.flex == "0 0 120px"
    assert control.container.layout.grid_gap == "0px"
    assert control.container.layout.overflow == "hidden"
    assert control.previous.layout.width == control.following.layout.width == "34px"
    assert control.previous.layout.margin == control.following.layout.margin == "0"
    assert control.previous.layout.flex == control.following.layout.flex == "0 0 34px"
    assert control.previous.description == "◀"
    assert control.following.description == "▶"
    assert control.previous.icon == control.following.icon == ""
    assert "Disminuir puntos de muestreo" in control.previous.tooltip
    assert "Aumentar puntos de muestreo" in control.following.tooltip
    assert control.value.placeholder == "Puntos de muestreo"


def test_etiqueta_compartida_sigue_tipografia_del_capitulo_tres():
    group = compact_labeled_control("Máximo n", widgets.Text())
    label_html = group.children[0].value

    assert "font-family:sans-serif" in label_html
    assert "font-size:13px" in label_html
    assert "font-weight:700" in label_html
    assert "line-height:1.1" in label_html
    assert "color:#333" in label_html
    assert "standard-control-label" in group.children[0]._dom_classes
    assert group.children[0].layout.height == "32px"
    assert group.children[0].layout.display == "flex"
    assert group.children[0].layout.align_items == "center"
    assert group.children[0].layout.margin == "0"
    assert group.children[1].layout.margin == "0"
    assert group.layout.overflow == "hidden"


def test_contrato_compartido_impide_que_labels_compriman_campos():
    field = widgets.Text()
    group = compact_labeled_control(
        "Algoritmos activos",
        field,
        field_width=520,
        group_width=100,
        label_width=150,
    )

    assert STANDARD_FIELD_WIDTH == 188
    assert STANDARD_LABEL_CONTROL_GAP == 8
    assert STANDARD_CONTROL_ROW_GAP == 12
    assert STANDARD_CONTROL_COLUMN_GAP == 36
    assert group.layout.grid_gap == "8px"
    assert group.layout.width == "678px"
    assert group.layout.min_width == "678px"
    assert group.children[0].layout.flex == "0 0 150px"
    assert field.layout.flex == "0 0 520px"
    assert field.layout.min_width == field.layout.max_width == "520px"


def test_todos_los_layouts_usan_propiedades_admitidas_por_ipywidgets():
    project_root = Path(__file__).resolve().parents[1]
    valid_properties = set(widgets.Layout.class_traits())
    invalid = []

    for directory in ("common", *[f"capitulo{number}" for number in range(2, 9)]):
        for path in (project_root / directory).rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if not (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "Layout"
                ):
                    continue
                invalid.extend(
                    f"{path.relative_to(project_root)}:{node.lineno}:{keyword.arg}"
                    for keyword in node.keywords
                    if keyword.arg and keyword.arg not in valid_properties
                )

    assert invalid == []


def test_capitulos_aplican_el_estilo_canonico_al_label_efectivo():
    project_root = Path(__file__).resolve().parents[1]
    compact_label_sources = (
        "capitulo2/runtime/experimental_animation.py",
        "capitulo2/runtime/polynomial_animation.py",
        "capitulo4/runtime/experiment_ui.py",
        "core/search/search_common.py",
        "core/search/0_comparacion_busquedas_app.py",
        "core/sort/sort_common.py",
    )
    for relative_path in compact_label_sources:
        source = (project_root / relative_path).read_text(encoding="utf-8")
        assert ".compact-control-label" in source, relative_path

    recursion_source = (project_root / "capitulo5/runtime/recursion_tree_animation.py").read_text(encoding="utf-8")
    lab_source = (project_root / "capitulo6/runtime/recursive_analysis_lab.py").read_text(encoding="utf-8")
    for source in (recursion_source, lab_source):
        assert "font-family:sans-serif!important" in source
        assert "font-size:13px!important" in source
        assert "font-weight:700!important" in source
        assert "line-height:1.1!important" in source


def test_configuraciones_recursivas_no_generan_scroll_horizontal():
    project_root = Path(__file__).resolve().parents[1]
    recursion_source = (project_root / "capitulo5/runtime/recursion_tree_animation.py").read_text(encoding="utf-8")
    lab_source = (project_root / "capitulo6/runtime/recursive_analysis_lab.py").read_text(encoding="utf-8")

    assert ".recursion-tree-controls" in recursion_source
    assert "overflow-x:hidden!important" in recursion_source
    assert ".lab-parameter-controls" in lab_source
    assert "overflow-x:hidden!important" in lab_source
