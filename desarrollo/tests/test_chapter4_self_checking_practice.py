from __future__ import annotations

from desarrollo.tests.helpers import PROJECT_ROOT

PAGE = PROJECT_ROOT / "docs/capitulos/capitulo-4/practica-autocorregible.md"
SCRIPT = PROJECT_ROOT / "docs/assets/javascripts/chapter4-practice.js"
STYLESHEET = PROJECT_ROOT / "docs/assets/stylesheets/extra.css"


def test_chapter4_practice_is_published_after_proposed_exercises():
    nav = (PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    chapter = (PROJECT_ROOT / "docs/capitulos/capitulo-4.md").read_text(encoding="utf-8")
    exercises = (PROJECT_ROOT / "docs/capitulos/capitulo-4/ejercicios-propuestos.md").read_text(encoding="utf-8")

    assert nav.index("capitulo-4/ejercicios-propuestos.md") < nav.index("capitulo-4/practica-autocorregible.md")
    assert "capitulo-4/practica-autocorregible.md" in chapter
    assert 'href="../practica-autocorregible/"' in exercises
    assert PAGE.is_file()
    assert SCRIPT.is_file()


def test_chapter4_practice_covers_four_skills_and_local_progress():
    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")

    for skill in ("frequency", "cost", "asymptotic", "simulation"):
        assert f'data-practice-mode="{skill}"' in page
        assert f'data-mastery="{skill}"' in page
    assert "localStorage.getItem" in script
    assert "localStorage.setItem" in script
    assert "crypto?.getRandomValues" in script
    assert "nextUniqueQuestion(mode, state)" in script


def test_chapter4_practice_includes_code_boxes_and_simulation_controls():
    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    stylesheet = STYLESHEET.read_text(encoding="utf-8")

    assert "data-chapter4-practice" in page
    assert "self-check-practice__code-box" in script
    assert "self-check-practice__code-tabs" in script
    assert "self-check-practice__line-num" in script
    assert "self-check-practice__sim-row" in script
    assert "Pseudocódigo" in script
    assert "Java" in script
    assert '"c"' in script
    assert "Python" in script
    assert ".self-check-practice__code-box" in stylesheet
    assert ".self-check-practice__code-tabs" in stylesheet
    assert ".self-check-practice__line-num" in stylesheet
    assert ".self-check-practice__sim-results" in stylesheet

