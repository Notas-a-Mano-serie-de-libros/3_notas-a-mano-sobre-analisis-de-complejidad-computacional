from sort_common import ROLE_STYLES, create_state as create_sort_state, render_state_html, run_sort_app, step_sort


BOOK_ARRAY = [5, 2, 4, 6, 1, 3]


def create_state(size=None, descending=False, values=None, view="barras"):
    return create_sort_state("insercion", size=size, descending=descending, values=values, view=view)


def step_insertion_sort(state):
    step_sort(state)


def run_app():
    run_sort_app("insercion", BOOK_ARRAY)


__all__ = ["BOOK_ARRAY", "ROLE_STYLES", "create_state", "step_insertion_sort", "render_state_html", "run_app"]
