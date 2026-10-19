from __future__ import annotations

import re
import time
from html import escape

import ipywidgets as widgets


def set_disabled(controls, disabled):
    for control in controls:
        control.disabled = disabled


def pause(seconds, colab_output=None):
    if colab_output is not None:
        colab_output.eval_js(f"new Promise(resolve => setTimeout(resolve, {int(seconds * 1000)}))")
        return
    time.sleep(seconds)


class FormulaOutput(widgets.VBox):
    """Render MathJax in one persistent iframe and update it without blank frames."""

    def __init__(self, *, layout=None):
        self._frame = widgets.HTML(
            value=formula_host_html(),
            layout=widgets.Layout(width="100%", height="100%", margin="0"),
        )
        self._signal = widgets.HTML(
            value='<span class="formula-mathjax-signal" data-formula=""></span>',
            layout=widgets.Layout(display="none"),
        )
        options = {"children": (self._frame, self._signal)}
        if layout is not None:
            options["layout"] = layout
        super().__init__(**options)

    def set_formula(self, formula, height):
        height = max(0, int(height))
        self.layout.min_height = f"{height}px"
        self._frame.layout.height = f"{height}px"
        self._signal.value = (
            '<span class="formula-mathjax-signal" '
            f'data-formula="{escape(formula or "", quote=True)}"></span>'
        )


class OutputCache:
    def __init__(self):
        self.formula = object()
        self.html = object()
        self.formula_html = {}
        self.current_formula_html = ""
        self.max_formula_height = 0

    def render_formula_iframe(self, formula, height, hidden=False):
        key = (formula, height, hidden)
        if key in self.formula_html:
            return self.formula_html[key]

        srcdoc = mathjax_srcdoc(formula)
        visibility = "visibility:hidden;" if hidden else ""
        position = "position:absolute;top:0;left:0;" if hidden else ""
        html = (
            '<iframe class="formula-mathjax-frame" '
            f'srcdoc="{escape(srcdoc, quote=True)}" '
            f'style="display:block;width:100%;border:0;overflow:hidden;{position}'
            f'height:{height}px;background:transparent;{visibility}" '
            'scrolling="no"></iframe>'
        )
        self.formula_html[key] = html
        return html

    def render_formula_html(self, formula, height):
        new_html = self.render_formula_iframe(formula, height, hidden=bool(self.current_formula_html))
        if not self.current_formula_html:
            self.current_formula_html = new_html
            return new_html

        html = (
            '<div class="formula-frame-stack" '
            f'style="position:relative;width:100%;height:{height}px;overflow:hidden;">'
            f'{self.current_formula_html}{new_html}</div>'
        )
        self.current_formula_html = self.render_formula_iframe(formula, height, hidden=False)
        return html

    def update_formula(self, widget, formula, reserved_height=None):
        if formula == self.formula:
            return False
        height = formula_iframe_height(formula) if formula else 0
        if reserved_height is None:
            self.max_formula_height = max(self.max_formula_height, height)
        else:
            self.max_formula_height = reserved_height
        if hasattr(widget, "layout"):
            widget.layout.min_height = f"{self.max_formula_height}px"
        if hasattr(widget, "set_formula"):
            widget.set_formula(formula, self.max_formula_height)
        else:
            widget.value = self.render_formula_html(formula, self.max_formula_height) if formula else ""
        self.formula = formula
        return True

    def update_html(self, widget, html):
        if html == self.html:
            return False
        widget.value = html
        self.html = html
        return True

    def update_outputs(self, formula_widget, html_widget, formula, html, reserved_height=None):
        formula_changed = self.update_formula(formula_widget, formula, reserved_height)
        html_changed = self.update_html(html_widget, html)
        return formula_changed or html_changed


__all__ = [
    "FormulaOutput",
    "OutputCache",
    "formula_iframe_height",
    "mathjax_srcdoc",
    "pause",
    "set_disabled",
]


def formula_host_html():
    srcdoc = mathjax_host_srcdoc()
    return (
        '<iframe class="formula-mathjax-frame formula-mathjax-host" '
        f'srcdoc="{escape(srcdoc, quote=True)}" '
        'style="display:block;width:100%;height:100%;border:0;overflow:hidden;'
        'background:transparent" scrolling="no"></iframe>'
    )


def mathjax_host_srcdoc():
    return """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
html,body{margin:0;padding:0;background:#ffffff;overflow:hidden;color:#111111;height:100%;}
body{color:#111;font-size:16px;line-height:1.2;}
#formula{display:flex;align-items:flex-end;justify-content:flex-start;min-height:100%;text-align:left;}
mjx-container[jax="SVG"]{font-size:100% !important;margin:0 !important;}
mjx-container[jax="SVG"][display="true"]{text-align:left !important;}
</style>
<script>
window.MathJax = {
  tex: {
    inlineMath: [['\\\\(', '\\\\)']],
    displayMath: [['\\\\[', '\\\\]']],
    processEscapes: true
  },
  svg: { fontCache: 'none' },
  startup: { typeset: false }
};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js" integrity="sha256-1CldwzdEg2k1wTmf7s5RWVd7NMXI/7nxxjJM2C4DqII=" crossorigin="anonymous"></script>
</head>
<body>
<div id="formula"></div>
<script>
window.addEventListener('load', function () {
  var renderedFormula = '';
  var requestedFormula = '';
  var requestId = 0;
  var observer = null;

  function signalRoot() {
    try {
      var node = window.frameElement;
      while (node && node.parentElement) {
        node = node.parentElement;
        if (node.querySelector && node.querySelector('.formula-mathjax-signal')) return node;
      }
    } catch (_error) {}
    return null;
  }

  function readFormula(root) {
    var signal = root && root.querySelector('.formula-mathjax-signal');
    return signal ? (signal.getAttribute('data-formula') || '') : '';
  }

  function render(formula) {
    if (formula === renderedFormula || formula === requestedFormula) return;
    if (!formula) {
      requestId += 1;
      document.getElementById('formula').replaceChildren();
      renderedFormula = '';
      requestedFormula = '';
      return;
    }
    requestedFormula = formula;
    var currentRequest = ++requestId;
    MathJax.tex2svgPromise(formula, {display: true}).then(function (node) {
      if (currentRequest !== requestId) return;
      document.getElementById('formula').replaceChildren(node);
      renderedFormula = formula;
      requestedFormula = '';
    }).catch(function () {
      if (currentRequest === requestId) requestedFormula = '';
    });
  }

  function connect() {
    var root = signalRoot();
    if (!root || !window.MathJax || !MathJax.tex2svgPromise) {
      window.setTimeout(connect, 30);
      return;
    }
    render(readFormula(root));
    observer = new MutationObserver(function () { render(readFormula(root)); });
    observer.observe(root, {subtree: true, childList: true, attributes: true});
  }

  connect();
});
</script>
</body>
</html>"""


def formula_iframe_height(formula):
    row_breaks = re.findall(r"\\\\(?:\[(\d+(?:\.\d+)?)pt\])?", formula)
    rows = max(1, len(row_breaks) + 1)
    explicit_spacing = sum(float(value) * 1.34 for value in row_breaks if value)
    environments = (
        formula.count(r"\begin{array}") +
        formula.count(r"\begin{aligned}") +
        formula.count(r"\begin{gathered}")
    )
    tall_terms = formula.count(r"\frac") + formula.count(r"\left\lfloor") + formula.count(r"\right\rfloor")
    tall_rows = min(rows, max(0, tall_terms // 2))
    fraction_count = formula.count(r"\frac")
    height = 32 + rows * 25 + explicit_spacing + environments * 8 + tall_rows * 20 + fraction_count * 5
    return max(42, min(520, int(round(height))))


def mathjax_srcdoc(formula):
    tex = escape(formula.strip())
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<style>
html,body{{margin:0;padding:0;background:#ffffff;overflow:hidden;color:#111111;}}
body{{color:#111;font-size:16px;line-height:1.2;}}
#formula{{display:flex;align-items:flex-end;justify-content:flex-start;min-height:100%;visibility:hidden;text-align:left;}}
body.math-ready #formula{{visibility:visible;}}
mjx-container[jax="SVG"]{{font-size:100% !important;margin:0 !important;}}
mjx-container[jax="SVG"][display="true"]{{text-align:left !important;}}
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
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js" integrity="sha256-1CldwzdEg2k1wTmf7s5RWVd7NMXI/7nxxjJM2C4DqII=" crossorigin="anonymous"></script>
</head>
<body>
<div id="formula" style="visibility:hidden">\\[{tex}\\]</div>
<script>
window.addEventListener('load', function () {{
  function reveal() {{
    var el = document.getElementById('formula');
    if (el) {{ el.style.visibility = 'visible'; }}
    if (window.frameElement) {{
      window.frameElement.style.visibility = 'visible';
      var previous = window.frameElement.previousElementSibling;
      if (previous && previous.classList && previous.classList.contains('formula-mathjax-frame')) {{
        previous.style.display = 'none';
      }}
    }}
    document.body.classList.add('math-ready');
  }}
  if (window.MathJax && MathJax.typesetPromise) {{
    MathJax.typesetPromise([document.getElementById('formula')]).then(function () {{
      reveal();
    }}).catch(function () {{
      reveal();
    }});
  }} else {{
    setTimeout(reveal, 200);
  }}
}});
</script>
</body>
</html>"""
