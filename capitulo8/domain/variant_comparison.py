from __future__ import annotations

import asyncio
from html import escape

from IPython.display import display
import ipywidgets as widgets

from common.widget_controls import bounded_int_control, button_control, compact_labeled_control, dropdown_control
from sort_common import (
    build_sort_panel,
    colab_pause,
    copy_sort_state,
    generate_values,
    normalized_bar_height,
    render_multi_sort_legend,
    sort_action_button_row,
    sort_controls_grid,
    step_sort,
)
from sort_config import DEFAULT_BAR_SIZE, FONT_FAMILY, MAX_SIZE, ORDER_OPTIONS, ROLE_STYLES, SORT_THEME_CSS

try:
    from google.colab import output as colab_output
except ImportError:
    colab_output = None


def create_comparison_state(variants, state_factory, size=DEFAULT_BAR_SIZE, values=None, descending=False):
    values = list(values) if values is not None else generate_values(size)
    return {
        "values": values,
        "descending": descending,
        "algorithms": [
            {
                "key": key,
                "title": title,
                "state": state_factory(key, values, descending),
                "steps": 0,
            }
            for key, title in variants
        ],
    }


def step_all(state):
    for item in state["algorithms"]:
        if not item["state"]["sorting_complete"]:
            step_sort(item["state"])
            item["steps"] += 1


def complete(state):
    return all(item["state"]["sorting_complete"] for item in state["algorithms"])


def copy_state(state):
    return {
        **state,
        "values": list(state["values"]),
        "algorithms": [
            {**item, "state": copy_sort_state(item["state"])}
            for item in state["algorithms"]
        ],
    }


def build_trace(state):
    probe = copy_state(state)
    while not complete(probe):
        step_all(probe)
        yield copy_state(probe)


def render_bar(value, role, maximum):
    fill, _border, text = ROLE_STYLES[role]
    height = normalized_bar_height(value, maximum)
    return f"""
    <div class="variant-bar-wrap">
      <div class="variant-bar-value">{escape(str(value))}</div>
      <div class="variant-bar variant-bar-role-{role}" style="height:{height}px;background:{fill};color:{text};"></div>
    </div>
    """


def render_result_symbol(item):
    if not item["state"]["sorting_complete"]:
        return ""
    return '<span class="variant-result-symbol" role="img" aria-label="Ordenado" title="Ordenado">✓</span>'


def render_html(state):
    rows = []
    for item in state["algorithms"]:
        sort_state = item["state"]
        values = sort_state["arr"]
        reference_values = sort_state.get("initial_values", values)
        maximum = max(reference_values) if reference_values else 1
        bars = "".join(render_bar(value, sort_state["roles"][index], maximum) for index, value in enumerate(values))
        indexes = '<div class="variant-indexes">' + "".join(
            f'<span>{index}</span>' for index in range(len(values))
        ) + "</div>"
        result = render_result_symbol(item)
        rows.append(f"""
        <div class="variant-row">
          <div class="variant-name">{item["title"]}</div>
          <div class="variant-steps">{item["steps"]}</div>
          <div class="variant-array">
            <div class="variant-bars-result" style="--variant-count:{len(values)};">
              <div class="variant-bars">{bars}</div>
              <div class="variant-result" aria-live="polite">{result}</div>
            </div>
            {indexes}
          </div>
        </div>
        """)
    legend = render_multi_sort_legend(item["key"] for item in state["algorithms"])
    return f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Scheherazade+New:wght@400;700&display=swap');
{SORT_THEME_CSS}
      .variant-app {{ width:100%;background:#ffffff;color:#111827;border:0;border-radius:0;padding:0 14px 14px;box-sizing:border-box;font-family:'{FONT_FAMILY}',serif;overflow-x:hidden;contain:layout paint; }}
      .variant-header,.variant-row {{ display:grid;grid-template-columns:minmax(90px,132px) 58px minmax(0,1fr);gap:8px;align-items:center; }}
      .variant-row {{ min-height:245px; }}
      .variant-header {{ font-weight:700;font-size:22px;text-align:center; }}
      .variant-name {{ font-weight:700;font-size:21px;text-align:center;line-height:1.2; }}
      .variant-steps {{ font-size:19px;text-align:center; }}
      .variant-array {{ min-width:0;overflow-x:hidden;padding:6px 0 3px;contain:layout paint; }}
      .variant-bars-result {{ display:flex;align-items:flex-start;justify-content:center;gap:4px;width:100%; }}
      .variant-bars {{ min-height:210px;display:flex;align-items:flex-end;justify-content:center;gap:0;width:auto;min-width:0;flex:1 1 auto;contain:layout paint; }}
      .variant-bar-wrap {{ flex:1 1 0;min-width:8px;max-width:34px;text-align:center; }}
      .variant-bar-value {{ height:18px;line-height:16px;font-size:14px;margin-bottom:2px;overflow:hidden;color:#111827;font-family:'{FONT_FAMILY}',serif;text-shadow:none;-webkit-font-smoothing:antialiased; }}
      .variant-bar {{ width:100%;box-sizing:border-box;border:1px solid var(--sort-border);border-radius:0;outline:none;box-shadow:none;position:relative;transition:transform 100ms ease,opacity 80ms ease; }}
      .variant-bar-wrap + .variant-bar-wrap {{ margin-left:-1px; }}
      .variant-bar-wrap {{ border-bottom:1px solid var(--sort-border); }}
      .variant-bar-role-current,.variant-bar-role-pivot {{ border-color:var(--sort-border);box-shadow:none; }}
      .variant-bar-role-sorted::after {{ content:"✓";position:absolute;top:2px;right:2px;color:#2e7d32;font:700 10px/1 sans-serif; }}
      .variant-bar-role-excluded {{ opacity:var(--sort-muted-opacity); }}
      .variant-indexes {{ display:flex;justify-content:center;gap:0;padding-top:4px;width:calc(100% - 36px);margin-right:36px; }}
      .variant-indexes span {{ flex:1 1 0;min-width:8px;max-width:34px;text-align:center;font-size:14px;color:#111827;text-shadow:none;-webkit-font-smoothing:antialiased; }}
      .variant-result {{ width:32px;min-width:32px;height:48px;display:flex;align-items:center;justify-content:center;margin-top:81px; }}
      .variant-result-symbol {{ display:inline-flex;align-items:center;justify-content:center;min-width:28px;height:28px;font-size:30px;line-height:1;font-weight:700;color:#7bdc80;text-shadow:0 1px 2px rgba(0,0,0,.95); }}
      @media(max-width:760px) {{
        .variant-header {{ display:none; }}
        .variant-row {{ grid-template-columns:1fr;gap:6px; }}
        .variant-name {{ text-align:left; }}
        .variant-bars {{ width:min(calc(100% - 34px), calc(var(--variant-count) * 28px)); }}
        .variant-bar-value,
        .variant-indexes span {{ font-size:12px; }}
      }}
      @media(prefers-reduced-motion:reduce) {{
        .variant-bar,
        .variant-result-symbol {{ transition:none; }}
      }}
    </style>
    <div class="variant-app">
      {legend}
      <div class="variant-header"><div>Algoritmo</div><div>Pasos</div><div>Arreglo</div></div>
      {''.join(rows)}
    </div>
    """


def run_comparison_app(variants, state_factory):
    if colab_output is not None:
        colab_output.enable_custom_widget_manager()

    size = bounded_int_control(value=DEFAULT_BAR_SIZE, min_value=2, max_value=MAX_SIZE, step=1, description="Tamaño", width="180px", description_style={})
    order = dropdown_control(options=ORDER_OPTIONS, value=False, description="Orden", width="210px", description_style={})
    size_group = compact_labeled_control("Tamaño", size)
    order_group = compact_labeled_control("Orden", order)
    auto = button_control(description="Ordenar", button_style="success", width="150px")
    finish = button_control(description="Finalizar", button_style="info", width="150px", disabled=True)
    reset = button_control(description="Generar nuevo arreglo", button_style="warning", width="190px")
    output = widgets.HTML(layout=widgets.Layout(width="100%"))
    execution = {"running": False, "run_id": 0}

    def new_state(values=None):
        return create_comparison_state(
            variants,
            state_factory,
            size=len(values) if values is not None else size.value,
            values=values,
            descending=order.value,
        )

    state = new_state()

    def redraw():
        output.value = render_html(state)

    def idle():
        execution["running"] = False
        auto.disabled = False
        reset.disabled = False
        finish.disabled = True

    def running():
        execution["running"] = True
        auto.disabled = True
        reset.disabled = True
        finish.disabled = False

    def finish_all():
        nonlocal state
        final = None
        for final in build_trace(state):
            pass
        if final is not None:
            state = final

    async def auto_async(run_id):
        nonlocal state
        running()
        for snapshot in build_trace(state):
            if execution["run_id"] != run_id:
                return
            state = snapshot
            redraw()
            await asyncio.sleep(0.08)
        idle()

    def auto_sync(run_id):
        nonlocal state
        running()
        for snapshot in build_trace(state):
            if execution["run_id"] != run_id:
                return
            state = snapshot
            redraw()
            colab_pause()
        idle()

    def start(*_args):
        if execution["running"] or complete(state):
            return
        execution["run_id"] += 1
        run_id = execution["run_id"]
        if colab_output is not None:
            auto_sync(run_id)
            return
        try:
            asyncio.get_running_loop().create_task(auto_async(run_id))
        except RuntimeError:
            asyncio.run(auto_async(run_id))

    def finish_now(*_args):
        execution["run_id"] += 1
        finish_all()
        redraw()
        idle()

    def regenerate(*_args):
        nonlocal state
        execution["run_id"] += 1
        state = new_state(generate_values(size.value))
        redraw()
        idle()

    def rebuild(change=None):
        nonlocal state
        if change is not None and change["name"] != "value":
            return
        execution["run_id"] += 1
        state = new_state()
        redraw()
        idle()

    auto.on_click(start)
    finish.on_click(finish_now)
    reset.on_click(regenerate)
    size.observe(rebuild, names="value")
    order.observe(rebuild, names="value")
    parameters = widgets.VBox(
        [
            sort_controls_grid([size_group, order_group]),
            sort_action_button_row([auto, finish, reset]),
        ],
        layout=widgets.Layout(width="100%", gap="0"),
    )
    display(build_sort_panel(parameters, output, title="Comparación de variantes de ordenamiento:"))
    redraw()


__all__ = [
    "build_trace",
    "complete",
    "create_comparison_state",
    "render_html",
    "run_comparison_app",
    "step_all",
]
