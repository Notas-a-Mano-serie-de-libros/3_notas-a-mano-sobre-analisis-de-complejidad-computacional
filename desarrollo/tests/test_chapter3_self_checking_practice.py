from __future__ import annotations

from desarrollo.tests.helpers import PROJECT_ROOT

PAGE = PROJECT_ROOT / "docs/capitulos/capitulo-3/practica-autocorregible.md"
SCRIPT = PROJECT_ROOT / "docs/assets/javascripts/chapter3-practice.js"
STYLESHEET = PROJECT_ROOT / "docs/assets/stylesheets/extra.css"


def test_practice_is_published_after_the_book_exercises():
    nav = (PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    chapter = (PROJECT_ROOT / "docs/capitulos/capitulo-3.md").read_text(encoding="utf-8")
    exercises = (PROJECT_ROOT / "docs/capitulos/capitulo-3/ejercicios-propuestos.md").read_text(encoding="utf-8")

    assert nav.index("capitulo-3/ejercicios-propuestos.md") < nav.index("capitulo-3/practica-autocorregible.md")
    assert 'href="practica-autocorregible/"' in chapter
    assert 'href="../practica-autocorregible/"' in exercises
    assert PAGE.is_file()


def test_complementary_exercises_use_editorial_copy_and_centered_stats():
    page = PAGE.read_text(encoding="utf-8")
    nav = (PROJECT_ROOT / "mkdocs.yml").read_text(encoding="utf-8")
    stylesheet = STYLESHEET.read_text(encoding="utf-8")

    assert "# Ejercicios complementarios" in page
    assert "Ejercicios complementarios: capitulos/capitulo-3/practica-autocorregible.md" in nav
    assert "Estos ejercicios amplían la práctica del libro" in page
    assert "conserva su firma" not in page
    assert ".self-check-practice__stats div { display: grid; justify-items: center; text-align: center; }" in stylesheet
    assert "text-align: center; width: 100%;" in stylesheet


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


def test_action_buttons_have_icons_while_mode_tabs_use_descriptive_titles():
    page = PAGE.read_text(encoding="utf-8")

    buttons = [line for line in page.splitlines() if "<button" in line]
    assert len(buttons) == 8
    mode_buttons = [button for button in buttons if "data-practice-mode" in button]
    action_buttons = [button for button in buttons if "data-practice-mode" not in button]
    assert all('self-check-practice__button-icon' not in button for button in mode_buttons)
    assert all('self-check-practice__button-icon' in button for button in action_buttons)
    for title in ("Simplificar expresión", "Relación de crecimiento", "Demostración por límite", "Construcción de cota"):
        assert title in page
    assert 'class="md-button md-button--primary"' in page
    assert 'class="md-button self-check-practice__secondary" type="button" data-practice-hint' in page


def test_static_witness_symbols_use_mathematical_html():
    page = PAGE.read_text(encoding="utf-8")

    assert "Selección de valores para <var>c</var> y <var>n</var><sub>0</sub>" in page
    assert "valores de <var>c</var> y <var>n</var><sub>0</sub>" in page
    assert "(c,n_0)" not in page


def test_practice_requires_all_relations_and_accepts_non_unique_witnesses():
    script = SCRIPT.read_text(encoding="utf-8")

    assert "sameSet(selected, question.answer)" in script
    assert "c <= question.a" in script
    assert "c >= question.a" in script
    assert "witnessMinimum(question, c)" in script
    assert "El primer requisito que falla" in script


def test_generators_cover_non_polynomial_function_families_and_show_g():
    script = SCRIPT.read_text(encoding="utf-8")

    for family in ('key: "log"', 'key: "nlogn"', 'key: "exponential"', 'key: "factorial"'):
        assert family in script
    assert 'answer: "factorial"' in script
    assert 'answer: "linear"' in script
    assert "C(n)=${question.left}\\\\qquad g(n)=${question.right}" in script
    assert '["linear", "log", "nlogn", "poly"]' in script


def test_witness_exercise_has_a_synchronized_draggable_graph():
    script = SCRIPT.read_text(encoding="utf-8")
    stylesheet = STYLESHEET.read_text(encoding="utf-8")

    assert "data-witness-graph" in script
    assert "drawWitnessGraph" in script
    assert "setupWitnessGraph" in script
    assert 'addEventListener("input", redraw)' in script
    assert 'addEventListener("pointerdown"' in script
    assert 'addEventListener("pointermove"' in script
    assert "setPointerCapture" in script
    assert "C(n)" in script and "c\\\\cdot g(n)" in script
    assert 'curve: "#1565C0"' in script
    assert '"#B71C1C" : "#EF6C00"' in script
    assert 'n0: "#2E7D32"' in script
    assert "figcaption" not in script
    assert 'name="witness-view-start"' in script
    assert 'name="witness-view-end"' in script
    assert "niceTicks(minimumN, xMax, 5)" in script
    assert "data-witness-legend-c" in script
    assert "data-witness-legend-bound" in script
    assert "data-witness-legend-n0" in script
    assert "\\\\(n_0=${n0}\\\\)" in script
    assert "padding = { left: 86" in script
    assert "context.arc(handleX" not in script
    assert "context.arc(n0X" not in script
    assert "handleX, handleY, n0X" in script
    assert "Constante \\\\(\\\\mathbf{c}\\\\)" in script
    assert "Umbral \\\\(\\\\mathbf{n}_0\\\\)" in script
    assert "self-check-practice__formula--plain" in script
    assert ".self-check-practice__formula--plain { background: transparent" in stylesheet
    assert "box-sizing: border-box" in stylesheet
    assert "min-width: 0" in stylesheet


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
