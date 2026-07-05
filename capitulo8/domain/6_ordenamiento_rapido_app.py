from sort_common import ROLE_STYLES, create_state as create_sort_state, render_state_html, run_sort_app, step_sort


BOOK_ARRAY = [10, 7, 8, 9, 1, 5]


def create_state(size=None, descending=False, values=None, view="barras", pivot_strategy="end"):
    return create_sort_state("rapido", size=size, descending=descending, values=values, view=view, pivot_strategy=pivot_strategy)


def step_quick_sort(state):
    step_sort(state)


def run_app():
    run_sort_app("rapido", BOOK_ARRAY, has_pivot=True, has_tree=True)


__all__ = ["BOOK_ARRAY", "ROLE_STYLES", "create_state", "step_quick_sort", "render_state_html", "run_app"]
