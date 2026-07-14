from __future__ import annotations

import asyncio
from html import escape

from IPython.display import display
import ipywidgets as widgets

from common.widget_controls import bounded_int_control, button_control, dropdown_control
from sort_common import colab_pause, copy_sort_state, create_state as create_sort_state, generate_values, render_state_html, run_sort_app, step_sort
from sort_config import DEFAULT_BAR_SIZE, GAP_SEQUENCE_OPTIONS, FONT_FAMILY, MAX_SIZE, ORDER_OPTIONS, ROLE_STYLES

try:
    from google.colab import output as colab_output
except ImportError:
    colab_output = None


BOOK_ARRAY = [35, 12, 48, 7, 26, 19, 41, 3, 30, 14]


def create_state(size=None, descending=False, values=None, view="barras", gap_sequence="shell"):
    return create_sort_state("shell", size=size, descending=descending, values=values, view=view, gap_sequence=gap_sequence)


def step_shell_sort(state):
    step_sort(state)


def run_app():
    run_sort_app("shell", BOOK_ARRAY, has_gap_sequence=True)


SHELL_SEQUENCE_ROWS = (
    ("shell", "Shell"),
    ("hibbard", "Hibbard"),
    ("sedgewick", "Sedgewick"),
    ("pratt", "Pratt"),
)
ROW_HTML_CACHE_LIMIT = 512
_ROW_HTML_CACHE = {}


def create_sequence_item(sequence, title, values, descending):
    return {
        "key": sequence,
        "title": title,
        "state": create_sort_state(
            "shell",
            size=len(values),
            descending=descending,
            values=values,
            view="barras",
            gap_sequence=sequence,
        ),
        "steps": 0,
        "html_cache": {},
    }


def create_gap_comparison_state(size=DEFAULT_BAR_SIZE, values=None, descending=False):
    values = list(values) if values is not None else generate_values(size)
    return {
        "values": values,
        "descending": descending,
        "algorithms": [
            create_sequence_item(sequence, title, values, descending)
            for sequence, title in SHELL_SEQUENCE_ROWS
        ],
    }


def step_all_sequences(state):
    for item in state["algorithms"]:
        sort_state = item["state"]
        if not sort_state["sorting_complete"]:
            step_sort(sort_state)
            item["steps"] += 1


def all_sequences_complete(state):
    return all(item["state"]["sorting_complete"] for item in state["algorithms"])


def copy_sequence_item(item):
    return {
        **item,
        "state": copy_sort_state(item["state"]),
        "html_cache": dict(item.get("html_cache", {})),
    }


def copy_gap_comparison_state(state):
    return {
        **state,
        "values": list(state["values"]),
        "algorithms": [copy_sequence_item(item) for item in state["algorithms"]],
    }


def build_gap_comparison_trace(state):
    probe = copy_gap_comparison_state(state)
    while not all_sequences_complete(probe):
        step_all_sequences(probe)
        yield copy_gap_comparison_state(probe)


def render_index_row(values):
    indexes = "".join(f'<div class="shell-comparison-index">{index}</div>' for index, _value in enumerate(values))
    return f'<div class="shell-comparison-index-row">{indexes}</div>'


def render_bar(value, role, max_value):
    fill, _border, text = ROLE_STYLES[role]
    height = 18 + (value / max_value) * 170 if max_value else 18
    return f"""
    <div class="shell-comparison-bar-wrap">
      <div class="shell-comparison-bar-area">
        <div class="shell-comparison-bar-stack">
          <div class="shell-comparison-bar-value">{escape(str(value))}</div>
          <div class="shell-comparison-bar" style="height:{height}px; background:{fill}; color:{text};"></div>
        </div>
      </div>
    </div>
    """


def render_result_symbol(item):
    if not item["state"]["sorting_complete"]:
        return ""
    return '<span class="shell-comparison-result-symbol" aria-label="Ordenado" title="Ordenado">✓</span>'


def render_sequence_bars(item, show_indexes=False):
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
    <div class="shell-comparison-row">
      <div class="shell-comparison-name">{item["title"]}</div>
      <div class="shell-comparison-steps">{item["steps"]}</div>
      <div class="shell-comparison-array-wrap">
        <div class="shell-comparison-bars-result">
          <div class="shell-comparison-bars">{bars}</div>
          <div class="shell-comparison-result">{result}</div>
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
        item["steps"],
        show_indexes,
        sort_state.get("sorting_complete"),
        tuple(sort_state["arr"]),
        tuple(sort_state["roles"]),
    )


def render_cached_sequence_row(item, show_indexes=False):
    key = comparison_row_key(item, show_indexes)
    cached = _ROW_HTML_CACHE.get(key)
    if cached is not None:
        return cached

    html = render_sequence_bars(item, show_indexes=show_indexes)
    if len(_ROW_HTML_CACHE) >= ROW_HTML_CACHE_LIMIT:
        _ROW_HTML_CACHE.clear()
    _ROW_HTML_CACHE[key] = html
    return html


def render_gap_comparison_styles():
    return f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400;700&display=swap');
      .shell-comparison-app {{
        width: 100%;
        box-sizing: border-box;
        font-family: '{FONT_FAMILY}', serif;
        color: #f7f7f7;
        background: #000000;
        padding: 8px;
      }}
      .shell-comparison-app * {{
        box-sizing: border-box;
      }}
      .shell-comparison-table {{
        display: flex;
        flex-direction: column;
        gap: 0;
        width: 100%;
        background: #000000;
      }}
      .shell-comparison-header,
      .shell-comparison-row {{
        display: grid;
        grid-template-columns: minmax(96px, 128px) 62px minmax(0, 1fr);
        gap: 8px;
        width: 100%;
        background: #000000;
        font-family: '{FONT_FAMILY}', serif;
        color: #f7f7f7;
      }}
      .shell-comparison-header {{
        align-items: end;
        padding-bottom: 0;
      }}
      .shell-comparison-row {{
        align-items: center;
      }}
      .shell-comparison-head-cell,
      .shell-comparison-name {{
        font-size: 22px;
        line-height: 1.2;
        color: #f7f7f7;
        text-align: center;
        font-weight: 700;
      }}
      .shell-comparison-steps {{
        font-size: 20px;
        color: #f7f7f7;
        text-align: center;
        white-space: nowrap;
      }}
      .shell-comparison-array-wrap {{
        min-width: 0;
        overflow-x: hidden;
        background: #000000;
        padding: 8px 0 4px;
      }}
      .shell-comparison-bars-result {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 4px;
        width: 100%;
      }}
      .shell-comparison-bars {{
        display: flex;
        align-items: flex-end;
        justify-content: center;
        gap: clamp(1px, 0.35vw, 3px);
        min-height: 220px;
        width: calc(100% - 36px);
      }}
      .shell-comparison-bar-wrap {{
        width: auto;
        flex: 1 1 0;
        min-width: 8px;
        max-width: 34px;
        text-align: center;
      }}
      .shell-comparison-bar-area {{
        height: 200px;
        display: flex;
        align-items: flex-end;
        justify-content: center;
      }}
      .shell-comparison-bar-stack {{
        width: 100%;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
      }}
      .shell-comparison-bar-value {{
        color: #f7f7f7;
        font-size: 14px;
        line-height: 16px;
        height: 18px;
        margin-bottom: 2px;
        overflow: hidden;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.92);
      }}
      .shell-comparison-bar {{
        width: 100%;
        border: none;
        border-radius: 0;
      }}
      .shell-comparison-index-row {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: clamp(1px, 0.35vw, 3px);
        min-height: 20px;
        padding-top: 4px;
        width: 100%;
      }}
      .shell-comparison-index {{
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
      .shell-comparison-result {{
        width: 32px;
        min-width: 32px;
        height: 48px;
        display: flex;
        align-items: center;
        justify-content: center;
      }}
      .shell-comparison-result-symbol {{
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
        .shell-comparison-header {{
          display: none;
        }}
        .shell-comparison-row {{
          grid-template-columns: 1fr;
          gap: 6px;
        }}
        .shell-comparison-steps {{
          font-size: 18px;
        }}
      }}
      @media (min-width: 761px) {{
        .shell-comparison-name,
        .shell-comparison-steps {{
          white-space: nowrap;
        }}
      }}
    </style>
    """


def render_gap_comparison_header_html():
    return """
    <div class="shell-comparison-header">
      <div class="shell-comparison-head-cell">h</div>
      <div class="shell-comparison-head-cell">Pasos</div>
      <div class="shell-comparison-head-cell">Arreglo</div>
    </div>
    """


def render_gap_comparison_rows_html(state):
    return "".join(
        render_cached_sequence_row(item, show_indexes=index == 0)
        for index, item in enumerate(state["algorithms"])
    )


def render_gap_comparison_body_html(state):
    return f"""
    <div class="shell-comparison-app">
      <div class="shell-comparison-table">
        {render_gap_comparison_header_html()}
        {render_gap_comparison_rows_html(state)}
      </div>
    </div>
    """


def render_gap_comparison_html(state):
    return f"""
    {render_gap_comparison_styles()}
    {render_gap_comparison_body_html(state)}
    """


def run_gap_comparison_app():
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
    auto_button = button_control(description="Ordenar", button_style="success", width="150px")
    finish_button = button_control(description="Finalizar", button_style="info", width="150px", disabled=True)
    reset_button = button_control(description="Generar nuevo arreglo", button_style="warning", width="190px")
    style_output = widgets.HTML(value=render_gap_comparison_styles(), layout=widgets.Layout(width="100%"))
    body_output = widgets.HTML(layout=widgets.Layout(width="100%", margin="0", padding="0"))
    html_output = widgets.VBox([style_output, body_output], layout=widgets.Layout(width="100%"))
    control_state = {"updating": False}
    execution_state = {"running": False, "finish_requested": False, "run_id": 0}

    def build_state(values=None):
        size = len(values) if values is not None else size_input.value
        return create_gap_comparison_state(size=size, values=values, descending=order_dropdown.value)

    state = build_state()

    def redraw(force_static=False):
        if force_static:
            styles = render_gap_comparison_styles()
            if style_output.value != styles:
                style_output.value = styles
        body = render_gap_comparison_body_html(state)
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

    def finish_all_sequences():
        nonlocal state
        final_state = None
        for snapshot in build_gap_comparison_trace(state):
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
        for snapshot in build_gap_comparison_trace(state):
            if execution_state["run_id"] != run_id:
                return
            if execution_state["finish_requested"]:
                finish_all_sequences()
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
        for snapshot in build_gap_comparison_trace(state):
            if execution_state["run_id"] != run_id:
                return
            if execution_state["finish_requested"]:
                finish_all_sequences()
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
        if all_sequences_complete(state):
            return
        execution_state["run_id"] += 1
        execution_state["finish_requested"] = True
        finish_all_sequences()
        redraw()
        set_idle_buttons()

    auto_button.on_click(run_auto)
    finish_button.on_click(finish_comparison)
    reset_button.on_click(generate_new)
    size_input.observe(lambda change: reset_comparison() if change["name"] == "value" else None, names="value")
    order_dropdown.observe(lambda change: reset_comparison() if change["name"] == "value" else None, names="value")

    layout = widgets.VBox(
        [
            widgets.HBox([size_input, order_dropdown], layout=widgets.Layout(width="100%", gap="12px")),
            widgets.HBox([auto_button, finish_button, reset_button], layout=widgets.Layout(width="100%", gap="10px", margin="12px 0 0 0")),
            html_output,
        ],
        layout=widgets.Layout(width="100%", gap="10px"),
    )
    display(layout)
    redraw(force_static=True)


__all__ = [
    "BOOK_ARRAY",
    "ROLE_STYLES",
    "SHELL_SEQUENCE_ROWS",
    "all_sequences_complete",
    "create_gap_comparison_state",
    "create_state",
    "render_gap_comparison_html",
    "render_state_html",
    "run_app",
    "run_gap_comparison_app",
    "step_all_sequences",
    "step_shell_sort",
]
