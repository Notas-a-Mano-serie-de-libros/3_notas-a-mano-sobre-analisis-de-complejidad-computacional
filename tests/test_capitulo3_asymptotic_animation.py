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


def test_arrastre_reutiliza_calculos_sin_diferir_la_actualizacion_de_n0():
    html = load_animation_module()._BIG_O_HTML
    assert "window.requestAnimationFrame||function(callback){return setTimeout(callback,16);}" in html
    assert "if(drawFramePending)return;" in html
    assert "if(cacheKey===thresholdCacheKey)return thresholdCacheValue;" in html
    assert "if(cacheKey===sampleCacheKey)return sampleCacheValue;" in html
    assert "updateText(a,b,ck,gk,c,threshold,lim);" in html
    assert "function updateText(a,b,ck,gk,c,threshold,lim)" in html
    assert "typesetTimer" not in html
    assert "panelRefreshTimer" not in html


def test_grafica_separa_capas_estaticas_de_elementos_dinamicos():
    html = load_animation_module()._BIG_O_HTML
    assert "staticBackground=document.createElement('canvas')" in html
    assert "staticCurves=document.createElement('canvas')" in html
    assert "function renderStaticLayers(key,data,a,b,yrange)" in html
    assert "if(key===staticLayerKey)return;" in html
    assert "drawStaticLayer(staticBackground);" in html
    assert "drawValidArea(data,a,b,yrange,n0);" in html
    assert "drawStaticLayer(staticCurves);" in html
    assert html.index("drawStaticLayer(staticBackground);") < html.index(
        "drawValidArea(data,a,b,yrange,n0);"
    ) < html.index("drawStaticLayer(staticCurves);")
    assert "drawN0DisplacementFade(threshold,n0,a,b);" in html
    assert "drawN0(n0,a,b,ck,yrange);" in html


def test_umbral_y_cruces_se_distinguen_del_n0_seleccionado():
    html = load_animation_module()._BIG_O_HTML
    assert 'id="bo-leg-threshold"' in html
    assert "function drawThresholdAndCrossings(threshold,a,b,ck,gk,c,yrange)" in html
    assert "ctx.strokeStyle='#00838F'" in html
    assert "drawThresholdAndCrossings(threshold,a,b,ck,gk,c,yrange);" in html
    assert "Math.abs(left-bound)>Math.max" in html
    assert "(isStrictMode()?'\\\\inf(I)=':'\\\\min(I)=')" in html


def test_enfoque_n0_mantiene_estado_activo_hasta_cambiar_la_vista():
    html = load_animation_module()._BIG_O_HTML
    assert "n0FocusActive=true;" in html
    assert "focusButton.classList.toggle('active',n0FocusActive);" in html
    assert "function deactivateN0Focus()" in html
    assert "deactivateN0Focus();" in html


def test_resize_no_recrea_el_lienzo_si_el_tamano_no_cambio():
    html = load_animation_module()._BIG_O_HTML
    assert "if(cv.width!==pixelWidth || cv.height!==pixelHeight)" in html
    assert "staticLayerKey='';" in html


def test_boton_enfoca_la_grafica_alrededor_del_n0_seleccionado():
    html = load_animation_module()._BIG_O_HTML
    assert 'id="bo-zoom-n0"' in html
    assert 'aria-label="Ver el comportamiento alrededor de n₀"' in html
    assert "function focusAroundN0()" in html
    assert "var n0=selectedN0(estimateN0(ck,gk,c));" in html
    assert "n0/Math.pow(10,0.12)" in html
    assert "n0*Math.pow(10,0.18)" in html
    assert "Math.max(0.05,Math.abs(n0)*0.03,epsilonVal()*2)" in html
    assert "nextA=Math.max(0,n0-radius);" in html
    assert "nextB=Math.min(MAX_B,n0+radius*1.2);" in html
    assert "syncInputs(nextA,nextB);" in html
    assert "Y_OFFSET=0;Y_SCALE=1;" in html
    assert "function focusVerticalAroundCurves(data,yrange)" in html
    assert "var values=data.c.concat(data.cg);" in html
    assert "Y_SCALE=Math.min(80,plotHeight*0.78/Math.abs(bottom-top));" in html
    assert "focusVerticalAroundCurves(focusData,Y_RANGE_OVERRIDE);" in html
    assert "el('bo-zoom-n0').addEventListener('click',focusAroundN0);" in html


def test_boton_n0_se_desactiva_si_el_umbral_no_puede_mostrarse():
    html = load_animation_module()._BIG_O_HTML
    assert "focusButton.disabled=n0===null || (isLogScale() && n0===0);" in html
    assert "n₀ = 0 no puede mostrarse en una escala logarítmica" in html


def test_mas_acerca_y_menos_aleja_la_vista():
    html = load_animation_module()._BIG_O_HTML
    assert 'id="bo-zoom-in" title="Acercar la vista"' in html
    assert 'id="bo-zoom-out" title="Alejar la vista"' in html
    assert "function zoomIn()" in html
    assert "function zoomOut()" in html
    assert "zoomAt(zoomCenter(ab[0],ab[1]),0.5);" in html
    assert "zoomAt(zoomCenter(ab[0],ab[1]),2);" in html
    assert "el('bo-zoom-in').addEventListener('click',zoomIn);" in html
    assert "el('bo-zoom-out').addEventListener('click',zoomOut);" in html


def test_parametros_adicionales_conservan_zoom_vista_y_n0_seleccionado():
    html = load_animation_module()._BIG_O_HTML
    assert "Y_RANGE_OVERRIDE=null,lastYRange=null" in html
    assert "function preserveViewportForParameterChange()" in html
    assert "Y_RANGE_OVERRIDE={min:lastYRange.min,max:lastYRange.max};" in html
    listeners = html.split("['bo-c','bo-c1','bo-c2'].forEach", 1)[1].split(
        "el('bo-scale').addEventListener", 1
    )[0]
    assert "preserveViewportForParameterChange();" in listeners
    assert "resetSelectedN0();" not in listeners
    assert "Y_OFFSET=0" not in listeners
    assert "Y_SCALE=1" not in listeners
    assert "Y_RANGE_OVERRIDE=null" not in listeners


def test_solo_reset_y_cambios_estructurales_liberan_el_rango_vertical():
    html = load_animation_module()._BIG_O_HTML
    assert "Y_OFFSET=0;Y_SCALE=1;Y_RANGE_OVERRIDE=null;" in html
    assert "el('bo-scale').addEventListener('input',function(){Y_RANGE_OVERRIDE=null;deactivateN0Focus();draw();});" in html
    assert "Y_RANGE_OVERRIDE=yBounds(focusData);" in html


def test_bloqueo_independiente_de_ejes_evitan_cambios_de_vista():
    html = load_animation_module()._BIG_O_HTML
    assert 'id="bo-lock-x"' in html
    assert 'id="bo-lock-y"' in html
    assert "if(lockX)return;" in html
    assert "if(!lockX)syncInputs(na,nb);" in html
    assert "if(!lockY)Y_OFFSET=panStart.yOffset+(p.y-panStart.y);" in html
    assert "this.classList.toggle('active',lockX)" in html
    assert "this.classList.toggle('active',lockY)" in html


def test_historial_restaura_vista_parametros_y_n0():
    html = load_animation_module()._BIG_O_HTML
    assert 'id="bo-history-undo"' in html
    assert 'id="bo-history-redo"' in html
    assert "function viewSnapshot()" in html
    assert "function captureHistory()" in html
    assert "function restoreSnapshot(snapshot)" in html
    assert "function undoHistory()" in html
    assert "function redoHistory()" in html
    assert "historyUndo.length>50" in html


def test_n0_dinamico_no_recompone_la_demostracion_ni_la_tabla():
    html = load_animation_module()._BIG_O_HTML
    assert "function renderDynamicMath(id,latex)" in html
    assert "mathJax.tex2svgPromise(requested,{display:false})" in html
    assert "state.pending=latex;" in html
    assert "if(state.running)return;" in html
    assert "function updateDynamicN0(n0)" in html
    assert "if(drag==='n0')updateDynamicN0(n0);" in html


def test_muestreo_se_adapta_al_ancho_curvatura_y_cruce():
    html = load_animation_module()._BIG_O_HTML
    assert "function adaptiveSampleCount(ck,gk)" in html
    assert "Math.max(120,Math.min(520,count))" in html
    assert "if(FNS[ck].rank>=7 || FNS[gk].rank>=7)" in html
    assert "var crossing=estimateN0(ck,gk,c);" in html
    assert "positions.push(crossing);" in html


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


def test_boton_activa_y_desactiva_zoom_con_trackpad():
    html = load_animation_module()._BIG_O_HTML
    assert 'id="bo-zoom-trackpad"' in html
    assert 'aria-pressed="false"' in html
    assert "trackpadZoomEnabled=false" in html
    assert "trackpadZoomEnabled=!trackpadZoomEnabled" in html
    assert "if(!trackpadZoomEnabled)return;" in html


def test_etiquetas_de_controles_estan_centradas_en_su_columna():
    html = load_animation_module()._BIG_O_HTML
    assert ".label-text{display:inline-flex;align-items:center;justify-content:center;" in html
    assert "min-width:48px;text-align:center" in html


def test_grafica_usa_altura_ampliada():
    html = load_animation_module()._BIG_O_HTML
    assert ".plot-wrap{position:relative;width:100%;height:480px}" in html
    assert "canvas{display:block;width:100%;height:480px" in html


def test_leyenda_esta_dentro_de_la_esquina_superior_izquierda():
    html = load_animation_module()._BIG_O_HTML
    assert ".legend{position:absolute;left:92px;top:48px;" in html
    assert "flex-direction:column;align-items:flex-start" in html
    assert "width:250px;box-sizing:border-box" in html
    assert "PAD={l:82,r:32,t:38,b:58}" in html
    assert ".axis-x{left:82px;right:32px" in html
    assert "ctx.rect(PAD.l,PAD.t,W-PAD.l-PAD.r,H-PAD.t-PAD.b)" in html
    assert "border:1px solid rgba(80,80,80,.28)" in html
    assert "box-shadow:0 1px 3px rgba(0,0,0,.10)" in html
    plot = html.split('<div class="plot-wrap">', 1)[1].split('<div class="note"', 1)[0]
    assert plot.index('id="bo-leg-c"') < plot.index('id="bo-leg-low"')
    assert plot.index('id="bo-leg-low"') < plot.index('id="bo-leg-cg"')
    assert plot.index('id="bo-leg-cg"') < plot.index('id="bo-leg-n0"')


def test_parametros_reservan_altura_para_dos_filas():
    html = load_animation_module()._BIG_O_HTML
    assert ".ctrl.vertical.additional{min-height:72px}" in html


def test_etiquetas_a_y_b_quedan_debajo_de_los_ticks_y_evitan_el_titulo():
    html = load_animation_module()._BIG_O_HTML
    assert "ctx.moveTo(x,y+22);ctx.lineTo(x-6,y+33);ctx.lineTo(x+6,y+33)" in html
    assert "if(!overlapsAxisTitle){" in html
    assert "ctx.fillText(label,x,y+36)" in html
    assert "axisTitle='Tamaño de la entrada (n)'" in html
    assert "ctx.fillStyle='#6A1B9A';ctx.strokeStyle='#6A1B9A'" in html
    assert "function n0Color(){return '#2E7D32'}" in html


def test_titulo_de_interseccion_theta_esta_alineado_a_la_izquierda():
    html = load_animation_module()._BIG_O_HTML
    assert '<div class="theta-intersection"><div class="solution-title">Valores que cumplen ambas desigualdades ' in html


def test_theta_separa_limite_inferior_y_superior():
    html = load_animation_module()._BIG_O_HTML
    assert "thetaLimitProcedureHtml" in html
    assert "limitProcedureHtml(ck,gk,'\\\\liminf')" in html
    assert "limitProcedureHtml(ck,gk,'\\\\limsup')" in html
    assert "<strong>Límite inferior (Big-'+titleTex('\\\\Omega')+'):</strong>" in html
    assert "<strong>Límite superior (Big-'+titleTex('O')+'):</strong>" in html


def test_tabla_final_muestra_solo_el_limite_solicitado_por_la_notacion():
    html = load_animation_module()._BIG_O_HTML
    render_limits = html.split("function renderLimits", 1)[1].split(
        "function pointer", 1
    )[0]
    assert "<th>Resultado del límite '+tex('(k)')+'</th><th>Pertenencia</th>" in render_limits
    assert "tex(displayLimitValue(limitValue(ck,gk)))" in render_limits
    assert "tex('k='+displayLimitValue(limitValue(ck,gk)))" not in render_limits
    assert "limitExpressionLatex(ck,gk,false)" not in render_limits
    assert "Límite inferior" not in render_limits
    assert "Límite superior" not in render_limits


def test_tabla_final_resalta_pertenencia_y_sustituye_directamente_las_funciones():
    html = load_animation_module()._BIG_O_HTML
    assert "tbody tr.member td{background:#E8F5E9!important}" in html
    assert "tbody tr.nonmember td{background:#FFEBEE!important}" in html
    assert "var rowClass=(isMember(ck,gk)?'member':'nonmember')" in html


def test_informacion_inferior_se_organiza_en_secciones_plegables():
    html = load_animation_module()._BIG_O_HTML
    assert '<details class="info-section" id="bo-result-section" open>' in html
    assert '<details class="info-section" id="bo-limit-section">' in html
    assert '<details class="info-section" id="bo-n0-section">' in html
    assert '<details class="info-section" id="bo-comparison-section">' in html
    assert html.count('<details class="info-section"') == 4
    assert html.count(" open>") == 1
    assert ".result-body{min-height:172px" in html
    assert r"<summary>Conjunto solución y \(\boldsymbol{n_0}\)</summary>" in html


def test_resultado_resume_respuesta_antes_del_procedimiento():
    html = load_animation_module()._BIG_O_HTML
    assert 'id="bo-result-main"' in html
    assert 'id="bo-result-n0"' in html
    assert "function resultSummaryHtml(ck,gk,c,threshold)" in html
    assert "realThresholdSetLatex(" in html
    assert r"\\begin{gathered}" in html
    assert r"\\begin{aligned}'+relation" not in html
    assert "renderDynamicMath('bo-result-n0',latex);" in html
    assert ".result-body{min-height:172px;box-sizing:border-box;text-align:center}" in html
    assert ".result-body .cards,#bo-wrap .result-body .card,#bo-wrap .result-body .val{text-align:center}" in html


def test_tarjetas_inferiores_conservan_solo_tres_datos_principales():
    html = load_animation_module()._BIG_O_HTML
    result_section = html.split('id="bo-result-section"', 1)[1].split(
        "</details>", 1
    )[0]
    assert result_section.count('class="card"') == 3
    assert "n₀ seleccionado" in result_section
    assert "Condición sobre c" in result_section
    assert "Conclusión" in result_section
    assert "Intervalo visible" not in html
    assert "Límite del cociente" not in html


def test_limite_y_n0_se_generan_en_bloques_independientes():
    html = load_animation_module()._BIG_O_HTML
    assert "function limitProofHtml(ck,gk,c)" in html
    assert "function n0ProofHtml(ck,gk,c,n0)" in html
    assert "el('bo-limit-proof').innerHTML=limitProofHtml(ck,gk,c);" in html
    assert "el('bo-n0-proof').innerHTML=n0ProofHtml(ck,gk,c,threshold);" in html


def test_titulos_theta_separan_constante_y_funcion_con_producto():
    html = load_animation_module()._BIG_O_HTML
    assert "titleTex('c_1\\\\cdot g(n)\\\\le C(n)')" in html
    assert "titleTex('C(n)\\\\le c_2\\\\cdot g(n)')" in html


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


def test_solo_la_comparacion_permite_cambiar_la_notacion(monkeypatch):
    module = load_animation_module()
    rendered = []
    monkeypatch.setattr(module, "display", lambda value: rendered.append(value.data))

    module.run_comparison_app()
    module.run_big_o_app()

    assert "var MODE_SELECTABLE=true;" in rendered[0]
    assert ".mode-section{display:grid}" in rendered[0]
    assert '<select id="' in rendered[0]
    assert '" >' in rendered[0]
    assert '<span class="label-text">\\(\\mathcal{F}\\)</span>' in rendered[0]
    assert rendered[0].index("\\(\\mathcal{F}\\)") < rendered[0].index(
        "\\(\\text{Escala}\\)"
    ) < rendered[0].index("Funciones de referencia:")
    assert "var MODE='big_o';" in rendered[0]
    assert "var MODE_SELECTABLE=false;" in rendered[1]
    assert ".mode-section{display:grid}" in rendered[1]
    assert '" disabled>' in rendered[1]
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
