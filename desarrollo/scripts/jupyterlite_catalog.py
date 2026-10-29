"""Catálogo canónico de notebooks, runtimes y perfiles de JupyterLite."""

from __future__ import annotations

from pathlib import Path


def _chapter_paths(chapter: int, *names: str) -> tuple[Path, ...]:
    return tuple(Path(f"simulaciones/capitulo{chapter}/{name}") for name in names)


CHAPTER_CONFIGS = {
    2: {
        "notebooks": _chapter_paths(
            2,
            "notebooks/1_complejidad_constante.ipynb",
            "notebooks/2_complejidad_logaritmica.ipynb",
            "notebooks/3_complejidad_lineal.ipynb",
            "notebooks/4_complejidad_log_lineal.ipynb",
            "notebooks/5_complejidad_cuadratica.ipynb",
            "notebooks/6_complejidad_cubica.ipynb",
            "notebooks/7_complejidad_polinomial_general.ipynb",
            "notebooks/8_complejidad_exponencial.ipynb",
            "notebooks/9_complejidad_factorial.ipynb",
            "notebooks/0_comparacion_crecimiento.ipynb",
            "notebooks/10_calculo_complejidad_canonica.ipynb",
        ),
        "runtime_files": tuple(
            Path(path)
            for path in (
                "common/__init__.py",
                "common/animation_runtime.py",
                "common/experimental_simulation.py",
                "common/graphics.py",
                "common/widget_controls.py",
                "common/remote_fetch.py",
                "common/simulation_views.py",
                "simulaciones/capitulo2/runtime/experimental_animation.py",
                "simulaciones/capitulo2/runtime/constant_animation.py",
                "simulaciones/capitulo2/runtime/complexity_animations.py",
                "simulaciones/capitulo2/runtime/theoretical_graphs.py",
                "simulaciones/capitulo2/runtime/polynomial_animation.py",
                "simulaciones/capitulo2/runtime/growth_comparison.py",
                "simulaciones/capitulo2/runtime/canonical_complexity.py",
                "simulaciones/capitulo2/runtime/colab_bootstrap.py",
            )
        ),
        "packages": ("matplotlib", "numpy"),
    },
    3: {
        "notebooks": _chapter_paths(
            3,
            "notebooks/0_comparacion_notaciones_asintoticas.ipynb",
            "notebooks/1_notacion_big_o.ipynb",
            "notebooks/2_notacion_little_o.ipynb",
            "notebooks/3_notacion_big_omega.ipynb",
            "notebooks/4_notacion_little_omega.ipynb",
            "notebooks/5_notacion_theta.ipynb",
        ),
        "runtime_files": _chapter_paths(
            3,
            "runtime/asymptotic_bootstrap.py",
            "runtime/asymptotic_animation.py",
        ),
        "packages": ("matplotlib", "numpy", "scipy"),
    },
    4: {
        "notebooks": _chapter_paths(
            4,
            "notebooks/ejemplo1_(sumar_numeros).ipynb",
            "notebooks/ejemplo2_(imprimir_elementos_arreglo).ipynb",
            "notebooks/ejemplo3_(imprimir_elementos_matriz).ipynb",
            "notebooks/ejemplo4_(inicializar_matriz_variable).ipynb",
            "notebooks/ejemplo5_(ciclos_incremento_no_lineal).ipynb",
            "notebooks/ejemplo7_(ciclo_sin_dependencia).ipynb",
            "notebooks/ejemplo9_(complejidad_oculta).ipynb",
        ),
        "runtime_files": tuple(
            Path(f"common/{name}")
            for name in (
                "__init__.py",
                "animation_runtime.py",
                "chart_runtime.py",
                "exercise_laboratory.py",
                "experimental_simulation.py",
                "graphics.py",
                "plot_style.py",
                "remote_fetch.py",
                "simulation_views.py",
                "visual_roles.py",
                "widget_controls.py",
            )
        )
        + tuple(
            Path(f"simulaciones/capitulo4/runtime/{name}")
            for name in (
                "__init__.py",
                "colab_bootstrap.py",
                "experiment_ui.py",
                "experimental_analysis.py",
                "util.py",
            )
        ),
        "packages": ("matplotlib", "numpy"),
    },
    5: {
        "notebooks": _chapter_paths(
            5,
            "notebooks/0_arboles_recursion.ipynb",
            "notebooks/1_metodos_solucion_relaciones_recurrencia.ipynb",
        ),
        "runtime_files": tuple(
            Path(f"common/{name}")
            for name in (
                "__init__.py",
                "animation_runtime.py",
                "chart_runtime.py",
                "exercise_laboratory.py",
                "experimental_simulation.py",
                "graphics.py",
                "plot_style.py",
                "remote_fetch.py",
                "simulation_views.py",
                "visual_roles.py",
                "widget_controls.py",
            )
        )
        + tuple(
            Path(f"simulaciones/capitulo5/runtime/{name}")
            for name in (
                "__init__.py",
                "colab_bootstrap.py",
                "recurrence_solution_methods.py",
                "recursion_tree_animation.py",
            )
        ),
        "packages": ("numpy", "sympy"),
    },
    6: {
        "notebooks": _chapter_paths(
            6,
            "notebooks/0_laboratorio_analisis_recursivo.ipynb",
            "notebooks/comparacion_fibonacci.ipynb",
            "notebooks/ejemplo_recursion.ipynb",
        ),
        "runtime_files": tuple(
            Path(f"common/{name}")
            for name in (
                "__init__.py",
                "animation_runtime.py",
                "chart_runtime.py",
                "exercise_laboratory.py",
                "experimental_simulation.py",
                "graphics.py",
                "plot_style.py",
                "remote_fetch.py",
                "simulation_views.py",
                "visual_roles.py",
                "widget_controls.py",
            )
        )
        + tuple(
            Path(f"simulaciones/capitulo6/runtime/{name}")
            for name in (
                "__init__.py",
                "colab_bootstrap.py",
                "examples_bootstrap.py",
                "recursive_analysis_lab.py",
                "recursive_examples_analysis.py",
            )
        )
        + tuple(
            Path(f"simulaciones/capitulo4/runtime/{name}")
            for name in (
                "__init__.py",
                "colab_bootstrap.py",
                "experiment_ui.py",
                "experimental_analysis.py",
                "util.py",
            )
        ),
        "packages": ("matplotlib", "numpy"),
    },
    7: {
        "notebooks": _chapter_paths(
            7,
            "notebooks/0_comparacion_busquedas.ipynb",
            "notebooks/1_busqueda_secuencial.ipynb",
            "notebooks/2_busqueda_binaria.ipynb",
            "notebooks/3_busqueda_interpolacion.ipynb",
            "notebooks/4_busqueda_saltos.ipynb",
            "notebooks/5_busqueda_exponencial.ipynb",
            "notebooks/6_busqueda_ternaria.ipynb",
            "notebooks/ejercicios_propuestos.ipynb",
        ),
        "runtime_files": tuple(
            Path(f"common/{name}")
            for name in (
                "__init__.py",
                "animation_runtime.py",
                "case_analysis.py",
                "chart_runtime.py",
                "desk_check.py",
                "exercise_laboratory.py",
                "experimental_simulation.py",
                "graphics.py",
                "plot_style.py",
                "remote_fetch.py",
                "simulation_views.py",
                "visual_roles.py",
                "widget_controls.py",
            )
        )
        + tuple(
            Path(path)
            for path in (
                "core/__init__.py",
                "core/search/__init__.py",
                "core/search/search_common.py",
                "core/search/0_comparacion_busquedas_app.py",
                "core/search/1_busqueda_secuencial_app.py",
                "core/search/2_busqueda_binaria_app.py",
                "core/search/3_busqueda_interpolacion_app.py",
                "core/search/4_busqueda_saltos_app.py",
                "core/search/5_busqueda_exponencial_app.py",
                "core/search/6_busqueda_ternaria_app.py",
                "core/search/busquedas_chart.py",
                "core/search/interpolation_visual.py",
                "core/search/search_metrics.py",
                "simulaciones/capitulo2/runtime/experimental_animation.py",
                "simulaciones/capitulo7/runtime/__init__.py",
                "simulaciones/capitulo7/runtime/abrir_busqueda.py",
                "simulaciones/capitulo7/runtime/colab_bootstrap.py",
                "simulaciones/capitulo7/runtime/exercises_lab.py",
                "simulaciones/capitulo7/runtime/launchers.py",
            )
        ),
        "packages": ("matplotlib", "numpy", "scipy", "sympy"),
    },
    8: {
        "notebooks": _chapter_paths(
            8,
            "notebooks/0_comparacion_ordenamientos.ipynb",
            "notebooks/1_ordenamiento_burbuja.ipynb",
            "notebooks/2_ordenamiento_seleccion.ipynb",
            "notebooks/3_ordenamiento_insercion.ipynb",
            "notebooks/4_ordenamiento_shell.ipynb",
            "notebooks/5_ordenamiento_mezcla.ipynb",
            "notebooks/6_ordenamiento_rapido.ipynb",
            "notebooks/7_ordenamiento_radix.ipynb",
            "notebooks/ejercicios_propuestos.ipynb",
        ),
        "runtime_files": tuple(
            Path(f"common/{name}")
            for name in (
                "__init__.py",
                "animation_runtime.py",
                "case_analysis.py",
                "chart_runtime.py",
                "desk_check.py",
                "exercise_laboratory.py",
                "experimental_simulation.py",
                "graphics.py",
                "plot_style.py",
                "remote_fetch.py",
                "simulation_views.py",
                "visual_roles.py",
                "widget_controls.py",
            )
        )
        + tuple(
            Path(path)
            for path in (
                "core/__init__.py",
                "core/sort/__init__.py",
                "core/sort/sort_config.py",
                "core/sort/sort_messages.py",
                "core/sort/sort_algorithms.py",
                "core/sort/sort_tree.py",
                "core/sort/sort_common.py",
                "core/sort/variant_comparison.py",
                "core/sort/0_comparacion_ordenamientos_app.py",
                "core/sort/1_ordenamiento_burbuja_app.py",
                "core/sort/2_ordenamiento_seleccion_app.py",
                "core/sort/3_ordenamiento_insercion_app.py",
                "core/sort/4_ordenamiento_shell_app.py",
                "core/sort/5_ordenamiento_mezcla_app.py",
                "core/sort/6_ordenamiento_rapido_app.py",
                "core/sort/7_ordenamiento_radix_app.py",
                "core/sort/ordenamientos_chart.py",
                "core/sort/sort_metrics.py",
                "simulaciones/capitulo8/runtime/__init__.py",
                "simulaciones/capitulo8/runtime/colab_bootstrap.py",
                "simulaciones/capitulo8/runtime/exercises_lab.py",
                "simulaciones/capitulo8/runtime/launchers.py",
            )
        ),
        "packages": ("matplotlib", "numpy"),
    },
}

PAGE_NOTEBOOKS = {
    (2, "__chapter__"): _chapter_paths(
        2,
        "notebooks/0_comparacion_crecimiento.ipynb",
        "notebooks/10_calculo_complejidad_canonica.ipynb",
    ),
    (2, "0-complejidad-sublineal"): _chapter_paths(2, "notebooks/2_complejidad_logaritmica.ipynb"),
    (2, "1-complejidad-constante"): _chapter_paths(2, "notebooks/1_complejidad_constante.ipynb"),
    (2, "2-complejidad-logaritmica"): _chapter_paths(2, "notebooks/2_complejidad_logaritmica.ipynb"),
    (2, "3-complejidad-lineal"): _chapter_paths(2, "notebooks/3_complejidad_lineal.ipynb"),
    (2, "4-complejidad-log-lineal"): _chapter_paths(2, "notebooks/4_complejidad_log_lineal.ipynb"),
    (2, "5-complejidad-cuadratica"): _chapter_paths(2, "notebooks/5_complejidad_cuadratica.ipynb"),
    (2, "6-complejidad-cubica"): _chapter_paths(2, "notebooks/6_complejidad_cubica.ipynb"),
    (2, "7-complejidad-polinomial-general"): _chapter_paths(2, "notebooks/7_complejidad_polinomial_general.ipynb"),
    (2, "8-complejidad-exponencial"): _chapter_paths(2, "notebooks/8_complejidad_exponencial.ipynb"),
    (2, "9-complejidad-factorial"): _chapter_paths(2, "notebooks/9_complejidad_factorial.ipynb"),
    (3, "0-comparacion-notaciones-asintoticas"): _chapter_paths(3, "notebooks/0_comparacion_notaciones_asintoticas.ipynb"),
    (3, "1-notacion-big-o"): _chapter_paths(3, "notebooks/1_notacion_big_o.ipynb"),
    (3, "2-notacion-little-o"): _chapter_paths(3, "notebooks/2_notacion_little_o.ipynb"),
    (3, "3-notacion-big-omega"): _chapter_paths(3, "notebooks/3_notacion_big_omega.ipynb"),
    (3, "4-notacion-little-omega"): _chapter_paths(3, "notebooks/4_notacion_little_omega.ipynb"),
    (3, "5-notacion-theta"): _chapter_paths(3, "notebooks/5_notacion_theta.ipynb"),
    (4, "ejemplo1-sumar-numeros"): _chapter_paths(4, "notebooks/ejemplo1_(sumar_numeros).ipynb"),
    (4, "ejemplo2-imprimir-elementos-arreglo"): _chapter_paths(4, "notebooks/ejemplo2_(imprimir_elementos_arreglo).ipynb"),
    (4, "ejemplo3-imprimir-elementos-matriz"): _chapter_paths(4, "notebooks/ejemplo3_(imprimir_elementos_matriz).ipynb"),
    (4, "ejemplo4-inicializar-matriz-variable"): _chapter_paths(4, "notebooks/ejemplo4_(inicializar_matriz_variable).ipynb"),
    (4, "ejemplo5-ciclos-incremento-no-lineal"): _chapter_paths(4, "notebooks/ejemplo5_(ciclos_incremento_no_lineal).ipynb"),
    (4, "ejemplo7-ciclo-sin-dependencia"): _chapter_paths(4, "notebooks/ejemplo7_(ciclo_sin_dependencia).ipynb"),
    (4, "ejemplo9-complejidad-oculta"): _chapter_paths(4, "notebooks/ejemplo9_(complejidad_oculta).ipynb"),
    (5, "formas-de-recurrencia"): _chapter_paths(5, "notebooks/0_arboles_recursion.ipynb"),
    (5, "solucion-relaciones-recurrencia"): _chapter_paths(5, "notebooks/1_metodos_solucion_relaciones_recurrencia.ipynb"),
    (6, "__chapter__"): _chapter_paths(6, "notebooks/0_laboratorio_analisis_recursivo.ipynb"),
    (6, "fibonacci"): _chapter_paths(
        6,
        "notebooks/comparacion_fibonacci.ipynb",
        "notebooks/ejemplo_recursion.ipynb",
    ),
    (7, "1-busqueda-secuencial"): _chapter_paths(7, "notebooks/1_busqueda_secuencial.ipynb"),
    (7, "2-busqueda-binaria"): _chapter_paths(7, "notebooks/2_busqueda_binaria.ipynb"),
    (7, "3-busqueda-interpolacion"): _chapter_paths(7, "notebooks/3_busqueda_interpolacion.ipynb"),
    (7, "4-busqueda-saltos"): _chapter_paths(7, "notebooks/4_busqueda_saltos.ipynb"),
    (7, "5-busqueda-exponencial"): _chapter_paths(7, "notebooks/5_busqueda_exponencial.ipynb"),
    (7, "6-busqueda-ternaria"): _chapter_paths(7, "notebooks/6_busqueda_ternaria.ipynb"),
    (7, "ejercicios-propuestos"): _chapter_paths(7, "notebooks/ejercicios_propuestos.ipynb"),
    (8, "1-ordenamiento-burbuja"): _chapter_paths(8, "notebooks/1_ordenamiento_burbuja.ipynb"),
    (8, "2-ordenamiento-seleccion"): _chapter_paths(8, "notebooks/2_ordenamiento_seleccion.ipynb"),
    (8, "3-ordenamiento-insercion"): _chapter_paths(8, "notebooks/3_ordenamiento_insercion.ipynb"),
    (8, "4-ordenamiento-shell"): _chapter_paths(8, "notebooks/4_ordenamiento_shell.ipynb"),
    (8, "5-ordenamiento-mezcla"): _chapter_paths(8, "notebooks/5_ordenamiento_mezcla.ipynb"),
    (8, "6-ordenamiento-rapido"): _chapter_paths(8, "notebooks/6_ordenamiento_rapido.ipynb"),
    (8, "7-ordenamiento-radix"): _chapter_paths(8, "notebooks/7_ordenamiento_radix.ipynb"),
    (8, "ejercicios-propuestos"): _chapter_paths(8, "notebooks/ejercicios_propuestos.ipynb"),
}

PACKAGE_PROFILES = {
    ("matplotlib", "numpy"): "graficas",
    ("matplotlib", "numpy", "scipy"): "graficas-cientificas",
    ("numpy", "sympy"): "algebra-simbolica",
    ("matplotlib", "numpy", "scipy", "sympy"): "analisis-completo",
}

CHAPTER_PROFILES = {
    chapter: PACKAGE_PROFILES[config["packages"]]
    for chapter, config in CHAPTER_CONFIGS.items()
}

PROFILE_CONFIGS = {
    profile: {
        "chapters": tuple(
            chapter for chapter, name in CHAPTER_PROFILES.items() if name == profile
        ),
        "packages": packages,
        "notebooks": tuple(
            dict.fromkeys(
                notebook
                for chapter, name in CHAPTER_PROFILES.items()
                if name == profile
                for notebook in CHAPTER_CONFIGS[chapter]["notebooks"]
            )
        ),
        "runtime_files": tuple(
            dict.fromkeys(
                runtime
                for chapter, name in CHAPTER_PROFILES.items()
                if name == profile
                for runtime in CHAPTER_CONFIGS[chapter]["runtime_files"]
            )
        ),
    }
    for packages, profile in PACKAGE_PROFILES.items()
}


def chapter_content_files(chapter: int) -> tuple[Path, ...]:
    if chapter not in CHAPTER_CONFIGS:
        raise ValueError(f"No hay un demo JupyterLite configurado para el capítulo {chapter}")
    config = CHAPTER_CONFIGS[chapter]
    return (*config["notebooks"], *config["runtime_files"])


def profile_content_files(profile: str) -> tuple[Path, ...]:
    if profile not in PROFILE_CONFIGS:
        raise ValueError(f"No hay un perfil JupyterLite configurado: {profile}")
    config = PROFILE_CONFIGS[profile]
    return (*config["notebooks"], *config["runtime_files"])


def profile_for_chapter(chapter: int) -> str:
    try:
        return CHAPTER_PROFILES[chapter]
    except KeyError as error:
        raise ValueError(
            f"No hay un demo JupyterLite configurado para el capítulo {chapter}"
        ) from error


def page_notebooks(chapter: int, page: str) -> tuple[Path, ...]:
    try:
        return PAGE_NOTEBOOKS[(chapter, page)]
    except KeyError as error:
        raise ValueError(
            f"No hay notebooks JupyterLite en el catálogo para {chapter}/{page}"
        ) from error
