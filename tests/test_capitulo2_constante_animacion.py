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
from theoretical_graphs import (  # noqa: E402
    GRAPH_STYLE,
    THEORETICAL_CONFIGS,
    align_axes_at_origin,
    maximum_safe_power,
    plot_logarithmic_slow_growth,
    theoretical_domain,
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
    source = Path(EXPERIMENT_DIR / "experimental_animation.py").read_text(encoding="utf-8")

    assert 'description="Ejecutar"' in source
    assert 'description="Reiniciar"' in source
    assert "[apply_button, reset_button]" in source
    assert "reset_button.on_click(reset_app)" in source
    assert "def schedule_task(coro):" in source
    assert "loop.create_task(coro)" in source
    assert "asyncio.run(coro)" in source
    assert "task = schedule_task(run_experiment())" in source
    assert "await asyncio.sleep(0.01)" in source


def test_simulacion_habilita_widgets_en_colab():
    source = Path(EXPERIMENT_DIR / "experimental_animation.py").read_text(encoding="utf-8")

    assert "from google.colab import output as colab_output" in source
    assert "colab_output.enable_custom_widget_manager()" in source
    assert "nest_asyncio.apply()" in source


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
    assert "theoretical_graphs.py" in source
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
    theoretical_source = Path(EXPERIMENT_DIR / "theoretical_graphs.py").read_text(encoding="utf-8")

    common_visual_style = (
        'plt.style.use("default")',
        '"figure.facecolor": "white"',
        '"axes.facecolor": "white"',
        '"savefig.facecolor": "white"',
        '"savefig.edgecolor": "white"',
        '"figure.dpi": 600',
        '"savefig.dpi": 600',
        "figsize=(8, 4)",
        "ax1.grid(True)",
    )
    saved_figure_style = (
        'bbox_inches="tight"',
        "pad_inches=0.05",
    )

    for style_line in common_visual_style:
        assert style_line in constant_source
        assert style_line in general_source
        assert style_line in theoretical_source

    for style_line in saved_figure_style:
        assert style_line in constant_source
        assert style_line in general_source


def test_graficas_teoricas_definen_todas_las_complejidades_y_limites_seguros():
    assert set(THEORETICAL_CONFIGS) == {"constant", *PROFILE_CONFIGS.keys()}
    assert GRAPH_STYLE["figure.dpi"] == 600
    assert GRAPH_STYLE["savefig.dpi"] == 600
    assert maximum_safe_power(1_000_000) == 1_000_000
    assert maximum_safe_power(20_000) == 10_000
    assert maximum_safe_power(30) == 10
    assert theoretical_domain(10).tolist() == list(range(11))


def test_graficas_teoricas_ubican_leyenda_segun_crecimiento():
    lower_right = {"constant", "logarithmic", "linear", "log_linear"}
    upper_left = {"quadratic", "cubic", "exponential", "factorial"}

    assert {name for name, config in THEORETICAL_CONFIGS.items() if config["legend_location"] == "lower right"} == lower_right
    assert {name for name, config in THEORETICAL_CONFIGS.items() if config["legend_location"] == "upper left"} == upper_left


def test_graficas_teoricas_alinean_ejes_en_el_origen():
    import matplotlib.pyplot as plt

    fig, axis = plt.subplots()
    align_axes_at_origin(axis)

    assert axis.spines["left"].get_position() == ("data", 0)
    assert axis.spines["bottom"].get_position() == ("data", 0)
    assert axis.spines["right"].get_edgecolor()[3] == 0
    assert axis.spines["top"].get_edgecolor()[3] == 0
    plt.close(fig)


def test_grafica_logaritmica_extrema_llega_hasta_10_a_la_100():
    import matplotlib.pyplot as plt

    captured = {}
    original_show = plt.show
    plt.show = lambda *args, **kwargs: None
    try:
        plot_logarithmic_slow_growth()
        axis = plt.gcf().axes[0]
        captured["xlim"] = axis.get_xlim()
        captured["ylim"] = axis.get_ylim()
        captured["tick_labels"] = [label.get_text() for label in axis.get_xticklabels()]
        captured["legend_location"] = axis.get_legend()._loc
    finally:
        plt.show = original_show
        plt.close("all")

    assert captured["xlim"][1] == 100
    assert captured["ylim"][1] > 332
    assert "$10^{100}$" in captured["tick_labels"]
    assert captured["legend_location"] == 4


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


def test_notebooks_incluyen_grafica_teorica_correcta():
    expected = {
        "1_complejidad_constante.ipynb": "constant",
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
        graph_cells = [
            "".join(cell.get("source", []))
            for cell in notebook["cells"]
            if cell["cell_type"] == "code" and "plot_theoretical_growth" in "".join(cell.get("source", []))
        ]

        assert len(graph_cells) == 1
        assert f'plot_theoretical_growth("{simulation_name}")' in graph_cells[0]
        assert "theoretical_graphs.py" in graph_cells[0]
        assert "urllib.request.urlopen" in graph_cells[0]


def test_notebook_logaritmico_explica_cambio_de_base():
    notebook = json.loads(Path(EXPERIMENT_DIR / "2_complejidad_logaritmica.ipynb").read_text(encoding="utf-8"))
    source = "".join(notebook["cells"][1].get("source", []))

    assert r"\log_\ell(n)" in source
    assert r"\log_\ell(n) = \frac{\log_b(n)}{\log_b(\ell)}" in source
    assert "misma familia logarítmica" in source
    assert "crece extremadamente lento" in source
    assert r"\log_2(10^{100}) = 100\log_2(10) \approx 332.19" in source
    assert "la siguiente mejor opción práctica suelen ser las soluciones logarítmicas" in source


def test_notebook_logaritmico_incluye_figura_hasta_10_a_la_100():
    notebook = json.loads(Path(EXPERIMENT_DIR / "2_complejidad_logaritmica.ipynb").read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

    assert "plot_logarithmic_slow_growth()" in source
    assert "Crecimiento logarítmico hasta $10^{100}$" in source


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
        expected_code_cells = 5 if notebook_name == "2_complejidad_logaritmica.ipynb" else 4
        assert len(code_cells) == expected_code_cells
        assert code_cells[0].startswith("#@title Gráfica del comportamiento teórico")
        example_cell_index = 2 if notebook_name == "2_complejidad_logaritmica.ipynb" else 1
        assert code_cells[example_cell_index].startswith("def ")
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

        if notebook_name == "2_complejidad_logaritmica.ipynb":
            assert types == [
                "markdown",
                "markdown",
                "code",
                "code",
                "markdown",
                "code",
                "markdown",
                "markdown",
                "code",
                "markdown",
                "code",
            ]
            assert headings[1] == "## Forma teórica"
            assert headings[2].startswith("#@title Gráfica del comportamiento teórico")
            assert headings[3].startswith("#@title Crecimiento logarítmico hasta")
            assert headings[4].startswith("## Ejemplo:")
            assert headings[7] == "## Simulaciones experimentales"
            assert headings[8].startswith("#@title Simulación interactiva de complejidad temporal")
            assert headings[9] == "### Complejidad espacial experimental"
            assert headings[10].startswith("#@title Simulación interactiva de complejidad espacial")
            continue

        assert types == [
            "markdown",
            "markdown",
            "code",
            "markdown",
            "code",
            "markdown",
            "markdown",
            "code",
            "markdown",
            "code",
        ]
        assert headings[1] == "## Forma teórica"
        assert headings[2].startswith("#@title Gráfica del comportamiento teórico")
        assert headings[3].startswith("## Ejemplo:")
        assert headings[6] == "## Simulaciones experimentales"
        assert headings[7].startswith("#@title Simulación interactiva de complejidad temporal")
        assert headings[8] == "### Complejidad espacial experimental"
        assert headings[9].startswith("#@title Simulación interactiva de complejidad espacial")


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
