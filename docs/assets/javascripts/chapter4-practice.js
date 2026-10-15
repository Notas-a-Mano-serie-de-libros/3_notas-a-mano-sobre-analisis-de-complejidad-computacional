(() => {
  "use strict";

  const masteryGoal = 3;
  const modes = {
    frequency: {
      level: "Nivel 1 · Conteo de instrucciones",
      title: "Determine la frecuencia de ejecución de la línea resaltada",
      hint: "Identifique los límites del ciclo (inicio, fin y paso) para calcular cuántas veces se ejecuta el cuerpo interior en función de \\(n\\).",
    },
    cost: {
      level: "Nivel 2 · Función de costo C(n)",
      title: "Deduzca la función exacta de costo C(n)",
      hint: "Plantee la sumatoria asociada a los ciclos anidados y use las fórmulas de sumas notables (Gauss: \\(\\sum_{i=1}^n i = \\frac{n(n+1)}{2}\\)).",
    },
    asymptotic: {
      level: "Nivel 3 · Clasificación asintótica",
      title: "Clasifique el orden de complejidad temporal del algoritmo",
      hint: "Considere el comportamiento asintótico: descarte constantes y conserve el término de mayor tasa de crecimiento \\(\\Theta(g(n))\\).",
    },
    simulation: {
      level: "Nivel 4 · Verificación experimental",
      title: "Compruebe empíricamente el conteo de operaciones",
      hint: "Ingrese o seleccione la fórmula candidata para \\(C(n)\\) y evalúe con el deslizador si coincide exactamente con el conteo de ejecuciones para todo \\(n\\).",
    },
  };

  const LANGUAGES = [
    { id: "pseudo", label: "Pseudocódigo" },
    { id: "java", label: "Java" },
    { id: "c", label: "C" },
    { id: "python", label: "Python" },
  ];

  function emptyState() {
    return {
      attempts: 0,
      correct: 0,
      streak: 0,
      best: 0,
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
        attempts: Math.max(0, Number(stored.attempts) || 0),
        correct: Math.max(0, Number(stored.correct) || 0),
        streak: Math.max(0, Number(stored.streak) || 0),
        best: Math.max(0, Number(stored.best) || 0),
        mastery: Object.fromEntries(Object.keys(modes).map((key) => [key, Math.min(masteryGoal, Math.max(0, Number(stored.mastery?.[key]) || 0))])),
        seen: Object.fromEntries(Object.keys(modes).map((key) => [key, Array.isArray(stored.seen?.[key]) ? stored.seen[key].filter((item) => typeof item === "string") : []])),
      };
    } catch (_error) {
      return empty;
    }
  }

  function saveState(panel, state) {
    try {
      localStorage.setItem(panel.dataset.storageKey, JSON.stringify(state));
    } catch (_error) {
      // Ignorar si el navegador bloquea storage
    }
  }

  function randomInt(min, max) {
    const range = max - min + 1;
    if (window.crypto?.getRandomValues) {
      const sample = new Uint32Array(1);
      window.crypto.getRandomValues(sample);
      return min + (sample[0] % range);
    }
    return min + Math.floor(Math.random() * range);
  }

  function pickRandom(list) {
    return list[randomInt(0, list.length - 1)];
  }

  function shuffled(items) {
    const result = [...items];
    for (let i = result.length - 1; i > 0; i -= 1) {
      const j = randomInt(0, i);
      [result[i], result[j]] = [result[j], result[i]];
    }
    return result;
  }

  function clearMath(element) {
    if (typeof window.MathJax?.typesetClear === "function") window.MathJax.typesetClear([element]);
  }

  function typesetMath(element) {
    if (typeof window.MathJax?.typesetPromise !== "function") return;
    window.MathJax.typesetPromise([element]).catch(() => {});
  }

  // --- Renderizado con pestañas multilingüe y números de línea ---

  function renderCodeBlock(codeSnippets) {
    const tabsHtml = LANGUAGES.map((lang, idx) => `
      <button type="button" class="self-check-practice__code-tab" data-lang="${lang.id}" role="tab" aria-selected="${idx === 0 ? "true" : "false"}" tabindex="${idx === 0 ? "0" : "-1"}">
        ${lang.label}
      </button>
    `).join("");

    const panelsHtml = LANGUAGES.map((lang, idx) => {
      const lines = codeSnippets[lang.id] || [];
      const linesHtml = lines.map((item, lineIdx) => {
        const isTarget = item.highlight ? " target-line" : "";
        return `<div class="self-check-practice__code-line${isTarget}"><span class="self-check-practice__line-num">${lineIdx + 1}</span><span class="self-check-practice__line-code">${item.text}</span></div>`;
      }).join("");

      return `
        <div class="self-check-practice__code-panel" data-panel-lang="${lang.id}" role="tabpanel" ${idx === 0 ? "" : "hidden"}>
          <div class="self-check-practice__code-box">
            <pre><code>${linesHtml}</code></pre>
          </div>
        </div>
      `;
    }).join("");

    return `
      <div class="self-check-practice__code-container">
        <div class="self-check-practice__code-tabs" role="tablist" aria-label="Lenguajes de programación">
          ${tabsHtml}
        </div>
        ${panelsHtml}
      </div>
    `;
  }

  function attachCodeTabEvents(container) {
    const tabs = container.querySelectorAll(".self-check-practice__code-tab");
    const panels = container.querySelectorAll(".self-check-practice__code-panel");

    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        const lang = tab.dataset.lang;
        tabs.forEach((t) => {
          const isSelected = t === tab;
          t.setAttribute("aria-selected", String(isSelected));
          t.setAttribute("tabindex", isSelected ? "0" : "-1");
        });
        panels.forEach((p) => {
          if (p.dataset.panelLang === lang) {
            p.removeAttribute("hidden");
          } else {
            p.setAttribute("hidden", "true");
          }
        });
      });
    });
  }

  // --- Generadores de ejercicios para Capítulo 4 ---

  function generateFrequency() {
    const kind = randomInt(0, 5);

    // Tipo 0: Salto aditivo constante con paso k (k entre 2 y 7)
    if (kind === 0) {
      const k = randomInt(2, 7);
      const start = pickRandom([0, 1]);
      const salt = randomInt(10, 999);
      const signature = `freq:step:${k}:start:${start}:${salt}`;
      const codeSnippets = {
        pseudo: [
          { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">${start}</span> <span class="kw">to</span> n <span class="kw">step</span> <span class="num">${k}</span> <span class="kw">do</span>` },
          { text: `    <span class="com">// Cuerpo del ciclo</span>` },
          { text: `    operacion_basica();`, highlight: true },
          { text: `<span class="kw">end for</span>` },
        ],
        java: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">${start}</span>; i <span class="op">&lt;=</span> n; i <span class="op">+=</span> <span class="num">${k}</span>) {` },
          { text: `    <span class="com">// Operación elemental</span>` },
          { text: `    operacionBasica();`, highlight: true },
          { text: `}` },
        ],
        c: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">${start}</span>; i <span class="op">&lt;=</span> n; i <span class="op">+=</span> <span class="num">${k}</span>) {` },
          { text: `    <span class="com">/* Operación elemental */</span>` },
          { text: `    operacion_basica();`, highlight: true },
          { text: `}` },
        ],
        python: [
          { text: `<span class="kw">for</span> i <span class="kw">in</span> range(<span class="num">${start}</span>, n <span class="op">+</span> <span class="num">1</span>, <span class="num">${k}</span>):` },
          { text: `    <span class="com"># Operación elemental</span>` },
          { text: `    operacion_basica()`, highlight: true },
        ],
      };

      const correctTex = start === 1 ? `\\lceil n/${k} \\rceil` : `\\lfloor n/${k} \\rfloor + 1`;
      return {
        signature,
        codeSnippets,
        prompt: `Considere el siguiente ciclo con tamaño de entrada \\(n\\), inicio en \\(${start}\\) y salto de avance \\(i \\leftarrow i + ${k}\\):`,
        options: shuffled([
          { value: "correct", tex: correctTex },
          { value: "w1", tex: `n - ${k}` },
          { value: "w2", tex: `${k}n` },
          { value: "w3", tex: `\\lfloor n/2 \\rfloor` },
        ]),
        answer: "correct",
        reason: start === 1
          ? `Al comenzar en 1 y dar saltos de \\(${k}\\) en \\(${k}\\) hasta \\(n\\), el total de pasos es \\(\\lceil n/${k} \\rceil\\).`
          : `Al comenzar en 0 y dar saltos de \\(${k}\\) en \\(${k}\\) hasta \\(n\\), el total de pasos es \\(\\lfloor n/${k} \\rfloor + 1\\).`,
      };
    }

    // Tipo 1: Salto multiplicativo creciente (i = i * factor, factor = 2, 3 o 4)
    if (kind === 1) {
      const factor = pickRandom([2, 3, 4]);
      const salt = randomInt(10, 999);
      const signature = `freq:mult:${factor}:${salt}`;
      const codeSnippets = {
        pseudo: [
          { text: `i <span class="op">=</span> <span class="num">1</span>` },
          { text: `<span class="kw">while</span> i <span class="op">&lt;=</span> n <span class="kw">do</span>` },
          { text: `    operacion_basica();`, highlight: true },
          { text: `    i <span class="op">=</span> i <span class="op">*</span> <span class="num">${factor}</span>` },
          { text: `<span class="kw">end while</span>` },
        ],
        java: [
          { text: `<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>;` },
          { text: `<span class="kw">while</span> (i <span class="op">&lt;=</span> n) {` },
          { text: `    operacionBasica();`, highlight: true },
          { text: `    i <span class="op">*=</span> <span class="num">${factor}</span>;` },
          { text: `}` },
        ],
        c: [
          { text: `<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>;` },
          { text: `<span class="kw">while</span> (i <span class="op">&lt;=</span> n) {` },
          { text: `    operacion_basica();`, highlight: true },
          { text: `    i <span class="op">*=</span> <span class="num">${factor}</span>;` },
          { text: `}` },
        ],
        python: [
          { text: `i <span class="op">=</span> <span class="num">1</span>` },
          { text: `<span class="kw">while</span> i <span class="op">&lt;=</span> n:` },
          { text: `    operacion_basica()`, highlight: true },
          { text: `    i <span class="op">*=</span> <span class="num">${factor}</span>` },
        ],
      };

      return {
        signature,
        codeSnippets,
        prompt: `Considere el siguiente ciclo con salto multiplicativo \\(i \\leftarrow i \\times ${factor}\\):`,
        options: shuffled([
          { value: "correct", tex: `\\lfloor \\log_{${factor}}(n) \\rfloor + 1` },
          { value: "w1", tex: `\\frac{n}{${factor}}` },
          { value: "w2", tex: `${factor}^n` },
          { value: "w3", tex: `\\log_{${factor}}(n) - 1` },
        ]),
        answer: "correct",
        reason: `La variable \\(i\\) toma valores \\(1, ${factor}, ${factor}^2, \\dots, ${factor}^k\\) hasta que \\(${factor}^k > n\\). La cantidad exacta de iteraciones es \\(\\lfloor \\log_{${factor}}(n) \\rfloor + 1\\).`,
      };
    }

    // Tipo 2: Salto multiplicativo decreciente / división (i = n; i > 0; i = i / div)
    if (kind === 2) {
      const div = pickRandom([2, 3]);
      const salt = randomInt(10, 999);
      const signature = `freq:div:${div}:${salt}`;
      const codeSnippets = {
        pseudo: [
          { text: `i <span class="op">=</span> n` },
          { text: `<span class="kw">while</span> i <span class="op">&gt;</span> <span class="num">0</span> <span class="kw">do</span>` },
          { text: `    operacion_basica();`, highlight: true },
          { text: `    i <span class="op">=</span> <span class="kw">floor</span>(i <span class="op">/</span> <span class="num">${div}</span>)` },
          { text: `<span class="kw">end while</span>` },
        ],
        java: [
          { text: `<span class="kw">int</span> i <span class="op">=</span> n;` },
          { text: `<span class="kw">while</span> (i <span class="op">&gt;</span> <span class="num">0</span>) {` },
          { text: `    operacionBasica();`, highlight: true },
          { text: `    i <span class="op">/=</span> <span class="num">${div}</span>;` },
          { text: `}` },
        ],
        c: [
          { text: `<span class="kw">int</span> i <span class="op">=</span> n;` },
          { text: `<span class="kw">while</span> (i <span class="op">&gt;</span> <span class="num">0</span>) {` },
          { text: `    operacion_basica();`, highlight: true },
          { text: `    i <span class="op">/=</span> <span class="num">${div}</span>;` },
          { text: `}` },
        ],
        python: [
          { text: `i <span class="op">=</span> n` },
          { text: `<span class="kw">while</span> i <span class="op">&gt;</span> <span class="num">0</span>:` },
          { text: `    operacion_basica()`, highlight: true },
          { text: `    i <span class="op">//=</span> <span class="num">${div}</span>` },
        ],
      };

      return {
        signature,
        codeSnippets,
        prompt: `Considere el siguiente ciclo con reducción sucesiva por división entera entre \\(${div}\\):`,
        options: shuffled([
          { value: "correct", tex: `\\lfloor \\log_{${div}}(n) \\rfloor + 1` },
          { value: "w1", tex: `\\frac{n}{${div}}` },
          { value: "w2", tex: `n - ${div}` },
          { value: "w3", tex: `\\log_{${div}}(n) - 1` },
        ]),
        answer: "correct",
        reason: `Al dividir iterativamente entre \\(${div}\\) hasta llegar a 0, la cantidad de pasos coincide exactamente con la representación en base \\(${div}\\), es decir, \\(\\lfloor \\log_{${div}}(n) \\rfloor + 1\\).`,
      };
    }

    // Tipo 3: Bucle triangular clásico (j = 1 to i)
    if (kind === 3) {
      const salt = randomInt(10, 999);
      const signature = `freq:triangular:${salt}`;
      const codeSnippets = {
        pseudo: [
          { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
          { text: `    <span class="kw">for</span> j <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> i <span class="kw">do</span>` },
          { text: `        operacion_basica();`, highlight: true },
          { text: `    <span class="kw">end for</span>` },
          { text: `<span class="kw">end for</span>` },
        ],
        java: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> <span class="num">1</span>; j <span class="op">&lt;=</span> i; j<span class="op">++</span>) {` },
          { text: `        operacionBasica();`, highlight: true },
          { text: `    }` },
          { text: `}` },
        ],
        c: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> <span class="num">1</span>; j <span class="op">&lt;=</span> i; j<span class="op">++</span>) {` },
          { text: `        operacion_basica();`, highlight: true },
          { text: `    }` },
          { text: `}` },
        ],
        python: [
          { text: `<span class="kw">for</span> i <span class="kw">in</span> range(<span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>):` },
          { text: `    <span class="kw">for</span> j <span class="kw">in</span> range(<span class="num">1</span>, i <span class="op">+</span> <span class="num">1</span>):` },
          { text: `        operacion_basica()`, highlight: true },
        ],
      };

      return {
        signature,
        codeSnippets,
        prompt: "Considere el siguiente ciclo anidado donde el límite del ciclo interior depende de la variable del ciclo exterior:",
        options: shuffled([
          { value: "correct", tex: "\\frac{n(n+1)}{2}" },
          { value: "w1", tex: "n^2" },
          { value: "w2", tex: "\\frac{n(n-1)}{2}" },
          { value: "w3", tex: "n(n+1)" },
        ]),
        answer: "correct",
        reason: "El ciclo exterior toma valores de \\(1\\) a \\(n\\) y en cada iteración \\(i\\) el ciclo interior ejecuta \\(i\\) veces. La suma es \\(\\sum_{i=1}^n i = \\frac{n(n+1)}{2}\\).",
      };
    }

    // Tipo 4: Bucle triangular estricto (j = i + 1 to n)
    if (kind === 4) {
      const salt = randomInt(10, 999);
      const signature = `freq:strictly-triangular:${salt}`;
      const codeSnippets = {
        pseudo: [
          { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
          { text: `    <span class="kw">for</span> j <span class="op">=</span> i <span class="op">+</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
          { text: `        operacion_basica();`, highlight: true },
          { text: `    <span class="kw">end for</span>` },
          { text: `<span class="kw">end for</span>` },
        ],
        java: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> i <span class="op">+</span> <span class="num">1</span>; j <span class="op">&lt;=</span> n; j<span class="op">++</span>) {` },
          { text: `        operacionBasica();`, highlight: true },
          { text: `    }` },
          { text: `}` },
        ],
        c: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> i <span class="op">+</span> <span class="num">1</span>; j <span class="op">&lt;=</span> n; j<span class="op">++</span>) {` },
          { text: `        operacion_basica();`, highlight: true },
          { text: `    }` },
          { text: `}` },
        ],
        python: [
          { text: `<span class="kw">for</span> i <span class="kw">in</span> range(<span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>):` },
          { text: `    <span class="kw">for</span> j <span class="kw">in</span> range(i <span class="op">+</span> <span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>):` },
          { text: `        operacion_basica()`, highlight: true },
        ],
      };

      return {
        signature,
        codeSnippets,
        prompt: "Considere el siguiente patrón de comparación por pares en un arreglo de tamaño \\(n\\):",
        options: shuffled([
          { value: "correct", tex: "\\frac{n(n-1)}{2}" },
          { value: "w1", tex: "\\frac{n(n+1)}{2}" },
          { value: "w2", tex: "n(n-1)" },
          { value: "w3", tex: "\\frac{n^2}{2}" },
        ]),
        answer: "correct",
        reason: "Para cada \\(i\\) de \\(1\\) a \\(n-1\\), \\(j\\) realiza \\(n-i\\) iteraciones. La suma es \\(\\sum_{i=1}^{n-1} (n-i) = \\frac{n(n-1)}{2}\\).",
      };
    }

    // Tipo 5: Salto variable dependiente del índice exterior (paso i)
    const salt = randomInt(10, 999);
    const signature = `freq:harmonic:${salt}`;
    const codeSnippets = {
      pseudo: [
        { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
        { text: `    <span class="kw">for</span> j <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">step</span> i <span class="kw">do</span>` },
        { text: `        operacion_basica();`, highlight: true },
        { text: `    <span class="kw">end for</span>` },
        { text: `<span class="kw">end for</span>` },
      ],
      java: [
        { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
        { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> <span class="num">1</span>; j <span class="op">&lt;=</span> n; j <span class="op">+=</span> i) {` },
        { text: `        operacionBasica();`, highlight: true },
        { text: `    }` },
        { text: `}` },
      ],
      c: [
        { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
        { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> <span class="num">1</span>; j <span class="op">&lt;=</span> n; j <span class="op">+=</span> i) {` },
        { text: `        operacion_basica();`, highlight: true },
        { text: `    }` },
        { text: `}` },
      ],
      python: [
        { text: `<span class="kw">for</span> i <span class="kw">in</span> range(<span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>):` },
        { text: `    <span class="kw">for</span> j <span class="kw">in</span> range(<span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>, i):` },
        { text: `        operacion_basica()`, highlight: true },
      ],
    };

    return {
      signature,
      codeSnippets,
      prompt: "Considere el siguiente ciclo anidado con salto variable \\(j \\leftarrow j + i\\) dependiente del ciclo exterior:",
      options: shuffled([
        { value: "correct", tex: "\\approx n \\ln(n)" },
        { value: "w1", tex: "n^2" },
        { value: "w2", tex: "\\frac{n(n+1)}{2}" },
        { value: "w3", tex: "n" },
      ]),
      answer: "correct",
      reason: "Para cada \\(i\\), el ciclo interior ejecuta \\(\\approx n/i\\) veces. La suma total es \\(\\sum_{i=1}^n \\frac{n}{i} = n \\sum_{i=1}^n \\frac{1}{i} \\approx n \\ln(n)\\) (serie armónica).",
    };
  }

  function generateCost() {
    const kind = randomInt(0, 3);

    // Tipo 0: Ciclo simple con costos c1 y c2 aleatorios
    if (kind === 0) {
      const c1 = randomInt(2, 6);
      const c2 = randomInt(1, 5);
      const c0 = randomInt(1, 3);
      const salt = randomInt(10, 999);
      const signature = `cost:linear:${c1}:${c2}:${c0}:${salt}`;
      const perIter = c1 + c2;

      const codeSnippets = {
        pseudo: [
          { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
          { text: `    paso_uno();   <span class="com">// costo c₁ = ${c1}</span>` },
          { text: `    paso_dos();   <span class="com">// costo c₂ = ${c2}</span>` },
          { text: `<span class="kw">end for</span>` },
          { text: `finalizar();      <span class="com">// costo c₀ = ${c0}</span>` },
        ],
        java: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
          { text: `    pasoUno();   <span class="com">// costo c₁ = ${c1}</span>` },
          { text: `    pasoDos();   <span class="com">// costo c₂ = ${c2}</span>` },
          { text: `}` },
          { text: `finalizar();      <span class="com">// costo c₀ = ${c0}</span>` },
        ],
        c: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
          { text: `    paso_uno();   <span class="com">/* costo c₁ = ${c1} */</span>` },
          { text: `    paso_dos();   <span class="com">/* costo c₂ = ${c2} */</span>` },
          { text: `}` },
          { text: `finalizar();      <span class="com">/* costo c₀ = ${c0} */</span>` },
        ],
        python: [
          { text: `<span class="kw">for</span> i <span class="kw">in</span> range(<span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>):` },
          { text: `    paso_uno()   <span class="com"># costo c₁ = ${c1}</span>` },
          { text: `    paso_dos()   <span class="com"># costo c₂ = ${c2}</span>` },
          { text: `finalizar()      <span class="com"># costo c₀ = ${c0}</span>` },
        ],
      };

      return {
        signature,
        codeSnippets,
        prompt: `Si cada instrucción tiene el costo exacto indicado en el comentario, deduzca la función de costo total \\(C(n)\\):`,
        options: shuffled([
          { value: "correct", tex: `C(n) = ${perIter}n + ${c0}` },
          { value: "w1", tex: `C(n) = ${c1}n + ${c2}` },
          { value: "w2", tex: `C(n) = ${perIter}n` },
          { value: "w3", tex: `C(n) = n + ${perIter}` },
        ]),
        answer: "correct",
        reason: `En cada una de las \\(n\\) iteraciones se ejecutan \\(c_1 + c_2 = ${c1} + ${c2} = ${perIter}\\) operaciones, más la instrucción final de costo \\(${c0}\\): \\(C(n) = ${perIter}n + ${c0}\\).`,
      };
    }

    // Tipo 1: Bucle anidado triangular con costo unitario k
    if (kind === 1) {
      const k = pickRandom([1, 2, 3]);
      const salt = randomInt(10, 999);
      const signature = `cost:poly2:${k}:${salt}`;
      const codeSnippets = {
        pseudo: [
          { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
          { text: `    <span class="kw">for</span> j <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> i <span class="kw">do</span>` },
          { text: `        operacion(); <span class="com">// costo unitario c = ${k}</span>` },
          { text: `    <span class="kw">end for</span>` },
          { text: `<span class="kw">end for</span>` },
        ],
        java: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> <span class="num">1</span>; j <span class="op">&lt;=</span> i; j<span class="op">++</span>) {` },
          { text: `        operacion(); <span class="com">// costo unitario c = ${k}</span>` },
          { text: `    }` },
          { text: `}` },
        ],
        c: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> <span class="num">1</span>; j <span class="op">&lt;=</span> i; j<span class="op">++</span>) {` },
          { text: `        operacion(); <span class="com">/* costo unitario c = ${k} */</span>` },
          { text: `    }` },
          { text: `}` },
        ],
        python: [
          { text: `<span class="kw">for</span> i <span class="kw">in</span> range(<span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>):` },
          { text: `    <span class="kw">for</span> j <span class="kw">in</span> range(<span class="num">1</span>, i <span class="op">+</span> <span class="num">1</span>):` },
          { text: `        operacion() <span class="com"># costo unitario c = ${k}</span>` },
        ],
      };

      const correctTex = k === 1 ? "C(n) = \\frac{1}{2}n^2 + \\frac{1}{2}n" : `C(n) = \\frac{${k}}{2}n^2 + \\frac{${k}}{2}n`;
      return {
        signature,
        codeSnippets,
        prompt: `Deduzca la función de costo polinomial exacta \\(C(n)\\) sumando las iteraciones del ciclo interior (con costo \\(c=${k}\\)):`,
        options: shuffled([
          { value: "correct", tex: correctTex },
          { value: "w1", tex: `C(n) = ${k}n^2 + ${k}n` },
          { value: "w2", tex: `C(n) = \\frac{${k}}{2}n^2 - \\frac{${k}}{2}n` },
          { value: "w3", tex: `C(n) = ${k}n^2` },
        ]),
        answer: "correct",
        reason: `La sumatoria es \\(c \\sum_{i=1}^n i = ${k} \\cdot \\frac{n(n+1)}{2} = ${correctTex.replace("C(n) = ", "")}\\).`,
      };
    }

    // Tipo 2: Matriz cuadrada de orden n x n con constante k
    if (kind === 2) {
      const k = pickRandom([1, 2, 4]);
      const salt = randomInt(10, 999);
      const signature = `cost:matrix:${k}:${salt}`;
      const codeSnippets = {
        pseudo: [
          { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
          { text: `    <span class="kw">for</span> j <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
          { text: `        matriz[i][j] <span class="op">=</span> matriz[i][j] <span class="op">+</span> <span class="num">1</span>; <span class="com">// costo = ${k}</span>` },
          { text: `    <span class="kw">end for</span>` },
          { text: `<span class="kw">end for</span>` },
        ],
        java: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">0</span>; i <span class="op">&lt;</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> <span class="num">0</span>; j <span class="op">&lt;</span> n; j<span class="op">++</span>) {` },
          { text: `        matriz[i][j] <span class="op">+=</span> <span class="num">1</span>; <span class="com">// costo = ${k}</span>` },
          { text: `    }` },
          { text: `}` },
        ],
        c: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">0</span>; i <span class="op">&lt;</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> <span class="num">0</span>; j <span class="op">&lt;</span> n; j<span class="op">++</span>) {` },
          { text: `        matriz[i][j] <span class="op">+=</span> <span class="num">1</span>; <span class="com">/* costo = ${k} */</span>` },
          { text: `    }` },
          { text: `}` },
        ],
        python: [
          { text: `<span class="kw">for</span> i <span class="kw">in</span> range(n):` },
          { text: `    <span class="kw">for</span> j <span class="kw">in</span> range(n):` },
          { text: `        matriz[i][j] <span class="op">+=</span> <span class="num">1</span> <span class="com"># costo = ${k}</span>` },
        ],
      };

      const correctTex = k === 1 ? "C(n) = n^2" : `C(n) = ${k}n^2`;
      return {
        signature,
        codeSnippets,
        prompt: `Deduzca la función exacta de costo \\(C(n)\\) para recorrer una matriz cuadrada \\(n \\times n\\) con costo de celda \\(${k}\\):`,
        options: shuffled([
          { value: "correct", tex: correctTex },
          { value: "w1", tex: `C(n) = ${2 * k}n` },
          { value: "w2", tex: `C(n) = ${k}n(n+1)` },
          { value: "w3", tex: `C(n) = n^3` },
        ]),
        answer: "correct",
        reason: `Ambos ciclos son independientes de tamaño \\(n\\): \\(\\sum_{i=1}^n \\sum_{j=1}^n ${k} = ${k} \\cdot n \\cdot n = ${correctTex.replace("C(n) = ", "")}\\).`,
      };
    }

    // Tipo 3: Ciclo con paso k (k = 2, 3, 4) y costo c por iteración
    const step = pickRandom([2, 3, 4]);
    const salt = randomInt(10, 999);
    const signature = `cost:step:${step}:${salt}`;
    const codeSnippets = {
      pseudo: [
        { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">step</span> <span class="num">${step}</span> <span class="kw">do</span>` },
        { text: `    procesar_bloque(); <span class="com">// costo unitario c = 1</span>` },
        { text: `<span class="kw">end for</span>` },
      ],
      java: [
        { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i <span class="op">+=</span> <span class="num">${step}</span>) {` },
        { text: `    procesarBloque(); <span class="com">// costo unitario c = 1</span>` },
        { text: `}` },
      ],
      c: [
        { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i <span class="op">+=</span> <span class="num">${step}</span>) {` },
        { text: `    procesar_bloque(); <span class="com">/* costo unitario c = 1 */</span>` },
        { text: `}` },
      ],
      python: [
        { text: `<span class="kw">for</span> i <span class="kw">in</span> range(<span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>, <span class="num">${step}</span>):` },
        { text: `    procesar_bloque() <span class="com"># costo unitario c = 1</span>` },
      ],
    };

    return {
      signature,
      codeSnippets,
      prompt: `Deduzca la función exacta de costo \\(C(n)\\) para este ciclo que avanza de \\(${step}\\) en \\(${step}\\):`,
      options: shuffled([
        { value: "correct", tex: `C(n) = \\lceil n/${step} \\rceil` },
        { value: "w1", tex: `C(n) = ${step}n` },
        { value: "w2", tex: `C(n) = n - ${step}` },
        { value: "w3", tex: `C(n) = \\lfloor n/2 \\rfloor` },
      ]),
      answer: "correct",
      reason: `Al iniciar en 1 e incrementar \\(i\\) en \\(${step}\\) en cada paso hasta \\(n\\), el total de operaciones es exactamente \\(\\lceil n/${step} \\rceil\\).`,
    };
  }

  function generateAsymptotic() {
    const kind = randomInt(0, 4);

    // Tipo 0: Ciclo exterior n, ciclo interior con salto multiplicativo (n log n)
    if (kind === 0) {
      const base = pickRandom([2, 3, 4]);
      const salt = randomInt(10, 999);
      const signature = `asymp:nlogn:${base}:${salt}`;
      const codeSnippets = {
        pseudo: [
          { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
          { text: `    j <span class="op">=</span> <span class="num">1</span>` },
          { text: `    <span class="kw">while</span> j <span class="op">&lt;=</span> n <span class="kw">do</span>` },
          { text: `        ejecutar();` },
          { text: `        j <span class="op">=</span> j <span class="op">*</span> <span class="num">${base}</span>` },
          { text: `    <span class="kw">end while</span>` },
          { text: `<span class="kw">end for</span>` },
        ],
        java: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">int</span> j <span class="op">=</span> <span class="num">1</span>;` },
          { text: `    <span class="kw">while</span> (j <span class="op">&lt;=</span> n) {` },
          { text: `        ejecutar();` },
          { text: `        j <span class="op">*=</span> <span class="num">${base}</span>;` },
          { text: `    }` },
          { text: `}` },
        ],
        c: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">int</span> j <span class="op">=</span> <span class="num">1</span>;` },
          { text: `    <span class="kw">while</span> (j <span class="op">&lt;=</span> n) {` },
          { text: `        ejecutar();` },
          { text: `        j <span class="op">*=</span> <span class="num">${base}</span>;` },
          { text: `    }` },
          { text: `}` },
        ],
        python: [
          { text: `<span class="kw">for</span> i <span class="kw">in</span> range(<span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>):` },
          { text: `    j <span class="op">=</span> <span class="num">1</span>` },
          { text: `    <span class="kw">while</span> j <span class="op">&lt;=</span> n:` },
          { text: `        ejecutar()` },
          { text: `        j <span class="op">*=</span> <span class="num">${base}</span>` },
        ],
      };

      return {
        signature,
        codeSnippets,
        prompt: `Determine la cota asintótica ajustada \\(\\Theta(g(n))\\) donde el ciclo interior avanza con factor \\(j \\leftarrow j \\times ${base}\\):`,
        options: shuffled([
          { value: "correct", tex: "\\Theta(n\\log(n))" },
          { value: "w1", tex: "\\Theta(n^2)" },
          { value: "w2", tex: "\\Theta(n)" },
          { value: "w3", tex: "\\Theta(\\log(n))" },
        ]),
        answer: "correct",
        reason: `El ciclo exterior ejecuta \\(n\\) veces y el interior ejecuta \\(\\approx \\log_{${base}}(n)\\) veces. El producto resulta en \\(\\Theta(n\\log(n))\\).`,
      };
    }

    // Tipo 1: Ciclo exterior n con ciclo interior de límite constante K (complejidad Theta(n))
    if (kind === 1) {
      const kConst = pickRandom([50, 100, 250, 500]);
      const salt = randomInt(10, 999);
      const signature = `asymp:fixed-inner:${kConst}:${salt}`;
      const codeSnippets = {
        pseudo: [
          { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
          { text: `    <span class="kw">for</span> j <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> <span class="num">${kConst}</span> <span class="kw">do</span>` },
          { text: `        tarea_fija();` },
          { text: `    <span class="kw">end for</span>` },
          { text: `<span class="kw">end for</span>` },
        ],
        java: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> <span class="num">1</span>; j <span class="op">&lt;=</span> <span class="num">${kConst}</span>; j<span class="op">++</span>) {` },
          { text: `        tareaFija();` },
          { text: `    }` },
          { text: `}` },
        ],
        c: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> <span class="num">1</span>; j <span class="op">&lt;=</span> <span class="num">${kConst}</span>; j<span class="op">++</span>) {` },
          { text: `        tarea_fija();` },
          { text: `    }` },
          { text: `}` },
        ],
        python: [
          { text: `<span class="kw">for</span> i <span class="kw">in</span> range(<span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>):` },
          { text: `    <span class="kw">for</span> j <span class="kw">in</span> range(<span class="num">1</span>, <span class="num">${kConst + 1}</span>):` },
          { text: `        tarea_fija()` },
        ],
      };

      return {
        signature,
        codeSnippets,
        prompt: `Determine la cota asintótica ajustada \\(\\Theta(g(n))\\) para este ciclo anidado con límite constante \\(${kConst}\\):`,
        options: shuffled([
          { value: "correct", tex: "\\Theta(n)" },
          { value: "w1", tex: "\\Theta(n^2)" },
          { value: "w2", tex: "\\Theta(1)" },
          { value: "w3", tex: `\\Theta(${kConst}n)` },
        ]),
        answer: "correct",
        reason: `El ciclo interior no depende de \\(n\\) y siempre se repite ${kConst} veces (costo constante \\(O(1)\\)). Por tanto, la cota asintótica es lineal \\(\\Theta(n)\\).`,
      };
    }

    // Tipo 2: Condición cuadrática i * i <= n (complejidad Theta(sqrt(n)))
    if (kind === 2) {
      const step = pickRandom([1, 2]);
      const salt = randomInt(10, 999);
      const signature = `asymp:sqrt:${step}:${salt}`;
      const codeSnippets = {
        pseudo: [
          { text: `i <span class="op">=</span> <span class="num">1</span>` },
          { text: `<span class="kw">while</span> i <span class="op">*</span> i <span class="op">&lt;=</span> n <span class="kw">do</span>` },
          { text: `    verificar();` },
          { text: `    i <span class="op">=</span> i <span class="op">+</span> <span class="num">${step}</span>` },
          { text: `<span class="kw">end while</span>` },
        ],
        java: [
          { text: `<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>;` },
          { text: `<span class="kw">while</span> (i <span class="op">*</span> i <span class="op">&lt;=</span> n) {` },
          { text: `    verificar();` },
          { text: `    i <span class="op">+=</span> <span class="num">${step}</span>;` },
          { text: `}` },
        ],
        c: [
          { text: `<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>;` },
          { text: `<span class="kw">while</span> (i <span class="op">*</span> i <span class="op">&lt;=</span> n) {` },
          { text: `    verificar();` },
          { text: `    i <span class="op">+=</span> <span class="num">${step}</span>;` },
          { text: `}` },
        ],
        python: [
          { text: `i <span class="op">=</span> <span class="num">1</span>` },
          { text: `<span class="kw">while</span> i <span class="op">*</span> i <span class="op">&lt;=</span> n:` },
          { text: `    verificar()` },
          { text: `    i <span class="op">+=</span> <span class="num">${step}</span>` },
        ],
      };

      return {
        signature,
        codeSnippets,
        prompt: "Determine la cota asintótica ajustada \\(\\Theta(g(n))\\) del algoritmo con condición cuadrática en la guarda:",
        options: shuffled([
          { value: "correct", tex: "\\Theta(\\sqrt{n})" },
          { value: "w1", tex: "\\Theta(n)" },
          { value: "w2", tex: "\\Theta(n^2)" },
          { value: "w3", tex: "\\Theta(\\log(n))" },
        ]),
        answer: "correct",
        reason: "El ciclo se detiene cuando \\(i^2 > n\\), lo que equivale a \\(i > \\sqrt{n}\\). Con avances aditivos de tamaño constante, la complejidad es \\(\\Theta(\\sqrt{n})\\).",
      };
    }

    // Tipo 3: Tres ciclos anidados independientes de tamaño n (Theta(n^3))
    if (kind === 3) {
      const salt = randomInt(10, 999);
      const signature = `asymp:cubic:${salt}`;
      const codeSnippets = {
        pseudo: [
          { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
          { text: `    <span class="kw">for</span> j <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
          { text: `        <span class="kw">for</span> k <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
          { text: `            operar();` },
          { text: `        <span class="kw">end for</span>` },
          { text: `    <span class="kw">end for</span>` },
          { text: `<span class="kw">end for</span>` },
        ],
        java: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">0</span>; i <span class="op">&lt;</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> <span class="num">0</span>; j <span class="op">&lt;</span> n; j<span class="op">++</span>) {` },
          { text: `        <span class="kw">for</span> (<span class="kw">int</span> k <span class="op">=</span> <span class="num">0</span>; k <span class="op">&lt;</span> n; k<span class="op">++</span>) {` },
          { text: `            operar();` },
          { text: `        }` },
          { text: `    }` },
          { text: `}` },
        ],
        c: [
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">0</span>; i <span class="op">&lt;</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> <span class="num">0</span>; j <span class="op">&lt;</span> n; j<span class="op">++</span>) {` },
          { text: `        <span class="kw">for</span> (<span class="kw">int</span> k <span class="op">=</span> <span class="num">0</span>; k <span class="op">&lt;</span> n; k<span class="op">++</span>) {` },
          { text: `            operar();` },
          { text: `        }` },
          { text: `    }` },
          { text: `}` },
        ],
        python: [
          { text: `<span class="kw">for</span> i <span class="kw">in</span> range(n):` },
          { text: `    <span class="kw">for</span> j <span class="kw">in</span> range(n):` },
          { text: `        <span class="kw">for</span> k <span class="kw">in</span> range(n):` },
          { text: `            operar()` },
        ],
      };

      return {
        signature,
        codeSnippets,
        prompt: "Determine la cota asintótica ajustada \\(\\Theta(g(n))\\) para tres ciclos anidados independientes:",
        options: shuffled([
          { value: "correct", tex: "\\Theta(n^3)" },
          { value: "w1", tex: "\\Theta(n^2)" },
          { value: "w2", tex: "\\Theta(3n)" },
          { value: "w3", tex: "\\Theta(n!)" },
        ]),
        answer: "correct",
        reason: "Tres ciclos independientes de 1 a \\(n\\) multiplican sus iteraciones: \\(n \\times n \\times n = \\Theta(n^3)\\).",
      };
    }

    // Tipo 4: Salto aditivo grande k (Theta(n))
    const step = randomInt(3, 8);
    const salt = randomInt(10, 999);
    const signature = `asymp:step:${step}:${salt}`;
    const codeSnippets = {
      pseudo: [
        { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">step</span> <span class="num">${step}</span> <span class="kw">do</span>` },
        { text: `    procesar();` },
        { text: `<span class="kw">end for</span>` },
      ],
      java: [
        { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i <span class="op">+=</span> <span class="num">${step}</span>) {` },
        { text: `    procesar();` },
        { text: `}` },
      ],
      c: [
        { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i <span class="op">+=</span> <span class="num">${step}</span>) {` },
        { text: `    procesar();` },
        { text: `}` },
      ],
      python: [
        { text: `<span class="kw">for</span> i <span class="kw">in</span> range(<span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>, <span class="num">${step}</span>):` },
        { text: `    procesar()` },
      ],
    };

    return {
      signature,
      codeSnippets,
      prompt: `Determine la cota asintótica ajustada \\(\\Theta(g(n))\\) para este ciclo que avanza en saltos de \\(${step}\\):`,
      options: shuffled([
        { value: "correct", tex: "\\Theta(n)" },
        { value: "w1", tex: `\\Theta(n/${step})` },
        { value: "w2", tex: "\\Theta(1)" },
        { value: "w3", tex: "\\Theta(\\log(n))" },
      ]),
      answer: "correct",
      reason: `Aunque se divide entre la constante \\(${step}\\), las constantes multiplicativas se absorben en el análisis asintótico: \\(\\lceil n/${step} \\rceil = \\Theta(n)\\).`,
    };
  }

  function generateSimulation() {
    const kind = randomInt(0, 3);

    // Tipo 0: Bucle triangular clásico sum(i)
    if (kind === 0) {
      const salt = randomInt(10, 999);
      const signature = `sim:triangular:${salt}`;
      const codeSnippets = {
        pseudo: [
          { text: `conteo <span class="op">=</span> <span class="num">0</span>` },
          { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
          { text: `    <span class="kw">for</span> j <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> i <span class="kw">do</span>` },
          { text: `        conteo <span class="op">=</span> conteo <span class="op">+</span> <span class="num">1</span>` },
          { text: `    <span class="kw">end for</span>` },
          { text: `<span class="kw">end for</span>` },
        ],
        java: [
          { text: `<span class="kw">int</span> conteo <span class="op">=</span> <span class="num">0</span>;` },
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> <span class="num">1</span>; j <span class="op">&lt;=</span> i; j<span class="op">++</span>) {` },
          { text: `        conteo<span class="op">++</span>;` },
          { text: `    }` },
          { text: `}` },
        ],
        c: [
          { text: `<span class="kw">int</span> conteo <span class="op">=</span> <span class="num">0</span>;` },
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
          { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> <span class="num">1</span>; j <span class="op">&lt;=</span> i; j<span class="op">++</span>) {` },
          { text: `        conteo<span class="op">++</span>;` },
          { text: `    }` },
          { text: `}` },
        ],
        python: [
          { text: `conteo <span class="op">=</span> <span class="num">0</span>` },
          { text: `<span class="kw">for</span> i <span class="kw">in</span> range(<span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>):` },
          { text: `    <span class="kw">for</span> j <span class="kw">in</span> range(<span class="num">1</span>, i <span class="op">+</span> <span class="num">1</span>):` },
          { text: `        conteo <span class="op">+=</span> <span class="num">1</span>` },
        ],
      };

      return {
        signature,
        codeSnippets,
        prompt: "Utilice el control interactivo para variar \\(n\\) y verificar experimentalmente cuántas operaciones ejecuta el algoritmo frente a la fórmula teórica:",
        formulaFn: (n) => (n * (n + 1)) / 2,
        formulaTex: "C(n) = \\frac{n(n+1)}{2}",
        initialN: 5,
        options: shuffled([
          { value: "correct", tex: "C(n) = \\frac{n(n+1)}{2}" },
          { value: "w1", tex: "C(n) = n^2" },
          { value: "w2", tex: "C(n) = \\frac{n(n-1)}{2}" },
          { value: "w3", tex: "C(n) = 2n" },
        ]),
        answer: "correct",
        reason: "Al variar \\(n\\) se comprueba que para \\(n=5\\) el conteo da 15 y para \\(n=10\\) da 55, coincidiendo exactamente con \\(\\frac{n(n+1)}{2}\\).",
      };
    }

    // Tipo 1: Salto multiplicativo i *= factor
    if (kind === 1) {
      const factor = pickRandom([2, 3]);
      const salt = randomInt(10, 999);
      const signature = `sim:log:${factor}:${salt}`;
      const codeSnippets = {
        pseudo: [
          { text: `conteo <span class="op">=</span> <span class="num">0</span>` },
          { text: `i <span class="op">=</span> <span class="num">1</span>` },
          { text: `<span class="kw">while</span> i <span class="op">&lt;=</span> n <span class="kw">do</span>` },
          { text: `    conteo <span class="op">=</span> conteo <span class="op">+</span> <span class="num">1</span>` },
          { text: `    i <span class="op">=</span> i <span class="op">*</span> <span class="num">${factor}</span>` },
          { text: `<span class="kw">end while</span>` },
        ],
        java: [
          { text: `<span class="kw">int</span> conteo <span class="op">=</span> <span class="num">0</span>;` },
          { text: `<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>;` },
          { text: `<span class="kw">while</span> (i <span class="op">&lt;=</span> n) {` },
          { text: `    conteo<span class="op">++</span>;` },
          { text: `    i <span class="op">*=</span> <span class="num">${factor}</span>;` },
          { text: `}` },
        ],
        c: [
          { text: `<span class="kw">int</span> conteo <span class="op">=</span> <span class="num">0</span>;` },
          { text: `<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>;` },
          { text: `<span class="kw">while</span> (i <span class="op">&lt;=</span> n) {` },
          { text: `    conteo<span class="op">++</span>;` },
          { text: `    i <span class="op">*=</span> <span class="num">${factor}</span>;` },
          { text: `}` },
        ],
        python: [
          { text: `conteo <span class="op">=</span> <span class="num">0</span>` },
          { text: `i <span class="op">=</span> <span class="num">1</span>` },
          { text: `<span class="kw">while</span> i <span class="op">&lt;=</span> n:` },
          { text: `    conteo <span class="op">+=</span> <span class="num">1</span>` },
          { text: `    i <span class="op">*=</span> <span class="num">${factor}</span>` },
        ],
      };

      const logFn = factor === 2
        ? (n) => Math.floor(Math.log2(n)) + 1
        : (n) => Math.floor(Math.log(n) / Math.log(3)) + 1;

      return {
        signature,
        codeSnippets,
        prompt: `Simule el conteo en tiempo real al variar \\(n\\) para confirmar la función de crecimiento con avance \\(i \\leftarrow i \\times ${factor}\\):`,
        formulaFn: logFn,
        formulaTex: `C(n) = \\lfloor \\log_{${factor}}(n) \\rfloor + 1`,
        initialN: 8,
        options: shuffled([
          { value: "correct", tex: `C(n) = \\lfloor \\log_{${factor}}(n) \\rfloor + 1` },
          { value: "w1", tex: `C(n) = \\frac{n}{${factor}}` },
          { value: "w2", tex: `C(n) = \\log_{${factor}}(n)` },
          { value: "w3", tex: `C(n) = ${factor}n` },
        ]),
        answer: "correct",
        reason: `Al probar valores de \\(n\\) con potencias de \\(${factor}\\), se comprueba que el total de iteraciones es \\(\\lfloor \\log_{${factor}}(n) \\rfloor + 1\\).`,
      };
    }

    // Tipo 2: Salto aditivo k (k = 2, 3, 4, 5)
    if (kind === 2) {
      const step = pickRandom([2, 3, 4, 5]);
      const salt = randomInt(10, 999);
      const signature = `sim:step:${step}:${salt}`;
      const codeSnippets = {
        pseudo: [
          { text: `conteo <span class="op">=</span> <span class="num">0</span>` },
          { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">step</span> <span class="num">${step}</span> <span class="kw">do</span>` },
          { text: `    conteo <span class="op">=</span> conteo <span class="op">+</span> <span class="num">1</span>` },
          { text: `<span class="kw">end for</span>` },
        ],
        java: [
          { text: `<span class="kw">int</span> conteo <span class="op">=</span> <span class="num">0</span>;` },
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i <span class="op">+=</span> <span class="num">${step}</span>) {` },
          { text: `    conteo<span class="op">++</span>;` },
          { text: `}` },
        ],
        c: [
          { text: `<span class="kw">int</span> conteo <span class="op">=</span> <span class="num">0</span>;` },
          { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i <span class="op">+=</span> <span class="num">${step}</span>) {` },
          { text: `    conteo<span class="op">++</span>;` },
          { text: `}` },
        ],
        python: [
          { text: `conteo <span class="op">=</span> <span class="num">0</span>` },
          { text: `<span class="kw">for</span> i <span class="kw">in</span> range(<span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>, <span class="num">${step}</span>):` },
          { text: `    conteo <span class="op">+=</span> <span class="num">1</span>` },
        ],
      };

      return {
        signature,
        codeSnippets,
        prompt: `Simule las iteraciones del bucle con salto de paso \\(${step}\\) variando \\(n\\):`,
        formulaFn: (n) => Math.ceil(n / step),
        formulaTex: `C(n) = \\lceil n/${step} \\rceil`,
        initialN: 10,
        options: shuffled([
          { value: "correct", tex: `C(n) = \\lceil n/${step} \\rceil` },
          { value: "w1", tex: `C(n) = ${step}n` },
          { value: "w2", tex: `C(n) = n - ${step}` },
          { value: "w3", tex: `C(n) = \\lfloor n/2 \\rfloor` },
        ]),
        answer: "correct",
        reason: `Al variar \\(n\\) se verifica empíricamente que las iteraciones coinciden exactamente con \\(\\lceil n/${step} \\rceil\\).`,
      };
    }

    // Tipo 3: Triangular estricto j = i + 1 to n
    const salt = randomInt(10, 999);
    const signature = `sim:strictly-triangular:${salt}`;
    const codeSnippets = {
      pseudo: [
        { text: `conteo <span class="op">=</span> <span class="num">0</span>` },
        { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
        { text: `    <span class="kw">for</span> j <span class="op">=</span> i <span class="op">+</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
        { text: `        conteo <span class="op">=</span> conteo <span class="op">+</span> <span class="num">1</span>` },
        { text: `    <span class="kw">end for</span>` },
        { text: `<span class="kw">end for</span>` },
      ],
      java: [
        { text: `<span class="kw">int</span> conteo <span class="op">=</span> <span class="num">0</span>;` },
        { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
        { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> i <span class="op">+</span> <span class="num">1</span>; j <span class="op">&lt;=</span> n; j<span class="op">++</span>) {` },
        { text: `        conteo<span class="op">++</span>;` },
        { text: `    }` },
        { text: `}` },
      ],
      c: [
        { text: `<span class="kw">int</span> conteo <span class="op">=</span> <span class="num">0</span>;` },
        { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
        { text: `    <span class="kw">for</span> (<span class="kw">int</span> j <span class="op">=</span> i <span class="op">+</span> <span class="num">1</span>; j <span class="op">&lt;=</span> n; j<span class="op">++</span>) {` },
        { text: `        conteo<span class="op">++</span>;` },
        { text: `    }` },
        { text: `}` },
      ],
      python: [
        { text: `conteo <span class="op">=</span> <span class="num">0</span>` },
        { text: `<span class="kw">for</span> i <span class="kw">in</span> range(<span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>):` },
        { text: `    <span class="kw">for</span> j <span class="kw">in</span> range(i <span class="op">+</span> <span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>):` },
        { text: `        conteo <span class="op">+=</span> <span class="num">1</span>` },
      ],
    };

    return {
      signature,
      codeSnippets,
      prompt: "Simule el conteo para el patrón de comparaciones estrictas por parejas variando el valor de \\(n\\):",
      formulaFn: (n) => (n * (n - 1)) / 2,
      formulaTex: "C(n) = \\frac{n(n-1)}{2}",
      initialN: 6,
      options: shuffled([
        { value: "correct", tex: "C(n) = \\frac{n(n-1)}{2}" },
        { value: "w1", tex: "C(n) = \\frac{n(n+1)}{2}" },
        { value: "w2", tex: "C(n) = n(n-1)" },
        { value: "w3", tex: "C(n) = \\frac{n^2}{2}" },
      ]),
      answer: "correct",
      reason: "Al variar \\(n\\) se comprueba que para \\(n=6\\) el conteo es 15, para \\(n=5\\) es 10, coincidiendo exactamente con \\(\\frac{n(n-1)}{2}\\).",
    };
  }

  function fallbackQuestion(mode, index) {
    const unique = Date.now() + index;
    const baseSnippets = (opLine) => ({
      pseudo: [
        { text: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>` },
        { text: `    ${opLine};`, highlight: true },
        { text: `<span class="kw">end for</span>` },
      ],
      java: [
        { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
        { text: `    ${opLine}();`, highlight: true },
        { text: `}` },
      ],
      c: [
        { text: `<span class="kw">for</span> (<span class="kw">int</span> i <span class="op">=</span> <span class="num">1</span>; i <span class="op">&lt;=</span> n; i<span class="op">++</span>) {` },
        { text: `    ${opLine}();`, highlight: true },
        { text: `}` },
      ],
      python: [
        { text: `<span class="kw">for</span> i <span class="kw">in</span> range(<span class="num">1</span>, n <span class="op">+</span> <span class="num">1</span>):` },
        { text: `    ${opLine}()`, highlight: true },
      ],
    });

    if (mode === "frequency") {
      return {
        signature: `fallback-f:${unique}`,
        codeSnippets: baseSnippets("operacion_basica"),
        prompt: "Considere el siguiente ciclo simple con límite \\(n\\):",
        options: [{ value: "correct", tex: "n" }, { value: "w1", tex: "n+1" }, { value: "w2", tex: "n-1" }, { value: "w3", tex: "2n" }],
        answer: "correct",
        reason: "Un ciclo simple de 1 a \\(n\\) con paso 1 ejecuta exactamente \\(n\\) veces.",
      };
    }
    if (mode === "cost") {
      return {
        signature: `fallback-c:${unique}`,
        codeSnippets: baseSnippets("instruccion_costo_1"),
        prompt: "Deduzca \\(C(n)\\) si cada iteración tiene un costo unitario de 1:",
        options: [{ value: "correct", tex: "C(n) = n" }, { value: "w1", tex: "C(n) = n^2" }],
        answer: "correct",
        reason: "\\(C(n) = n\\).",
      };
    }
    if (mode === "asymptotic") {
      return {
        signature: `fallback-a:${unique}`,
        codeSnippets: baseSnippets("ejecutar"),
        prompt: "Determine la cota asintótica ajustada:",
        options: [{ value: "correct", tex: "\\Theta(n)" }, { value: "w1", tex: "\\Theta(n^2)" }],
        answer: "correct",
        reason: "El algoritmo ejecuta un número de pasos estrictamente proporcional a \\(n\\): \\(\\Theta(n)\\).",
      };
    }
    return {
      signature: `fallback-s:${unique}`,
      codeSnippets: baseSnippets("conteo = conteo + 1"),
      prompt: "Simule el conteo lineal variando \\(n\\):",
      formulaFn: (n) => n,
      formulaTex: "C(n) = n",
      initialN: 5,
      options: [{ value: "correct", tex: "C(n) = n" }, { value: "w1", tex: "C(n) = 2n" }],
      answer: "correct",
      reason: "El conteo coincide exactamente con \\(n\\).",
    };
  }

  function nextUniqueQuestion(mode, state) {
    // Si la memoria de vistos supera 30 elementos, purgar la mitad más antigua para garantizar rotación infinita
    if (state.seen[mode].length > 30) {
      state.seen[mode] = state.seen[mode].slice(-15);
    }

    const seen = new Set(state.seen[mode]);
    for (let attempt = 0; attempt < 500; attempt += 1) {
      const q = mode === "frequency" ? generateFrequency()
        : mode === "cost" ? generateCost()
          : mode === "asymptotic" ? generateAsymptotic()
            : generateSimulation();
      if (!seen.has(q.signature)) {
        state.seen[mode].push(q.signature);
        return q;
      }
    }

    // Si todas las firmas recientes chocaran, generamos un fallback garantizado o vaciamos el historial
    state.seen[mode] = [];
    const fallback = fallbackQuestion(mode, state.seen[mode].length);
    state.seen[mode].push(fallback.signature);
    return fallback;
  }

  // --- Funciones de renderizado ---

  function renderChoicesQuestion(container, question, modeClass = "") {
    clearMath(container);
    const codeBlockHtml = renderCodeBlock(question.codeSnippets);
    container.innerHTML = `<p class="self-check-practice__prompt">${question.prompt}</p>
      ${codeBlockHtml}
      <fieldset class="self-check-practice__choices ${modeClass}">
        <legend>Seleccione la respuesta correcta</legend>
        ${question.options.map((opt) => `<label><input type="radio" name="chapter4-answer" value="${opt.value}"><span>\\(${opt.tex}\\)</span></label>`).join("")}
      </fieldset>`;
    attachCodeTabEvents(container);
    typesetMath(container);
  }

  function renderFrequency(container, question) {
    renderChoicesQuestion(container, question, "self-check-practice__choices--code");
  }

  function renderCost(container, question) {
    renderChoicesQuestion(container, question, "self-check-practice__choices--code");
  }

  function renderAsymptotic(container, question) {
    renderChoicesQuestion(container, question, "self-check-practice__choices--code");
  }

  function renderSimulation(container, question) {
    clearMath(container);
    const codeBlockHtml = renderCodeBlock(question.codeSnippets);
    container.innerHTML = `<p class="self-check-practice__prompt">${question.prompt}</p>
      ${codeBlockHtml}
      <div class="self-check-practice__sim-row">
        <label>
          <span class="label-text">\\(\\mathbf{n}\\)</span>
          <input type="range" min="1" max="25" value="${question.initialN}" data-sim-range>
          <strong data-sim-n-display>${question.initialN}</strong>
        </label>
      </div>
      <div class="self-check-practice__sim-results">
        <div class="self-check-practice__sim-card">
          <div class="lbl">Iteraciones reales ejecutadas</div>
          <div class="val" data-sim-real>${question.formulaFn(question.initialN)}</div>
        </div>
        <div class="self-check-practice__sim-card">
          <div class="lbl">Crecimiento estimado</div>
          <div class="val" data-sim-growth>\\(n = ${question.initialN}\\)</div>
        </div>
      </div>
      <fieldset class="self-check-practice__choices self-check-practice__choices--code">
        <legend>Fórmula de costo C(n) que predice exactamente estas iteraciones</legend>
        ${question.options.map((opt) => `<label><input type="radio" name="chapter4-answer" value="${opt.value}"><span>\\(${opt.tex}\\)</span></label>`).join("")}
      </fieldset>`;

    attachCodeTabEvents(container);

    const range = container.querySelector("[data-sim-range]");
    const nDisplay = container.querySelector("[data-sim-n-display]");
    const realDisplay = container.querySelector("[data-sim-real]");
    const growthDisplay = container.querySelector("[data-sim-growth]");

    range.addEventListener("input", () => {
      const val = Number(range.value);
      nDisplay.textContent = val;
      realDisplay.textContent = question.formulaFn(val);
      growthDisplay.innerHTML = `\\(n = ${val}\\)`;
      typesetMath(growthDisplay);
    });

    typesetMath(container);
  }

  function evaluateStandard(container, question) {
    const selected = container.querySelector("input[name='chapter4-answer']:checked");
    if (!selected) return { incomplete: true, message: "Seleccione una opción antes de comprobar." };
    if (selected.value === question.answer) {
      return { correct: true, message: `Correcto. ${question.reason}` };
    }
    return { correct: false, message: `Incorrecto. ${question.reason}` };
  }

  function initializePractice(panel) {
    if (panel.dataset.initialized) return;
    panel.dataset.initialized = "true";
    let state = safeState(panel);
    let mode = "frequency";
    let current;
    let solved = false;

    const questionContainer = panel.querySelector("[data-practice-question]");
    const feedback = panel.querySelector("[data-practice-feedback]");
    const checkLabel = panel.querySelector("[data-practice-check-label]");

    const renderProgress = () => {
      panel.querySelector("[data-practice-correct]").textContent = state.correct;
      panel.querySelector("[data-practice-attempts]").textContent = state.attempts;
      panel.querySelector("[data-practice-best]").textContent = state.best;
      Object.keys(modes).forEach((key) => {
        const val = state.mastery[key];
        const meter = panel.querySelector(`[data-mastery='${key}']`);
        if (meter) {
          meter.value = val;
          meter.textContent = `${val} de ${masteryGoal}`;
        }
        const lbl = panel.querySelector(`[data-mastery-label='${key}']`);
        if (lbl) lbl.textContent = val >= masteryGoal ? "Afianzada" : `${val}/${masteryGoal}`;
      });
    };

    const showFeedback = (kind, message, focus = false) => {
      clearMath(feedback);
      feedback.dataset.state = kind;
      feedback.innerHTML = message;
      typesetMath(feedback);
      if (focus) feedback.focus({ preventScroll: true });
    };

    const newQuestion = () => {
      current = nextUniqueQuestion(mode, state);
      saveState(panel, state);
      solved = false;
      panel.querySelector("[data-practice-level]").textContent = modes[mode].level;
      panel.querySelector("[data-practice-title]").textContent = modes[mode].title;
      ({
        frequency: renderFrequency,
        cost: renderCost,
        asymptotic: renderAsymptotic,
        simulation: renderSimulation,
      })[mode](questionContainer, current);
      checkLabel.textContent = "Comprobar respuesta";
      showFeedback("", "");
    };

    const checkAnswer = () => {
      if (solved) {
        newQuestion();
        return;
      }
      const result = evaluateStandard(questionContainer, current);
      if (result.incomplete) {
        showFeedback("hint", result.message, true);
        return;
      }
      state.attempts += 1;
      if (result.correct) {
        solved = true;
        state.correct += 1;
        state.streak += 1;
        state.best = Math.max(state.best, state.streak);
        state.mastery[mode] = Math.min(masteryGoal, state.mastery[mode] + 1);
        questionContainer.querySelectorAll("input").forEach((input) => {
          input.disabled = true;
        });
        checkLabel.textContent = "Siguiente ejercicio";
        showFeedback("correct", result.message, true);
      } else {
        state.streak = 0;
        showFeedback("error", result.message, true);
      }
      saveState(panel, state);
      renderProgress();
    };

    panel.querySelectorAll("[data-practice-mode]").forEach((button) => {
      button.addEventListener("click", () => {
        mode = button.dataset.practiceMode;
        panel.querySelectorAll("[data-practice-mode]").forEach((c) => c.setAttribute("aria-pressed", String(c === button)));
        newQuestion();
      });
    });

    panel.querySelector("[data-practice-new]").addEventListener("click", newQuestion);
    panel.querySelector("[data-practice-hint]").addEventListener("click", () => showFeedback("hint", modes[mode].hint, true));
    panel.querySelector("[data-practice-reset]").addEventListener("click", () => {
      state = emptyState();
      saveState(panel, state);
      renderProgress();
      newQuestion();
      showFeedback("hint", "El progreso y el historial de ejercicios se reiniciaron.", true);
    });
    panel.querySelector("[data-practice-check]").addEventListener("click", checkAnswer);

    questionContainer.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        checkAnswer();
      }
    });

    renderProgress();
    newQuestion();
  }

  function prepareChapter4Practice(root = document) {
    root.querySelectorAll("[data-chapter4-practice]").forEach(initializePractice);
  }

  if (typeof document$ !== "undefined") document$.subscribe(prepareChapter4Practice);
  else document.addEventListener("DOMContentLoaded", () => prepareChapter4Practice());
})();
