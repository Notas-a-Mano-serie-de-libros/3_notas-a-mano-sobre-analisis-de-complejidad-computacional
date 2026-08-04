from sort_common import ROLE_STYLES, create_state as create_sort_state, render_state_html, run_sort_app, step_sort


BOOK_ARRAY = [38, 27, 43, 3, 9, 82, 10]


def create_state(size=None, descending=False, values=None, view="barras"):
    return create_sort_state("mezcla", size=size, descending=descending, values=values, view=view)


def step_merge_sort(state):
    step_sort(state)


def run_app():
    run_sort_app("mezcla", BOOK_ARRAY, has_tree=True)


__all__ = ["BOOK_ARRAY", "ROLE_STYLES", "create_state", "step_merge_sort", "render_state_html", "run_app"]
