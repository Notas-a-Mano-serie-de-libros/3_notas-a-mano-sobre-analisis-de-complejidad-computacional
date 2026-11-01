from __future__ import annotations

from desarrollo.tests.helpers import PROJECT_ROOT

PAGE = PROJECT_ROOT / "docs/capitulos/capitulo-2/practica-autocorregible.md"
SCRIPT = PROJECT_ROOT / "docs/assets/javascripts/chapter2-practice.js"
STYLESHEET = PROJECT_ROOT / "docs/assets/stylesheets/extra.css"


def test_chapter2_practice_is_published_after_proposed_exercises():
    nav = (PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    chapter = (PROJECT_ROOT / "docs/capitulos/capitulo-2.md").read_text(encoding="utf-8")
    exercises = (PROJECT_ROOT / "docs/capitulos/capitulo-2/ejercicios-propuestos.md").read_text(encoding="utf-8")

    assert nav.index("capitulo-2/ejercicios-propuestos.md") < nav.index("capitulo-2/practica-autocorregible.md")
    assert 'href="practica-autocorregible/"' in chapter
    assert 'href="../practica-autocorregible/"' in exercises
    assert PAGE.is_file()
    assert SCRIPT.is_file()


def test_chapter2_practice_covers_four_skills_and_canonical_formulas():
    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")

    for skill in ("properties", "canonical", "crossover", "viability"):
        assert f'data-practice-mode="{skill}"' in page
        assert f'data-mastery="{skill}"' in page
    assert "localStorage.getItem" in script
    assert "localStorage.setItem" in script
    assert "crypto?.getRandomValues" in script
    assert "nextUniqueQuestion(mode, state)" in script
    assert "t = T_0 \\cdot T(n)" in script or "T_0" in script
    assert "S_0" in script


def test_chapter2_practice_container_and_styles():
    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")
    stylesheet = STYLESHEET.read_text(encoding="utf-8")

    assert "data-chapter2-practice" in page
    assert "data-chapter2-practice" in script
    assert "self-check-practice" in stylesheet
    assert "self-check-practice__choices" in stylesheet
    assert "self-check-practice__feedback" in stylesheet
