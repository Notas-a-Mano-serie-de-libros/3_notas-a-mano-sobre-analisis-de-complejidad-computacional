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
    effective_max_safe_elements,
    measure_profile_point,
    pending_table_html as pending_profile_table_html,
    profile_warning_html,
    results_table as profile_results_table,
)
from complexity_animations import PROFILE_CONFIGS, make_profile  # noqa: E402
from theoretical_graphs import (  # noqa: E402
    GRAPH_STYLE,
    THEORETICAL_CONFIGS,
    align_axes_at_origin,
    maximum_safe_power,
    plot_logarithmic_slow_growth,
    plot_polynomial_family,
    polynomial_flat_group_limit,
    polynomial_values,
    polynomial_visible_ceiling,
    polynomial_visible_exponent,
    theoretical_domain,
)
from polynomial_animation import (  # noqa: E402
    DEFAULT_MAX_DEGREE,
    DEFAULT_MAXIMUM_N,
    MAX_DEGREE,
    TABLE_MAX_DEGREE,
    polynomial_table,
    polynomial_table_height,
    render_polynomial_figure,
    scientific_latex,
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


def test_entrada_muy_grande_con_modo_forzado_no_promete_saltar_medicion():
    warning = warning_html(10**7, 10, force_full_execution=True)

    assert "Advertencia de recursos" in warning
    assert "modo forzado está activo" in warning
    assert "se intentarán medir todos" in warning
    assert "mostrarán únicamente la estimación teórica" not in warning


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


def test_simulacion_incluye_opcion_para_forzar_ejecucion_completa():
    source = Path(EXPERIMENT_DIR / "experimental_animation.py").read_text(encoding="utf-8")

    assert "force_execution = widgets.Checkbox" in source
    assert 'description="Ejecutar todos los valores"' in source
    assert "force_execution.value = False" in source
    assert "force_execution.disabled = not enabled" in source
    assert "force_execution.observe(refresh_warning" in source
    assert "effective_max_safe_elements(profile, force_execution.value)" in source
    assert "profile_warning_html(profile, maximum_n(), execution_value(), force_execution.value)" in source


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
    assert "polynomial_animation.py" in source
    assert "theoretical_graphs.py" in source
    assert "SIMULATION_NAME" in source
    assert "polynomial_general" in source
    assert "simulation_module = importlib.import_module(module_name)" in source
    assert "simulation_module.run_app(simulation_name" in source
    assert "simulation_module.run_app()" in source


def test_bootstrap_tolera_que_google_no_este_instalado():
    source = Path(EXPERIMENT_DIR / "colab_bootstrap.py").read_text(encoding="utf-8")

    assert 'find_spec("google.colab")' in source
    assert "except ModuleNotFoundError:" in source


def test_bootstrap_prioriza_simulacion_y_limpia_estado_del_kernel():
    source = Path(EXPERIMENT_DIR / "colab_bootstrap.py").read_text(encoding="utf-8")

    simulation_branch = source.index('if "SIMULATION_NAME" in globals():')
    graph_branch = source.index('elif "THEORETICAL_GRAPH" in globals():')
    assert simulation_branch < graph_branch
    assert 'globals().pop(control_name, None)' in source


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


def test_perfiles_generales_advierten_modo_forzado_sin_saltar_medicion():
    for name in PROFILE_CONFIGS:
        profile = make_profile(name, mode="time")
        warning = profile.warning_html(profile.max_safe_elements * 10, 1, "time", True)

        assert "modo forzado está activo" in warning
        assert "mostrarán únicamente la estimación teórica" not in warning


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
    polynomial_source = Path(EXPERIMENT_DIR / "polynomial_animation.py").read_text(encoding="utf-8")

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
        assert style_line in polynomial_source
    assert "plt.rcParams.update(GRAPH_STYLE)" in polynomial_source
    assert "figsize=(8, 4)" in polynomial_source
    assert "ax1.grid(True)" in polynomial_source


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


def test_valores_polinomiales_respetan_grado_cero_y_potencias():
    n_values = np.array([0, 2, 10], dtype=np.float64)

    assert polynomial_values(n_values, 0).tolist() == [1.0, 1.0, 1.0]
    assert polynomial_values(n_values, 2).tolist() == [0.0, 4.0, 100.0]


def test_grafica_polinomial_estatica_usa_k_0_a_4():
    import matplotlib.pyplot as plt

    captured = {}
    original_show = plt.show
    plt.show = lambda *args, **kwargs: None
    try:
        plot_polynomial_family(max_degree=4, maximum_n=10)
        axis = plt.gcf().axes[0]
        captured["line_count"] = len(axis.lines)
        captured["xlim"] = axis.get_xlim()
        captured["ylim"] = axis.get_ylim()
        captured["ylabel"] = axis.get_ylabel()
        captured["title"] = axis.get_title()
        captured["legend"] = axis.get_legend()
        captured["labels"] = [line.get_label() for line in axis.lines]
        captured["annotations"] = [text.get_text() for text in axis.texts]
    finally:
        plt.show = original_show
        plt.close("all")

    assert captured["line_count"] == 5
    assert captured["xlim"] == (1.0, 10.6)
    assert captured["ylim"] == (0.0, 10.0)
    assert captured["ylabel"] == "Función de complejidad teórica"
    assert captured["title"] == r"$C(n)=n^k$ para $k \in [0, 4]$"
    assert captured["legend"] is None
    assert captured["labels"] == [rf"$n^{{{degree}}}$" for degree in range(5)]
    assert captured["annotations"] == [rf"$n^{{{degree}}}$" for degree in range(5)]


def test_grafica_polinomial_agrupa_curvas_planas_para_grados_altos():
    import matplotlib.pyplot as plt

    captured = {}
    original_show = plt.show
    plt.show = lambda *args, **kwargs: None
    try:
        plot_polynomial_family(max_degree=10, maximum_n=10)
        axis = plt.gcf().axes[0]
        captured["xlim"] = axis.get_xlim()
        captured["ylim"] = axis.get_ylim()
        captured["yticks"] = axis.get_yticks()
        captured["title"] = axis.get_title()
        captured["legend"] = axis.get_legend()
        captured["annotations"] = [text.get_text() for text in axis.texts]
    finally:
        plt.show = original_show
        plt.close("all")

    assert polynomial_visible_exponent(10) == 11
    assert polynomial_visible_ceiling(10, 10) == 10**11
    assert polynomial_flat_group_limit(10) == 9
    assert captured["xlim"] == (2.0, 10.8)
    assert captured["ylim"] == (-0.05 * 10**11, 10**11)
    assert captured["yticks"][0] == 0
    assert min(captured["yticks"]) >= 0
    assert captured["title"] == r"$C(n)=n^k$ para $k \in [0, 10]$"
    assert captured["legend"] is None
    assert r"$n^{[0,9]}$" in captured["annotations"]
    assert r"$n^{9}$" not in captured["annotations"]
    assert r"$n^{10}$" in captured["annotations"]


def test_grafica_polinomial_no_superpone_grupo_con_primera_curva_visible():
    import matplotlib.pyplot as plt

    captured = {}
    original_show = plt.show
    plt.show = lambda *args, **kwargs: None
    try:
        plot_polynomial_family(max_degree=5, maximum_n=10)
        axis = plt.gcf().axes[0]
        captured["annotations"] = [text.get_text() for text in axis.texts]
    finally:
        plt.show = original_show
        plt.close("all")

    assert polynomial_visible_exponent(5) == 6
    assert polynomial_visible_ceiling(5, 10) == 10**6
    assert polynomial_flat_group_limit(5, 10) == 4
    assert r"$n^{[0,4]}$" in captured["annotations"]
    assert r"$n^{4}$" not in captured["annotations"]
    assert r"$n^{5}$" in captured["annotations"]


def test_grafica_polinomial_generaliza_salto_de_escala_mas_alla_de_diez():
    import matplotlib.pyplot as plt

    captured = {}
    original_show = plt.show
    plt.show = lambda *args, **kwargs: None
    try:
        plot_polynomial_family(max_degree=20, maximum_n=10)
        axis = plt.gcf().axes[0]
        captured["ylim"] = axis.get_ylim()
        captured["yticks"] = axis.get_yticks()
        captured["annotations"] = [text.get_text() for text in axis.texts]
    finally:
        plt.show = original_show
        plt.close("all")

    assert polynomial_visible_exponent(20) == 21
    assert polynomial_visible_ceiling(20, 10) == 10**21
    assert polynomial_flat_group_limit(20, 10) == 19
    assert captured["ylim"] == (-0.05 * 10**21, 10**21)
    assert captured["yticks"][0] == 0
    assert min(captured["yticks"]) >= 0
    assert r"$n^{[0,19]}$" in captured["annotations"]
    assert r"$n^{19}$" not in captured["annotations"]
    assert r"$n^{20}$" in captured["annotations"]


def test_grafica_polinomial_mantiene_escala_por_bloques_de_cinco_grados():
    assert [polynomial_visible_exponent(degree) for degree in range(5, 15)] == [
        6,
        6,
        6,
        6,
        6,
        11,
        11,
        11,
        11,
        11,
    ]


def test_grafica_polinomial_mantiene_labels_en_bandas_estables_dentro_del_bloque():
    import matplotlib.pyplot as plt

    captured = {}
    original_show = plt.show
    plt.show = lambda *args, **kwargs: None
    try:
        plot_polynomial_family(max_degree=7, maximum_n=10)
        axis = plt.gcf().axes[0]
        captured["positions"] = {text.get_text(): text.xy for text in axis.texts}
        captured["offsets"] = {text.get_text(): text.get_position() for text in axis.texts}
    finally:
        plt.show = original_show
        plt.close("all")

    visible_ceiling = polynomial_visible_ceiling(7, 10)
    assert captured["positions"][r"$n^{[0,4]}$"][1] == 10**4
    assert captured["offsets"][r"$n^{[0,4]}$"] == (5, 0)
    assert captured["positions"][r"$n^{5}$"][1] == 10**5
    assert captured["offsets"][r"$n^{6}$"] == (12, 0)
    assert captured["positions"][r"$n^{6}$"][1] <= visible_ceiling * 0.31
    assert captured["positions"][r"$n^{7}$"][1] <= visible_ceiling * 0.49


def test_simulacion_polinomial_teorica_no_incluye_resultados_experimentales():
    table = polynomial_table(10, 4)

    assert DEFAULT_MAXIMUM_N == 10
    assert DEFAULT_MAX_DEGREE == 4
    assert MAX_DEGREE is None
    assert "<th>Grado (k)</th>" in table
    assert "<th>Forma teórica</th>" in table
    assert r"Operaciones teóricas para \(n=10\) [adimensional]" in table
    assert r"\(n^{0}\)" in table
    assert r"\(10^{4}\)" in table
    assert "Escala equivalente" not in table
    assert "1.000000" not in table
    assert r"\times" not in table
    assert "T=" not in table
    assert "S=" not in table
    assert scientific_latex(10**10) == r"10^{10}"
    assert scientific_latex(25_000) == r"2.5\times 10^{4}"
    assert "experimental" not in table.lower()
    assert "Estado" not in table


def test_simulacion_polinomial_renderiza_una_figura_embebida():
    figure_html = render_polynomial_figure(10, 3)

    assert figure_html.startswith('<img src="data:image/png;base64,')
    assert "max-width:100%" in figure_html


def test_simulacion_polinomial_usa_stepper_no_campo_editable_para_k():
    source = Path(EXPERIMENT_DIR / "polynomial_animation.py").read_text(encoding="utf-8")

    assert "degree_down = widgets.Button" in source
    assert "degree_up = widgets.Button" in source
    assert "[degree_down, degree_value, degree_up]" in source
    assert "degree_down.on_click(decrease_degree)" in source
    assert "degree_up.on_click(increase_degree)" in source
    assert "BoundedIntText" not in source


def test_simulacion_polinomial_muestra_tabla_fija_y_actualiza_figura_automaticamente():
    source = Path(EXPERIMENT_DIR / "polynomial_animation.py").read_text(encoding="utf-8")

    assert TABLE_MAX_DEGREE == 5
    assert polynomial_table_height(5) == 308
    assert "polynomial_table_html(maximum_n, TABLE_MAX_DEGREE)" in source
    assert "def refresh" in source
    assert "figure_output.value = render_polynomial_figure(maximum_n, max_degree)" in source
    assert "refresh()" in source
    assert 'description="Aplicar"' not in source
    assert "def apply_selection" not in source
    assert "apply_button" not in source
    assert "widgets.ToggleButtons" not in source
    assert "point_table_html" not in source
    assert "range(ANIMATION_TARGET_DEGREE + 1)" not in source
    assert "threading.Thread" not in source
    assert "run_sequence_button" not in source
    assert 'description="Ejecutar desde 0 hasta 20"' not in source
    assert 'margin="18px 0 0 0"' in source
    assert 'table_container.layout.overflow_y = "hidden"' in source
    assert "[style, controls_row, table_container, figure_output]" in source


def test_notebooks_generales_invocan_perfiles_interactivos():
    expected = {
        "2_complejidad_logaritmica.ipynb": "logarithmic",
        "3_complejidad_lineal.ipynb": "linear",
        "4_complejidad_log_lineal.ipynb": "log_linear",
        "5_complejidad_cuadratica.ipynb": "quadratic",
        "6_complejidad_cubica.ipynb": "cubic",
        "8_complejidad_exponencial.ipynb": "exponential",
        "9_complejidad_factorial.ipynb": "factorial",
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
        "8_complejidad_exponencial.ipynb": "exponential",
        "9_complejidad_factorial.ipynb": "factorial",
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


def test_notebook_polinomial_general_tiene_estructura_teorica_interactiva():
    notebook = json.loads(Path(EXPERIMENT_DIR / "7_complejidad_polinomial_general.ipynb").read_text(encoding="utf-8"))
    cells = notebook["cells"]
    source = "\n".join("".join(cell.get("source", [])) for cell in cells)
    headings = ["".join(cell.get("source", [])).strip().splitlines()[0] for cell in cells]

    assert [cell["cell_type"] for cell in cells] == ["markdown", "markdown", "code", "markdown", "code"]
    assert headings[0].startswith("# Complejidad polinomial general")
    assert headings[1] == "## Forma teórica"
    assert headings[2].startswith("#@title Gráfica del comportamiento teórico")
    assert headings[3] == "## Simulación teórica interactiva"
    assert headings[4].startswith("#@title Simulación teórica interactiva")
    assert r"C(n)=n^k" in source
    assert r"k\in[0,4]" in source
    assert "plot_polynomial_family(max_degree=4, maximum_n=10)" in source
    assert 'SIMULATION_NAME = "polynomial_general"' in source
    assert "colab_bootstrap.py" in source
    assert "urllib.request.urlopen" in source
    assert "no se realizan ejecuciones experimentales" in source
    assert "El valor máximo de $n$ se mantiene fijo y de solo lectura en $10$" in source
    assert "botones laterales" in source
    assert "La tabla siempre muestra el valor teórico calculado hasta $k=5$" in source
    assert "Al cambiar el valor de $k$, la figura se actualiza automáticamente" in source
    assert "cantidad adimensional de operaciones teóricas" in source
    assert all(cell.get("outputs", []) == [] for cell in cells if cell["cell_type"] == "code")
    assert all(cell.get("execution_count") is None for cell in cells if cell["cell_type"] == "code")


def test_notebooks_buscan_bootstrap_local_antes_del_remoto():
    notebooks = (
        "1_complejidad_constante.ipynb",
        "2_complejidad_logaritmica.ipynb",
        "3_complejidad_lineal.ipynb",
        "4_complejidad_log_lineal.ipynb",
        "5_complejidad_cuadratica.ipynb",
        "6_complejidad_cubica.ipynb",
        "8_complejidad_exponencial.ipynb",
        "9_complejidad_factorial.ipynb",
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


def test_notebook_polinomial_busca_bootstrap_local_antes_del_remoto():
    notebook = json.loads(Path(EXPERIMENT_DIR / "7_complejidad_polinomial_general.ipynb").read_text(encoding="utf-8"))
    simulation_cells = [
        "".join(cell.get("source", [])) for cell in notebook["cells"] if cell["cell_type"] == "code" and "SIMULATION_NAME" in "".join(cell.get("source", []))
    ]

    assert len(simulation_cells) == 1
    source = simulation_cells[0]
    assert source.index("_bootstrap_path = next(") < source.index("urllib.request.urlopen")
    assert "Path.cwd().parents" in source
    assert 'base / "colab_bootstrap.py"' in source


def test_referencias_colab_del_capitulo_2_siguen_orden_actual():
    abrir_source = Path(Path(__file__).parents[1] / "abrir.py").read_text(encoding="utf-8")
    readme_source = Path(EXPERIMENT_DIR / "README.md").read_text(encoding="utf-8")
    chapter_readme_source = Path(Path(__file__).parents[1] / "capitulo2" / "README.md").read_text(encoding="utf-8")

    expected_paths = (
        "1_complejidad_constante.ipynb",
        "2_complejidad_logaritmica.ipynb",
        "3_complejidad_lineal.ipynb",
        "4_complejidad_log_lineal.ipynb",
        "5_complejidad_cuadratica.ipynb",
        "6_complejidad_cubica.ipynb",
        "7_complejidad_polinomial_general.ipynb",
        "8_complejidad_exponencial.ipynb",
        "9_complejidad_factorial.ipynb",
    )

    for path in expected_paths:
        assert path in readme_source
        assert path in chapter_readme_source

    assert '"2/polinomial-general"' in abrir_source
    assert "7_complejidad_polinomial_general.ipynb" in abrir_source
    assert r"\newcommand{\colabComplejidadPolinomialGeneral}" in readme_source
    assert "7_complejidad_exponencial.ipynb" not in readme_source + chapter_readme_source + abrir_source
    assert "8_complejidad_factorial.ipynb" not in readme_source + chapter_readme_source + abrir_source


def test_notebooks_generales_no_conservan_celdas_de_imports_antiguas():
    notebooks = (
        "2_complejidad_logaritmica.ipynb",
        "3_complejidad_lineal.ipynb",
        "4_complejidad_log_lineal.ipynb",
        "5_complejidad_cuadratica.ipynb",
        "6_complejidad_cubica.ipynb",
        "8_complejidad_exponencial.ipynb",
        "9_complejidad_factorial.ipynb",
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
        "8_complejidad_exponencial.ipynb",
        "9_complejidad_factorial.ipynb",
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


def test_motor_comun_permite_saltar_limite_seguro_bajo_demanda():
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

    assert effective_max_safe_elements(profile) == 1_000
    assert effective_max_safe_elements(profile, force_full_execution=True) == 10**10


def test_motor_comun_mantiene_compatibilidad_con_advertencias_de_tres_argumentos():
    profile = ExperimentProfile(
        mode="time",
        theoretical_value=1e-6,
        unit="s",
        metric="Tiempo",
        theoretical_metric="Tiempo teórico",
        max_safe_elements=1_000,
        measure=lambda n, executions: 0.0,
        render_result=lambda *args: ("", ""),
        warning_html=lambda maximum_n, executions, mode: f"{maximum_n}-{executions}-{mode}",
    )

    assert profile_warning_html(profile, 100, 7, force_full_execution=True) == "100-7-time"


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
