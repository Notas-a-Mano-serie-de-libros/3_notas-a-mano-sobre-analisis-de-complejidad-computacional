from pathlib import Path

from scripts.validate_repository_paths import validate_repository_paths


ROOT = Path(__file__).resolve().parents[1]


def test_repository_links_and_paths_are_current():
    assert validate_repository_paths() == []


def test_chapters_separate_public_notebooks_from_runtime_logic():
    """Cada capítulo expone notebooks/ y encapsula la implementación en runtime/."""
    for chapter_number in range(2, 9):
        chapter_dir = ROOT / f"capitulo{chapter_number}"
        notebooks_dir = chapter_dir / "notebooks"
        assert notebooks_dir.is_dir()
        assert (chapter_dir / "runtime").is_dir()

        assert {path.name for path in chapter_dir.iterdir()} == {"images", "notebooks", "runtime"}
        assert (notebooks_dir / "README.md").is_file()
        assert (chapter_dir / "images" / "recursos").is_dir()
        assert (chapter_dir / "images" / "generadas").is_dir()

        nested_notebooks = [
            path.relative_to(chapter_dir).as_posix()
            for path in chapter_dir.rglob("*.ipynb")
            if path.parent != notebooks_dir
        ]
        if chapter_number in {2, 4}:
            assert nested_notebooks
            assert all(
                path.startswith("notebooks/graficas/")
                for path in nested_notebooks
            )
        else:
            assert nested_notebooks == [], (
                f"{chapter_dir.name} contiene notebooks fuera de notebooks/: "
                f"{nested_notebooks}"
            )

        internal_public_files = [
            path.relative_to(chapter_dir / "runtime").as_posix()
            for path in (chapter_dir / "runtime").rglob("*")
            if path.is_file() and path.suffix in {".ipynb", ".pdf"}
        ]
        assert internal_public_files == []


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
        ROOT / "capitulo2" / "runtime" / "experimental_animation.py",
        ROOT / "capitulo2" / "runtime" / "polynomial_animation.py",
        ROOT / "capitulo3" / "runtime" / "asymptotic_animation.py",
        ROOT / "capitulo4" / "runtime" / "experiment_ui.py",
        ROOT / "capitulo5" / "runtime" / "recursion_tree_animation.py",
        ROOT / "capitulo6" / "runtime" / "recursive_analysis_lab.py",
    )
    for source_path in engines:
        source = source_path.read_text(encoding="utf-8")
        assert "common.simulation_views" in source
        assert "standard_view_styles" in source


def test_graphics_live_inside_their_chapter():
    graphics_directories = sorted(
        path for path in ROOT.rglob("graficas") if ".git" not in path.parts
    )
    assert graphics_directories == [
        ROOT / "capitulo2" / "notebooks" / "graficas",
        ROOT / "capitulo4" / "notebooks" / "graficas",
    ]
    for chapter_number in range(2, 9):
        images_dir = ROOT / f"capitulo{chapter_number}" / "images"
        assert {path.name for path in images_dir.iterdir()} == {"generadas", "recursos"}
    graphics_source = (ROOT / "common" / "graphics.py").read_text(encoding="utf-8")
    assert 'PROJECT_ROOT / chapter / "images" / "generadas"' in graphics_source
