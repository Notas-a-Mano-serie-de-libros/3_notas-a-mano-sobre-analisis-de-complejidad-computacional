(() => {
  "use strict";

  const masteryGoal = 3;
  const modes = {
    properties: {
      level: "Nivel 1 · Fundamentos matemáticos",
      title: "Propiedades formales de las funciones de complejidad",
      hint: "Recuerde las 3 propiedades de la sección 2.1.1: dominio restringido a \\(n \\in \\mathbb{N}\\), no negatividad (\\(C(n) \\ge 0\\)) y crecimiento monótono no decreciente (\\(n_1 \\le n_2 \\implies C(n_1) \\le C(n_2)\\)).",
    },
    canonical: {
      level: "Nivel 2 · Fórmulas canónicas",
      title: "Cálculo de tiempo t y memoria s",
      hint: "Aplique las relaciones canónicas: \\(t = T_0 \\cdot T(n)\\) y \\(s = S_0 \\cdot S(n)\\). Verifique cuidadosamente las unidades de tiempo y las conversiones de memoria (KB/MB vs KiB/MiB).",
    },
    crossover: {
      level: "Nivel 3 · Puntos de cruce",
      title: "Constantes ocultas vs. tasa de crecimiento",
      hint: "Resuelva la igualdad o inecuación \\(C_A(n) \\le C_B(n)\\) para encontrar a partir de qué umbral de entrada el costo de la función con menor tasa de crecimiento supera a la otra.",
    },
    viability: {
      level: "Nivel 4 · Viabilidad física y escala",
      title: "Simulador de muros computacionales de ejecución",
      hint: "Varíe el deslizador de tamaño de entrada \\(n\\) y observe en tiempo real qué órdenes de magnitud superan los límites físicos de viabilidad operativa.",
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
      // Ignorar si storage bloqueado
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

  // --- Generador Nivel 1: Propiedades formales de C(n) ---

  function generateProperties() {
    const kind = randomInt(0, 4);

    if (kind === 0) {
      // Parábola con raíces positivas: decrece y se hace negativa
      const r1 = randomInt(3, 6);
      const r2 = r1 + randomInt(4, 8);
      const b = r1 + r2;
      const c = r1 * r2;
      const vertex = Math.floor(b / 2);
      const salt = randomInt(10, 999);
      return {
        signature: `prop:quad:${b}:${c}:${salt}`,
        prompt: `Considere la función candidata \\(C(n) = n^2 - ${b}n + ${c}\\) definida para \\(n \\in \\mathbb{N}\\). Determine si cumple los requisitos formales de una función de complejidad:`,
        options: shuffled([
          { value: "correct", tex: `\\text{No es válida: viola la no negatividad y la monotonía (decrece para } n < ${vertex} \\text{ y es negativa en } (${r1}, ${r2})\\text{)}` },
          { value: "w1", tex: "\\text{Es válida porque al ser cuadrática siempre tiende a infinito cuando } n \\to \\infty" },
          { value: "w2", tex: "\\text{Es válida únicamente si se restringe el dominio a números reales positivos}" },
          { value: "w3", tex: "\\text{No es válida únicamente porque } n \\text{ no puede ser un número entero}" },
        ]),
        answer: "correct",
        reason: `Para \\(n \\in (${r1}, ${r2})\\), \\(C(n) < 0\\), lo que viola el postulado de no negatividad (\\(C(n) \\ge 0\\)). Además, su derivada \\(2n - ${b}\\) es negativa para \\(n < ${b}/2\\), violando el crecimiento monótono no decreciente.`,
      };
    }

    if (kind === 1) {
      // Función trigonométrica oscilatoria periódica
      const amp = randomInt(20, 80);
      const off = amp + randomInt(10, 30);
      const salt = randomInt(10, 999);
      return {
        signature: `prop:trig:${amp}:${off}:${salt}`,
        prompt: `Analice si la función analítica \\(C(n) = ${amp} \\cdot \\cos(n) + ${off}\\) es admisible para modelar el costo de un algoritmo en función de \\(n\\):`,
        options: shuffled([
          { value: "correct", tex: "\\text{No es válida: su comportamiento es periódico y oscilatorio, violando la monotonía no decreciente}" },
          { value: "w1", tex: "\\text{Es válida porque para todo } n \\in \\mathbb{N} \\text{ la función es estrictamente positiva}" },
          { value: "w2", tex: "\\text{Es válida porque las funciones trigonométricas están acotadas}" },
          { value: "w3", tex: "\\text{No es válida únicamente porque no está definida para números impares}" },
        ]),
        answer: "correct",
        reason: "Aunque \\(C(n) > 0\\) para todo \\(n\\), una función periódica oscila hacia arriba y abajo, violando la condición de que el costo acumulado no disminuye al aumentar el tamaño de entrada (\\(n_1 \\le n_2 \\implies C(n_1) \\le C(n_2)\\)).",
      };
    }

    if (kind === 2) {
      // Función estrictamente decreciente: 1/n o e^(-n)
      const k = randomInt(5, 50);
      const salt = randomInt(10, 999);
      return {
        signature: `prop:decay:${k}:${salt}`,
        prompt: `Considere la función \\(C(n) = \\frac{${k}}{n + 1}\\) para \\(n \\in \\mathbb{N}\\). Determine si satisface la definición de función de complejidad:`,
        options: shuffled([
          { value: "correct", tex: "\\text{No es válida: es monótonamente decreciente (el costo disminuiría a medida que entran más datos)}" },
          { value: "w1", tex: "\\text{Es válida porque es estrictamente no negativa para todo } n \\ge 0" },
          { value: "w2", tex: "\\text{Es válida porque modela algoritmos con costo sublineal perfecto}" },
          { value: "w3", tex: "\\text{No es válida únicamente porque tiene una asíntota en } n = 0" },
        ]),
        answer: "correct",
        reason: "Al incrementar \\(n\\), \\(C(n)\\) disminuye progresivamente hacia 0. En el análisis de complejidad, procesar mayor volumen de datos nunca puede reducir el costo de cómputo en el caso general.",
      };
    }

    if (kind === 3) {
      // Función con raíz cuadrada / sublineal válida
      const coef = randomInt(2, 6);
      const salt = randomInt(10, 999);
      return {
        signature: `prop:sqrt:${coef}:${salt}`,
        prompt: `Evalúe la función \\(C(n) = ${coef}\\sqrt{n} + \\log_2(n + 1)\\) con \\(n \\in \\mathbb{N}\\):`,
        options: shuffled([
          { value: "correct", tex: "\\text{Es válida: cumple dominio en } \\mathbb{N}\\text{, es no negativa y monótonamente no decreciente}" },
          { value: "w1", tex: "\\text{No es válida porque las raíces cuadradas generan números irracionales}" },
          { value: "w2", tex: "\\text{No es válida porque la función crece más lento que una función lineal}" },
          { value: "w3", tex: "\\text{Es válida únicamente si } n \\text{ es un cuadrado perfecto}" },
        ]),
        answer: "correct",
        reason: "La función está bien definida para todo número natural \\(n \\ge 0\\), su valor es estrictamente no negativo (\\(C(n) \\ge 0\\)) y su primera derivada es positiva para todo \\(n > 0\\), garantizando monotonía no decreciente.",
      };
    }

    // Caso 4: Polinomio monótono no decreciente válido
    const a = randomInt(2, 5);
    const b = randomInt(3, 9);
    const c = randomInt(1, 10);
    const salt = randomInt(10, 999);
    return {
      signature: `prop:poly:${a}:${b}:${c}:${salt}`,
      prompt: `Evalúe la función \\(C(n) = ${a}n^2 + ${b}n + ${c}\\) para \\(n \\in \\mathbb{N}\\):`,
      options: shuffled([
        { value: "correct", tex: "\\text{Es completamente válida: satisface restricción del dominio, no negatividad y crecimiento monótono}" },
        { value: "w1", tex: "\\text{No es válida porque tiene un término independiente que no depende de } n" },
        { value: "w2", tex: "\\text{No es válida porque mezcla órdenes cuadrático y lineal}" },
        { value: "w3", tex: "\\text{Es válida únicamente cuando } n \\to \\infty" },
      ]),
      answer: "correct",
      reason: "Con coeficientes estrictamente positivos, \\(C(n) \\ge 0\\) para todo \\(n \\ge 0\\) y para cualesquiera \\(n_1 \\le n_2\\) se tiene \\(C(n_1) \\le C(n_2)\\).",
    };
  }

  // --- Generador Nivel 2: Fórmulas canónicas t = T0 * T(n) y s = S0 * S(n) ---

  function generateCanonical() {
    const kind = randomInt(0, 4);

    // Tipo 0: Tiempo lineal o log-lineal
    if (kind === 0) {
      const isLogLinear = pickRandom([true, false]);
      const nExp = randomInt(4, 6);
      const n = Math.pow(10, nExp);
      const t0Micros = pickRandom([1, 2, 5, 10]); // microsegundos
      const t0 = t0Micros * 1e-6;
      const salt = randomInt(10, 999);

      if (isLogLinear) {
        // n = 10^5 o 10^6, aprox log2(n)
        const log2Val = Math.round(Math.log2(n));
        const totalOps = n * log2Val;
        const totalSec = totalOps * t0;
        const signature = `canon:time:nlogn:${nExp}:${t0Micros}:${salt}`;

        return {
          signature,
          prompt: `Una máquina ejecuta una instrucción en un tiempo medio \\(T_0 = ${t0Micros} \\times 10^{-6}\\text{ s}\\) (\\(${t0Micros}\\,\\mu\\text{s}\\)). Si un algoritmo tiene complejidad temporal \\(T(n) = n \\log_2(n)\\) con \\(n = 10^{${nExp}}\\) datos (asumiendo \\(\\log_2(10^{${nExp}}) \\approx ${log2Val}\\)), calcule el tiempo total teórico \\(t = T_0 \\cdot T(n)\\):`,
          options: shuffled([
            { value: "correct", tex: `t \\approx ${totalSec.toFixed(2)}\\text{ s}` },
            { value: "w1", tex: `t \\approx ${(totalSec * 10).toFixed(2)}\\text{ s}` },
            { value: "w2", tex: `t \\approx ${(totalSec / log2Val).toFixed(2)}\\text{ s}` },
            { value: "w3", tex: `t \\approx ${(totalSec * 2).toFixed(2)}\\text{ s}` },
          ]),
          answer: "correct",
          reason: `\\(T(${n.toExponential()}) = 10^{${nExp}} \\cdot ${log2Val} = ${(n * log2Val).toExponential()}\\) operaciones. Luego, \\(t = ${t0Micros}\\times 10^{-6} \\cdot ${(n * log2Val).toExponential()} = ${totalSec.toFixed(2)}\\text{ s}\\).`,
        };
      }

      const totalSec = n * t0;
      const signature = `canon:time:linear:${nExp}:${t0Micros}:${salt}`;
      return {
        signature,
        prompt: `Una computadora procesa cada operación elemental en \\(T_0 = ${t0Micros} \\times 10^{-6}\\text{ s}\\). Para un algoritmo de complejidad lineal \\(T(n) = n\\) con entrada \\(n = 10^{${nExp}}\\) datos, calcule el tiempo total teórico \\(t\\):`,
        options: shuffled([
          { value: "correct", tex: `t = ${totalSec.toFixed(totalSec < 1 ? 3 : 2)}\\text{ s}` },
          { value: "w1", tex: `t = ${(totalSec * 1000).toFixed(1)}\\text{ s}` },
          { value: "w2", tex: `t = ${(totalSec / 10).toFixed(3)}\\text{ s}` },
          { value: "w3", tex: `t = ${(totalSec * 60).toFixed(2)}\\text{ s}` },
        ]),
        answer: "correct",
        reason: `\\(t = T_0 \\cdot T(n) = (${t0Micros} \\times 10^{-6}\\text{ s}) \\cdot 10^{${nExp}} = ${totalSec.toFixed(3)}\\text{ s}\\).`,
      };
    }

    // Tipo 1: Tiempo cuadrático o cúbico
    if (kind === 1) {
      const isCubic = pickRandom([true, false]);
      const n = isCubic ? pickRandom([200, 400, 500]) : pickRandom([1000, 2000, 5000]);
      const t0Millis = pickRandom([1, 2, 4]); // milisegundos
      const t0 = t0Millis * 1e-3;
      const salt = randomInt(10, 999);

      if (isCubic) {
        const ops = Math.pow(n, 3);
        const sec = ops * t0;
        const signature = `canon:cubic:${n}:${t0Millis}:${salt}`;
        return {
          signature,
          prompt: `Suponga que cada operación básica requiere \\(T_0 = ${t0Millis}\\text{ ms}\\) (\\(${t0Millis * 1e-3}\\text{ s}\\)) y la complejidad temporal es \\(T(n) = n^3\\). Para un tamaño de entrada \\(n = ${n}\\), determine el tiempo total \\(t = T_0 \\cdot T(n)\\):`,
          options: shuffled([
            { value: "correct", tex: `t = ${sec.toLocaleString("es-CO")}\\text{ s}` },
            { value: "w1", tex: `t = ${(sec / 10).toLocaleString("es-CO")}\\text{ s}` },
            { value: "w2", tex: `t = ${(sec * 1000).toLocaleString("es-CO")}\\text{ s}` },
            { value: "w3", tex: `t = ${(sec / n).toFixed(1)}\\text{ s}` },
          ]),
          answer: "correct",
          reason: `\\(T(${n}) = ${n}^3 = ${ops.toExponential()}\\) operaciones. Multiplicando por \\(T_0 = ${t0Millis * 1e-3}\\text{ s}\\) resulta \\(t = ${sec.toLocaleString("es-CO")}\\text{ s}\\).`,
        };
      }

      const ops = n * n;
      const sec = ops * t0;
      const signature = `canon:quad:${n}:${t0Millis}:${salt}`;
      return {
        signature,
        prompt: `Un algoritmo cuadrático \\(T(n) = n^2\\) se ejecuta en un procesador donde \\(T_0 = ${t0Millis}\\text{ ms}\\) (\\(${t0Millis * 1e-3}\\text{ s}\\)). Calcule el tiempo total \\(t\\) requerido para procesar \\(n = ${n.toLocaleString("es-CO")}\\) elementos:`,
        options: shuffled([
          { value: "correct", tex: `t = ${sec.toLocaleString("es-CO")}\\text{ s}` },
          { value: "w1", tex: `t = ${(sec / 1000).toFixed(2)}\\text{ s}` },
          { value: "w2", tex: `t = ${(sec * 2).toLocaleString("es-CO")}\\text{ s}` },
          { value: "w3", tex: `t = ${(n * t0).toFixed(1)}\\text{ s}` },
        ]),
        answer: "correct",
        reason: `\\(T(${n}) = ${n}^2 = ${ops.toLocaleString("es-CO")}\\) operaciones. \\(t = (${t0Millis * 1e-3}\\text{ s}) \\cdot ${ops} = ${sec.toLocaleString("es-CO")}\\text{ s}\\).`,
      };
    }

    // Tipo 2: Consumo de memoria espacial y prefijos (KB vs KiB)
    if (kind === 2) {
      const s0 = pickRandom([4, 8, 16]); // bytes
      const n = pickRandom([10000, 20000, 40000]);
      const isKiB = pickRandom([true, false]);
      const salt = randomInt(10, 999);
      const totalBytes = s0 * n;

      if (isKiB) {
        const kib = totalBytes / 1024;
        const signature = `canon:space:kib:${s0}:${n}:${salt}`;
        return {
          signature,
          prompt: `Un algoritmo con complejidad espacial lineal \\(S(n) = n\\) consume \\(S_0 = ${s0}\\text{ bytes}\\) por elemento. Calcule la memoria total \\(s = S_0 \\cdot S(n)\\) para \\(n = ${n.toLocaleString("es-CO")}\\) datos, expresada exactamente en **kibibytes (KiB)** (donde \\(1\\text{ KiB} = 1\\,024\\text{ bytes}\\)):`,
          options: shuffled([
            { value: "correct", tex: `s \\approx ${kib.toFixed(2)}\\text{ KiB}` },
            { value: "w1", tex: `s = ${(totalBytes / 1000).toFixed(1)}\\text{ KiB}` },
            { value: "w2", tex: `s \\approx ${(kib * 1024).toFixed(0)}\\text{ KiB}` },
            { value: "w3", tex: `s \\approx ${(kib / 8).toFixed(2)}\\text{ KiB}` },
          ]),
          answer: "correct",
          reason: `Total en bytes: \\(s = ${s0} \\times ${n} = ${totalBytes.toLocaleString("es-CO")}\\text{ B}\\). Dividiendo entre 1.024 bytes por KiB: \\(\\frac{${totalBytes}}{1\\,024} \\approx ${kib.toFixed(2)}\\text{ KiB}\\).`,
        };
      }

      const kb = totalBytes / 1000;
      const signature = `canon:space:kb:${s0}:${n}:${salt}`;
      return {
        signature,
        prompt: `Un sistema almacena \\(S_0 = ${s0}\\text{ bytes}\\) por registro. Para un algoritmo con \\(S(n) = n\\) y una entrada de \\(n = ${n.toLocaleString("es-CO")}\\) datos, determine el consumo total en **kilobytes decimales (KB)** (donde \\(1\\text{ KB} = 10^3\\text{ bytes}\\)):`,
        options: shuffled([
          { value: "correct", tex: `s = ${kb.toFixed(1)}\\text{ KB}` },
          { value: "w1", tex: `s \\approx ${(totalBytes / 1024).toFixed(2)}\\text{ KB}` },
          { value: "w2", tex: `s = ${(kb * 1000).toLocaleString("es-CO")}\\text{ KB}` },
          { value: "w3", tex: `s = ${(kb / 8).toFixed(2)}\\text{ KB}` },
        ]),
        answer: "correct",
        reason: `Total bytes: \\(s = ${s0} \\times ${n} = ${totalBytes.toLocaleString("es-CO")}\\text{ B}\\). En el estándar decimal SI, \\(1\\text{ KB} = 1\\,000\\text{ B}\\), por lo que \\(s = ${kb.toFixed(1)}\\text{ KB}\\).`,
      };
    }

    // Tipo 3: Capacidad máxima antes de agotar memoria límite
    if (kind === 3) {
      const memMb = pickRandom([64, 128, 256, 512]);
      const s0 = pickRandom([8, 16, 32]);
      const memBytes = memMb * 1024 * 1024;
      const maxN = Math.floor(memBytes / s0);
      const salt = randomInt(10, 999);
      const signature = `canon:maxN:${memMb}:${s0}:${salt}`;

      return {
        signature,
        prompt: `Un dispositivo embebido dispone de exactamente \\(${memMb}\\text{ MiB}\\) de memoria libre (\\(${memMb} \\times 2^{20}\\text{ bytes}\\)). Si un algoritmo consume \\(S_0 = ${s0}\\text{ bytes}\\) por registro con complejidad espacial \\(S(n) = n\\), ¿cuántos elementos \\(n\\) puede almacenar como máximo sin desbordar la memoria?`,
        options: shuffled([
          { value: "correct", tex: `n_{\\max} = ${maxN.toLocaleString("es-CO")}\\text{ elementos}` },
          { value: "w1", tex: `n_{\\max} = ${(memMb * 1000000 / s0).toFixed(0)}\\text{ elementos}` },
          { value: "w2", tex: `n_{\\max} = ${(maxN / 2).toLocaleString("es-CO")}\\text{ elementos}` },
          { value: "w3", tex: `n_{\\max} = ${(maxN * s0).toExponential(2)}\\text{ elementos}` },
        ]),
        answer: "correct",
        reason: `Memoria disponible: \\(${memMb} \\times 1\\,048\\,576 = ${memBytes.toLocaleString("es-CO")}\\text{ bytes}\\). Dividiendo entre \\(S_0 = ${s0}\\text{ bytes/elem}\\): \\(n_{\\max} = \\lfloor ${memBytes} / ${s0} \\rfloor = ${maxN.toLocaleString("es-CO")}\\) elementos.`,
      };
    }

    // Tipo 4: Explosión exponencial o factorial
    const n = pickRandom([20, 25, 30]);
    const salt = randomInt(10, 999);
    const signature = `canon:exp:${n}:${salt}`;
    const ops = Math.pow(2, n);
    // en segundos si T0 = 1 microsegundo
    const sec = ops * 1e-6;
    const days = sec / 86400;

    return {
      signature,
      prompt: `Si un algoritmo tiene complejidad temporal exponencial \\(T(n) = 2^n\\) y una máquina ejecuta \\(10^6\\) instrucciones por segundo (\\(T_0 = 1\\,\\mu\\text{s}\\)), calcule el tiempo total teórico aproximado para procesar apenas \\(n = ${n}\\) datos:`,
      options: shuffled([
        { value: "correct", tex: n < 25 ? `t \\approx ${sec.toFixed(1)}\\text{ segundos}` : `t \\approx ${days.toFixed(1)}\\text{ días}` },
        { value: "w1", tex: `t \\approx ${(n * 1e-6).toFixed(4)}\\text{ segundos}` },
        { value: "w2", tex: `t \\approx ${(n * n * 1e-6).toFixed(4)}\\text{ segundos}` },
        { value: "w3", tex: `t \\approx ${Math.pow(10, n / 10).toFixed(1)}\\text{ milisegundos}` },
      ]),
      answer: "correct",
      reason: `\\(T(${n}) = 2^{${n}} = ${ops.toLocaleString("es-CO")}\\) operaciones. Con \\(T_0 = 10^{-6}\\text{ s}\\), el tiempo es \\(t = ${ops} \\times 10^{-6}\\text{ s} = ${sec.toFixed(1)}\\text{ s}\\)${n >= 25 ? ` \\((\\approx ${days.toFixed(1)}\\text{ días})\\)` : ""}, ilustrando por qué el crecimiento exponencial se vuelve físicamente inviable para valores moderados de \\(n\\).`,
    };
  }

  // --- Generador Nivel 3: Puntos de cruce (Constantes vs. Crecimiento) ---

  function generateCrossover() {
    const kind = randomInt(0, 2);

    if (kind === 0) {
      // Lineal con constante grande vs. Cuadrática con constante pequeña
      // c1 * n = c2 * n^2  => n_cruce = c1 / c2
      const c2 = pickRandom([0.05, 0.1, 0.2, 0.5]);
      const nCruce = pickRandom([200, 500, 1000, 2000]);
      const c1 = Math.round(c2 * nCruce);
      const salt = randomInt(10, 999);
      const signature = `cross:lin-quad:${c1}:${c2}:${salt}`;

      return {
        signature,
        prompt: `Considere dos algoritmos alternativos para resolver la misma tarea con funciones de costo:
          \\[ C_A(n) = ${c1}n \\qquad C_B(n) = ${c2}n^2 \\]
          Determine a partir de qué tamaño de entrada \\(n\\) el algoritmo lineal \\(A\\) es estrictamente más eficiente que el algoritmo cuadrático \\(B\\) (es decir, \\(C_A(n) < C_B(n)\\)):`,
        options: shuffled([
          { value: "correct", tex: `n > ${nCruce}` },
          { value: "w1", tex: `n > ${Math.round(nCruce / 2)}` },
          { value: "w2", tex: `n > ${nCruce * 2}` },
          { value: "w3", tex: "\\text{El algoritmo } A \\text{ siempre es mejor para todo } n \\ge 1" },
        ]),
        answer: "correct",
        reason: `Igualando costos: \\(${c1}n = ${c2}n^2 \\implies n = \\frac{${c1}}{${c2}} = ${nCruce}\\). Para \\(n < ${nCruce}\\), el algoritmo cuadrático \\(B\\) ejecuta menos operaciones gracias a su coeficiente menor. El algoritmo lineal \\(A\\) solo resulta más eficiente cuando \\(n > ${nCruce}\\).`,
      };
    }

    if (kind === 1) {
      // Constante fija grande vs. Lineal
      // c_fijo vs c_lin * n => n_cruce = c_fijo / c_lin
      const cLin = pickRandom([2, 5, 10]);
      const nCruce = pickRandom([50, 100, 250, 500]);
      const cFijo = cLin * nCruce;
      const salt = randomInt(10, 999);
      const signature = `cross:const-lin:${cFijo}:${cLin}:${salt}`;

      return {
        signature,
        prompt: `Un algoritmo \\(A\\) realiza una inicialización costosa independiente de la entrada \\(C_A(n) = ${cFijo.toLocaleString("es-CO")}\\) (complejidad constante), mientras que otro algoritmo \\(B\\) tiene costo lineal \\(C_B(n) = ${cLin}n\\). ¿Para qué valores de \\(n\\) resulta preferible el algoritmo de costo constante \\(A\\)?`,
        options: shuffled([
          { value: "correct", tex: `n > ${nCruce}` },
          { value: "w1", tex: `n < ${nCruce}` },
          { value: "w2", tex: `n = ${cFijo}` },
          { value: "w3", tex: "\\text{Nunca es preferible porque su costo base es muy alto}" },
        ]),
        answer: "correct",
        reason: `Para \\(n < ${nCruce}\\), \\(${cLin}n < ${cFijo}\\), por lo que el algoritmo lineal \\(B\\) es más rápido. Para \\(n > ${nCruce}\\), el costo lineal supera a la constante y el algoritmo \\(A\\) se vuelve más ventajoso.`,
      };
    }

    // Cuadrática vs Exponencial (n^2 vs 2^n)
    // Para n pequeños: n^2 vs 2^n. 2^n sobrepasa a n^2 a partir de n = 5 (2^4=16 vs 4^2=16; 2^5=32 > 25)
    // Con constante: c * n^2 vs 2^n
    const salt = randomInt(10, 999);
    const signature = `cross:quad-exp:${salt}`;
    return {
      signature,
      prompt: `Considere las funciones \\(C_1(n) = 16n^2\\) y \\(C_2(n) = 2^n\\). Calcule a partir de qué valor entero de \\(n\\) la función exponencial \\(C_2(n)\\) supera permanentemente a la cuadrática \\(C_1(n)\\):`,
      options: shuffled([
        { value: "correct", tex: "n \\ge 9 \\quad (2^9 = 512 > 16 \\times 9^2 = 1\\,296 \\dots \\text{en } n=11: 2^{11} = 2\\,048 > 16\\times 121=1\\,936)" },
        { value: "w1", tex: "n \\ge 4" },
        { value: "w2", tex: "n \\ge 30" },
        { value: "w3", tex: "n \\ge 2" },
      ]),
      answer: "correct",
      reason: "Para \\(n=10\\): \\(16(10^2) = 1\\,600\\) y \\(2^{10} = 1\\,024\\). Para \\(n=11\\): \\(16(11^2) = 1\\,936\\) y \\(2^{11} = 2\\,048\\). A partir de \\(n = 11\\) la exponencial domina definitivamente a la función cuadrática.",
    };
  }

  // --- Generador Nivel 4: Viabilidad física y escala interactiva ---

  function generateViability() {
    const kind = randomInt(0, 2);

    if (kind === 0) {
      // Restricción de tiempo límite (ejercicio 4 y 6 del libro)
      const maxSec = pickRandom([1, 5, 10]);
      const nExp = randomInt(5, 7);
      const n = Math.pow(10, nExp);
      const t0Micros = pickRandom([1, 2, 5]);
      const t0 = t0Micros * 1e-6;
      const maxOps = maxSec / t0; // max operaciones permitidas
      const salt = randomInt(10, 999);
      const signature = `viab:limit:${maxSec}:${nExp}:${t0Micros}:${salt}`;

      // n = 10^6:
      // lineal: 10^6 ops
      // n log n: ~ 2 * 10^7 ops
      // n^2: 10^12 ops
      return {
        signature,
        prompt: `Por restricciones de diseño en tiempo real, un sistema debe procesar \\(n = 10^{${nExp}}\\) datos en menos de \\(${maxSec}\\text{ segundos}\\). La arquitectura disponible ejecuta cada instrucción elemental en \\(T_0 = ${t0Micros}\\,\\mu\\text{s}\\) (máximo admitido: \\(\\frac{${maxSec}\\text{ s}}{${t0Micros}\\times 10^{-6}\\text{ s}} = ${maxOps.toExponential()}\\) operaciones). ¿Cuál es la mayor familia de complejidad admisible que cumple estrictamente esta restricción?`,
        options: shuffled([
          { value: "correct", tex: maxOps >= n * Math.log2(n) ? "\\text{Log-lineal } T(n) = n\\log_2(n)" : "\\text{Lineal } T(n) = n" },
          { value: "w1", tex: "\\text{Cuadrática } T(n) = n^2" },
          { value: "w2", tex: "\\text{Exponencial } T(n) = 2^n" },
          { value: "w3", tex: "\\text{Cúbica } T(n) = n^3" },
        ]),
        answer: "correct",
        reason: `Para \\(n = 10^{${nExp}}\\), una complejidad cuadrática requeriría \\(10^{${2 * nExp}}\\) operaciones (\\(${((Math.pow(10, 2 * nExp) * t0) / 3600).toFixed(1)}\\text{ horas}\\)), superando catastróficamente los ${maxSec} s. La máxima familia viable bajo este límite de reloj es la opción indicada.`,
      };
    }

    if (kind === 1) {
      // Sensibilidad de escala: qué pasa si duplicamos o decuplicamos n
      const factor = pickRandom([2, 10]);
      const salt = randomInt(10, 999);
      const signature = `viab:scale:quad:${factor}:${salt}`;
      const mult = factor * factor;

      return {
        signature,
        prompt: `Si un algoritmo tiene complejidad temporal estrictamente cuadrática \\(T(n) = n^2\\) y se multiplica el tamaño de la entrada por un factor de \\(${factor}\\) (es decir, \\(n_{\\text{nuevo}} = ${factor}n\\)), ¿por qué factor se multiplica el tiempo de ejecución \\(t\\)?`,
        options: shuffled([
          { value: "correct", tex: `\\text{Se multiplica por } ${mult} \\quad (${factor}^2)` },
          { value: "w1", tex: `\\text{Se multiplica por } ${factor}` },
          { value: "w2", tex: `\\text{Se multiplica por } ${factor * 2}` },
          { value: "w3", tex: `\\text{Aumenta en una constante aditiva } +${mult}` },
        ]),
        answer: "correct",
        reason: `Para funciones homogéneas de grado 2: \\(T(${factor}n) = (${factor}n)^2 = ${factor}^2 \\cdot n^2 = ${mult} \\cdot T(n)\\). Al aumentar la entrada ${factor} veces, el tiempo se incrementa ${mult} veces.`,
      };
    }

    // Regla de escala para exponencial
    const salt = randomInt(10, 999);
    const signature = `viab:scale:exp:${salt}`;
    return {
      signature,
      prompt: "Si un algoritmo tiene complejidad exponencial \\(T(n) = 2^n\\), ¿qué ocurre con el número de operaciones requeridas si el tamaño de entrada aumenta en apenas una unidad (\\(n \\to n + 1\\))?",
      options: shuffled([
        { value: "correct", tex: "\\text{El número total de operaciones se duplica exactamente } (\\times 2)" },
        { value: "w1", tex: "\\text{El número total de operaciones aumenta en 2 unidades } (+2)" },
        { value: "w2", tex: "\\text{El número de operaciones aumenta en } n^2" },
        { value: "w3", tex: "\\text{No sufre variaciones perceptibles}" },
      ]),
      answer: "correct",
      reason: "\\(T(n+1) = 2^{n+1} = 2 \\cdot 2^n = 2 \\cdot T(n)\\). Cada dato adicional duplica por completo la carga de trabajo de la máquina, lo que explica la inviabilidad física de los algoritmos de fuerza bruta.",
    };
  }

  function fallbackQuestion(mode, index) {
    const unique = Date.now() + index;
    if (mode === "properties") {
      return {
        signature: `fallback-prop:${unique}`,
        prompt: "Considere \\(C(n) = 5n + 10\\) con \\(n \\in \\mathbb{N}\\). ¿Es una función de complejidad válida?",
        options: [{ value: "correct", tex: "\\text{Sí, cumple todas las propiedades formales}" }, { value: "w1", tex: "\\text{No}" }],
        answer: "correct",
        reason: "Es no negativa y monótona no decreciente en \\(\\mathbb{N}\\).",
      };
    }
    if (mode === "canonical") {
      return {
        signature: `fallback-canon:${unique}`,
        prompt: "Si \\(T_0 = 0.001\\text{ s}\\) y \\(T(n) = n\\), para \\(n = 5000\\) calcule \\(t\\):",
        options: [{ value: "correct", tex: "t = 5\\text{ s}" }, { value: "w1", tex: "t = 50\\text{ s}" }],
        answer: "correct",
        reason: "\\(t = 0.001 \\times 5000 = 5\\text{ s}\\).",
      };
    }
    if (mode === "crossover") {
      return {
        signature: `fallback-cross:${unique}`,
        prompt: "Si \\(C_A(n) = 100n\\) y \\(C_B(n) = n^2\\), ¿para qué valor de \\(n\\) se igualan los costos?",
        options: [{ value: "correct", tex: "n = 100" }, { value: "w1", tex: "n = 10" }],
        answer: "correct",
        reason: "\\(100n = n^2 \\implies n = 100\\).",
      };
    }
    return {
      signature: `fallback-viab:${unique}`,
      prompt: "En una función lineal \\(T(n) = n\\), si la entrada se triplica (\\(3n\\)), ¿por cuánto se multiplica el tiempo?",
      options: [{ value: "correct", tex: "\\text{Por 3}" }, { value: "w1", tex: "\\text{Por 9}" }],
      answer: "correct",
      reason: "\\(T(3n) = 3n = 3T(n)\\).",
    };
  }

  function nextUniqueQuestion(mode, state) {
    if (state.seen[mode].length > 30) {
      state.seen[mode] = state.seen[mode].slice(-15);
    }
    const seen = new Set(state.seen[mode]);
    for (let attempt = 0; attempt < 500; attempt += 1) {
      const q = mode === "properties" ? generateProperties()
        : mode === "canonical" ? generateCanonical()
          : mode === "crossover" ? generateCrossover()
            : generateViability();
      if (!seen.has(q.signature)) {
        state.seen[mode].push(q.signature);
        return q;
      }
    }
    state.seen[mode] = [];
    const fallback = fallbackQuestion(mode, state.seen[mode].length);
    state.seen[mode].push(fallback.signature);
    return fallback;
  }

  function renderChoicesQuestion(container, question) {
    clearMath(container);
    container.innerHTML = `<p class="self-check-practice__prompt">${question.prompt}</p>
      <fieldset class="self-check-practice__choices">
        <legend>Seleccione la respuesta correcta</legend>
        ${question.options.map((opt) => `<label><input type="radio" name="chapter2-answer" value="${opt.value}"><span>\\(${opt.tex}\\)</span></label>`).join("")}
      </fieldset>`;
    typesetMath(container);
  }

  function evaluateStandard(container, question) {
    const selected = container.querySelector("input[name='chapter2-answer']:checked");
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
    let mode = "properties";
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
      renderChoicesQuestion(questionContainer, current);
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

  function prepareChapter2Practice(root = document) {
    root.querySelectorAll("[data-chapter2-practice]").forEach(initializePractice);
  }

  if (typeof document$ !== "undefined") document$.subscribe(prepareChapter2Practice);
  else document.addEventListener("DOMContentLoaded", () => prepareChapter2Practice());
})();
