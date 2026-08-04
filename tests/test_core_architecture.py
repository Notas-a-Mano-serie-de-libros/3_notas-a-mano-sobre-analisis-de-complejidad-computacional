from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_domain_packages_live_outside_chapters():
    assert not (ROOT / "capitulo7" / "domain").exists()
    assert not (ROOT / "capitulo8" / "domain").exists()
    assert (ROOT / "core" / "search" / "search_common.py").exists()
    assert (ROOT / "core" / "sort" / "sort_common.py").exists()


def test_domain_views_use_the_common_view_contract():
    for source_path in (
        ROOT / "core" / "search" / "search_common.py",
        ROOT / "core" / "search" / "0_comparacion_busquedas_app.py",
        ROOT / "core" / "sort" / "sort_common.py",
    ):
        source = source_path.read_text(encoding="utf-8")
        assert "common.simulation_views" in source
        assert "build_simulation_view" in source


def test_chapter_engines_consume_the_common_visual_contract():
    engines = (
        ROOT / "capitulo2" / "analisis_complejidad_temporal_experimental" / "experimental_animation.py",
        ROOT / "capitulo2" / "analisis_complejidad_temporal_experimental" / "polynomial_animation.py",
        ROOT / "capitulo3" / "asymptotic_animation.py",
        ROOT / "capitulo4" / "experiment_ui.py",
        ROOT / "capitulo5" / "recursion_tree_animation.py",
        ROOT / "capitulo6" / "recursive_analysis_lab.py",
    )
    for source_path in engines:
        source = source_path.read_text(encoding="utf-8")
        assert "common.simulation_views" in source
        assert "standard_view_styles" in source
