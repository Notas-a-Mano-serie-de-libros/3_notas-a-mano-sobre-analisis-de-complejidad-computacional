"""Comparación animada y a escala lineal real de familias de crecimiento."""

from __future__ import annotations

import json
import math
import uuid
from html import escape

import ipywidgets as widgets
from IPython.display import Javascript, clear_output, display

from common.widget_controls import (
    action_button_row,
    bounded_int_control,
    button_control,
    collapsible_panel,
    compact_labeled_control,
    dropdown_control,
    shared_ui_styles,
)

MIN_N, MIN_TARGET_N, MAX_N, DEFAULT_N = 0, 1, 1_000, 100
SPEED_OPTIONS = (("1x", 1.0), ("2x", 2.0), ("5x", 5.0), ("10x", 10.0))
BASE_DURATION, LN_10 = 20.0, math.log(10)
PRESETS = (
    ("Personalizada", "custom"),
    ("Crecimiento moderado", "moderate"),
    ("Polinomiales", "polynomial"),
    ("Crecimiento rápido", "fast"),
    ("Todas", "all"),
)
FAMILIES = (
    ("constant", "1", "1", "#607d8b"),
    ("log", "log<sub>2</sub>(<i>n</i>)", "log₂(n)", "#00838f"),
    ("linear", "<i>n</i>", "n", "#2e7d32"),
    ("nlogn", "<i>n</i> &middot; log<sub>2</sub>(<i>n</i>)", "n · log₂(n)", "#558b2f"),
    ("square", "<i>n</i><sup>2</sup>", "n²", "#ef6c00"),
    ("cube", "<i>n</i><sup>3</sup>", "n³", "#d84315"),
    ("exponential", "2<sup><i>n</i></sup>", "2ⁿ", "#ad1457"),
    ("factorial", "<i>n</i>!", "n!", "#6a1b9a"),
)
FAMILY_BY_KEY = {family[0]: family for family in FAMILIES}
PRESET_KEYS = {
    "moderate": ("constant", "log", "linear", "nlogn"),
    "polynomial": ("linear", "square", "cube"),
    "fast": ("square", "cube", "exponential", "factorial"),
    "all": tuple(FAMILY_BY_KEY),
}


def _exact_value(key: str, n: int) -> int | float:
    """Calcula el valor exacto que se muestra para un n entero."""
    n = max(MIN_N, int(n))
    functions = {
        "constant": lambda: 1,
        "log": lambda: math.log2(n) if n > 0 else 0,
        "linear": lambda: n,
        "nlogn": lambda: n * math.log2(n) if n > 0 else 0,
        "square": lambda: n**2,
        "cube": lambda: n**3,
        "exponential": lambda: 2**n,
        "factorial": lambda: math.factorial(n),
    }
    try:
        return functions[key]()
    except KeyError as error:
        raise ValueError(f"Familia desconocida: {key}") from error


def _log_value(key: str, n: float) -> float | None:
    """Devuelve ln(f(n)); None representa el valor cero."""
    n = max(float(n), 0.0)
    if key == "constant":
        return 0.0
    if key in {"log", "nlogn"}:
        if n <= 1:
            return None
        log_n = math.log(n)
        log_2_n = math.log2(n)
        return math.log(log_2_n) + (log_n if key == "nlogn" else 0)
    if key == "linear":
        return math.log(n) if n > 0 else None
    if key == "square":
        return 2 * math.log(n) if n > 0 else None
    if key == "cube":
        return 3 * math.log(n) if n > 0 else None
    if key == "exponential":
        return n * math.log(2)
    if key == "factorial":
        return math.lgamma(n + 1)
    raise ValueError(f"Familia desconocida: {key}")


def _decimal(value: float, digits: int = 2) -> str:
    if abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    rendered = f"{value:.{digits}f}".rstrip("0").rstrip(".")
    return rendered.replace(".", ",")


def _scientific_parts(log_value: float) -> tuple[float, int]:
    exponent = math.floor(log_value / LN_10 + 1e-9)
    coefficient = math.exp(log_value - exponent * LN_10)
    return (1.0, exponent + 1) if coefficient >= 9.995 else (coefficient, exponent)


def _format_exact_value(value: int | float, *, html: bool = True) -> str:
    """Formatea valores sin pérdida de precisión ni artefactos de agrupador confuso."""
    if isinstance(value, (int, float)):
        if abs(value) < 1_000_000:
            if isinstance(value, int) or abs(value - round(value)) < 1e-9:
                return str(int(round(value)))
            rendered = f"{value:.2f}".rstrip("0").rstrip(".")
            return rendered.replace(".", ",")
        digits = str(abs(int(value))) if isinstance(value, int) else None
        if digits:
            exponent = len(digits) - 1
            if len(digits) >= 4:
                coefficient = round(int(digits[:4]) / 1000, 2)
            else:
                coefficient = round(int(digits) / (10**exponent), 2)
        else:
            coefficient, exponent = _scientific_parts(math.log(abs(value)))
            coefficient = round(coefficient, 2)
        if coefficient >= 9.995:
            coefficient, exponent = 1.0, exponent + 1
        coef_str = _decimal(coefficient)
        exponent_text = f"<sup>{exponent}</sup>" if html else f"^{exponent}"
        return f"{coef_str} × 10{exponent_text}"
    return str(value)


def _format_log_axis(log_value: float | None) -> str:
    if log_value is None:
        return "0"
    if log_value < math.log(1_000_000):
        val = math.exp(log_value)
        if abs(val - round(val)) < 1e-9:
            return str(int(round(val)))
        return f"{val:.2f}".rstrip("0").rstrip(".").replace(".", ",")
    exponent = int(math.floor(log_value / LN_10 + 1e-9))
    coefficient = round(math.exp(log_value - exponent * LN_10), 2)
    if coefficient >= 9.995:
        coefficient, exponent = 1.0, exponent + 1
    coef_str = _decimal(coefficient)
    return f'{coef_str} × 10<tspan dy="-5" font-size="9">{exponent}</tspan><tspan dy="5"></tspan>'


def _format_sci_tick(val: float) -> str:
    if val == 0:
        return "0"
    if val < 1_000_000:
        if abs(val - round(val)) < 1e-9:
            return str(int(round(val)))
        return f"{val:.2f}".rstrip("0").rstrip(".").replace(".", ",")
    exp = int(math.floor(math.log10(val) + 1e-9))
    coef = round(val / (10**exp), 2)
    if coef >= 9.995:
        coef, exp = 1.0, exp + 1
    coef_str = str(int(round(coef))) if abs(coef - round(coef)) < 1e-9 else f"{coef:.2f}".rstrip("0").rstrip(".").replace(".", ",")
    return f'{coef_str} × 10<tspan dy="-5" font-size="9">{exp}</tspan><tspan dy="5"></tspan>'


def _calc_ratio(key: str, n_val: float, scale_mode: str, log_maximum: float) -> float:
    log_v = _log_value(key, n_val)
    if log_v is None:
        return 0.0
    if scale_mode == "log":
        numerator = _log1p_from_log(log_v)
        denominator = _log1p_from_log(log_maximum)
        if denominator <= 0:
            return 0.0
        return min(1.0, max(0.0, numerator / denominator))
    diff = log_v - log_maximum
    return math.exp(diff) if diff > -745 else 0.0


def _log1p_from_log(log_value: float) -> float:
    """Calcula ln(1 + exp(log_value)) sin desbordamiento."""
    if log_value > 36:
        return log_value + math.log1p(math.exp(-log_value))
    return math.log1p(math.exp(log_value))


def _log_expm1(value: float) -> float | None:
    """Calcula ln(exp(value) - 1); None representa exactamente cero."""
    if value <= 0:
        return None
    if value > 36:
        return value + math.log1p(-math.exp(-value))
    return math.log(math.expm1(value))


def _svg_polyline(key: str, x_max: float, log_maximum: float, scale_mode: str, width: int, height: int) -> str:
    left, right, top, bottom = 100, 20, 24, 52
    plot_width, plot_height = width - left - right, height - top - bottom
    # Un muestreo fijo y denso evita que las curvas de valores pequeños se vean
    # como una sucesión de segmentos rectos durante la animación.
    sample_count = 181 if x_max > 0 else 2
    points = []
    for index in range(sample_count):
        x_value = x_max * index / (sample_count - 1)
        x = left + x_value / max(1.0, x_max) * plot_width
        y = top + (1 - _calc_ratio(key, x_value, scale_mode, log_maximum)) * plot_height
        points.append(f"{x:.2f},{y:.2f}")
    return " ".join(points)


def _render_chart(
    current_n: float,
    selected_keys: tuple[str, ...],
    scale_mode: str = "linear",
    x_limit: float | None = None,
) -> str:
    width, height = 650, 410
    left, right, top, bottom = 100, 20, 24, 52
    plot_width, plot_height = width - left - right, height - top - bottom
    x_max = max(1.0, current_n if x_limit is None else x_limit)
    final_logs = [_log_value(key, current_n) for key in selected_keys]
    log_maximum = max((value for value in final_logs if value is not None), default=0.0)
    grid = []
    if scale_mode == "log":
        transformed_maximum = _log1p_from_log(log_maximum)
        ticks_data = []
        for i in range(5):
            ratio = i / 4
            label = _format_log_axis(_log_expm1(ratio * transformed_maximum))
            ticks_data.append((ratio, label))
    else:
        ticks_data = []
        for i in range(5):
            ratio = i / 4
            if ratio == 0:
                label = "0"
            elif log_maximum < math.log(1_000_000):
                val = math.exp(log_maximum) * ratio
                label = _format_sci_tick(val)
            else:
                diff = log_maximum + math.log(ratio)
                exp = int(math.floor(diff / LN_10 + 1e-9))
                coef = round(math.exp(diff - exp * LN_10), 2)
                if coef >= 9.995:
                    coef, exp = 1.0, exp + 1
                coef_str = str(int(round(coef))) if abs(coef - round(coef)) < 1e-9 else f"{coef:.2f}".rstrip("0").rstrip(".").replace(".", ",")
                label = f'{coef_str} × 10<tspan dy="-5" font-size="9">{exp}</tspan><tspan dy="5"></tspan>'
            ticks_data.append((ratio, label))

    for ratio, label in ticks_data:
        y = top + (1 - ratio) * plot_height
        grid.append(
            f'<line x1="{left}" y1="{y:.2f}" x2="{width - right}" y2="{y:.2f}" />'
            f'<text class="growth-app__y-tick" data-ratio="{ratio:.2f}" x="{left - 12}" y="{y + 4:.2f}" text-anchor="end">{label}</text>'
        )

    lines = []
    for key in selected_keys:
        _, _, text, color = FAMILY_BY_KEY[key]
        point_x = left + current_n / x_max * plot_width
        point_y = top + (1 - _calc_ratio(key, current_n, scale_mode, log_maximum)) * plot_height
        lines.append(
            f'<polyline class="growth-app__curve" data-family="{key}" points="{_svg_polyline(key, max(0.0, current_n), log_maximum, scale_mode, width, height)}" '
            f'fill="none" stroke="{color}" stroke-width="2.5" vector-effect="non-scaling-stroke">'
            f'<title>{escape(text)}</title></polyline><circle class="growth-app__curve-point" data-family="{key}" cx="{point_x:.2f}" cy="{point_y:.2f}" '
            f'r="4" fill="{color}"><title>{escape(text)}</title></circle>'
        )
    candidates = (0, max(1, round(x_max / 2)), max(1, round(x_max)))
    ticks = list(dict.fromkeys(candidates))
    x_labels = "".join(
        f'<text class="growth-app__x-tick" data-ratio="{value / max(1, x_max):.2f}" '
        f'x="{left + value / max(1, x_max) * plot_width:.2f}" y="{height - 30}" text-anchor="middle">{value}</text>'
        for value in ticks
    )
    scale_label = "Escala logarítmica" if scale_mode == "log" else "Escala lineal"
    maximum_key = max(
        selected_keys,
        key=lambda key: _log_value(key, current_n) if _log_value(key, current_n) is not None else -math.inf,
        default=None,
    )
    maximum_label = (
        _format_exact_value(_exact_value(maximum_key, round(current_n))) if maximum_key else "0"
    )
    return f"""
      <div class="growth-app__chart" role="img" aria-label="Gráfica de las funciones seleccionadas ({scale_label})">
        <div class="growth-app__range">Rango visible: 0 ≤ <i>f</i>(<i>n</i>) ≤ {maximum_label}</div>
        <svg viewBox="0 0 {width} {height}" preserveAspectRatio="xMidYMid meet">
          <g class="growth-app__grid">{"".join(grid)}</g>
          <line class="growth-app__axis" x1="{left}" y1="{top}" x2="{left}" y2="{height - bottom}" />
          <line class="growth-app__axis" x1="{left}" y1="{height - bottom}" x2="{width - right}" y2="{height - bottom}" />
          {"".join(lines)}<g class="growth-app__x-labels">{x_labels}</g>
          <text class="growth-app__axis-name" x="{left + plot_width / 2:.2f}" y="{height - 8}" text-anchor="middle">Tamaño de entrada n</text>
          <text class="growth-app__axis-name" transform="translate(22 {top + plot_height / 2:.2f}) rotate(-90)" text-anchor="middle">f(n)</text>
        </svg>
      </div>
    """


def _render_race(current_n: float, display_n: int, selected_keys: tuple[str, ...], scale_mode: str = "linear") -> str:
    """Crea una carrera de barras con transición suave al reordenarse."""
    visual_logs = {key: _log_value(key, current_n) for key in selected_keys}
    log_maximum = max((value for value in visual_logs.values() if value is not None), default=0.0)
    order = sorted(
        selected_keys,
        key=lambda key: visual_logs[key] if visual_logs[key] is not None else -math.inf,
        reverse=True,
    )
    rank_of = {key: rank for rank, key in enumerate(order)}
    row_height = 42
    total_height = len(selected_keys) * row_height
    rows = []
    for key in selected_keys:
        rank = rank_of[key]
        _, formula, text, color = FAMILY_BY_KEY[key]
        exact_value = _exact_value(key, display_n)
        width = _calc_ratio(key, current_n, scale_mode, log_maximum) * 100
        top_offset = rank * row_height
        rows.append(
            f'<div class="growth-app__race-row" data-family="{key}" style="--family-color:{color}; transform: translateY({top_offset}px);">'
            f'<span class="growth-app__rank">{rank + 1}</span>'
            f'<span class="growth-app__race-formula">{formula}</span>'
            '<span class="growth-app__bar-track" aria-hidden="true">'
            f'<span class="growth-app__bar" style="width:{width:.12g}%"></span></span>'
            f'<output class="growth-app__race-value">{_format_exact_value(exact_value)}</output>'
            "</div>"
        )
    return (
        f'<div class="growth-app__race" role="img" aria-label="Carrera de barras de las funciones seleccionadas" style="height:{total_height}px;">'
        f"{''.join(rows)}</div>"
    )


def _comparison_message(n: int, logs: dict[str, float | None]) -> str:
    if n <= 2:
        return "Al comienzo, varias funciones todavía tienen valores iguales o cercanos."
    if n <= 5:
        return "Las funciones polinomiales empiezan a separarse de las funciones lineal y logarítmica."
    if n <= 10:
        return f"2<sup><i>n</i></sup> ya es aproximadamente {_decimal(2**n / n)} veces mayor que <i>n</i>."
    factorial_log, exponential_log = logs.get("factorial"), logs.get("exponential")
    if factorial_log is not None and exponential_log is not None and factorial_log > exponential_log:
        coefficient, exponent = _scientific_parts(factorial_log - exponential_log)
        return (
            f"<i>n</i>! es aproximadamente {_decimal(coefficient)} × 10<sup>{exponent}</sup> veces mayor "
            "que 2<sup><i>n</i></sup>; las demás familias quedan concentradas cerca del origen."
        )
    return "Las funciones seleccionadas se comparan sin comprimir sus diferencias de magnitud."


def _render(
    current_n: float,
    selected_keys: tuple[str, ...] | None = None,
    scale_mode: str = "linear",
    *,
    app_id: str = "",
    target_n: int | None = None,
) -> str:
    if selected_keys is None:
        selected_keys = tuple(family[0] for family in FAMILIES)
    n = max(MIN_N, min(MAX_N, int(round(current_n))))
    logs = {key: _log_value(key, current_n) for key in selected_keys}
    scale_note = (
        "<strong>Escala logarítmica:</strong> comprime los órdenes de magnitud para comparar visualmente todas las familias a la vez."
        if scale_mode == "log"
        else "<strong>Escala lineal real:</strong> una función puede quedar prácticamente sobre cero cuando otra la supera por muchos órdenes de magnitud."
    )
    visualization = (
        '<div class="growth-app__unified">'
        '<section class="growth-app__view"><h4>Crecimiento de las curvas</h4>'
        f"{_render_chart(current_n, selected_keys, scale_mode, target_n)}</section>"
        '<section class="growth-app__view growth-app__race-view"><h4>Carrera de crecimiento</h4>'
        f"{_render_race(current_n, n, selected_keys, scale_mode)}</section></div>"
    )
    return f"""
      <section class="growth-app__visual" data-growth-app-id="{escape(app_id)}" data-scale="{escape(scale_mode)}"><header class="growth-app__header">
        <div><span>Comparación interactiva</span><h3>¿Cómo se separan las funciones?</h3></div>
        <div class="growth-app__current"><small>Valor actual</small><strong><i>n</i> = {n}</strong></div>
      </header><div class="growth-app__milestone" role="status" hidden></div><div class="growth-app__panel">{visualization}</div>
      <div class="growth-app__insight" role="status">{_comparison_message(n, logs)}</div>
      <section class="growth-app__summary" aria-live="polite" hidden></section>
      <div class="growth-app__comparison" role="status" aria-live="polite" hidden></div>
      <div class="growth-app__conclusion" role="status" aria-live="polite"></div>
      <p class="growth-app__note">{scale_note}</p></section>
    """


def _javascript_app(
    app_id: str,
    target: int,
    selected_keys: tuple[str, ...],
    scale_mode: str,
    speed: float,
) -> str:
    """Runtime visual a 60 FPS; Python conserva cálculo, controles y fallback."""
    template = r"""
(() => {
  const appId = __APP_ID__;
  const target = __TARGET__;
  const reduceMotion = window.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches ?? false;
  const duration = reduceMotion ? 250 : __DURATION__;
  const scaleMode = __SCALE__;
  const keys = __KEYS__;
  const formulas = __FORMULAS__;
  const FAMILY_COLORS = __COLORS__;
  const registry = window.__growthComparisonApps ||= {};
  registry[appId]?.destroy?.();

  const boot = (attempt = 0) => {
    const visual = document.querySelector(`[data-growth-app-id="${appId}"]`);
    if (!visual) {
      if (attempt < 120) requestAnimationFrame(() => boot(attempt + 1));
      return;
    }
    const root = visual.closest('.growth-comparison-app');
    const pauseButton = root?.querySelector('.growth-app__pause-button');
    const insight = visual.querySelector('.growth-app__insight');
    const milestone = visual.querySelector('.growth-app__milestone');
    const summary = visual.querySelector('.growth-app__summary');
    const comparison = visual.querySelector('.growth-app__comparison');
    const conclusion = visual.querySelector('.growth-app__conclusion');
    const rangeLabel = visual.querySelector('.growth-app__range');
    const currentLabel = visual.querySelector('.growth-app__current strong');
    const curves = new Map(
      [...visual.querySelectorAll('.growth-app__curve')].map((curve) => [curve.dataset.family, curve])
    );
    const points = new Map(
      [...visual.querySelectorAll('.growth-app__curve-point')].map((node) => [node.dataset.family, node])
    );
    const xTicks = [...visual.querySelectorAll('.growth-app__x-tick')];
    const yTicks = [...visual.querySelectorAll('.growth-app__y-tick')];
    const rows = new Map(
      [...visual.querySelectorAll('.growth-app__race-row')].map((node) => [node.dataset.family, node])
    );
    const selectedSummaryKeys = new Set();
    const previousSummaryRanks = new Map();
    const LN10 = Math.log(10);
    const lanczos = [
      0.99999999999980993, 676.5203681218851, -1259.1392167224028,
      771.32342877765313, -176.61502916214059, 12.507343278686905,
      -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7
    ];
    const logGamma = (z) => {
      if (z < 0.5) return Math.log(Math.PI) - Math.log(Math.sin(Math.PI * z)) - logGamma(1 - z);
      z -= 1;
      let x = lanczos[0];
      for (let i = 1; i < lanczos.length; i += 1) x += lanczos[i] / (z + i);
      const t = z + lanczos.length - 1.5;
      return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
    };
    const logValue = (key, n) => {
      n = Math.max(0, n);
      if (key === 'constant') return 0;
      if (key === 'log' || key === 'nlogn') {
        if (n <= 1) return -Infinity;
        const logarithm = Math.log2(n);
        return Math.log(logarithm) + (key === 'nlogn' ? Math.log(n) : 0);
      }
      if (key === 'linear') return n > 0 ? Math.log(n) : -Infinity;
      if (key === 'square') return n > 0 ? 2 * Math.log(n) : -Infinity;
      if (key === 'cube') return n > 0 ? 3 * Math.log(n) : -Infinity;
      if (key === 'exponential') return n * Math.log(2);
      if (key === 'factorial') return logGamma(n + 1);
      return -Infinity;
    };
    const softplus = (value) => value > 36 ? value + Math.log1p(Math.exp(-value)) : Math.log1p(Math.exp(value));
    const decimal = (value, digits = 2) => {
      if (Math.abs(value - Math.round(value)) < 1e-9) return String(Math.round(value));
      return value.toFixed(digits).replace(/0+$/, '').replace(/\.$/, '').replace('.', ',');
    };
    const scientific = (logarithm) => {
      if (!Number.isFinite(logarithm)) return '0';
      if (logarithm < Math.log(1e6)) return decimal(Math.exp(logarithm));
      let exponent = Math.floor(logarithm / LN10 + 1e-9);
      let coefficient = Math.exp(logarithm - exponent * LN10);
      if (coefficient >= 9.995) { coefficient = 1; exponent += 1; }
      return `${decimal(coefficient)} × 10<tspan dy="-5" font-size="9">${exponent}</tspan><tspan dy="5"></tspan>`;
    };
    const scientificHtml = (logarithm) => {
      if (!Number.isFinite(logarithm)) return '0';
      if (logarithm < Math.log(1e6)) return decimal(Math.exp(logarithm));
      let exponent = Math.floor(logarithm / LN10 + 1e-9);
      let coefficient = Math.exp(logarithm - exponent * LN10);
      if (coefficient >= 9.995) { coefficient = 1; exponent += 1; }
      return `${decimal(coefficient)} × 10<sup>${exponent}</sup>`;
    };
    const inverseSoftplus = (value) => {
      if (value <= 0) return -Infinity;
      return value > 36 ? value + Math.log1p(-Math.exp(-value)) : Math.log(Math.expm1(value));
    };
    const formattedValue = (key, n) => {
      const rounded = Math.max(0, Math.round(n));
      let value;
      if (key === 'constant') value = 1;
      else if (key === 'log') value = rounded > 0 ? Math.log2(rounded) : 0;
      else if (key === 'linear') value = rounded;
      else if (key === 'nlogn') value = rounded > 0 ? rounded * Math.log2(rounded) : 0;
      else if (key === 'square') value = rounded ** 2;
      else if (key === 'cube') value = rounded ** 3;
      else if (key === 'exponential' && rounded < 53) value = 2 ** rounded;
      else if (key === 'factorial' && rounded <= 18) {
        value = 1;
        for (let i = 2; i <= rounded; i += 1) value *= i;
      }
      if (Number.isFinite(value) && Math.abs(value) < 1e6) return decimal(value);
      const logarithm = logValue(key, rounded);
      if (!Number.isFinite(logarithm)) return '0';
      let exponent = Math.floor(logarithm / LN10 + 1e-9);
      let coefficient = Math.exp(logarithm - exponent * LN10);
      if (coefficient >= 9.995) { coefficient = 1; exponent += 1; }
      return `${decimal(coefficient)} × 10<sup>${exponent}</sup>`;
    };
    const exactTooltip = (key, n) => {
      const rounded = Math.max(0, Math.round(n));
      if (key === 'constant') return '1';
      if (key === 'log') return rounded > 0 ? String(Math.log2(rounded)) : '0';
      if (key === 'linear') return String(rounded);
      if (key === 'nlogn') return rounded > 0 ? String(rounded * Math.log2(rounded)) : '0';
      if (key === 'square') return String(BigInt(rounded) ** 2n);
      if (key === 'cube') return String(BigInt(rounded) ** 3n);
      if (key === 'exponential') return String(2n ** BigInt(rounded));
      if (key === 'factorial') {
        let value = 1n;
        for (let i = 2n; i <= BigInt(rounded); i += 1n) value *= i;
        return String(value);
      }
      return '';
    };
    const ratioFor = (value, maximum) => {
      if (!Number.isFinite(value)) return 0;
      if (scaleMode === 'log') {
        const denominator = softplus(maximum);
        return denominator > 0 ? Math.max(0, Math.min(1, softplus(value) / denominator)) : 0;
      }
      const difference = value - maximum;
      return difference > -745 ? Math.min(1, Math.exp(difference)) : 0;
    };
    const updateChart = (n, logs, maximum) => {
      const domain = Math.max(1, target);
      const left = 100, top = 24, plotWidth = 530, plotHeight = 334;
      const samples = 181;
      curves.forEach((curve, key) => {
        const coordinates = [];
        for (let index = 0; index < samples; index += 1) {
          const xValue = n * index / (samples - 1);
          const x = left + xValue / domain * plotWidth;
          const y = top + (1 - ratioFor(logValue(key, xValue), maximum)) * plotHeight;
          coordinates.push(`${x.toFixed(2)},${y.toFixed(2)}`);
        }
        curve.setAttribute('points', coordinates.join(' '));
        const point = points.get(key);
        if (point) {
          point.setAttribute('cx', String(left + n / domain * plotWidth));
          point.setAttribute('cy', String(top + (1 - ratioFor(logs[key], maximum)) * plotHeight));
        }
      });
      xTicks.forEach((tick) => {
        const ratio = Number(tick.dataset.ratio);
        tick.textContent = decimal(domain * ratio, domain < 10 ? 1 : 0);
      });
      const transformedMaximum = softplus(maximum);
      yTicks.forEach((tick) => {
        const ratio = Number(tick.dataset.ratio);
        if (ratio === 0) { tick.textContent = '0'; return; }
        const tickLog = scaleMode === 'log'
          ? inverseSoftplus(transformedMaximum * ratio)
          : maximum + Math.log(ratio);
        tick.innerHTML = scientific(tickLog);
      });
      if (rangeLabel) rangeLabel.innerHTML = `Rango visible: 0 ≤ <i>f</i>(<i>n</i>) ≤ ${scientificHtml(maximum)}`;
    };
    const milestoneFor = (n) => {
      const candidates = [
        { at: 3, keys: ['linear', 'nlogn'], text: '<i>n</i> · log<sub>2</sub>(<i>n</i>) supera a <i>n</i>.' },
        { at: 4, keys: ['factorial', 'exponential'], text: '<i>n</i>! supera a 2<sup><i>n</i></sup>.' },
        { at: 6, keys: ['factorial', 'cube'], text: '<i>n</i>! supera a <i>n</i><sup>3</sup>.' },
        { at: 10, keys: ['exponential', 'cube'], text: '2<sup><i>n</i></sup> supera a <i>n</i><sup>3</sup>.' },
      ];
      return [...candidates].reverse().find((item) => n >= item.at && item.keys.every((key) => keys.includes(key)));
    };
    const updateMilestone = (n) => {
      if (!milestone) return;
      const item = milestoneFor(n);
      milestone.hidden = !item;
      if (item) milestone.innerHTML = `<strong>Hito en <i>n</i> = ${item.at}</strong><span>${item.text}</span>`;
    };
    const ratioText = (difference) => {
      if (!Number.isFinite(difference)) return '—';
      const orders = Math.max(0, difference / LN10);
      const ratio = Math.exp(Math.min(difference, 700));
      const ratioLabel = difference > 700 ? scientificHtml(difference) : formattedValueFromNumber(ratio);
      return `${decimal(orders, 1)} órdenes de magnitud (≈ ${ratioLabel} veces)`;
    };
    const formattedValueFromNumber = (value) => {
      if (!Number.isFinite(value) || value >= 1e6) return scientificHtml(Math.log(value));
      return decimal(value);
    };
    const updateSelection = () => {
      const active = selectedSummaryKeys.size > 0;
      visual.classList.toggle('has-summary-selection', active);
      curves.forEach((node, key) => node.classList.toggle('is-selected', selectedSummaryKeys.has(key)));
      points.forEach((node, key) => node.classList.toggle('is-selected', selectedSummaryKeys.has(key)));
      rows.forEach((node, key) => node.classList.toggle('is-selected', selectedSummaryKeys.has(key)));
      summary?.querySelectorAll('tbody tr').forEach((node) => {
        node.classList.toggle('is-selected', selectedSummaryKeys.has(node.dataset.family));
        node.setAttribute('aria-selected', String(selectedSummaryKeys.has(node.dataset.family)));
      });
    };
    const updateComparison = (n, logs) => {
      if (!comparison) return;
      const chosen = [...selectedSummaryKeys];
      comparison.hidden = chosen.length !== 2;
      if (chosen.length !== 2) return;
      const [first, second] = chosen.sort((a, b) => logs[b] - logs[a]);
      const difference = logs[first] - logs[second];
      if (!Number.isFinite(difference)) {
        comparison.innerHTML = `Para <i>n</i> = ${Math.round(n)}, ${formulas[first]} y ${formulas[second]} todavía no admiten una razón positiva comparable.`;
        return;
      }
      comparison.innerHTML = `Para <i>n</i> = ${Math.round(n)}, <strong>${formulas[first]}</strong> es aproximadamente <strong>${scientificHtml(difference)}</strong> veces mayor que ${formulas[second]}.`;
    };
    const updateConclusion = (n, logs) => {
      if (!conclusion) return;
      const order = [...keys].sort((a, b) => logs[b] - logs[a]);
      if (!order.length || n < 1) { conclusion.textContent = 'Reproduce la simulación para observar cómo se separan las familias de crecimiento.'; return; }
      const leader = order[0];
      const runnerUp = order[1];
      const gap = runnerUp ? logs[leader] - logs[runnerUp] : 0;
      const reason = gap > LN10
        ? `La diferencia ya supera ${decimal(gap / LN10, 1)} órdenes de magnitud y seguirá ampliándose con entradas mayores.`
        : 'Las primeras posiciones todavía están próximas, pero sus tasas de crecimiento no son equivalentes.';
      conclusion.innerHTML = `<strong>Conclusión:</strong> para <i>n</i> = ${Math.round(n)}, ${formulas[leader]} domina la comparación. ${reason}`;
    };
    const updateSummary = (n, logs) => {
      if (!summary) return;
      const order = [...keys].sort((a, b) => logs[b] - logs[a]);
      const rows = order.map((key, index) => {
        const next = order[index + 1];
        const difference = next && Number.isFinite(logs[key]) && Number.isFinite(logs[next])
          ? Math.max(0, logs[key] - logs[next]) : null;
        const value = formattedValue(key, n);
        const tooltip = exactTooltip(key, n);
        return `<tr data-family="${key}" tabindex="0" role="button" aria-selected="false" title="Seleccionar ${formulas[key].replace(/<[^>]+>/g, '')}"><th scope="row">${index + 1}</th><td class="growth-app__summary-formula"><span class="growth-app__color-key" style="--family-color:${FAMILY_COLORS[key]}"></span>${formulas[key]}</td><td title="Valor completo: ${tooltip}">${value}</td><td>${difference === null ? '—' : ratioText(difference)}</td></tr>`;
      }).join('');
      summary.innerHTML = `<h4>Resumen en <i>n</i> = ${Math.round(n)}</h4><p class="growth-app__summary-help">Selecciona hasta dos filas para destacar y comparar funciones.</p><div class="growth-app__summary-table-wrap"><table><thead><tr><th scope="col">Posición</th><th scope="col">Función</th><th scope="col">Resultado</th><th scope="col">Diferencia respecto a la siguiente</th></tr></thead><tbody>${rows}</tbody></table></div>`;
      summary.hidden = false;
      summary.querySelectorAll('tbody tr').forEach((row) => {
        const currentRank = order.indexOf(row.dataset.family);
        const previousRank = previousSummaryRanks.get(row.dataset.family);
        if (!reduceMotion && previousRank !== undefined && previousRank !== currentRank) {
          row.animate(
            [{ transform: `translateY(${(previousRank - currentRank) * row.offsetHeight}px)` }, { transform: 'translateY(0)' }],
            { duration: 260, easing: 'ease-out' }
          );
        }
        previousSummaryRanks.set(row.dataset.family, currentRank);
        const activate = () => {
          const key = row.dataset.family;
          if (selectedSummaryKeys.has(key)) selectedSummaryKeys.delete(key);
          else {
            if (selectedSummaryKeys.size >= 2) selectedSummaryKeys.delete(selectedSummaryKeys.values().next().value);
            selectedSummaryKeys.add(key);
          }
          updateSelection();
          updateComparison(n, logs);
        };
        row.addEventListener('click', activate);
        row.addEventListener('keydown', (event) => {
          if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); activate(); }
        });
      });
      updateSelection();
    };
    const setPauseVisual = (isPaused, finished = false) => {
      if (!pauseButton) return;
      const canContinue = isPaused && !finished;
      const text = canContinue ? 'Continuar' : 'Pausar';
      pauseButton.innerHTML = `<i class="fa fa-${canContinue ? 'play' : 'pause'}" aria-hidden="true"></i> ${text}`;
      pauseButton.title = text;
      pauseButton.setAttribute('aria-label', text);
      pauseButton.disabled = finished;
    };
    const messageFor = (n, logs) => {
      if (!keys.length) return 'Selecciona una o más funciones para comenzar la comparación.';
      if (n <= 2) return 'Al comienzo, varias funciones todavía tienen valores iguales o cercanos.';
      if (n <= 5) return 'Las funciones polinomiales empiezan a separarse de las funciones lineal y logarítmica.';
      if (n <= 10) return `2<sup><i>n</i></sup> ya es aproximadamente ${decimal((2 ** Math.round(n)) / Math.max(1, Math.round(n)))} veces mayor que <i>n</i>.`;
      const factorial = logs.factorial;
      const exponential = logs.exponential;
      if (Number.isFinite(factorial) && Number.isFinite(exponential) && factorial > exponential) {
        const difference = factorial - exponential;
        const exponent = Math.floor(difference / LN10 + 1e-9);
        const coefficient = Math.exp(difference - exponent * LN10);
        return `<i>n</i>! es aproximadamente ${decimal(coefficient)} × 10<sup>${exponent}</sup> veces mayor que 2<sup><i>n</i></sup>.`;
      }
      return 'Las funciones seleccionadas se comparan con sus valores reales; solo cambia la representación visual de la escala.';
    };

    let fraction = 0;
    let paused = false;
    let frame = 0;
    let started = performance.now();
    let chartMaximum = 0;
    let previousFraction = 0;
    let previousSummaryN = -1;
    const summaryStep = Math.max(1, Math.ceil(target / 100));
    const render = (nextFraction) => {
      fraction = Math.max(0, Math.min(1, nextFraction));
      const n = target * fraction;
      const displayN = Math.max(0, Math.round(n));
      if (currentLabel) currentLabel.innerHTML = `<i>n</i> = ${displayN}`;
      const logs = Object.fromEntries(keys.map((key) => [key, logValue(key, n)]));
      const finite = Object.values(logs).filter(Number.isFinite);
      const maximum = finite.length ? Math.max(...finite) : 0;
      const movingBackward = fraction < previousFraction;
      chartMaximum = movingBackward ? maximum : chartMaximum + (maximum - chartMaximum) * 0.22;
      if (fraction >= 1) chartMaximum = maximum;
      if (Math.abs(chartMaximum - maximum) < 1e-6) chartMaximum = maximum;
      previousFraction = fraction;
      const order = [...keys].sort((a, b) => logs[b] - logs[a]);
      order.forEach((key, rank) => {
        const row = rows.get(key);
        if (!row) return;
        row.style.transform = `translateY(${rank * 42}px)`;
        row.querySelector('.growth-app__rank').textContent = String(rank + 1);
        row.querySelector('.growth-app__bar').style.width = `${ratioFor(logs[key], maximum) * 100}%`;
        row.querySelector('.growth-app__race-value').innerHTML = formattedValue(key, n);
      });
      updateChart(n, logs, chartMaximum);
      updateMilestone(displayN);
      if (insight) insight.innerHTML = messageFor(displayN, logs);
      const summaryDue = displayN < previousSummaryN
        || displayN === target
        || previousSummaryN < 0
        || displayN - previousSummaryN >= summaryStep;
      if (summaryDue) {
        previousSummaryN = displayN;
        if (displayN >= 1) updateSummary(displayN, logs);
        else if (summary) summary.hidden = true;
        updateComparison(displayN, logs);
        updateConclusion(displayN, logs);
      }
    };
    const tick = (now) => {
      if (!visual.isConnected) return;
      if (!paused) {
        render((now - started) / duration);
        if (fraction >= 1) {
          paused = true;
          setPauseVisual(true, true);
          return;
        }
      }
      frame = requestAnimationFrame(tick);
    };
    const app = {
      togglePause() {
        const replay = paused && fraction >= 1;
        if (replay) render(0);
        paused = !paused;
        setPauseVisual(paused);
        if (!paused) {
          started = performance.now() - fraction * duration;
          if (replay) frame = requestAnimationFrame(tick);
        }
      },
      finish() {
        paused = true;
        render(1);
        setPauseVisual(true, true);
      },
      reset() { cancelAnimationFrame(frame); paused = true; render(0); setPauseVisual(true); },
      destroy() { cancelAnimationFrame(frame); },
      render,
    };
    registry[appId] = app;
    render(0);
    setPauseVisual(false);
    frame = requestAnimationFrame(tick);
  };
  boot();
})();
"""
    return (
        template.replace("__APP_ID__", json.dumps(app_id))
        .replace("__TARGET__", str(int(target)))
        .replace(
            "__DURATION__",
            str(max(250.0, BASE_DURATION * 1000 / float(speed))),
        )
        .replace("__SCALE__", json.dumps(scale_mode))
        .replace("__KEYS__", json.dumps(selected_keys, ensure_ascii=False))
        .replace(
            "__FORMULAS__",
            json.dumps({key: FAMILY_BY_KEY[key][1] for key in selected_keys}, ensure_ascii=False),
        )
        .replace(
            "__COLORS__",
            json.dumps({key: FAMILY_BY_KEY[key][3] for key in selected_keys}, ensure_ascii=False),
        )
    )


def _javascript_command(app_id: str, command: str) -> str:
    return (
        "window.__growthComparisonApps?.["
        + json.dumps(app_id)
        + "]?."
        + command
        + "?.();"
    )


def _styles() -> str:
    return (
        shared_ui_styles(".growth-comparison-app")
        + """
<style>
.growth-comparison-app{width:100%;font-family:sans-serif}.growth-comparison-app .growth-app__configuration{padding:14px 16px 16px;border:1px solid #dedede;border-top:0}.growth-comparison-app .growth-app__controls{display:flex!important;flex-flow:row wrap!important;gap:12px 36px!important;align-items:center!important;width:100%}.growth-comparison-app .growth-app__controls>.widget-box{flex:0 0 292px!important;width:292px!important;min-width:292px!important;max-width:292px!important}.growth-comparison-app .growth-app__selection-message{color:#a94728;font-size:12px;min-height:18px}.growth-comparison-app .growth-app__visual{border:1px solid #dedede;border-top:4px solid #a94728;background:#fff;margin-top:16px;padding:18px}.growth-comparison-app .growth-app__header{display:flex;justify-content:space-between;align-items:flex-start;gap:16px}.growth-comparison-app .growth-app__header span{color:#a94728;font-size:11px;font-weight:800;letter-spacing:.09em;text-transform:uppercase}.growth-comparison-app .growth-app__header h3{font-size:18px;margin:3px 0 0}.growth-comparison-app .growth-app__current{border-left:3px solid #a94728;padding-left:12px;text-align:right;white-space:nowrap}.growth-comparison-app .growth-app__current small{display:block;color:#666;font-size:12px}.growth-comparison-app .growth-app__current strong{display:block;color:#a94728;font-family:'STIX Two Math','Cambria Math',serif;font-size:24px}.growth-comparison-app .growth-app__panel{border:1px solid #dedede;margin-top:16px;padding:16px 12px}.growth-comparison-app .growth-app__insight{margin-top:16px;border-left:3px solid #a94728;background:#fbf5f2;padding:10px 12px;font-size:14px}.growth-comparison-app .growth-app__note{color:#666;font-size:12px}.growth-comparison-app .growth-app__chart{border:1px solid #dedede;background:#fff;width:100%;overflow:hidden}.growth-comparison-app .growth-app__chart svg{display:block;width:100%;height:auto;min-height:310px}.growth-comparison-app .growth-app__grid line{stroke:#ddd}.growth-comparison-app .growth-app__grid text,.growth-comparison-app .growth-app__x-labels{fill:#555;font:11px sans-serif}.growth-comparison-app .growth-app__axis{stroke:#777}.growth-comparison-app .growth-app__axis-name{fill:#333;font:600 15px sans-serif}
.growth-comparison-app .growth-app__unified{display:grid;grid-template-columns:minmax(0,1.12fr) minmax(350px,.88fr);gap:18px;align-items:stretch}.growth-comparison-app .growth-app__view{min-width:0;border:1px solid #dedede;background:#fff;padding:12px}.growth-comparison-app .growth-app__view h4{font-size:14px;text-align:center;margin:0 0 10px}.growth-comparison-app .growth-app__race{position:relative;width:100%}.growth-comparison-app .growth-app__race-row{position:absolute;left:0;right:0;top:0;display:grid;grid-template-columns:20px 94px minmax(90px,1fr) 104px;column-gap:12px;align-items:center;height:36px;transition:transform .24s ease,opacity .18s ease}.growth-comparison-app .growth-app__rank{color:#777;font-size:11px;text-align:center;font-weight:700}.growth-comparison-app .growth-app__race-formula{color:var(--family-color);font:600 15px 'STIX Two Math','Cambria Math',serif;text-align:center;white-space:nowrap;padding-right:4px}.growth-comparison-app .growth-app__bar-track{height:22px;background:repeating-linear-gradient(90deg,#fafafa 0,#fafafa calc(25% - 1px),#e5e5e5 25%);overflow:hidden}.growth-comparison-app .growth-app__bar{display:block;height:100%;min-width:2px;background:var(--family-color);transition:width .08s linear}.growth-comparison-app .growth-app__race-value{font:12px 'STIX Two Math','Cambria Math',serif;text-align:right;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.growth-comparison-app .growth-app__panel{background:#fafafa}.growth-comparison-app .growth-app__chart{border:0}.growth-comparison-app .growth-app__chart svg{min-height:330px}.growth-comparison-app .growth-app__curve{transition:opacity .18s ease,stroke-width .18s ease}.growth-comparison-app .growth-app__curve-point{pointer-events:none;transition:opacity .18s ease,r .18s ease}.growth-comparison-app .has-summary-selection .growth-app__curve:not(.is-selected),.growth-comparison-app .has-summary-selection .growth-app__curve-point:not(.is-selected),.growth-comparison-app .has-summary-selection .growth-app__race-row:not(.is-selected){opacity:.18}.growth-comparison-app .growth-app__curve.is-selected{stroke-width:4}.growth-comparison-app .growth-app__curve-point.is-selected{r:6}.growth-comparison-app .growth-app__race-row.is-selected{filter:saturate(1.25)}
.growth-comparison-app .growth-app__functions-frame{border:1px solid #767676;background:#fff;padding:6px 12px;border-radius:0;box-sizing:border-box}
.growth-comparison-app .growth-app__functions-group{width:100%!important;min-width:0!important;max-width:none!important;overflow:visible!important;align-items:center!important}.growth-comparison-app .growth-app__functions-group>.standard-control-label{align-self:stretch!important;height:auto!important;display:flex!important;align-items:center!important;justify-content:center!important;text-align:center!important}.growth-comparison-app .growth-app__functions-group>.standard-control-label .compact-control-label{display:block!important;width:100%!important;text-align:center!important}.growth-comparison-app .growth-app__functions-group>.widget-box:last-child{width:auto!important;min-width:0!important;max-width:none!important;flex:1 1 520px!important}.growth-comparison-app .growth-app__function-grid{display:flex;flex-direction:column;gap:8px;width:100%}
.growth-comparison-app .growth-app__function-row{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px 16px;width:100%;align-items:center}
.growth-comparison-app .growth-app__function-option{display:grid!important;grid-template-columns:24px minmax(0,1fr) 24px!important;align-items:center!important;gap:8px!important;width:100%!important;min-width:0!important;overflow:visible!important}
.growth-comparison-app .growth-app__function-checkbox{flex:0 0 18px!important;width:18px!important;min-width:18px!important;margin:0!important;overflow:visible!important}
.growth-comparison-app .growth-app__function-checkbox input[type="checkbox"]{margin:0!important;width:16px!important;height:16px!important}
.growth-comparison-app .growth-app__function-checkbox .widget-label{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}
.growth-comparison-app .growth-app__function-formula{grid-column:2!important;width:100%!important;min-width:0!important;margin:0!important;overflow:visible!important;text-align:center!important}.growth-comparison-app .growth-app__function-spacer{grid-column:3!important;width:24px!important;min-width:24px!important}
.growth-comparison-app .growth-app__function-formula .widget-html-content{font:600 17px/1.25 'STIX Two Math','Cambria Math','Scheherazade New',serif!important;color:#292929!important;white-space:nowrap!important;overflow:visible!important;text-align:center!important}
.growth-comparison-app .growth-app__function-formula i{font-style:italic}.growth-comparison-app .growth-app__function-formula sub,.growth-comparison-app .growth-app__function-formula sup{font-size:.72em;line-height:0}
.growth-comparison-app .growth-family-constant input{accent-color:#607d8b}.growth-comparison-app .growth-family-log input{accent-color:#00838f}.growth-comparison-app .growth-family-linear input{accent-color:#2e7d32}.growth-comparison-app .growth-family-nlogn input{accent-color:#558b2f}.growth-comparison-app .growth-family-square input{accent-color:#ef6c00}.growth-comparison-app .growth-family-cube input{accent-color:#d84315}.growth-comparison-app .growth-family-exponential input{accent-color:#ad1457}.growth-comparison-app .growth-family-factorial input{accent-color:#6a1b9a}
.growth-comparison-app .growth-app__preset-row{display:flex!important;flex-flow:row wrap!important;align-items:center!important;gap:8px!important}.growth-comparison-app .growth-app__scale-help{color:#555;font-size:12px;margin-top:-4px}
.growth-comparison-app .growth-app__slider-wrap{display:flex;flex-direction:column;gap:4px;width:100%;margin-top:2px}
.growth-comparison-app .growth-app__slider-label{font-size:12px;font-weight:600;color:#555}
.growth-comparison-app .growth-app__n-compound{display:flex!important;align-items:center!important;gap:10px!important}.growth-comparison-app .growth-app__n-compound>.widget-int{flex:0 0 88px!important;width:88px!important;min-width:88px!important;max-width:88px!important}
.growth-comparison-app .growth-app__range{min-height:24px;padding:2px 8px 4px;color:#555;font:12px 'STIX Two Math','Cambria Math',serif;text-align:right}.growth-comparison-app .growth-app__milestone{display:flex;gap:8px 16px;align-items:center;margin-top:12px;padding:9px 12px;border-left:3px solid #1976d2;background:#f3f8fd;font:13px 'STIX Two Math','Cambria Math',serif}.growth-comparison-app .growth-app__milestone[hidden]{display:none}.growth-comparison-app .growth-app__summary{margin-top:16px;background:#fff}.growth-comparison-app .growth-app__summary[hidden],.growth-comparison-app .growth-app__comparison[hidden]{display:none}.growth-comparison-app .growth-app__summary h4{margin:0 0 3px;font-size:15px}.growth-comparison-app .growth-app__summary-help{margin:0 0 8px;color:#666;font-size:12px}.growth-comparison-app .growth-app__summary-table-wrap{width:100%;overflow-x:auto}.growth-comparison-app .growth-app__summary table{width:100%;min-width:760px;border-collapse:collapse;font:14px 'STIX Two Math','Cambria Math',serif}.growth-comparison-app .growth-app__summary th,.growth-comparison-app .growth-app__summary td{border:1px solid #c8c8c8;padding:8px 10px;text-align:center;white-space:nowrap}.growth-comparison-app .growth-app__summary thead th{background:#ededed;font-size:15px}.growth-comparison-app .growth-app__summary tbody th{background:#f7f7f7}.growth-comparison-app .growth-app__summary tbody tr{cursor:pointer;transition:background-color .2s ease,transform .2s ease}.growth-comparison-app .growth-app__summary tbody tr:hover th,.growth-comparison-app .growth-app__summary tbody tr:hover td{background:#f4f8fc}.growth-comparison-app .growth-app__summary tbody tr:focus{outline:3px solid #1976d2;outline-offset:-3px}.growth-comparison-app .growth-app__summary tbody tr.is-selected th,.growth-comparison-app .growth-app__summary tbody tr.is-selected td{background:#e7f2fd}.growth-comparison-app .growth-app__summary-formula{font-weight:700}.growth-comparison-app .growth-app__color-key{display:inline-block;width:12px;height:3px;margin-right:8px;vertical-align:middle;background:var(--family-color)}.growth-comparison-app .growth-app__summary tbody tr:first-child th,.growth-comparison-app .growth-app__summary tbody tr:first-child td{background:#fff5e9}.growth-comparison-app .growth-app__summary tbody tr:first-child.is-selected th,.growth-comparison-app .growth-app__summary tbody tr:first-child.is-selected td{background:#e7f2fd}.growth-comparison-app .growth-app__comparison,.growth-comparison-app .growth-app__conclusion{margin-top:12px;padding:10px 12px;font:13px 'STIX Two Math','Cambria Math',serif}.growth-comparison-app .growth-app__comparison{border-left:3px solid #1976d2;background:#f3f8fd}.growth-comparison-app .growth-app__conclusion{border-left:3px solid #558b2f;background:#f4f8f1}
@media(prefers-reduced-motion:reduce){.growth-comparison-app *{scroll-behavior:auto!important;transition-duration:.01ms!important;animation-duration:.01ms!important;animation-iteration-count:1!important}}
@media(max-width:900px){.growth-comparison-app .growth-app__unified{grid-template-columns:1fr}.growth-comparison-app .growth-app__race-view{order:2}.growth-comparison-app .growth-app__function-row{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:640px){.growth-comparison-app .growth-app__header{flex-direction:column}.growth-comparison-app .growth-app__chart svg{min-height:260px}.growth-comparison-app .growth-app__race-row{grid-template-columns:18px 58px minmax(70px,1fr) 82px;gap:5px}.growth-comparison-app .growth-app__race-value{font-size:10px}.growth-comparison-app .growth-app__summary th:nth-child(2),.growth-comparison-app .growth-app__summary td:nth-child(2){position:sticky;left:0;z-index:1;background:#fff}.growth-comparison-app .growth-app__summary thead th:nth-child(2){z-index:2;background:#ededed}}
</style>"""
    )


def run_app():
    """Muestra la simulación con el contrato visual común del portal."""
    app_id = f"growth-{uuid.uuid4().hex}"
    n_input = bounded_int_control(
        value=DEFAULT_N,
        min_value=MIN_TARGET_N,
        max_value=MAX_N,
        step=1,
        description="",
        width="88px",
    )
    speed_input = dropdown_control(
        options=SPEED_OPTIONS,
        value=1.0,
        description="Velocidad",
        width="160px",
    )
    n_slider = widgets.IntSlider(
        value=DEFAULT_N,
        min=MIN_TARGET_N,
        max=MAX_N,
        step=1,
        description="",
        continuous_update=True,
        readout=False,
        layout=widgets.Layout(width="auto", flex="1 1 auto"),
    )
    selectors = {}
    selector_options = []
    for key, formula, text, color in FAMILIES:
        # La etiqueta visible usa HTML matemático; el checkbox queda sin una
        # segunda etiqueta textual para evitar duplicados en JupyterLite.
        cb = widgets.Checkbox(value=True, description="", indent=False)
        cb.add_class("growth-app__function-checkbox")
        selectors[key] = cb
        formula_widget = widgets.HTML(
            value=f'<span style="color:{color}" aria-label="{escape(text)}">{formula}</span>'
        )
        formula_widget.add_class("growth-app__function-formula")
        spacer = widgets.HTML(value="")
        spacer.add_class("growth-app__function-spacer")
        option = widgets.HBox(
            [cb, formula_widget, spacer],
            layout=widgets.Layout(width="100%", align_items="center", grid_gap="8px", overflow="visible"),
        )
        option.add_class("growth-app__function-option")
        option.add_class(f"growth-family-{key}")
        selector_options.append(option)
    row1 = widgets.HBox(selector_options[:4], layout=widgets.Layout(width="100%"))
    row1.add_class("growth-app__function-row")
    row2 = widgets.HBox(selector_options[4:], layout=widgets.Layout(width="100%"))
    row2.add_class("growth-app__function-row")
    function_grid = widgets.VBox(
        [row1, row2],
        layout=widgets.Layout(width="100%", grid_gap="4px"),
    )
    function_grid.add_class("growth-app__function-grid")
    functions_frame = widgets.Box(
        [function_grid],
        layout=widgets.Layout(
            width="100%",
            border_top="1px solid #767676",
            border_right="1px solid #767676",
            border_bottom="1px solid #767676",
            border_left="1px solid #767676",
            padding="6px 12px",
            overflow="visible",
        ),
    )
    functions_frame.add_class("growth-app__functions-frame")
    functions_group = compact_labeled_control(
        "Funciones visibles",
        functions_frame,
    )
    functions_group.add_class("growth-app__functions-group")
    functions_group.layout.margin = "0"
    functions_group.layout.width = "100%"
    functions_group.layout.overflow = "visible"
    selection_message = widgets.HTML(value="", layout=widgets.Layout(width="100%"))
    selection_message.add_class("growth-app__selection-message")
    execute_button = button_control(description="Reproducir", button_style="success", width="128px")
    pause_button = button_control(description="Pausar", button_style="", width="158px", disabled=True)
    finish_button = button_control(description="Finalizar", button_style="", width="128px", disabled=True)
    reset_button = button_control(description="Reiniciar", button_style="warning", width="128px")
    execute_button.icon, pause_button.icon, finish_button.icon, reset_button.icon = (
        "play",
        "pause",
        "fast-forward",
        "refresh",
    )
    pause_button.add_class("growth-app__pause-button")
    scale_input = dropdown_control(
        options=(("Lineal", "linear"), ("Logarítmica", "log")),
        value="linear",
        description="Escala",
        width="160px",
    )
    controls = widgets.Box(
        [
            compact_labeled_control("Escala", scale_input),
            compact_labeled_control("Velocidad", speed_input),
        ],
        layout=widgets.Layout(
            width="100%",
            display="flex",
            flex_flow="row wrap",
            grid_gap="12px 36px",
            align_items="center",
            overflow="visible",
        ),
    )
    controls.add_class("growth-app__controls")
    n_compound = widgets.HBox(
        [n_slider, n_input],
        layout=widgets.Layout(width="100%", align_items="center", grid_gap="10px"),
    )
    n_compound.add_class("growth-app__n-compound")
    slider_wrap = widgets.VBox(
        [
            widgets.HTML('<label class="growth-app__slider-label">Valor final de <i>n</i> (1 – 1 000)</label>'),
            n_compound,
        ],
        layout=widgets.Layout(width="100%", grid_gap="2px"),
    )
    slider_wrap.add_class("growth-app__slider-wrap")
    preset_input = dropdown_control(
        options=PRESETS,
        value="custom",
        description="Combinación",
        width="220px",
    )
    select_all_button = button_control(description="Seleccionar todas", button_style="", width="156px")
    clear_button = button_control(description="Limpiar selección", button_style="", width="156px")
    select_all_button.icon, clear_button.icon = "check-square-o", "eraser"
    preset_row = widgets.HBox(
        [
            compact_labeled_control("Combinación", preset_input),
            select_all_button,
            clear_button,
        ],
        layout=widgets.Layout(width="100%", flex_flow="row wrap", align_items="center", grid_gap="8px"),
    )
    preset_row.add_class("growth-app__preset-row")
    scale_help = widgets.HTML(
        '<p class="growth-app__scale-help"><strong>La escala solo cambia la representación visual;</strong> los valores calculados permanecen iguales.</p>'
    )
    configuration_content = widgets.VBox(
        [
            controls,
            scale_help,
            slider_wrap,
            preset_row,
            functions_group,
            selection_message,
        ],
        layout=widgets.Layout(width="100%", grid_gap="12px"),
    )
    configuration_content.add_class("growth-app__configuration")
    configuration_panel = collapsible_panel(
        "Configuración",
        configuration_content,
        prefix="growth-app",
        open_by_default=True,
    )
    output = widgets.HTML(layout=widgets.Layout(width="100%", margin="0"))
    javascript_output = widgets.Output(
        layout=widgets.Layout(width="0", height="0", margin="0", padding="0", overflow="hidden")
    )
    state = {"syncing": False, "selection_syncing": False}

    def selected_keys():
        return tuple(key for key, selector in selectors.items() if selector.value)

    def send_javascript(source):
        with javascript_output:
            clear_output(wait=True)
            display(Javascript(source))

    def redraw():
        pause_button.disabled = True
        finish_button.disabled = True
        pause_button.description = "Pausar"
        pause_button.icon = "pause"
        output.value = _render(
            MIN_N,
            selected_keys(),
            str(scale_input.value),
            app_id=app_id,
            target_n=int(n_input.value),
        )

    def sync_n(value):
        state["syncing"] = True
        try:
            n_input.value = n_slider.value = max(MIN_TARGET_N, min(MAX_N, int(value)))
        finally:
            state["syncing"] = False

    def on_n_change(change):
        if state["syncing"] or change.get("name") != "value":
            return
        value = max(MIN_TARGET_N, min(MAX_N, int(change["new"])))
        sync_n(value)
        send_javascript(_javascript_command(app_id, "destroy"))
        redraw()

    def on_function_change(change):
        if state["selection_syncing"] or change.get("name") != "value":
            return
        state["selection_syncing"] = True
        try:
            preset_input.value = "custom"
        finally:
            state["selection_syncing"] = False
        selection_message.value = "" if selected_keys() else "Selecciona una o más funciones para ejecutar."
        send_javascript(_javascript_command(app_id, "destroy"))
        redraw()

    def apply_selection(keys, preset="custom"):
        state["selection_syncing"] = True
        try:
            selected = set(keys)
            for key, selector in selectors.items():
                selector.value = key in selected
            preset_input.value = preset
        finally:
            state["selection_syncing"] = False
        selection_message.value = "" if keys else "Selecciona una o más funciones para ejecutar."
        send_javascript(_javascript_command(app_id, "destroy"))
        redraw()

    def reset_view(*_args):
        send_javascript(_javascript_command(app_id, "destroy"))
        redraw()

    def reset_all(*_args):
        send_javascript(_javascript_command(app_id, "destroy"))
        redraw()

    def execute(*_args):
        keys = selected_keys()
        if not keys:
            selection_message.value = "Selecciona una o más funciones para ejecutar."
            return
        target, speed = int(n_input.value), float(speed_input.value)
        sync_n(target)
        pause_button.disabled = False
        finish_button.disabled = False
        pause_button.description = "Pausar"
        pause_button.icon = "pause"
        output.value = _render(
            target,
            keys,
            str(scale_input.value),
            app_id=app_id,
            target_n=target,
        )
        send_javascript(
            _javascript_app(app_id, target, keys, str(scale_input.value), speed)
        )

    def toggle_pause(*_args):
        send_javascript(_javascript_command(app_id, "togglePause"))

    def finish(*_args):
        send_javascript(_javascript_command(app_id, "finish"))
        pause_button.disabled = finish_button.disabled = True

    def on_preset_change(change):
        if state["selection_syncing"] or change.get("name") != "value":
            return
        preset = str(change["new"])
        if preset != "custom":
            apply_selection(PRESET_KEYS[preset], preset)

    n_input.observe(on_n_change, names="value")
    n_slider.observe(on_n_change, names="value")
    scale_input.observe(lambda change: reset_view() if change.get("name") == "value" else None, names="value")
    preset_input.observe(on_preset_change, names="value")
    for selector in selectors.values():
        selector.observe(on_function_change, names="value")
    execute_button.on_click(execute)
    pause_button.on_click(toggle_pause)
    finish_button.on_click(finish)
    reset_button.on_click(reset_all)
    select_all_button.on_click(lambda *_args: apply_selection(PRESET_KEYS["all"], "all"))
    clear_button.on_click(lambda *_args: apply_selection((), "custom"))
    root = widgets.VBox(
        [
            widgets.HTML(value=_styles(), layout=widgets.Layout(width="0", height="0", margin="0")),
            configuration_panel,
            action_button_row([execute_button, pause_button, finish_button, reset_button]),
            output,
            javascript_output,
        ],
        layout=widgets.Layout(width="100%", grid_gap="0", overflow="visible"),
    )
    root.add_class("growth-comparison-app")
    redraw()
    display(root)
    return root


__all__ = [
    "FAMILIES",
    "MIN_TARGET_N",
    "MAX_N",
    "PRESETS",
    "SPEED_OPTIONS",
    "_exact_value",
    "_render",
    "run_app",
]
