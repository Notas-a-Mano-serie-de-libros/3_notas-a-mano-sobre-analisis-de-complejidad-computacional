from IPython.display import display
import ipywidgets as widgets

from common.widget_controls import bounded_int_control, button_control, compact_labeled_control, dropdown_control
from sort_common import ROLE_STYLES, create_state as create_sort_state, render_state_html, run_sort_app, step_sort
from sort_config import DEFAULT_BAR_SIZE, MAX_SIZE, ORDER_OPTIONS, PARTITION_OPTIONS, PIVOT_OPTIONS
from variant_comparison import (
    build_trace as build_variant_trace,
    complete as variants_complete,
    create_comparison_state as create_variant_comparison_state,
    render_html as render_variant_comparison_html,
    run_comparison_app as run_variant_comparison_app,
    step_all as step_all_variants,
)


BOOK_ARRAY = [10, 7, 8, 9, 1, 5]
PARTITION_VARIANTS = (("hoare", "Hoare"), ("lomuto", "Lomuto"))
PIVOT_VARIANTS = tuple((key, label) for label, key in PIVOT_OPTIONS)


def create_state(size=None, descending=False, values=None, view="barras", pivot_strategy="middle", partition_scheme="hoare"):
    return create_sort_state(
        "rapido",
        size=size,
        descending=descending,
        values=values,
        view=view,
        pivot_strategy=pivot_strategy,
        partition_scheme=partition_scheme,
    )


def step_quick_sort(state):
    step_sort(state)


def run_app():
    run_sort_app("rapido", BOOK_ARRAY, has_pivot=True, has_tree=True, has_partition=True)


def create_comparison_state(size=32, values=None, descending=False):
    def state_factory(scheme, shared_values, shared_descending):
        return create_state(
            size=len(shared_values),
            values=shared_values,
            descending=shared_descending,
            view="barras",
            pivot_strategy="middle",
            partition_scheme=scheme,
        )

    return create_variant_comparison_state(
        PARTITION_VARIANTS,
        state_factory,
        size=size,
        values=values,
        descending=descending,
    )


def render_comparison_html(state):
    return render_variant_comparison_html(state)


def run_comparison_app():
    def state_factory(scheme, values, descending):
        return create_state(
            size=len(values),
            values=values,
            descending=descending,
            view="barras",
            pivot_strategy="middle",
            partition_scheme=scheme,
        )

    run_variant_comparison_app(PARTITION_VARIANTS, state_factory)


def create_pivot_comparison_state(size=32, values=None, descending=False, partition_scheme="hoare"):
    def state_factory(pivot_strategy, shared_values, shared_descending):
        return create_state(
            size=len(shared_values),
            values=shared_values,
            descending=shared_descending,
            view="barras",
            pivot_strategy=pivot_strategy,
            partition_scheme=partition_scheme,
        )

    state = create_variant_comparison_state(
        PIVOT_VARIANTS,
        state_factory,
        size=size,
        values=values,
        descending=descending,
    )
    state["partition_scheme"] = partition_scheme
    return state


def render_pivot_comparison_html(state):
    return render_variant_comparison_html(state)


def run_pivot_comparison_app():
    from sort_common import colab_pause, generate_values

    size = bounded_int_control(value=DEFAULT_BAR_SIZE, min_value=2, max_value=MAX_SIZE, step=1, description="Tamaño", width="180px", description_style={})
    order = dropdown_control(options=ORDER_OPTIONS, value=False, description="Orden", width="210px", description_style={})
    partition = dropdown_control(options=PARTITION_OPTIONS, value="hoare", description="Partición", width="190px", description_style={})
    size_group = compact_labeled_control("Tamaño", size)
    order_group = compact_labeled_control("Orden", order)
    partition_group = compact_labeled_control("Partición", partition)
    auto = button_control(description="Ordenar", button_style="success", width="150px")
    finish = button_control(description="Finalizar", button_style="info", width="150px", disabled=True)
    reset = button_control(description="Generar nuevo arreglo", button_style="warning", width="190px")
    output = widgets.HTML(layout=widgets.Layout(width="100%"))
    execution = {"running": False, "run_id": 0}

    def new_state(values=None):
        return create_pivot_comparison_state(
            size=len(values) if values is not None else size.value,
            values=values,
            descending=order.value,
            partition_scheme=partition.value,
        )

    state = new_state()

    def redraw():
        output.value = render_pivot_comparison_html(state)

    def idle():
        execution["running"] = False
        auto.disabled = variants_complete(state)
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
        for final in build_variant_trace(state):
            pass
        if final is not None:
            state = final

    def run_until_complete(run_id):
        nonlocal state
        running()
        for snapshot in build_variant_trace(state):
            if execution["run_id"] != run_id:
                return
            state = snapshot
            redraw()
            colab_pause()
        idle()

    def start(*_args):
        if execution["running"] or variants_complete(state):
            return
        execution["run_id"] += 1
        run_until_complete(execution["run_id"])

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
    partition.observe(rebuild, names="value")
    display(widgets.VBox([
        widgets.HBox([size_group, order_group, partition_group], layout=widgets.Layout(width="100%", gap="42px")),
        widgets.HBox([auto, finish, reset], layout=widgets.Layout(width="100%", gap="10px", margin="12px 0 0 0")),
        output,
    ], layout=widgets.Layout(width="100%", gap="10px")))
    redraw()


__all__ = [
    "BOOK_ARRAY",
    "PARTITION_VARIANTS",
    "PIVOT_VARIANTS",
    "ROLE_STYLES",
    "create_comparison_state",
    "create_pivot_comparison_state",
    "create_state",
    "render_pivot_comparison_html",
    "render_comparison_html",
    "render_state_html",
    "run_app",
    "run_comparison_app",
    "run_pivot_comparison_app",
    "step_all_variants",
    "step_quick_sort",
]
