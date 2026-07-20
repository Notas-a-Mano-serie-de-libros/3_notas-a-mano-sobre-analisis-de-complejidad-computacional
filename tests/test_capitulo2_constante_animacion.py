from pathlib import Path
import sys

import numpy as np


EXPERIMENT_DIR = Path(__file__).parents[1] / "capitulo2" / "analisis_complejidad_temporal_experimental"
sys.path.insert(0, str(EXPERIMENT_DIR))

from constant_animation import (  # noqa: E402
    build_experiment_sizes,
    measure_access,
    measure_access_memory,
    next_order_of_magnitude,
    previous_order_of_magnitude,
    results_table,
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


def test_rango_experimental_conserva_puntos_intermedios_y_potencias():
    sizes, checkpoints = build_experiment_sizes(10_000, points=200)

    assert len(sizes) >= 200
    assert sizes[0] == 1
    assert sizes[-1] == 10_000
    assert np.array_equal(checkpoints, [10, 100, 1_000, 10_000])
    assert set(checkpoints).issubset(set(sizes))
