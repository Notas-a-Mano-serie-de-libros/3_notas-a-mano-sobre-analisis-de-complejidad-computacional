from __future__ import annotations

import math
import re

import numpy as np
import sympy as sp


FUNCTIONS = {
    "zero": ("0", None),
    "constant": ("1", (0.0, 0.0)),
    "logarithmic": (r"\log_2(n)", (0.0, 1.0)),
    "linear": ("n", (1.0, 0.0)),
    "log_linear": (r"n\log_2(n)", (1.0, 1.0)),
    "quadratic": ("n^2", (2.0, 0.0)),
    "cubic": ("n^3", (3.0, 0.0)),
    "exponential": ("2^n", None),
    "factorial": ("n!", None),
}


def _function_data(function_type, degree):
    if function_type == "polynomial":
        return rf"n^{{{degree}}}", (float(degree), 0.0)
    if function_type == "polylogarithmic":
        polynomial_degree, log_power, log_base = degree
        return (
            rf"n^{{{polynomial_degree}}}"
            rf"\log_{{{log_base}}}^{{{log_power}}}(n)",
            (float(polynomial_degree), float(log_power)),
        )
    return FUNCTIONS[function_type]


def applicable_master_variants(coefficients, reductions, function_type, degree):
    """Return only the master-theorem versions supported by the recurrence."""
    _, profile = _function_data(function_type, degree)
    if profile is None:
        return []
    if len(coefficients) != 1:
        return [("Generalizado", "generalized")]
    _, log_power = profile
    variants = []
    if log_power == 0:
        variants.append(("Básico", "basic"))
    variants.extend([
        ("Extendido", "extended"),
        ("Generalizado", "generalized"),
    ])
    return variants


def _sympy_function(function_type, degree, argument):
    if function_type == "zero":
        return sp.Integer(0)
    if function_type == "constant":
        return sp.Integer(1)
    if function_type == "logarithmic":
        return sp.log(argument, 2)
    if function_type == "linear":
        return argument
    if function_type == "log_linear":
        return argument * sp.log(argument, 2)
    if function_type == "quadratic":
        return argument**2
    if function_type == "cubic":
        return argument**3
    if function_type == "polynomial":
        return argument**degree
    if function_type == "polylogarithmic":
        polynomial_degree, log_power, log_base = degree
        return (
            argument**polynomial_degree
            * sp.log(argument, log_base) ** log_power
        )
    if function_type == "exponential":
        return 2**argument
    return sp.factorial(argument)


def _latex_function(function_type, degree, argument):
    wrapped = rf"\left({argument}\right)"
    if function_type == "zero":
        return "0"
    if function_type == "constant":
        return "1"
    if function_type == "logarithmic":
        return rf"\log_2{wrapped}"
    if function_type == "linear":
        return wrapped
    if function_type == "log_linear":
        return rf"{wrapped}\log_2{wrapped}"
    if function_type == "quadratic":
        return rf"{wrapped}^2"
    if function_type == "cubic":
        return rf"{wrapped}^3"
    if function_type == "polynomial":
        return rf"{wrapped}^{{{degree}}}"
    if function_type == "polylogarithmic":
        polynomial_degree, log_power, log_base = degree
        return (
            rf"{wrapped}^{{{polynomial_degree}}}"
            rf"\log_{{{log_base}}}^{{{log_power}}}{wrapped}"
        )
    if function_type == "exponential":
        return rf"2^{{{wrapped}}}"
    return rf"{wrapped}!"


def _iterative_expansion(relation_type, a, reduction, function_type, degree):
    n = sp.symbols("n", positive=True)
    recurrence = sp.Function("C")
    lines = []
    for level in range(1, 7):
        if relation_type == "division":
            divisor = sp.Rational(str(1 / reduction))
            recursive_argument = n / divisor**level
            accumulated = sp.Add(*(
                sp.Integer(a) ** i
                * _sympy_function(function_type, degree, n / divisor**i)
                for i in range(level)
            ))
        else:
            decrement = sp.Integer(int(reduction))
            recursive_argument = n - level * decrement
            accumulated = sp.Add(*(
                sp.Integer(a) ** i
                * _sympy_function(function_type, degree, n - i * decrement)
                for i in range(level)
            ))
        expression = sp.Integer(a) ** level * recurrence(recursive_argument)
        expression += sp.simplify(accumulated)
        left_side = "C(n)&=" if level == 1 else "&="
        expression_latex = sp.latex(sp.simplify(expression), mul_symbol="dot")
        expression_latex = re.sub(
            r"(\d+(?:\.\d+)?)\s*\\cdot\s*(?=(?:C|n|k)\b)",
            r"\1",
            expression_latex,
        )
        lines.append(rf"{left_side}{expression_latex}")
    return r"\[\begin{aligned}" + r"\\[4pt]".join(lines) + r"\\[4pt]&=\cdots\end{aligned}\]"


def _theta(power, log_power=0, log_base=2):
    n_part = "1" if abs(power) < 1e-9 else (
        "n" if abs(power - 1) < 1e-9 else rf"n^{{{power:.4g}}}"
    )
    if abs(log_power) < 1e-9:
        return rf"\Theta\left({n_part}\right)"
    log_symbol = (
        r"\log_2"
        if math.isclose(log_base, 2)
        else rf"\log_{{{log_base:g}}}"
    )
    log_part = (
        rf"{log_symbol}(n)"
        if abs(log_power - 1) < 1e-9
        else rf"{log_symbol}^{{{log_power:.4g}}}(n)"
    )
    product = log_part if n_part == "1" else rf"{n_part}\cdot {log_part}"
    return rf"\Theta\left({product}\right)"


def _n_power(power):
    if abs(power) < 1e-9:
        return "1"
    if abs(power - 1) < 1e-9:
        return "n"
    return rf"n^{{{power:.5g}}}"


def _panel(title, applies, body):
    status = "Aplica" if applies else "No aplica"
    status_class = "method-status-ok" if applies else "method-status-no"
    return (
        '<details class="recursion-info-section method-solution-panel" open>'
        f"<summary>{title} "
        f'<span class="{status_class}">{status}</span></summary>'
        f'<div class="method-solution-content">{body}</div>'
        "</details>"
    )


def _master_section(title, body, open_by_default=False):
    open_attribute = " open" if open_by_default else ""
    return (
        f'<details class="master-method-section"{open_attribute}>'
        f"<summary>{title}</summary>"
        f'<div class="master-method-section-content">{body}</div>'
        "</details>"
    )


def _asymptotic_division(a, factor, profile, log_base=2):
    critical = math.log(a, 1 / factor)
    if profile is None:
        return _theta(critical, log_base=log_base)
    degree, log_power = profile
    if degree < critical - 1e-9:
        return _theta(critical, log_base=log_base)
    if degree > critical + 1e-9:
        return _theta(degree, log_power, log_base)
    return _theta(degree, log_power + 1, log_base)


def _asymptotic_development(closed_form, asymptotic_result):
    original_expression = closed_form.replace("C(n)=", "", 1)
    return (
        r"\[\begin{aligned}"
        rf"C(n)&\in\Theta\left({original_expression}\right)\\[6pt]"
        rf"&\in{asymptotic_result}"
        r"\end{aligned}\]"
    )


def _division_closed_form(a, divisor, function_type, degree, base_case=1):
    f_latex, profile = _function_data(function_type, degree)
    log_base = degree[2] if function_type == "polylogarithmic" else 2
    j_latex = rf"\log_{{{divisor:g}}}(n)"
    critical = math.log(a, divisor)
    leaf = _n_power(critical)
    base_latex = f"{base_case:g}"
    leaf_term = (
        "0"
        if math.isclose(base_case, 0)
        else leaf
        if math.isclose(base_case, 1)
        else base_latex
        if leaf == "1"
        else rf"{base_latex}\cdot {leaf}"
    )
    work = _n_power(profile[0]) if profile is not None else "1"
    if function_type == "zero":
        return leaf, rf"C(n)={leaf_term}"
    if profile is None:
        return None
    power, log_power = profile
    ratio = a / (divisor**power)
    if math.isclose(ratio, 1.0):
        if log_power == 0:
            evaluated = "j" if work == "1" else rf"{work}\cdot j"
            accumulated_term = (
                j_latex if work == "1" else rf"{work}\cdot {j_latex}"
            )
            closed = rf"C(n)={leaf_term}+{accumulated_term}"
        else:
            evaluated = (
                rf"{work}\cdot\left[j\cdot\log_{{{log_base:g}}}(n)"
                rf"-\log_{{{log_base:g}}}({divisor:g})"
                rf"\frac{{j(j-1)}}{{2}}\right]"
            )
            closed = (
                rf"C(n)={leaf_term}+{work}\cdot\left["
                rf"{j_latex}\cdot\log_{{{log_base:g}}}(n)"
                rf"-\log_{{{log_base:g}}}({divisor:g})"
                rf"\frac{{{j_latex}({j_latex}-1)}}{{2}}\right]"
            )
    else:
        ratio_latex = f"{ratio:.6g}"
        geometric = rf"\frac{{1-{ratio_latex}^j}}{{1-{ratio_latex}}}"
        if log_power == 0:
            evaluated = geometric if work == "1" else rf"{work}\cdot {geometric}"
            closed = (
                rf"C(n)={leaf_term}+"
                + ("" if work == "1" else rf"{work}\cdot ")
                + rf"\frac{{1-{ratio_latex}^{{{j_latex}}}}}{{1-{ratio_latex}}}"
            )
        else:
            weighted = (
                rf"\frac{{{ratio_latex}-j{ratio_latex}^j"
                rf"+(j-1){ratio_latex}^{{j+1}}}}{{(1-{ratio_latex})^2}}"
            )
            evaluated = (
                rf"{work}\cdot\left[\log_{{{log_base:g}}}(n)"
                rf"\cdot {geometric}-\log_{{{log_base:g}}}({divisor:g})"
                rf"\cdot {weighted}\right]"
            )
            closed = (
                rf"C(n)={leaf_term}+"
                + evaluated.replace("j", j_latex)
            )
    return evaluated, closed


def _reduction_closed_form(a, decrement, function_type, degree, base_case=1):
    f_latex, profile = _function_data(function_type, degree)
    if function_type == "zero":
        exact = (
            rf"C(n)={base_case:g}\cdot"
            rf"{a:g}^{{(n-1)/{decrement:g}}}"
        )
        return "0", exact
    if profile is None or profile[1] != 0:
        return None
    power = int(profile[0])
    n, i, j = sp.symbols("n i j", integer=True, nonnegative=True)
    a_sym = sp.Integer(int(a))
    decrement_sym = sp.Integer(int(decrement))
    summand = a_sym**i * (n - decrement_sym * i) ** power
    evaluated = sp.simplify(sp.summation(summand, (i, 0, j - 1)))
    if evaluated.has(sp.Sum):
        return None
    j_value = sp.Rational(1, int(decrement)) * (n - 1)
    base_sym = sp.Rational(str(base_case))
    closed = sp.simplify(base_sym * a_sym**j + evaluated)
    closed = sp.simplify(closed.subs(j, j_value))
    return (
        sp.latex(evaluated, mul_symbol="dot"),
        rf"C(n)={sp.latex(closed, mul_symbol='dot')}",
    )


def _iterative(
    relation_type, coefficients, reductions, function_type, degree, base_case=1
):
    title = "Sustitución iterativa"
    f_latex, profile = _function_data(function_type, degree)
    if len(coefficients) != 1:
        return _panel(
            title,
            False,
            "<p><b>Forma requerida para este desarrollo:</b> una sola cadena recursiva, "
            r"\(C(n)=aC(g(n))+f(n)\).</p>"
            "<p>La relación seleccionada contiene varios términos recursivos. Cada "
            "sustitución produce ramas con argumentos diferentes, por lo que no existe "
            "un único índice de expansión que lleve simultáneamente todos los términos "
            "al caso base. No puede aplicarse el procedimiento iterativo uniforme "
            "desarrollado en el capítulo.</p>",
        )
    a, reduction = coefficients[0], reductions[0]
    if relation_type == "division":
        divisor = 1 / reduction
        closed_data = _division_closed_form(
            a, divisor, function_type, degree, base_case
        )
        if closed_data is None:
            return _panel(
                title,
                False,
                rf"<p>La recurrencia puede expandirse, pero para "
                rf"\(f(n)={f_latex}\) la sumatoria resultante no pertenece a las "
                "series geométricas o aritmético-geométricas evaluadas por este "
                "procedimiento. Como no se obtiene una forma cerrada, el método "
                "no se considera aplicable analíticamente en esta animación.</p>",
            )
        evaluated_sum, closed_form = closed_data
        expansion = _iterative_expansion(
            relation_type, a, reduction, function_type, degree
        )
        general_sum = evaluated_sum.replace("j", "k").replace(r"\cdot k", "k")
        evaluated_at_base = evaluated_sum.replace(
            "j", rf"\log_{{{divisor:g}}}(n)"
        )
        recursive_factor = rf"{a:g}^{{\log_{{{divisor:g}}}(n)}}"
        body = (
            rf"<p><b>Paso 1: Expandir la relación</b></p>"
            + expansion
            + rf"<p><b>Paso 2: Obtener la expresión general</b></p>"
            rf"\[C(n)={a:g}^kC\left(\frac{{n}}{{{divisor:g}^k}}\right)"
            rf"+{general_sum}\]"
            rf"<p><b>Paso 3: Alcanzar el caso base</b></p>"
            rf"\[\frac{{n}}{{{divisor:g}^k}}=1"
            rf"\quad\Rightarrow\quad k=\log_{{{divisor:g}}}(n)\]"
            rf"<p><b>Paso 4: Aplicar las condiciones iniciales</b></p>"
            rf"\[\begin{{aligned}}"
            rf"C(n)&={recursive_factor}\cdot C(1)+{evaluated_at_base}\\[6pt]"
            rf"&={recursive_factor}\cdot {base_case:g}+{evaluated_at_base}\\[6pt]"
            rf"&={closed_form.replace('C(n)=', '')}"
            rf"\end{{aligned}}\]"
            rf"<p><b>Resultado asintótico</b></p>"
            + _asymptotic_development(
                closed_form,
                _asymptotic_division(
                    a,
                    reduction,
                    profile,
                    degree[2] if function_type == "polylogarithmic" else 2,
                ),
            )
        )
    else:
        closed_data = _reduction_closed_form(
            a, reduction, function_type, degree, base_case
        )
        if closed_data is None:
            return _panel(
                title,
                False,
                rf"<p>La expansión existe, pero con \(f(n)={f_latex}\) no se obtiene "
                "una suma cerrada mediante las identidades polinómicas y geométricas "
                "implementadas. El procedimiento analítico se detiene antes de producir "
                r"una función explícita de \(n\).</p>",
            )
        evaluated_sum, closed_form = closed_data
        expansion = _iterative_expansion(
            relation_type, a, reduction, function_type, degree
        )
        general_sum = evaluated_sum.replace("j", "k").replace(r"\cdot k", "k")
        k_latex = rf"\frac{{n-1}}{{{reduction:g}}}"
        evaluated_at_base = evaluated_sum.replace("j", k_latex)
        recursive_factor = rf"{a:g}^{{{k_latex}}}"
        body = (
            rf"<p><b>Paso 1: Expandir la relación</b></p>"
            + expansion
            + rf"<p><b>Paso 2: Obtener la expresión general</b></p>"
            rf"\[C(n)={a:g}^kC(n-k\cdot{reduction:g})+{general_sum}\]"
            rf"<p><b>Paso 3: Alcanzar el caso base</b></p>"
            rf"\[n-k\cdot{reduction:g}=1"
            rf"\quad\Rightarrow\quad k=\frac{{n-1}}{{{reduction:g}}}\]"
            rf"<p><b>Paso 4: Aplicar las condiciones iniciales</b></p>"
            rf"\[\begin{{aligned}}"
            rf"C(n)&={recursive_factor}\cdot C(1)+{evaluated_at_base}\\[6pt]"
            rf"&={recursive_factor}\cdot {base_case:g}+{evaluated_at_base}\\[6pt]"
            rf"&={closed_form.replace('C(n)=', '')}"
            rf"\end{{aligned}}\]"
        )
    return _panel(title, True, body)


def _tree(relation_type, coefficients, reductions, function_type, degree, base_case=1):
    title = "Árbol de recurrencia"
    if len(set(reductions)) != 1:
        return _panel(
            title,
            False,
            "<p>El procedimiento analítico presentado en el capítulo requiere un árbol "
            "uniforme: todos los hijos deben reducir el problema de la misma manera.</p>"
            r"<p>Como existen valores \(b_i\) diferentes, una ruta alcanza un argumento "
            r"\(n\prod b_i\) distinto del de las otras rutas. Las hojas aparecen en "
            "profundidades diferentes y no existe un único costo por nivel que pueda "
            "sumarse con la fórmula del caso balanceado.</p>",
        )
    children = sum(coefficients)
    reduction = reductions[0]
    f_latex, _ = _function_data(function_type, degree)
    from capitulo5.recursion_tree_animation import _render_svg

    reduction_parameter = reduction if relation_type == "reduction" else 2
    symbolic_levels = {0: "0", 1: "1", 2: "2", 3: "k", 4: "h"}

    def symbolic_node_label(node):
        subscript = symbolic_levels[node["level"]]
        return rf"f(n_{{{subscript}}})"

    def symbolic_node_cost(node):
        level = node["level"]
        if relation_type == "division":
            divisor = 1 / reduction
            arguments = {
                0: "n",
                1: rf"\dfrac{{n}}{{{divisor:g}}}",
                2: rf"\dfrac{{n}}{{{divisor:g}^2}}",
                3: rf"\dfrac{{n}}{{{divisor:g}^k}}",
                4: "1",
            }
        else:
            arguments = {
                0: "n",
                1: rf"n-{reduction:g}",
                2: rf"n-2\cdot{reduction:g}",
                3: rf"n-k\cdot{reduction:g}",
                4: "1",
            }
        argument = arguments[level]
        if function_type == "linear":
            return argument
        return _latex_function(function_type, degree, argument)

    def cost_at_level(level):
        if relation_type == "division":
            divisor = 1 / reduction
            argument = "n" if level == 0 else rf"\dfrac{{n}}{{{divisor:g}^{level}}}"
        else:
            decrease = level * reduction
            argument = "n" if level == 0 else rf"n-{decrease:g}"
        if function_type == "linear":
            return argument
        return _latex_function(function_type, degree, argument)

    tree_svg = _render_svg(
        relation_type,
        children,
        reduction_parameter,
        4,
        True,
        function_type,
        degree,
        4,
        "solution-tree-arrow",
        tuple(coefficients),
        tuple(reductions),
        symbolic_node_label,
        "",
        symbolic_levels,
        3,
        4,
        symbolic_node_cost,
    )
    table_levels = (
        ("0", "1", cost_at_level(0)),
        ("1", f"{children}", cost_at_level(1)),
        ("2", rf"{children}^2", cost_at_level(2)),
        (
            "k",
            rf"{children}^k",
            (
                (
                    rf"\dfrac{{n}}{{{1 / reduction:g}^k}}"
                    if relation_type == "division"
                    else rf"n-k\cdot{reduction:g}"
                )
                if function_type == "linear"
                else _latex_function(
                    function_type,
                    degree,
                    (
                        rf"\dfrac{{n}}{{{1 / reduction:g}^k}}"
                        if relation_type == "division"
                        else rf"n-k\cdot{reduction:g}"
                    ),
                )
            ),
        ),
        (
            "h",
            rf"{children}^h",
            "1" if function_type == "linear"
            else _latex_function(function_type, degree, "1"),
        ),
    )
    level_table = (
        '<div class="recursion-level-table tree-method-level-table">'
        '<table><thead><tr><th><b>Nivel</b></th>'
        '<th><b>Número de nodos</b></th>'
        r'<th>\(\boldsymbol{f_i(n)}\)</th></tr></thead><tbody>'
        + "".join(
            rf'<tr data-level="{visible_level}">'
            rf"<td>\(\displaystyle {level}\)</td>"
            rf"<td>\(\displaystyle {nodes}\)</td>"
            rf"<td>\(\displaystyle {cost}\)</td></tr>"
            for visible_level, (level, nodes, cost) in enumerate(table_levels)
        )
        + "</tbody></table></div>"
    )
    if relation_type == "division":
        divisor = 1 / reduction
        argument_k = rf"\dfrac{{n}}{{{divisor:g}^k}}"
        node_cost = _latex_function(function_type, degree, argument_k)
        height_condition = (
            rf"\dfrac{{n}}{{{divisor:g}^h}}=1"
            rf"\quad\Rightarrow\quad h=\log_{{{divisor:g}}}(n)"
        )
    else:
        argument_k = rf"n-k\cdot{reduction:g}"
        node_cost = _latex_function(function_type, degree, argument_k)
        height_condition = (
            rf"n-h\cdot{reduction:g}=1"
            rf"\quad\Rightarrow\quad h=\dfrac{{n-1}}{{{reduction:g}}}"
        )
    level_cost = rf"{children}^k\cdot {node_cost}"
    if relation_type == "division":
        closed_data = _division_closed_form(
            children, divisor, function_type, degree, base_case
        )
        evaluated_sum = closed_data[0] if closed_data else None
        final_result = closed_data[1] if closed_data else None
        asymptotic_result = _asymptotic_division(
            children,
            reduction,
            _function_data(function_type, degree)[1],
            degree[2] if function_type == "polylogarithmic" else 2,
        )
        height_value = rf"\log_{{{divisor:g}}}(n)"
    else:
        closed_data = _reduction_closed_form(
            children, reduction, function_type, degree, base_case
        )
        evaluated_sum = closed_data[0] if closed_data else None
        final_result = closed_data[1] if closed_data else None
        asymptotic_result = None
        height_value = rf"\dfrac{{n-1}}{{{reduction:g}}}"
    sum_at_height = evaluated_sum.replace("j", "(h+1)") if evaluated_sum else None
    evaluated_at_height = (
        evaluated_sum.replace("j", rf"\left({height_value}+1\right)")
        if evaluated_sum else None
    )
    body = (
        rf"<p><b>Paso 1: Construir el árbol de recurrencia</b></p>"
        + tree_svg
        + rf"<p><b>Paso 2: Calcular el costo del nivel "
        rf"\(\boldsymbol{{k}}\)</b></p>"
        + level_table
        + rf"<p>El tamaño de cada subproblema en el nivel \(k\) es "
        rf"\({argument_k}\). Como \(f(n)={f_latex}\), el costo de cada nodo es:</p>"
        rf"\[f_k(n)={node_cost}\]"
        rf"<p>El número de nodos existentes en ese nivel es:</p>"
        rf"\[\#_{{\mathrm{{nodos}}}}={children}^k\]"
        rf"<p>El costo total del nivel se obtiene multiplicando ambas expresiones:</p>"
        rf"\[C_k(n)=\#_{{\mathrm{{nodos}}}}\cdot f_k(n)"
        rf"={level_cost}\]"
        rf"<p><b>Paso 3: Determinar el último nivel</b></p>"
        rf"<p>El árbol finaliza cuando el tamaño del subproblema alcanza el caso base:</p>"
        rf"\[{height_condition}\]"
        rf"<p><b>Paso 4: Sumar el costo de todos los niveles</b></p>"
        rf"\[\begin{{aligned}}"
        rf"C(n)&=\sum_{{k=0}}^{{h}}C_k(n)\\[6pt]"
        rf"&=\sum_{{k=0}}^{{h}}{level_cost}"
        rf"\end{{aligned}}\]"
        + (
            rf"<p><b>Paso 5: Resolver la expresión obtenida</b></p>"
            rf"\[\begin{{aligned}}"
            rf"C(n)&={sum_at_height}\\[6pt]"
            rf"&={evaluated_at_height}\\[6pt]"
            rf"&={final_result.replace('C(n)=', '')}"
            rf"\end{{aligned}}\]"
            + (
                rf"<p><b>Resultado asintótico</b></p>"
                + _asymptotic_development(final_result, asymptotic_result)
                if asymptotic_result
                else ""
            )
            if final_result
            else (
                "<p>La suma por niveles queda definida, pero la función seleccionada "
                "no admite una evaluación cerrada dentro del catálogo implementado.</p>"
            )
        )
    )
    return _panel(title, True, body)


def _akra_root(coefficients, reductions):
    low, high = 0.0, 32.0
    for _ in range(120):
        middle = (low + high) / 2
        value = sum(a * b**middle for a, b in zip(coefficients, reductions))
        if value > 1:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def _master(
    relation_type, coefficients, reductions, function_type, degree, variant, base_case=1
):
    names = {"basic": "básico", "extended": "extendido", "generalized": "generalizado"}
    title = f"Teorema maestro {names[variant]}"
    f_latex, profile = _function_data(function_type, degree)
    selected_log_base = (
        float(degree[2]) if function_type == "polylogarithmic" else 2.0
    )
    if relation_type != "division":
        return _panel(
            title, False,
            r"<p>Las tres variantes requieren subproblemas multiplicativos "
            r"\(C(b_i n)\), con \(0&lt;b_i&lt;1\). La relación seleccionada reduce "
            r"el argumento mediante \(C(n-b_i)\), por lo que no cumple la forma requerida.</p>",
        )
    simple = len(coefficients) == 1
    if variant in {"basic", "extended"} and not simple:
        return _panel(
            title, False,
            r"<p>Esta variante exige un único término \(aC(n/b)\). La relación "
            "seleccionada contiene varios tamaños de subproblema; debe utilizarse "
            "la variante generalizada.</p>",
        )
    if profile is None:
        return _panel(
            title, False,
            rf"<p>La función \(f(n)={f_latex}\) no tiene la forma "
            r"\(\Theta(n^k)\) requerida por la variante básica ni la forma "
            r"\(\Theta\left(n^k\cdot\log_2^p(n)\right)\) tratada por las "
            r"variantes implementadas.</p>",
        )
    degree_n, log_power = profile
    if variant == "basic" and log_power != 0:
        return _panel(
            title, False,
            rf"<p>La variante básica requiere \(f(n)\in\Theta(n^k)\). "
            rf"La función seleccionada es \(f(n)={f_latex}\) e incluye un factor "
            "logarítmico. Selecciona la variante extendida.</p>",
        )
    if variant == "generalized":
        root = _akra_root(coefficients, reductions)
        if degree_n < root - 1e-9:
            integral_order = r"\Theta(1)"
            generalized_result = _theta(root, log_base=selected_log_base)
        elif degree_n > root + 1e-9:
            integral_order = (
                rf"\Theta\left(n^{{{degree_n-root:.4g}}}"
                rf"\cdot\log_{{{selected_log_base:g}}}^{{{log_power:g}}}(n)\right)"
            )
            generalized_result = _theta(
                degree_n, log_power, selected_log_base
            )
        else:
            integral_order = (
                rf"\Theta\left(\log_{{{selected_log_base:g}}}"
                rf"^{{{log_power+1:g}}}(n)\right)"
            )
            generalized_result = _theta(
                root, log_power + 1, selected_log_base
            )
        integral_numerator = rf"u^{{{degree_n:g}}}"
        if log_power:
            integral_numerator += (
                rf"\cdot\log_{{{selected_log_base:g}}}"
                rf"^{{{log_power:g}}}(u)"
            )
        equation = "+".join(
            rf"{a:g}\cdot({b:g})^p" for a, b in zip(coefficients, reductions)
        )
        general_solution = (
            rf"\[C(n)\in\Theta\left(n^p\left(1+"
            rf"\int_1^n\frac{{f(u)}}{{u^{{p+1}}}}\,du\right)\right)\]"
        )
        procedure = (
            rf"<p><b>1. Identificar los parámetros.</b></p>"
            rf"\[a_i={tuple(coefficients)},\qquad b_i={tuple(reductions)},"
            rf"\qquad f(n)={f_latex}\]"
            rf"<p><b>2. Resolver la ecuación para "
            rf"\(\boldsymbol{{p}}\).</b></p>"
            rf"\[{equation}=1\Longrightarrow p\approx {root:.5g}\]"
            rf"<p><b>3. Definir la integral.</b></p>"
            rf"\[I=\int_1^n\frac{{f(u)}}{{u^{{p+1}}}}\,du"
            rf"=\int_1^n\frac{{{integral_numerator}}}"
            rf"{{u^{{{root+1:.5g}}}}}\,du\]"
            rf"<p><b>4. Evaluar el orden de la integral.</b></p>"
            rf"\[I\in{integral_order}\]"
            rf"<p><b>5. Sustituir en la forma general.</b></p>"
            rf"\[C(n)\in{generalized_result}\]"
        )
        body = (
            _master_section("Solución general", general_solution)
            + _master_section(
                "Aplicación a la relación seleccionada", procedure, True
            )
        )
        return _panel(title, True, body)
    a, factor = coefficients[0], reductions[0]
    divisor = 1 / factor
    critical = math.log(a, divisor)

    def master_theta(power, logarithm_power=0):
        n_part = _n_power(power)
        if not logarithm_power:
            return rf"\Theta\left({n_part}\right)"
        logarithm = (
            rf"\log_{{{selected_log_base:g}}}(n)"
            if math.isclose(logarithm_power, 1)
            else (
                rf"\log_{{{selected_log_base:g}}}"
                rf"^{{{logarithm_power:g}}}(n)"
            )
        )
        product = logarithm if n_part == "1" else rf"{n_part}\cdot {logarithm}"
        return rf"\Theta\left({product}\right)"

    if degree_n < critical - 1e-9:
        case = "Caso 1: domina el costo de las hojas"
        case_number = 1
        comparison_symbol = ">"
        result = master_theta(critical)
    elif degree_n > critical + 1e-9:
        case = "Caso 3: domina el costo externo"
        case_number = 3
        comparison_symbol = r"\lt"
        result = master_theta(degree_n, log_power)
    else:
        case = "Caso 2: ambos costos tienen el mismo orden"
        case_number = 2
        comparison_symbol = "="
        result = master_theta(degree_n, log_power + 1)
    if variant == "basic":
        cases = (
            r"\[C(n)\in\left\{\begin{array}{ll@{\hspace{3em}}l}"
            r"\Theta\left(n^{\log_b(a)}\right)"
            r" & \text{si } f(n)\in O\left(n^{\log_b(a)}\right)"
            r" & \text{(Caso 1)}\\[10pt]"
            r"\Theta\left(n^{\log_b(a)}\cdot\log_b(n)\right)"
            r" & \text{si } f(n)\in\Theta\left(n^{\log_b(a)}\right)"
            r" & \text{(Caso 2)}\\[10pt]"
            r"\Theta\left(f(n)\right)"
            r" & \text{si } f(n)\in\Omega\left(n^{\log_b(a)}\right)"
            r"\text{ y }a\cdot f\left(\dfrac{n}{b}\right)\leq c\cdot f(n)"
            r" & \text{(Caso 3)}"
            r"\end{array}\right.\]"
        )
    else:
        cases = (
            r'<h5 class="method-case-heading">Caso 1 '
            r"\(\boldsymbol{\left(a>b^k\right)}\):</h5>"
            r"\[C(n)\in\Theta\left(n^{\log_b(a)}\right)\]"
            r'<h5 class="method-case-heading">Caso 2 '
            r"\(\boldsymbol{\left(a=b^k\right)}\):</h5>"
            r"\[C(n)\in\begin{cases}"
            r"\Theta\left(n^k\cdot\log_b^{(p+1)}(n)\right)"
            r" & \text{si }p>-1\\[10pt]"
            r"\Theta\left(n^k\cdot\log_b\left(\log_b(n)\right)\right)"
            r" & \text{si }p=-1\\[10pt]"
            r"\Theta\left(n^k\right)"
            r" & \text{si }p<-1"
            r"\end{cases}\]"
            r'<h5 class="method-case-heading">Caso 3 '
            r"\(\boldsymbol{\left(a\lt b^k\right)}\):</h5>"
            r"\[C(n)\in\begin{cases}"
            r"\Theta\left(n^k\cdot\log_b^p(n)\right)"
            r" & \text{si }p\geq 0\\[10pt]"
            r"\Theta\left(n^k\right)"
            r" & \text{si }p<0"
            r"\end{cases}\]"
        )
    procedure = (
        rf"<p><b>1. Identificar los parámetros.</b></p>"
        rf"\[a={a:g},\qquad b={divisor:g},\qquad f(n)={f_latex},"
        rf"\qquad k={degree_n:g},\qquad p={log_power:g}\]"
        rf"<p><b>2. Calcular el costo crítico.</b></p>"
        rf"\[n^{{\log_b(a)}}=n^{{\log_{{{divisor:g}}}({a:g})}}"
        rf"=n^{{{critical:.5g}}}\]"
        rf"<p><b>3. Comparar \(\boldsymbol{{f(n)}}\) con el costo crítico.</b></p>"
        + (
            rf"\[n^{{\log_b(a)}}\;{comparison_symbol}\;f(n)"
            rf"\qquad\text{{(Caso {case_number})}}\]"
            if variant == "basic"
            else rf'<p class="method-step-description">{case}.</p>'
        )
        + (
            rf"<p><b>4. Verificar regularidad.</b></p>"
            rf"\[a\cdot f\left(\dfrac{{n}}{{b}}\right)"
            rf"\leq {a/(divisor**degree_n):.5g}\cdot f(n),"
            rf"\qquad {a/(divisor**degree_n):.5g}&lt;1\]"
            if degree_n > critical + 1e-9 else ""
        )
        + rf"<p><b>5. Aplicar el caso correspondiente.</b></p>"
        rf"\[C(n)\in {result}\]"
        rf"<p>El caso base \(C(1)={base_case:g}\) modifica únicamente la "
        rf"constante multiplicativa y no el orden asintótico.</p>"
    )
    body = (
        _master_section("Solución general", cases)
        + _master_section(
            "Aplicación a la relación seleccionada", procedure, True
        )
    )
    return _panel(title, True, body)


def _characteristic(
    relation_type, coefficients, reductions, function_type, degree, base_case=1
):
    title = "Ecuación característica"
    if relation_type != "reduction":
        return _panel(
            title, False,
            r"<p>El método requiere retardos enteros \(C(n-i)\) y coeficientes "
            r"constantes. Los términos seleccionados tienen la forma \(C(b_i n)\), "
            "por lo que no producen un polinomio característico de grado fijo.</p>",
        )
    if any(not float(value).is_integer() for value in reductions):
        return _panel(title, False, r"<p>Todos los retardos \(b_i\) deben ser enteros.</p>")
    f_latex, profile = _function_data(function_type, degree)
    if function_type in {
        "logarithmic", "log_linear", "polylogarithmic", "factorial"
    }:
        return _panel(
            title, False,
            rf"<p>La parte homogénea sí puede construirse, pero \(f(n)={f_latex}\) "
            "no pertenece a las formas de solución particular desarrolladas en la "
            "tabla del capítulo. No puede completarse el procedimiento con ese catálogo.</p>",
        )
    order = int(max(reductions))
    polynomial = [0.0] * (order + 1)
    polynomial[0] = 1.0
    for coefficient, lag in zip(coefficients, reductions):
        polynomial[int(lag)] -= coefficient
    roots = np.roots(polynomial)
    roots_latex = ", ".join(
        f"{root.real:.5g}" if abs(root.imag) < 1e-9
        else f"{root.real:.5g}{root.imag:+.5g}i"
        for root in roots
    )
    terms = "".join(
        rf"-{coefficient:g}x^{{{order-int(lag)}}}"
        for coefficient, lag in zip(coefficients, reductions)
    )
    dominant = max(abs(root) for root in roots)
    n_symbol = sp.symbols("n", integer=True)
    recurrence_function = sp.Function("C")
    recurrence_equation = recurrence_function(n_symbol) - sum(
        sp.Integer(int(coefficient))
        * recurrence_function(n_symbol - int(lag))
        for coefficient, lag in zip(coefficients, reductions)
    ) - _sympy_function(function_type, degree, n_symbol)
    initial_conditions = {
        recurrence_function(index): sp.Rational(str(base_case))
        for index in range(1, order + 1)
    }
    exact_solution = sp.rsolve(
        recurrence_equation,
        recurrence_function(n_symbol),
        initial_conditions,
    )
    if exact_solution is None:
        return _panel(
            title,
            False,
            "<p>La ecuación característica y sus raíces pueden construirse, pero "
            "el solucionador simbólico no encontró una expresión cerrada compatible "
            "con el término externo y los casos base seleccionados.</p>",
        )
    verification = sp.simplify(
        recurrence_equation.replace(
            lambda expression: (
                expression.is_Function
                and expression.func == recurrence_function
            ),
            lambda expression: exact_solution.subs(
                n_symbol, expression.args[0]
            ),
        )
    )
    exact_latex = sp.latex(sp.simplify(exact_solution))
    if function_type == "zero":
        particular = r"C_p(n)=0"
    elif function_type == "exponential":
        particular = (
            r"C_p(n)=B2^n"
            + (r"\text{, multiplicada por }n^s\text{ si }2\text{ es raíz de multiplicidad }s")
        )
    else:
        polynomial_degree = profile[0]
        particular = (
            rf"C_p(n)=B_{{{polynomial_degree:g}}}n^{{{polynomial_degree:g}}}"
            rf"+\cdots+B_1n+B_0"
        )
    body = (
        rf"<p><b>1. Separar la parte homogénea.</b> "
        rf"\(C_h(n)=\sum_i a_iC_h(n-b_i)\).</p>"
        rf"<p><b>2. Proponer "
        rf"\(\boldsymbol{{C_h(n)=x^n}}\).</b> Al sustituir y dividir por "
        rf"\(x^{{n-{order}}}\):</p>"
        rf"\[P(x)=x^{{{order}}}{terms}=0.\]"
        rf"<p><b>3. Calcular las raíces.</b> \(r_i\approx {roots_latex}\).</p>"
        rf"<p><b>4. Construir la solución homogénea.</b> Para raíces simples:</p>"
        rf"\[C_h(n)=\sum_i A_ir_i^n.\]"
        rf"<p>Una raíz \(r\) de multiplicidad \(s\) aporta "
        rf"\((A_0+A_1n+\cdots+A_{{s-1}}n^{{s-1}})r^n\).</p>"
        rf"<p><b>5. Proponer la solución particular.</b></p>"
        rf"\[{particular}.\]"
        rf"<p>Se sustituye \(C_p(n)\) en la recurrencia y se igualan coeficientes "
        rf"para hallar los valores \(B_i\).</p>"
        rf"<p><b>6. Formar la solución completa.</b></p>"
        rf"<p>Se utilizan los casos base "
        rf"\(C(1)=\cdots=C({order})={base_case:g}\) para determinar las constantes.</p>"
        rf"\[C(n)={exact_latex}\]"
        rf"<p><b>7. Verificar la solución.</b></p>"
        rf"\[\text{{residuo}}={sp.latex(verification)}\]"
        rf"<p>La raíz homogénea dominante tiene módulo \({dominant:.5g}\).</p>"
    )
    return _panel(title, True, body)


def solve_selected_method(
    relation_type,
    coefficients,
    reductions,
    function_type,
    degree,
    method,
    master_variant,
    base_case=1,
):
    if method == "iterative":
        return _iterative(
            relation_type, coefficients, reductions, function_type, degree, base_case
        )
    if method == "tree":
        return _tree(
            relation_type, coefficients, reductions, function_type, degree, base_case
        )
    if method == "master":
        return _master(
            relation_type, coefficients, reductions, function_type, degree,
            master_variant, base_case,
        )
    return _characteristic(
        relation_type, coefficients, reductions, function_type, degree, base_case
    )


SOLUTION_STYLES = """
<style>
.method-solution-panel summary{display:flex;align-items:center;gap:9px;font-size:16px;
line-height:1.45}
.method-status-ok,.method-status-no{display:inline-block;padding:2px 7px;border-radius:999px;
font:600 13px/1.4 system-ui,sans-serif}
.method-status-ok{color:#166534;background:#dcfce7}
.method-status-no{color:#991b1b;background:#fee2e2}
.method-solution-content{box-sizing:border-box;width:100%;max-width:100%;padding:12px 18px;
color:#333;overflow:visible;font-size:16px;line-height:1.55}
.method-solution-content p{max-width:100%;margin:8px 0;white-space:normal;
overflow-wrap:anywhere;font-size:16px!important;line-height:1.55}
.method-step-description{font-weight:400!important}
.method-solution-content table{font-size:16px;line-height:1.55}
.method-solution-heading,.method-case-heading{display:block;width:100%;margin:14px 0 6px;
line-height:1.35}
.method-solution-heading{font-size:17px}.method-case-heading{font-size:16px}
.master-method-section{box-sizing:border-box;width:100%;margin:0;
border:1px solid #dedede;border-bottom:0;border-radius:0;background:#fff;
overflow:hidden}
.master-method-section:first-child{border-radius:4px 4px 0 0}
.master-method-section:last-child{border-bottom:1px solid #dedede;
border-radius:0 0 4px 4px}
.master-method-section>summary{box-sizing:border-box;width:100%;padding:9px 12px;
cursor:pointer;background:#f7f7f7;font-size:16px;font-weight:700;line-height:1.45}
.master-method-section[open]>summary{border-bottom:1px solid #e2e2e2}
.master-method-section-content{box-sizing:border-box;width:100%;padding:8px 12px}
.method-solution-content mjx-container{max-width:100%!important;overflow:visible!important;
font-size:16px!important}
.method-solution-content mjx-container[display="true"]{font-size:20px!important;
line-height:1.5!important;margin:14px 0!important}
.method-solution-content mjx-container>svg{display:block;max-width:100%!important;height:auto}
.method-solution-content .recursion-tree-plot-wrap,
.method-solution-content .recursion-tree-figure{box-sizing:border-box;width:100%!important;
max-width:100%!important;overflow:visible!important}
.method-solution-content .recursion-tree-plot-wrap{min-height:0!important;
border:0!important;background:transparent!important}
.method-solution-content .recursion-tree-figure,
.method-solution-content .recursion-tree-figure>svg{background:transparent!important}
.method-solution-panel .tree-node-equation{font-size:16px}
.method-solution-panel .level-label{font-size:16px}
.tree-method-level-table{margin:12px 0}
.tree-method-level-table th{font-weight:700!important}
</style>
"""
