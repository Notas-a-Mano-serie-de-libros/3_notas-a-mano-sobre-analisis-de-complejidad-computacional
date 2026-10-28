"""Cálculo tabular de complejidad teórica con las unidades canónicas del libro."""

from __future__ import annotations

import json
import math
import uuid

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

MAX_ORDER = 7
DEFAULT_CONSTANT = 1.0
TEMPORAL_FACTOR = 1e-6
SPATIAL_FACTOR = 1.0
BASE_SECONDS_PER_ORDER = 2.8
SPEED_OPTIONS = (("1x", 1.0), ("2x", 2.0), ("5x", 5.0), ("10x", 10.0))
FAMILIES = (
    ("constant", "<i>c</i>"),
    ("log", "log<sub>2</sub>(<i>n</i>)"),
    ("linear", "<i>n</i>"),
    ("nlogn", "<i>n</i> &middot; log<sub>2</sub>(<i>n</i>)"),
    ("square", "<i>n</i><sup>2</sup>"),
    ("cube", "<i>n</i><sup>3</sup>"),
    ("exponential", "2<sup><i>n</i></sup>"),
    ("factorial", "<i>n</i>!"),
)
FAMILY_COLORS = {
    "constant": "#607d8b",
    "log": "#00838f",
    "linear": "#2e7d32",
    "nlogn": "#558b2f",
    "square": "#ef6c00",
    "cube": "#d84315",
    "exponential": "#ad1457",
    "factorial": "#6a1b9a",
}


def _function_log(key: str, n: int, constant: float = DEFAULT_CONSTANT) -> float | None:
    """Devuelve ln(f(n)); ``None`` representa un resultado exactamente nulo."""

    if n < 1:
        raise ValueError("n debe ser mayor o igual que 1")
    if key == "constant":
        return math.log(constant) if constant > 0 else None
    if key == "log":
        value = math.log2(n)
        return math.log(value) if value > 0 else None
    if key == "linear":
        return math.log(n)
    if key == "nlogn":
        value = n * math.log2(n)
        return math.log(value) if value > 0 else None
    if key == "square":
        return 2 * math.log(n)
    if key == "cube":
        return 3 * math.log(n)
    if key == "exponential":
        return n * math.log(2)
    if key == "factorial":
        return math.lgamma(n + 1)
    raise ValueError(f"Familia desconocida: {key}")


def _result_log(
    key: str,
    n: int,
    complexity_type: str,
    constant: float = DEFAULT_CONSTANT,
) -> float | None:
    """Calcula el logaritmo natural del resultado expresado en la unidad canónica."""

    factor = TEMPORAL_FACTOR if complexity_type == "temporal" else SPATIAL_FACTOR
    if complexity_type not in {"temporal", "spatial"}:
        raise ValueError(f"Tipo de complejidad desconocido: {complexity_type}")
    value = _function_log(key, n, constant)
    return None if value is None else value + math.log(factor)


def _decimal(value: float) -> str:
    rendered = f"{value:.2f}".rstrip("0").rstrip(".")
    return rendered.replace(".", ",")


def _scientific_html(logarithm: float | None) -> str:
    """Representa un valor no negativo en notación científica estable."""

    if logarithm is None:
        return "0"
    ln_10 = math.log(10)
    exponent = math.floor(logarithm / ln_10 + 1e-12)
    coefficient = math.exp(logarithm - exponent * ln_10)
    coefficient = round(coefficient, 2)
    if coefficient >= 10:
        coefficient, exponent = 1.0, exponent + 1
    power = f"10<sup>{exponent}</sup>"
    return power if abs(coefficient - 1) < 1e-12 else f"{_decimal(coefficient)} &middot; {power}"


def _reference_html(complexity_type: str) -> str:
    if complexity_type == "temporal":
        return (
            '<div class="canonical-app__reference"><strong>Referencia temporal</strong>'
            '<span><i>t</i> &asymp; <i>T</i><sub>0</sub> &middot; <i>T</i>(<i>n</i>), '
            '<i>T</i><sub>0</sub> = 10<sup>&minus;6</sup> s = 1 &micro;s</span></div>'
        )
    return (
        '<div class="canonical-app__reference"><strong>Referencia espacial</strong>'
        '<span><i>s</i> &asymp; <i>S</i><sub>0</sub> &middot; <i>S</i>(<i>n</i>), '
        '<i>S</i><sub>0</sub> = 1 byte</span></div>'
    )


def _render_table(
    complexity_type: str,
    constant: float = DEFAULT_CONSTANT,
    max_order: int = MAX_ORDER,
) -> str:
    """Construye la tabla de resultados para n = 10^0, ..., 10^max_order."""

    if not 0 <= max_order <= MAX_ORDER:
        raise ValueError(f"El orden máximo debe estar entre 0 y {MAX_ORDER}")
    if constant < 0:
        raise ValueError("c no puede ser negativo")
    temporal = complexity_type == "temporal"
    symbol, unit = ("t", "s") if temporal else ("s", "bytes")
    base = (
        '<i>T</i><sub>0</sub> = 10<sup>&minus;6</sup> s'
        if temporal
        else '<i>S</i><sub>0</sub> = 1 byte'
    )
    headers = "".join(f'<th scope="col">{formula}</th>' for _key, formula in FAMILIES)
    rows = []
    for order in range(max_order + 1):
        n = 10**order
        cells = "".join(
            '<td class="canonical-app__number">'
            f'{_scientific_html(_result_log(key, n, complexity_type, constant))}</td>'
            for key, _formula in FAMILIES
        )
        rows.append(
            '<tr><th scope="row" class="canonical-app__n">'
            f'10<sup>{order}</sup></th>{cells}</tr>'
        )
    title = "temporal" if temporal else "espacial"
    return f"""
      <section class="canonical-app__results" aria-live="polite">
        <header><div><span>Cálculo canónico</span><h3>Complejidad {title} teórica</h3></div>
        <p>{base}; <i>c</i> = {_decimal(constant)}</p></header>
        <div class="canonical-app__table-wrap">
          <table><caption>Resultados de {symbol} [{unit}] para cada función</caption>
            <thead><tr><th scope="col">Cantidad de datos</th>{headers}</tr></thead>
            <tbody>{''.join(rows)}</tbody>
          </table>
        </div>
        <p class="canonical-app__footnote">Los valores se muestran en {unit}; las cantidades extremas se conservan mediante notación científica.</p>
      </section>
    """


def _render_simulation(
    complexity_type: str,
    constant: float = DEFAULT_CONSTANT,
    max_order: int = MAX_ORDER,
    app_id: str = "canonical-preview",
) -> str:
    """Construye la gráfica animable y la tabla incremental de hitos."""

    if complexity_type not in {"temporal", "spatial"}:
        raise ValueError(f"Tipo de complejidad desconocido: {complexity_type}")
    if not 1 <= max_order <= MAX_ORDER:
        raise ValueError(f"El orden máximo debe estar entre 1 y {MAX_ORDER}")
    if constant < 0:
        raise ValueError("c no puede ser negativo")
    temporal = complexity_type == "temporal"
    title = "temporal" if temporal else "espacial"
    y_label = "t [s]" if temporal else "s [bytes]"
    base = (
        '<i>T</i><sub>0</sub> = 10<sup>&minus;6</sup> s'
        if temporal
        else '<i>S</i><sub>0</sub> = 1 byte'
    )
    plot_left, plot_right = 148, 720
    plot_width = plot_right - plot_left
    x_ticks = "".join(
        f'<g class="canonical-app__x-tick" transform="translate({plot_left + order * plot_width / max_order:.2f} 330)">'
        f'<line y2="6"></line><text y="24">10<tspan baseline-shift="super" font-size="10">{order}</tspan></text></g>'
        for order in range(max_order + 1)
    )
    paths = "".join(
        f'<path class="canonical-app__curve" data-canonical-curve="{key}" stroke="{FAMILY_COLORS[key]}" d=""></path>'
        f'<circle class="canonical-app__point" data-canonical-point="{key}" fill="{FAMILY_COLORS[key]}" r="3.5" cx="{plot_left}" cy="320"></circle>'
        for key, _formula in FAMILIES
    )
    race_rows = "".join(
        '<div class="canonical-app__race-row" '
        f'data-canonical-race-row="{key}" style="--series-color:{FAMILY_COLORS[key]};transform:translateY({index * 42}px)">'
        f'<span class="canonical-app__rank">{index + 1}</span>'
        f'<span class="canonical-app__race-formula">{formula}</span>'
        '<span class="canonical-app__race-track"><span class="canonical-app__race-bar"></span></span>'
        '<span class="canonical-app__race-value">0</span></div>'
        for index, (key, formula) in enumerate(FAMILIES)
    )
    headers = "".join(f'<th scope="col">{formula}</th>' for _key, formula in FAMILIES)
    return f"""
      <section class="canonical-app__simulation" data-canonical-app="{app_id}" aria-live="polite">
        <header class="canonical-app__simulation-header">
          <div><span>Simulación canónica</span><h3>Complejidad {title} teórica</h3></div>
          <div class="canonical-app__current"><small>Tamaño de entrada</small><strong data-canonical-current><i>n</i> = 10<sup>0</sup></strong></div>
        </header>
        <div class="canonical-app__unified">
          <section class="canonical-app__view canonical-app__chart-wrap"><h4>Crecimiento canónico</h4>
            <svg class="canonical-app__chart" viewBox="0 0 760 390" role="img" aria-labelledby="{app_id}-chart-title {app_id}-chart-desc">
              <title id="{app_id}-chart-title">Crecimiento de las funciones de complejidad {title}</title>
              <desc id="{app_id}-chart-desc">Las curvas avanzan con el tamaño de entrada y el eje vertical se reajusta a los valores alcanzados.</desc>
              <rect class="canonical-app__plot-bg" x="{plot_left}" y="24" width="{plot_width}" height="296"></rect>
              <g class="canonical-app__y-grid" data-canonical-y-grid></g>
              <line class="canonical-app__axis" x1="{plot_left}" y1="320" x2="{plot_right}" y2="320"></line>
              <line class="canonical-app__axis" x1="{plot_left}" y1="24" x2="{plot_left}" y2="320"></line>
              <g class="canonical-app__x-ticks">{x_ticks}</g>
              <g class="canonical-app__curves">{paths}</g>
              <text class="canonical-app__axis-title" x="434" y="382" text-anchor="middle">Cantidad de datos <tspan font-style="italic">n</tspan></text>
              <text class="canonical-app__axis-title" x="22" y="172" text-anchor="middle" transform="rotate(-90 22 172)">{y_label}</text>
            </svg>
          </section>
          <section class="canonical-app__view canonical-app__race-view"><h4>Carrera de crecimiento</h4>
            <div class="canonical-app__race" aria-label="Clasificación de funciones por resultado">{race_rows}</div>
            <p>Longitudes representadas en la misma escala logarítmica de la gráfica.</p>
          </section>
        </div>
        <div class="canonical-app__milestone" data-canonical-status>La tabla registrará cada potencia de 10 alcanzada.</div>
        <section class="canonical-app__results">
          <header><div><span>Hitos alcanzados</span><h3>Valores calculados</h3></div><p>{base}; <i>c</i> = {_decimal(constant)}</p></header>
          <div class="canonical-app__table-wrap">
            <table><caption>Resultados para cada orden de magnitud alcanzado</caption>
              <thead><tr><th scope="col">Cantidad de datos</th>{headers}</tr></thead>
              <tbody data-canonical-table-body></tbody>
            </table>
          </div>
          <p class="canonical-app__footnote">Cada fila aparece cuando <i>n</i> alcanza exactamente una nueva potencia de 10.</p>
        </section>
      </section>
    """


def _javascript_app(
    app_id: str,
    complexity_type: str,
    constant: float,
    max_order: int,
    speed: float,
    *,
    autoplay: bool = True,
) -> str:
    """Genera el controlador JavaScript de la animación continua."""

    config = json.dumps(
        {
            "appId": app_id,
            "type": complexity_type,
            "constant": constant,
            "maxOrder": max_order,
            "speed": speed,
            "baseSecondsPerOrder": BASE_SECONDS_PER_ORDER,
            "families": [key for key, _formula in FAMILIES],
            "autoplay": autoplay,
        }
    )
    return rf"""
(() => {{
  const config = {config};
  window.__canonicalComplexityApps = window.__canonicalComplexityApps || {{}};
  const previous = window.__canonicalComplexityApps[config.appId];
  if (previous && previous.destroy) previous.destroy();
  const boot = (attempt = 0) => {{
    const root = document.querySelector(`[data-canonical-app="${{config.appId}}"]`);
    if (!root) {{ if (attempt < 40) setTimeout(() => boot(attempt + 1), 50); return; }}
    const current = root.querySelector('[data-canonical-current]');
    const status = root.querySelector('[data-canonical-status]');
    const tbody = root.querySelector('[data-canonical-table-body]');
    const grid = root.querySelector('[data-canonical-y-grid]');
    const paths = Object.fromEntries([...root.querySelectorAll('[data-canonical-curve]')].map(el => [el.dataset.canonicalCurve, el]));
    const points = Object.fromEntries([...root.querySelectorAll('[data-canonical-point]')].map(el => [el.dataset.canonicalPoint, el]));
    const raceRows = Object.fromEntries([...root.querySelectorAll('[data-canonical-race-row]')].map(el => [el.dataset.canonicalRaceRow, el]));
    const ln10 = Math.log(10);
    const factorLog10 = config.type === 'temporal' ? -6 : 0;
    const yFloor = factorLog10 - 2;
    let fraction = 0, startedAt = 0, frame = 0, paused = !config.autoplay, destroyed = false;
    let lastMilestone = -1, visibleMax = yFloor + 2;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const duration = reducedMotion ? 250 : config.baseSecondsPerOrder * Math.max(1, config.maxOrder) * 1000 / config.speed;

    const logGamma = z => {{
      const p = [0.99999999999980993,676.5203681218851,-1259.1392167224028,771.32342877765313,-176.6150291621406,12.507343278686905,-0.13857109526572012,9.984369578019571e-6,1.5056327351493116e-7];
      if (z < 0.5) return Math.log(Math.PI) - Math.log(Math.sin(Math.PI * z)) - logGamma(1 - z);
      z -= 1; let x = p[0]; for (let i = 1; i < p.length; i++) x += p[i] / (z + i);
      const t = z + 7.5; return 0.5 * Math.log(2 * Math.PI) + (z + 0.5) * Math.log(t) - t + Math.log(x);
    }};
    const functionLog = (key, n) => {{
      if (key === 'constant') return config.constant > 0 ? Math.log(config.constant) : null;
      if (key === 'log') {{ const v = Math.log2(n); return v > 0 ? Math.log(v) : null; }}
      if (key === 'linear') return Math.log(n);
      if (key === 'nlogn') {{ const v = n * Math.log2(n); return v > 0 ? Math.log(v) : null; }}
      if (key === 'square') return 2 * Math.log(n);
      if (key === 'cube') return 3 * Math.log(n);
      if (key === 'exponential') return n * Math.log(2);
      return logGamma(n + 1);
    }};
    const resultLog10 = (key, n) => {{ const value = functionLog(key, n); return value === null ? null : value / ln10 + factorLog10; }};
    const sci = log10 => {{
      if (log10 === null) return '0';
      let exponent = Math.floor(log10 + 1e-12), coefficient = Math.pow(10, log10 - exponent);
      coefficient = Math.round(coefficient * 100) / 100;
      if (coefficient >= 10) {{ coefficient = 1; exponent += 1; }}
      const decimal = String(coefficient).replace('.', ',');
      return `${{Math.abs(coefficient - 1) < 1e-12 ? '' : `${{decimal}} &middot; `}}10<sup>${{exponent}}</sup>`;
    }};
    const rowHtml = order => {{
      const n = 10 ** order;
      const cells = config.families.map(key => `<td class="canonical-app__number">${{sci(resultLog10(key, n))}}</td>`).join('');
      return `<tr${{order === lastMilestone ? ' class="is-latest"' : ''}}><th scope="row" class="canonical-app__n">10<sup>${{order}}</sup></th>${{cells}}</tr>`;
    }};
    const updateTable = order => {{
      const milestone = Math.max(0, Math.min(config.maxOrder, order));
      if (milestone === lastMilestone) return;
      lastMilestone = milestone;
      tbody.innerHTML = Array.from({{length: milestone + 1}}, (_, i) => rowHtml(i)).join('');
      status.innerHTML = `Orden alcanzado: <strong><i>n</i> = 10<sup>${{milestone}}</sup></strong>. La tabla contiene ${{milestone + 1}} ${{milestone === 0 ? 'fila' : 'filas'}}.`;
    }};
    const niceStep = range => {{
      const rough = Math.max(1e-12, range / 5);
      const power = 10 ** Math.floor(Math.log10(rough));
      const fraction = rough / power;
      return (fraction <= 1 ? 1 : fraction <= 2 ? 2 : fraction <= 5 ? 5 : 10) * power;
    }};
    const scaleFor = maximum => {{
      const step = niceStep(Math.max(1, maximum - yFloor));
      const top = Math.max(yFloor + step, Math.ceil(maximum / step) * step);
      return {{step, top}};
    }};
    const drawGrid = (maxLog, step) => {{
      const values = [yFloor];
      let value = Math.ceil((yFloor + 1e-12) / step) * step;
      for (; value <= maxLog + step * 1e-9; value += step) {{
        if (value > yFloor + step * 1e-9) values.push(value);
      }}
      if (values[values.length - 1] < maxLog - step * 1e-9) values.push(maxLog);
      let html = '';
      for (const tickValue of values) {{
        const ratio = (tickValue - yFloor) / (maxLog - yFloor), y = 320 - ratio * 296;
        const roundedExponent = Math.abs(tickValue) < 1e-9 ? 0 : Math.round(tickValue * 100) / 100;
        const exponent = String(roundedExponent).replace('.', ',');
        html += `<line x1="148" x2="720" y1="${{y}}" y2="${{y}}"></line><text x="138" y="${{y + 4}}" text-anchor="end">10<tspan baseline-shift="super" font-size="10">${{exponent}}</tspan></text>`;
      }}
      grid.innerHTML = html;
    }};
    const drawChart = orderProgress => {{
      const samples = Math.max(2, Math.ceil(orderProgress * 26) + 1);
      const logs = [];
      for (let i = 0; i < samples; i++) {{
        const order = samples === 1 ? 0 : orderProgress * i / (samples - 1), n = 10 ** order;
        for (const key of config.families) {{ const value = resultLog10(key, n); if (value !== null && Number.isFinite(value)) logs.push(value); }}
      }}
      const target = Math.max(yFloor + 2, ...logs);
      const scale = scaleFor(target);
      visibleMax = scale.top;
      drawGrid(visibleMax, scale.step);
      const x = order => 148 + 572 * order / config.maxOrder;
      const y = value => 320 - 296 * Math.max(0, Math.min(1, (value - yFloor) / (visibleMax - yFloor)));
      for (const key of config.families) {{
        const segments = []; let endpoint = null;
        for (let i = 0; i < samples; i++) {{
          const order = orderProgress * i / (samples - 1), value = resultLog10(key, 10 ** order);
          if (value === null || !Number.isFinite(value) || value < yFloor) continue;
          endpoint = [x(order), y(value)]; segments.push(`${{segments.length ? 'L' : 'M'}}${{endpoint[0].toFixed(2)}},${{endpoint[1].toFixed(2)}}`);
        }}
        paths[key].setAttribute('d', segments.join(' '));
        points[key].style.display = endpoint ? '' : 'none';
        if (endpoint) {{ points[key].setAttribute('cx', endpoint[0]); points[key].setAttribute('cy', endpoint[1]); }}
      }}
      const n = 10 ** orderProgress;
      const values = Object.fromEntries(config.families.map(key => [key, resultLog10(key, n)]));
      const order = [...config.families].sort((a, b) => (values[b] ?? -Infinity) - (values[a] ?? -Infinity));
      order.forEach((key, rank) => {{
        const row = raceRows[key]; if (!row) return;
        const value = values[key];
        const ratio = value === null ? 0 : Math.max(0, Math.min(1, (value - yFloor) / (visibleMax - yFloor)));
        row.style.transform = `translateY(${{rank * 42}}px)`;
        row.querySelector('.canonical-app__rank').textContent = String(rank + 1);
        row.querySelector('.canonical-app__race-bar').style.width = `${{ratio * 100}}%`;
        row.querySelector('.canonical-app__race-value').innerHTML = sci(value);
      }});
    }};
    const render = value => {{
      fraction = Math.max(0, Math.min(1, value));
      const orderProgress = config.maxOrder * fraction;
      const milestone = Math.min(config.maxOrder, Math.floor(orderProgress + 1e-9));
      const exact = Math.abs(orderProgress - Math.round(orderProgress)) < 0.002;
      current.innerHTML = exact ? `<i>n</i> = 10<sup>${{Math.round(orderProgress)}}</sup>` : `<i>n</i> &asymp; 10<sup>${{orderProgress.toFixed(2).replace('.', ',')}}</sup>`;
      drawChart(orderProgress);
      updateTable(milestone);
    }};
    const tick = now => {{
      if (destroyed || paused) return;
      if (!startedAt) startedAt = now - fraction * duration;
      render((now - startedAt) / duration);
      if (fraction < 1) frame = requestAnimationFrame(tick); else status.innerHTML += ' <strong>Simulación finalizada.</strong>';
    }};
    const api = {{
      pause() {{ paused = !paused; if (!paused && fraction < 1) {{ startedAt = performance.now() - fraction * duration; frame = requestAnimationFrame(tick); }} return paused; }},
      finish() {{ paused = true; cancelAnimationFrame(frame); render(1); status.innerHTML += ' <strong>Simulación finalizada.</strong>'; }},
      destroy() {{ destroyed = true; cancelAnimationFrame(frame); delete window.__canonicalComplexityApps[config.appId]; }}
    }};
    window.__canonicalComplexityApps[config.appId] = api;
    render(0);
    if (config.autoplay) frame = requestAnimationFrame(tick);
  }};
  boot();
}})();
"""


def _styles() -> str:
    return shared_ui_styles(".canonical-complexity-app") + """
<style>
.canonical-complexity-app{width:100%;font-family:sans-serif}.canonical-complexity-app .canonical-app__configuration{padding:14px 16px 16px;border:1px solid #dedede;border-top:0}.canonical-complexity-app .canonical-app__controls{display:flex!important;flex-flow:row wrap!important;gap:12px 36px!important;align-items:center!important;width:100%}.canonical-complexity-app .canonical-app__reference{display:flex;flex-flow:row wrap;gap:6px 18px;align-items:baseline;border-left:3px solid #a94728;background:#fbf5f2;padding:10px 12px;font-family:'STIX Two Math','Cambria Math',serif}.canonical-complexity-app .canonical-app__reference strong{font-family:sans-serif;font-size:13px}.canonical-complexity-app .canonical-app__simulation{border:1px solid #dedede;border-top:4px solid #a94728;background:#fff;margin-top:16px;padding:18px}.canonical-complexity-app .canonical-app__simulation-header,.canonical-complexity-app .canonical-app__results header{display:flex;justify-content:space-between;align-items:flex-start;gap:18px;margin-bottom:14px}.canonical-complexity-app .canonical-app__simulation-header>div>span,.canonical-complexity-app .canonical-app__results header span{color:#a94728;font-size:11px;font-weight:800;letter-spacing:.09em;text-transform:uppercase}.canonical-complexity-app h3{font-size:18px;margin:3px 0 0}.canonical-complexity-app .canonical-app__current{border-left:3px solid #a94728;padding-left:12px;text-align:right}.canonical-complexity-app .canonical-app__current small{display:block;color:#666;font-size:12px}.canonical-complexity-app .canonical-app__current strong{display:block;font:20px 'STIX Two Math','Cambria Math',serif;margin-top:3px}.canonical-complexity-app .canonical-app__unified{display:grid;grid-template-columns:minmax(0,1.18fr) minmax(360px,.82fr);gap:16px}.canonical-complexity-app .canonical-app__view{border:1px solid #e1e1e1;background:#fff;padding:8px 10px 12px;min-width:0}.canonical-complexity-app .canonical-app__view>h4{text-align:center;margin:4px 0 2px;font-size:15px}.canonical-complexity-app .canonical-app__chart{display:block;width:100%;max-height:430px}.canonical-complexity-app .canonical-app__plot-bg{fill:#fcfcfc;stroke:#ddd}.canonical-complexity-app .canonical-app__axis{stroke:#555;stroke-width:1.3}.canonical-complexity-app .canonical-app__x-tick line{stroke:#555}.canonical-complexity-app .canonical-app__x-tick text,.canonical-complexity-app .canonical-app__y-grid text{fill:#555;font:13px 'STIX Two Math','Cambria Math',serif}.canonical-complexity-app .canonical-app__y-grid line{stroke:#e6e6e6}.canonical-complexity-app .canonical-app__axis-title{fill:#222;font:600 17px 'STIX Two Math','Cambria Math',serif}.canonical-complexity-app .canonical-app__curve{fill:none;stroke-width:2.5;stroke-linecap:round;stroke-linejoin:round}.canonical-complexity-app .canonical-app__point{stroke:#fff;stroke-width:1}.canonical-complexity-app .canonical-app__race-view{overflow:hidden}.canonical-complexity-app .canonical-app__race{position:relative;height:336px;margin-top:12px}.canonical-complexity-app .canonical-app__race-row{position:absolute;inset:0 0 auto 0;height:36px;display:grid;grid-template-columns:24px 100px minmax(70px,1fr) 104px;gap:8px;align-items:center;transition:transform .18s linear}.canonical-complexity-app .canonical-app__rank{color:#777;font-weight:700;text-align:center}.canonical-complexity-app .canonical-app__race-formula{color:var(--series-color);font:600 16px 'STIX Two Math','Cambria Math',serif;text-align:right;padding-right:4px}.canonical-complexity-app .canonical-app__race-track{height:20px;background:#f4f4f4;border-left:1px solid #ddd;overflow:hidden}.canonical-complexity-app .canonical-app__race-bar{display:block;width:0;height:100%;background:var(--series-color);transition:width .12s linear}.canonical-complexity-app .canonical-app__race-value{text-align:right;font:13px 'STIX Two Math','Cambria Math',serif;white-space:nowrap}.canonical-complexity-app .canonical-app__race-view>p{color:#666;font-size:11px;text-align:center;margin:4px 0 0}.canonical-complexity-app .canonical-app__milestone{margin-top:12px;padding:10px 12px;background:#fbf5f2;border-left:3px solid #a94728;font-size:13px}.canonical-complexity-app .canonical-app__results{margin-top:16px}.canonical-complexity-app .canonical-app__results header p{margin:0;text-align:right;font-family:'STIX Two Math','Cambria Math',serif}.canonical-complexity-app .canonical-app__table-wrap{width:100%;overflow-x:auto}.canonical-complexity-app table{width:100%;min-width:900px;border-collapse:collapse;font:14px 'STIX Two Math','Cambria Math',serif}.canonical-complexity-app caption{text-align:left;font-family:sans-serif;font-size:13px;font-weight:700;padding:0 0 8px}.canonical-complexity-app th,.canonical-complexity-app td{border:1px solid #c8c8c8;padding:8px 10px;text-align:center;white-space:nowrap}.canonical-complexity-app thead th{background:#ededed;font-size:15px}.canonical-complexity-app tbody th{background:#f7f7f7}.canonical-complexity-app tbody tr.is-latest th,.canonical-complexity-app tbody tr.is-latest td{background:#fff5e9}.canonical-complexity-app .canonical-app__number{font-variant-numeric:tabular-nums}.canonical-complexity-app .canonical-app__footnote{color:#666;font-size:12px;margin:10px 0 0}
@media (max-width:980px){.canonical-complexity-app .canonical-app__unified{grid-template-columns:1fr}}@media (max-width:700px){.canonical-complexity-app .canonical-app__simulation-header,.canonical-complexity-app .canonical-app__results header{display:block}.canonical-complexity-app .canonical-app__current{text-align:left;margin-top:10px}.canonical-complexity-app .canonical-app__results header p{text-align:left;margin-top:8px}.canonical-complexity-app .canonical-app__race-row{grid-template-columns:20px 88px minmax(60px,1fr) 92px}}
</style>
"""


def run_app():
    """Muestra el crecimiento canónico animado y su tabla de hitos."""

    type_input = dropdown_control(
        options=(("Temporal", "temporal"), ("Espacial", "spatial")),
        value="temporal",
        description="",
        width="188px",
    )
    constant_input = widgets.BoundedFloatText(
        value=DEFAULT_CONSTANT,
        min=0,
        max=1_000_000,
        step=1,
        description="",
        layout=widgets.Layout(width="188px"),
    )
    order_input = bounded_int_control(
        value=MAX_ORDER,
        min_value=1,
        max_value=MAX_ORDER,
        step=1,
        description="",
        width="188px",
    )
    speed_input = dropdown_control(
        options=SPEED_OPTIONS,
        value=1.0,
        description="",
        width="188px",
    )
    controls = widgets.Box(
        [
            compact_labeled_control("Tipo", type_input),
            compact_labeled_control("Constante c", constant_input),
            compact_labeled_control("Orden máximo", order_input),
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
    controls.add_class("canonical-app__controls")
    reference = widgets.HTML(value=_reference_html("temporal"), layout=widgets.Layout(width="100%"))
    configuration = widgets.VBox(
        [controls, reference],
        layout=widgets.Layout(width="100%", grid_gap="12px"),
    )
    configuration.add_class("canonical-app__configuration")
    panel = collapsible_panel(
        "Configuración",
        configuration,
        prefix="canonical-app",
        open_by_default=True,
    )
    execute_button = button_control(description="Reproducir", button_style="success", width="128px")
    pause_button = button_control(description="Pausar", button_style="", width="128px")
    finish_button = button_control(description="Finalizar", button_style="", width="128px")
    reset_button = button_control(description="Reiniciar", button_style="warning", width="128px")
    execute_button.icon, pause_button.icon = "play", "pause"
    finish_button.icon, reset_button.icon = "step-forward", "refresh"
    pause_button.disabled = finish_button.disabled = True
    app_id = f"canonical-{uuid.uuid4().hex}"
    output = widgets.HTML(
        value=_render_simulation("temporal", DEFAULT_CONSTANT, MAX_ORDER, app_id),
        layout=widgets.Layout(width="100%"),
    )
    javascript_output = widgets.Output(layout=widgets.Layout(width="0", height="0", overflow="hidden"))

    def send_javascript(source: str):
        with javascript_output:
            clear_output(wait=True)
            display(Javascript(source))

    def clear_results(*_args):
        reference.value = _reference_html(str(type_input.value))
        output.value = _render_simulation(
            str(type_input.value),
            float(constant_input.value),
            int(order_input.value),
            app_id,
        )
        pause_button.description, pause_button.icon = "Pausar", "pause"
        pause_button.disabled = finish_button.disabled = True
        send_javascript(
            _javascript_app(
                app_id,
                str(type_input.value),
                float(constant_input.value),
                int(order_input.value),
                float(speed_input.value),
                autoplay=False,
            )
        )

    def execute(*_args):
        output.value = _render_simulation(
            str(type_input.value),
            float(constant_input.value),
            int(order_input.value),
            app_id,
        )
        pause_button.description, pause_button.icon = "Pausar", "pause"
        pause_button.disabled = finish_button.disabled = False
        send_javascript(
            _javascript_app(
                app_id,
                str(type_input.value),
                float(constant_input.value),
                int(order_input.value),
                float(speed_input.value),
            )
        )

    def pause(*_args):
        send_javascript(
            f"var paused=window.__canonicalComplexityApps?.[{json.dumps(app_id)}]?.pause?.();"
        )
        if pause_button.description == "Pausar":
            pause_button.description, pause_button.icon = "Reproducir", "play"
        else:
            pause_button.description, pause_button.icon = "Pausar", "pause"

    def finish(*_args):
        send_javascript(
            f"window.__canonicalComplexityApps?.[{json.dumps(app_id)}]?.finish?.();"
        )
        pause_button.disabled = finish_button.disabled = True

    def reset(*_args):
        type_input.value = "temporal"
        constant_input.value = DEFAULT_CONSTANT
        order_input.value = MAX_ORDER
        speed_input.value = 1.0
        clear_results()

    type_input.observe(lambda change: clear_results() if change.get("name") == "value" else None, names="value")
    constant_input.observe(lambda change: clear_results() if change.get("name") == "value" else None, names="value")
    order_input.observe(lambda change: clear_results() if change.get("name") == "value" else None, names="value")
    speed_input.observe(lambda change: clear_results() if change.get("name") == "value" else None, names="value")
    execute_button.on_click(execute)
    pause_button.on_click(pause)
    finish_button.on_click(finish)
    reset_button.on_click(reset)
    root = widgets.VBox(
        [
            widgets.HTML(value=_styles(), layout=widgets.Layout(width="0", height="0", margin="0")),
            panel,
            action_button_row([execute_button, pause_button, finish_button, reset_button]),
            output,
            javascript_output,
        ],
        layout=widgets.Layout(width="100%", grid_gap="0", overflow="visible"),
    )
    root.add_class("canonical-complexity-app")
    display(root)
    send_javascript(
        _javascript_app(
            app_id,
            "temporal",
            DEFAULT_CONSTANT,
            MAX_ORDER,
            1.0,
            autoplay=False,
        )
    )
    return root


__all__ = [
    "DEFAULT_CONSTANT",
    "BASE_SECONDS_PER_ORDER",
    "FAMILIES",
    "FAMILY_COLORS",
    "MAX_ORDER",
    "SPEED_OPTIONS",
    "SPATIAL_FACTOR",
    "TEMPORAL_FACTOR",
    "_javascript_app",
    "_render_simulation",
    "_render_table",
    "_result_log",
    "_scientific_html",
    "run_app",
]
