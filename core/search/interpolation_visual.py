from __future__ import annotations

import math
import random
from pathlib import Path

import matplotlib.pyplot as plt
from IPython.display import HTML, Math, display
import ipywidgets as widgets
from common.graphics import graphics_path
from common.simulation_views import standard_view_styles


ARRAY_SIZE = 10
GRAPH_PATH = graphics_path("capitulo7", "interpolacion", "formula_interpolacion.png")
GENERAL_GRAPH_PATH = graphics_path("capitulo7", "interpolacion", "formula_interpolacion_general.png")


plt.style.use("default")
plt.rcParams["figure.facecolor"] = "white"
plt.rcParams["axes.facecolor"] = "white"
plt.rcParams["savefig.facecolor"] = "white"
plt.rcParams["savefig.edgecolor"] = "white"
plt.rcParams["figure.dpi"] = 500
plt.rcParams["savefig.dpi"] = 500


def generate_uniform_values(size=ARRAY_SIZE):
    start = random.randint(0, 12)
    step = random.randint(7, 13)
    return [start + step * index for index in range(size)]


def generate_non_uniform_values(size=ARRAY_SIZE):
    start = random.randint(0, 8)
    increments = [random.randint(1, 5)]
    for index in range(1, size):
        increments.append(increments[-1] + random.randint(1, 6) + index // 2)

    values = [start]
    for increment in increments:
        values.append(values[-1] + increment)
    return values[:size]


def generate_values(uniform=True):
    return generate_uniform_values() if uniform else generate_non_uniform_values()


def estimate_position(values, target):
    low = 0
    high = len(values) - 1
    x0 = values[low]
    x1 = values[high]
    y0 = low
    y1 = high
    if x1 == x0:
        return x0, x1, y0, y1, 0.0
    estimate = y0 + ((y1 - y0) * (target - x0)) / (x1 - x0)
    return x0, x1, y0, y1, estimate


def nearest_index(values, target):
    return min(range(len(values)), key=lambda index: abs(values[index] - target))


def save_figure(fig, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight", pad_inches=.05)


def draw_general_formula_visual():
    x0, y0 = 2.0, 1.0
    x1, y1 = 8.0, 5.0
    x = 5.0
    y = y0 + ((y1 - y0) * (x - x0)) / (x1 - x0)
    label_box = {"boxstyle": "round,pad=0.2", "facecolor": "white", "edgecolor": "none", "alpha": 0.9}

    display(Math(r"y = y_0 + \frac{(y_1 - y_0)(x - x_0)}{x_1 - x_0}"))
    display(HTML("<div style='height: 18px;'></div>"))

    fig, ax = plt.subplots(figsize=(8, 4), dpi=500, facecolor="white")
    ax.set_facecolor("white")
    ax.plot([x0, x1], [y0, y1], color="#1565C0", linewidth=2.8)
    ax.scatter(
        [x0, x1, x],
        [y0, y1, y],
        s=[115, 115, 150],
        color=["#ffffff", "#ffffff", "#E8F5E9"],
        edgecolor=["#1565C0", "#1565C0", "#2E7D32"],
        linewidth=2.2,
        zorder=4,
    )
    ax.vlines(x0, 0, y0, color="#78909C", linestyle=":", linewidth=1.7)
    ax.hlines(y0, 0, x0, color="#78909C", linestyle=":", linewidth=1.7)
    ax.vlines(x1, 0, y1, color="#78909C", linestyle=":", linewidth=1.7)
    ax.hlines(y1, 0, x1, color="#78909C", linestyle=":", linewidth=1.7)
    ax.vlines(x, 0, y, color="#2E7D32", linestyle="--", linewidth=1.6)
    ax.hlines(y, 0, x, color="#2E7D32", linestyle="--", linewidth=1.6)

    ax.annotate(r"$(x_0, y_0)$", (x0, y0), textcoords="offset points", xytext=(8, -20), fontsize=12, bbox=label_box)
    ax.annotate(r"$(x_1, y_1)$", (x1, y1), textcoords="offset points", xytext=(8, -20), fontsize=12, bbox=label_box)
    ax.annotate(r"$(x, y)$", (x, y), textcoords="offset points", xytext=(8, -20), fontsize=12, color="#1B5E20", bbox=label_box)

    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xlim(0, 9.2)
    ax.set_ylim(0, 5.8)
    ax.tick_params(axis="both", which="major", pad=5)
    ax.grid(True, linestyle="--", linewidth=0.6, color="#b8b8b8", alpha=0.7)
    plt.tight_layout()
    save_figure(fig, GENERAL_GRAPH_PATH)
    plt.show()


def run_general_formula_visual():
    draw_general_formula_visual()


def draw_interpolation_visual(values, target, uniform=True):
    x0, x1, y0, y1, estimate = estimate_position(values, target)
    clamped_estimate = max(0, min(len(values) - 1, estimate))
    distribution_label = "uniforme" if uniform else "no uniforme"

    display(Math(rf"arr = \left[{', '.join(str(value) for value in values)}\right]"))
    display(HTML("<div style='height: 12px;'></div>"))
    display(Math(r"y = y_0 + \frac{(y_1 - y_0)(x - x_0)}{x_1 - x_0}"))
    display(HTML("<div style='height: 12px;'></div>"))
    display(Math(
        rf"y = {y0} + \frac{{({y1} - {y0})({target:.2f} - {x0})}}{{{x1} - {x0}}}"
        rf" = {estimate:.2f}"
    ))
    display(HTML("<div style='height: 30px;'></div>"))

    fig, ax = plt.subplots(figsize=(10.5, 5.8), dpi=500, facecolor="white")
    ax.set_facecolor("white")
    positions = list(range(len(values)))

    line_color = "#1565C0" if uniform else "#6A1B9A"
    ax.plot(values, positions, color=line_color, linewidth=2.4, label=f"Datos con distribución {distribution_label}")
    ax.scatter(values, positions, s=95, color="#ffffff", edgecolor=line_color, linewidth=2.2, zorder=3)
    ax.scatter([target], [clamped_estimate], s=170, color="#E8F5E9", edgecolor="#2E7D32", linewidth=2.4, zorder=5)
    ax.scatter(
        [x0, x1],
        [y0, y1],
        s=145,
        color="#FFF2CC",
        edgecolor="#D6B656",
        linewidth=2.2,
        zorder=4,
        label="Puntos de referencia",
    )
    ax.axvline(target, color="#2E7D32", linestyle="--", linewidth=1.6)
    ax.axhline(clamped_estimate, color="#2E7D32", linestyle="--", linewidth=1.6)

    for value, position in zip(values, positions):
        ax.annotate(
            f"{value}",
            (value, position),
            textcoords="offset points",
            xytext=(0, 8),
            ha="center",
            fontsize=10,
        )

    ax.annotate(
        f"y calculado = {estimate:.2f}",
        (target, clamped_estimate),
        textcoords="offset points",
        xytext=(12, -26),
        fontsize=11,
        color="#1B5E20",
    )

    ax.set_title(
        f"Cálculo de y por interpolación lineal ({distribution_label})",
        fontsize=13,
    )
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticks(values)
    ax.set_yticks(positions)
    ax.grid(True, linestyle="--", linewidth=0.6, color="#b8b8b8", alpha=0.7)
    ax.legend(loc="upper left")
    padding = max(4, (max(values) - min(values)) * 0.05)
    ax.set_xlim(min(values) - padding, max(values) + padding)
    ax.set_ylim(-0.7, len(values) - 0.3)
    plt.tight_layout()
    save_figure(fig, GRAPH_PATH)
    plt.show()


def run_interpolation_visual():
    _HTML = standard_view_styles("#iv-wrap") + r"""
<style>
#iv-wrap{width:100%;max-width:100%;overflow-x:hidden;background:#ffffff;color:#333;
  padding:14px 4px;font-family:sans-serif;box-sizing:border-box}
#iv-wrap,#iv-wrap *{box-sizing:border-box}
#iv-wrap label,#iv-wrap .label-text,#iv-wrap .stepper-field,#iv-wrap .range-value,
#iv-wrap .card,#iv-wrap .fml{color:#333}
#iv-wrap .iv-main-panel{width:100%;border:0;border-radius:0;
  overflow:hidden;background:#fff}
#iv-wrap .iv-panel-title,#iv-wrap .iv-subpanel-title{width:100%;margin:0;padding:10px 14px;
  border-bottom:1px solid #e2e2e2;background:#f7f7f7;color:#333;font-weight:700;
  line-height:1.35;text-align:left}
#iv-wrap .iv-panel-body{width:100%;padding:0;background:#fff}
#iv-wrap .iv-subpanel{width:100%;margin:0;border:1px solid #dedede;background:#fff}
#iv-wrap .iv-subpanel:first-child{border-radius:5px 5px 0 0}
#iv-wrap .iv-subpanel:last-child{border-radius:0 0 5px 5px}
#iv-wrap .iv-subpanel+.iv-subpanel{border-top:0}
#iv-wrap .iv-subpanel-title{padding:8px 12px;border-bottom-color:#e5e5e5}
#iv-wrap summary.iv-subpanel-title{box-sizing:border-box;cursor:pointer;list-style-position:inside}
#iv-wrap .iv-panel-content{width:100%;padding:12px;background:#fff}
#iv-wrap .plot-wrap{position:relative;width:100%;height:390px}
#iv-wrap canvas{display:block;width:100%;height:390px;
  background:#ffffff;border:1px solid #e0e0e0;touch-action:none}
#iv-wrap .plot-label{position:absolute;z-index:2;pointer-events:none;transform:translate(-50%,-100%);
  padding:2px 5px;border:1px solid transparent;background:transparent;white-space:nowrap;
  font-size:13px;line-height:1}
#iv-wrap .function-label{left:68px;top:12px;transform:none;color:#1565C0}
#iv-wrap .ctrl{display:flex;column-gap:36px;row-gap:12px;flex-wrap:wrap;margin:0 0 12px;
  align-items:center;font-size:13px;color:#333}
#iv-wrap .ctrl label{display:flex;align-items:center;gap:8px;color:#333;font-family:sans-serif;font-size:13px;font-weight:700;line-height:1.1;min-height:32px}
#iv-wrap .ctrl label mjx-container{font-size:100%!important;font-weight:700!important}
#iv-wrap .label-text{display:inline-flex;align-items:center;justify-content:center;
  width:96px;min-width:96px;text-align:left}
#iv-wrap select,#iv-wrap input[type=number]{width:188px;height:32px;box-sizing:border-box;
  padding:2px 6px;border:1px solid #ccc;border-radius:3px;background:#fff;
  color:#333;font-size:13px;text-align:center}
#iv-wrap input[type=number]:focus,#iv-wrap select:focus{outline:none;border-color:#1976D2;
  box-shadow:0 0 0 1px #1976D2}
#iv-wrap .stepper{display:inline-grid;grid-template-columns:34px 120px 34px;
  gap:0;align-items:center}
#iv-wrap .stepper-field{display:flex;align-items:center;justify-content:center;width:120px;
  height:32px;box-sizing:border-box;border:1px solid #ccc;border-radius:0;
  background:#fff;text-align:center;font-size:14px;font-weight:400;white-space:nowrap}
#iv-wrap button{width:34px;height:32px;border:1px solid #ccc;border-radius:0;
  background:#f7f7f7;color:#333;box-shadow:none;cursor:pointer;
  font-family:sans-serif;font-size:13px;line-height:1;margin:0}
#iv-wrap button:hover{background:#eee}
#iv-wrap button:disabled{background:#f7f7f7;color:#333;cursor:not-allowed;opacity:.45}
#iv-wrap .stepper button{border-color:#ccc;border-radius:0;margin:0;padding:0}
#iv-wrap button.active{background:#f7f7f7;border-color:#ccc;color:#333}
#iv-wrap button:focus-visible{outline:2px solid #1976D2;outline-offset:1px}
#iv-wrap .range-field{display:grid;grid-template-columns:96px 126px 54px;gap:8px;
  align-items:center}
#iv-wrap input[type=range]{width:126px;margin:0;accent-color:#1976D2;cursor:pointer}
#iv-wrap .range-value{display:flex;align-items:center;justify-content:center;width:54px;
  height:32px;box-sizing:border-box;border:1px solid #ccc;border-radius:3px;
  background:#fff;font-weight:400}
#iv-wrap .ctrl .sep{display:none}
#iv-wrap .action-buttons{display:flex;width:100%;gap:0;margin:16px 0 0;padding:0;
  justify-content:flex-end;align-items:center}
#iv-wrap .action-buttons button{display:inline-flex;align-items:center;justify-content:center;
  gap:6px;width:auto;min-width:150px;height:38px;padding:0 12px;
  border-color:#ccc;border-radius:0;margin:0;font-size:14px}
#iv-wrap .action-buttons .button-icon{display:inline-flex;width:14px;align-items:center;
  justify-content:center;font-family:sans-serif;font-size:14px;line-height:1}
#iv-wrap .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:10px;margin-top:12px}
#iv-wrap .card{background:#f7f7f7;border:1px solid #e8e8e8;border-radius:4px;padding:10px 14px}
#iv-wrap .card .lbl{font-size:12px;color:#555;margin-bottom:5px}
#iv-wrap .card .val{font-size:16px;font-weight:600;min-height:25px}
#iv-wrap .fml{margin-top:10px;background:#f7f7f7;border:1px solid #e8e8e8;
  border-radius:4px;padding:10px 20px;font-size:15px;color:#333;min-height:52px;
  display:flex;align-items:center;justify-content:center;gap:6px;flex-wrap:wrap}
#iv-wrap mjx-container{margin:0!important}
</style>
<div id="iv-wrap">
 <div class="iv-main-panel">
  <div class="iv-panel-body">
  <details class="iv-subpanel" open>
   <summary class="iv-subpanel-title">Configuración</summary>
   <div class="iv-panel-content">
    <div class="ctrl">
    <label><span class="label-text">\(\mathbf{f}(x)\)</span>
      <span class="stepper">
        <button type="button" id="iv-fn-dec" aria-label="Función anterior">◀</button>
        <span class="stepper-field" id="iv-fn-field">\(0.8x+1\)</span>
        <button type="button" id="iv-fn-inc" aria-label="Función siguiente">▶</button>
      </span>
      <select id="iv-fn" hidden aria-hidden="true">
        <option value="lin">0.8x + 1</option>
        <option value="sq">x² / 10</option>
        <option value="sin">5 + 4·sin(x)</option>
        <option value="sqrt">3·√x</option>
      </select>
    </label>
    <label><span class="label-text">\(\mathbf{x}_{\max}\)</span>
      <input type="number" id="iv-n" min="2" max="200" value="10" step="1">
    </label>
    </div>
    <div class="ctrl">
    <label class="range-field"><span class="label-text">\(\mathbf{x}_{0}\)</span>
      <input type="range" id="iv-s0" min="0" max="75" value="15" step="1">
      <span class="range-value" id="iv-v0">\(1.5\)</span></label>
    <div class="sep"></div>
    <label class="range-field"><span class="label-text">\(\mathbf{x}\)</span>
      <input type="range" id="iv-sx" min="15" max="85" value="50" step="1">
      <span class="range-value" id="iv-vx">\(5.0\)</span></label>
    <div class="sep"></div>
    <label class="range-field"><span class="label-text">\(\mathbf{x}_{1}\)</span>
      <input type="range" id="iv-s1" min="25" max="100" value="85" step="1">
      <span class="range-value" id="iv-v1">\(8.5\)</span></label>
    </div>
    <div class="action-buttons">
      <button type="button" id="iv-play" aria-pressed="false"><span class="button-icon" aria-hidden="true">▶</span><span class="button-label">Reproducir</span></button>
      <button type="button" id="iv-reset"><span class="button-icon" aria-hidden="true">↻</span><span class="button-label">Restablecer</span></button>
    </div>
   </div>
  </details>
  <details class="iv-subpanel" open>
   <summary class="iv-subpanel-title">Resultado</summary>
   <div class="iv-panel-content iv-result-content">
    <div class="plot-wrap" id="iv-plot">
    <canvas id="iv-cv"></canvas>
    <span class="plot-label function-label" id="iv-graph-f">\(f(x)=0.8x+1\)</span>
    <span class="plot-label" id="iv-label-p0">\((x_0,y_0)\)</span>
    <span class="plot-label" id="iv-label-p1">\((x_1,y_1)\)</span>
    <span class="plot-label" id="iv-label-real">\((x,f(x))\)</span>
    </div>
    <div class="cards">
    <div class="card"><div class="lbl">Valor seleccionado</div>
      <div class="val" id="iv-dx" style="color:#333">—</div></div>
    <div class="card"><div class="lbl">Posición estimada</div>
      <div class="val" id="iv-di" style="color:#B71C1C">—</div></div>
    <div class="card"><div class="lbl">Posición real \(f(x)\)</div>
      <div class="val" id="iv-dt" style="color:#1B5E20">—</div></div>
    <div class="card"><div class="lbl">Error absoluto</div>
      <div class="val" id="iv-erra" style="color:#E65100">—</div></div>
    <div class="card"><div class="lbl">Error relativo</div>
      <div class="val" id="iv-err" style="color:#E65100">—</div></div>
    </div>
    <div class="fml" id="iv-fml-vals" style="display:none"></div>
   </div>
  </details>
  </div>
 </div>
</div>
<script>
(function(){
  var root=document.getElementById('iv-wrap');
  var cv=document.getElementById('iv-cv'),ctx=cv.getContext('2d');
  var XD=[0,10],YD=[-0.5,12.5],PAD,W,H,selX=5.0,dragPoint=null;
  var playTimer=null,lastMathUpdate=0,mathUpdateDelay=45;
  var dynamicMathState={};
  if(!window.__interpolationMathJaxReady){
    window.__interpolationMathJaxReady=new Promise(function(resolve,reject){
      if(window.MathJax && MathJax.typesetPromise){resolve(window.MathJax);return;}
      window.MathJax={
        tex:{
          inlineMath:[['\\\\(','\\\\)']],
          displayMath:[['\\\\[','\\\\]']],
          processEscapes:true
        },
        svg:{fontCache:'none'},
        startup:{typeset:false}
      };
      var script=document.createElement('script');
      script.src='https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js';
      script.async=true;
      script.onload=function(){
        var startup=window.MathJax && MathJax.startup && MathJax.startup.promise;
        Promise.resolve(startup).then(function(){resolve(window.MathJax);},reject);
      };
      script.onerror=function(){reject(new Error('No fue posible cargar MathJax.'));};
      document.head.appendChild(script);
    });
  }
  var interpolationMathReady=window.__interpolationMathJaxReady.then(function(mathJax){
    return mathJax.typesetPromise([root]).then(function(){return mathJax;});
  });
  function renderDynamicMath(id,latex,display){
    var state=dynamicMathState[id]||(dynamicMathState[id]={running:false,pending:null});
    state.pending={latex:latex,display:!!display};
    if(state.running)return;
    state.running=true;
    var requested=state.pending;state.pending=null;
    interpolationMathReady.then(function(mathJax){
      return mathJax.tex2svgPromise(requested.latex,{display:requested.display});
    }).then(function(rendered){
      var node=document.getElementById(id);
      if(rendered && node && state.pending===null)node.replaceChildren(rendered);
    }).catch(function(error){
      console.error('No fue posible actualizar la expresión de interpolación.',error);
    }).finally(function(){
      state.running=false;
      if(state.pending!==null)renderDynamicMath(id,state.pending.latex,state.pending.display);
    });
  }
  var FN_KEYS=['lin','sq','sin','sqrt'];
  var FNS={
    lin: {fn:function(x){return 0.8*x+1;},       lbl:'f(x) = 0.8x + 1',latex:'0.8x+1'},
    sq:  {fn:function(x){return x*x/10;},         lbl:'f(x) = x² / 10',latex:'\\\\dfrac{x^2}{10}'},
    sin: {fn:function(x){return 5+4*Math.sin(x);},lbl:'f(x) = 5 + 4·sin(x)',latex:'5+4\\\\cdot\\\\sin(x)'},
    sqrt:{fn:function(x){return 3*Math.sqrt(x);}, lbl:'f(x) = 3·√x',latex:'3\\\\sqrt{x}'}
  };
  function stepFunction(direction){
    var select=document.getElementById('iv-fn');
    var index=FN_KEYS.indexOf(select.value);
    select.value=FN_KEYS[(index+direction+FN_KEYS.length)%FN_KEYS.length];
    renderDynamicMath('iv-fn-field',FNS[select.value].latex,false);
    renderDynamicMath('iv-graph-f','f(x)='+FNS[select.value].latex,false);
    draw();
  }
  function getN(){return Math.max(2,parseFloat(document.getElementById('iv-n').value)||10);}
  function resize(){
    var r=cv.getBoundingClientRect(),dpr=window.devicePixelRatio||1;
    cv.width=r.width*dpr; cv.height=r.height*dpr;
    ctx.setTransform(dpr,0,0,dpr,0,0);
    W=r.width; H=r.height; PAD={l:58,r:28,t:36,b:46};
  }
  function niceTicks(lo,hi,count){
    var range=hi-lo,step=Math.pow(10,Math.floor(Math.log10(range/count)));
    var steps=[1,2,5,10];
    for(var i=0;i<steps.length;i++){
      if(range/(step*steps[i])<=count+1){step*=steps[i];break;}
    }
    var ticks=[];
    var start=Math.ceil(lo/step)*step;
    for(var v=start;v<=hi+1e-9;v+=step) ticks.push(parseFloat(v.toFixed(10)));
    return ticks;
  }
  function computeYD(fn,xd){
    var mn=Infinity,mx=-Infinity;
    for(var i=0;i<=200;i++){
      var v=fn(xd[0]+i/200*(xd[1]-xd[0]));
      if(v<mn)mn=v; if(v>mx)mx=v;
    }
    var pad=(mx-mn)*0.12;
    return [mn-pad, mx+pad];
  }
  function tc(x,y){
    return [PAD.l+(x-XD[0])/(XD[1]-XD[0])*(W-PAD.l-PAD.r),
            H-PAD.b-(y-YD[0])/(YD[1]-YD[0])*(H-PAD.t-PAD.b)];
  }
  function fc(cx){return XD[0]+(cx-PAD.l)/(W-PAD.l-PAD.r)*(XD[1]-XD[0]);}
  function gs(){
    var k=document.getElementById('iv-fn').value;
    var n=getN(); XD=[0,n];
    var x0=parseFloat(document.getElementById('iv-s0').value)/10;
    var x1=parseFloat(document.getElementById('iv-s1').value)/10;
    x0=Math.min(x0,n); x1=Math.min(x1,n);
    var fn=FNS[k].fn;
    YD=computeYD(fn,XD);
    return {fn:fn,lbl:FNS[k].lbl,x0:Math.min(x0,x1),x1:Math.max(x0,x1)};
  }
  function nearPoint(ex,ey,px,py){
    var c=tc(px,py),dx=ex-c[0],dy=ey-c[1];
    return Math.sqrt(dx*dx+dy*dy)<14;
  }
  function setSlider(id,val,dispId){
    var el=document.getElementById(id);
    el.value=Math.round(val*10);
    renderDynamicMath(dispId,val.toFixed(1),false);
  }
  function setXSlider(val){
    var el=document.getElementById('iv-sx');
    el.value=Math.round(val*10);
    renderDynamicMath('iv-vx',val.toFixed(1),false);
  }
  function updateXSliderBounds(x0,x1){
    var el=document.getElementById('iv-sx');
    el.min=Math.round(x0*10); el.max=Math.round(x1*10);
    if(parseFloat(el.value)<parseFloat(el.min))el.value=el.min;
    if(parseFloat(el.value)>parseFloat(el.max))el.value=el.max;
    renderDynamicMath('iv-vx',(parseFloat(el.value)/10).toFixed(1),false);
    return parseFloat(el.value)/10;
  }
  function resetCards(){
    ['iv-dx','iv-di','iv-dt','iv-erra','iv-err'].forEach(function(k){
      renderDynamicMath(k,'\\\\text{—}',false);
    });
    document.getElementById('iv-fml-vals').style.display='none';
  }
  function placePlotLabel(id,cx,cy){
    var node=document.getElementById(id);
    node.style.left=cx+'px';node.style.top=(cy-10)+'px';
    node.style.transform='translate(-50%,-100%)';
  }
  function updateMathResults(y0,y1,yi,yt,err,errPct,x0,x1,force){
    var now=performance.now();
    if(!force && now-lastMathUpdate<mathUpdateDelay)return;
    lastMathUpdate=now;
    renderDynamicMath('iv-dx','x='+selX.toFixed(3),false);
    renderDynamicMath('iv-di','y_{\\\\mathrm{est}}='+yi.toFixed(4),false);
    renderDynamicMath('iv-dt','y_{\\\\mathrm{real}}='+yt.toFixed(4),false);
    renderDynamicMath('iv-erra','E_a='+err.toFixed(4),false);
    renderDynamicMath('iv-err','E_r='+errPct.toFixed(2)+'\\\\%',false);
    document.getElementById('iv-fml-vals').style.display='flex';
    renderDynamicMath('iv-fml-vals',
      '\\\\begin{aligned}'+
      'y &=y_0+\\\\dfrac{(y_1-y_0)(x-x_0)}{x_1-x_0}\\\\\\\\[4pt]'+
      '&='+y0.toFixed(3)+'+\\\\dfrac{('+(y1-y0).toFixed(3)+')('+
      (selX-x0).toFixed(3)+')}{'+(x1-x0).toFixed(3)+'}\\\\\\\\[4pt]'+
      '&='+y0.toFixed(3)+'+\\\\dfrac{'+((y1-y0)*(selX-x0)).toFixed(4)+
      '}{'+(x1-x0).toFixed(3)+'}\\\\\\\\[4pt]'+
      '&='+yi.toFixed(4)+
      '\\\\end{aligned}',true);
  }
  function draw(){
    ctx.clearRect(0,0,W,H);
    ctx.fillStyle='#ffffff'; ctx.fillRect(0,0,W,H);
    var s=gs(),fn=s.fn,x0=s.x0,x1=s.x1;
    var xTicks=niceTicks(XD[0],XD[1],7);
    var yTicks=niceTicks(YD[0],YD[1],6);
    /* grid */
    xTicks.forEach(function(gx){
      var p=tc(gx,YD[0]);
      ctx.strokeStyle='#b8b8b8';ctx.lineWidth=0.6;ctx.setLineDash([4,4]);
      ctx.beginPath();ctx.moveTo(p[0],PAD.t);ctx.lineTo(p[0],H-PAD.b);ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle='#666';ctx.font='11px sans-serif';ctx.textAlign='center';
      ctx.fillText(gx,p[0],H-PAD.b+15);
    });
    yTicks.forEach(function(gy){
      var q=tc(XD[0],gy);
      ctx.strokeStyle='#b8b8b8';ctx.lineWidth=0.6;ctx.setLineDash([4,4]);
      ctx.beginPath();ctx.moveTo(PAD.l,q[1]);ctx.lineTo(W-PAD.r,q[1]);ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle='#666';ctx.font='11px sans-serif';ctx.textAlign='right';
      ctx.fillText(gy,PAD.l-6,q[1]+4);
    });
    /* axes */
    var oy=tc(XD[0],Math.max(YD[0],0))[1];
    ctx.strokeStyle='#90A4AE';ctx.lineWidth=1;ctx.setLineDash([]);
    ctx.beginPath();ctx.moveTo(PAD.l,oy);ctx.lineTo(W-PAD.r,oy);ctx.stroke();
    ctx.beginPath();ctx.moveTo(PAD.l,PAD.t);ctx.lineTo(PAD.l,H-PAD.b);ctx.stroke();
    /* interval shading */
    var y0=fn(x0),y1=fn(x1);
    var cx0=tc(x0,YD[0])[0],cx1=tc(x1,YD[0])[0];
    ctx.fillStyle='rgba(21,101,192,0.05)';
    ctx.fillRect(cx0,PAD.t,cx1-cx0,H-PAD.t-PAD.b);
    /* real function */
    ctx.strokeStyle='#1565C0';ctx.lineWidth=2.4;ctx.setLineDash([]);
    ctx.beginPath();
    for(var i=0;i<=300;i++){
      var xp=XD[0]+i/300*(XD[1]-XD[0]),cp=tc(xp,fn(xp));
      if(i===0)ctx.moveTo(cp[0],cp[1]);else ctx.lineTo(cp[0],cp[1]);
    }
    ctx.stroke();
    /* interpolation line */
    var sl=(y1-y0)/(x1-x0),ext=(XD[1]-XD[0])*0.03;
    ctx.strokeStyle='#B71C1C';ctx.lineWidth=1.8;ctx.setLineDash([7,4]);
    var pa=tc(x0-ext,y0+sl*(-ext)),pb=tc(x1+ext,y1+sl*ext);
    ctx.beginPath();ctx.moveTo(pa[0],pa[1]);ctx.lineTo(pb[0],pb[1]);
    ctx.stroke();ctx.setLineDash([]);
    /* reference points — draggable */
    [[x0,y0,0],[x1,y1,1]].forEach(function(pt){
      var c=tc(pt[0],pt[1]);
      var isActive=(dragPoint==='p'+pt[2]);
      var pointColor=pt[2]===0?'#1565C0':'#6A1B9A';
      ctx.fillStyle=pt[2]===0?'#E3F2FD':'#F3E5F5';
      ctx.strokeStyle=isActive?'#E65100':pointColor;
      ctx.lineWidth=isActive?2.8:2.2;
      ctx.beginPath();ctx.arc(c[0],c[1],isActive?9:7,0,Math.PI*2);ctx.fill();ctx.stroke();
      var label=document.getElementById(pt[2]===0?'iv-label-p0':'iv-label-p1');
      label.style.color=pointColor;
      placePlotLabel(label.id,c[0],c[1]);
    });
    /* selected point */
    if(selX!==null){
      var yi=y0+(y1-y0)*(selX-x0)/(x1-x0),yt=fn(selX);
      var cxS=tc(selX,YD[0])[0],cyI=tc(selX,yi)[1],cyT=tc(selX,yt)[1];
      ctx.strokeStyle='#2E7D32';ctx.lineWidth=1.6;ctx.setLineDash([4,4]);
      ctx.beginPath();ctx.moveTo(cxS,H-PAD.b);ctx.lineTo(cxS,Math.min(cyI,cyT)-8);
      ctx.stroke();ctx.setLineDash([]);
      ctx.strokeStyle='#B71C1C';ctx.lineWidth=1;ctx.setLineDash([3,3]);
      ctx.beginPath();ctx.moveTo(PAD.l,cyI);ctx.lineTo(cxS,cyI);ctx.stroke();
      ctx.setLineDash([]);
      if(Math.abs(cyI-cyT)>2){
        ctx.strokeStyle='#E65100';ctx.lineWidth=3;
        ctx.beginPath();ctx.moveTo(cxS,cyI);ctx.lineTo(cxS,cyT);ctx.stroke();
      }
      var rr=dragPoint==='sel'?10:8;
      ctx.fillStyle='#ffffff';ctx.strokeStyle='#B71C1C';ctx.lineWidth=2.4;
      ctx.beginPath();ctx.arc(cxS,cyI,rr,0,Math.PI*2);ctx.fill();ctx.stroke();
      ctx.fillStyle='#B71C1C';ctx.beginPath();ctx.arc(cxS,cyI,3.5,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='#E8F5E9';ctx.strokeStyle='#2E7D32';ctx.lineWidth=2.4;
      ctx.beginPath();ctx.arc(cxS,cyT,6,0,Math.PI*2);ctx.fill();ctx.stroke();
      var realLabel=document.getElementById('iv-label-real');
      realLabel.style.color='#2E7D32';
      placePlotLabel('iv-label-real',cxS,cyT);
      var err=Math.abs(yt-yi),errPct=yt!==0?err/Math.abs(yt)*100:0;
      updateMathResults(y0,y1,yi,yt,err,errPct,x0,x1,dragPoint===null);
    }
    /* legend — bottom right */
    var items=[
      {col:'#1565C0',dash:false,label:'f(x) real'},
      {col:'#B71C1C',dash:true, label:'Interpolación lineal'},
      {col:'#E65100',dot:true,  label:'Error'}
    ];
    var lh=24,lw=178,lx=W-PAD.r-8,ly=H-PAD.b-items.length*lh-14;
    ctx.fillStyle='rgba(255,255,255,0.92)';
    ctx.strokeStyle='#ddd';ctx.lineWidth=0.8;
    ctx.beginPath();ctx.roundRect(lx-lw,ly-8,lw,items.length*lh+16,4);
    ctx.fill();ctx.stroke();
    items.forEach(function(it,i){
      var iy=ly+i*lh+12;
      if(it.dot){
        ctx.fillStyle=it.col;
        ctx.beginPath();ctx.arc(lx-lw+14,iy,5,0,Math.PI*2);ctx.fill();
      } else {
        ctx.strokeStyle=it.col;ctx.lineWidth=2;ctx.setLineDash(it.dash?[5,3]:[]);
        ctx.beginPath();ctx.moveTo(lx-lw+4,iy);ctx.lineTo(lx-lw+24,iy);ctx.stroke();
        ctx.setLineDash([]);
      }
      ctx.fillStyle='#333';ctx.font='11px sans-serif';ctx.textAlign='left';
      ctx.fillText(it.label,lx-lw+30,iy+4);
    });
  }
  function evtCoords(e){
    var r=cv.getBoundingClientRect();
    var src=e.touches?e.touches[0]:e;
    return {cx:src.clientX-r.left, cy:src.clientY-r.top};
  }
  function clampSel(x){var s=gs();return Math.max(s.x0,Math.min(s.x1,x));}
  function inInterval(x){var s=gs();return x>=s.x0-0.3&&x<=s.x1+0.3;}
  function onDown(cx,cy){
    var s=gs(),y0=s.fn(s.x0),y1=s.fn(s.x1);
    if(nearPoint(cx,cy,s.x0,y0)){dragPoint='p0';}
    else if(nearPoint(cx,cy,s.x1,y1)){dragPoint='p1';}
    else if(inInterval(fc(cx))){dragPoint='sel';selX=clampSel(fc(cx));setXSlider(selX);}
    draw();
  }
  function onMove(cx,cy){
    var s=gs(),x=fc(cx);
    if(dragPoint==='p0'){
      var newX=Math.max(XD[0],Math.min(s.x1-0.5,x));
      setSlider('iv-s0',newX,'iv-v0');
      selX=updateXSliderBounds(newX,s.x1);
      draw();
    } else if(dragPoint==='p1'){
      var newX=Math.max(s.x0+0.5,Math.min(XD[1],x));
      setSlider('iv-s1',newX,'iv-v1');
      selX=updateXSliderBounds(s.x0,newX);
      draw();
    } else if(dragPoint==='sel'){
      selX=clampSel(x);setXSlider(selX); draw();
    } else {
      var y0=s.fn(s.x0),y1=s.fn(s.x1);
      if(nearPoint(cx,cy,s.x0,y0)||nearPoint(cx,cy,s.x1,y1)) cv.style.cursor='grab';
      else if(inInterval(x)) cv.style.cursor='ew-resize';
      else cv.style.cursor='default';
    }
  }
  function onUp(){dragPoint=null;lastMathUpdate=0;draw();}
  function stopPlayback(){
    if(playTimer!==null){clearInterval(playTimer);playTimer=null;}
    var button=document.getElementById('iv-play');
    button.classList.remove('active');button.setAttribute('aria-pressed','false');
    button.innerHTML='<span class="button-icon" aria-hidden="true">▶</span><span class="button-label">Reproducir</span>';
  }
  function togglePlayback(){
    if(playTimer!==null){stopPlayback();return;}
    var button=document.getElementById('iv-play');
    button.classList.add('active');button.setAttribute('aria-pressed','true');
    button.innerHTML='<span class="button-icon" aria-hidden="true">❚❚</span><span class="button-label">Pausar</span>';
    playTimer=setInterval(function(){
      var s=gs(),step=Math.max((s.x1-s.x0)/120,0.01);
      selX+=step;
      if(selX>s.x1)selX=s.x0;
      setXSlider(selX);draw();
    },32);
  }
  function resetSimulation(){
    stopPlayback();
    document.getElementById('iv-fn').value='lin';
    document.getElementById('iv-n').value='10';
    document.getElementById('iv-s0').value='15';
    document.getElementById('iv-s0').max='75';
    document.getElementById('iv-s1').value='85';
    document.getElementById('iv-s1').max='100';
    document.getElementById('iv-sx').min='15';
    document.getElementById('iv-sx').max='85';
    document.getElementById('iv-sx').value='50';
    selX=5;dragPoint=null;lastMathUpdate=0;
    renderDynamicMath('iv-fn-field',FNS.lin.latex,false);
    renderDynamicMath('iv-graph-f','f(x)='+FNS.lin.latex,false);
    renderDynamicMath('iv-v0','1.5',false);
    renderDynamicMath('iv-vx','5.0',false);
    renderDynamicMath('iv-v1','8.5',false);
    draw();
  }
  cv.addEventListener('mousedown',function(e){var c=evtCoords(e);onDown(c.cx,c.cy);});
  cv.addEventListener('mousemove',function(e){var c=evtCoords(e);onMove(c.cx,c.cy);});
  cv.addEventListener('mouseup',onUp);
  cv.addEventListener('mouseleave',function(){dragPoint=null;});
  cv.addEventListener('touchstart',function(e){e.preventDefault();var c=evtCoords(e);onDown(c.cx,c.cy);},{passive:false});
  cv.addEventListener('touchmove',function(e){e.preventDefault();var c=evtCoords(e);onMove(c.cx,c.cy);},{passive:false});
  cv.addEventListener('touchend',function(){onUp();},{passive:false});
  document.getElementById('iv-fn-dec').addEventListener('click',function(){stepFunction(-1);});
  document.getElementById('iv-fn-inc').addEventListener('click',function(){stepFunction(1);});
  document.getElementById('iv-play').addEventListener('click',togglePlayback);
  document.getElementById('iv-reset').addEventListener('click',resetSimulation);
  document.getElementById('iv-s0').addEventListener('input',function(){
    var x0=parseFloat(document.getElementById('iv-s0').value)/10;
    var x1=parseFloat(document.getElementById('iv-s1').value)/10;
    renderDynamicMath('iv-v0',x0.toFixed(1),false);
    selX=updateXSliderBounds(x0,x1); draw();
  });
  document.getElementById('iv-s1').addEventListener('input',function(){
    var x0=parseFloat(document.getElementById('iv-s0').value)/10;
    var x1=parseFloat(document.getElementById('iv-s1').value)/10;
    renderDynamicMath('iv-v1',x1.toFixed(1),false);
    selX=updateXSliderBounds(x0,x1); draw();
  });
  document.getElementById('iv-sx').addEventListener('input',function(){
    selX=parseFloat(document.getElementById('iv-sx').value)/10;
    renderDynamicMath('iv-vx',selX.toFixed(1),false);
    draw();
  });
  document.getElementById('iv-n').addEventListener('change',function(){
    var n=getN();
    var fn=FNS[document.getElementById('iv-fn').value].fn;
    var s0=document.getElementById('iv-s0'),s1=document.getElementById('iv-s1');
    s0.max=Math.round((n-0.5)*10); s1.max=Math.round(n*10);
    /* reset extremes to f(0) and f(n) */
    s0.value=0; s1.value=Math.round(n*10);
    renderDynamicMath('iv-v0',(0).toFixed(1),false);
    renderDynamicMath('iv-v1',n.toFixed(1),false);
    selX=updateXSliderBounds(0,n);
    draw();
  });
  window.addEventListener('resize',function(){resize();draw();});
  resize();draw();
})();
</script>
"""
    display(HTML(_HTML))


__all__ = [
    "ARRAY_SIZE",
    "GRAPH_PATH",
    "GENERAL_GRAPH_PATH",
    "draw_interpolation_visual",
    "draw_general_formula_visual",
    "estimate_position",
    "generate_non_uniform_values",
    "generate_uniform_values",
    "generate_values",
    "run_interpolation_visual",
    "run_general_formula_visual",
]
