from sort_common import ROLE_STYLES, create_state as create_sort_state, render_state_html, run_sort_app, step_sort


BOOK_ARRAY = [64, 25, 12, 22, 11]


def create_state(size=None, descending=False, values=None, view="barras"):
    return create_sort_state("seleccion", size=size, descending=descending, values=values, view=view)


def step_selection_sort(state):
    step_sort(state)


def run_app():
    run_sort_app("seleccion", BOOK_ARRAY)


__all__ = ["BOOK_ARRAY", "ROLE_STYLES", "create_state", "step_selection_sort", "render_state_html", "run_app"]
