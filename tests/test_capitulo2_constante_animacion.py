from pathlib import Path
import sys

import numpy as np


EXPERIMENT_DIR = Path(__file__).parents[1] / "capitulo2" / "analisis_complejidad_temporal_experimental"
sys.path.insert(0, str(EXPERIMENT_DIR))

from constant_animation import (  # noqa: E402
    DEFAULT_EXECUTIONS,
    DEFAULT_MAXIMUM_EXPONENT,
    MAX_SAFE_ELEMENTS,
    STATUS_COMPLETE,
    STATUS_LOADING,
    STATUS_PENDING,
    STATUS_SKIPPED,
    build_experiment_sizes,
    measure_access,
    measure_access_memory,
    next_order_of_magnitude,
    pending_table_html,
    previous_order_of_magnitude,
    results_table,
    results_table_widget,
    warning_html,
)


def test_medicion_constante_devuelve_un_tiempo_valido():
    elapsed = measure_access(100, 3)
    assert elapsed >= 0


def test_medicion_espacial_constante_devuelve_bytes_validos():
    measured_bytes = measure_access_memory(100, 3)
    assert measured_bytes >= 0


def test_entrada_pequena_no_muestra_advertencia():
    assert warning_html(100_000, 10) == ""


def test_entrada_muy_grande_advierte_y_explica_el_limite():
    warning = warning_html(10**7, 10)
    assert "Advertencia de recursos" in warning
    assert "medición experimental" in warning
    assert "1,000,000" in warning


def test_spinner_sube_al_siguiente_orden_de_magnitud():
    assert next_order_of_magnitude(10) == 100
    assert next_order_of_magnitude(50) == 100
    assert next_order_of_magnitude(100) == 1_000


def test_spinner_baja_al_orden_de_magnitud_anterior():
    assert previous_order_of_magnitude(100) == 10
    assert previous_order_of_magnitude(50) == 10


def test_tabla_incluye_una_fila_por_cada_potencia():
    table = results_table([10, 100], [1e-7, float("nan")])
    assert r"\(10^{1}=10\)" in table
    assert r"\(10^{2}=100\)" in table
    assert r"1.000000\times 10^{-7}" in table
    assert "Tiempo teórico [s]" in table
    assert "No ejecutado" in table


def test_tabla_espacial_usa_bytes():
    table = results_table([10], [0], mode="memory")
    assert "Memoria teórica" in table
    assert "Memoria experimental [bytes]" in table


def test_tabla_previa_muestra_todas_las_filas_como_pendientes():
    table = results_table([10, 100, 1_000], [float("nan")] * 3, pending=True)
    assert table.count("Pendiente") == 3
    assert "No ejecutado" not in table


def test_tabla_muestra_estado_en_espera_carga_y_completado():
    table = results_table(
        [10, 100, 1_000],
        [float("nan"), float("nan"), 1e-7],
        pending=True,
        statuses=[STATUS_PENDING, STATUS_LOADING, STATUS_COMPLETE],
    )

    assert "<th>Estado</th>" in table
    assert "En espera" in table
    assert "constant-loading" in table
    assert "constant-result-symbol found" in table
    assert ">✓</span>" in table


def test_tabla_muestra_solo_teorico_para_tamanos_no_ejecutados():
    table = results_table(
        [10, MAX_SAFE_ELEMENTS * 10],
        [1e-7, float("nan")],
        pending=True,
        statuses=[STATUS_COMPLETE, STATUS_SKIPPED],
    )

    assert "Solo teórico" in table
    assert r"\text{No ejecutado}" in table


def test_tabla_dinamica_usa_iframe_con_mathjax_explicito():
    import ipywidgets as widgets

    table = results_table_widget([10], [1e-7])
    assert isinstance(table, widgets.HTML)
    assert "constant-mathjax-frame" in table.value
    assert "MathJax.typesetPromise" in table.value
    assert "@keyframes constant-spin" in table.value
    assert "color:#2d7d32;" in table.value


def test_tabla_pendiente_reinicia_resultados_pendientes():
    table = pending_table_html(1_000)

    assert "constant-mathjax-frame" in table
    assert table.count("Pendiente") == 3
    assert "En espera" in table
    assert ">✓</span>" not in table


def test_simulacion_incluye_boton_reiniciar_junto_a_ejecutar():
    source = Path(EXPERIMENT_DIR / "constant_animation.py").read_text(encoding="utf-8")

    assert 'description="Ejecutar"' in source
    assert 'description="Reiniciar"' in source
    assert "[apply_button, reset_button]" in source
    assert "reset_button.on_click(reset_app)" in source
    assert "asyncio.create_task(run_experiment())" in source
    assert "await asyncio.sleep(0.01)" in source


def test_simulacion_declara_defaults_y_estados():
    assert DEFAULT_MAXIMUM_EXPONENT == 5
    assert DEFAULT_EXECUTIONS == 10
    assert STATUS_PENDING == "pending"
    assert STATUS_LOADING == "loading"
    assert STATUS_COMPLETE == "complete"
    assert STATUS_SKIPPED == "skipped"
    assert pending_table_html(10**DEFAULT_MAXIMUM_EXPONENT).count("Pendiente") == DEFAULT_MAXIMUM_EXPONENT


def test_rango_experimental_conserva_puntos_intermedios_y_potencias():
    sizes, checkpoints = build_experiment_sizes(10_000, points=200)

    assert len(sizes) >= 200
    assert sizes[0] == 1
    assert sizes[-1] == 10_000
    assert np.array_equal(checkpoints, [10, 100, 1_000, 10_000])
    assert set(checkpoints).issubset(set(sizes))
