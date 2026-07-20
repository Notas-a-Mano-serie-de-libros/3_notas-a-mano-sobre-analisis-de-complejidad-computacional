from pathlib import Path
import sys
import json

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
from experimental_animation import (  # noqa: E402
    ExperimentProfile,
    build_experiment_sizes as build_profile_sizes,
    measure_profile_point,
    pending_table_html as pending_profile_table_html,
    results_table as profile_results_table,
)
from complexity_animations import PROFILE_CONFIGS, make_profile  # noqa: E402


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
    source = Path(EXPERIMENT_DIR / "experimental_animation.py").read_text(encoding="utf-8")

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


def test_bootstrap_remoto_descarga_motor_comun_y_perfiles():
    source = Path(EXPERIMENT_DIR / "colab_bootstrap.py").read_text(encoding="utf-8")

    assert "experimental_animation.py" in source
    assert "complexity_animations.py" in source
    assert "constant_animation.py" in source
    assert "SIMULATION_NAME" in source
    assert "simulation_module = importlib.import_module(module_name)" in source
    assert "simulation_module.run_app(simulation_name" in source


def test_perfiles_generales_se_pueden_construir():
    expected_names = {"logarithmic", "linear", "log_linear", "quadratic", "cubic", "exponential", "factorial"}

    assert set(PROFILE_CONFIGS) == expected_names
    for name in expected_names:
        for mode in ("time", "memory"):
            profile = make_profile(name, mode=mode)
            assert profile.mode == mode
            assert profile.max_safe_elements >= 10
            assert profile.default_executions >= 1
            assert profile.render_result is not None
            assert profile.warning_html(10, 1, mode) == ""


def test_perfiles_generales_no_usan_teoria_constante():
    for name in PROFILE_CONFIGS:
        for mode in ("time", "memory"):
            profile = make_profile(name, mode=mode)
            assert profile.theoretical(10) != profile.theoretical(100)


def test_perfiles_generales_usan_misma_funcion_teorica_en_tiempo_y_espacio():
    for name in PROFILE_CONFIGS:
        time_profile = make_profile(name, mode="time")
        memory_profile = make_profile(name, mode="memory")

        assert np.isclose(memory_profile.theoretical(10), time_profile.theoretical(10) / 1e-6)
        assert np.isclose(memory_profile.theoretical(100), time_profile.theoretical(100) / 1e-6)


def test_perfiles_generales_usan_estilo_visual_de_constante():
    constant_source = Path(EXPERIMENT_DIR / "constant_animation.py").read_text(encoding="utf-8")
    general_source = Path(EXPERIMENT_DIR / "complexity_animations.py").read_text(encoding="utf-8")

    for style_line in (
        'plt.style.use("default")',
        '"figure.facecolor": "white"',
        '"axes.facecolor": "white"',
        '"savefig.facecolor": "white"',
        '"savefig.edgecolor": "white"',
        '"figure.dpi": 500',
        '"savefig.dpi": 500',
        "figsize=(8, 4)",
        'bbox_inches="tight"',
        "pad_inches=0.05",
        'ax1.legend(loc="upper right")',
        "ax1.grid(True)",
    ):
        assert style_line in constant_source
        assert style_line in general_source


def test_notebooks_generales_invocan_perfiles_interactivos():
    expected = {
        "2_complejidad_logaritmica.ipynb": "logarithmic",
        "3_complejidad_lineal.ipynb": "linear",
        "4_complejidad_log_lineal.ipynb": "log_linear",
        "5_complejidad_cuadratica.ipynb": "quadratic",
        "6_complejidad_cubica.ipynb": "cubic",
        "7_complejidad_exponencial.ipynb": "exponential",
        "8_complejidad_factorial.ipynb": "factorial",
    }

    for notebook_name, simulation_name in expected.items():
        notebook = json.loads(Path(EXPERIMENT_DIR / notebook_name).read_text(encoding="utf-8"))
        source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
        assert f'SIMULATION_NAME = "{simulation_name}"' in source
        assert 'SIMULATION_MODE = "time"' in source
        assert 'SIMULATION_MODE = "memory"' in source
        assert "for base in (Path.cwd(), *Path.cwd().parents)" in source
        assert 'base / "colab_bootstrap.py"' in source
        assert 'base / "capitulo2" / "analisis_complejidad_temporal_experimental"' in source
        assert "_bootstrap_path is not None" in source
        assert "colab_bootstrap.py" in source
        assert "Solo teórico" in source
        assert "Complejidad espacial experimental" in source


def test_notebooks_buscan_bootstrap_local_antes_del_remoto():
    notebooks = (
        "1_complejidad_constante.ipynb",
        "2_complejidad_logaritmica.ipynb",
        "3_complejidad_lineal.ipynb",
        "4_complejidad_log_lineal.ipynb",
        "5_complejidad_cuadratica.ipynb",
        "6_complejidad_cubica.ipynb",
        "7_complejidad_exponencial.ipynb",
        "8_complejidad_factorial.ipynb",
    )

    for notebook_name in notebooks:
        notebook = json.loads(Path(EXPERIMENT_DIR / notebook_name).read_text(encoding="utf-8"))
        simulation_cells = [
            "".join(cell.get("source", []))
            for cell in notebook["cells"]
            if cell["cell_type"] == "code" and "SIMULATION_NAME" in "".join(cell.get("source", []))
        ]

        assert len(simulation_cells) == 2
        for source in simulation_cells:
            local_lookup_position = source.index("_bootstrap_path = next(")
            remote_position = source.index("urllib.request.urlopen")

            assert local_lookup_position < remote_position
            assert "Path.cwd().parents" in source
            assert 'base / "colab_bootstrap.py"' in source


def test_notebooks_generales_no_conservan_celdas_de_imports_antiguas():
    notebooks = (
        "2_complejidad_logaritmica.ipynb",
        "3_complejidad_lineal.ipynb",
        "4_complejidad_log_lineal.ipynb",
        "5_complejidad_cuadratica.ipynb",
        "6_complejidad_cubica.ipynb",
        "7_complejidad_exponencial.ipynb",
        "8_complejidad_factorial.ipynb",
    )

    for notebook_name in notebooks:
        notebook = json.loads(Path(EXPERIMENT_DIR / notebook_name).read_text(encoding="utf-8"))
        code_cells = ["".join(cell.get("source", [])) for cell in notebook["cells"] if cell["cell_type"] == "code"]
        assert len(code_cells) == 3
        assert code_cells[0].startswith("def ")
        assert all("matplotlib.pyplot" not in cell for cell in code_cells)
        assert all("from scipy" not in cell for cell in code_cells)
        assert all("plt.rcParams" not in cell for cell in code_cells)


def test_notebooks_generales_siguen_estructura_de_constante():
    notebooks = (
        "2_complejidad_logaritmica.ipynb",
        "3_complejidad_lineal.ipynb",
        "4_complejidad_log_lineal.ipynb",
        "5_complejidad_cuadratica.ipynb",
        "6_complejidad_cubica.ipynb",
        "7_complejidad_exponencial.ipynb",
        "8_complejidad_factorial.ipynb",
    )

    for notebook_name in notebooks:
        notebook = json.loads(Path(EXPERIMENT_DIR / notebook_name).read_text(encoding="utf-8"))
        cells = notebook["cells"]
        headings = ["".join(cell.get("source", [])).strip().splitlines()[0] for cell in cells]
        types = [cell["cell_type"] for cell in cells]

        assert types == ["markdown", "markdown", "markdown", "code", "markdown", "markdown", "code", "markdown", "code"]
        assert headings[1] == "## Forma teórica"
        assert headings[2].startswith("## Ejemplo:")
        assert headings[5] == "## Simulaciones experimentales"
        assert headings[6].startswith("#@title Simulación interactiva de complejidad temporal")
        assert headings[7] == "### Complejidad espacial experimental"
        assert headings[8].startswith("#@title Simulación interactiva de complejidad espacial")


def test_rango_experimental_conserva_puntos_intermedios_y_potencias():
    sizes, checkpoints = build_experiment_sizes(10_000, points=200)

    assert len(sizes) >= 200
    assert sizes[0] == 1
    assert sizes[-1] == 10_000
    assert np.array_equal(checkpoints, [10, 100, 1_000, 10_000])
    assert set(checkpoints).issubset(set(sizes))


def test_motor_comun_respeta_limite_seguro_y_checkpoints():
    sizes, checkpoints = build_profile_sizes(10_000, max_safe_elements=1_000, points=50)

    assert sizes[-1] == 10_000
    assert checkpoints.tolist() == [10, 100, 1_000, 10_000]
    assert 10_000 in set(sizes)


def test_motor_comun_renderiza_tabla_pendiente_desde_perfil():
    profile = ExperimentProfile(
        mode="time",
        theoretical_value=1e-6,
        unit="s",
        metric="Tiempo",
        theoretical_metric="Tiempo teórico",
        max_safe_elements=1_000,
        measure=lambda n, executions: 0.0,
        render_result=lambda *args: ("", ""),
        warning_html=lambda maximum_n, executions, mode: "",
    )

    table = pending_profile_table_html(1_000, profile)

    assert table.count("Pendiente") == 3
    assert "Estado" in table
    assert "En espera" in table


def test_motor_comun_reutiliza_preparacion_por_punto():
    calls = []

    profile = ExperimentProfile(
        mode="time",
        theoretical_value=1e-6,
        unit="s",
        metric="Tiempo",
        theoretical_metric="Tiempo teórico",
        max_safe_elements=1_000,
        measure=lambda n, executions: -1,
        prepare=lambda n: {"n": n},
        measure_prepared=lambda prepared, executions: calls.append((prepared["n"], executions)) or 0.25,
        render_result=lambda *args: ("", ""),
        warning_html=lambda maximum_n, executions, mode: "",
    )

    assert measure_profile_point(profile, 100, 7) == 0.25
    assert calls == [(100, 7)]


def test_motor_comun_permite_tiempo_teorico_por_n():
    profile = ExperimentProfile(
        mode="time",
        theoretical_value=1e-6,
        theoretical=lambda n: n * 1e-6,
        unit="s",
        metric="Tiempo",
        theoretical_metric="Tiempo teórico",
        max_safe_elements=1_000,
        measure=lambda n, executions: 0.0,
        render_result=lambda *args: ("", ""),
        warning_html=lambda maximum_n, executions, mode: "",
    )

    table = profile_results_table([10, 100], [1e-7, 1e-7], profile)

    assert r"1.000000\times 10^{-5}" in table
    assert r"1.000000\times 10^{-4}" in table
