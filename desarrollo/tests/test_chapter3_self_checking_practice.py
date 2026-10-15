from __future__ import annotations

from desarrollo.tests.helpers import PROJECT_ROOT

PAGE = PROJECT_ROOT / "docs/capitulos/capitulo-3/practica-autocorregible.md"
SCRIPT = PROJECT_ROOT / "docs/assets/javascripts/chapter3-practice.js"


def test_practice_is_published_after_the_book_exercises():
    nav = (PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    chapter = (PROJECT_ROOT / "docs/capitulos/capitulo-3.md").read_text(encoding="utf-8")
    exercises = (PROJECT_ROOT / "docs/capitulos/capitulo-3/ejercicios-propuestos.md").read_text(encoding="utf-8")

    assert nav.index("capitulo-3/ejercicios-propuestos.md") < nav.index("capitulo-3/practica-autocorregible.md")
    assert 'href="practica-autocorregible/"' in chapter
    assert 'href="../practica-autocorregible/"' in exercises
    assert PAGE.is_file()


def test_practice_covers_four_skills_and_keeps_progress_locally():
    page = PAGE.read_text(encoding="utf-8")
    script = SCRIPT.read_text(encoding="utf-8")

    for skill in ("dominant", "relations", "limits", "witnesses"):
        assert f'data-practice-mode="{skill}"' in page
        assert f'data-mastery="{skill}"' in page
    assert "localStorage.getItem" in script
    assert "localStorage.setItem" in script
    assert "fetch(" not in script


def test_questions_are_random_and_never_repeat_while_progress_is_kept():
    script = SCRIPT.read_text(encoding="utf-8")

    assert "crypto?.getRandomValues" in script
    assert "nextUniqueQuestion(mode, state)" in script
    assert "new Set(state.seen[mode])" in script
    assert "state.seen[mode].push(question.signature)" in script
    assert "saveState(panel, state)" in script
    assert "fallbackQuestion" in script


def test_limit_exercises_connect_the_limit_with_the_strongest_relation():
    script = SCRIPT.read_text(encoding="utf-8")

    assert "renderLimits" in script
    assert "evaluateLimits" in script
    assert r"\\lim_{n\\to\\infty}" in script
    assert 'zero: "o"' in script
    assert 'positive: "Theta"' in script
    assert 'infinity: "omega"' in script


def test_every_practice_button_has_an_icon_and_actions_share_button_style():
    page = PAGE.read_text(encoding="utf-8")

    buttons = [line for line in page.splitlines() if "<button" in line]
    assert len(buttons) == 8
    assert all('self-check-practice__button-icon' in button for button in buttons)
    assert 'class="md-button md-button--primary"' in page
    assert 'class="md-button self-check-practice__secondary" type="button" data-practice-hint' in page


def test_static_witness_symbols_use_mathematical_html():
    page = PAGE.read_text(encoding="utf-8")

    assert "Testigos (<var>c</var>, <var>n</var><sub>0</sub>)" in page
    assert "valores de <var>c</var> y <var>n</var><sub>0</sub>" in page
    assert "(c,n_0)" not in page


def test_practice_requires_all_relations_and_accepts_non_unique_witnesses():
    script = SCRIPT.read_text(encoding="utf-8")

    assert "sameSet(selected, question.answer)" in script
    assert "c <= question.a" in script
    assert "c >= question.a" in script
    assert "Math.ceil((question.b / (c - question.a))" in script
    assert "Math.ceil((question.b / (question.a - c))" in script
    assert "El primer requisito que falla" in script


def test_dynamic_equations_are_typeset_with_mathjax():
    script = SCRIPT.read_text(encoding="utf-8")

    assert "MathJax?.typesetClear" in script
    assert "MathJax?.typesetPromise" in script
    assert "\\\\log(n)" in script
    assert "\\\\log n" not in script
    assert "typesetMath(container)" in script
    assert "typesetMath(feedback)" in script
    assert '\\\\[C(n)=' in script
    assert "<sup>" not in script
    assert "${symbol} c\\\\cdot" in script


def test_practice_exposes_accessible_feedback_and_controls():
    page = PAGE.read_text(encoding="utf-8")

    assert 'role="status"' in page
    assert 'aria-live="polite"' in page
    assert 'aria-label="Tipo de ejercicio"' in page
    assert 'aria-pressed="true"' in page


def test_practice_has_specific_reading_guidance_and_closing_prompt():
    main = (PROJECT_ROOT / "docs/overrides/main.html").read_text(encoding="utf-8")
    closings = (PROJECT_ROOT / "docs/overrides/section_closings.html").read_text(encoding="utf-8")

    route = "capitulos/capitulo-3/practica-autocorregible.md"
    assert f'source == "{route}"' in main
    assert f'"{route}"' in closings
