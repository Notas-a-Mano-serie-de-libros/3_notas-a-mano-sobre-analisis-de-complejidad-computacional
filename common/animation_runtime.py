from __future__ import annotations

import time


def set_disabled(controls, disabled):
    for control in controls:
        control.disabled = disabled


def pause(seconds, colab_output=None):
    if colab_output is not None:
        colab_output.eval_js(f"new Promise(resolve => setTimeout(resolve, {int(seconds * 1000)}))")
        return
    time.sleep(seconds)


class OutputCache:
    def __init__(self):
        self.formula = object()
        self.html = object()

    def update_formula(self, widget, formula):
        if formula == self.formula:
            return False
        if hasattr(widget, "clear_output"):
            from IPython.display import Math, display

            with widget:
                widget.clear_output(wait=True)
                if formula:
                    display(Math(formula))
        else:
            widget.value = f"$${formula}$$" if formula else ""
        self.formula = formula
        return True

    def update_html(self, widget, html):
        if html == self.html:
            return False
        widget.value = html
        self.html = html
        return True


__all__ = [
    "OutputCache",
    "pause",
    "set_disabled",
]
