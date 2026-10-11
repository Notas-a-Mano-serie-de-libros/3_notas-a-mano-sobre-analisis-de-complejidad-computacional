from __future__ import annotations


def apply_plot_style(matplotlib_module, dpi=500):
    matplotlib_module.rcParams.update({
        "figure.dpi": dpi,
        "savefig.dpi": dpi,
    })


__all__ = ["apply_plot_style"]
