from __future__ import annotations

import asyncio
from html import escape

from IPython.display import display
import ipywidgets as widgets

from common.widget_controls import bounded_int_control, button_control, compact_labeled_control, dropdown_control
from sort_common import colab_pause, copy_sort_state, create_state as create_sort_state, generate_values, step_sort
from sort_config import DEFAULT_BAR_SIZE, FONT_FAMILY, MAX_SIZE, ORDER_OPTIONS, ROLE_STYLES

try:
    from google.colab import output as colab_output
except ImportError:
    colab_output = None


ALGORITHMS = (
    ("radix", "Ordenamiento<br>radix"),
    ("rapido", "Ordenamiento<br>rápido"),
    ("mezcla", "Ordenamiento<br>mezcla"),
    ("shell", "Ordenamiento<br>Shell"),
    ("insercion", "Ordenamiento<br>inserción"),
    ("seleccion", "Ordenamiento<br>selección"),
    ("burbuja", "Ordenamiento<br>burbuja"),
)
ALGORITHM_OPTIONS = (
    ("Radix", "radix"),
    ("Rápido", "rapido"),
    ("Mezcla", "mezcla"),
    ("Shell", "shell"),
    ("Inserción", "insercion"),
    ("Selección", "seleccion"),
    ("Burbuja", "burbuja"),
)
DEFAULT_ALGORITHMS = tuple(value for _label, value in ALGORITHM_OPTIONS)
ALGORITHM_COLUMN_WIDTHS = (116, 128, 118, 82)
ALGORITHM_COLUMN_GAP = 8
ALGORITHM_ROW_HEIGHT = 34
ALGORITHM_ROW_GAP = 2
ALGORITHM_FIELD_PADDING_X = 8
ALGORITHM_FIELD_PADDING_Y = 5
ALGORITHM_FIELD_WIDTH = sum(ALGORITHM_COLUMN_WIDTHS) + (len(ALGORITHM_COLUMN_WIDTHS) - 1) * ALGORITHM_COLUMN_GAP + 2 * ALGORITHM_FIELD_PADDING_X + 2
ALGORITHM_FIELD_HEIGHT = 2 * ALGORITHM_ROW_HEIGHT + ALGORITHM_ROW_GAP + 2 * ALGORITHM_FIELD_PADDING_Y + 2
ALGORITHM_GROUP_GAP = 2
ALGORITHM_GROUP_WIDTH = ALGORITHM_FIELD_WIDTH
ROW_HTML_CACHE_LIMIT = 512
_ROW_HTML_CACHE = {}


def create_algorithm_state(key, title, values, descending, gap_sequence="shell"):
    return {
        "key": key,
        "title": title,
        "state": create_sort_state(
            key,
            size=len(values),
            descending=descending,
            values=values,
            view="barras",
            gap_sequence=gap_sequence,
        ),
        "steps": 0,
        "html_cache": {},
    }


def create_comparison_state(size=DEFAULT_BAR_SIZE, values=None, descending=False, selected_algorithms=None, gap_sequence="shell"):
    values = list(values) if values is not None else generate_values(size)
    selected = set(selected_algorithms if selected_algorithms is not None else DEFAULT_ALGORITHMS)
    algorithms = [
        create_algorithm_state(key, title, values, descending, gap_sequence=gap_sequence)
        for key, title in ALGORITHMS
        if key in selected
    ]
    return {
        "values": values,
        "descending": descending,
        "gap_sequence": gap_sequence,
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
        "gap_sequence": state["gap_sequence"],
        "selected_algorithms": tuple(state["selected_algorithms"]),
        "algorithms": [copy_sort_item(item) for item in state["algorithms"]],
    }


def build_comparison_trace(state):
    probe = copy_comparison_state(state)
    while not all_sorts_complete(probe):
        step_all_sorts(probe)
        yield copy_comparison_state(probe)


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


def render_result_symbol(item):
    if not item["state"]["sorting_complete"]:
        return ""
    return '<span class="comparison-result-symbol" role="img" aria-label="Ordenado" title="Ordenado">✓</span>'


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
    result = render_result_symbol(item)
    html = f"""
    <div class="comparison-row">
      <div class="comparison-name">{item["title"]}</div>
      <div class="comparison-steps">{item["steps"]}</div>
      <div class="comparison-array-wrap">
        <div class="comparison-bars-result" style="--comparison-count:{len(values)};">
          <div class="comparison-bars">{bars}</div>
          <div class="comparison-result" aria-live="polite">{result}</div>
        </div>
        {indexes}
      </div>
    </div>
    """
    if item["state"]["sorting_complete"]:
        item["html_cache"][cache_key] = html
    return html


def comparison_row_key(item, show_indexes=False):
    sort_state = item["state"]
    return (
        item["key"],
        item["title"],
        item["steps"],
        show_indexes,
        sort_state.get("sorting_complete"),
        tuple(sort_state["arr"]),
        tuple(sort_state["roles"]),
    )


def render_cached_comparison_row(item, show_indexes=False):
    key = comparison_row_key(item, show_indexes)
    cached = _ROW_HTML_CACHE.get(key)
    if cached is not None:
        return cached

    html = render_bars(item, show_indexes=show_indexes)
    if len(_ROW_HTML_CACHE) >= ROW_HTML_CACHE_LIMIT:
        _ROW_HTML_CACHE.clear()
    _ROW_HTML_CACHE[key] = html
    return html


def render_comparison_styles():
    return f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400;700&display=swap');
      .comparison-app {{
        width: 100%;
        box-sizing: border-box;
        font-family: '{FONT_FAMILY}', serif;
        color: #f7f7f7;
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
        grid-template-columns: minmax(90px, 132px) 58px minmax(0, 1fr);
        gap: 8px;
        width: 100%;
        background: #000000;
        font-family: '{FONT_FAMILY}', serif;
        color: #f7f7f7;
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
        font-size: 21px;
        line-height: 1.2;
        color: #f7f7f7;
        text-align: center;
        font-weight: 700;
      }}
      .comparison-steps {{
        font-size: 19px;
        color: #f7f7f7;
        text-align: center;
        white-space: nowrap;
      }}
      .comparison-array-wrap {{
        min-width: 0;
        overflow-x: hidden;
        background: #000000;
        padding: 6px 0 3px;
        contain: layout paint;
      }}
      .comparison-bars-result {{
        display: flex;
        align-items: flex-start;
        justify-content: center;
        gap: 4px;
        width: 100%;
      }}
      .comparison-bars {{
        display: flex;
        align-items: flex-end;
        justify-content: center;
        gap: clamp(1px, 0.35vw, 3px);
        min-height: 210px;
        width: min(calc(100% - 36px), calc(var(--comparison-count) * 37px));
        contain: layout paint;
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
        color: #f7f7f7;
        font-size: 14px;
        line-height: 16px;
        height: 18px;
        margin-bottom: 2px;
        overflow: hidden;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.92);
      }}
      .comparison-bar {{
        width: 100%;
        border: none;
        border-radius: 0;
        outline: 1px solid rgba(255, 255, 255, 0.2);
        outline-offset: -1px;
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
        color: #f7f7f7;
        font-size: 14px;
        line-height: 16px;
        overflow: hidden;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.92);
      }}
      .comparison-result {{
        width: 32px;
        min-width: 32px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 81px;
      }}
      .comparison-result-symbol {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 28px;
        height: 28px;
        font-size: 30px;
        line-height: 1;
        font-weight: 700;
        color: #7bdc80;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.95);
      }}
      @media (max-width: 760px) {{
        .comparison-header {{
          display: none;
        }}
        .comparison-row {{
          grid-template-columns: 1fr;
          gap: 6px;
        }}
        .comparison-name {{
          text-align: left;
        }}
        .comparison-steps {{
          font-size: 18px;
        }}
        .comparison-bars {{
          width: min(calc(100% - 34px), calc(var(--comparison-count) * 28px));
        }}
        .comparison-bar-value,
        .comparison-index {{
          font-size: 12px;
        }}
      }}
      @media (prefers-reduced-motion: reduce) {{
        .comparison-bar,
        .comparison-result-symbol {{
          transition: none;
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
        render_cached_comparison_row(item, show_indexes=index == 0)
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

    size_input = bounded_int_control(
        value=DEFAULT_BAR_SIZE,
        min_value=2,
        max_value=MAX_SIZE,
        step=1,
        description="Tamaño",
        width="180px",
        description_style={},
    )
    order_dropdown = dropdown_control(
        options=ORDER_OPTIONS,
        value=False,
        description="Orden",
        width="210px",
        description_style={},
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
            margin="0",
            overflow="visible",
        ),
    )
    auto_button = button_control(description="Ordenar", button_style="success", width="150px")
    finish_button = button_control(description="Finalizar", button_style="info", width="150px", disabled=True)
    reset_button = button_control(description="Generar nuevo arreglo", button_style="warning", width="190px")
    size_group = compact_labeled_control("Tamaño", size_input)
    order_group = compact_labeled_control("Orden", order_dropdown)
    primary_controls = widgets.VBox(
        [size_group, order_group],
        layout=widgets.Layout(width="100%", gap="12px"),
    )
    style_output = widgets.HTML(value=render_comparison_styles(), layout=widgets.Layout(width="100%"))
    body_output = widgets.HTML(layout=widgets.Layout(width="100%", margin="0", padding="0"))
    html_output = widgets.VBox(
        [style_output, body_output],
        layout=widgets.Layout(width="100%"),
    )
    control_state = {"updating": False}
    execution_state = {"running": False, "finish_requested": False, "run_id": 0}

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
            styles = render_comparison_styles()
            if style_output.value != styles:
                style_output.value = styles
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

    def schedule_task(coro):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(coro)
            return None
        return loop.create_task(coro)

    def finish_all_sorts():
        nonlocal state
        final_state = None
        for snapshot in build_comparison_trace(state):
            final_state = snapshot
        if final_state is not None:
            state = final_state

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

    async def run_auto_async(run_id):
        nonlocal state
        set_running_buttons()
        for snapshot in build_comparison_trace(state):
            if execution_state["run_id"] != run_id:
                return
            if execution_state["finish_requested"]:
                finish_all_sorts()
                break
            state = snapshot
            redraw()
            await asyncio.sleep(0.08)
        if execution_state["run_id"] == run_id:
            redraw()
            set_idle_buttons()

    def run_auto_sync(run_id):
        nonlocal state
        set_running_buttons()
        for snapshot in build_comparison_trace(state):
            if execution_state["run_id"] != run_id:
                return
            if execution_state["finish_requested"]:
                finish_all_sorts()
                break
            state = snapshot
            redraw()
            colab_pause()
        if execution_state["run_id"] == run_id:
            redraw()
            set_idle_buttons()

    def run_auto(*_args):
        if execution_state["running"]:
            return
        execution_state["run_id"] += 1
        run_id = execution_state["run_id"]
        if colab_output is not None:
            run_auto_sync(run_id)
            return
        schedule_task(run_auto_async(run_id))

    def finish_comparison(*_args):
        nonlocal state
        if all_sorts_complete(state):
            return
        execution_state["run_id"] += 1
        execution_state["finish_requested"] = True
        finish_all_sorts()
        redraw()
        set_idle_buttons()

    auto_button.on_click(run_auto)
    finish_button.on_click(finish_comparison)
    reset_button.on_click(generate_new)
    size_input.observe(lambda change: reset_comparison() if change["name"] == "value" else None, names="value")
    order_dropdown.observe(lambda change: reset_comparison() if change["name"] == "value" else None, names="value")
    for checkbox in algorithm_checks.values():
        checkbox.observe(lambda change: reset_comparison() if change["name"] == "value" else None, names="value")

    layout = widgets.VBox(
        [
            widgets.HBox([primary_controls, algorithms_group], layout=widgets.Layout(width="100%", gap="18px", align_items="flex-start")),
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
