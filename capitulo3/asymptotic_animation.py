from __future__ import annotations

from IPython.display import HTML, display


def _run_app(mode: str):
    display(HTML(_BIG_O_HTML.replace("__MODE__", mode)))


def run_big_o_app():
    _run_app("big_o")


def run_little_o_app():
    _run_app("little_o")


def run_big_omega_app():
    _run_app("big_omega")


def run_little_omega_app():
    _run_app("little_omega")


def run_theta_app():
    _run_app("theta")


run_app = run_big_o_app


_BIG_O_HTML = r"""
<style>
#bo-wrap{background:#ffffff;font-family:sans-serif;padding:14px 4px;color:#333}
#bo-wrap .plot-wrap{position:relative;width:100%;height:380px}
#bo-wrap canvas{display:block;width:100%;height:380px;background:#ffffff;border:1px solid #e0e0e0;touch-action:none;cursor:grab}
#bo-wrap .axis-label{position:absolute;pointer-events:none;font-size:14px;color:#333}
#bo-wrap .axis-x{left:82px;right:32px;bottom:8px;text-align:center}
#bo-wrap .axis-y{left:-24px;top:50%;width:120px;text-align:center;transform:translateY(-50%) rotate(-90deg);transform-origin:center}
#bo-wrap .controls-grid{display:grid;grid-template-columns:max-content max-content max-content;column-gap:36px;row-gap:12px;margin-bottom:12px;align-items:start}
#bo-wrap .control-section{display:grid;grid-template-columns:max-content;grid-template-rows:auto auto;row-gap:8px}
#bo-wrap .ctrl{display:flex;gap:28px;flex-wrap:wrap;margin:0 0 12px 4px;align-items:center;font-size:13px;color:#333}
#bo-wrap .ctrl.vertical{flex-direction:column;align-items:flex-start;gap:8px}
#bo-wrap .ctrl.additional .label-text{width:124px;min-width:124px;justify-content:center;text-align:center}
#bo-wrap .controls-grid .ctrl{margin-bottom:0}
#bo-wrap .ctrl label{display:flex;align-items:center;gap:8px;font-weight:600;min-height:32px}
#bo-wrap .ctrl .label-text{display:inline-flex;align-items:center;justify-content:flex-end;width:52px;min-width:52px}
#bo-wrap .theta-c{display:none}
#bo-wrap .row-title{font-weight:700;color:#333;line-height:1.1}
#bo-wrap select,#bo-wrap input[type=number],#bo-wrap input[type=text]{width:112px;height:32px;box-sizing:border-box;padding:2px 4px;border:1px solid #ccc;border-radius:3px;font-size:13px;text-align:center}
#bo-wrap .stepper{display:inline-grid;grid-template-columns:34px 112px 34px;gap:4px;align-items:center}
#bo-wrap .stepper-field{display:flex;align-items:center;justify-content:center;width:112px;height:32px;box-sizing:border-box;border:1px solid #ccc;border-radius:3px;background:#fff;text-align:center;font-size:14px}
#bo-wrap .editable-field{outline:none;cursor:text;font-weight:400}
#bo-wrap .editable-field:focus{border-color:#1976D2;box-shadow:0 0 0 1px #1976D2}
#bo-wrap .stepper input{width:112px}
#bo-wrap .stepper button{width:34px;height:32px;border:1px solid #ccc;border-radius:3px;background:#f7f7f7;color:#333;cursor:pointer;font-size:13px;line-height:1}
#bo-wrap .stepper button:hover{background:#eeeeee}
#bo-wrap .cards{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-top:12px}
#bo-wrap .card{background:#f7f7f7;border:1px solid #e8e8e8;border-radius:4px;padding:10px 14px}
#bo-wrap .card .lbl{font-size:11px;color:#78909C;margin-bottom:3px}
#bo-wrap .card .val{font-size:15px;font-weight:600}
#bo-wrap .fml{margin-top:10px;background:#f7f7f7;border:1px solid #e8e8e8;border-radius:4px;padding:10px 20px;font-size:15px;color:#333;min-height:44px;text-align:center}
#bo-wrap .demo-title{font-weight:700;font-size:15px;margin:2px 0 8px;color:#333;text-align:left}
#bo-wrap .demo-line{display:block;text-align:center;margin:6px 0}
#bo-wrap .demo-sep{height:1px;background:#e0e0e0;margin:12px 0}
#bo-wrap #bo-limits{display:flex;justify-content:center;width:100%;overflow-x:auto}
#bo-wrap table{margin:12px auto 0!important;border-collapse:collapse!important;text-align:center!important;width:auto!important;color:#333!important;background:#fff!important;border:0!important}
#bo-wrap th,#bo-wrap td{padding:7px 14px!important;white-space:nowrap!important;border:0!important;border-bottom:1px solid #d0d0d0!important;color:#333!important;background:#fff!important;text-align:center!important;vertical-align:middle!important}
#bo-wrap th{font-weight:700!important}
#bo-wrap thead tr{border-bottom:1px solid #9E9E9E}
#bo-wrap tr.active td{background:#f5f5f5!important;border-top:1px solid #9E9E9E!important;border-bottom:1px solid #9E9E9E!important}
#bo-wrap .ok{color:#2E7D32;font-weight:700}
#bo-wrap .bad{color:#B71C1C;font-weight:700}
#bo-wrap .loose{color:#E65100;font-weight:700}
#bo-wrap .instructions{margin:0 0 24px 0;color:#333}
#bo-wrap .instructions .row-title{margin-bottom:4px}
#bo-wrap .instructions ul{margin:0 0 0 18px;padding:0;font-size:13px;color:#555}
#bo-wrap .instructions li{margin:2px 0}
#bo-wrap .legend{display:flex;justify-content:center;gap:22px;flex-wrap:wrap;margin-top:8px;font-size:14px;color:#333}
#bo-wrap .legend .sw{display:inline-block;width:22px;height:0;border-top:3px solid currentColor;vertical-align:middle;margin-right:6px}
#bo-wrap .note{margin:8px auto 0;max-width:980px;text-align:center;font-size:13px;color:#555}
#bo-wrap .actions{display:flex;gap:8px;align-items:center}
#bo-wrap .action-btn{height:32px;border:1px solid #ccc;border-radius:3px;background:#f7f7f7;color:#333;cursor:pointer;padding:0 12px;font-size:13px}
#bo-wrap .action-btn:hover{background:#eeeeee}
@media(max-width:900px){#bo-wrap .cards{grid-template-columns:repeat(2,1fr)}}
</style>

<div id="bo-wrap">
  <div class="instructions">
    <div class="row-title">Instrucciones:</div>
    <ul>
      <li>Usa los controles para seleccionar \(C(n)\), \(g(n)\), el intervalo visible, las constantes, los términos menores y la escala.</li>
      <li>Puedes escribir valores para \(a\) y \(b\), incluyendo valores como \(10^{20}\), \(1\) o \(15.5\).</li>
      <li>Arrastra cerca del borde izquierdo o derecho de la gráfica para mover \(a\) o \(b\); arrastra el interior para desplazar el intervalo.</li>
    </ul>
  </div>
  <div class="controls-grid">
  <div class="control-section">
    <div class="row-title">Funciones de referencia:</div>
    <div class="ctrl">
    <label><span class="label-text">\(C(n)\)</span>
      <span class="stepper">
        <button type="button" id="bo-cfn-dec">◀</button>
        <span class="stepper-field" id="bo-cfn">—</span>
        <button type="button" id="bo-cfn-inc">▶</button>
      </span>
    </label>
    </div>
    <div class="ctrl">
    <label><span class="label-text">\(g(n)\)</span>
      <span class="stepper">
        <button type="button" id="bo-gfn-dec">◀</button>
        <span class="stepper-field" id="bo-gfn">—</span>
        <button type="button" id="bo-gfn-inc">▶</button>
      </span>
    </label>
    </div>
  </div>
  <div class="control-section">
    <div class="row-title">Intervalo:</div>
    <div class="ctrl vertical">
    <label><span class="label-text">\(a\)</span>
      <span class="stepper">
        <button type="button" id="bo-a-dec">◀</button>
        <span class="stepper-field editable-field" id="bo-a" role="textbox" contenteditable="true" data-raw="0">\(0\)</span>
        <button type="button" id="bo-a-inc">▶</button>
      </span>
    </label>
    <label><span class="label-text">\(b\)</span>
      <span class="stepper">
        <button type="button" id="bo-b-dec">◀</button>
        <span class="stepper-field editable-field" id="bo-b" role="textbox" contenteditable="true" data-raw="10**20">\(10^{20}\)</span>
        <button type="button" id="bo-b-inc">▶</button>
      </span>
    </label>
    </div>
  </div>
  <div class="control-section">
    <div class="row-title">Parámetros adicionales:</div>
    <div class="ctrl vertical additional">
    <label><span class="label-text">\(\text{Términos menores}\)</span><input type="number" id="bo-lower" min="0" max="4" value="0" step="1"></label>
    <label class="single-c"><span class="label-text">\(c\)</span><input type="number" id="bo-c" min="0.1" max="1000" value="1" step="0.1"></label>
    <label class="theta-c"><span class="label-text">\(c_1\)</span><input type="number" id="bo-c1" min="0.1" max="1000" value="1" step="0.1"></label>
    <label class="theta-c"><span class="label-text">\(c_2\)</span><input type="number" id="bo-c2" min="0.1" max="1000" value="1" step="0.1"></label>
    <label><span class="label-text">\(\text{Escala}\)</span>
      <select id="bo-scale">
        <option value="linear" selected>Lineal</option>
        <option value="log">Logarítmica</option>
      </select>
    </label>
    <div class="actions"><span class="label-text"></span><button type="button" class="action-btn" id="bo-reset">Restablecer</button></div>
    </div>
  </div>
  </div>
  <div class="plot-wrap">
    <canvas id="bo-cv"></canvas>
    <div class="axis-label axis-x">\(\text{Tamaño de la entrada }(n)\)</div>
    <div class="axis-label axis-y" id="bo-axis-y">—</div>
  </div>
  <div class="legend">
    <span style="color:#1565C0"><span class="sw"></span><span id="bo-leg-c">—</span></span>
    <span style="color:#B71C1C"><span class="sw"></span><span id="bo-leg-cg">—</span></span>
    <span style="color:#EF6C00;display:none" id="bo-leg-low-wrap"><span class="sw"></span><span id="bo-leg-low">—</span></span>
    <span style="color:#66BB6A"><span class="sw" style="border-top-style:dotted"></span><span id="bo-leg-n0">—</span></span>
  </div>
  <div class="note" id="bo-reading">—</div>
  <div class="cards">
    <div class="card"><div class="lbl">Intervalo visible</div><div class="val" id="bo-interval">—</div></div>
    <div class="card"><div class="lbl">n₀ estimado</div><div class="val" id="bo-n0">—</div></div>
    <div class="card"><div class="lbl">Límite del cociente</div><div class="val" id="bo-limit">—</div></div>
    <div class="card"><div class="lbl" id="bo-c-rule-label">Condición sobre c</div><div class="val" id="bo-c-rule">—</div></div>
    <div class="card"><div class="lbl">Conclusión</div><div class="val" id="bo-status">—</div></div>
  </div>

  <div class="fml" id="bo-quotient">—</div>
  <div id="bo-limits"></div>
</div>

<script>
window.MathJax = window.MathJax || {tex:{inlineMath:[['\\(','\\)'],['$$','$$']],displayMath:[['\\[','\\]'],['$$','$$']]},svg:{fontCache:'none'}};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
<script>
(function(){
  var MODE='__MODE__';
  var root=document.getElementById('bo-wrap');
  var cv=document.getElementById('bo-cv'),ctx=cv.getContext('2d');
  var W=0,H=0,PAD={l:82,r:32,t:38,b:58},drag=null,panStart=null;
  var FNS={
    one:{label:'1',latex:'1',rank:0,fn:function(n){return 1;}},
    log:{label:'log₂(n)',latex:'\\log_2(n)',rank:1,fn:function(n){return n<=1?0:Math.log2(n);}},
    n:{label:'n',latex:'n',rank:2,fn:function(n){return n;}},
    nlog:{label:'n·log₂(n)',latex:'n\\cdot\\log_2(n)',rank:3,fn:function(n){return n<=1?0:n*Math.log2(n);}},
    n2:{label:'n²',latex:'n^2',rank:4,fn:function(n){return n*n;}},
    n3:{label:'n³',latex:'n^3',rank:5,fn:function(n){return n*n*n;}},
    book:{label:'n³+2n²+n+5',latex:'n^3+2n^2+n+5',rank:5,fn:function(n){return n*n*n+2*n*n+n+5;}},
    exp:{label:'2ⁿ',latex:'2^n',rank:6,fn:function(n){return n>1023?Infinity:Math.pow(2,n);}},
    fact:{label:'n!',latex:'n!',rank:7,fn:function(n){var r=1,m=Math.min(Math.floor(n),170);for(var i=2;i<=m;i++)r*=i;return r;}}
  };
  var ORDER=['one','log','n','nlog','n2','n3','exp','fact'];
  var C_ORDER=['one','log','n','nlog','n2','n3','book','exp','fact'];
  var LOWER_TERMS=[];
  var MAX_B=100000000000000000000;
  var STATE_A=0,STATE_B=MAX_B,STATE_C_INDEX=4,STATE_G_INDEX=4;
  function el(id){return document.getElementById(id);}
  function cKey(){return C_ORDER[STATE_C_INDEX]}
  function gKey(){return ORDER[STATE_G_INDEX]}
  function cVal(){return Math.max(0.1,parseFloat(el('bo-c').value)||1)}
  function c1Val(){return Math.max(0.1,parseFloat(el('bo-c1').value)||1)}
  function c2Val(){return Math.max(0.1,parseFloat(el('bo-c2').value)||1)}
  function upperFactor(c){return isThetaMode()?c.c2:c}
  function lowerFactor(c){return isThetaMode()?c.c1:c}
  function scaleMode(){return el('bo-scale').value}
  function lowerCount(){return Math.max(0,Math.min(4,parseInt(el('bo-lower').value,10)||0))}
  function isLogScale(){return scaleMode()==='log'}
  function decadeValue(exp){return Math.pow(10,Math.max(0,Math.round(exp)))}
  function nearestDecade(value,allowZero){
    if(allowZero && value<=0)return 0;
    if(value<=1)return 1;
    return Math.pow(10,Math.round(Math.log10(value)));
  }
  function powerText(value){
    if(!isFinite(value))return '∞';
    if(value===0)return '0';
    return '10**'+Math.round(Math.log10(Math.max(1,value)));
  }
  function fieldText(value){
    if(!isFinite(value))return '';
    if(value===0)return '0';
    if(isPowerOfTen(value))return powerText(value);
    return fmtNumber(value);
  }
  function powerLatex(value){
    if(!isFinite(value))return '\\infty';
    if(value===0)return '0';
    return '10^{'+Math.round(Math.log10(Math.max(1,value)))+'}';
  }
  function isPowerOfTen(value){
    if(!isFinite(value) || value<=0)return false;
    var exp=Math.round(Math.log10(value));
    return Math.abs(value-Math.pow(10,exp))<=Math.max(1e-9,Math.abs(value)*1e-10);
  }
  function valueLatex(value){
    if(!isFinite(value))return '\\infty';
    if(value===0)return '0';
    if(isPowerOfTen(value))return powerLatex(value);
    return fmtNumber(value);
  }
  function fmtNumber(value){
    if(!isFinite(value))return '∞';
    if(Number.isInteger(value))return String(value);
    return String(Math.round(value*1000000)/1000000);
  }
  function nextPower(value,allowZero){
    if(allowZero && value<=0)return 1;
    return Math.pow(10,Math.min(20,Math.floor(Math.log10(Math.max(1,value)))+1));
  }
  function previousPower(value,allowZero){
    if(allowZero && value<=1)return 0;
    return Math.pow(10,Math.max(0,Math.ceil(Math.log10(Math.max(1,value)))-1));
  }
  function axisScale(maxValue){
    var exp=Math.max(0,Math.floor(Math.log10(Math.max(1,maxValue))));
    if(exp<4)return {scale:1,label:''};
    return {scale:Math.pow(10,exp),label:'10',exp:exp};
  }
  function fmtScaledAxis(value,scale){
    if(!isFinite(value))return '∞';
    if(value===0)return '0';
    var scaled=value/scale;
    return scaled.toFixed(2).replace(/\.?0+$/,'');
  }
  function fmt(x){
    if(!isFinite(x))return '∞';
    if(Math.abs(x)>=10000 || (Math.abs(x)>0 && Math.abs(x)<0.001))return x.toExponential(2);
    return (Math.round(x*100)/100).toString();
  }
  function drawPowerOfTenLabel(x,y,align,baseline,exp){
    ctx.save();
    ctx.fillStyle='#333';
    var base='10';
    var expText=String(exp);
    ctx.font='14px sans-serif';
    var baseWidth=ctx.measureText(base).width;
    ctx.font='10px sans-serif';
    var expWidth=ctx.measureText(expText).width;
    var gap=2;
    var totalWidth=baseWidth+gap+expWidth;
    var startX=align==='right'?x-totalWidth:(align==='center'?x-totalWidth/2:x);
    ctx.textAlign='left';
    ctx.textBaseline=baseline;
    ctx.font='14px sans-serif';
    ctx.fillText(base,startX,y);
    ctx.font='10px sans-serif';
    ctx.fillText(expText,startX+baseWidth+gap,y-6);
    ctx.restore();
  }
  function limitValue(ck,gk){
    if(FNS[ck].rank<FNS[gk].rank)return '0';
    if(FNS[ck].rank===FNS[gk].rank)return '1';
    return '∞';
  }
  function modeLatex(){
    if(MODE==='little_o')return 'o';
    if(MODE==='big_omega')return '\\Omega';
    if(MODE==='little_omega')return '\\omega';
    if(MODE==='theta')return '\\Theta';
    return 'O';
  }
  function modeName(){
    if(MODE==='little_o')return 'notación o';
    if(MODE==='big_omega')return 'notación Ω';
    if(MODE==='little_omega')return 'notación ω';
    if(MODE==='theta')return 'notación Θ';
    return 'notación O';
  }
  function limitOperatorLatex(){
    if(MODE==='big_o')return '\\limsup';
    if(MODE==='big_omega')return '\\liminf';
    return '\\lim';
  }
  function limitExpressionLatex(ck,gk){
    var op=limitOperatorLatex();
    return '\\displaystyle k='+op+'_{n\\to\\infty}\\left(\\frac{C(n)}{g(n)}\\right)='+
      op+'_{n\\to\\infty}\\left(\\frac{'+cLatex()+'}{'+latexOf(gk)+'}\\right)='+
      displayLimitValue(limitValue(ck,gk));
  }
  function isUpperMode(){return MODE==='big_o' || MODE==='little_o'}
  function isLowerMode(){return MODE==='big_omega' || MODE==='little_omega'}
  function isThetaMode(){return MODE==='theta'}
  function cColor(){return '#1565C0'}
  function cgColor(){return isLowerMode()?'#EF6C00':'#B71C1C'}
  function c1gColor(){return '#EF6C00'}
  function n0Color(){return '#2E7D32'}
  function areaColor(){
    if(isThetaMode())return 'rgba(21,101,192,0.25)';
    if(isLowerMode())return 'rgba(21,101,192,0.25)';
    return 'rgba(183,28,28,0.30)';
  }
  function isMember(ck,gk){
    if(MODE==='big_o')return FNS[ck].rank<=FNS[gk].rank;
    if(MODE==='little_o')return FNS[ck].rank<FNS[gk].rank;
    if(MODE==='big_omega')return FNS[ck].rank>=FNS[gk].rank;
    if(MODE==='little_omega')return FNS[ck].rank>FNS[gk].rank;
    if(MODE==='theta')return FNS[ck].rank===FNS[gk].rank;
    return false;
  }
  function cLowerBound(ck,gk){
    if(MODE==='theta')return isMember(ck,gk)?1:Infinity;
    if(MODE==='little_o' || MODE==='little_omega')return isMember(ck,gk)?0:Infinity;
    if(MODE==='big_omega'){
      if(FNS[ck].rank<FNS[gk].rank)return Infinity;
      return 0;
    }
    if(FNS[ck].rank>FNS[gk].rank)return Infinity;
    if(FNS[ck].rank===FNS[gk].rank)return 1;
    return 0;
  }
  function cUpperBound(ck,gk){
    if(MODE==='big_omega' && FNS[ck].rank===FNS[gk].rank)return 1;
    return Infinity;
  }
  function cRule(ck,gk){
    var k=cLowerBound(ck,gk);
    if(!isFinite(k))return MODE==='theta'?'\\text{No existen }c_1,c_2':'\\text{No existe }c';
    var upper=cUpperBound(ck,gk);
    if(isFinite(upper))return '0\\lt c\\le '+fmt(upper);
    if(MODE==='theta')return '0\\lt c_1\\le '+displayLimitValue(limitValue(ck,gk))+'\\le c_2';
    if(k===0)return 'c\\gt 0';
    return 'c\\ge '+fmt(k);
  }
  function defaultC(ck,gk){
    var k=cLowerBound(ck,gk);
    if(!isFinite(k))return '';
    var upper=cUpperBound(ck,gk);
    if(isFinite(upper))return upper;
    return k===0?1:k;
  }
  function latexOf(key){return FNS[key].latex}
  function termLatex(term){
    if(term.key==='one')return String(term.coef);
    if(term.coef===1)return latexOf(term.key);
    return term.coef+'\\cdot '+latexOf(term.key);
  }
  function cLatex(){
    var parts=[latexOf(cKey())];
    LOWER_TERMS.forEach(function(term){parts.push(termLatex(term));});
    return parts.join('+');
  }
  function cFn(ck,n){
    var total=FNS[ck].fn(n);
    LOWER_TERMS.forEach(function(term){total+=term.coef*FNS[term.key].fn(n);});
    return total;
  }
  function randomInt(min,max){return min+Math.floor(Math.random()*(max-min+1))}
  function syncLowerControl(){
    var input=el('bo-lower');
    if(cKey()==='book'){
      input.value=0;
      input.disabled=true;
      return;
    }
    var available=ORDER.filter(function(key){return FNS[key].rank<FNS[cKey()].rank;}).length;
    input.max=Math.min(4,available);
    input.disabled=available===0;
    if(available===0)input.value=0;
    if(lowerCount()>available)input.value=available;
  }
  function regenerateLowerTerms(){
    syncLowerControl();
    LOWER_TERMS=[];
    var candidates=ORDER.filter(function(key){return FNS[key].rank<FNS[cKey()].rank;});
    var count=Math.min(lowerCount(),candidates.length);
    for(var i=0;i<count;i++){
      var index=randomInt(0,candidates.length-1);
      var key=candidates.splice(index,1)[0];
      LOWER_TERMS.push({key:key,coef:randomInt(1,5)});
    }
    LOWER_TERMS.sort(function(a,b){return FNS[b.key].rank-FNS[a.key].rank;});
  }
  function tex(content){return '\\('+content+'\\)'}
  function texBlock(content){return '\\['+content+'\\]'}
  function displayLimitValue(value){
    if(value==='∞')return '\\infty';
    return value;
  }
  function typeset(attempt){
    attempt=attempt||0;
    if(window.MathJax && MathJax.typesetPromise){
      MathJax.typesetPromise([root]).catch(function(){});
    }else if(attempt<8){
      setTimeout(function(){typeset(attempt+1);},150);
    }
  }
  function enforceC(ck,gk){
    if(isThetaMode())return enforceThetaC(ck,gk);
    var input=el('bo-c'),k=cLowerBound(ck,gk);
    if(!isFinite(k)){
      input.disabled=true;
      input.value='';
      return 1;
    }
    input.disabled=false;
    input.min=k===0?0.1:k;
    var upper=cUpperBound(ck,gk);
    input.max=isFinite(upper)?upper:1000;
    if(input.value==='' || (parseFloat(input.value)||0)<parseFloat(input.min)){
      input.value=defaultC(ck,gk);
    }
    if(isFinite(upper) && (parseFloat(input.value)||0)>upper){
      input.value=upper;
    }
    return cVal();
  }
  function enforceThetaC(ck,gk){
    var cInput=el('bo-c'),c1Input=el('bo-c1'),c2Input=el('bo-c2');
    cInput.disabled=true;
    if(!isMember(ck,gk)){
      c1Input.disabled=true;c2Input.disabled=true;
      c1Input.value='';c2Input.value='';
      return {c1:1,c2:1};
    }
    c1Input.disabled=false;c2Input.disabled=false;
    c1Input.min=0.1;c2Input.min=1;
    c1Input.max=1;c2Input.max=1000;
    if(c1Input.value==='' || (parseFloat(c1Input.value)||0)<=0 || (parseFloat(c1Input.value)||0)>1)c1Input.value=1;
    if(c2Input.value==='' || (parseFloat(c2Input.value)||0)<1)c2Input.value=1;
    return {c1:c1Val(),c2:c2Val()};
  }
  function updateConstantControls(){
    var theta=isThetaMode();
    Array.prototype.forEach.call(root.querySelectorAll('.single-c'),function(node){node.style.display=theta?'none':'flex';});
    Array.prototype.forEach.call(root.querySelectorAll('.theta-c'),function(node){node.style.display=theta?'flex':'none';});
  }
  function relationClass(ck,gk){
    if(!isMember(ck,gk))return 'bad';
    if(MODE==='big_o' && FNS[ck].rank<FNS[gk].rank)return 'loose';
    if(MODE==='big_omega' && FNS[ck].rank>FNS[gk].rank)return 'loose';
    return 'ok';
  }
  function membershipText(ck,gk){
    if(isMember(ck,gk))return '\\('+cLatex()+'\\in '+modeLatex()+'('+latexOf(gk)+')\\)';
    return '\\('+cLatex()+'\\notin '+modeLatex()+'('+latexOf(gk)+')\\)';
  }
  function estimateN0(ck,gk,c){
    if(!isMember(ck,gk))return null;
    if(isUpperMode() && FNS[ck].rank===FNS[gk].rank && c<1)return null;
    if(MODE==='big_omega' && FNS[ck].rank===FNS[gk].rank && c>1)return null;
    if(isThetaMode() && (c.c1<=0 || c.c2<1))return null;
    var max=1000,suffixOk=true,first=null;
    for(var n=max;n>=2;n--){
      suffixOk=suffixOk && satisfiesInequality(ck,gk,c,n);
      if(suffixOk)first=n;
    }
    return first;
  }
  function satisfiesInequality(ck,gk,c,n){
    var left=cFn(ck,n),ref=FNS[gk].fn(n);
    if(MODE==='big_o')return left<=c*ref;
    if(MODE==='little_o')return left<c*ref;
    if(MODE==='big_omega')return left>=c*ref;
    if(MODE==='little_omega')return left>c*ref;
    if(isThetaMode())return c.c1*ref<=left && left<=c.c2*ref;
    return false;
  }
  function estimateA(ck,gk,c){
    var n0=estimateN0(ck,gk,c);
    if(n0===null)return null;
    if(n0<=2)return 2;
    var lo=n0-1,hi=n0;
    if(satisfiesInequality(ck,gk,c,lo))return lo;
    for(var i=0;i<42;i++){
      var mid=(lo+hi)/2;
      if(satisfiesInequality(ck,gk,c,mid))hi=mid;
      else lo=mid;
    }
    return hi;
  }
  function parsePowerInput(value,allowZero){
    var text=String(value).trim().replace(/\s+/g,'');
    if(allowZero && text==='0')return 0;
    var match=text.match(/^10(?:\\*\\*|\\^)(\\d+)$/);
    if(match)return Math.pow(10,Math.min(20,parseInt(match[1],10)));
    var numeric=parseFloat(text);
    if(!isFinite(numeric))return allowZero?0:1;
    return numeric;
  }
  function inequalityLatex(ck,gk,c,n0){
    if(!isMember(ck,gk))return '\\text{No existe }c\\text{ que satisfaga la desigualdad para todo }n\\ge n_0';
    var base='';
    if(MODE==='big_o')base='C(n)\\le c\\cdot g(n)\\quad '+cLatex()+'\\le '+fmt(c)+'\\cdot '+latexOf(gk);
    if(MODE==='little_o')base='C(n)\\lt c\\cdot g(n)\\quad '+cLatex()+'\\lt '+fmt(c)+'\\cdot '+latexOf(gk);
    if(MODE==='big_omega')base='C(n)\\ge c\\cdot g(n)\\quad '+cLatex()+'\\ge '+fmt(c)+'\\cdot '+latexOf(gk);
    if(MODE==='little_omega')base='C(n)\\gt c\\cdot g(n)\\quad '+cLatex()+'\\gt '+fmt(c)+'\\cdot '+latexOf(gk);
    if(isThetaMode())base='\\begin{aligned}c_1\\cdot g(n)&\\le C(n)\\le c_2\\cdot g(n)\\\\'+fmt(c.c1)+'\\cdot '+latexOf(gk)+'&\\le '+cLatex()+'\\le '+fmt(c.c2)+'\\cdot '+latexOf(gk)+'\\end{aligned}';
    return base;
  }
  function proofHtml(ck,gk,c,n0,lim){
    var limitLine=texBlock(limitExpressionLatex(ck,gk)+'\\quad\\therefore\\quad '+cRule(ck,gk));
    var n0Title=isThetaMode()?'Cálculo de \\(\\mathbf{n}_0\\) para \\(\\mathbf{c}_1='+fmt(c.c1)+'\\) y \\(\\mathbf{c}_2='+fmt(c.c2)+'\\):':'Cálculo de \\(\\mathbf{n}_0\\) para \\(\\mathbf{c}='+fmt(c)+'\\):';
    var aValue=estimateA(ck,gk,c);
    var aDisplay=aValue===null?null:fmt(aValue);
    var n0FromA=aValue===null?null:Math.ceil(aValue);
    var inequalityLine=texBlock('\\displaystyle '+inequalityLatex(ck,gk,c,n0));
    if(aValue===null){
      return '<div class="demo-title">Demostración por límite:</div>'+
        '<div class="demo-line">'+limitLine+'</div>'+
        '<div class="demo-sep"></div>'+
        '<div class="demo-title">'+n0Title+'</div>'+
        '<div class="demo-line">'+inequalityLine+'</div>'+
        '<div class="demo-line">'+texBlock('\\displaystyle A\\text{ no existe para este }c\\quad\\Rightarrow\\quad n_0\\text{ no existe}')+'</div>';
    }
    var aLine=texBlock('\\displaystyle n\\ge '+aDisplay);
    var thresholdLine=texBlock('\\displaystyle A='+aDisplay);
    var n0Line=texBlock('\\displaystyle n_0=\\lceil A\\rceil=\\lceil '+aDisplay+'\\rceil='+n0FromA);
    return '<div class="demo-title">Demostración por límite:</div>'+
      '<div class="demo-line">'+limitLine+'</div>'+
      '<div class="demo-sep"></div>'+
      '<div class="demo-title">'+n0Title+'</div>'+
      '<div class="demo-line">'+inequalityLine+'</div>'+
      '<div class="demo-line">'+aLine+'</div>'+
      '<div class="demo-line">'+thresholdLine+'</div>'+
      '<div class="demo-line">'+n0Line+'</div>';
  }
  function readingText(ck,gk,n0,lim){
    if(!isMember(ck,gk))return 'La función seleccionada no satisface la relación asintótica de esta notación con la referencia actual.';
    if(MODE==='big_o')return 'La curva azul queda eventualmente debajo de la cota construida con la función de referencia.';
    if(MODE==='little_o')return 'La curva azul queda estrictamente por debajo de cualquier múltiplo positivo de la referencia para valores suficientemente grandes.';
    if(MODE==='big_omega')return 'La curva azul queda eventualmente por encima de la cota inferior construida con la función de referencia.';
    if(MODE==='little_omega')return 'La curva azul supera estrictamente cualquier múltiplo positivo de la referencia para valores suficientemente grandes.';
    if(MODE==='theta')return 'La curva azul queda atrapada entre las dos cotas construidas con la misma función de referencia.';
    return '';
  }
  function resize(){
    var dpr=window.devicePixelRatio||1;
    var r=cv.getBoundingClientRect();
    cv.width=r.width*dpr;cv.height=r.height*dpr;
    ctx.setTransform(dpr,0,0,dpr,0,0);
    W=r.width;H=r.height;
  }
  function interval(){
    return [STATE_A,STATE_B];
  }
  function syncInputs(a,b){
    a=Math.max(0,Math.min(MAX_B-1,a));
    b=Math.max(1,Math.min(MAX_B,b));
    if(b<=a)b=a===0?1:Math.min(MAX_B,a*10);
    if(b<=a){a=0;b=1;}
    STATE_A=a;STATE_B=b;
    setEditableField('bo-a',a);
    setEditableField('bo-b',b);
  }
  function setEditableField(id,value){
    var target=el(id);
    target.dataset.raw=fieldText(value);
    target.dataset.lastValue=String(value);
    if(document.activeElement===target)return;
    target.innerHTML=tex(valueLatex(value));
  }
  function beginEditableField(id){
    var target=el(id);
    target.textContent=target.dataset.raw || '';
  }
  function sanitizeEditableField(id){
    var target=el(id);
    var text=target.textContent.replace(/[^0-9.*]/g,'');
    var firstDot=text.indexOf('.');
    if(firstDot!==-1)text=text.slice(0,firstDot+1)+text.slice(firstDot+1).replace(/\\./g,'');
    target.textContent=text;
  }
  function sample(a,b,ck,gk,c){
    var xs=[],ys1=[],ys2=[],ys3=[],ys4=[],mx=0,mn=Infinity;
    var logSampling=isLogScale();
    var logLo=logSampling?Math.log10(logXMin(a,b)):0;
    var logHi=logSampling?Math.log10(Math.max(b,logXMin(a,b))):0;
    for(var i=0;i<=260;i++){
      var n=logSampling?Math.pow(10,logLo+(logHi-logLo)*i/260):a+(b-a)*i/260;
      var v1=cFn(ck,n),v2=FNS[gk].fn(n),v3=upperFactor(c)*v2,v4=lowerFactor(c)*v2;
      if(isFinite(v1)&&isFinite(v2)&&isFinite(v3)&&isFinite(v4)){
        xs.push(n);ys1.push(v1);ys2.push(v2);ys3.push(v3);ys4.push(v4);
        mx=Math.max(mx,v1,v2,v3,v4);
        [v1,v2,v3,v4].forEach(function(v){if(v>0)mn=Math.min(mn,v);});
      }
    }
    return {xs:xs,c:ys1,g:ys2,cg:ys3,c1g:ys4,max:mx||1,min:isFinite(mn)?mn:1};
  }
  function logXMin(a,b){
    if(a>0)return a;
    return 1;
  }
  function xTransform(n,a,b){
    if(isLogScale())return Math.log10(Math.max(n,logXMin(a,b)));
    return n;
  }
  function visualXMin(a,b){return a<=0?-0.05*(b-a):a}
  function xDisplayBounds(a,b){
    var lo=isLogScale()?xTransform(logXMin(a,b),a,b):visualXMin(a,b);
    var bpos=xTransform(b,a,b);
    var span=Math.max(bpos-lo,1e-9);
    return {lo:lo-span*0.06,hi:bpos+span*0.06};
  }
  function tx(n,a,b){
    var bounds=xDisplayBounds(a,b);
    return PAD.l+(xTransform(n,a,b)-bounds.lo)/(bounds.hi-bounds.lo)*(W-PAD.l-PAD.r);
  }
  function yTransform(y){
    if(scaleMode()==='log')return Math.log10(y);
    return y;
  }
  function yBounds(data){
    if(!isLogScale())return {min:0,max:Math.max(data.max*1.08,10)};
    var min=Math.max(data.min/1.2,1e-9);
    var max=Math.max(data.max*1.08,min*10);
    return {min:min,max:max};
  }
  function ty(y,yrange){
    if(scaleMode()==='log'){
      if(!(y>0))return null;
      var lo=yTransform(yrange.min),hi=yTransform(yrange.max);
      return H-PAD.b-(yTransform(y)-lo)/(hi-lo)*(H-PAD.t-PAD.b);
    }
    return H-PAD.b-y/yrange.max*(H-PAD.t-PAD.b);
  }
  function fx(px,a,b){
    var ratio=(px-PAD.l)/(W-PAD.l-PAD.r);
    var bounds=xDisplayBounds(a,b);
    if(isLogScale()){
      return Math.pow(10,bounds.lo+ratio*(bounds.hi-bounds.lo));
    }
    return bounds.lo+ratio*(bounds.hi-bounds.lo);
  }
  function niceTicks(lo,hi,count){
    var range=Math.max(hi-lo,1e-9),raw=range/count;
    var pow=Math.pow(10,Math.floor(Math.log10(raw)));
    var mult=[1,2,5,10],step=pow;
    for(var i=0;i<mult.length;i++){if(raw<=mult[i]*pow){step=mult[i]*pow;break;}}
    var ticks=[],start=Math.ceil(lo/step)*step;
    for(var v=start;v<=hi+step*0.5;v+=step)ticks.push(v);
    return ticks;
  }
  function logTicks(ymin,ymax){
    var minExp=Math.floor(Math.log10(Math.max(ymin,1e-9)));
    var maxExp=Math.ceil(Math.log10(Math.max(ymax,ymin*10)));
    var step=Math.max(1,Math.ceil((maxExp-minExp+1)/6));
    var ticks=[];
    for(var exp=minExp;exp<=maxExp;exp+=step)ticks.push(Math.pow(10,exp));
    var top=Math.pow(10,maxExp);
    if(ticks[ticks.length-1]!==top)ticks.push(top);
    return ticks.filter(function(v,index,arr){return v>=ymin && v<=ymax && arr.indexOf(v)===index;});
  }
  function logXTicks(a,b){
    var lo=logXMin(a,b),hi=Math.max(b,lo);
    var minExp=Math.floor(Math.log10(lo));
    var maxExp=Math.ceil(Math.log10(hi));
    var step=Math.max(1,Math.ceil((maxExp-minExp+1)/6));
    var ticks=[];
    for(var exp=minExp;exp<=maxExp;exp+=step){
      var value=Math.pow(10,exp);
      if(value>=lo && value<=hi)ticks.push(value);
    }
    if(ticks.indexOf(hi)===-1 && isPowerOfTen(hi))ticks.push(hi);
    return ticks;
  }
  function drawAxes(a,b,yrange){
    ctx.save();
    ctx.strokeStyle='#b8b8b8';ctx.lineWidth=0.7;ctx.setLineDash([4,4]);
    ctx.fillStyle='#333';ctx.font='14px sans-serif';ctx.textAlign='center';ctx.textBaseline='top';
    var xScale=isLogScale()?{scale:1,label:''}:axisScale(b);
    var xt=isLogScale()?logXTicks(a,b):niceTicks(0,b,5);
    for(var i=0;i<xt.length;i++){
      var x=tx(xt[i],a,b);
      ctx.beginPath();ctx.moveTo(x,PAD.t);ctx.lineTo(x,H-PAD.b);ctx.stroke();
      if(isLogScale())drawPowerOfTenLabel(x,H-PAD.b+8,'center','top',Math.round(Math.log10(xt[i])));
      else ctx.fillText(fmtScaledAxis(xt[i],xScale.scale),x,H-PAD.b+8);
    }
    if(xScale.label){
      drawPowerOfTenLabel(W-PAD.r,H-PAD.b+25,'right','top',xScale.exp);
    }
    ctx.textAlign='right';ctx.textBaseline='middle';
    var yScale=isLogScale()?{scale:1,label:''}:axisScale(yrange.max);
    var yt=isLogScale()?logTicks(yrange.min,yrange.max):niceTicks(0,yrange.max,5);
    for(var j=0;j<yt.length;j++){
      var y=ty(yt[j],yrange);
      if(y===null)continue;
      ctx.beginPath();ctx.moveTo(PAD.l,y);ctx.lineTo(W-PAD.r,y);ctx.stroke();
      if(isLogScale())drawPowerOfTenLabel(PAD.l-8,y,'right','middle',Math.round(Math.log10(yt[j])));
      else ctx.fillText(fmtScaledAxis(yt[j],yScale.scale),PAD.l-8,y);
    }
    if(yScale.label){
      drawPowerOfTenLabel(PAD.l,PAD.t-8,'left','bottom',yScale.exp);
    }
    ctx.setLineDash([]);ctx.strokeStyle='#333';ctx.lineWidth=1.2;
    ctx.beginPath();ctx.moveTo(PAD.l,PAD.t);ctx.lineTo(PAD.l,H-PAD.b);ctx.lineTo(W-PAD.r,H-PAD.b);ctx.stroke();
    ctx.restore();
  }
  function drawLine(xs,ys,a,b,yrange,color,width,dash){
    ctx.save();ctx.strokeStyle=color;ctx.lineWidth=width||2;ctx.setLineDash(dash||[]);
    ctx.beginPath();
    var started=false;
    for(var i=0;i<xs.length;i++){
      var x=tx(xs[i],a,b),y=ty(ys[i],yrange);
      if(y===null){started=false;continue;}
      if(!started){ctx.moveTo(x,y);started=true;}else ctx.lineTo(x,y);
    }
    ctx.stroke();ctx.restore();
  }
  function drawValidArea(data,a,b,yrange,n0){
    if(n0===null)return;
    var upper=[],lower=[];
    for(var i=0;i<data.xs.length;i++){
      if(data.xs[i]<n0)continue;
      var top=null,bottom=null;
      if(MODE==='big_o' && data.cg[i]>=data.c[i]){top=data.cg[i];bottom=data.c[i];}
      if(MODE==='little_o' && data.cg[i]>data.c[i]){top=data.cg[i];bottom=data.c[i];}
      if(MODE==='big_omega' && data.c[i]>=data.cg[i]){top=data.c[i];bottom=data.cg[i];}
      if(MODE==='little_omega' && data.c[i]>data.cg[i]){top=data.c[i];bottom=data.cg[i];}
      if(isThetaMode()){
        var low=data.c1g[i],high=data.cg[i];
        if(data.c[i]>=low && data.c[i]<=high){top=high;bottom=low;}
      }
      if(top!==null && (!isLogScale() || (top>0 && bottom>0))){
        upper.push([tx(data.xs[i],a,b),ty(top,yrange)]);
        lower.push([tx(data.xs[i],a,b),ty(bottom,yrange)]);
      }
    }
    if(upper.length<2)return;
    ctx.save();
    ctx.fillStyle=areaColor();
    ctx.beginPath();
    ctx.moveTo(upper[0][0],upper[0][1]);
    for(var j=1;j<upper.length;j++)ctx.lineTo(upper[j][0],upper[j][1]);
    for(var k=lower.length-1;k>=0;k--)ctx.lineTo(lower[k][0],lower[k][1]);
    ctx.closePath();
    ctx.fill();
    ctx.restore();
  }
  function drawN0(n0,a,b,ck,yrange){
    if(n0===null || n0<a || n0>b)return;
    var x=tx(n0,a,b), y=ty(cFn(ck,n0),yrange);
    ctx.save();
    ctx.strokeStyle=n0Color();ctx.fillStyle=n0Color();ctx.lineWidth=2;ctx.setLineDash([3,4]);
    ctx.beginPath();ctx.moveTo(x,PAD.t);ctx.lineTo(x,H-PAD.b);ctx.stroke();
    ctx.restore();
  }
  function drawEndpointMarker(n,a,b,label){
    var x=tx(n,a,b),y=H-PAD.b;
    ctx.save();
    ctx.fillStyle='#2E7D32';ctx.strokeStyle='#2E7D32';
    ctx.beginPath();
    ctx.moveTo(x,y+2);ctx.lineTo(x-6,y+13);ctx.lineTo(x+6,y+13);ctx.closePath();ctx.fill();
    ctx.font='bold 12px sans-serif';ctx.textAlign='center';ctx.textBaseline='top';
    ctx.fillText(label,x,y+16);
    ctx.restore();
  }
  function draw(){
    resize();
    var ck=cKey(),gk=gKey(),c=enforceC(ck,gk);
    var ab=interval();syncInputs(ab[0],ab[1]);var a=interval()[0],b=interval()[1];
    var data=sample(a,b,ck,gk,c),yrange=yBounds(data);
    var n0=estimateN0(ck,gk,c),lim=limitValue(ck,gk);
    ctx.clearRect(0,0,W,H);ctx.fillStyle='#fff';ctx.fillRect(0,0,W,H);
    drawAxes(a,b,yrange);
    drawValidArea(data,a,b,yrange,n0);
    drawLine(data.xs,data.c,a,b,yrange,cColor(),2.4);
    drawLine(data.xs,data.cg,a,b,yrange,cgColor(),2.4);
    if(isThetaMode()){
      drawLine(data.xs,data.c1g,a,b,yrange,c1gColor(),2.0);
    }
    drawN0(n0,a,b,ck,yrange);
    drawEndpointMarker(a,a,b,'a');
    drawEndpointMarker(b,a,b,'b');
    updateText(a,b,ck,gk,c);
  }
  function updateText(a,b,ck,gk,c){
    var n0=estimateN0(ck,gk,c),lim=limitValue(ck,gk),cls=relationClass(ck,gk);
    el('bo-interval').innerHTML=tex('['+valueLatex(a)+', '+valueLatex(b)+']');
    el('bo-n0').innerHTML=n0===null?tex('\\text{No existe}') : tex('n_0='+n0);
    el('bo-limit').innerHTML=tex('k='+displayLimitValue(lim));
    el('bo-c-rule-label').textContent=isThetaMode()?'Condición sobre c₁,c₂':'Condición sobre c';
    el('bo-c-rule').innerHTML=tex(cRule(ck,gk));
    el('bo-status').className='val '+cls;
    el('bo-status').innerHTML=membershipText(ck,gk);
    el('bo-reading').innerHTML=readingText(ck,gk,n0,lim);
    el('bo-axis-y').innerHTML=tex(modeLatex()+'(g(n))');
    el('bo-cfn').innerHTML=tex(cLatex());
    el('bo-gfn').innerHTML=tex(latexOf(gk));
    el('bo-leg-c').innerHTML=tex('C(n)='+cLatex());
    el('bo-leg-c').parentElement.style.color=cColor();
    el('bo-leg-cg').parentElement.style.color=cgColor();
    el('bo-leg-cg').innerHTML=isThetaMode()?tex('c_2\\cdot g(n)='+fmt(c.c2)+'\\cdot '+latexOf(gk)):tex('c\\cdot g(n)='+fmt(c)+'\\cdot '+latexOf(gk));
    el('bo-leg-low-wrap').style.display=isThetaMode()?'inline':'none';
    el('bo-leg-low-wrap').style.color=c1gColor();
    el('bo-leg-low').innerHTML=tex('c_1\\cdot g(n)='+fmt(c.c1)+'\\cdot '+latexOf(gk));
    el('bo-leg-n0').parentElement.style.color=n0Color();
    el('bo-leg-n0').innerHTML=n0===null?tex('n_0\\text{ no existe}') : tex('n_0='+n0);
    el('bo-quotient').innerHTML=proofHtml(ck,gk,c,n0,lim);
    renderLimits(ck,gk);
    typeset();
  }
  function renderLimits(ck,selectedG){
    var html='<table><thead><tr><th>'+tex('\\mathbf{g(n)}')+'</th><th>Límite</th><th>Resultado</th></tr></thead><tbody>';
    ORDER.forEach(function(gk){
      var cls=relationClass(ck,gk),active=gk===selectedG?' class="active"':'';
      html+='<tr'+active+'><td>'+tex(latexOf(gk))+'</td><td>'+tex(limitExpressionLatex(ck,gk).replace(/^\\displaystyle k=/,'\\displaystyle '))+'</td><td class="'+cls+'">'+membershipText(ck,gk)+'</td></tr>';
    });
    html+='</tbody></table>';
    el('bo-limits').innerHTML=html;
  }
  function pointer(ev){
    var r=cv.getBoundingClientRect();
    var p=ev.touches?ev.touches[0]:ev;
    return {x:p.clientX-r.left,y:p.clientY-r.top};
  }
  function handleEndpointInput(id){
    var input=el(id),raw=parsePowerInput(input.textContent,id==='bo-a');
    if(!isFinite(raw))return;
    if(id==='bo-a')syncInputs(raw,STATE_B);
    if(id==='bo-b')syncInputs(STATE_A,raw);
    typeset();
  }
  function stepFunction(kind,direction){
    if(kind==='c'){
      STATE_C_INDEX=Math.max(0,Math.min(C_ORDER.length-1,STATE_C_INDEX+direction));
      regenerateLowerTerms();
    }else{
      STATE_G_INDEX=Math.max(0,Math.min(ORDER.length-1,STATE_G_INDEX+direction));
    }
    var dc=defaultC(cKey(),gKey());
    el('bo-c').value=dc;
    if(isThetaMode()){el('bo-c1').value=1;el('bo-c2').value=1;}
    updateConstantControls();
    draw();
  }
  function stepEndpoint(kind,direction){
    if(kind==='a'){
      var nextA=direction>0?nextPower(STATE_A,true):previousPower(STATE_A,true);
      syncInputs(Math.min(nextA,STATE_B-1),STATE_B);
    }else{
      var nextB=direction>0?nextPower(STATE_B,false):previousPower(STATE_B,false);
      syncInputs(STATE_A,Math.max(nextB,STATE_A+1));
    }
    draw();
  }
  function setFunctionPair(ck,gk){
    STATE_C_INDEX=C_ORDER.indexOf(ck);
    STATE_G_INDEX=ORDER.indexOf(gk);
  }
  function resetInterval(){
    syncInputs(0,MAX_B);
  }
  function resetToBookExample(){
    el('bo-lower').value=0;
    resetInterval();
    setFunctionPair('book','n3');
    regenerateLowerTerms();
    var dc=defaultC(cKey(),gKey());
    el('bo-c').value=dc;
    if(isThetaMode()){
      el('bo-c1').value=0.5;
      el('bo-c2').value=2;
    }
    updateConstantControls();
    draw();
  }
  function resetAll(){
    el('bo-scale').value='linear';
    resetToBookExample();
  }
  cv.addEventListener('mousedown',function(ev){
    var p=pointer(ev),ab=interval(),a=ab[0],b=ab[1];
    var da=Math.abs(p.x-tx(a,a,b)),db=Math.abs(p.x-tx(b,a,b));
    drag=da<18?'a':(db<18?'b':'pan');
    panStart={x:p.x,a:a,b:b};
    cv.style.cursor=drag==='pan'?'grabbing':'ew-resize';
  });
  cv.addEventListener('dblclick',function(){
    resetInterval();
    draw();
  });
  cv.addEventListener('mousemove',function(ev){
    if(!drag)return;
    var p=pointer(ev),ab=interval(),a=ab[0],b=ab[1],x=fx(p.x,a,b);
    if(drag==='a')syncInputs(Math.min(Math.max(0,x),b-1),b);
    if(drag==='b')syncInputs(a,Math.max(x,a+1));
    if(drag==='pan' && panStart){
      var span=panStart.b-panStart.a;
      var delta=fx(panStart.x,a,b)-fx(p.x,a,b);
      var na=panStart.a+delta,nb=panStart.b+delta;
      if(na<0){na=0;nb=na+span;}
      if(nb>MAX_B){nb=MAX_B;na=Math.max(0,nb-span);}
      syncInputs(na,nb);
    }
    draw();
  });
  window.addEventListener('mouseup',function(){drag=null;panStart=null;cv.style.cursor='grab';});
  cv.addEventListener('touchstart',function(ev){ev.preventDefault();var p=pointer(ev),ab=interval(),a=ab[0],b=ab[1];var da=Math.abs(p.x-tx(a,a,b)),db=Math.abs(p.x-tx(b,a,b));drag=da<24?'a':(db<24?'b':'pan');panStart={x:p.x,a:a,b:b};});
  cv.addEventListener('touchmove',function(ev){if(!drag)return;ev.preventDefault();var p=pointer(ev),ab=interval(),a=ab[0],b=ab[1],x=fx(p.x,a,b);if(drag==='a')syncInputs(Math.min(Math.max(0,x),b-1),b);if(drag==='b')syncInputs(a,Math.max(x,a+1));if(drag==='pan'&&panStart){var span=panStart.b-panStart.a;var delta=fx(panStart.x,a,b)-fx(p.x,a,b);var na=panStart.a+delta,nb=panStart.b+delta;if(na<0){na=0;nb=na+span;}if(nb>MAX_B){nb=MAX_B;na=Math.max(0,nb-span);}syncInputs(na,nb);}draw();});
  window.addEventListener('touchend',function(){drag=null;panStart=null;});
  ['bo-lower','bo-c','bo-c1','bo-c2','bo-scale'].forEach(function(id){
    el(id).addEventListener('input',function(){
      if(id==='bo-lower'){
        regenerateLowerTerms();
        var dc=defaultC(cKey(),gKey());
        el('bo-c').value=dc;
        if(isThetaMode()){el('bo-c1').value=1;el('bo-c2').value=1;}
      }
      draw();
    });
  });
  el('bo-reset').addEventListener('click',resetAll);
  ['bo-a','bo-b'].forEach(function(id){
    el(id).addEventListener('focus',function(){beginEditableField(id);});
    el(id).addEventListener('input',function(){sanitizeEditableField(id);});
    el(id).addEventListener('blur',function(){handleEndpointInput(id);draw();});
    el(id).addEventListener('keydown',function(ev){
      if(ev.key==='Enter'){ev.preventDefault();el(id).blur();}
    });
  });
  el('bo-cfn-dec').addEventListener('click',function(){stepFunction('c',-1);});
  el('bo-cfn-inc').addEventListener('click',function(){stepFunction('c',1);});
  el('bo-gfn-dec').addEventListener('click',function(){stepFunction('g',-1);});
  el('bo-gfn-inc').addEventListener('click',function(){stepFunction('g',1);});
  el('bo-a-dec').addEventListener('click',function(){stepEndpoint('a',-1);});
  el('bo-a-inc').addEventListener('click',function(){stepEndpoint('a',1);});
  el('bo-b-dec').addEventListener('click',function(){stepEndpoint('b',-1);});
  el('bo-b-inc').addEventListener('click',function(){stepEndpoint('b',1);});
  window.addEventListener('resize',draw);
  regenerateLowerTerms();
  updateConstantControls();
  el('bo-c').value=defaultC(cKey(),gKey());
  el('bo-c1').value=1;
  el('bo-c2').value=1;
  syncInputs(STATE_A,STATE_B);
  draw();
})();
</script>
"""


__all__ = [
    "run_big_o_app",
    "run_little_o_app",
    "run_big_omega_app",
    "run_little_omega_app",
    "run_theta_app",
    "run_app",
]
