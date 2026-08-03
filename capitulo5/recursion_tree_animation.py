from __future__ import annotations

import html
import builtins
import math
from fractions import Fraction
from functools import lru_cache

import ipywidgets as widgets
from IPython.display import Javascript, clear_output, display


try:
    from google.colab import output as _colab_output  # type: ignore
except (ImportError, ModuleNotFoundError):
    _colab_output = None


RUNNING_IN_COLAB = _colab_output is not None
SUBSCRIPT = str.maketrans("0123456789-", "₀₁₂₃₄₅₆₇₈₉₋")
SUPERSCRIPT = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")
MAX_VISIBLE_LEAVES = 128
NODE_RADIUS = 29
MINIMUM_LEAF_SPACING = 82
FUNCTION_LATEX = {
    "zero": "0",
    "constant": "1",
    "logarithmic": r"\log_2(n)",
    "linear": "n",
    "log_linear": r"n\cdot\log_2(n)",
    "quadratic": "n^2",
    "cubic": "n^3",
    "polynomial": "n^k",
    "polylogarithmic": r"n^k\cdot\log_\ell^p(n)",
    "exponential": "2^n",
    "factorial": "n!",
}

def _subscript(value):
    return str(value).translate(SUBSCRIPT)


def _superscript(value):
    return str(value).translate(SUPERSCRIPT)


def _visible_depth(branching_factor, requested_depth):
    if branching_factor <= 1:
        return requested_depth
    maximum = int(math.floor(math.log(MAX_VISIBLE_LEAVES, branching_factor)))
    return max(1, min(requested_depth, maximum))


def _child_depths(branching_factor, remaining_depth, level, balanced):
    if balanced:
        return [remaining_depth - 1] * branching_factor
    depths = []
    for child_index in range(branching_factor):
        penalty = 0 if child_index == 0 else 1 + ((child_index + level) % 2)
        depths.append(max(0, remaining_depth - 1 - penalty))
    return depths


def _build_tree(branching_factor, depth, balanced):
    counter = [0]

    def build(level, remaining_depth, path):
        node = {
            "id": counter[0],
            "level": level,
            "path": path,
            "children": [],
            "x": 0.0,
        }
        counter[0] += 1
        if remaining_depth > 0:
            child_depths = _child_depths(
                branching_factor, remaining_depth, level, balanced
            )
            node["children"] = [
                build(level + 1, child_depth, path + (child_index + 1,))
                for child_index, child_depth in enumerate(child_depths)
            ]
        return node

    return build(0, depth, ())


def _layout_tree(root):
    nodes = list(_walk(root))
    maximum_level = max(node["level"] for node in nodes)
    branching_factor = max(1, len(root["children"]))
    leaf_slots = branching_factor**maximum_level

    for node in nodes:
        level = node["level"]
        if level == 0:
            node_index = 0
        else:
            node_index = 0
            for branch_index in node["path"]:
                node_index = node_index * branching_factor + branch_index - 1
        span = branching_factor ** (maximum_level - level)
        node["x"] = node_index * span + span / 2

    return max(1, leaf_slots)


def _walk(root):
    yield root
    for child in root["children"]:
        yield from _walk(child)


@lru_cache(maxsize=128)
def _base_levels(branching_factor, depth, balanced):
    if balanced:
        return frozenset({depth})
    root = _build_tree(branching_factor, depth, False)
    return frozenset(
        node["level"] for node in _walk(root) if not node["children"]
    )


def _node_label(node):
    return f"f(n{_subscript(node['level'])})"


def _node_label_markup(node):
    return rf"\(f(n_{{{int(node['level'])}}})\)"


def _expanded_term_values(coefficients, values):
    expanded = []
    for coefficient, value in zip(coefficients or (), values or ()):
        expanded.extend([float(value)] * int(coefficient))
    return expanded


def _initial_size(
    relation_type,
    branching_factor,
    reduction_parameter,
    depth,
    term_b=None,
):
    if relation_type == "reduction":
        reductions = [int(value) for value in (term_b or (reduction_parameter,))]
        return max(reductions) * depth + 1
    factors = [float(value) for value in (term_b or ()) if float(value) > 0]
    return (1 / min(factors)) ** depth if factors else 2**depth


def _node_argument(
    node,
    relation_type,
    branching_factor,
    reduction_parameter,
    depth,
    term_a=None,
    term_b=None,
):
    initial = _initial_size(
        relation_type, branching_factor, reduction_parameter, depth, term_b
    )
    level = node["level"]
    expanded_values = _expanded_term_values(term_a, term_b)
    if relation_type == "reduction":
        reduction = sum(
            expanded_values[branch - 1] if branch <= len(expanded_values) else reduction_parameter
            for branch in node["path"]
        )
        value = max(1.0, initial - reduction)
        latex = "n_0" if not node["path"] else rf"n_0-{reduction:g}"
    else:
        multiplier = 1.0
        for branch in node["path"]:
            multiplier *= (
                expanded_values[branch - 1]
                if branch <= len(expanded_values)
                else 1.0 / reduction_parameter
            )
        value = initial * multiplier
        latex = "n_0" if not node["path"] else rf"{multiplier:.4g}\,n_0"
    return value, latex


def _recurrence_text(
    relation_type,
    branching_factor,
    reduction_parameter,
    term_a=None,
    term_b=None,
    function_type=None,
):
    external_suffix = "" if function_type == "zero" else " + f(n)"
    terms = ", ".join(
        (
            f"{coefficient}C(n−{value:g})"
            if relation_type == "reduction"
            else f"{coefficient}C({value:g}n)"
        )
        for coefficient, value in zip(term_a or (), term_b or ())
    )
    return f"C(n) = [{terms}]{external_suffix}"


def _render_svg(
    relation_type,
    branching_factor,
    reduction_parameter,
    requested_depth,
    balanced,
    function_type,
    polynomial_degree,
    active_level,
    marker_id="recursion-arrow",
    term_a=None,
    term_b=None,
    node_label_latex=None,
    node_label_class="",
    symbolic_level_labels=None,
    dashed_from_level=None,
    text_only_level=None,
    node_cost_latex=None,
):
    visible_depth = _visible_depth(branching_factor, requested_depth)
    root = _build_tree(branching_factor, visible_depth, balanced)
    leaf_count = _layout_tree(root)
    all_nodes = list(_walk(root))
    maximum_level = max(node["level"] for node in all_nodes)
    shown_level = min(active_level, maximum_level)
    nodes = [node for node in all_nodes if node["level"] <= shown_level]
    truncated = visible_depth < requested_depth

    width = max(760, leaf_count * MINIMUM_LEAF_SPACING + 180)
    top = 84
    level_gap = 104
    bottom = 82 if truncated else 42
    height = top + maximum_level * level_gap + bottom
    horizontal_padding = 48
    usable_width = width - 2 * horizontal_padding

    def coordinates(node):
        x = horizontal_padding + (node["x"] / leaf_count) * usable_width
        y = top + node["level"] * level_gap
        return x, y

    edges = []
    for node in nodes:
        parent_x, parent_y = coordinates(node)
        for child in node["children"]:
            if child["level"] > shown_level:
                continue
            child_x, child_y = coordinates(child)
            horizontal_direction = (
                -1 if child_x < parent_x else 1 if child_x > parent_x else 0
            )
            if horizontal_direction:
                start_x = parent_x + horizontal_direction * NODE_RADIUS
                start_y = parent_y
            else:
                start_x = parent_x
                start_y = parent_y + NODE_RADIUS
            end_x = child_x
            end_y = child_y - NODE_RADIUS - 2
            approach_y = end_y - 18
            control_1_x = start_x + (child_x - parent_x) * 0.35
            control_1_y = start_y
            control_2_x = end_x
            control_2_y = approach_y - (child_y - parent_y) * 0.22
            edges.append(
                f'<path d="M {start_x:.2f} {start_y:.2f} '
                f'C {control_1_x:.2f} {control_1_y:.2f}, '
                f'{control_2_x:.2f} {control_2_y:.2f}, '
                f'{end_x:.2f} {approach_y:.2f} '
                f'L {end_x:.2f} {end_y:.2f}" '
                f'class="tree-edge {"level-current" if child["level"] == shown_level else "level-past"} '
                f'{"symbolic-jump" if dashed_from_level is not None and child["level"] >= dashed_from_level else ""}" '
                f'data-parent-path="{".".join(map(str, node["path"]))}" '
                f'data-child-path="{".".join(map(str, child["path"]))}" '
                f'data-level="{child["level"]}" marker-end="url(#{marker_id})"/>'
            )

    continuation = []
    if truncated and shown_level == maximum_level:
        for node in nodes:
            if node["children"] or node["level"] != maximum_level:
                continue
            x, y = coordinates(node)
            continuation.append(
                f'<path d="M {x:.2f} {y + 30:.2f} L {x:.2f} {y + 58:.2f}" '
                f'class="tree-continuation"/>'
                f'<text x="{x:.2f}" y="{y + 78:.2f}" class="continuation-label">⋮</text>'
            )

    node_markup = []
    for node in nodes:
        x, y = coordinates(node)
        node_latex = (
            node_label_latex(node)
            if node_label_latex is not None
            else f'f(n_{{{int(node["level"])}}})'
        )
        label = rf"\({node_latex}\)"
        accessible_label = html.escape(node_latex)
        path = ".".join(map(str, node["path"]))
        argument_value, argument_latex = _node_argument(
            node,
            relation_type,
            branching_factor,
            reduction_parameter,
            requested_depth,
            term_a,
            term_b,
        )
        cost_latex = (
            node_cost_latex(node)
            if node_cost_latex is not None
            else _complexity_value_latex(
                function_type, argument_value, polynomial_degree
            )
        )
        level_class = "level-current" if node["level"] == shown_level else "level-past"
        base_class = "case-base" if not truncated and not node["children"] else ""
        if RUNNING_IN_COLAB:
            equation_markup = (
                f'<g class="tree-node-math {node_label_class}" '
                f'data-node-tex="{html.escape(node_latex, quote=True)}" '
                f'data-x="{x:.2f}" data-y="{y:.2f}"></g>'
            )
        else:
            equation_markup = (
                f'<foreignObject x="{x - NODE_RADIUS:.2f}" '
                f'y="{y - NODE_RADIUS:.2f}" '
                f'width="{2 * NODE_RADIUS}" height="{2 * NODE_RADIUS}">'
                f'<div xmlns="http://www.w3.org/1999/xhtml" '
                f'class="tree-node-equation {node_label_class}">{label}</div>'
                f'</foreignObject>'
            )
        tooltip_width = 220
        tooltip_height = 48
        tooltip_markup = (
            f'<foreignObject class="tree-node-cost-tooltip" '
            f'x="{x - tooltip_width / 2:.2f}" y="{y - NODE_RADIUS - 56:.2f}" '
            f'width="{tooltip_width}" height="{tooltip_height}">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" '
            f'class="tree-node-cost-tooltip-content" '
            f'style="background:#123a63;color:#fff;border:2px solid #fff;">'
            f'\\({cost_latex}\\)</div></foreignObject>'
        )
        node_markup.append(
            f'<g class="tree-node {level_class} {base_class}" role="button" tabindex="0" '
            f'aria-label="{accessible_label}" data-tree-node="1" '
            f'data-path="{path}" data-level="{node["level"]}" '
            f'data-argument-latex="{html.escape(argument_latex, quote=True)}" '
            f'data-cost-latex="{html.escape(cost_latex, quote=True)}">'
            + (
                ""
                if text_only_level is not None and node["level"] == text_only_level
                else f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{NODE_RADIUS}"/>'
            )
            + f'{equation_markup}'
            + tooltip_markup
            + f'</g>'
        )

    level_labels = []
    for level in range(shown_level + 1):
        y = top + level * level_gap
        level_label = (
            symbolic_level_labels.get(level, str(level))
            if symbolic_level_labels
            else str(level)
        )
        level_labels.append(
            f'<text x="{width - 8}" y="{y + 5}" class="level-label">'
            f'nivel {level_label}</text>'
        )

    structure = "balanceado" if balanced else "desbalanceado"
    recurrence = _recurrence_text(
        relation_type,
        branching_factor,
        reduction_parameter,
        term_a,
        term_b,
        function_type,
    )
    detail = (
        f"árbol {structure} · "
        f"{len(nodes)} nodos visibles · nivel activo {active_level}"
    )
    if truncated:
        detail += f" de {requested_depth}"
    summary = f"{recurrence} · {detail}"

    return f"""
    <div class="recursion-tree-plot-wrap">
      <div class="recursion-tree-figure">
      <svg viewBox="0 0 {width} {height}" role="img"
           data-base-width="{width}" data-base-height="{height}" style="width:100%"
           aria-label="{html.escape(summary)}">
        <defs>
          <marker id="{marker_id}" viewBox="0 0 10 10" refX="8" refY="5"
                  markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" class="arrow-head"/>
          </marker>
        </defs>
        {''.join(edges)}
        {''.join(continuation)}
        {''.join(node_markup)}
        {''.join(level_labels)}
      </svg>
      </div>
    </div>
    """


def _latex_integer(value):
    return f"{int(value):,}".replace(",", r"\,")


def _latex_from_log10(logarithm):
    if logarithm == -math.inf:
        return "0"
    if logarithm < 6:
        value = 10**logarithm
        if math.isclose(value, round(value), rel_tol=1e-10, abs_tol=1e-10):
            return _latex_integer(round(value))
        return f"{value:.4g}"
    exponent = int(math.floor(logarithm))
    coefficient = 10 ** (logarithm - exponent)
    return rf"{coefficient:.4g}\times 10^{{{exponent}}}"


def _complexity_log10(function_type, value, polynomial_degree):
    value = max(1.0, float(value))
    logarithm_n = math.log10(value)
    if function_type == "zero":
        return -math.inf
    if function_type == "constant":
        return 0.0
    if function_type == "logarithmic":
        result = math.log2(value)
        return -math.inf if result == 0 else math.log10(result)
    if function_type == "linear":
        return logarithm_n
    if function_type == "log_linear":
        logarithmic_factor = math.log2(value)
        if logarithmic_factor == 0:
            return -math.inf
        return logarithm_n + math.log10(logarithmic_factor)
    if function_type == "quadratic":
        return 2 * logarithm_n
    if function_type == "cubic":
        return 3 * logarithm_n
    if function_type == "polynomial":
        return polynomial_degree * logarithm_n
    if function_type == "polylogarithmic":
        degree, log_power, log_base = polynomial_degree
        logarithmic_factor = math.log(value, log_base)
        if logarithmic_factor == 0 and log_power > 0:
            return -math.inf
        if logarithmic_factor == 0:
            return degree * logarithm_n
        return degree * logarithm_n + log_power * math.log10(logarithmic_factor)
    if function_type == "exponential":
        return value * math.log10(2)
    return math.lgamma(round(value) + 1) / math.log(10)


def _complexity_value_latex(function_type, value, polynomial_degree):
    return _latex_from_log10(
        _complexity_log10(function_type, value, polynomial_degree)
    )


def _equation_markup(
    relation_type,
    branching_factor,
    reduction_parameter,
    function_type,
    polynomial_degree,
    term_a=None,
    term_b=None,
):
    external_suffix = r"+f(n)"
    if relation_type == "reduction":
        recursive_expression = (
            rf"\left[\displaystyle\sum_{{i=1}}^{{m}}"
            rf"a_iC\left(n-b_i\right)\right]{external_suffix}"
        )
        largest_reduction = max(term_b or (reduction_parameter,))
        recursive_condition = rf"n>{largest_reduction:g}"
        base_condition = rf"1\leq n\leq {largest_reduction:g}"
    else:
        recursive_expression = (
            rf"\left[\displaystyle\sum_{{i=1}}^{{m}}"
            rf"a_iC\left(b_i\cdot n\right)\right]{external_suffix}"
        )
        recursive_condition = "n>1"
        base_condition = "n=1"
    recurrence = (
        r"C(n)=\begin{cases}"
        rf"{recursive_expression} & \text{{si }} {recursive_condition}\\[10pt]"
        rf"c & \text{{si }} {base_condition}"
        r"\end{cases}"
    )
    return (
        '<details class="recursion-info-section" open>'
        '<summary>Expresión general</summary>'
        f'<div class="recursion-equation">\\(\\displaystyle {recurrence}\\)</div>'
        "</details>"
    )


def _expanded_equation_markup(
    relation_type,
    term_a,
    term_b,
    function_type,
    polynomial_degree,
    base_value=1,
):
    terms = []
    for coefficient, value in zip(term_a, term_b):
        coefficient_latex = "" if coefficient == 1 else str(coefficient)
        if relation_type == "reduction":
            recursive_call = rf"C\left(n-{value:g}\right)"
        else:
            fraction = Fraction(float(value)).limit_denominator(1000)
            has_exact_fraction = math.isclose(
                float(fraction), float(value), rel_tol=0, abs_tol=1e-12
            )
            if not has_exact_fraction:
                argument = rf"{value:g}\cdot n"
            elif fraction.denominator == 1:
                argument = rf"{fraction.numerator}\cdot n"
            elif fraction.numerator == 1:
                argument = rf"\dfrac{{n}}{{{fraction.denominator}}}"
            else:
                argument = (
                    rf"\dfrac{{{fraction.numerator}}}{{{fraction.denominator}}}"
                    rf"\cdot n"
                )
            recursive_call = rf"C\left({argument}\right)"
        terms.append(f"{coefficient_latex}{recursive_call}")

    expression = "+".join(terms)
    if function_type != "zero":
        external_cost = FUNCTION_LATEX[function_type]
        if function_type == "polynomial":
            external_cost = rf"n^{{{polynomial_degree}}}"
        elif function_type == "polylogarithmic":
            degree, log_power, log_base = polynomial_degree
            external_cost = (
                rf"n^{{{degree}}}\cdot"
                rf"\log_{{{log_base}}}^{{{log_power}}}(n)"
            )
        expression += rf"+{external_cost}"

    if relation_type == "reduction":
        largest_reduction = max(term_b)
        recursive_condition = rf"n>{largest_reduction:g}"
        base_condition = rf"1\leq n\leq {largest_reduction:g}"
    else:
        recursive_condition = "n>1"
        base_condition = "n=1"
    recurrence = (
        r"C(n)=\begin{cases}"
        rf"{expression} & \text{{si }} {recursive_condition}\\[10pt]"
        rf"{base_value:g} & \text{{si }} {base_condition}"
        r"\end{cases}"
    )

    return (
        '<details class="recursion-info-section" open>'
        '<summary>Expresión resultante</summary>'
        f'<div class="recursion-equation">\\(\\displaystyle {recurrence}\\)</div>'
        "</details>"
    )


def _level_table_markup(
    relation_type,
    branching_factor,
    reduction_parameter,
    depth,
    balanced,
    function_type,
    polynomial_degree,
    active_level,
    term_a=None,
    term_b=None,
):
    initial_size = _initial_size(
        relation_type, branching_factor, reduction_parameter, depth, term_b
    )
    visible_depth = _visible_depth(branching_factor, depth)
    base_levels = set()
    if visible_depth == depth:
        base_levels = _base_levels(branching_factor, depth, balanced)

    rows = []
    for level in range(depth + 1):
        if level > active_level:
            rows.append(
                '<tr class="level-pending" aria-label="Nivel pendiente">'
                "<td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td>"
                "</tr>"
            )
            continue
        node_count = branching_factor**level
        count_expression = (
            rf"{branching_factor}^{{{level}}}={_latex_integer(node_count)}"
            if balanced
            else rf"\leq {_latex_integer(node_count)}"
        )
        if relation_type == "reduction":
            reductions = [float(value) for value in (term_b or (reduction_parameter,))]
            minimum = max(1, initial_size - level * max(reductions))
            maximum = max(1, initial_size - level * min(reductions))
            argument = (
                rf"\left[n_0-{level}\cdot {max(reductions):g},"
                rf"n_0-{level}\cdot {min(reductions):g}\right]"
            )
        else:
            factors = [float(value) for value in (term_b or (1.0,))]
            minimum_factor = min(factors)
            maximum_factor = max(factors)
            minimum = initial_size * (minimum_factor**level)
            maximum = initial_size * (maximum_factor**level)
            argument = (
                rf"\left[{minimum_factor:g}^{{{level}}}n_0,"
                rf"{maximum_factor:g}^{{{level}}}n_0\right]"
            )
        minimum_value = _complexity_value_latex(
            function_type, minimum, polynomial_degree
        )
        maximum_value = _complexity_value_latex(
            function_type, maximum, polynomial_degree
        )
        if math.isclose(minimum, maximum):
            argument = argument if level else "n_0"
            function_value = minimum_value
        else:
            function_value = rf"\left[{minimum_value},{maximum_value}\right]"
        rows.append(
            f'<tr data-level="{level}" class="'
            f'{"level-current" if level == active_level else "level-past"} '
            f'{"case-base" if level in base_levels else ""}">'
            f"<td>\\(\\displaystyle {level}\\)</td>"
            f"<td>\\(\\displaystyle {count_expression}\\)</td>"
            f"<td>\\(\\displaystyle {argument}\\)</td>"
            f"<td>\\(\\displaystyle {function_value}\\)</td>"
            "</tr>"
        )

    return (
        '<details class="recursion-info-section" open>'
        '<summary>Costo por nivel</summary>'
        '<div class="recursion-level-table">'
        "<table><thead><tr>"
        "<th>Nivel</th><th>Nodos</th><th>Argumento</th><th>\\(f(n_i)\\)</th>"
        "</tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div></details>"
    )


def run_app(builder_only=False):
    if RUNNING_IN_COLAB:
        _colab_output.enable_custom_widget_manager()

    previous_cleanup = getattr(builtins, "_recursion_tree_app_cleanup", None)
    if callable(previous_cleanup):
        previous_cleanup()

    relation_type = widgets.Dropdown(
        options=[
            ("Relación de reducción", "reduction"),
            ("Relación de división", "division"),
        ],
        value="division",
        layout=widgets.Layout(width="188px"),
    )
    function_options = [
        ("zero", r"0"),
        ("constant", r"1"),
        ("logarithmic", r"\log_2(n)"),
        ("linear", r"n"),
        ("log_linear", r"n\cdot\log_2(n)"),
        ("quadratic", r"n^2"),
        ("cubic", r"n^3"),
        ("polynomial", r"n^k"),
        ("polylogarithmic", r"n^k\cdot\log_\ell^p(n)"),
        ("exponential", r"2^n"),
        ("factorial", r"n!"),
    ]
    function_type = widgets.Dropdown(
        options=[(latex, value) for value, latex in function_options],
        value="linear",
        layout=widgets.Layout(display="none"),
    )
    function_previous = widgets.Button(
        description="◀", tooltip="Función anterior",
        layout=widgets.Layout(width="34px", height="32px"),
    )
    function_readout = widgets.HTMLMath(
        layout=widgets.Layout(
            width="120px", height="32px",
            border="1px solid var(--jp-border-color2, #bdbdbd)",
            display="flex", align_items="center", justify_content="center",
        ),
    )
    function_readout.add_class("recursion-function-readout")
    function_following = widgets.Button(
        description="▶", tooltip="Función siguiente",
        layout=widgets.Layout(width="34px", height="32px"),
    )
    function_selector = widgets.HBox(
        [function_previous, function_readout, function_following],
        layout=widgets.Layout(width="188px", align_items="center", gap="0px"),
    )
    function_selector.add_class("recursion-function-selector")
    function_selector.add_class("recursion-stepper")

    def select_function(delta):
        def handler(_):
            values = [value for value, _ in function_options]
            if builder_only and method.value == "master":
                values = [
                    value
                    for value in values
                    if value not in {"zero", "exponential", "factorial"}
                ]
            current = values.index(function_type.value)
            function_type.value = values[(current + delta) % len(values)]

        return handler

    def update_function_readout(*_):
        latex_by_value = dict(function_options)
        function_readout.value = rf"\({latex_by_value[function_type.value]}\)"

    function_previous.on_click(select_function(-1))
    function_following.on_click(select_function(1))
    function_type.observe(update_function_readout, names="value")
    update_function_readout()
    parameter_state = {
        "h": 3,
        "k": 4,
        "p": 1,
        "ell": 2,
        "m": 1,
        "term_a": [2],
        "term_b": [0.5],
    }
    animation_state = {"level": 0}
    parameter_readouts = {}

    def parameter_stepper(name, minimum, maximum):
        previous = widgets.Button(
            description="◀", tooltip="Valor anterior",
            layout=widgets.Layout(width="34px", height="32px"),
        )
        readout = widgets.HTMLMath(
            value=rf"\({parameter_state[name]}\)",
            layout=widgets.Layout(
                width="120px", height="32px",
                border="1px solid var(--jp-border-color2, #bdbdbd)",
                display="flex", align_items="center", justify_content="center",
            ),
        )
        readout.add_class("recursion-parameter-readout")
        following = widgets.Button(
            description="▶", tooltip="Valor siguiente",
            layout=widgets.Layout(width="34px", height="32px"),
        )
        parameter_readouts[name] = readout

        def change(delta):
            def handler(_):
                lower = 1 if name == "b" and relation_type.value == "reduction" else minimum
                value = min(maximum, max(lower, parameter_state[name] + delta))
                if value != parameter_state[name]:
                    parameter_state[name] = value
                    readout.value = rf"\({value}\)"
                    if name == "m":
                        sync_term_input_lengths(value)
                    reset_progress()
            return handler

        previous.on_click(change(-1))
        following.on_click(change(1))
        stepper = widgets.HBox(
            [previous, readout, following],
            layout=widgets.Layout(width="188px", align_items="center", gap="0px"),
        )
        stepper.add_class("recursion-stepper")
        return stepper

    depth = parameter_stepper("h", 1, 7)
    polynomial_degree = parameter_stepper("k", 1, 8)
    logarithmic_power = parameter_stepper("p", 0, 8)
    logarithmic_base = parameter_stepper("ell", 2, 10)
    term_count = parameter_stepper("m", 1, 6)
    term_count.add_class("recursion-term-count-control")
    polynomial_degree.add_class("recursion-parameter-value-control")
    logarithmic_power.add_class("recursion-parameter-value-control")
    logarithmic_base.add_class("recursion-parameter-value-control")
    term_a_input = widgets.Text(
        value="2",
        placeholder="Ejemplo: 1, 1",
        layout=widgets.Layout(width="188px", height="32px"),
    )
    term_b_input = widgets.Text(
        value="0.5",
        placeholder="Ejemplo: 0.5, 0.25",
        layout=widgets.Layout(width="188px", height="32px"),
    )
    term_a_input.add_class("recursion-term-value-control")
    term_b_input.add_class("recursion-term-value-control")
    base_case_input = widgets.Text(
        value="1",
        placeholder="Ejemplo: 1",
        layout=widgets.Layout(width="188px", height="32px"),
    )
    term_validation = widgets.HTMLMath(layout=widgets.Layout(width="252px"))

    def sync_term_input_lengths(term_count_value):
        def resized(values, default):
            values = list(values[:term_count_value])
            values.extend([default] * (term_count_value - len(values)))
            return values

        current_a = parameter_state.get("term_a", [])
        current_b = parameter_state.get("term_b", [])
        next_a = resized(current_a, 1)
        default_b = 1 if relation_type.value == "reduction" else 0.5
        next_b = resized(current_b, default_b)
        term_a_input.value = ", ".join(str(value) for value in next_a)
        term_b_input.value = ", ".join(f"{value:g}" for value in next_b)

    def labeled(label, control, label_width=52, row_width=252):
        label_widget = widgets.HTMLMath(
            value=label,
            layout=widgets.Layout(
                width=f"{label_width}px",
                min_width=f"{label_width}px",
                max_width=f"{label_width}px",
                flex=f"0 0 {label_width}px",
            ),
        )
        label_widget.add_class("recursion-control-label")
        row = widgets.HBox(
            [
                label_widget,
                control,
            ],
            layout=widgets.Layout(
                width=f"{row_width}px",
                min_width=f"{row_width}px",
                max_width=f"{row_width}px",
                align_items="center",
                gap="8px",
            ),
        )
        row.add_class("recursion-labeled-control")
        return row

    type_control = labeled(
        "<b>Tipo</b>", relation_type, label_width=96, row_width=296
    )
    function_control = labeled(
        r"\(\boldsymbol{f(n)}\)", function_selector,
        label_width=96, row_width=296,
    )
    degree_control = labeled(
        r"\(\boldsymbol{k}\)", polynomial_degree, row_width=256
    )
    logarithmic_power_control = labeled(
        r"\(\boldsymbol{p}\)", logarithmic_power, row_width=256
    )
    logarithmic_base_control = labeled(
        r"\(\boldsymbol{\ell}\)", logarithmic_base, row_width=256
    )
    term_count_control = labeled(
        r"\(\boldsymbol{m}\)", term_count, row_width=256
    )
    term_a_control = labeled(
        r"\(\boldsymbol{a_i}\)", term_a_input, row_width=256
    )
    term_b_control = labeled(
        r"\(\boldsymbol{b_i}\)", term_b_input, row_width=256
    )
    base_case_control = labeled(
        "<b>Caso base</b>", base_case_input, label_width=96, row_width=296
    )
    division_methods = [
        ("Sustitución iterativa", "iterative"),
        ("Árbol de recurrencia", "tree"),
        ("Teorema maestro", "master"),
    ]
    reduction_methods = [
        ("Sustitución iterativa", "iterative"),
        ("Árbol de recurrencia", "tree"),
        ("Ecuación característica", "characteristic"),
    ]
    method = widgets.Dropdown(
        options=division_methods,
        value="iterative",
        layout=widgets.Layout(width="188px"),
    )
    master_flavor = widgets.Dropdown(
        options=[],
        value=None,
        layout=widgets.Layout(width="188px"),
    )
    method_control = labeled(
        "<b>Método</b>", method, label_width=96, row_width=296
    )
    master_flavor_control = labeled(
        "<b>Versión</b>", master_flavor, label_width=96, row_width=296
    )
    master_flavor_control.layout.display = "none"
    master_variant_note = widgets.HTML(
        layout=widgets.Layout(
            width="188px", margin="0 0 0 108px", display="none"
        )
    )
    master_variant_note.add_class("recursion-master-variant-note")

    def control_section(title, children):
        section = widgets.VBox(
            [widgets.HTML(f'<div class="recursion-control-title">{title}</div>'), *children],
            layout=widgets.Layout(width="auto"),
        )
        section.add_class("recursion-control-section")
        return section

    parameter_controls = widgets.VBox(
        [
            term_count_control,
            term_a_control,
            term_b_control,
            degree_control,
            logarithmic_power_control,
            logarithmic_base_control,
            term_validation,
        ],
        layout=widgets.Layout(width="256px", gap="12px"),
    )
    parameter_controls.add_class("recursion-parameter-controls")
    parameters_section = control_section("Parámetros", [parameter_controls])

    additional_controls = [labeled(r"\(\boldsymbol{h}\)", depth)]
    if builder_only:
        additional_controls = [
            labeled(r"\(\boldsymbol{h}\)", depth),
            method_control,
            master_flavor_control,
            master_variant_note,
        ]

    controls = widgets.Box(
        [
            control_section(
                "Relación de recurrencia:",
                [
                    type_control,
                    function_control,
                    base_case_control,
                ],
            ),
            parameters_section,
            control_section(
                "Profundidad del árbol:",
                additional_controls,
            ),
        ],
        layout=widgets.Layout(
            width="auto", display="flex", flex_flow="row wrap",
            align_items="flex-start", justify_content="flex-start",
            gap="12px 36px",
        ),
    )
    controls.add_class("recursion-tree-controls")
    if builder_only:
        controls.children[2].children[0].value = (
            '<div class="recursion-control-title">Parámetros adicionales</div>'
        )
        controls.children[2].children[1].layout.display = "none"

    def update_master_flavor_visibility(change=None):
        is_master = method.value == "master"
        entering_master = (
            is_master
            and change is not None
            and change.get("old") != "master"
        )
        if entering_master:
            function_type.value = "constant"
        master_flavor_control.layout.display = "flex" if is_master else "none"
        master_variant_note.layout.display = "block" if is_master else "none"
        if is_master:
            update_master_variant_options()
        update_term_count_availability()

    def prevent_unsupported_function_for_master(change):
        if (
            builder_only
            and method.value == "master"
            and change.get("new") in {"zero", "exponential", "factorial"}
        ):
            function_type.value = "constant"

    def update_term_count_availability(change=None):
        if not builder_only:
            return
        allows_multiple_terms = (
            method.value == "characteristic"
            or (
                method.value == "master"
                and master_flavor.value == "generalized"
            )
        )
        if allows_multiple_terms:
            term_count.remove_class("recursion-control-disabled")
        else:
            term_count.add_class("recursion-control-disabled")
        for index, control in enumerate(term_count.children):
            if isinstance(control, widgets.Button):
                control.disabled = not allows_multiple_terms
                control.tooltip = (
                    ("Valor anterior" if index == 0 else "Valor siguiente")
                    if allows_multiple_terms
                    else "Este método utiliza un único término recursivo."
                )
        if not allows_multiple_terms and parameter_state["m"] != 1:
            parameter_state["m"] = 1
            parameter_readouts["m"].value = r"\(1\)"
            sync_term_input_lengths(1)

    def update_method_options():
        if not builder_only:
            return
        current_method = method.value
        method.options = (
            reduction_methods
            if relation_type.value == "reduction"
            else division_methods
        )
        available_methods = {value for _, value in method.options}
        method.value = (
            current_method if current_method in available_methods else "iterative"
        )
        update_master_flavor_visibility()

    method.observe(update_master_flavor_visibility, names="value")
    master_flavor.observe(update_term_count_availability, names="value")
    function_type.observe(
        prevent_unsupported_function_for_master, names="value"
    )
    update_method_options()
    update_master_flavor_visibility()
    builder_resolve = widgets.Button(
        description="Aplicar método", icon="calculator",
        layout=widgets.Layout(width="auto", flex="0 0 auto"),
    )
    builder_reset = widgets.Button(
        description="Restablecer", icon="refresh",
        layout=widgets.Layout(width="auto", flex="0 0 auto"),
    )
    builder_actions = widgets.HBox(
        [builder_resolve, builder_reset],
        layout=widgets.Layout(
            width="100%", flex_flow="row wrap", align_items="center",
            justify_content="flex-end", gap="0px",
        ),
    )
    builder_actions.add_class("recursion-playback")
    configuration_header = widgets.HTML(
        '<button type="button" class="recursion-tree-panel-summary" '
        'aria-expanded="true">Configuración</button>',
        layout=widgets.Layout(width="100%"),
    )
    configuration_content = widgets.VBox(
        [controls], layout=widgets.Layout(width="100%", gap="0")
    )
    configuration_content.add_class("recursion-builder-panel-content")
    configuration_content.add_class("recursion-tree-panel-content")
    configuration_panel = widgets.VBox(
        [configuration_header, configuration_content],
        layout=widgets.Layout(width="100%", gap="0"),
    )
    configuration_panel.add_class("recursion-builder-panel")
    configuration_panel.add_class("recursion-tree-widget-panel")

    action_layout = widgets.Layout(width="auto", flex="0 0 auto")
    previous_level = widgets.Button(
        description="Anterior", icon="step-backward", layout=action_layout
    )
    next_level = widgets.Button(
        description="Siguiente", icon="step-forward", layout=action_layout
    )
    play = widgets.Button(description="Reproducir", icon="play", layout=action_layout)
    pause = widgets.Button(description="Pausar", icon="pause", layout=action_layout)
    reset = widgets.Button(
        description="Restablecer", icon="refresh", layout=action_layout
    )
    previous_level.add_class("recursion-previous-button")
    next_level.add_class("recursion-next-button")
    play.add_class("recursion-play-button")
    pause.add_class("recursion-pause-button")
    reset.add_class("recursion-reset-button")
    playback = widgets.HBox(
        [previous_level, next_level, play, pause, reset],
        layout=widgets.Layout(
            width="100%", flex_flow="row wrap", align_items="center",
            justify_content="flex-end", gap="0px",
        ),
    )
    playback.add_class("recursion-playback")
    configuration_content.children = (
        (controls, builder_actions)
        if builder_only
        else (controls, playback)
    )

    equation = widgets.HTMLMath(layout=widgets.Layout(width="100%"))
    expanded_equation = widgets.HTMLMath(layout=widgets.Layout(width="100%"))
    method_solution = widgets.HTMLMath(layout=widgets.Layout(width="100%"))
    method_solution.add_class("recursion-panel-output")
    method_solution.layout.display = "none"
    level_table = widgets.HTMLMath(layout=widgets.Layout(width="100%"))
    figure = widgets.HTMLMath(layout=widgets.Layout(width="100%"))
    figure.add_class("recursion-figure-output")
    zoom_toolbar = widgets.HTML(
        value=(
            '<div class="recursion-zoom-controls" aria-label="Controles de zoom">'
            '<button type="button" class="recursion-zoom-btn" data-tree-zoom="out" '
            'title="Alejar la vista" aria-label="Alejar la vista">−</button>'
            '<button type="button" class="recursion-zoom-btn" data-tree-zoom="in" '
            'title="Acercar la vista" aria-label="Acercar la vista">+</button>'
            '<button type="button" class="recursion-zoom-btn" data-tree-zoom="reset" '
            'title="Restablecer el zoom" aria-label="Restablecer el zoom">↺</button>'
            "</div>"
        ),
        layout=widgets.Layout(width="auto"),
    )
    zoom_toolbar.add_class("recursion-zoom-toolbar")
    plot_container = widgets.VBox(
        [zoom_toolbar, figure],
        layout=widgets.Layout(width="100%"),
    )
    plot_container.add_class("recursion-plot-container")
    note = widgets.HTML(layout=widgets.Layout(width="100%"))
    for panel_output in (equation, expanded_equation, level_table):
        panel_output.add_class("recursion-panel-output")
    level_table.add_class("recursion-level-table-output")
    tree_panel_header = widgets.HTML(
        value=(
            '<button type="button" class="recursion-tree-panel-summary" '
            'aria-expanded="true">'
            "Árbol de recursión:</button>"
        ),
        layout=widgets.Layout(width="100%"),
    )
    tree_panel_content = widgets.VBox(
        [plot_container, note] if not builder_only else [],
        layout=widgets.Layout(width="100%", gap="0px"),
    )
    tree_panel_content.add_class("recursion-tree-panel-content")
    tree_panel = widgets.VBox(
        [tree_panel_header, tree_panel_content],
        layout=widgets.Layout(width="100%", gap="0px"),
    )
    tree_panel.add_class("recursion-panel-output")
    tree_panel.add_class("recursion-tree-widget-panel")
    panel_children = (
        [equation, configuration_panel, expanded_equation, method_solution]
        if builder_only
        else [equation, configuration_panel, expanded_equation, tree_panel, level_table]
    )
    panels = widgets.VBox(
        panel_children,
        layout=widgets.Layout(width="100%", gap="0px"),
    )
    panels.add_class("recursion-info-sections")
    styles = widgets.HTML(
        """
        <style>
          @import url('https://fonts.googleapis.com/css2?family=STIX+Two+Math&display=swap');
          .recursion-tree-root{box-sizing:border-box;width:100%;padding:14px 4px;
            background:#fff;color:#333;font-family:sans-serif}
          .recursion-tree-root>.widget-box,.recursion-tree-root .widget-html-content,
          .recursion-tree-root .widget-htmlmath-content{background:#fff;color:#333}
          .recursion-tree-controls{box-sizing:border-box!important;display:flex!important;width:auto!important;
            flex-flow:row wrap!important;
            column-gap:36px!important;row-gap:12px!important;
            justify-content:start!important;align-items:start!important;margin-bottom:12px;
            overflow:visible!important}
          .recursion-control-section{box-sizing:border-box!important;display:flex;gap:12px;
            width:auto!important;overflow:visible!important}
          .recursion-control-title{margin-bottom:0;font-family:sans-serif;font-size:13px;font-weight:700;color:#333;line-height:1.1}
          .recursion-control-section .widget-hbox{min-height:32px}
          .recursion-labeled-control{box-sizing:border-box!important;
            flex:none!important}
          .recursion-control-label{box-sizing:border-box!important;flex-shrink:0!important;
            color:#333!important;font-family:sans-serif!important;font-size:13px!important;
            font-weight:700!important;line-height:1.1!important}
          .recursion-control-label mjx-container{font-size:100%!important;font-weight:700!important}
          .recursion-parameter-controls{
            box-sizing:border-box!important;width:256px!important;max-width:256px!important;
            overflow:visible!important}
          .recursion-parameter-controls::-webkit-scrollbar,
          .recursion-parameter-controls *::-webkit-scrollbar{
            display:none!important;width:0!important;height:0!important}
          .recursion-control-section button{border:1px solid #ccc;border-radius:0;
            box-sizing:border-box!important;margin:0!important;padding:0!important;
            background:#f7f7f7;color:#333;font-size:14px!important}
          .recursion-control-section button .fa,
          .recursion-control-section button i{
            width:14px!important;margin:0!important;font-size:14px!important;
            line-height:1!important;text-align:center!important}
          .recursion-control-section button:hover{background:#eee}
          .recursion-parameter-readout{
            box-sizing:border-box!important;width:120px!important;height:32px!important;
            min-height:32px!important;max-height:32px!important;display:flex!important;
            align-items:center!important;justify-content:center!important;padding:0!important}
          .recursion-term-count-control{
            box-sizing:border-box!important;width:188px!important;
            min-width:188px!important;max-width:188px!important;margin-left:0!important}
          .recursion-parameter-value-control{
            box-sizing:border-box!important;width:188px!important;
            min-width:188px!important;max-width:188px!important;margin-left:0!important}
          .recursion-term-count-control .recursion-parameter-readout,
          .recursion-parameter-value-control .recursion-parameter-readout{
            width:120px!important;min-width:120px!important;max-width:120px!important}
          .recursion-tree-root .recursion-term-value-control{
            box-sizing:border-box!important;width:188px!important;
            min-width:188px!important;max-width:188px!important;margin-left:0!important}
          .recursion-control-disabled{opacity:.5!important}
          .recursion-control-disabled .widget-button,
          .recursion-control-disabled .recursion-parameter-readout{
            cursor:not-allowed!important}
          .recursion-function-readout{
            box-sizing:border-box!important;width:120px!important;height:32px!important;
            min-height:32px!important;max-height:32px!important;display:flex!important;
            align-items:center!important;justify-content:center!important;padding:0!important;
            background:#fff!important;color:#333!important;border:1px solid #ccc!important;
            border-radius:0!important}
          .recursion-parameter-readout .widget-htmlmath-content,
          .recursion-parameter-readout .widget-html-content,
          .recursion-function-readout .widget-htmlmath-content,
          .recursion-function-readout .widget-html-content{
            box-sizing:border-box;width:100%!important;height:30px!important;
            display:flex!important;align-items:center!important;justify-content:center!important;
            padding:0!important;text-align:center!important}
          .recursion-tree-root select,
          .recursion-tree-root .widget-dropdown select{
            box-sizing:border-box;width:100%!important;height:32px;padding:2px 24px 2px 6px;
            border:1px solid #ccc;border-radius:3px;background-color:#fff!important;
            color:#333!important;color-scheme:light;font-size:13px}
          .recursion-control-section .widget-dropdown{
            box-sizing:border-box!important;width:188px!important;
            min-width:188px!important;max-width:188px!important}
          .recursion-tree-root select option{
            background:#fff!important;color:#333!important}
          .recursion-function-selector{
            box-sizing:border-box!important;display:flex!important;
            width:188px!important;min-width:188px!important;max-width:188px!important;
            gap:0!important;overflow:visible!important}
          .recursion-function-selector .widget-button{
            box-sizing:border-box!important;flex:0 0 34px!important;
            width:34px!important;min-width:34px!important;max-width:34px!important}
          .recursion-function-selector .recursion-function-readout{
            box-sizing:border-box!important;flex:0 0 120px!important;
            width:120px!important;min-width:120px!important;max-width:120px!important}
          .recursion-stepper{
            box-sizing:border-box!important;display:flex!important;width:188px!important;
            min-width:188px!important;max-width:188px!important;flex:0 0 188px!important;
            gap:0!important;margin:0!important;padding:0!important;overflow:visible!important}
          .recursion-stepper>.widget-button{
            box-sizing:border-box!important;width:34px!important;min-width:34px!important;
            max-width:34px!important;flex:0 0 34px!important;margin:0!important;
            padding:0!important;border:1px solid #ccc!important;border-radius:0!important;
            font-size:13px!important;line-height:1!important}
          .recursion-stepper .recursion-parameter-readout{
            box-sizing:border-box!important;width:120px!important;min-width:120px!important;
            max-width:120px!important;flex:0 0 120px!important;margin:0!important;
            border:1px solid #ccc!important;border-radius:0!important}
          .recursion-tree-root .widget-text{
            box-sizing:border-box!important;width:188px!important;height:32px!important;
            min-width:0!important;overflow:visible!important}
          .recursion-tree-root .widget-text input{
            box-sizing:border-box!important;width:100%!important;height:32px!important;
            min-height:32px!important;padding:3px 8px!important;
            border:1px solid #ccc!important;border-radius:3px!important;
            background:#fff!important;color:#333!important;color-scheme:light!important;
            box-shadow:none!important;font-size:13px!important}
          .recursion-tree-root .widget-text input:focus{
            outline:none!important;border-color:#1976d2!important;
            box-shadow:0 0 0 1px #1976d2!important}
          .recursion-term-input-invalid input{
            border-color:#b85450!important;box-shadow:0 0 0 1px #b85450!important}
          .recursion-term-validation{box-sizing:border-box;width:100%;min-height:18px;
            overflow-wrap:anywhere;color:#b85450;font-size:12px;
            line-height:16px;padding-left:60px}
          .recursion-playback{box-sizing:border-box;width:100%;min-height:40px;padding:0;
            margin:16px 0 0;border:0;border-radius:0;background:#fff;gap:0!important;
            display:flex!important;flex-flow:row wrap!important;justify-content:flex-end!important;
            align-items:center!important;height:auto!important;overflow:visible!important}
          .recursion-playback button{box-sizing:border-box!important;flex:0 0 auto!important;
            width:auto!important;height:38px!important;min-height:38px!important;
            border:1px solid #bbb;border-radius:0!important;
            background:#f7f7f7!important;color:#333!important}
          .recursion-info-sections,.recursion-info-sections>.widget-box{
            box-sizing:border-box;width:100%!important;gap:0!important}
          .recursion-builder-panel{box-sizing:border-box!important;width:100%!important;
            max-width:none!important;margin:0!important;border:1px solid #dedede;
            border-bottom:0;border-radius:0;background:#fff;overflow:hidden}
          .recursion-builder-panel:first-child{border-radius:5px 5px 0 0}
          .recursion-builder-panel-header{box-sizing:border-box;width:100%;padding:10px 14px;
            border-bottom:1px solid #e2e2e2;background:#f7f7f7;color:#333;
            font-size:16px;line-height:1.45;font-weight:700;text-align:left}
          .recursion-builder-panel-content{box-sizing:border-box!important;width:100%!important;
            padding:12px;background:#fff}
          .recursion-builder-panel .recursion-equation{
            box-sizing:border-box!important;display:flex!important;width:100%!important;
            min-height:64px;align-items:center!important;justify-content:center!important;
            padding:16px 20px}
          .recursion-panel-output,.recursion-panel-output .widget-htmlmath-content,
          .recursion-panel-output .widget-html-content{
            box-sizing:border-box;width:100%!important;max-width:none!important;margin:0!important}
          .recursion-info-section{box-sizing:border-box;display:block;width:100%;margin:0;
            border:1px solid #dedede;border-bottom:0;border-radius:0;background:#fff;overflow:hidden}
          .recursion-panel-output:first-child .recursion-info-section{
            border-radius:5px 5px 0 0}
          .recursion-panel-output:last-child .recursion-info-section{
            border-bottom:1px solid #dedede;border-radius:0 0 5px 5px}
          .recursion-info-section>summary,.recursion-tree-panel-summary{
            box-sizing:border-box!important;display:block!important;width:100%!important;
            min-height:44px!important;padding:10px 14px!important;border:0!important;
            border-radius:0!important;background:#f7f7f7!important;color:#333!important;
            cursor:pointer!important;font-family:sans-serif!important;font-size:16px!important;
            font-weight:700!important;line-height:24px!important;text-align:left!important;
            list-style:none!important}
          .recursion-info-section>summary::-webkit-details-marker{display:none}
          .recursion-info-section>summary::before,.recursion-tree-panel-summary::before{
            box-sizing:border-box;display:inline-block;width:20px;margin-right:0;
            color:#333;font-family:sans-serif;font-size:15px;font-weight:400;
            line-height:1;text-align:left;content:"▶";transform-origin:7px 50%;
            transition:transform .12s ease}
          .recursion-info-section[open]>summary::before,
          .recursion-tree-panel-summary[aria-expanded="true"]::before{
            transform:rotate(90deg)}
          .recursion-info-section[open]>summary{border-bottom:1px solid #e2e2e2}
          .recursion-tree-widget-panel{box-sizing:border-box;width:100%!important;margin:0!important;
            border:1px solid #dedede;border-bottom:0;border-radius:0;background:#fff;overflow:hidden}
          .recursion-tree-panel-summary[aria-expanded="true"]{border-bottom:1px solid #e2e2e2}
          .recursion-tree-panel-content{box-sizing:border-box;width:100%!important;
            padding:12px;background:#fff;overflow:hidden}
          .recursion-tree-panel-content.is-collapsed{display:none!important}
          .recursion-equation{width:100%;box-sizing:border-box;padding:16px 20px;
            text-align:center;font-size:15px}
          .recursion-level-table{display:flex;flex-direction:column;
            box-sizing:border-box;align-items:center;justify-content:center;overflow:clip;
            padding-bottom:12px;text-align:center;font-size:16px}
          .recursion-level-table-output,.recursion-level-table-output .widget-htmlmath-content,
          .recursion-level-table-output .widget-html-content{box-sizing:border-box;width:100%!important;
            display:flex!important;flex-direction:column!important;align-items:center!important;
            justify-content:center!important;text-align:center!important}
          .recursion-level-table table{display:table;width:max-content!important;max-width:100%;
            margin:0 auto!important;border-collapse:collapse;text-align:center}
          .recursion-level-table th,.recursion-level-table td{padding:7px 16px;
            border-bottom:1px solid var(--jp-border-color2,#d0d0d0);text-align:center;
            box-sizing:border-box;height:40px;vertical-align:middle;white-space:nowrap;
            background:#fff!important;color:#000!important;
            transition:opacity .18s,background .18s}
          .recursion-level-table th{font-weight:700}
          .recursion-level-table mjx-container{color:#000!important}
          .recursion-level-table tr[data-level]{cursor:pointer}
          .recursion-level-table tr[data-level]:hover td,
          .recursion-level-table tr.is-highlighted td{background:#f2f2f2!important}
          .recursion-level-table tr.is-selected td{background:#e3edf8!important;
            font-weight:600}
          .recursion-level-table tr.case-base td{background:#e8f5e9!important}
          .recursion-level-table tr.case-base:hover td,
          .recursion-level-table tr.case-base.is-highlighted td{background:#dff0e2!important}
          .recursion-master-variant-note,
          .recursion-master-variant-note .widget-html-content{box-sizing:border-box;
            width:188px!important;text-align:center!important}
          .recursion-master-variant-note .recursion-term-validation{
            width:100%;text-align:center!important}
          .recursion-level-table tr.level-pending{pointer-events:none}
          .recursion-plot-container{position:relative;box-sizing:border-box;width:100%;min-width:0;
            max-width:100%;overflow:hidden!important}
          .recursion-figure-output,
          .recursion-figure-output .widget-htmlmath-content,
          .recursion-figure-output .widget-html-content{
            box-sizing:border-box;width:100%!important;max-width:100%!important;
            min-width:0!important;overflow:hidden!important}
          .recursion-zoom-toolbar{position:absolute!important;top:10px;right:10px;
            z-index:20!important;width:auto!important;height:32px!important;
            overflow:visible!important;pointer-events:auto!important}
          .recursion-zoom-toolbar .widget-html-content{overflow:visible!important;background:transparent!important}
          .recursion-tree-plot-wrap{position:relative;box-sizing:border-box;width:100%;
            min-width:0;min-height:300px;overflow:hidden;border:1px solid #e0e0e0;background:#fff}
          .recursion-zoom-controls{display:flex!important;gap:0!important;visibility:visible!important}
          .recursion-zoom-btn{width:34px;height:32px;padding:0;border:1px solid #bbb;
            border-radius:0;background:#f7f7f7!important;color:#333;cursor:pointer;
            font-size:20px;line-height:1}
          .recursion-zoom-btn:hover{background:#eee!important}
          .recursion-tree-figure{box-sizing:border-box;width:100%;max-width:100%;min-width:0;
            margin:0;overflow:hidden;color:#111;background:#fff}
          .recursion-tree-figure>svg{display:block;width:100%;min-width:0;max-width:100%;
            height:auto;margin:0 auto;background:#fff;transform:translateZ(0);
            backface-visibility:hidden}
          .tree-edge{fill:none;stroke:#202124;stroke-width:1.7}
          .tree-edge.symbolic-jump{stroke-dasharray:5 6}
          .tree-edge.level-past{opacity:.48}
          .tree-node.level-past>circle,
          .tree-node.level-past>.tree-node-equation,
          .tree-node.level-past>.tree-node-math{opacity:.48}
          .tree-continuation{fill:none;stroke:#5f6368;stroke-width:1.5;stroke-dasharray:4 5}
          .arrow-head{fill:#202124}
          .tree-node{cursor:pointer;transition:opacity .18s}
          .tree-node circle{fill:#fff;stroke:#202124;stroke-width:1.7}
          .tree-node.is-selected circle{fill:#f2f2f2;stroke-width:2.6}
          .tree-node.is-highlighted circle{fill:#fff;stroke-width:2.2}
          .tree-node.case-base circle{fill:#e8f5e9}
          .tree-node.case-base.is-selected circle,
          .tree-node.case-base.is-highlighted circle{fill:#dff0e2}
          .tree-node.is-collapsed circle{stroke-dasharray:4 3}
          .tree-node.is-dimmed,.tree-edge.is-dimmed{opacity:.15!important}
          .branch-hidden{display:none}
          .continuation-label,.level-label{fill:#111;text-anchor:middle;
            font-family:"STIX Two Math","Cambria Math","Times New Roman",serif}
          .tree-node-equation{box-sizing:border-box;width:100%;height:100%;display:flex;
            align-items:center;justify-content:center;overflow:hidden;color:#111;
            padding:2px;font-size:14px;text-align:center;pointer-events:none}
          .tree-node-equation mjx-container{display:flex!important;width:100%!important;
            max-width:100%!important;height:100%!important;margin:0!important;
            align-items:center!important;justify-content:center!important;font-size:100%!important}
          .tree-node-equation mjx-container>svg{display:block!important;max-width:100%!important;
            max-height:100%!important;width:auto!important;height:auto!important}
          .tree-node-math,.tree-node-math-svg{pointer-events:none}
          .tree-node-cost-tooltip{display:none;overflow:visible;pointer-events:none}
          .tree-node:hover>.tree-node-cost-tooltip,
          .tree-node:focus>.tree-node-cost-tooltip{display:block}
          .tree-node-cost-tooltip-content{box-sizing:border-box;width:max-content;
            max-width:220px;margin:0 auto;padding:7px 12px;border:2px solid #fff!important;
            border-radius:5px;background:#123a63!important;color:#fff!important;
            font:600 15px/1.35 system-ui,sans-serif;text-align:center;
            box-shadow:0 4px 12px rgba(0,0,0,.5);white-space:nowrap}
          .tree-node-cost-tooltip-content mjx-container,
          .tree-node-cost-tooltip-content mjx-container *{color:#fff!important;
            fill:#fff!important;stroke:#fff!important}
          .tree-node-cost-tooltip-content mjx-container{font-size:17px!important;
            margin:0!important}
          .tree-node-cost-tooltip-content mjx-container svg,
          .tree-node-cost-tooltip-content mjx-container svg *{color:#fff!important;
            fill:#fff!important;stroke:transparent!important}
          .continuation-label{font-size:22px}.level-label{text-anchor:end;font-size:15px}
          .recursion-tree-note{box-sizing:border-box;width:100%;min-height:30px;padding:6px 10px;
            color:#555;background:#fff;text-align:center;font-size:13px}
        </style>
        """
    )

    def parse_term_parameters():
        term_count_value = parameter_state["m"]
        raw_a = term_a_input.value.strip()
        raw_b = term_b_input.value.strip()
        error = ""
        if (
            raw_a.count(",") != term_count_value - 1
            or raw_b.count(",") != term_count_value - 1
        ):
            error = (
                rf"Cada campo debe contener \(m-1={term_count_value - 1}\) comas "
                rf"para definir exactamente \(m={term_count_value}\) valores."
            )
        try:
            values_a = [int(value.strip()) for value in raw_a.split(",")]
            if relation_type.value == "reduction":
                values_b = [int(value.strip()) for value in raw_b.split(",")]
            else:
                values_b = [float(value.strip()) for value in raw_b.split(",")]
        except ValueError:
            values_a, values_b = [], []
            error = r"Usa únicamente valores numéricos separados por comas."
        if not error and (
            len(values_a) != term_count_value or len(values_b) != term_count_value
        ):
            error = rf"Se requieren exactamente \(m={term_count_value}\) valores en cada campo."
        if not error and any(value < 1 for value in values_a):
            error = r"Cada \(a_i\) debe ser un entero mayor o igual que \(1\)."
        if (
            not error
            and relation_type.value == "reduction"
            and any(value < 1 for value in values_b)
        ):
            error = r"En una reducción, cada \(b_i\) debe pertenecer a \(\mathbb{N}^{+}\)."
        if (
            not error
            and relation_type.value == "division"
            and any(not 0 < value < 1 for value in values_b)
        ):
            error = r"Cada \(b_i\) debe satisfacer \(0<b_i<1\)."

        for control in (term_a_input, term_b_input):
            if error:
                control.add_class("recursion-term-input-invalid")
            else:
                control.remove_class("recursion-term-input-invalid")
        term_validation.value = (
            f'<div class="recursion-term-validation">{error}</div>'
            if error
            else '<div class="recursion-term-validation"></div>'
        )
        return None if error else (values_a, values_b)

    def parse_base_case():
        try:
            value = float(base_case_input.value.strip())
        except ValueError:
            base_case_input.add_class("recursion-term-input-invalid")
            return None
        if not math.isfinite(value):
            base_case_input.add_class("recursion-term-input-invalid")
            return None
        base_case_input.remove_class("recursion-term-input-invalid")
        return value

    def update_master_variant_options(parsed=None):
        if not builder_only or method.value != "master":
            return
        if parsed is None:
            parsed = parse_term_parameters()
        if parsed is None:
            master_flavor.options = []
            master_flavor.disabled = True
            master_variant_note.value = (
                '<div class="recursion-term-validation">'
                "Corrige los parámetros para determinar las versiones aplicables."
                "</div>"
            )
            return
        term_a, term_b = parsed
        current_variant = master_flavor.value
        selected_function = function_type.value
        if selected_function in {"zero", "exponential", "factorial"}:
            variants = []
        elif len(term_a) != 1:
            variants = [("Generalizado", "generalized")]
        else:
            variants = []
            if (
                selected_function not in {"logarithmic", "log_linear"}
                and not (
                    selected_function == "polylogarithmic"
                    and parameter_state["p"] != 0
                )
            ):
                variants.append(("Básico", "basic"))
            variants.extend([
                ("Extendido", "extended"),
                ("Generalizado", "generalized"),
            ])
        master_flavor.options = variants
        available = {value for _, value in variants}
        master_flavor.value = (
            current_variant if current_variant in available
            else (variants[0][1] if variants else None)
        )
        master_flavor.disabled = not variants
        master_variant_note.value = (
            '<div class="recursion-term-validation"></div>'
            if variants
            else (
                '<div class="recursion-term-validation">'
                "Ninguna versión del teorema maestro aplica a la función seleccionada."
                "</div>"
            )
        )

    def update(*_):
        h, k, p, ell = (
            parameter_state[key] for key in ("h", "k", "p", "ell")
        )
        function_parameters = (
            (k, p, ell)
            if function_type.value == "polylogarithmic"
            else k
        )
        parsed = parse_term_parameters()
        base_value = parse_base_case()
        if parsed is None or base_value is None:
            note.value = (
                '<div class="recursion-tree-note">'
                "Corrige los valores de \\(a_i\\) y \\(b_i\\) para actualizar el árbol."
                "</div>"
            )
            return
        term_a, term_b = parsed
        update_master_variant_options(parsed)
        parameter_state["term_a"] = term_a
        parameter_state["term_b"] = term_b
        branching_factor = sum(term_a)
        reduction_parameter = max(term_b) if relation_type.value == "reduction" else 2
        animation_state["level"] = min(animation_state["level"], h)
        active = animation_state["level"]
        degree_control.layout.display = (
            "flex"
            if function_type.value in {"polynomial", "polylogarithmic"}
            else "none"
        )
        logarithmic_power_control.layout.display = (
            "flex" if function_type.value == "polylogarithmic" else "none"
        )
        logarithmic_base_control.layout.display = (
            "flex" if function_type.value == "polylogarithmic" else "none"
        )
        balanced = len(set(term_b)) == 1
        equation.value = _equation_markup(
            relation_type.value,
            branching_factor,
            reduction_parameter,
            function_type.value,
            function_parameters,
            term_a,
            term_b,
        )
        expanded_equation.value = _expanded_equation_markup(
            relation_type.value,
            term_a,
            term_b,
            function_type.value,
            function_parameters,
            base_value,
        )
        level_table.value = _level_table_markup(
            relation_type.value,
            branching_factor,
            reduction_parameter,
            h,
            balanced,
            function_type.value,
            function_parameters,
            active,
            term_a,
            term_b,
        )
        figure.value = _render_svg(
            relation_type.value,
            branching_factor,
            reduction_parameter,
            h,
            balanced,
            function_type.value,
            function_parameters,
            active,
            "recursion-arrow-single",
            term_a,
            term_b,
        )
        visible = _visible_depth(branching_factor, h)
        if visible < h:
            message = "Las ramas punteadas indican niveles omitidos para mantener los nodos legibles."
        elif len(set(term_b)) > 1:
            message = "La tabla presenta un intervalo porque las ramas usan valores distintos de \\(b_i\\)."
        elif branching_factor == 1:
            message = r"Con \(a_1=1\), el árbol se reduce a una cadena."
        else:
            message = ""
        note.value = f'<div class="recursion-tree-note">{message}</div>'

    def reset_progress(*_):
        animation_state["level"] = 0
        update()

    def change_level(delta):
        animation_state["level"] = min(
            parameter_state["h"], max(0, animation_state["level"] + delta)
        )
        update()

    previous_level.on_click(lambda _: change_level(-1))
    next_level.on_click(lambda _: change_level(1))
    reset.on_click(reset_progress)
    def change_relation(change):
        if change.get("name") != "value":
            return
        update_method_options()
        default_b = 1 if relation_type.value == "reduction" else 0.5
        parameter_state["term_b"] = [default_b] * parameter_state["m"]
        term_b_input.value = ", ".join(
            f"{value:g}" for value in parameter_state["term_b"]
        )
        reset_progress()

    def reset_builder(*_):
        parameter_state.update(
            h=3,
            k=4,
            p=1,
            ell=2,
            m=1,
            term_a=[2],
            term_b=[0.5],
        )
        for name in ("h", "k", "p", "ell", "m"):
            parameter_readouts[name].value = rf"\({parameter_state[name]}\)"
        relation_type.value = "division"
        function_type.value = "linear"
        method.value = "iterative"
        master_flavor.value = None
        base_case_input.value = "1"
        term_a_input.value = "2"
        term_b_input.value = "0.5"
        method_solution.value = ""
        method_solution.layout.display = "none"
        reset_progress()

    def solve_builder(*_):
        parsed = parse_term_parameters()
        base_value = parse_base_case()
        if parsed is None or base_value is None:
            method_solution.value = ""
            method_solution.layout.display = "none"
            return
        from capitulo5.recurrence_solution_methods import (
            SOLUTION_STYLES,
            solve_selected_method,
        )

        term_a, term_b = parsed
        update_master_variant_options(parsed)
        if method.value == "master" and master_flavor.value is None:
            method_solution.value = SOLUTION_STYLES + (
                '<details class="recursion-info-section method-solution-panel" open>'
                '<summary>Teorema maestro '
                '<span class="method-status-no">No aplica</span></summary>'
                '<div class="method-solution-content"><p>Ninguna versión del '
                'teorema maestro es compatible con la función seleccionada.</p></div>'
                '</details>'
            )
            method_solution.layout.display = "flex"
            return
        method_solution.value = SOLUTION_STYLES + solve_selected_method(
            relation_type.value,
            tuple(term_a),
            tuple(term_b),
            function_type.value,
            (
                (
                    parameter_state["k"],
                    parameter_state["p"],
                    parameter_state["ell"],
                )
                if function_type.value == "polylogarithmic"
                else parameter_state["k"]
            ),
            method.value,
            master_flavor.value,
            base_value,
        )
        method_solution.layout.display = "flex"

    def reset_on_method_change(change):
        if change.get("name") != "value" or change.get("old") == change.get("new"):
            return
        method_solution.value = ""
        method_solution.layout.display = "none"
        reset_progress()

    relation_type.observe(change_relation, names="value")
    function_type.observe(reset_progress, names="value")
    for control in (term_a_input, term_b_input, base_case_input):
        control.observe(reset_progress, names="value")
    method.observe(reset_on_method_change, names="value")
    builder_resolve.on_click(solve_builder)
    builder_reset.on_click(reset_builder)

    app = widgets.VBox(
        [styles, panels],
        layout=widgets.Layout(width="100%"),
    )
    app.add_class("recursion-tree-root")
    app.add_class(
        "recursion-runtime-colab" if RUNNING_IN_COLAB else "recursion-runtime-local"
    )

    def cleanup():
        app.close()

    builtins._recursion_tree_app_cleanup = cleanup
    update()
    clear_output(wait=True)
    display(app)
    display(Javascript(
        r"""
        (() => {
          if (!window.__recursionTreeMathJaxReady) {
            if (window.MathJax && typeof window.MathJax.typesetPromise === 'function') {
              window.__recursionTreeMathJaxReady = Promise.resolve(window.MathJax);
            } else {
              window.__recursionTreeMathJaxReady = new Promise((resolve, reject) => {
              window.MathJax = {
                tex: {
                  inlineMath: [['\\(', '\\)'], ['$$', '$$']],
                  displayMath: [['\\[', '\\]'], ['$$', '$$']]
                },
                svg: {fontCache: 'none'}
              };
              const script = document.createElement('script');
              script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js';
              script.async = true;
              script.onload = () => {
                const startup = window.MathJax?.startup?.promise;
                Promise.resolve(startup).then(
                  () => resolve(window.MathJax),
                  reject
                );
              };
              script.onerror = () => reject(
                new Error('No fue posible cargar MathJax.')
              );
              document.head.appendChild(script);
              });
            }
          }
          if (window.__recursionTreeController) {
            window.__recursionTreeController.abort();
          }
          const controller = new AbortController();
          const signal = controller.signal;
          const roots = document.querySelectorAll('.recursion-tree-root');
          const activeRoot = roots.length ? roots[roots.length - 1] : null;
          if (!activeRoot) return;
          let playbackTimer = 0;
          let playbackCount = -1;
          const stopPlayback = () => {
            if (playbackTimer) clearTimeout(playbackTimer);
            playbackTimer = 0;
            playbackCount = -1;
          };
          const widgetButton = selector => {
            const element = activeRoot.querySelector(selector);
            if (!element) return null;
            return element.matches('button') ? element : element.querySelector('button');
          };
          const schedulePlayback = delay => {
            clearTimeout(playbackTimer);
            playbackTimer = setTimeout(playbackStep, delay);
          };
          const playbackStep = () => {
            if (!activeRoot.isConnected) {
              stopPlayback();
              return;
            }
            const pending = activeRoot.querySelector('.recursion-level-table tr.level-pending');
            const completed = activeRoot.querySelectorAll(
              '.recursion-level-table tr[data-level]'
            ).length;
            if (!pending) {
              if (playbackCount === -2) schedulePlayback(100);
              else stopPlayback();
              return;
            }
            if (playbackCount === -2) playbackCount = -1;
            if (typesetRunning || typesetQueued || completed === playbackCount) {
              schedulePlayback(100);
              return;
            }
            playbackCount = completed;
            widgetButton('.recursion-next-button')?.click();
            schedulePlayback(100);
          };
          const rootFor = el => el.closest('.recursion-tree-root');
          const pathIsDescendant = (path, parent) =>
            parent === '' ? path !== '' : path.startsWith(parent + '.');
          const clearHover = root => root.querySelectorAll('.is-dimmed,.is-highlighted')
            .forEach(el => el.classList.remove('is-dimmed','is-highlighted'));
          const highlightLevel = (root, level) => {
            clearHover(root);
            root.querySelectorAll('[data-level]').forEach(el => {
              if (el.dataset.level === level) el.classList.add('is-highlighted');
              else el.classList.add('is-dimmed');
            });
          };
          const applyZoom = root => {
            const zoom = Number(root.dataset.treeZoom || 1);
            root.querySelectorAll('.recursion-tree-figure>svg').forEach(svg => {
              const width = Number(svg.dataset.baseWidth || 760);
              const height = Number(svg.dataset.baseHeight || 400);
              const visibleWidth = width / zoom;
              const visibleHeight = height / zoom;
              const x = (width - visibleWidth) / 2;
              const y = (height - visibleHeight) / 2;
              svg.setAttribute('viewBox', `${x} ${y} ${visibleWidth} ${visibleHeight}`);
              svg.style.width = '100%';
            });
          };
          const repaintGraph = root => {
            root.querySelectorAll('.recursion-tree-figure>svg').forEach(svg => {
              svg.style.visibility = 'hidden';
              void svg.getBoundingClientRect();
              svg.style.visibility = 'visible';
            });
          };
          document.addEventListener('click', event => {
            const summary = event.target.closest('.recursion-tree-panel-summary');
            if (!summary) return;
            const panel = summary.closest('.recursion-tree-widget-panel');
            const content = panel?.querySelector('.recursion-tree-panel-content');
            if (!content) return;
            const collapsed = content.classList.toggle('is-collapsed');
            summary.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
            const marker = summary.querySelector('.recursion-panel-marker');
            if (marker) marker.textContent = collapsed ? '▸' : '▾';
          }, {signal});
          document.addEventListener('click', event => {
            if (!activeRoot.contains(event.target)) return;
            if (event.target.closest('.recursion-play-button')) {
              stopPlayback();
              if (!activeRoot.querySelector('.recursion-level-table tr.level-pending')) {
                playbackCount = -2;
                widgetButton('.recursion-reset-button')?.click();
              } else {
                playbackCount = -1;
              }
              schedulePlayback(100);
              return;
            }
            if (
              event.target.closest('.recursion-pause-button') ||
              event.target.closest('.recursion-reset-button') ||
              event.target.closest('.recursion-previous-button') ||
              (event.isTrusted && event.target.closest('.recursion-next-button')) ||
              event.target.closest('.recursion-tree-controls')
            ) {
              stopPlayback();
            }
          }, {signal});
          document.addEventListener('change', event => {
            if (activeRoot.contains(event.target) && event.target.closest('.recursion-tree-controls')) {
              stopPlayback();
            }
          }, {signal});
          document.addEventListener('click', event => {
            const button = event.target.closest('[data-tree-zoom]');
            if (!button) return;
            const root = rootFor(button);
            let zoom = Number(root.dataset.treeZoom || 1);
            if (button.dataset.treeZoom === 'in') zoom = Math.min(2.5, zoom * 1.2);
            else if (button.dataset.treeZoom === 'out') zoom = Math.max(0.5, zoom / 1.2);
            else zoom = 1;
            root.dataset.treeZoom = String(zoom);
            applyZoom(root);
          }, {signal});
          let repaintTimer = 0;
          let typesetTimer = 0;
          let typesetRunning = false;
          let typesetQueued = false;
          const nodeMathCache = new Map();
          const nodeMathTemplate = (mathJax, tex) => {
            if (!nodeMathCache.has(tex)) {
              nodeMathCache.set(
                tex,
                mathJax.tex2svgPromise(tex, {display: false}).then(output => {
                  const svg = output.querySelector('svg');
                  if (!svg) throw new Error(`No se pudo formatear ${tex}`);
                  return svg;
                })
              );
            }
            return nodeMathCache.get(tex);
          };
          const renderNodeMath = mathJax => Promise.all(
            Array.from(activeRoot.querySelectorAll('.tree-node-math:not([data-rendered])'))
              .map(async holder => {
                holder.dataset.rendered = 'true';
                const source = await nodeMathTemplate(mathJax, holder.dataset.nodeTex);
                const svg = source.cloneNode(true);
                const x = Number(holder.dataset.x);
                const y = Number(holder.dataset.y);
                const enlarged = holder.classList.contains('solution-tree-node-label');
                const width = enlarged ? 56 : 50;
                const height = enlarged ? 38 : 30;
                svg.setAttribute('x', String(x - width / 2));
                svg.setAttribute('y', String(y - height / 2));
                svg.setAttribute('width', String(width));
                svg.setAttribute('height', String(height));
                svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');
                svg.classList.add('tree-node-math-svg');
                holder.appendChild(svg);
              })
          );
          const typesetActiveApp = () => {
            typesetQueued = true;
            clearTimeout(typesetTimer);
            typesetTimer = setTimeout(() => {
              if (typesetRunning) return;
              typesetRunning = true;
              typesetQueued = false;
              window.__recursionTreeMathJaxReady
                .then(mathJax =>
                  mathJax.typesetPromise([activeRoot])
                    .then(() => renderNodeMath(mathJax))
                )
                .then(() => {
                  applyZoom(activeRoot);
                  repaintGraph(activeRoot);
                })
                .catch(error => console.error(error))
                .finally(() => {
                  typesetRunning = false;
                  if (typesetQueued) typesetActiveApp();
                });
            }, 40);
          };
          const observer = new MutationObserver(() => {
            clearTimeout(repaintTimer);
            repaintTimer = setTimeout(() => {
              typesetActiveApp();
            }, 40);
          });
          observer.observe(activeRoot, {childList:true, subtree:true});
          typesetActiveApp();
          document.addEventListener('mouseover', event => {
            const target = event.target.closest('[data-tree-node],.recursion-level-table tr[data-level]');
            if (target) highlightLevel(rootFor(target), target.dataset.level);
          }, {signal});
          document.addEventListener('mouseout', event => {
            const target = event.target.closest('[data-tree-node],.recursion-level-table tr[data-level]');
            if (target && !target.contains(event.relatedTarget)) clearHover(rootFor(target));
          }, {signal});
          document.addEventListener('click', event => {
            const row = event.target.closest('.recursion-level-table tr[data-level]');
            if (row) {
              const root = rootFor(row);
              root.querySelectorAll(
                '.recursion-level-table tr.is-selected'
              ).forEach(el => el.classList.remove('is-selected'));
              root.querySelectorAll(
                '.tree-node.is-selected'
              ).forEach(el => el.classList.remove('is-selected'));
              row.classList.add('is-selected');
              root.querySelectorAll(
                `.tree-node[data-level="${row.dataset.level}"]`
              ).forEach(el => el.classList.add('is-selected'));
              return;
            }
            const node = event.target.closest('[data-tree-node]');
            if (!node) return;
            const root = rootFor(node);
            root.querySelectorAll('.tree-node.is-selected').forEach(el => el.classList.remove('is-selected'));
            node.classList.add('is-selected');
          }, {signal});
          document.addEventListener('dblclick', event => {
            const node = event.target.closest('[data-tree-node]');
            if (!node) return;
            event.preventDefault();
            const root = rootFor(node), path = node.dataset.path;
            const collapsed = node.classList.toggle('is-collapsed');
            root.querySelectorAll('[data-tree-node]').forEach(el => {
              if (pathIsDescendant(el.dataset.path, path)) el.classList.toggle('branch-hidden', collapsed);
            });
            root.querySelectorAll('.tree-edge').forEach(el => {
              if (pathIsDescendant(el.dataset.childPath, path))
                el.classList.toggle('branch-hidden', collapsed);
            });
          }, {signal});
          window.__recursionTreeController = {
            abort() {
              controller.abort();
              observer.disconnect();
              stopPlayback();
              clearTimeout(repaintTimer);
              clearTimeout(typesetTimer);
            }
          };
        })();
        """
    ))
