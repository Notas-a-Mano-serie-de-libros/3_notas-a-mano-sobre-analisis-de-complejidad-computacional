(() => {
  "use strict";

  const masteryGoal = 3;
  const modes = {
    dominant: { level: "Fundamentos", title: "Identifique el término dominante", hint: "Busque el sumando que crece más rápido cuando \\(n\\) aumenta; su coeficiente no cambia la familia." },
    relations: { level: "Comprensión", title: "Seleccione todas las relaciones válidas", hint: "Compare los grados de \\(C(n)\\) y \\(g(n)\\). Después determine si su cociente tiende a cero, a una constante positiva o a infinito." },
    limits: { level: "Definición por límite", title: "Calcule el límite y concluya la relación", hint: "Divida numerador y denominador entre la mayor potencia de \\(n\\). Relacione \\(0\\), \\(L>0\\) y \\(+\\infty\\) con \\(o\\), \\(\\Theta\\) y \\(\\omega\\)." },
    witnesses: { level: "Aplicación", title: "Construya testigos para la cota", hint: "Divida la desigualdad entre la mayor potencia de \\(n\\) y despeje el término que contiene \\(1/n\\)." },
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
    const kind = randomInt(0, 2); const a = randomInt(2, 97); const b = randomInt(2, 97); const constant = randomInt(1, 97);
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

  function generateComparison() {
    const caseType = ["zero", "positive", "infinity"][randomInt(0, 2)]; let leftDegree; let rightDegree;
    if (caseType === "zero") { leftDegree = randomInt(1, 6); rightDegree = randomInt(leftDegree + 1, 9); }
    else if (caseType === "infinity") { rightDegree = randomInt(1, 6); leftDegree = randomInt(rightDegree + 1, 9); }
    else { leftDegree = randomInt(1, 8); rightDegree = leftDegree; }
    const leftCoefficient = randomInt(1, 47); const rightCoefficient = randomInt(1, 47);
    const leftConstant = randomInt(1, 97); const rightConstant = randomInt(1, 97);
    const answers = { zero: ["O", "o"], positive: ["O", "Omega", "Theta"], infinity: ["Omega", "omega"] };
    const strongest = { zero: "o", positive: "Theta", infinity: "omega" };
    const limit = caseType === "positive" ? ratioTex(leftCoefficient, rightCoefficient) : (caseType === "zero" ? "0" : "+\\infty");
    return {
      signature: `comparison:${leftCoefficient}:${leftDegree}:${leftConstant}:${rightCoefficient}:${rightDegree}:${rightConstant}`,
      left: `${leftCoefficient}${powerTerm(leftDegree)}+${leftConstant}`, right: `${rightCoefficient}${powerTerm(rightDegree)}+${rightConstant}`,
      answer: answers[caseType], answerLimit: caseType, answerRelation: strongest[caseType], limit,
      ratio: ratioTex(leftCoefficient, rightCoefficient),
      reason: caseType === "zero" ? "El cociente tiende a \\(0\\): \\(C\\) crece estrictamente más lento que \\(g\\)."
        : caseType === "positive" ? `El cociente tiende a \\(${limit}\\), una constante positiva: existen cota superior, inferior y ajustada.`
          : "El cociente tiende a \\(+\\infty\\): \\(C\\) crece estrictamente más rápido que \\(g\\).",
    };
  }

  function generateWitness() {
    const relation = randomInt(0, 1) ? "O" : "Omega"; const a = randomInt(2, 49); const b = randomInt(1, 97); const power = randomInt(2, 9);
    return { signature: `witness:${relation}:${a}:${b}:${power}`, relation, a, b, power, sign: relation === "O" ? 1 : -1 };
  }

  function fallbackQuestion(mode, index) {
    const unique = 10000 + index;
    if (mode === "dominant") return { signature: `fallback-d:${unique}`, expression: `${unique}n^{4}+3n+1`, answer: "poly:4", options: shuffled(["poly:3", "poly:4", "poly:5", "nlogn"]), reason: "El grado mayor es \\(4\\)." };
    if (mode === "witnesses") return { signature: `fallback-w:${unique}`, relation: "O", a: unique, b: 7, power: 3, sign: 1 };
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
    container.innerHTML = `<p class="self-check-practice__prompt">Para <strong>\\(C(n)=${question.left}\\)</strong> y <strong>\\(g(n)=${question.right}\\)</strong>, marque todas las afirmaciones verdaderas.</p>
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

  function renderWitnesses(container, question) {
    const lowerPower = powerTerm(question.power - 1); const operator = question.sign > 0 ? "+" : "-";
    const symbol = question.relation === "O" ? "\\leq" : "\\geq"; const notation = question.relation === "Omega" ? "\\Omega" : "O";
    clearMath(container);
    container.innerHTML = `<p class="self-check-practice__prompt">Proponga <strong>\\(c&gt;0\\)</strong> y un <strong>\\(n_0\\) natural positivo</strong> que demuestren que</p>
      <div class="self-check-practice__formula">\\[C(n)=${question.a}${powerTerm(question.power)}${operator}${question.b}${lowerPower}\\in ${notation}(${powerTerm(question.power)})\\]</div>
      <p>Sus valores deben hacer verdadera <strong>\\(C(n)${symbol} c\\cdot ${powerTerm(question.power)}\\)</strong> para todo <strong>\\(n\\geq n_0\\)</strong>.</p>
      <div class="self-check-practice__number-fields"><label><span>Constante c</span><input type="text" inputmode="decimal" autocomplete="off" name="witness-c" aria-describedby="witness-format" placeholder="Ej.: 4,5"></label><label><span>Umbral n₀</span><input type="number" inputmode="numeric" min="1" step="1" name="witness-n0" placeholder="Ej.: 8"></label></div><small id="witness-format">Puede escribir los decimales de c con coma o punto.</small>`;
    typesetMath(container);
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
    if (limit.value !== question.answerLimit) return { correct: false, message: `Revise primero los grados del numerador y del denominador. El cociente tiende a \\(${question.limit}\\).` };
    if (relation.value !== question.answerRelation) return { correct: false, message: `El límite es correcto. De \\(${question.limit}\\) se deduce \\(${strongestRelationLabels[question.answerRelation]}\\).` };
    return { correct: true, message: `Correcto. \\(\\lim_{n\\to\\infty}C(n)/g(n)=${question.limit}\\), por lo que \\(${strongestRelationLabels[question.answerRelation]}\\).` };
  }

  function evaluateWitnesses(container, question) {
    const c = parseDecimal(container.querySelector("input[name='witness-c']").value); const n0 = Number(container.querySelector("input[name='witness-n0']").value);
    if (!Number.isFinite(c) || !Number.isFinite(n0)) return { incomplete: true, message: "Complete \\(c\\) y \\(n_0\\) antes de comprobar." };
    if (c <= 0) return { correct: false, message: "El primer requisito que falla es \\(c>0\\)." };
    if (!Number.isInteger(n0) || n0 < 1) return { correct: false, message: "\\(n_0\\) debe ser un natural positivo." };
    const tolerance = 1e-10;
    if (question.relation === "O") {
      if (c <= question.a) return { correct: false, message: `Necesita \\(c>${question.a}\\).` };
      const minimum = Math.max(1, Math.ceil((question.b / (c - question.a)) - tolerance));
      if (n0 < minimum) return { correct: false, message: `Con \\(c=${c}\\), necesita \\(n_0\\geq ${minimum}\\).` };
      return { correct: true, message: `Correcto: \\(${question.a}+\\frac{${question.b}}{n}\\leq ${c}\\) desde \\(n=${n0}\\).` };
    }
    if (c >= question.a) return { correct: false, message: `Elija \\(0<c<${question.a}\\).` };
    const minimum = Math.max(1, Math.ceil((question.b / (question.a - c)) - tolerance));
    if (n0 < minimum) return { correct: false, message: `Con \\(c=${c}\\), necesita \\(n_0\\geq ${minimum}\\).` };
    return { correct: true, message: `Correcto: \\(${question.a}-\\frac{${question.b}}{n}\\geq ${c}\\) desde \\(n=${n0}\\).` };
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
