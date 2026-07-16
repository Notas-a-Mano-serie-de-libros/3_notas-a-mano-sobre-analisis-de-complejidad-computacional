from sort_common import ROLE_STYLES, create_state as create_sort_state, render_state_html, run_sort_app, step_sort


BOOK_ARRAY = [170, 45, 75, 90, 802, 24, 2, 66]


def create_state(size=None, descending=False, values=None, view="barras", radix_max=999, radix_data_type="numero", radix_number_mode="positive", radix_base=10):
    return create_sort_state(
        "radix",
        size=size,
        descending=descending,
        values=values,
        view=view,
        radix_max=radix_max,
        radix_data_type=radix_data_type,
        radix_number_mode=radix_number_mode,
        radix_base=radix_base,
    )


def step_radix_sort(state):
    step_sort(state)


def run_app():
    run_sort_app("radix", BOOK_ARRAY, has_radix_max=True)


__all__ = ["BOOK_ARRAY", "ROLE_STYLES", "create_state", "step_radix_sort", "render_state_html", "run_app"]
