from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess

import pytest


PROJECT_ROOT = Path(__file__).parents[1]
ANIMATION_PATH = PROJECT_ROOT / "capitulo3" / "asymptotic_animation.py"
BOOTSTRAP_PATH = PROJECT_ROOT / "capitulo3" / "asymptotic_bootstrap.py"
COMPARISON_NOTEBOOK = PROJECT_ROOT / "capitulo3" / "0_comparacion_notaciones_asintoticas.ipynb"
ASYMPTOTIC_NOTEBOOKS = [
    PROJECT_ROOT / "capitulo3" / f"{number}_{name}.ipynb"
    for number, name in [
        (1, "notacion_big_o"),
        (2, "notacion_little_o"),
        (3, "notacion_big_omega"),
        (4, "notacion_little_omega"),
        (5, "notacion_theta"),
    ]
]


def load_animation_module():
    spec = importlib.util.spec_from_file_location("cap3_asymptotic_test", ANIMATION_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_math_engine(mode: str, expression: str):
    if shutil.which("node") is None:
        pytest.skip("Node.js no está disponible para validar el motor JavaScript")
    html = load_animation_module()._BIG_O_HTML
    start = html.index("  var FNS={")
    end = html.index("  function resize()", start)
    engine = html[start:end]
    script = f"(function(){{var MODE={json.dumps(mode)};\n{engine}\nconsole.log(JSON.stringify({expression}));}})();"
    completed = subprocess.run(
        ["node", "-e", script],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


@pytest.mark.parametrize(
    ("mode", "c_key", "g_key", "constant", "expected"),
    [
        ("big_o", "book", "n3", "1.1", 20.603151099841746),
        ("big_omega", "book", "n3", "0.5", 0),
        ("theta", "book", "n3", "{c1:0.5,c2:1.1}", 20.603151099841746),
        ("little_o", "n3", "n4", "0.1", 10),
        ("little_omega", "n3", "n2", "2", 2),
    ],
)
def test_n0_verificado_en_los_cinco_modos(mode, c_key, g_key, constant, expected):
    expression = f"estimateN0({json.dumps(c_key)},{json.dumps(g_key)},{constant})"
    assert run_math_engine(mode, expression) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("mode", "expected_g"),
    [
        ("big_o", "n3"),
        ("little_o", "n4"),
        ("big_omega", "n3"),
        ("little_omega", "n2"),
        ("theta", "n3"),
    ],
)
def test_referencia_inicial_es_valida_para_cada_notacion(mode, expected_g):
    assert run_math_engine(mode, "gKey()") == expected_g


@pytest.mark.parametrize(
    ("mode", "constant", "expected"),
    [
        ("big_o", "2", 2.93),
        ("little_o", "10", 0.97),
        ("big_omega", "0.5", 0),
        ("little_omega", "1", 0),
        ("theta", "{c1:0.5,c2:2}", 2.93),
    ],
)
def test_n0_coincide_con_los_ejemplos_del_libro(mode, constant, expected):
    g_key = "n4" if mode == "little_o" else ("n2" if mode == "little_omega" else "n3")
    expression = f"estimateN0('book',{json.dumps(g_key)},{constant})"
    assert run_math_engine(mode, expression) == pytest.approx(expected, abs=0.01)


def test_intervalos_distinguen_extremos_abiertos_y_cerrados():
    closed = run_math_engine(
        "big_o",
        "(function(){var n0=estimateN0('book','n3',2);"
        "return realThresholdSetLatex(n0,"
        "solutionIncludesBoundary('book','n3',2,n0));})()",
    )
    opened = run_math_engine(
        "little_o",
        "(function(){var n0=estimateN0('book','n4',10);"
        "return realThresholdSetLatex(n0,"
        "solutionIncludesBoundary('book','n4',10,n0));})()",
    )
    omega_opened = run_math_engine(
        "little_omega",
        "(function(){var n0=estimateN0('book','n2',1);"
        "return realThresholdSetLatex(n0,"
        "solutionIncludesBoundary('book','n2',1,n0));})()",
    )
    assert closed.startswith("[")
    assert opened.startswith("(")
    assert omega_opened == "(0,\\infty)"
    assert closed.endswith(",\\infty)")
    assert opened.endswith(",\\infty)")


def test_caso_omega_del_libro_cumple_desde_cero():
    expression = "[0,1,2,20].map(function(n){return satisfiesInequality('book','n3',0.5,n);})"
    assert run_math_engine("big_omega", expression) == [True, True, True, True]


def test_pareja_sin_relacion_asintotica_no_inventa_n0():
    assert run_math_engine("big_o", "estimateN0('n3','n2',1)") is None


def test_mathjax_se_carga_una_vez_y_espera_startup():
    html = load_animation_module()._BIG_O_HTML
    assert "window.__asymptoticMathJaxReady" in html
    assert "'[tex]/boldsymbol','[tex]/cancel'" in html
    assert "MathJax.startup && MathJax.startup.promise" in html
    assert "mathJax.typesetPromise([root])" in html
    assert "catch(function(){})" not in html
    assert html.count("tex-svg.js") == 1


def test_resultado_muestra_intervalo_y_n0_directo_sin_bloque_de_seleccion():
    html = load_animation_module()._BIG_O_HTML
    assert r"n_0=\\lceil" not in html
    assert r"\\lceil A\\rceil" not in html
    assert "n₀ seleccionado" in html
    assert "realThresholdSetLatex" in html
    assert "'n\\\\in '+realThresholdSetLatex" in html
    assert "Valor de '+titleTex('n_0')+' seleccionado por defecto:" in html
    assert "Conjunto solución '+titleTex('S')" not in html
    assert "Selección de " not in html
    assert "n0SelectionLatex" not in html
    assert r"n_0=\\inf" not in html
    assert r"n_0=\\min" not in html


def test_notebooks_presentan_n0_como_umbral_real_seleccionado():
    for notebook_path in ASYMPTOTIC_NOTEBOOKS:
        notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
        source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
        assert r"\lceil A\rceil" not in source
        assert r"n_0\in\mathbb{N}" not in source
        assert r"n_0\in\mathbb{R}^{+}" in source
        assert r"\forall n\ge n_0" in source
        assert r"n_0=\inf" not in source


def test_notaciones_estrictas_seleccionan_un_valor_posterior_al_extremo():
    little_o = run_math_engine(
        "little_o",
        "selectedN0(estimateN0('book','n4',10))",
    )
    little_omega = run_math_engine(
        "little_omega",
        "selectedN0(estimateN0('book','n2',1))",
    )
    assert little_o == pytest.approx(0.976912067861)
    assert little_omega == pytest.approx(0.01)

    displayed = run_math_engine(
        "little_o",
        "thresholdNumber(selectedN0(estimateN0('book','n4',10)))",
    )
    assert displayed == "0.98"


def test_epsilon_es_configurable_y_limita_el_n0_seleccionado():
    selected = run_math_engine(
        "little_o",
        "(function(){el=function(){return {value:'0.05'};};"
        "return selectedN0(estimateN0('book','n4',10));})()",
    )
    assert selected == pytest.approx(1.016912067861)

    clamped = run_math_engine(
        "little_omega",
        "(function(){el=function(){return {value:'0.05'};};"
        "STATE_N0=0.01;"
        "return selectedN0(estimateN0('book','n2',1));})()",
    )
    assert clamped == pytest.approx(0.05)


def test_bloque_informativo_permanece_estatico_al_desplazar_n0():
    html = run_math_engine(
        "little_o",
        "(function(){STATE_N0=5;"
        "return singleSolutionSetHtml('book','n4',10,"
        "estimateN0('book','n4',10));})()",
    )
    assert r"n_0=5" not in html
    assert r"n_0=0.97+\varepsilon=0.98" in html
    assert r"n\in (0.97,\infty)" in html
    assert "Conjunto solución:" in html
    assert "Conjunto solución \\\\(\\\\boldsymbol{S}\\\\)" not in html
    assert "El usuario puede mover la línea" not in html


def test_valores_grandes_usan_coeficiente_por_potencia_de_diez():
    assert run_math_engine("big_o", "fmt(250000)") == r"2.5\cdot 10^{5}"
    assert run_math_engine("big_o", "fmt(1.25e-5)") == r"1.25\cdot 10^{-5}"
    assert "e+" not in run_math_engine("big_o", "thresholdNumber(2.5e20)")


def test_control_epsilon_y_arrastre_de_n0_estan_disponibles():
    html = load_animation_module()._BIG_O_HTML
    assert 'id="bo-epsilon"' in html
    assert 'value="0.01"' in html
    assert "node.style.display=little?'flex':'none'" in html
    assert "drag=overN0?'n0'" in html
    assert "if(drag==='n0')" in html
    assert "drawN0DisplacementFade(threshold,n0,a,b)" in html
    assert "var left=PAD.l" in html
    assert "rgba(255,255,255,0.48)" in html
    assert "rgba(120,120,120,0.12)" in html


def test_titulo_de_interseccion_theta_esta_alineado_a_la_izquierda():
    html = load_animation_module()._BIG_O_HTML
    assert '<div class="theta-intersection"><div class="solution-title">Valores que cumplen ambas desigualdades ' in html


def test_theta_separa_limite_inferior_y_superior():
    html = load_animation_module()._BIG_O_HTML
    assert "thetaLimitProcedureHtml" in html
    assert "limitProcedureHtml(ck,gk,'\\\\liminf')" in html
    assert "limitProcedureHtml(ck,gk,'\\\\limsup')" in html
    assert "<th>Límite inferior</th><th>Límite superior</th>" in html
    assert "limitExpressionLatex(ck,gk,false,'\\\\liminf')" in html
    assert "limitExpressionLatex(ck,gk,false,'\\\\limsup')" in html
    assert "<strong>Límite inferior (Big-'+titleTex('\\\\Omega')+'):</strong>" in html
    assert "<strong>Límite superior (Big-'+titleTex('O')+'):</strong>" in html


def test_cada_render_obtiene_ids_independientes(monkeypatch):
    module = load_animation_module()
    rendered = []
    monkeypatch.setattr(module, "display", lambda value: rendered.append(value.data))

    module.run_big_o_app()
    module.run_big_o_app()

    assert len(rendered) == 2
    assert "bo-wrap" not in rendered[0]
    first_id = rendered[0].split('id="', 1)[1].split('"', 1)[0]
    second_id = rendered[1].split('id="', 1)[1].split('"', 1)[0]
    assert first_id != second_id


def test_comparacion_y_notebooks_especificos_muestran_el_selector(monkeypatch):
    module = load_animation_module()
    rendered = []
    monkeypatch.setattr(module, "display", lambda value: rendered.append(value.data))

    module.run_comparison_app()
    module.run_big_o_app()

    assert "var MODE_SELECTABLE=true;" in rendered[0]
    assert ".mode-section{display:grid}" in rendered[0]
    assert '<span class="label-text">\\(\\mathcal{F}\\)</span>' in rendered[0]
    assert rendered[0].index("\\(\\mathcal{F}\\)") < rendered[0].index(
        "\\(\\text{Escala}\\)"
    ) < rendered[0].index("Funciones de referencia:")
    assert "var MODE='big_o';" in rendered[0]
    assert "var MODE_SELECTABLE=true;" in rendered[1]
    assert ".mode-section{display:grid}" in rendered[1]
    assert "var MODE='big_o';" in rendered[1]


def test_notebook_comparativo_usa_el_mismo_motor_compartido():
    notebook = json.loads(COMPARISON_NOTEBOOK.read_text(encoding="utf-8"))
    source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
    assert 'ASYMPTOTIC_APP = "comparison"' in source
    assert "asymptotic_bootstrap.py" in source
    assert "0_comparacion_notaciones_asintoticas.ipynb" in (
        PROJECT_ROOT / "capitulo3" / "README.md"
    ).read_text(encoding="utf-8")


def test_no_quedan_residuos_de_terminos_menores_ni_eventos_duplicados():
    source = ANIMATION_PATH.read_text(encoding="utf-8")
    for dead_name in (
        "LOWER_TERMS",
        "regenerateLowerTerms",
        "decadeValue",
        "nearestDecade",
        "modeName",
        "isUpperMode",
    ):
        assert dead_name not in source
    assert "addEventListener('mousedown'" not in source
    assert "addEventListener('touchstart'" not in source
    assert "addEventListener('pointerdown'" in source
    assert "ResizeObserver" in source


def test_bootstrap_descarga_con_timeout_y_sin_cache_local_permanente():
    source = BOOTSTRAP_PATH.read_text(encoding="utf-8")
    assert '"comparison": "run_comparison_app"' in source
    assert "tempfile.gettempdir()" in source
    assert "timeout=30" in source
    assert '"Pragma": "no-cache"' in source
    assert "spec is None or spec.loader is None" in source
