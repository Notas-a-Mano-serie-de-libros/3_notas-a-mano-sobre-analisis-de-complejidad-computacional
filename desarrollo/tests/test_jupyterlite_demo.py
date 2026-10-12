from __future__ import annotations

import ast
import json
from types import SimpleNamespace

from desarrollo.scripts.build_jupyterlite_demo import (
    AUTORUN_EXTENSION_DIR,
    AUTORUN_EXTENSION_NAME,
    CHAPTER2_NOTEBOOKS,
    CHAPTER2_RUNTIME_FILES,
    CHAPTER_CONFIGS,
    CONTENT_FILES,
    LITE_DIR,
    NOTEBOOKS,
    WIDGET_PROFILES,
    WIDGET_WHEEL_REQUIREMENTS,
    chapter_content_files,
    configure_pyodide_packages,
    content_storage_name,
    prepare_contents,
    prepare_profile_contents,
)
from desarrollo.scripts.jupyterlite_catalog import (
    CHAPTER_PROFILES,
    PAGE_NOTEBOOKS,
    PROFILE_CONFIGS,
    profile_content_files,
)
from desarrollo.scripts.sync_jupyterlite_urls import notebook_url
from desarrollo.scripts.validate_pages_breadcrumbs import validate as validate_breadcrumbs
from desarrollo.tests.helpers import PROJECT_ROOT


def test_jupyterlite_demo_sources_and_configuration_exist():
    assert (LITE_DIR / "jupyter-lite.json").is_file()
    assert (AUTORUN_EXTENSION_DIR / "package.json").is_file()
    assert (AUTORUN_EXTENSION_DIR / "src" / "index.ts").is_file()
    config = json.loads((LITE_DIR / "jupyter-lite.json").read_text(encoding="utf-8"))
    assert config["jupyter-config-data"]["defaultKernelName"] == "python"
    assert config["jupyter-config-data"]["settingsOverrides"][
        "@jupyterlab/notebook-extension:tracker"
    ]["autoStartDefaultKernel"] is True
    assert NOTEBOOKS[0] in CONTENT_FILES
    assert all(notebook in CONTENT_FILES for notebook in NOTEBOOKS)
    assert all((PROJECT_ROOT / path).is_file() for path in CONTENT_FILES)
    assert len(CHAPTER2_NOTEBOOKS) == 9
    assert all((PROJECT_ROOT / path).is_file() for path in chapter_content_files(2))
    assert all(path in chapter_content_files(2) for path in CHAPTER2_RUNTIME_FILES)
    assert set(CHAPTER_CONFIGS) == set(range(2, 9))
    assert all(
        (PROJECT_ROOT / path).is_file()
        for chapter in range(4, 9)
        for path in chapter_content_files(chapter)
    )


def test_autorun_extension_executes_after_the_default_kernel_is_ready():
    extension = (
        AUTORUN_EXTENSION_DIR / "src" / "index.ts"
    ).read_text(encoding="utf-8")

    assert AUTORUN_EXTENSION_NAME == "@notas-a-mano/jupyterlite-auto-run"
    assert "tracker.widgetAdded.connect" in extension
    assert "await panel.context.sessionContext.ready" in extension
    assert "await installWidgetPackage(panel)" in extension
    assert "await piplite.install('ipywidgets==8.1.9')" in extension
    assert '"import ipywidgets"' in extension
    assert extension.index("await installWidgetPackage(panel)") < extension.index(
        "NotebookActions.runAll(panel.content, panel.context.sessionContext)"
    )
    assert "NotebookActions.runAll(panel.content, panel.context.sessionContext)" in extension
    assert '"notas-a-mano:jupyterlite-height"' in extension
    assert '".jp-WindowedPanel-outer"' in extension
    assert 'classList.remove("jp-mod-scrollPastEnd")' in extension
    assert "Array.from(scrollContainer.children).reduce" in extension
    assert "child.getBoundingClientRect().bottom - scrollBounds.top" in extension
    assert "window.parent.postMessage" in extension
    assert "new ResizeObserver(scheduleHeightReport)" in extension
    assert "new MutationObserver(scheduleHeightReport)" in extension


def test_chapter2_bootstrap_repairs_only_missing_runtime_files(tmp_path):
    bootstrap_path = (
        PROJECT_ROOT
        / "simulaciones"
        / "capitulo2"
        / "runtime"
        / "colab_bootstrap.py"
    )
    parsed = ast.parse(bootstrap_path.read_text(encoding="utf-8"))
    definitions = ast.Module(
        body=[
            node
            for node in parsed.body
            if isinstance(
                node,
                (ast.Import, ast.ImportFrom, ast.Assign, ast.AnnAssign, ast.FunctionDef),
            )
        ],
        type_ignores=[],
    )
    namespace = {"__name__": "chapter2_bootstrap_test"}
    exec(compile(definitions, str(bootstrap_path), "exec"), namespace)

    present_file = tmp_path / "runtime" / "present.py"
    present_file.parent.mkdir(parents=True)
    present_file.write_text("# disponible\n", encoding="utf-8")
    downloaded = []
    namespace["REQUIRED_FILES"] = ("runtime/present.py", "runtime/missing.py")
    namespace["find_project_root"] = lambda: tmp_path
    namespace["running_in_colab"] = lambda: False
    namespace["download_required_files"] = (
        lambda root, paths: downloaded.extend((root, tuple(paths)))
    )
    namespace["sys"] = SimpleNamespace(path=[], modules={})

    namespace["prepare_imports"]()

    assert downloaded == [tmp_path, ("runtime/missing.py",)]


def test_portal_resizes_embedded_jupyterlite_frames_from_trusted_messages():
    site_javascript = (
        PROJECT_ROOT / "docs" / "assets" / "javascripts" / "site.js"
    ).read_text(encoding="utf-8")
    stylesheet = (
        PROJECT_ROOT / "docs" / "assets" / "stylesheets" / "extra.css"
    ).read_text(encoding="utf-8")

    assert '"notas-a-mano:jupyterlite-height"' in site_javascript
    assert "event.origin !== window.location.origin" in site_javascript
    assert "candidate.contentWindow === event.source" in site_javascript
    assert 'frame.setAttribute("scrolling", "no")' in site_javascript
    assert "frame.style.height" in site_javascript
    assert ".jupyterlite-demo__frame" in stylesheet
    assert "overflow: hidden;" in stylesheet


def test_documentation_dependencies_include_the_jupyter_builder_cli():
    documentation_requirements = (
        PROJECT_ROOT / "requirements-publish.txt"
    ).read_text(encoding="utf-8")
    dependency_lock = (PROJECT_ROOT / "requirements-lock.txt").read_text(
        encoding="utf-8"
    )

    assert "jupyterlab>=4.6.4,<5" in documentation_requirements
    assert "jupyterlab==4.6.4" in dependency_lock


def test_widget_profiles_bundle_their_runtime_wheels():
    assert WIDGET_PROFILES == {"graficas", "algebra-simbolica", "analisis-completo"}
    assert WIDGET_WHEEL_REQUIREMENTS == (
        "comm==0.2.3",
        "ipywidgets==8.1.9",
        "jupyterlab_widgets==3.0.17",
    )
    build_script = (
        PROJECT_ROOT / "desarrollo" / "scripts" / "build_jupyterlite_demo.py"
    ).read_text(encoding="utf-8")
    assert 'f"--piplite-wheels={wheel}"' in build_script


def test_publicacion_invalida_el_contenido_persistido_cuando_cambia_el_demo():
    storage_name = content_storage_name()

    assert storage_name.startswith("Notas a mano · graficas-cientificas · ")
    assert len(storage_name.rsplit(" · ", 1)[1]) == 12
    assert content_storage_name(2).startswith("Notas a mano · graficas · ")


def test_catalogo_asigna_capitulos_y_recursos_a_cuatro_perfiles():
    assert len(PROFILE_CONFIGS) == 4
    assert set(CHAPTER_PROFILES) == set(range(2, 9))
    assert set(PROFILE_CONFIGS["graficas"]["chapters"]) == {2, 4, 6, 8}
    assert set(PROFILE_CONFIGS["graficas-cientificas"]["chapters"]) == {3}
    assert set(PROFILE_CONFIGS["algebra-simbolica"]["chapters"]) == {5}
    assert set(PROFILE_CONFIGS["analisis-completo"]["chapters"]) == {7}
    assert {
        PROJECT_ROOT / "common" / "animation_runtime.py",
        PROJECT_ROOT / "common" / "exercise_laboratory.py",
        PROJECT_ROOT / "common" / "simulation_views.py",
        PROJECT_ROOT / "common" / "widget_controls.py",
    }.issubset({PROJECT_ROOT / path for path in chapter_content_files(7)})
    assert (
        PROJECT_ROOT
        / "simulaciones"
        / "capitulo2"
        / "runtime"
        / "experimental_animation.py"
    ) in {PROJECT_ROOT / path for path in chapter_content_files(7)}
    assert all(
        (PROJECT_ROOT / path).is_file()
        for profile in PROFILE_CONFIGS
        for path in profile_content_files(profile)
    )
    assert all(
        notebook in PROFILE_CONFIGS[CHAPTER_PROFILES[chapter]]["notebooks"]
        for (chapter, _page), notebooks in PAGE_NOTEBOOKS.items()
        for notebook in notebooks
    )


def test_perfil_compartido_incluye_notebooks_de_todos_sus_capitulos(tmp_path):
    prepare_profile_contents(tmp_path, "graficas")

    assert all(
        (tmp_path / notebook).is_file()
        for chapter in (2, 4, 6, 8)
        for notebook in CHAPTER_CONFIGS[chapter]["notebooks"]
    )


def test_kernel_pyodide_precarga_dependencias_del_capitulo():
    config = {"jupyter-config-data": {"defaultKernelName": "python"}}
    packages = CHAPTER_CONFIGS[2]["packages"]

    configure_pyodide_packages(config, packages)

    settings = config["jupyter-config-data"]["litePluginSettings"][
        "@jupyterlite/pyodide-kernel-extension:kernel"
    ]
    assert settings["loadPyodideOptions"]["packages"] == list(packages)


def test_chapter_three_avoids_widget_runtime_in_webassembly():
    animation = (
        PROJECT_ROOT / "simulaciones/capitulo3/runtime/asymptotic_animation.py"
    ).read_text(encoding="utf-8")
    assert 'sys.platform == "emscripten"' in animation
    assert 'return ""' in animation


def test_pages_copy_prepares_each_interactive_notebook_for_pyodide(tmp_path):
    prepare_contents(tmp_path)
    for notebook_path in NOTEBOOKS:
        canonical = json.loads(
            (PROJECT_ROOT / notebook_path).read_text(encoding="utf-8")
        )
        canonical_source = "".join(canonical["cells"][0]["source"])
        assert "notebook-pages-button" in canonical_source
        assert "vuelve a Pages" in canonical_source

        published = json.loads((tmp_path / notebook_path).read_text(encoding="utf-8"))
        published_source = "".join(
            "".join(cell.get("source", [])) for cell in published["cells"]
        )
        assert "notebook-pages-button" not in published_source
        assert "vuelve a Pages" not in published_source
        assert all(
            "piplite.install" not in "".join(cell.get("source", []))
            for cell in published["cells"]
        )
        assert published["metadata"]["kernelspec"]["name"] == "python"
        assert published["metadata"]["kernelspec"]["display_name"] == "Python (Pyodide)"
        assert all(
            cell["metadata"]["editable"] is False
            and cell["metadata"]["deletable"] is False
            for cell in published["cells"]
        )


def test_pages_copy_includes_chapter_two_runtime_and_notebooks(tmp_path):
    prepare_contents(tmp_path, chapter=2)
    for notebook_path in CHAPTER2_NOTEBOOKS:
        canonical = json.loads(
            (PROJECT_ROOT / notebook_path).read_text(encoding="utf-8")
        )
        assert "notebook-pages-button" in "".join(canonical["cells"][0]["source"])

        published = json.loads((tmp_path / notebook_path).read_text(encoding="utf-8"))
        assert all(
            "piplite.install" not in "".join(cell.get("source", []))
            for cell in published["cells"]
        )
        assert published["metadata"]["kernelspec"]["name"] == "python"
        assert published["metadata"]["kernelspec"]["display_name"] == "Python (Pyodide)"
        assert all(
            cell["metadata"]["editable"] is False
            and cell["metadata"]["deletable"] is False
            for cell in published["cells"]
        )
        assert all("notebook-pages-button" not in "".join(cell.get("source", []))
                   for cell in published["cells"])
    assert all((tmp_path / path).is_file() for path in CHAPTER2_RUNTIME_FILES)


def test_pages_copy_includes_every_remaining_book_simulation(tmp_path):
    for chapter in range(4, 9):
        chapter_dir = tmp_path / f"chapter-{chapter}"
        prepare_contents(chapter_dir, chapter=chapter)
        config = CHAPTER_CONFIGS[chapter]
        for notebook_path in config["notebooks"]:
            notebook = json.loads((chapter_dir / notebook_path).read_text(encoding="utf-8"))
            assert notebook["metadata"]["kernelspec"]["display_name"] == "Python (Pyodide)"
            assert all(
                cell["metadata"]["editable"] is False
                and cell["metadata"]["deletable"] is False
                for cell in notebook["cells"]
            )
            assert all(
                "piplite.install" not in "".join(cell.get("source", []))
                for cell in notebook["cells"]
            )
        assert all(
            (chapter_dir / path).is_file()
            for path in config["runtime_files"]
        )


def test_all_canonical_simulation_notebook_cells_are_read_only():
    notebook_paths = sorted(
        (PROJECT_ROOT / "simulaciones").glob("capitulo[2-8]/notebooks/*.ipynb")
    )

    assert notebook_paths
    for path in notebook_paths:
        notebook = json.loads(path.read_text(encoding="utf-8"))
        assert all(
            cell.get("metadata", {}).get("editable") is False
            and cell.get("metadata", {}).get("deletable") is False
            for cell in notebook.get("cells", [])
        ), path.relative_to(PROJECT_ROOT)


def test_chapter_seven_interpolation_notebook_avoids_unavailable_sklearn():
    notebook = json.loads(
        (
            PROJECT_ROOT
            / "simulaciones/capitulo7/notebooks/3_busqueda_interpolacion.ipynb"
        ).read_text(encoding="utf-8")
    )
    code = "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
    )

    assert "from sklearn" not in code
    assert "mse = np.mean((times - fit_values) ** 2)" in code


def test_all_remaining_simulation_pages_embed_their_matching_notebook():
    for (chapter, page_name), notebooks in PAGE_NOTEBOOKS.items():
        if chapter not in range(4, 9):
            continue
        page = (
            PROJECT_ROOT
            / f"docs/capitulos/capitulo-{chapter}/{page_name}.md"
        ).read_text(encoding="utf-8")
        assert "<!-- jupyterlite-demo:start -->" in page
        for notebook in notebooks:
            assert notebook_url(chapter, notebook) in page
        assert "Abrir en pantalla completa" in page
        assert "Abrir en Colab" in page
        before_demo = page.split("<!-- jupyterlite-demo:start -->", 1)[0]
        assert '<div class="lab-action">' not in before_demo


def test_chapter_three_embeds_the_jupyterlite_notebook():
    pages = (
        (
            "docs/capitulos/capitulo-3/0-comparacion-notaciones-asintoticas.md",
            NOTEBOOKS[0],
        ),
        *(
            (
                f"docs/capitulos/capitulo-3/{page_name}.md",
                notebook,
            )
            for page_name, notebook in zip(
                (
                    "1-notacion-big-o",
                    "2-notacion-little-o",
                    "3-notacion-big-omega",
                    "4-notacion-little-omega",
                    "5-notacion-theta",
                ),
                NOTEBOOKS[1:],
                strict=True,
            )
        ),
    )
    for page_path, notebook in pages:
        page = (PROJECT_ROOT / page_path).read_text(encoding="utf-8")
        assert "## Simulación en el navegador" in page
        assert "<!-- jupyterlite-demo:start -->" in page
        assert 'class="jupyterlite-demo__frame"' in page
        assert notebook_url(3, notebook) in page
        assert page.index("## Simulación en el navegador") < page.index(
            '<nav class="section-return section-step"'
        )
        assert page.index("<!-- local-execution:end -->") < page.index(
            "<!-- jupyterlite-demo:start -->"
        )
        demo = page.split("<!-- jupyterlite-demo:start -->", 1)[1].split(
            "<!-- jupyterlite-demo:end -->", 1
        )[0]
        toolbar = demo.split('<div class="jupyterlite-demo__toolbar">', 1)[1].split(
            "</div>", 1
        )[0]
        actions = demo.split('<div class="jupyterlite-demo__actions">', 1)[1].split(
            "</div>", 1
        )[0]
        assert toolbar.strip() == "<span>Simulación interactiva</span>"
        assert demo.index('class="jupyterlite-demo__actions"') < demo.index(
            'class="jupyterlite-demo__frame"'
        )
        assert ">Abrir en Colab</a>" in actions
        assert ">Abrir en pantalla completa</a>" in actions
        assert actions.index("Abrir en Colab") < actions.index(
            "Abrir en pantalla completa"
        )
        assert '<div class="lab-action">' not in page.split(
            "<!-- jupyterlite-demo:start -->", 1
        )[0]


def test_chapter_two_embeds_each_jupyterlite_simulation_without_duplicate_button():
    pages = (
        ("0-complejidad-sublineal", CHAPTER2_NOTEBOOKS[1]),
        ("1-complejidad-constante", CHAPTER2_NOTEBOOKS[0]),
        ("2-complejidad-logaritmica", CHAPTER2_NOTEBOOKS[1]),
        ("3-complejidad-lineal", CHAPTER2_NOTEBOOKS[2]),
        ("4-complejidad-log-lineal", CHAPTER2_NOTEBOOKS[3]),
        ("5-complejidad-cuadratica", CHAPTER2_NOTEBOOKS[4]),
        ("6-complejidad-cubica", CHAPTER2_NOTEBOOKS[5]),
        ("7-complejidad-polinomial-general", CHAPTER2_NOTEBOOKS[6]),
        ("8-complejidad-exponencial", CHAPTER2_NOTEBOOKS[7]),
        ("9-complejidad-factorial", CHAPTER2_NOTEBOOKS[8]),
    )
    for page_name, notebook in pages:
        page = (
            PROJECT_ROOT / f"docs/capitulos/capitulo-2/{page_name}.md"
        ).read_text(encoding="utf-8")
        assert "## Simulación en el navegador" in page
        assert notebook_url(2, notebook) in page
        assert page.index("<!-- local-execution:end -->") < page.index(
            "<!-- jupyterlite-demo:start -->"
        )
        assert page.index("<!-- jupyterlite-demo:start -->") < page.index(
            '<nav class="section-return section-step"'
        )
        assert '<div class="lab-action">' not in page.split(
            "<!-- jupyterlite-demo:start -->", 1
        )[0]
        demo = page.split("<!-- jupyterlite-demo:start -->", 1)[1].split(
            "<!-- jupyterlite-demo:end -->", 1
        )[0]
        actions = demo.split('<div class="jupyterlite-demo__actions">', 1)[1].split(
            "</div>", 1
        )[0]
        assert demo.index('class="jupyterlite-demo__actions"') < demo.index(
            'class="jupyterlite-demo__frame"'
        )
        assert ">Abrir en Colab</a>" in actions
        assert ">Abrir en pantalla completa</a>" in actions


def test_homepage_diagram_shows_jupyterlite_as_a_general_portal_feature():
    homepage = (PROJECT_ROOT / "docs/index.md").read_text(encoding="utf-8")

    assert "## Cómo se conectan los recursos" in homepage
    diagram = homepage.split("```mermaid", 1)[1].split("```", 1)[0]
    assert "JupyterLite" in diagram
    assert "Laboratorios interactivos" in diagram
    assert "Pyodide" in diagram
    assert "Ejecución en el navegador" in diagram
    assert "Google Colab" in diagram
    assert "Jupyter local" in diagram
    assert "Capítulos 2 y 3" not in diagram


def test_jupyterlite_actions_share_button_style_and_have_icons():
    styles = (
        PROJECT_ROOT / "docs/assets/stylesheets/extra.css"
    ).read_text(encoding="utf-8")
    assert ".jupyterlite-demo__actions a.md-button" in styles
    assert ".jupyterlite-button::before" in styles
    assert 'url("../images/fullscreen-icon.svg")' in styles
    assert (PROJECT_ROOT / "docs/assets/images/colab-icon.svg").is_file()
    assert (PROJECT_ROOT / "docs/assets/images/fullscreen-icon.svg").is_file()


def test_pages_workflow_builds_demo_after_content_validation():
    workflow = (PROJECT_ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
    build = "python desarrollo/scripts/build_jupyterlite_demo.py"
    breadcrumbs = "python desarrollo/scripts/validate_pages_breadcrumbs.py --site-dir site"
    upload = "uses: actions/upload-pages-artifact@7b1f4a764d45c48632c6b24a0339c27f5614fb0b"
    assert workflow.index(breadcrumbs) < workflow.index(build) < workflow.index(upload)


def test_breadcrumb_validation_ignores_jupyterlite_application_pages(tmp_path):
    pages_index = tmp_path / "index.html"
    pages_index.write_text(
        '<nav class="editorial-breadcrumb"></nav>', encoding="utf-8"
    )
    lite_index = tmp_path / "jupyterlite/graficas/notebooks/index.html"
    lite_index.parent.mkdir(parents=True)
    lite_index.write_text("<!doctype html>", encoding="utf-8")

    assert validate_breadcrumbs(tmp_path) == []


def test_documentation_dependencies_include_jupyter_server():
    requirements = (PROJECT_ROOT / "requirements-publish.txt").read_text(encoding="utf-8")
    lock = (PROJECT_ROOT / "requirements-lock.txt").read_text(encoding="utf-8")
    assert "jupyter-server==2.21.1" in requirements
    assert "jupyter-server==2.21.1" in lock
