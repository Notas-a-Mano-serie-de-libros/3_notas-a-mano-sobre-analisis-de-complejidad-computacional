from sort_common import ROLE_STYLES, create_state as create_sort_state, render_state_html, run_sort_app, step_sort


BOOK_ARRAY = [35, 12, 48, 7, 26, 19, 41, 3, 30, 14]


def create_state(size=None, descending=False, values=None, view="barras", gap_sequence="shell"):
    return create_sort_state("shell", size=size, descending=descending, values=values, view=view, gap_sequence=gap_sequence)


def step_shell_sort(state):
    step_sort(state)


def run_app():
    run_sort_app("shell", BOOK_ARRAY, has_gap_sequence=True)


__all__ = ["BOOK_ARRAY", "ROLE_STYLES", "create_state", "step_shell_sort", "render_state_html", "run_app"]
