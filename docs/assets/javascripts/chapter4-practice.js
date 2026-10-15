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
      hint: "Ingrese una fórmula candidata para \\(C(n)\\) y evalúe con el deslizador si coincide exactamente con el conteo de ejecuciones para todo \\(n\\).",
    },
  };

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

  // --- Generadores de ejercicios para Capítulo 4 ---

  function generateFrequency() {
    const kind = randomInt(0, 3);
    if (kind === 0) {
      const k = randomInt(2, 5);
      const code = `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">step</span> <span class="num">${k}</span> <span class="kw">do</span>\n<span class="target-line">    operacion_basica();</span>\n<span class="kw">end for</span>`;
      return {
        signature: `freq:step:${k}`,
        code,
        prompt: `Considere el siguiente ciclo con tamaño de entrada \\(n\\) e incremento de \\(${k}\\) en \\(${k}\\):`,
        targetDescription: "la cantidad exacta de ejecuciones de <code>operacion_basica()</code>",
        options: shuffled([
          { value: "correct", tex: `\\lceil n/${k} \\rceil` },
          { value: "w1", tex: `n - ${k}` },
          { value: "w2", tex: `${k}n` },
          { value: "w3", tex: `\\lfloor n/2 \\rfloor` },
        ]),
        answer: "correct",
        reason: `Al avanzar de \\(${k}\\) en \\(${k}\\) comenzando en 1 hasta \\(n\\), la cantidad de pasos es \\(\\lceil n/${k} \\rceil\\).`,
      };
    }
    if (kind === 1) {
      const code = `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n    <span class="kw">for</span> j <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> i <span class="kw">do</span>\n<span class="target-line">        operacion_basica();</span>\n    <span class="kw">end for</span>\n<span class="kw">end for</span>`;
      return {
        signature: "freq:triangular",
        code,
        prompt: "Considere el siguiente ciclo anidado donde el límite del ciclo interior depende de la variable del ciclo exterior:",
        targetDescription: "la cantidad de veces que se ejecuta <code>operacion_basica()</code>",
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
    if (kind === 2) {
      const code = `i <span class="op">=</span> <span class="num">1</span>\n<span class="kw">while</span> i <span class="op">&lt;=</span> n <span class="kw">do</span>\n<span class="target-line">    operacion_basica();</span>\n    i <span class="op">=</span> i <span class="op">*</span> <span class="num">2</span>\n<span class="kw">end while</span>`;
      return {
        signature: "freq:doubling",
        code,
        prompt: "Considere el siguiente ciclo con incremento multiplicativo en la variable de control:",
        targetDescription: "la cantidad exacta de iteraciones de <code>operacion_basica()</code>",
        options: shuffled([
          { value: "correct", tex: "\\lfloor \\log_2(n) \\rfloor + 1" },
          { value: "w1", tex: "n / 2" },
          { value: "w2", tex: "2^n" },
          { value: "w3", tex: "\\log_2(n) - 1" },
        ]),
        answer: "correct",
        reason: "La variable \\(i\\) toma valores \\(1, 2, 4, 8, \\dots, 2^k\\) hasta que \\(2^k > n\\). La cantidad de iteraciones es \\(\\lfloor \\log_2(n) \\rfloor + 1\\).",
      };
    }
    const code = `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n    <span class="kw">for</span> j <span class="op">=</span> i <span class="op">+</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n<span class="target-line">        operacion_basica();</span>\n    <span class="kw">end for</span>\n<span class="kw">end for</span>`;
    return {
      signature: "freq:strictly-triangular",
      code,
      prompt: "Considere el siguiente patrón de comparación por parejas en un arreglo de tamaño \\(n\\):",
      targetDescription: "la cantidad de comparaciones ejecutadas por <code>operacion_basica()</code>",
      options: shuffled([
        { value: "correct", tex: "\\frac{n(n-1)}{2}" },
        { value: "w1", tex: "\\frac{n(n+1)}{2}" },
        { value: "w2", tex: "n(n-1)" },
        { value: "w3", tex: "n^2 / 2" },
      ]),
      answer: "correct",
      reason: "Para cada \\(i\\) de \\(1\\) a \\(n-1\\), \\(j\\) realiza \\(n-i\\) iteraciones. La suma es \\(\\sum_{i=1}^{n-1} (n-i) = \\frac{n(n-1)}{2}\\).",
    };
  }

  function generateCost() {
    const kind = randomInt(0, 2);
    if (kind === 0) {
      const c1 = randomInt(2, 4);
      const c2 = randomInt(1, 3);
      const code = `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n    paso_uno();   <span class="num">// costo c₁ = ${c1}</span>\n    paso_dos();   <span class="num">// costo c₂ = ${c2}</span>\n<span class="kw">end for</span>\nfinalizar();      <span class="num">// costo c₀ = 1</span>`;
      const perIter = c1 + c2;
      return {
        signature: `cost:linear:${c1}:${c2}`,
        code,
        prompt: `Si cada instrucción tiene el costo indicado en el comentario, deduzca la función de costo total \\(C(n)\\):`,
        options: shuffled([
          { value: "correct", tex: `C(n) = ${perIter}n + 1` },
          { value: "w1", tex: `C(n) = ${c1}n + ${c2}` },
          { value: "w2", tex: `C(n) = ${perIter}n` },
          { value: "w3", tex: `C(n) = n + ${perIter}` },
        ]),
        answer: "correct",
        reason: `En cada una de las \\(n\\) iteraciones se ejecutan \\(c_1 + c_2 = ${c1} + ${c2} = ${perIter}\\) operaciones, más la instrucción final de costo \\(1\\): \\(C(n) = ${perIter}n + 1\\).`,
      };
    }
    if (kind === 1) {
      const code = `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n    <span class="kw">for</span> j <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> i <span class="kw">do</span>\n        operacion(); <span class="num">// costo unitario 1</span>\n    <span class="kw">end for</span>\n<span class="kw">end for</span>`;
      return {
        signature: "cost:poly2",
        code,
        prompt: "Deduzca la función de costo polinomial exacta \\(C(n)\\) sumando las iteraciones del ciclo interior:",
        options: shuffled([
          { value: "correct", tex: "C(n) = \\frac{1}{2}n^2 + \\frac{1}{2}n" },
          { value: "w1", tex: "C(n) = n^2 + n" },
          { value: "w2", tex: "C(n) = \\frac{1}{2}n^2 - \\frac{1}{2}n" },
          { value: "w3", tex: "C(n) = n^2" },
        ]),
        answer: "correct",
        reason: "La sumatoria es \\(\\sum_{i=1}^n i = \\frac{n(n+1)}{2} = \\frac{1}{2}n^2 + \\frac{1}{2}n\\).",
      };
    }
    const code = `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n    <span class="kw">for</span> j <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n        matriz[i][j] <span class="op">=</span> <span class="num">0</span>;\n    <span class="kw">end for</span>\n<span class="kw">end for</span>`;
    return {
      signature: "cost:matrix",
      code,
      prompt: "Deduzca la función exacta de costo \\(C(n)\\) para inicializar una matriz cuadrada de orden \\(n\\times n\\):",
      options: shuffled([
        { value: "correct", tex: "C(n) = n^2" },
        { value: "w1", tex: "C(n) = 2n" },
        { value: "w2", tex: "C(n) = n(n+1)" },
        { value: "w3", tex: "C(n) = n^3" },
      ]),
      answer: "correct",
      reason: "Ambos ciclos son independientes y van de 1 a \\(n\\): \\(\\sum_{i=1}^n \\sum_{j=1}^n 1 = n \\cdot n = n^2\\).",
    };
  }

  function generateAsymptotic() {
    const kind = randomInt(0, 3);
    if (kind === 0) {
      const code = `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n    j <span class="op">=</span> <span class="num">1</span>\n    <span class="kw">while</span> j <span class="op">&lt;=</span> n <span class="kw">do</span>\n        ejecutar();\n        j <span class="op">=</span> j <span class="op">*</span> <span class="num">2</span>\n    <span class="kw">end while</span>\n<span class="kw">end for</span>`;
      return {
        signature: "asymp:nlogn",
        code,
        prompt: "Determine la cota asintótica ajustada \\(\\Theta(g(n))\\) para el siguiente algoritmo estructurado:",
        options: shuffled([
          { value: "correct", tex: "\\Theta(n\\log(n))" },
          { value: "w1", tex: "\\Theta(n^2)" },
          { value: "w2", tex: "\\Theta(n)" },
          { value: "w3", tex: "\\Theta(\\log(n))" },
        ]),
        answer: "correct",
        reason: "El ciclo exterior ejecuta \\(n\\) veces y el interior ejecuta \\(\\approx \\log_2(n)\\) veces en cada iteración. El producto resulta en \\(\\Theta(n\\log(n))\\).",
      };
    }
    if (kind === 1) {
      const code = `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n    <span class="kw">for</span> j <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> <span class="num">100</span> <span class="kw">do</span>\n        tarea_fija();\n    <span class="kw">end for</span>\n<span class="kw">end for</span>`;
      return {
        signature: "asymp:fixed-inner",
        code,
        prompt: "Determine la cota asintótica ajustada \\(\\Theta(g(n))\\) para este ciclo anidado con límite constante:",
        options: shuffled([
          { value: "correct", tex: "\\Theta(n)" },
          { value: "w1", tex: "\\Theta(n^2)" },
          { value: "w2", tex: "\\Theta(1)" },
          { value: "w3", tex: "\\Theta(100n)" },
        ]),
        answer: "correct",
        reason: "El ciclo interior no depende de \\(n\\) y siempre se repite 100 veces (costo constante \\(O(1)\\)). Por tanto, el costo total es lineal \\(\\Theta(n)\\).",
      };
    }
    if (kind === 2) {
      const code = `i <span class="op">=</span> <span class="num">1</span>\n<span class="kw">while</span> i <span class="op">*</span> i <span class="op">&lt;=</span> n <span class="kw">do</span>\n    verificar();\n    i <span class="op">=</span> i <span class="op">+</span> <span class="num">1</span>\n<span class="kw">end while</span>`;
      return {
        signature: "asymp:sqrt",
        code,
        prompt: "Determine la cota asintótica ajustada \\(\\Theta(g(n))\\) del algoritmo con condición cuadrática en la condición:",
        options: shuffled([
          { value: "correct", tex: "\\Theta(\\sqrt{n})" },
          { value: "w1", tex: "\\Theta(n)" },
          { value: "w2", tex: "\\Theta(n^2)" },
          { value: "w3", tex: "\\Theta(\\log(n))" },
        ]),
        answer: "correct",
        reason: "El ciclo se detiene cuando \\(i^2 > n\\), lo que equivale a \\(i > \\sqrt{n}\\). Por tanto, la complejidad es \\(\\Theta(\\sqrt{n})\\).",
      };
    }
    const code = `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n    <span class="kw">for</span> j <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n        <span class="kw">for</span> k <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n            operar();\n        <span class="kw">end for</span>\n    <span class="kw">end for</span>\n<span class="kw">end for</span>`;
    return {
      signature: "asymp:cubic",
      code,
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

  function generateSimulation() {
    const kind = randomInt(0, 1);
    if (kind === 0) {
      const code = `conteo <span class="op">=</span> <span class="num">0</span>\n<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n    <span class="kw">for</span> j <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> i <span class="kw">do</span>\n        conteo <span class="op">=</span> conteo <span class="op">+</span> <span class="num">1</span>\n    <span class="kw">end for</span>\n<span class="kw">end for</span>`;
      return {
        signature: "sim:triangular",
        code,
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
        reason: "Al variar \\(n\\) se comprueba que para \\(n=5\\) el conteo da 15, para \\(n=10\\) da 55, coincidiendo exactamente con \\(\\frac{n(n+1)}{2}\\).",
      };
    }
    const code = `conteo <span class="op">=</span> <span class="num">0</span>\ni <span class="op">=</span> <span class="num">1</span>\n<span class="kw">while</span> i <span class="op">&lt;=</span> n <span class="kw">do</span>\n    conteo <span class="op">=</span> conteo <span class="op">+</span> <span class="num">1</span>\n    i <span class="op">=</span> i <span class="op">*</span> <span class="num">2</span>\n<span class="kw">end while</span>`;
    return {
      signature: "sim:log",
      code,
      prompt: "Simule el conteo en tiempo real al variar \\(n\\) para confirmar la función de conteo del bucle:",
      formulaFn: (n) => Math.floor(Math.log2(n)) + 1,
      formulaTex: "C(n) = \\lfloor \\log_2(n) \\rfloor + 1",
      initialN: 8,
      options: shuffled([
        { value: "correct", tex: "C(n) = \\lfloor \\log_2(n) \\rfloor + 1" },
        { value: "w1", tex: "C(n) = n / 2" },
        { value: "w2", tex: "C(n) = \\log_2(n)" },
        { value: "w3", tex: "C(n) = 2n" },
      ]),
      answer: "correct",
      reason: "Para \\(n=8\\) el conteo es 4 (pasos 1, 2, 4, 8); para \\(n=16\\) es 5, coincidiendo exactamente con \\(\\lfloor \\log_2(n) \\rfloor + 1\\).",
    };
  }

  function fallbackQuestion(mode, index) {
    const unique = 1000 + index;
    if (mode === "frequency") {
      return {
        signature: `fallback-f:${unique}`,
        code: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n<span class="target-line">    op();</span>\n<span class="kw">end for</span>`,
        prompt: "Considere el siguiente ciclo simple:",
        targetDescription: "la cantidad de ejecuciones de <code>op()</code>",
        options: [{ value: "correct", tex: "n" }, { value: "w1", tex: "n+1" }, { value: "w2", tex: "n-1" }, { value: "w3", tex: "2n" }],
        answer: "correct",
        reason: "Un ciclo simple de 1 a \\(n\\) ejecuta \\(n\\) veces.",
      };
    }
    if (mode === "cost") {
      return {
        signature: `fallback-c:${unique}`,
        code: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n    op();\n<span class="kw">end for</span>`,
        prompt: "Deduzca \\(C(n)\\) si cada iteración cuesta 1:",
        options: [{ value: "correct", tex: "C(n) = n" }, { value: "w1", tex: "C(n) = n^2" }],
        answer: "correct",
        reason: "\\(C(n) = n\\).",
      };
    }
    if (mode === "asymptotic") {
      return {
        signature: `fallback-a:${unique}`,
        code: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n    op();\n<span class="kw">end for</span>`,
        prompt: "Determine la cota ajustada:",
        options: [{ value: "correct", tex: "\\Theta(n)" }, { value: "w1", tex: "\\Theta(n^2)" }],
        answer: "correct",
        reason: "Es de orden lineal \\(\\Theta(n)\\).",
      };
    }
    return {
      signature: `fallback-s:${unique}`,
      code: `<span class="kw">for</span> i <span class="op">=</span> <span class="num">1</span> <span class="kw">to</span> n <span class="kw">do</span>\n    op();\n<span class="kw">end for</span>`,
      prompt: "Simule el conteo lineal:",
      formulaFn: (n) => n,
      formulaTex: "C(n) = n",
      initialN: 5,
      options: [{ value: "correct", tex: "C(n) = n" }, { value: "w1", tex: "C(n) = 2n" }],
      answer: "correct",
      reason: "El conteo coincide exactamente con \\(n\\).",
    };
  }

  function nextUniqueQuestion(mode, state) {
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
    const fallback = fallbackQuestion(mode, state.seen[mode].length);
    state.seen[mode].push(fallback.signature);
    return fallback;
  }

  // --- Funciones de renderizado ---

  function renderChoicesQuestion(container, question, modeClass = "") {
    clearMath(container);
    container.innerHTML = `<p class="self-check-practice__prompt">${question.prompt}</p>
      <div class="self-check-practice__code-box"><pre><code>${question.code}</code></pre></div>
      <fieldset class="self-check-practice__choices ${modeClass}">
        <legend>Seleccione la respuesta correcta</legend>
        ${question.options.map((opt) => `<label><input type="radio" name="chapter4-answer" value="${opt.value}"><span>\\(${opt.tex}\\)</span></label>`).join("")}
      </fieldset>`;
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
    container.innerHTML = `<p class="self-check-practice__prompt">${question.prompt}</p>
      <div class="self-check-practice__code-box"><pre><code>${question.code}</code></pre></div>
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
