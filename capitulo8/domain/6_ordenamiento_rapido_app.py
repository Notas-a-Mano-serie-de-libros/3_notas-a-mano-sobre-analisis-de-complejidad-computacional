from sort_common import ROLE_STYLES, create_state as create_sort_state, render_state_html, run_sort_app, step_sort
from variant_comparison import (
    create_comparison_state as create_variant_comparison_state,
    render_html as render_variant_comparison_html,
    run_comparison_app as run_variant_comparison_app,
    step_all as step_all_variants,
)


BOOK_ARRAY = [10, 7, 8, 9, 1, 5]
PARTITION_VARIANTS = (("hoare", "Hoare"), ("lomuto", "Lomuto"))


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


__all__ = [
    "BOOK_ARRAY",
    "PARTITION_VARIANTS",
    "ROLE_STYLES",
    "create_comparison_state",
    "create_state",
    "render_comparison_html",
    "render_state_html",
    "run_app",
    "run_comparison_app",
    "step_all_variants",
    "step_quick_sort",
]
