from __future__ import annotations

import time
from html import escape


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
        self.formula_html = {}

    def render_formula_html(self, formula):
        if formula in self.formula_html:
            return self.formula_html[formula]

        height = formula_iframe_height(formula)
        srcdoc = mathjax_srcdoc(formula)
        html = (
            '<iframe class="formula-mathjax-frame" '
            f'srcdoc="{escape(srcdoc, quote=True)}" '
            'style="display:block;width:100%;border:0;overflow:hidden;'
            f'height:{height}px;background:transparent;" '
            'scrolling="no"></iframe>'
        )
        self.formula_html[formula] = html
        return html

    def update_formula(self, widget, formula):
        if formula == self.formula:
            return False
        widget.value = self.render_formula_html(formula) if formula else ""
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
    "formula_iframe_height",
    "mathjax_srcdoc",
    "pause",
    "set_disabled",
]


def formula_iframe_height(formula):
    rows = max(1, formula.count(r"\\") + 1)
    environments = formula.count(r"\begin{array}") + formula.count(r"\begin{aligned}")
    return max(42, min(320, 34 + rows * 22 + environments * 18))


def mathjax_srcdoc(formula):
    tex = escape(formula.strip())
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
html,body{{margin:0;padding:0;background:transparent;overflow:hidden;}}
body{{color:#111;font-size:16px;line-height:1.2;}}
@media (prefers-color-scheme:dark){{body{{color:#f2f2f2;}}}}
#formula{{display:flex;align-items:center;min-height:100%;}}
mjx-container[jax="SVG"]{{font-size:100% !important;margin:0 !important;}}
</style>
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['\\\\(', '\\\\)']],
    displayMath: [['\\\\[', '\\\\]']],
    processEscapes: true
  }},
  svg: {{ fontCache: 'none' }},
  startup: {{ typeset: false }}
}};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
<div id="formula">\\[{tex}\\]</div>
<script>
window.addEventListener('load', function () {{
  if (window.MathJax && MathJax.typesetPromise) {{
    MathJax.typesetPromise([document.getElementById('formula')]);
  }}
}});
</script>
</body>
</html>"""
