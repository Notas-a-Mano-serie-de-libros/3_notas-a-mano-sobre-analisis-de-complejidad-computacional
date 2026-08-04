from capitulo5.runtime.recurrence_solution_methods import (
    SOLUTION_STYLES,
    applicable_master_variants,
    solve_selected_method,
)


def test_iterative_solution_contains_complete_sequence():
    markup = solve_selected_method(
        "division", (2,), (0.5,), "linear", 4, "iterative", "basic"
    )
    assert "Aplica" in markup
    assert "Paso 1: Expandir la relación" in markup
    assert "Paso 2: Obtener la expresión general" in markup
    assert r"6n + 64C" in markup
    assert r"C(n)=2^kC\left(\frac{n}{2^k}\right)+nk" in markup
    assert "Paso 3: Alcanzar el caso base" in markup
    assert r"\quad\Rightarrow\quad k=\log_{2}(n)" in markup
    assert r"C(n)&=2^{\log_{2}(n)}\cdot C(1)" in markup
    assert r"&=n+n\cdot \log_{2}(n)" in markup
    assert (
        r"C(n)&\in\Theta\left(n+n\cdot \log_{2}(n)\right)\\[6pt]"
        r"&\in\Theta\left(n\cdot \log_2(n)\right)"
    ) in markup


def test_iterative_substitutes_selected_quadratic_function():
    markup = solve_selected_method(
        "division", (2,), (0.5,), "quadratic", 4, "iterative", "basic"
    )
    assert "Paso 1: Expandir la relación" in markup
    assert r"C(n)=2^kC\left(\frac{n}{2^k}\right)" in markup
    assert r"n^{2}\cdot \frac{1-0.5^k}{1-0.5}" in markup


def test_iterative_rejects_family_without_closed_sum():
    markup = solve_selected_method(
        "division", (2,), (0.5,), "factorial", 4, "iterative", "basic"
    )
    assert "No aplica" in markup
    assert "no se obtiene una forma cerrada" in markup


def test_basic_master_rejects_mixed_subproblem_sizes():
    markup = solve_selected_method(
        "division", (1, 1), (0.5, 1 / 3), "linear", 4, "master", "basic"
    )
    assert "No aplica" in markup
    assert "varios tamaños de subproblema" in markup


def test_master_variant_choices_only_include_applicable_versions():
    assert applicable_master_variants(
        (2,), (0.5,), "linear", 4
    ) == [
        ("Básico", "basic"),
        ("Extendido", "extended"),
        ("Generalizado", "generalized"),
    ]
    assert applicable_master_variants(
        (2,), (0.5,), "log_linear", 4
    ) == [
        ("Extendido", "extended"),
        ("Generalizado", "generalized"),
    ]
    assert applicable_master_variants(
        (1, 1), (0.5, 1 / 3), "linear", 4
    ) == [("Generalizado", "generalized")]
    assert applicable_master_variants(
        (2,), (0.5,), "factorial", 4
    ) == []


def test_generalized_master_solves_mixed_division():
    markup = solve_selected_method(
        "division", (1, 1), (1 / 3, 2 / 3), "quadratic", 4,
        "master", "generalized",
    )
    assert "Aplica" in markup
    assert "Solución general" in markup
    assert "Aplicación a la relación seleccionada" in markup
    assert "Resolver la ecuación para" in markup
    assert "Definir la integral" in markup
    assert "Evaluar el orden de la integral" in markup
    assert "Sustituir en la forma general" in markup


def test_basic_master_shows_cases_before_complete_procedure():
    markup = solve_selected_method(
        "division", (2,), (0.5,), "linear", 4, "master", "basic"
    )

    assert (
        '<details class="master-method-section"><summary>Solución general</summary>'
        in markup
    )
    assert (
        '<details class="master-method-section" open><summary>'
        "Aplicación a la relación seleccionada</summary>" in markup
    )
    assert r"C(n)\in\left\{\begin{array}{ll@{\hspace{3em}}l}" in markup
    assert r"\Theta\left(n^{\log_b(a)}\cdot\log_b(n)\right)" in markup
    assert r"a\cdot f\left(\dfrac{n}{b}\right)\leq c\cdot f(n)" in markup
    assert r"\text{(Caso 1)}" in markup
    assert r"\text{(Caso 2)}" in markup
    assert r"\text{(Caso 3)}" in markup
    assert markup.index("Solución general") < markup.index(
        "1. Identificar los parámetros"
    )
    assert "5. Aplicar el caso correspondiente" in markup
    assert r"C(n)\in \Theta\left(n\cdot \log_{2}(n)\right)" in markup
    assert r"n^{1}.\]" not in markup
    assert r"3. Comparar \(\boldsymbol{f(n)}\) con el costo crítico." in markup
    assert r"n^{\log_b(a)}\;=\;f(n)\qquad\text{(Caso 2)}" in markup


def test_extended_master_matches_book_case_format():
    markup = solve_selected_method(
        "division", (2,), (0.5,), "log_linear", 4, "master", "extended"
    )

    assert r"Caso 1 \(\boldsymbol{\left(a>b^k\right)}\)" in markup
    assert r"Caso 2 \(\boldsymbol{\left(a=b^k\right)}\)" in markup
    assert r"Caso 3 \(\boldsymbol{\left(a\lt b^k\right)}\)" in markup
    assert "a<b^k" not in markup
    assert r"\Theta\left(n^k\cdot\log_b^{(p+1)}(n)\right)" in markup
    assert r"\Theta\left(n^k\cdot\log_b\left(\log_b(n)\right)\right)" in markup
    assert r"\Theta\left(n^k\cdot\log_b^p(n)\right)" in markup
    assert 'class="method-step-description"' in markup


def test_characteristic_rejects_division_relation():
    markup = solve_selected_method(
        "division", (2,), (0.5,), "linear", 4, "characteristic", "basic"
    )
    assert "No aplica" in markup
    assert "retardos enteros" in markup


def test_tree_method_shows_tree_level_cost_and_total_sum():
    markup = solve_selected_method(
        "division", (2,), (0.5,), "linear", 4, "tree", "basic"
    )
    assert "Paso 1: Construir el árbol de recurrencia" in markup
    assert "<svg" in markup
    assert "f(n_{0})" in markup
    assert "f(n_{k})" in markup
    assert "f(n_{h})" in markup
    assert "nivel k" in markup
    assert "nivel h" in markup
    assert "symbolic-jump" in markup
    assert "<th><b>Nivel</b></th>" in markup
    assert "<th><b>Número de nodos</b></th>" in markup
    assert r"<th>\(\boldsymbol{f_i(n)}\)</th>" in markup
    assert "tree-node-cost-tooltip" in markup
    assert r">\(n\)</div>" in markup
    assert r">\(\dfrac{n}{2}\)</div>" in markup
    assert "Costo:" not in markup
    assert r"<td>\(\displaystyle 1\)</td>" in markup
    assert r"\left(1\right)" not in markup
    assert r"<td>\(\displaystyle 0\)</td>" in markup
    assert r"<td>\(\displaystyle n\)</td>" in markup
    assert r"<td>\(\displaystyle k\)</td>" in markup
    assert r"<td>\(\displaystyle 2^k\)</td>" in markup
    assert '<tr data-level="0">' in markup
    assert '<tr data-level="4">' in markup
    assert "Paso 2: Calcular el costo del nivel" in markup
    assert markup.index("Paso 2: Calcular el costo del nivel") < markup.index(
        '<div class="recursion-level-table tree-method-level-table">'
    )
    assert r"f_k(n)=\left(\dfrac{n}{2^k}\right)" in markup
    assert r"\#_{\mathrm{nodos}}=2^k" in markup
    assert r"C_k(n)=\#_{\mathrm{nodos}}\cdot f_k(n)" in markup
    assert "Paso 3: Determinar el último nivel" in markup
    assert r"\quad\Rightarrow\quad h=\log_{2}(n)" in markup
    assert r"h=\log_{2}(n)" in markup
    assert "Paso 4: Sumar el costo de todos los niveles" in markup
    assert r"C(n)&=\sum_{k=0}^{h}C_k(n)" in markup
    assert r"&=\sum_{k=0}^{h}2^k\cdot" in markup
    assert r"\sum_{k=0}^{h-1}" not in markup
    assert r"2^hC(1)" not in markup
    assert "Paso 5: Resolver la expresión obtenida" in markup
    assert r"&=n+n\cdot \log_{2}(n)" in markup
    assert "Cada nodo genera" not in markup


def test_method_explanation_has_no_internal_horizontal_scroll():
    assert "overflow-x:auto" not in SOLUTION_STYLES
    assert "overflow:visible!important" in SOLUTION_STYLES
    assert 'mjx-container[display="true"]{font-size:20px!important' in SOLUTION_STYLES


def test_base_case_is_used_in_complete_iterative_solution():
    markup = solve_selected_method(
        "division", (2,), (0.5,), "linear", 4, "iterative", "basic", 3
    )

    assert "Paso 4: Aplicar las condiciones iniciales</b>" in markup
    assert r"\boldsymbol{C(1)=3}" not in markup
    assert r"&=3\cdot n+n\cdot \log_{2}(n)" in markup


def test_characteristic_method_solves_constants_and_verifies_residual():
    markup = solve_selected_method(
        "reduction", (1, 1), (1, 2), "zero", 4,
        "characteristic", "basic", 1,
    )

    assert "Formar la solución completa" in markup
    assert r"C(1)=\cdots=C(2)=1" in markup
    assert r"\text{residuo}=0" in markup


def test_polylogarithmic_results_preserve_selected_logarithm_base():
    for method, variant in (
        ("iterative", None),
        ("tree", None),
        ("master", "extended"),
        ("master", "generalized"),
    ):
        markup = solve_selected_method(
            "division",
            (2,),
            (0.5,),
            "polylogarithmic",
            (2, 1, 3),
            method,
            variant,
            1,
        )

        assert r"\log_{3}" in markup
