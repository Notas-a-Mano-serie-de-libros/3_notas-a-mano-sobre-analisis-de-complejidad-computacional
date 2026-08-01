import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
UI_SOURCE = (ROOT / "capitulo4" / "experiment_ui.py").read_text(encoding="utf-8")
C2_UI_SOURCE = (
    ROOT
    / "capitulo2"
    / "analisis_complejidad_temporal_experimental"
    / "experimental_animation.py"
).read_text(encoding="utf-8")


def test_interfaz_comparte_paneles_y_medidas_del_capitulo_dos():
    assert "STEPPER_FIELD_WIDTH = 188" in UI_SOURCE
    assert "STEPPER_BUTTON_WIDTH = 34" in UI_SOURCE
    assert "STEPPER_VALUE_WIDTH = 120" in UI_SOURCE
    assert "STEPPER_GAP = 0" in UI_SOURCE
    assert 'configuration_panel = subpanel("Configuración"' in UI_SOURCE
    assert 'result_panel = subpanel("Resultado"' in UI_SOURCE
    assert "experimental-subpanel-summary" in UI_SOURCE
    assert "appearance: auto !important" in UI_SOURCE
    assert "-webkit-appearance: menulist !important" in UI_SOURCE
    assert "STEPPER_LABEL_WIDTH = 150" in UI_SOURCE
    assert 'options=[("Sí", False), ("No", True)]' in UI_SOURCE
    assert '"Restringir n máximo"' in UI_SOURCE
    assert "⚠ Ejecución sin restricciones" in UI_SOURCE
    assert "Ejecutar sin limitaciones incrementará el tiempo de ejecución y el consumo de recursos." in UI_SOURCE


def test_tabla_es_nativa_formateada_y_la_medicion_no_bloquea_la_vista():
    assert "constant-native-table" in UI_SOURCE
    assert "constant-equation" in UI_SOURCE
    assert "'STIX Two Math','STIXGeneral','Cambria Math','Latin Modern Math'" in UI_SOURCE
    assert "return mathjax_frame(table" not in UI_SOURCE
    assert "await asyncio.to_thread(" in UI_SOURCE
    assert "await asyncio.sleep(0)" in UI_SOURCE
    assert 'margin="16px 0 0 0"' in UI_SOURCE


def test_bloque_css_es_identico_al_del_capitulo_dos():
    start = "        <style>\n"
    end = "        </style>\n"

    def css_block(source):
        block_start = source.rindex(start)
        block_end = source.index(end, block_start) + len(end)
        return source[block_start:block_end]

    assert css_block(UI_SOURCE) == css_block(C2_UI_SOURCE)


def test_renderizador_matematico_es_identico_al_del_capitulo_dos():
    def mathjax_block(source):
        block_start = source.index("def mathjax_frame(")
        block_end = source.index("\ndef formula_widget(", block_start)
        return source[block_start:block_end]

    assert mathjax_block(UI_SOURCE) == mathjax_block(C2_UI_SOURCE)
    assert "prefers-color-scheme:dark" not in mathjax_block(UI_SOURCE)
    assert "body{{color:#000" in mathjax_block(UI_SOURCE)


def test_plantilla_de_grafica_conserva_titulos_y_contraste():
    analysis_source = (ROOT / "capitulo4" / "experimental_analysis.py").read_text(
        encoding="utf-8"
    )
    assert "def _render_template(maximum_n, mode):" in analysis_source
    assert 'ax.set_title("Complejidad teórica vs. experimental")' in analysis_source
    assert r'$\mathrm{Tamaño\ de\ la\ entrada}\ (n)$' in analysis_source
    assert "render_template=lambda maximum_n:" in analysis_source
    assert "fig.subplots_adjust(left=0.13, right=0.97, bottom=0.17, top=0.86)" in analysis_source
    assert 'bbox_inches="tight"' not in analysis_source.split("def _render_result", 1)[1]


def test_ejemplos_usan_una_sola_simulacion_con_selector_temporal_espacial():
    notebooks = sorted((ROOT / "capitulo4").glob("ejemplo*.ipynb"))
    notebooks = [path for path in notebooks if "_graficas" not in path.name]
    assert notebooks

    for path in notebooks:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        source = "\n".join(
            "".join(cell.get("source", [])) for cell in notebook.get("cells", [])
        )
        assert source.count("#@title Simulación experimental") == 1
        assert "EXPERIMENT_MODE" not in source
        assert "Complejidad espacial experimental" not in source

    analysis_source = (ROOT / "capitulo4" / "experimental_analysis.py").read_text(
        encoding="utf-8"
    )
    assert "UI.run_selectable_app" in analysis_source
    assert '("Temporal", "time")' in UI_SOURCE
    assert '("Espacial", "memory")' in UI_SOURCE
