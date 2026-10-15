(() => {
  "use strict";

  const masteryGoal = 3;
  const modes = {
    dominant: { level: "Fundamentos", title: "Identifique el término dominante", hint: "Busque el sumando que crece más rápido cuando \\(n\\) aumenta; su coeficiente no cambia la familia." },
    relations: { level: "Comprensión", title: "Seleccione todas las relaciones válidas", hint: "Compare las familias de \\(C(n)\\) y \\(g(n)\\). Después determine si su cociente tiende a cero, a una constante positiva o a infinito." },
    limits: { level: "Definición por límite", title: "Calcule el límite y concluya la relación", hint: "Simplifique el cociente conservando los factores dominantes. Relacione \\(0\\), \\(L>0\\) y \\(+\\infty\\) con \\(o\\), \\(\\Theta\\) y \\(\\omega\\)." },
    witnesses: { level: "Aplicación", title: "Construya testigos para la cota", hint: "Divida entre \\(g(n)\\) y observe la razón resultante. Ajuste primero \\(c\\) y después encuentre desde qué \\(n_0\\) se cumple la desigualdad." },
  };

  const relationLabels = {
    O: "C(n)\\in O(g(n))", o: "C(n)\\in o(g(n))", Omega: "C(n)\\in\\Omega(g(n))",
    omega: "C(n)\\in\\omega(g(n))", Theta: "C(n)\\in\\Theta(g(n))",
  };
  const strongestRelationLabels = { o: relationLabels.o, Theta: relationLabels.Theta, omega: relationLabels.omega };

  function emptyState() {
    return {
      attempts: 0, correct: 0, streak: 0, best: 0,
      mastery: Object.fromEntries(Object.keys(modes).map((key) => [key, 0])),
      seen: Object.fromEntries(Object.keys(modes).map((key) => [key, []])),
    };
  }

  function safeState(panel) {
    const empty = emptyState();
    try {
      const stored = JSON.parse(localStorage.getItem(panel.dataset.storageKey));
      if (!stored || typeof stored !== "object") return empty;
      return {
        attempts: Math.max(0, Number(stored.attempts) || 0), correct: Math.max(0, Number(stored.correct) || 0),
        streak: Math.max(0, Number(stored.streak) || 0), best: Math.max(0, Number(stored.best) || 0),
        mastery: Object.fromEntries(Object.keys(modes).map((key) => [key, Math.min(masteryGoal, Math.max(0, Number(stored.mastery?.[key]) || 0))])),
        seen: Object.fromEntries(Object.keys(modes).map((key) => [key, Array.isArray(stored.seen?.[key]) ? stored.seen[key].filter((item) => typeof item === "string") : []])),
      };
    } catch (_error) { return empty; }
  }

  function saveState(panel, state) {
    try { localStorage.setItem(panel.dataset.storageKey, JSON.stringify(state)); } catch (_error) {
      // La práctica sigue funcionando aunque el navegador bloquee el almacenamiento.
    }
  }

  function randomInt(minimum, maximum) {
    const range = maximum - minimum + 1;
    if (window.crypto?.getRandomValues) {
      const sample = new Uint32Array(1);
      window.crypto.getRandomValues(sample);
      return minimum + (sample[0] % range);
    }
    return minimum + Math.floor(Math.random() * range);
  }

  function shuffled(items) {
    const result = [...items];
    for (let index = result.length - 1; index > 0; index -= 1) {
      const replacement = randomInt(0, index);
      [result[index], result[replacement]] = [result[replacement], result[index]];
    }
    return result;
  }

  function powerTerm(power) { return power === 1 ? "n" : `n^{${power}}`; }

  function familyTex(value) {
    if (value === "log") return "\\Theta(\\log(n))";
    if (value === "linear") return "\\Theta(n)";
    if (value === "nlogn") return "\\Theta(n\\log(n))";
    if (value === "factorial") return "\\Theta(n!)";
    if (value.startsWith("poly:")) return `\\Theta(n^{${value.split(":")[1]}})`;
    return `\\Theta(${value.split(":")[1]}^{n})`;
  }

  function gcd(left, right) {
    let a = Math.abs(left); let b = Math.abs(right);
    while (b) [a, b] = [b, a % b];
    return a;
  }

  function ratioTex(numerator, denominator) {
    const divisor = gcd(numerator, denominator); const top = numerator / divisor; const bottom = denominator / divisor;
    return bottom === 1 ? String(top) : `\\frac{${top}}{${bottom}}`;
  }

  function generateDominant() {
    const kind = randomInt(0, 4); const a = randomInt(2, 97); const b = randomInt(2, 97); const constant = randomInt(1, 97);
    if (kind === 1) return {
      signature: `log:${a}:${b}:${constant}`, expression: `${a}n\\log(n)+${b}n+${constant}`, answer: "nlogn",
      options: shuffled(["linear", "log", "nlogn", "poly:2"]),
      reason: "El factor \\(\\log(n)\\) hace que \\(n\\log(n)\\) domine al término lineal.",
    };
    if (kind === 2) {
      const base = randomInt(2, 9); const degree = randomInt(2, 7);
      return {
        signature: `exp:${a}:${base}:${b}:${degree}:${constant}`, expression: `${a}\\cdot ${base}^{n}+${b}n^{${degree}}+${constant}`,
        answer: `exp:${base}`, options: shuffled([`poly:${degree}`, `exp:${base}`, "factorial", "nlogn"]),
        reason: "Una exponencial de base mayor que uno termina superando a cualquier polinomio de grado fijo.",
      };
    }
    if (kind === 3) {
      const base = randomInt(2, 6);
      return {
        signature: `factorial:${a}:${b}:${base}:${constant}`, expression: `${a}n!+${b}\\cdot ${base}^{n}+${constant}`,
        answer: "factorial", options: shuffled(["factorial", `exp:${base}`, "nlogn", "poly:4"]),
        reason: "El factorial termina superando a toda exponencial de base constante y, por tanto, también a los términos polinómicos y log-lineales.",
      };
    }
    if (kind === 4) return {
      signature: `linear:${a}:${b}:${constant}`, expression: `${a}n+${b}\\log(n)+${constant}`, answer: "linear",
      options: shuffled(["log", "linear", "nlogn", "poly:2"]),
      reason: "El término lineal crece más rápido que el logarítmico; los coeficientes y la constante no alteran esa comparación.",
    };
    const degree = randomInt(2, 8); const lowerDegree = randomInt(1, degree - 1); const optionDegrees = [];
    [degree, lowerDegree, degree + 1, degree + 2, 1].forEach((value) => {
      if (!optionDegrees.includes(value) && optionDegrees.length < 4) optionDegrees.push(value);
    });
    return {
      signature: `poly:${a}:${degree}:${b}:${lowerDegree}:${constant}`,
      expression: `${a}n^{${degree}}+${b}${powerTerm(lowerDegree)}+${constant}`, answer: `poly:${degree}`,
      options: shuffled(optionDegrees.map((value) => `poly:${value}`)),
      reason: `El exponente mayor es \\(${degree}\\); los términos de grados menores se vuelven relativamente despreciables.`,
    };
  }

  const comparisonFamilies = [
    { key: "log", name: "logarítmica", expression: (coefficient, constant) => `${coefficient}\\log(n)+${constant}` },
    { key: "linear", name: "lineal", expression: (coefficient, constant) => `${coefficient}n+${constant}` },
    { key: "nlogn", name: "log-lineal", expression: (coefficient, constant) => `${coefficient}n\\log(n)+${constant}` },
    { key: "quadratic", name: "cuadrática", expression: (coefficient, constant) => `${coefficient}n^{2}+${constant}` },
    { key: "cubic", name: "cúbica", expression: (coefficient, constant) => `${coefficient}n^{3}+${constant}` },
    { key: "exponential", name: "exponencial", expression: (coefficient, constant) => `${coefficient}\\cdot 2^{n}+${constant}` },
    { key: "factorial", name: "factorial", expression: (coefficient, constant) => `${coefficient}n!+${constant}` },
  ];

  function generateComparison() {
    const caseType = ["zero", "positive", "infinity"][randomInt(0, 2)]; let leftIndex; let rightIndex;
    if (caseType === "positive") leftIndex = rightIndex = randomInt(0, comparisonFamilies.length - 1);
    else {
      const slower = randomInt(0, comparisonFamilies.length - 2); const faster = randomInt(slower + 1, comparisonFamilies.length - 1);
      [leftIndex, rightIndex] = caseType === "zero" ? [slower, faster] : [faster, slower];
    }
    const leftCoefficient = randomInt(1, 47); const rightCoefficient = randomInt(1, 47);
    const leftConstant = randomInt(1, 97); const rightConstant = randomInt(1, 97);
    const leftFamily = comparisonFamilies[leftIndex]; const rightFamily = comparisonFamilies[rightIndex];
    const answers = { zero: ["O", "o"], positive: ["O", "Omega", "Theta"], infinity: ["Omega", "omega"] };
    const strongest = { zero: "o", positive: "Theta", infinity: "omega" };
    const limit = caseType === "positive" ? ratioTex(leftCoefficient, rightCoefficient) : (caseType === "zero" ? "0" : "+\\infty");
    return {
      signature: `comparison:${leftFamily.key}:${rightFamily.key}:${leftCoefficient}:${leftConstant}:${rightCoefficient}:${rightConstant}`,
      left: leftFamily.expression(leftCoefficient, leftConstant), right: rightFamily.expression(rightCoefficient, rightConstant),
      answer: answers[caseType], answerLimit: caseType, answerRelation: strongest[caseType], limit,
      ratio: ratioTex(leftCoefficient, rightCoefficient),
      reason: caseType === "zero" ? `El cociente tiende a \\(0\\): la familia ${leftFamily.name} crece estrictamente más lento que la ${rightFamily.name}.`
        : caseType === "positive" ? `El cociente tiende a \\(${limit}\\), una constante positiva: existen cota superior, inferior y ajustada.`
          : `El cociente tiende a \\(+\\infty\\): la familia ${leftFamily.name} crece estrictamente más rápido que la ${rightFamily.name}.`,
    };
  }

  function generateWitness() {
    const relation = randomInt(0, 1) ? "O" : "Omega"; const family = ["linear", "log", "nlogn", "poly"][randomInt(0, 3)];
    const a = randomInt(3, 24); const b = relation === "Omega" ? randomInt(1, a) : randomInt(1, 36); const power = randomInt(2, 6);
    return { signature: `witness:${relation}:${family}:${a}:${b}:${power}`, relation, family, a, b, power, sign: relation === "O" ? 1 : -1 };
  }

  function fallbackQuestion(mode, index) {
    const unique = 10000 + index;
    if (mode === "dominant") return { signature: `fallback-d:${unique}`, expression: `${unique}n^{4}+3n+1`, answer: "poly:4", options: shuffled(["poly:3", "poly:4", "poly:5", "nlogn"]), reason: "El grado mayor es \\(4\\)." };
    if (mode === "witnesses") return { signature: `fallback-w:${unique}`, relation: "O", family: "poly", a: unique, b: 7, power: 3, sign: 1 };
    return {
      signature: `fallback-${mode}:${unique}`, left: `${unique}n^{2}+1`, right: "n^{3}+1", answer: ["O", "o"],
      answerLimit: "zero", answerRelation: "o", limit: "0", ratio: String(unique), reason: "El cociente tiende a \\(0\\): el numerador tiene menor grado.",
    };
  }

  function nextUniqueQuestion(mode, state) {
    const seen = new Set(state.seen[mode]);
    for (let attempt = 0; attempt < 1000; attempt += 1) {
      const question = mode === "dominant" ? generateDominant() : (mode === "witnesses" ? generateWitness() : generateComparison());
      if (!seen.has(question.signature)) { state.seen[mode].push(question.signature); return question; }
    }
    const fallback = fallbackQuestion(mode, state.seen[mode].length); state.seen[mode].push(fallback.signature); return fallback;
  }

  function clearMath(element) { if (typeof window.MathJax?.typesetClear === "function") window.MathJax.typesetClear([element]); }
  function typesetMath(element) {
    if (typeof window.MathJax?.typesetPromise !== "function") return;
    window.MathJax.typesetPromise([element]).catch(() => {});
  }

  function renderDominant(container, question) {
    clearMath(container);
    container.innerHTML = `<p class="self-check-practice__prompt">Clasifique <strong>\\(C(n)=${question.expression}\\)</strong> por su crecimiento ajustado.</p>
      <fieldset class="self-check-practice__choices"><legend>Seleccione una respuesta</legend>${question.options.map((option) => `<label><input type="radio" name="dominant-answer" value="${option}"><span>\\(${familyTex(option)}\\)</span></label>`).join("")}</fieldset>`;
    typesetMath(container);
  }

  function renderRelations(container, question) {
    clearMath(container);
    container.innerHTML = `<p class="self-check-practice__prompt">Compare las dos funciones y marque todas las afirmaciones verdaderas.</p>
      <div class="self-check-practice__formula self-check-practice__formula--pair">\\[C(n)=${question.left}\\qquad g(n)=${question.right}\\]</div>
      <fieldset class="self-check-practice__choices self-check-practice__choices--relations"><legend>Puede haber más de una respuesta</legend>${Object.entries(relationLabels).map(([value, label]) => `<label><input type="checkbox" name="relation-answer" value="${value}"><span>\\(${label}\\)</span></label>`).join("")}</fieldset>`;
    typesetMath(container);
  }

  function renderLimits(container, question) {
    const limitOptions = shuffled([{ value: "zero", tex: "0" }, { value: "positive", tex: question.ratio }, { value: "infinity", tex: "+\\infty" }]);
    clearMath(container);
    container.innerHTML = `<p class="self-check-practice__prompt">Use la definición mediante el cociente para comparar <strong>\\(C(n)=${question.left}\\)</strong> y <strong>\\(g(n)=${question.right}\\)</strong>.</p>
      <div class="self-check-practice__formula">\\[\\lim_{n\\to\\infty}\\frac{C(n)}{g(n)}=\\lim_{n\\to\\infty}\\frac{${question.left}}{${question.right}}\\]</div>
      <fieldset class="self-check-practice__choices self-check-practice__choices--limits"><legend>1. Valor del límite</legend>${limitOptions.map((option) => `<label><input type="radio" name="limit-answer" value="${option.value}"><span>\\(${option.tex}\\)</span></label>`).join("")}</fieldset>
      <fieldset class="self-check-practice__choices self-check-practice__choices--limits"><legend>2. Relación más precisa que se deduce</legend>${Object.entries(strongestRelationLabels).map(([value, label]) => `<label><input type="radio" name="limit-relation" value="${value}"><span>\\(${label}\\)</span></label>`).join("")}</fieldset>`;
    typesetMath(container);
  }

  function witnessTerms(question) {
    if (question.family === "linear") return { gTex: "n", lowerTex: "1", g: (n) => n, lower: () => 1, minimumType: "inverse", minimumN: 1 };
    if (question.family === "log") return { gTex: "\\log(n)", lowerTex: "1", g: (n) => Math.log(n), lower: () => 1, minimumType: "log", minimumN: 2 };
    if (question.family === "nlogn") return { gTex: "n\\log(n)", lowerTex: "n", g: (n) => n * Math.log(n), lower: (n) => n, minimumType: "log", minimumN: 2 };
    return { gTex: powerTerm(question.power), lowerTex: powerTerm(question.power - 1), g: (n) => n ** question.power, lower: (n) => n ** (question.power - 1), minimumType: "inverse", minimumN: 1 };
  }

  function witnessMinimum(question, c) {
    const terms = witnessTerms(question); const gap = question.relation === "O" ? c - question.a : question.a - c;
    if (gap <= 0) return Number.POSITIVE_INFINITY;
    const raw = terms.minimumType === "log" ? Math.exp(question.b / gap) : question.b / gap;
    return Math.max(terms.minimumN, Math.ceil(raw - 1e-10));
  }

  function witnessDefaultC(question) {
    const terms = witnessTerms(question);
    if (question.relation === "Omega") return Math.max(0.1, question.a / 2);
    return terms.minimumType === "log" ? question.a + (question.b / Math.log(5)) : question.a + (question.b / 5);
  }

  function niceTicks(lower, upper, count) {
    const range = Math.max(upper - lower, 1e-9); const raw = range / count; const power = 10 ** Math.floor(Math.log10(raw));
    const multiplier = [1, 2, 5, 10].find((candidate) => raw <= candidate * power) || 10; const step = multiplier * power;
    const ticks = []; for (let value = Math.ceil(lower / step) * step; value <= upper + (step * .5); value += step) ticks.push(value);
    return ticks;
  }

  function graphNumber(value) { return Number(value.toFixed(2)).toString(); }

  function drawWitnessGraph(canvas, question, c, n0, viewStart, viewEnd, dragState = null) {
    const context = canvas.getContext("2d"); if (!context || !Number.isFinite(c) || !Number.isFinite(n0)) return;
    const ratio = window.devicePixelRatio || 1; const width = Math.max(300, canvas.clientWidth); const height = 250;
    canvas.width = Math.round(width * ratio); canvas.height = Math.round(height * ratio); context.setTransform(ratio, 0, 0, ratio, 0, 0);
    const colors = { curve: "#1565C0", bound: question.relation === "O" ? "#B71C1C" : "#EF6C00", n0: "#2E7D32", grid: "#dddddd", axis: "#333333" };
    const terms = witnessTerms(question); const minimumN = viewStart; const xMax = viewEnd; const padding = { left: 86, right: 18, top: 18, bottom: 48 };
    const plotWidth = width - padding.left - padding.right; const plotHeight = height - padding.top - padding.bottom;
    const values = []; let yMax = 1;
    for (let index = 0; index <= 80; index += 1) {
      const n = minimumN + ((xMax - minimumN) * index / 80); const base = terms.g(n); const curve = (question.a * base) + (question.sign * question.b * terms.lower(n)); const bound = c * base;
      values.push({ n, curve, bound }); yMax = Math.max(yMax, curve, bound);
    }
    if (dragState?.fixedYMax) yMax = dragState.fixedYMax;
    else yMax *= 1.08;
    const x = (n) => padding.left + ((n - minimumN) / (xMax - minimumN)) * plotWidth;
    const y = (value) => padding.top + plotHeight - (Math.max(0, value) / yMax) * plotHeight;
    const axisScale = (maximum) => { const exponent = Math.max(0, Math.floor(Math.log10(Math.max(1, maximum)))); return exponent < 4 ? { scale: 1, label: "" } : { scale: 10 ** exponent, label: `×10^${exponent}` }; };
    const xScale = axisScale(xMax); const yScale = axisScale(yMax); const tickText = (value, scale) => { const scaled = value / scale; return scaled.toFixed(2).replace(/\.?0+$/, ""); };
    context.fillStyle = "#ffffff"; context.fillRect(0, 0, width, height); context.font = "12px sans-serif"; context.lineWidth = .7; context.strokeStyle = colors.grid; context.fillStyle = colors.axis;
    niceTicks(minimumN, xMax, 5).forEach((value) => { const px = x(value); context.beginPath(); context.moveTo(px, padding.top); context.lineTo(px, padding.top + plotHeight); context.stroke(); context.textAlign = "center"; context.textBaseline = "top"; context.fillText(tickText(value, xScale.scale), px, padding.top + plotHeight + 7); });
    niceTicks(0, yMax, 5).forEach((value) => { const py = y(value); context.beginPath(); context.moveTo(padding.left, py); context.lineTo(width - padding.right, py); context.stroke(); context.textAlign = "right"; context.textBaseline = "middle"; context.fillText(tickText(value, yScale.scale), padding.left - 7, py); });
    context.textAlign = "right"; context.textBaseline = "top"; if (xScale.label) context.fillText(xScale.label, width - padding.right, padding.top + plotHeight + 22); context.textBaseline = "bottom"; if (yScale.label) context.fillText(yScale.label, padding.left, padding.top - 3);
    const valid = values.filter((point) => point.n >= n0 && (question.relation === "O" ? point.bound >= point.curve : point.curve >= point.bound));
    if (valid.length > 1) {
      context.fillStyle = question.relation === "O" ? "rgba(183,28,28,.30)" : "rgba(21,101,192,.25)"; context.beginPath();
      valid.forEach((point, index) => context[index ? "lineTo" : "moveTo"](x(point.n), y(question.relation === "O" ? point.bound : point.curve)));
      for (let index = valid.length - 1; index >= 0; index -= 1) context.lineTo(x(valid[index].n), y(question.relation === "O" ? valid[index].curve : valid[index].bound));
      context.closePath(); context.fill();
    }
    const plot = (key, color, dash = []) => { context.strokeStyle = color; context.lineWidth = 2.2; context.setLineDash(dash); context.beginPath(); values.forEach((point, index) => { const method = index ? "lineTo" : "moveTo"; context[method](x(point.n), y(point[key])); }); context.stroke(); context.setLineDash([]); };
    plot("curve", colors.curve); plot("bound", colors.bound);
    context.strokeStyle = colors.axis; context.lineWidth = 1.2; context.beginPath(); context.moveTo(padding.left, padding.top); context.lineTo(padding.left, padding.top + plotHeight); context.lineTo(width - padding.right, padding.top + plotHeight); context.stroke();
    const n0X = x(Math.min(xMax, Math.max(minimumN, n0))); context.strokeStyle = colors.n0; context.lineWidth = 1.5; context.setLineDash([3, 4]); context.beginPath(); context.moveTo(n0X, padding.top); context.lineTo(n0X, padding.top + plotHeight); context.stroke(); context.setLineDash([]);
    const handleN = minimumN + ((xMax - minimumN) * .76); const handleY = y(c * terms.g(handleN)); const handleX = x(handleN);
    context.fillStyle = colors.axis; context.textAlign = "center"; context.textBaseline = "bottom"; context.fillText("Tamaño de la entrada (n)", padding.left + (plotWidth / 2), height - 3);
    context.save(); context.translate(12, padding.top + (plotHeight / 2)); context.rotate(-Math.PI / 2); context.textAlign = "center"; context.textBaseline = "top"; context.fillText("Complejidad", 0, 0); context.restore();
    canvas._witnessGeometry = { padding, plotWidth, plotHeight, minimumN, xMax, yMax, handleX, handleY, n0X, terms };
  }

  function setupWitnessGraph(container, question) {
    const canvas = container.querySelector("[data-witness-graph]"); const cInput = container.querySelector("input[name='witness-c']"); const n0Input = container.querySelector("input[name='witness-n0']");
    const startInput = container.querySelector("input[name='witness-view-start']"); const endInput = container.querySelector("input[name='witness-view-end']"); const live = container.querySelector("[data-witness-graph-status]");
    const legendC = container.querySelector("[data-witness-legend-c]"); const legendBound = container.querySelector("[data-witness-legend-bound]"); const legendN0 = container.querySelector("[data-witness-legend-n0]");
    let drag = null;
    const redraw = () => {
      const c = parseDecimal(cInput.value); const n0 = Number(n0Input.value); const start = Number(startInput.value); const end = Number(endInput.value);
      if (!Number.isFinite(start) || !Number.isFinite(end) || end <= start) { live.textContent = "El extremo final del intervalo debe ser mayor que el inicial."; return; }
      drawWitnessGraph(canvas, question, c, n0, start, end, drag);
      const operator = question.sign > 0 ? "+" : "-"; const terms = witnessTerms(question); const lower = terms.lowerTex === "1" ? "" : terms.lowerTex;
      const legendSignature = `${c}:${n0}`;
      if (legendC.parentElement.parentElement.dataset.signature !== legendSignature) {
        const legend = legendC.parentElement.parentElement; clearMath(legend);
        legendC.innerHTML = `\\(C(n)=${question.a}${terms.gTex}${operator}${question.b}${lower}\\)`;
        legendBound.innerHTML = `\\(c\\cdot g(n)=${graphNumber(c)}\\cdot ${terms.gTex}\\)`;
        legendN0.innerHTML = `\\(n_0=${n0}\\)`; legend.dataset.signature = legendSignature; typesetMath(legend);
      }
      live.textContent = `Gráfica actualizada: intervalo de ${start} a ${end}, c = ${Number.isFinite(c) ? c.toFixed(2) : "—"} y n₀ = ${Number.isFinite(n0) ? n0 : "—"}.`;
    };
    [cInput, n0Input, startInput, endInput].forEach((input) => input.addEventListener("input", redraw));
    const position = (event) => { const rect = canvas.getBoundingClientRect(); return { x: event.clientX - rect.left, y: event.clientY - rect.top }; };
    canvas.addEventListener("pointerdown", (event) => {
      if (cInput.disabled || n0Input.disabled) return; const point = position(event); const geometry = canvas._witnessGeometry; if (!geometry) return;
      const cDistance = Math.hypot(point.x - geometry.handleX, point.y - geometry.handleY); const n0Distance = Math.abs(point.x - geometry.n0X);
      drag = { kind: cDistance < 24 ? "c" : (n0Distance < 24 ? "n0" : (cDistance < n0Distance ? "c" : "n0")), fixedYMax: geometry.yMax };
      canvas.setPointerCapture(event.pointerId); canvas.dataset.dragging = drag.kind; event.preventDefault();
    });
    canvas.addEventListener("pointermove", (event) => {
      if (!drag) return; const point = position(event); const geometry = canvas._witnessGeometry;
      if (drag.kind === "n0") {
        const value = geometry.minimumN + ((point.x - geometry.padding.left) / geometry.plotWidth) * (geometry.xMax - geometry.minimumN);
        n0Input.value = String(Math.max(geometry.minimumN, Math.round(value)));
      } else {
        const dataY = Math.max(.05, ((geometry.padding.top + geometry.plotHeight - point.y) / geometry.plotHeight) * drag.fixedYMax);
        cInput.value = String(Math.max(.05, dataY / geometry.terms.g(geometry.minimumN + ((geometry.xMax - geometry.minimumN) * .76))).toFixed(2));
      }
      redraw();
    });
    const stop = (event) => { if (!drag) return; drag = null; delete canvas.dataset.dragging; if (canvas.hasPointerCapture(event.pointerId)) canvas.releasePointerCapture(event.pointerId); redraw(); };
    canvas.addEventListener("pointerup", stop); canvas.addEventListener("pointercancel", stop); redraw();
    if (typeof ResizeObserver === "function") new ResizeObserver(redraw).observe(canvas);
  }

  function renderWitnesses(container, question) {
    const terms = witnessTerms(question); const operator = question.sign > 0 ? "+" : "-";
    const symbol = question.relation === "O" ? "\\leq" : "\\geq"; const notation = question.relation === "Omega" ? "\\Omega" : "O";
    const initialC = witnessDefaultC(question); const initialN0 = witnessMinimum(question, initialC); const graphDomainStart = terms.minimumN === 2 ? 1 : 0;
    const graphSpan = Math.max(12, Math.ceil(initialN0 * .6)); const graphStart = Math.max(graphDomainStart, initialN0 - Math.ceil(graphSpan / 2)); const graphEnd = graphStart + graphSpan;
    clearMath(container);
    container.innerHTML = `<p class="self-check-practice__prompt">Proponga <strong>\\(c&gt;0\\)</strong> y un <strong>\\(n_0\\) natural positivo</strong> que demuestren que</p>
      <div class="self-check-practice__formula self-check-practice__formula--plain">\\[C(n)=${question.a}${terms.gTex}${operator}${question.b}${terms.lowerTex === "1" ? "" : terms.lowerTex}\\in ${notation}(${terms.gTex})\\]</div>
      <p>Sus valores deben hacer verdadera <strong>\\(C(n)${symbol} c\\cdot g(n)\\)</strong>, con <strong>\\(g(n)=${terms.gTex}\\)</strong>, para todo <strong>\\(n\\geq n_0\\)</strong>.</p>
      <div class="self-check-practice__number-fields"><label><span>Constante \\(\\mathbf{c}\\)</span><input type="text" inputmode="decimal" autocomplete="off" name="witness-c" aria-describedby="witness-format" value="${initialC.toFixed(2)}"></label><label><span>Umbral \\(\\mathbf{n}_0\\)</span><input type="number" inputmode="numeric" min="${terms.minimumN}" step="1" name="witness-n0" value="${initialN0}"></label></div><small id="witness-format">Puede escribir los valores o arrastrar la curva de la cota y la línea vertical de la gráfica.</small>
      <p class="self-check-practice__graph-intro">Puede usar la gráfica presentada a continuación para verificar los valores que va a seleccionar de forma visual:</p>
      <div class="self-check-practice__interval-fields" aria-label="Intervalo visible de la gráfica"><label><span>Desde \\(n\\)</span><input type="number" inputmode="numeric" step="1" name="witness-view-start" value="${graphStart}"></label><label><span>Hasta \\(n\\)</span><input type="number" inputmode="numeric" step="1" name="witness-view-end" value="${graphEnd}"></label></div>
      <div class="self-check-practice__graph${question.relation === "Omega" ? " self-check-practice__graph--lower" : ""}"><canvas data-witness-graph role="img" aria-label="Comparación interactiva entre C de n y c por g de n. Arrastre la curva de la cota para cambiar c o la línea vertical para cambiar n cero."></canvas><div class="self-check-practice__graph-legend" aria-label="Leyenda de la gráfica"><span class="self-check-practice__legend-row self-check-practice__legend-row--curve"><i aria-hidden="true"></i><span data-witness-legend-c></span></span><span class="self-check-practice__legend-row self-check-practice__legend-row--bound"><i aria-hidden="true"></i><span data-witness-legend-bound></span></span><span class="self-check-practice__legend-row self-check-practice__legend-row--n0"><i aria-hidden="true"></i><span data-witness-legend-n0></span></span></div></div><span class="self-check-practice__sr-status" data-witness-graph-status aria-live="polite"></span>`;
    typesetMath(container); setupWitnessGraph(container, question);
  }

  function parseDecimal(value) { const normalized = value.trim().replace(",", "."); return normalized === "" ? Number.NaN : Number(normalized); }
  function sameSet(actual, expected) { return actual.size === expected.length && expected.every((value) => actual.has(value)); }

  function evaluateDominant(container, question) {
    const selected = container.querySelector("input[name='dominant-answer']:checked");
    if (!selected) return { incomplete: true, message: "Seleccione una clasificación antes de comprobar." };
    return selected.value === question.answer ? { correct: true, message: `Correcto. ${question.reason}` } : { correct: false, message: `Revise primero el término que crece más rápido. ${question.reason}` };
  }

  function evaluateRelations(container, question) {
    const selected = new Set(Array.from(container.querySelectorAll("input[name='relation-answer']:checked"), (input) => input.value));
    if (!selected.size) return { incomplete: true, message: "Marque al menos una relación antes de comprobar." };
    if (sameSet(selected, question.answer)) return { correct: true, message: `Correcto. ${question.reason}` };
    const expected = new Set(question.answer); const invalid = Array.from(selected).find((value) => !expected.has(value));
    if (invalid) return { correct: false, message: `La afirmación \\(${relationLabels[invalid]}\\) no corresponde al cociente. Aquí el límite es \\(${question.limit}\\).` };
    const missing = question.answer.find((value) => !selected.has(value));
    return { correct: false, message: `La selección es incompleta: revise también \\(${relationLabels[missing]}\\). Aquí el límite es \\(${question.limit}\\).` };
  }

  function evaluateLimits(container, question) {
    const limit = container.querySelector("input[name='limit-answer']:checked"); const relation = container.querySelector("input[name='limit-relation']:checked");
    if (!limit || !relation) return { incomplete: true, message: "Complete el valor del límite y la relación que se deduce." };
    if (limit.value !== question.answerLimit) return { correct: false, message: `Revise primero las familias dominantes del numerador y del denominador. El cociente tiende a \\(${question.limit}\\).` };
    if (relation.value !== question.answerRelation) return { correct: false, message: `El límite es correcto. De \\(${question.limit}\\) se deduce \\(${strongestRelationLabels[question.answerRelation]}\\).` };
    return { correct: true, message: `Correcto. \\(\\lim_{n\\to\\infty}C(n)/g(n)=${question.limit}\\), por lo que \\(${strongestRelationLabels[question.answerRelation]}\\).` };
  }

  function evaluateWitnesses(container, question) {
    const c = parseDecimal(container.querySelector("input[name='witness-c']").value); const n0 = Number(container.querySelector("input[name='witness-n0']").value);
    if (!Number.isFinite(c) || !Number.isFinite(n0)) return { incomplete: true, message: "Complete \\(c\\) y \\(n_0\\) antes de comprobar." };
    if (c <= 0) return { correct: false, message: "El primer requisito que falla es \\(c>0\\)." };
    if (!Number.isInteger(n0) || n0 < 1) return { correct: false, message: "\\(n_0\\) debe ser un natural positivo." };
    if (question.relation === "O") {
      if (c <= question.a) return { correct: false, message: `Necesita \\(c>${question.a}\\).` };
      const minimum = witnessMinimum(question, c);
      if (n0 < minimum) return { correct: false, message: `Con \\(c=${c}\\), necesita \\(n_0\\geq ${minimum}\\).` };
      return { correct: true, message: `Correcto: \\(C(n)/g(n)\\leq ${c}\\) desde \\(n=${n0}\\).` };
    }
    if (c >= question.a) return { correct: false, message: `Elija \\(0<c<${question.a}\\).` };
    const minimum = witnessMinimum(question, c);
    if (n0 < minimum) return { correct: false, message: `Con \\(c=${c}\\), necesita \\(n_0\\geq ${minimum}\\).` };
    return { correct: true, message: `Correcto: \\(C(n)/g(n)\\geq ${c}\\) desde \\(n=${n0}\\).` };
  }

  function initializePractice(panel) {
    if (panel.dataset.initialized) return; panel.dataset.initialized = "true";
    let state = safeState(panel); let mode = "dominant"; let current; let solved = false;
    const questionContainer = panel.querySelector("[data-practice-question]"); const feedback = panel.querySelector("[data-practice-feedback]");
    const checkLabel = panel.querySelector("[data-practice-check-label]");
    const renderProgress = () => {
      panel.querySelector("[data-practice-correct]").textContent = state.correct; panel.querySelector("[data-practice-attempts]").textContent = state.attempts; panel.querySelector("[data-practice-best]").textContent = state.best;
      Object.keys(modes).forEach((key) => { const value = state.mastery[key]; const meter = panel.querySelector(`[data-mastery='${key}']`); meter.value = value; meter.textContent = `${value} de ${masteryGoal}`; panel.querySelector(`[data-mastery-label='${key}']`).textContent = value >= masteryGoal ? "Afianzada" : `${value}/${masteryGoal}`; });
    };
    const showFeedback = (kind, message, focus = false) => { clearMath(feedback); feedback.dataset.state = kind; feedback.innerHTML = message; typesetMath(feedback); if (focus) feedback.focus({ preventScroll: true }); };
    const newQuestion = () => {
      current = nextUniqueQuestion(mode, state); saveState(panel, state); solved = false;
      panel.querySelector("[data-practice-level]").textContent = modes[mode].level; panel.querySelector("[data-practice-title]").textContent = modes[mode].title;
      ({ dominant: renderDominant, relations: renderRelations, limits: renderLimits, witnesses: renderWitnesses })[mode](questionContainer, current);
      checkLabel.textContent = "Comprobar respuesta"; showFeedback("", "");
    };
    const checkAnswer = () => {
      if (solved) { newQuestion(); return; }
      const result = ({ dominant: evaluateDominant, relations: evaluateRelations, limits: evaluateLimits, witnesses: evaluateWitnesses })[mode](questionContainer, current);
      if (result.incomplete) { showFeedback("hint", result.message, true); return; }
      state.attempts += 1;
      if (result.correct) { solved = true; state.correct += 1; state.streak += 1; state.best = Math.max(state.best, state.streak); state.mastery[mode] = Math.min(masteryGoal, state.mastery[mode] + 1); questionContainer.querySelectorAll("input").forEach((input) => { input.disabled = true; }); checkLabel.textContent = "Siguiente ejercicio"; showFeedback("correct", result.message, true); }
      else { state.streak = 0; showFeedback("error", result.message, true); }
      saveState(panel, state); renderProgress();
    };
    panel.querySelectorAll("[data-practice-mode]").forEach((button) => button.addEventListener("click", () => { mode = button.dataset.practiceMode; panel.querySelectorAll("[data-practice-mode]").forEach((candidate) => candidate.setAttribute("aria-pressed", String(candidate === button))); newQuestion(); }));
    panel.querySelector("[data-practice-new]").addEventListener("click", newQuestion);
    panel.querySelector("[data-practice-hint]").addEventListener("click", () => showFeedback("hint", modes[mode].hint, true));
    panel.querySelector("[data-practice-reset]").addEventListener("click", () => { state = emptyState(); saveState(panel, state); renderProgress(); newQuestion(); showFeedback("hint", "El progreso y el historial de ejercicios se reiniciaron.", true); });
    panel.querySelector("[data-practice-check]").addEventListener("click", checkAnswer);
    questionContainer.addEventListener("keydown", (event) => { if (event.key === "Enter" && !event.shiftKey) { event.preventDefault(); checkAnswer(); } });
    renderProgress(); newQuestion();
  }

  function prepareChapter3Practice(root = document) { root.querySelectorAll("[data-chapter3-practice]").forEach(initializePractice); }
  if (typeof document$ !== "undefined") document$.subscribe(prepareChapter3Practice);
  else document.addEventListener("DOMContentLoaded", () => prepareChapter3Practice());
})();
