import numpy as np

from common.experimental_simulation import (
    DEFAULT_SAMPLING_POINTS,
    SimulationConfig,
    build_experiment_sizes,
    next_order_of_magnitude,
    previous_order_of_magnitude,
)
from common.widget_controls import magnitude_stepper
from common.widget_controls import compact_labeled_control
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
