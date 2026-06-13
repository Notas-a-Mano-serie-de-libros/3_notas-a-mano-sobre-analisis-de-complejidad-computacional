from __future__ import annotations

import math
import random
from pathlib import Path

import matplotlib.pyplot as plt
from IPython.display import HTML, Math, display
import ipywidgets as widgets


ARRAY_SIZE = 10
GRAPH_PATH = Path("graficas") / "formula_interpolacion.png"
GENERAL_GRAPH_PATH = Path("graficas") / "formula_interpolacion_general.png"


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
    _HTML = """
<style>
#iv-wrap{background:#ffffff;font-family:sans-serif;padding:14px 4px}
#iv-wrap canvas{display:block;width:100%;height:340px;
  background:#ffffff;border:1px solid #e0e0e0;touch-action:none}
#iv-wrap .ctrl{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:8px;
  align-items:center;font-size:13px;color:#333}
#iv-wrap .ctrl label{display:flex;align-items:center;gap:6px}
#iv-wrap .ctrl input[type=number]{width:52px;padding:2px 4px;border:1px solid #ccc;
  border-radius:3px;font-size:13px;text-align:center}
#iv-wrap .ctrl .sep{width:1px;height:20px;background:#ddd;margin:0 2px}
#iv-wrap .cards{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:12px}
#iv-wrap .card{background:#f7f7f7;border:1px solid #e8e8e8;border-radius:4px;padding:10px 14px}
#iv-wrap .card .lbl{font-size:11px;color:#78909C;margin-bottom:3px}
#iv-wrap .card .val{font-size:16px;font-weight:600}
#iv-wrap .fml{margin-top:10px;background:#f7f7f7;border:1px solid #e8e8e8;
  border-radius:4px;padding:10px 20px;font-size:15px;color:#333;min-height:52px;
  display:flex;align-items:center;justify-content:center;gap:6px;flex-wrap:wrap}
#iv-wrap .frac{display:inline-flex;flex-direction:column;align-items:center;
  vertical-align:middle;margin:0 4px;line-height:1.25}
#iv-wrap .frac .num{border-bottom:1.5px solid #333;padding:0 5px 3px;white-space:nowrap}
#iv-wrap .frac .den{padding:3px 5px 0;white-space:nowrap}
</style>
<div id="iv-wrap">
  <div class="ctrl">
    <label>Función
      <select id="iv-fn">
        <option value="lin">f(x) = 0.8x + 1</option>
        <option value="sq">f(x) = x² / 10</option>
        <option value="sin">f(x) = 5 + 4·sin(x)</option>
        <option value="sqrt">f(x) = 3·√x</option>
      </select>
    </label>
    <label>n = <input type="number" id="iv-n" min="2" max="200" value="10" step="1"></label>
  </div>
  <div class="ctrl">
    <label>x₀ <input type="range" id="iv-s0" min="0" max="75" value="15"
      step="1" style="width:70px"> <span id="iv-v0">1.5</span></label>
    <div class="sep"></div>
    <label>x  <input type="range" id="iv-sx" min="15" max="85" value="50"
      step="1" style="width:80px"> <span id="iv-vx">5.0</span></label>
    <div class="sep"></div>
    <label>x₁ <input type="range" id="iv-s1" min="25" max="100" value="85"
      step="1" style="width:70px"> <span id="iv-v1">8.5</span></label>
  </div>
  <canvas id="iv-cv"></canvas>
  <div class="cards">
    <div class="card"><div class="lbl">x seleccionado</div>
      <div class="val" id="iv-dx" style="color:#333">—</div></div>
    <div class="card"><div class="lbl">y interpolado</div>
      <div class="val" id="iv-di" style="color:#B71C1C">—</div></div>
    <div class="card"><div class="lbl">y teórico f(x)</div>
      <div class="val" id="iv-dt" style="color:#1B5E20">—</div></div>
    <div class="card"><div class="lbl">error relativo</div>
      <div class="val" id="iv-err" style="color:#E65100">—</div></div>
  </div>
  <div class="fml" id="iv-fml-static">
    $$y = y_0 + \\dfrac{(y_1 - y_0)(x - x_0)}{x_1 - x_0}$$
  </div>
  <div class="fml" id="iv-fml-vals" style="display:none"></div>
</div>
<script>
(function(){
  var cv=document.getElementById('iv-cv'),ctx=cv.getContext('2d');
  var XD=[0,10],YD=[-0.5,12.5],PAD,W,H,selX=5.0,dragPoint=null;
  var FNS={
    lin: {fn:function(x){return 0.8*x+1;},       lbl:'f(x) = 0.8x + 1'},
    sq:  {fn:function(x){return x*x/10;},         lbl:'f(x) = x² / 10'},
    sin: {fn:function(x){return 5+4*Math.sin(x);},lbl:'f(x) = 5 + 4·sin(x)'},
    sqrt:{fn:function(x){return 3*Math.sqrt(x);}, lbl:'f(x) = 3·√x'}
  };
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
    document.getElementById(dispId).textContent=val.toFixed(1);
  }
  function setXSlider(val){
    var el=document.getElementById('iv-sx');
    el.value=Math.round(val*10);
    document.getElementById('iv-vx').textContent=val.toFixed(1);
  }
  function updateXSliderBounds(x0,x1){
    var el=document.getElementById('iv-sx');
    el.min=Math.round(x0*10); el.max=Math.round(x1*10);
    if(parseFloat(el.value)<parseFloat(el.min))el.value=el.min;
    if(parseFloat(el.value)>parseFloat(el.max))el.value=el.max;
    document.getElementById('iv-vx').textContent=(parseFloat(el.value)/10).toFixed(1);
    return parseFloat(el.value)/10;
  }
  function resetCards(){
    ['iv-dx','iv-di','iv-dt','iv-err'].forEach(function(k){
      document.getElementById(k).textContent='—';
    });
    document.getElementById('iv-fml-vals').style.display='none';
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
      ctx.fillStyle='#FFF2CC';ctx.strokeStyle=isActive?'#E65100':'#D6B656';
      ctx.lineWidth=isActive?2.8:2.2;
      ctx.beginPath();ctx.arc(c[0],c[1],isActive?9:7,0,Math.PI*2);ctx.fill();ctx.stroke();
      ctx.fillStyle='#333';ctx.font='bold 11px sans-serif';
      ctx.textAlign='center';ctx.fillText('(x'+pt[2]+',y'+pt[2]+')',c[0],c[1]-13);
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
      document.getElementById('iv-dx').textContent=selX.toFixed(3);
      document.getElementById('iv-di').textContent=yi.toFixed(4);
      document.getElementById('iv-dt').textContent=yt.toFixed(4);
      var err=Math.abs(yt-yi),errPct=yt!==0?err/Math.abs(yt)*100:0;
      document.getElementById('iv-err').textContent=errPct.toFixed(2)+'%';
      var vals=document.getElementById('iv-fml-vals');
      vals.style.display='flex';
      vals.innerHTML='y = '+y0.toFixed(3)+' + '
        +'<span class="frac"><span class="num">('+( y1-y0).toFixed(3)
        +')('+( selX-x0).toFixed(3)+')</span>'
        +'<span class="den">'+( x1-x0).toFixed(3)+'</span></span>'
        +' = <span style="color:#B71C1C;font-weight:600;margin-left:6px">'+yi.toFixed(4)+'</span>';
    }
    /* function label */
    ctx.fillStyle='#1565C0';ctx.font='12px sans-serif';ctx.textAlign='left';
    ctx.fillText(s.lbl,PAD.l+8,PAD.t+16);
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
  function onUp(){dragPoint=null;draw();}
  cv.addEventListener('mousedown',function(e){var c=evtCoords(e);onDown(c.cx,c.cy);});
  cv.addEventListener('mousemove',function(e){var c=evtCoords(e);onMove(c.cx,c.cy);});
  cv.addEventListener('mouseup',onUp);
  cv.addEventListener('mouseleave',function(){dragPoint=null;});
  cv.addEventListener('touchstart',function(e){e.preventDefault();var c=evtCoords(e);onDown(c.cx,c.cy);},{passive:false});
  cv.addEventListener('touchmove',function(e){e.preventDefault();var c=evtCoords(e);onMove(c.cx,c.cy);},{passive:false});
  cv.addEventListener('touchend',function(){onUp();},{passive:false});
  document.getElementById('iv-fn').addEventListener('input',function(){draw();});
  document.getElementById('iv-s0').addEventListener('input',function(){
    var x0=parseFloat(document.getElementById('iv-s0').value)/10;
    var x1=parseFloat(document.getElementById('iv-s1').value)/10;
    document.getElementById('iv-v0').textContent=x0.toFixed(1);
    selX=updateXSliderBounds(x0,x1); draw();
  });
  document.getElementById('iv-s1').addEventListener('input',function(){
    var x0=parseFloat(document.getElementById('iv-s0').value)/10;
    var x1=parseFloat(document.getElementById('iv-s1').value)/10;
    document.getElementById('iv-v1').textContent=x1.toFixed(1);
    selX=updateXSliderBounds(x0,x1); draw();
  });
  document.getElementById('iv-sx').addEventListener('input',function(){
    selX=parseFloat(document.getElementById('iv-sx').value)/10;
    document.getElementById('iv-vx').textContent=selX.toFixed(1);
    draw();
  });
  document.getElementById('iv-n').addEventListener('change',function(){
    var n=getN();
    var fn=FNS[document.getElementById('iv-fn').value].fn;
    var s0=document.getElementById('iv-s0'),s1=document.getElementById('iv-s1');
    s0.max=Math.round((n-0.5)*10); s1.max=Math.round(n*10);
    /* reset extremes to f(0) and f(n) */
    s0.value=0; s1.value=Math.round(n*10);
    document.getElementById('iv-v0').textContent=(0).toFixed(1);
    document.getElementById('iv-v1').textContent=n.toFixed(1);
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
