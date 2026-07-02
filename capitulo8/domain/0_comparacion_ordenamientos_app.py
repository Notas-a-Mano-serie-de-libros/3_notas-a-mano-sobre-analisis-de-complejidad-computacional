from __future__ import annotations

from html import escape

from IPython.display import display
import ipywidgets as widgets

from sort_common import colab_pause, copy_sort_state, create_state as create_sort_state, generate_values, step_sort
from sort_config import DEFAULT_BAR_SIZE, FONT_FAMILY, MAX_SIZE, ORDER_OPTIONS, ROLE_STYLES

try:
    from google.colab import output as colab_output
except ImportError:
    colab_output = None


ALGORITHMS = (
    ("mezcla", "Ordenamiento<br>mezcla"),
    ("rapido", "Ordenamiento<br>rápido"),
    ("insercion", "Ordenamiento<br>inserción"),
    ("burbuja", "Ordenamiento<br>burbuja"),
    ("seleccion", "Ordenamiento<br>selección"),
)
ALGORITHM_OPTIONS = (
    ("Mezcla", "mezcla"),
    ("Rápido", "rapido"),
    ("Inserción", "insercion"),
    ("Burbuja", "burbuja"),
    ("Selección", "seleccion"),
)
DEFAULT_ALGORITHMS = tuple(value for _label, value in ALGORITHM_OPTIONS)
ALGORITHM_COLUMN_WIDTHS = (118, 138, 122)
ALGORITHM_COLUMN_GAP = 8
ALGORITHM_ROW_HEIGHT = 34
ALGORITHM_ROW_GAP = 2
ALGORITHM_FIELD_PADDING_X = 8
ALGORITHM_FIELD_PADDING_Y = 5
ALGORITHM_FIELD_WIDTH = sum(ALGORITHM_COLUMN_WIDTHS) + (len(ALGORITHM_COLUMN_WIDTHS) - 1) * ALGORITHM_COLUMN_GAP + 2 * ALGORITHM_FIELD_PADDING_X + 2
ALGORITHM_FIELD_HEIGHT = 2 * ALGORITHM_ROW_HEIGHT + ALGORITHM_ROW_GAP + 2 * ALGORITHM_FIELD_PADDING_Y + 2
ALGORITHM_GROUP_GAP = 2
ALGORITHM_GROUP_WIDTH = ALGORITHM_FIELD_WIDTH


def create_algorithm_state(key, title, values, descending):
    return {
        "key": key,
        "title": title,
        "state": create_sort_state(key, size=len(values), descending=descending, values=values, view="barras"),
        "steps": 0,
        "html_cache": {},
    }


def create_comparison_state(size=DEFAULT_BAR_SIZE, values=None, descending=False, selected_algorithms=None):
    values = list(values) if values is not None else generate_values(size)
    selected = set(selected_algorithms if selected_algorithms is not None else DEFAULT_ALGORITHMS)
    algorithms = [
        create_algorithm_state(key, title, values, descending)
        for key, title in ALGORITHMS
        if key in selected
    ]
    return {
        "values": values,
        "descending": descending,
        "selected_algorithms": tuple(key for key, _title in ALGORITHMS if key in selected),
        "algorithms": algorithms,
    }


def step_all_sorts(state):
    for item in state["algorithms"]:
        sort_state = item["state"]
        if not sort_state["sorting_complete"]:
            step_sort(sort_state)
            item["steps"] += 1


def all_sorts_complete(state):
    return all(item["state"]["sorting_complete"] for item in state["algorithms"])


def copy_sort_item(item):
    return {
        **item,
        "state": copy_sort_state(item["state"]),
        "html_cache": dict(item.get("html_cache", {})),
    }


def copy_comparison_state(state):
    return {
        **state,
        "values": list(state["values"]),
        "selected_algorithms": tuple(state["selected_algorithms"]),
        "algorithms": [copy_sort_item(item) for item in state["algorithms"]],
    }


def build_comparison_trace(state):
    probe = copy_comparison_state(state)
    trace = []
    while not all_sorts_complete(probe):
        step_all_sorts(probe)
        trace.append(copy_comparison_state(probe))
    return trace


def selected_from_checks(algorithm_checks):
    return tuple(
        key
        for key, checkbox in algorithm_checks.items()
        if checkbox.value
    )


def render_index_row(values):
    indexes = "".join(f'<div class="comparison-index">{index}</div>' for index, _value in enumerate(values))
    return f'<div class="comparison-index-row">{indexes}</div>'


def render_bar(value, role, max_value):
    fill, _border, text = ROLE_STYLES[role]
    height = 18 + (value / max_value) * 170 if max_value else 18
    return f"""
    <div class="comparison-bar-wrap">
      <div class="comparison-bar-area">
        <div class="comparison-bar-stack">
          <div class="comparison-bar-value">{escape(str(value))}</div>
          <div class="comparison-bar" style="height:{height}px; background:{fill}; color:{text};"></div>
        </div>
      </div>
    </div>
    """


def render_bars(item, show_indexes=False):
    cache_key = "with_indexes" if show_indexes else "plain"
    if item["state"]["sorting_complete"] and cache_key in item["html_cache"]:
        return item["html_cache"][cache_key]

    sort_state = item["state"]
    values = sort_state["arr"]
    max_value = max(values) if values else 1
    indexes = render_index_row(values) if show_indexes else ""
    bars = "".join(
        render_bar(value, sort_state["roles"][index], max_value)
        for index, value in enumerate(values)
    )
    html = f"""
    <div class="comparison-row">
      <div class="comparison-name">{item["title"]}</div>
      <div class="comparison-steps">{item["steps"]}</div>
      <div class="comparison-array-wrap">
        <div class="comparison-bars">{bars}</div>
        {indexes}
      </div>
    </div>
    """
    if item["state"]["sorting_complete"]:
        item["html_cache"][cache_key] = html
    return html


def render_comparison_styles():
    return f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400;700&display=swap');
      .comparison-app {{
        width: 100%;
        box-sizing: border-box;
        font-family: '{FONT_FAMILY}', serif;
        color: #ffffff;
        background: #000000;
        padding: 8px;
      }}
      .comparison-app * {{
        box-sizing: border-box;
      }}
      .comparison-table {{
        display: flex;
        flex-direction: column;
        gap: 0;
        width: 100%;
        background: #000000;
      }}
      .comparison-header,
      .comparison-row {{
        display: grid;
        grid-template-columns: minmax(96px, 128px) 62px minmax(0, 1fr);
        gap: 8px;
        width: 100%;
        background: #000000;
        font-family: '{FONT_FAMILY}', serif;
        color: #ffffff;
      }}
      .comparison-header {{
        align-items: end;
        padding-bottom: 0;
      }}
      .comparison-row {{
        align-items: center;
      }}
      .comparison-head-cell,
      .comparison-name {{
        font-size: 22px;
        line-height: 1.2;
        color: #ffffff;
        text-align: center;
        font-weight: 700;
      }}
      .comparison-steps {{
        font-size: 20px;
        color: #ffffff;
        text-align: center;
        white-space: nowrap;
      }}
      .comparison-array-wrap {{
        min-width: 0;
        overflow-x: hidden;
        background: #000000;
        padding: 8px 0 4px;
      }}
      .comparison-bars {{
        display: flex;
        align-items: flex-end;
        justify-content: center;
        gap: clamp(1px, 0.35vw, 3px);
        min-height: 220px;
        width: 100%;
      }}
      .comparison-bar-wrap {{
        width: auto;
        flex: 1 1 0;
        min-width: 8px;
        max-width: 34px;
        text-align: center;
      }}
      .comparison-bar-area {{
        height: 200px;
        display: flex;
        align-items: flex-end;
        justify-content: center;
      }}
      .comparison-bar-stack {{
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
      }}
      .comparison-bar-value {{
        color: #ffffff;
        font-size: 14px;
        line-height: 16px;
        height: 18px;
        margin-bottom: 2px;
        overflow: hidden;
      }}
      .comparison-bar {{
        width: 100%;
        border: none;
        border-radius: 0;
      }}
      .comparison-index-row {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: clamp(1px, 0.35vw, 3px);
        min-height: 20px;
        padding-top: 4px;
        width: 100%;
      }}
      .comparison-index {{
        width: auto;
        flex: 1 1 0;
        min-width: 8px;
        max-width: 34px;
        text-align: center;
        color: #ffffff;
        font-size: 14px;
        line-height: 16px;
        overflow: hidden;
      }}
      @media (max-width: 760px) {{
        .comparison-header {{
          display: none;
        }}
        .comparison-row {{
          grid-template-columns: 1fr;
          gap: 6px;
        }}
        .comparison-steps {{
          font-size: 18px;
        }}
      }}
      @media (min-width: 761px) {{
        .comparison-name,
        .comparison-steps {{
          white-space: nowrap;
        }}
      }}
    </style>
    """


def render_comparison_header_html():
    return """
    <div class="comparison-header">
      <div class="comparison-head-cell">Algoritmo</div>
      <div class="comparison-head-cell">Pasos</div>
      <div class="comparison-head-cell">Arreglo</div>
    </div>
    """


def render_comparison_rows_html(state):
    return "".join(
        render_bars(item, show_indexes=index == 0)
        for index, item in enumerate(state["algorithms"])
    )


def render_comparison_body_html(state):
    rows = render_comparison_rows_html(state)
    return f"""
    <div class="comparison-app">
      <div class="comparison-table">
        {render_comparison_header_html()}
        {rows}
      </div>
    </div>
    """


def render_comparison_html(state):
    return f"""
    {render_comparison_styles()}
    {render_comparison_body_html(state)}
    """


def run_app():
    if colab_output is not None:
        colab_output.enable_custom_widget_manager()

    size_input = widgets.BoundedIntText(
        value=DEFAULT_BAR_SIZE,
        min=2,
        max=MAX_SIZE,
        step=1,
        description="Tamaño",
        layout=widgets.Layout(width="180px"),
    )
    order_dropdown = widgets.Dropdown(
        options=ORDER_OPTIONS,
        value=False,
        description="Orden",
        layout=widgets.Layout(width="210px"),
    )
    algorithm_checks = {
        value: widgets.Checkbox(value=True, description=label, indent=False, layout=widgets.Layout(width="100%"))
        for label, value in ALGORITHM_OPTIONS
    }
    algorithms_label = widgets.HTML(
        value="Algoritmos activos",
        layout=widgets.Layout(width=f"{ALGORITHM_FIELD_WIDTH}px", height="24px"),
    )
    algorithms_checks_box = widgets.GridBox(
        list(algorithm_checks.values()),
        layout=widgets.Layout(
            width="100%",
            grid_template_columns=" ".join(f"{width}px" for width in ALGORITHM_COLUMN_WIDTHS),
            grid_template_rows=f"repeat(2, {ALGORITHM_ROW_HEIGHT}px)",
            gap=f"{ALGORITHM_ROW_GAP}px {ALGORITHM_COLUMN_GAP}px",
            align_items="center",
            overflow="visible",
        ),
    )
    algorithms_checks_frame = widgets.Box(
        [algorithms_checks_box],
        layout=widgets.Layout(
            width=f"{ALGORITHM_FIELD_WIDTH}px",
            height=f"{ALGORITHM_FIELD_HEIGHT}px",
            border="1px solid #767676",
            padding=f"{ALGORITHM_FIELD_PADDING_Y}px {ALGORITHM_FIELD_PADDING_X}px",
            background_color="#ffffff",
            align_items="center",
            overflow="visible",
        ),
    )
    algorithms_group = widgets.VBox(
        [algorithms_label, algorithms_checks_frame],
        layout=widgets.Layout(
            width=f"{ALGORITHM_GROUP_WIDTH}px",
            align_items="stretch",
            gap=f"{ALGORITHM_GROUP_GAP}px",
            margin="0 0 0 32px",
            overflow="visible",
        ),
    )
    auto_button = widgets.Button(description="Ordenar", button_style="success", layout=widgets.Layout(width="150px"))
    finish_button = widgets.Button(description="Finalizar", button_style="info", disabled=True, layout=widgets.Layout(width="150px"))
    reset_button = widgets.Button(description="Generar nuevo arreglo", button_style="warning", layout=widgets.Layout(width="190px"))
    style_output = widgets.HTML(value=render_comparison_styles(), layout=widgets.Layout(width="100%"))
    body_output = widgets.HTML(layout=widgets.Layout(width="100%", margin="0", padding="0"))
    html_output = widgets.VBox(
        [style_output, body_output],
        layout=widgets.Layout(width="100%"),
    )
    control_state = {"updating": False}
    execution_state = {"running": False, "finish_requested": False}

    def build_state(values=None):
        size = len(values) if values is not None else size_input.value
        return create_comparison_state(
            size=size,
            values=values,
            descending=order_dropdown.value,
            selected_algorithms=selected_from_checks(algorithm_checks),
        )

    state = build_state()

    def redraw(force_static=False):
        if force_static:
            style_output.value = render_comparison_styles()
        body = render_comparison_body_html(state)
        if body_output.value != body:
            body_output.value = body

    def set_idle_buttons():
        execution_state["running"] = False
        execution_state["finish_requested"] = False
        auto_button.disabled = False
        reset_button.disabled = False
        finish_button.disabled = True

    def set_running_buttons():
        execution_state["running"] = True
        execution_state["finish_requested"] = False
        auto_button.disabled = True
        reset_button.disabled = True
        finish_button.disabled = False

    def finish_all_sorts():
        nonlocal state
        trace = build_comparison_trace(state)
        if trace:
            state = trace[-1]

    def reset_comparison(*_args):
        nonlocal state
        if control_state["updating"]:
            return
        state = build_state()
        set_idle_buttons()
        redraw(force_static=True)

    def generate_new(*_args):
        nonlocal state
        state = build_state(values=generate_values(size_input.value))
        set_idle_buttons()
        redraw(force_static=True)

    def run_auto(*_args):
        nonlocal state
        set_running_buttons()
        trace = build_comparison_trace(state)
        for snapshot in trace:
            if execution_state["finish_requested"]:
                finish_all_sorts()
                break
            state = snapshot
            redraw()
            colab_pause()
        redraw()
        set_idle_buttons()

    def finish_comparison(*_args):
        if not execution_state["running"]:
            return
        execution_state["finish_requested"] = True
        finish_button.disabled = True

    auto_button.on_click(run_auto)
    finish_button.on_click(finish_comparison)
    reset_button.on_click(generate_new)
    size_input.observe(lambda change: reset_comparison() if change["name"] == "value" else None, names="value")
    order_dropdown.observe(lambda change: reset_comparison() if change["name"] == "value" else None, names="value")
    for checkbox in algorithm_checks.values():
        checkbox.observe(lambda change: reset_comparison() if change["name"] == "value" else None, names="value")

    layout = widgets.VBox(
        [
            widgets.HBox([size_input, order_dropdown, algorithms_group], layout=widgets.Layout(width="100%", gap="12px")),
            widgets.HBox([auto_button, finish_button, reset_button], layout=widgets.Layout(width="100%", gap="10px", margin="12px 0 0 0")),
            html_output,
        ],
        layout=widgets.Layout(width="100%", gap="10px"),
    )
    display(layout)
    redraw(force_static=True)


__all__ = [
    "ALGORITHMS",
    "ALGORITHM_OPTIONS",
    "DEFAULT_ALGORITHMS",
    "all_sorts_complete",
    "create_comparison_state",
    "render_comparison_html",
    "run_app",
    "selected_from_checks",
    "step_all_sorts",
]
