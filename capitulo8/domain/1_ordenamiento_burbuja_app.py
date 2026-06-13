from sort_common import ROLE_STYLES, create_state as create_sort_state, render_state_html, run_sort_app, step_sort


BOOK_ARRAY = [5, 1, 4, 2, 8]


def create_state(size=None, descending=False, values=None, view="barras"):
    return create_sort_state("burbuja", size=size, descending=descending, values=values, view=view)


def step_bubble_sort(state):
    step_sort(state)


def run_app():
    run_sort_app("burbuja", BOOK_ARRAY)


__all__ = ["BOOK_ARRAY", "ROLE_STYLES", "create_state", "step_bubble_sort", "render_state_html", "run_app"]
