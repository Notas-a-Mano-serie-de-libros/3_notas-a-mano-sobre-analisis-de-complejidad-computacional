(() => {
  const workerURL = new URL("python-worker.js", document.currentScript.src);
  const keywords = new Set("False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield".split(" "));
  const builtins = new Set("abs all any bool dict enumerate float int isinstance len list max min object print range repr reversed set sorted str sum super tuple type ValueError OverflowError ZeroDivisionError NotImplementedError".split(" "));
  // Los nombres de clase coinciden con los tokens Pygments del tema de Pages.
  const tokenPattern = /(?:[rRuUbBfF]{0,2}(?:"""[\s\S]*?(?:"""|$)|'''[\s\S]*?(?:'''|$)|"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?))|#[^\n]*|(?:0[xX][\da-fA-F_]+|0[bB][01_]+|0[oO][0-7_]+|(?:\d[\d_]*(?:\.[\d_]*)?|\.\d[\d_]*)(?:[eE][+-]?[\d_]+)?[jJ]?)|[A-Za-z_][A-Za-z_0-9]*|(?:\*\*|\/\/|<<|>>|:=|==|!=|<=|>=|[-+*\/%&|^~<>=])|[^\w\s]|\s+/g;
  const repaint = (editor, code) => {
    const fragment = document.createDocumentFragment();
    let expectedName = null;
    for (const match of editor.value.matchAll(tokenPattern)) {
      const value = match[0];
      let kind = "";
      if (value.startsWith("#")) kind = "c1";
      else if (/^[rRuUbBfF]{0,2}["']/.test(value)) kind = "s";
      else if (/^(?:\d|\.\d)/.test(value)) kind = /[.eEjJ]/.test(value) ? "mf" : "mi";
      else if (keywords.has(value)) { kind = ["and", "or", "not", "in", "is"].includes(value) ? "ow" : ["True", "False", "None"].includes(value) ? "kc" : ["import", "from", "as"].includes(value) ? "kn" : "k"; if (value === "def" || value === "class") expectedName = value === "def" ? "nf" : "nc"; }
      else if (/^[A-Za-z_]/.test(value)) { kind = expectedName || (builtins.has(value) ? "nb" : "n"); expectedName = null; }
      else if (/^[-+*\/%&|^~<>=]/.test(value) || value === ":=") kind = "o";
      if (kind) { const span = document.createElement("span"); span.className = kind; span.textContent = value; fragment.append(span); }
      else fragment.append(document.createTextNode(value));
    }
    fragment.append(document.createTextNode("\n"));
    code.replaceChildren(fragment);
  };
  let worker = null;
  let active = null;
  let timeout = null;
  const finish = (message, output, terminate = false) => {
    clearTimeout(timeout);
    if (active) {
      active.querySelector("[data-run]").disabled = false;
      active.querySelector("[data-stop]").disabled = true;
      active.querySelector("[data-status]").textContent = message;
      if (output !== undefined) active.querySelector("[data-output]").textContent = output;
    }
    active = null;
    if (terminate) { worker?.terminate(); worker = null; }
  };
  const initialize = () => {
    if (active && !active.isConnected) finish("Ejecución detenida al cambiar de página.", undefined, true);
    document.querySelectorAll("[data-example-runner]").forEach((panel) => {
      if (panel.dataset.initialized) return;
      panel.dataset.initialized = "true";
      const editor = panel.querySelector("textarea");
      const initial = editor.value;
      const colored = panel.querySelector(".python-code-editor code");
      const preview = panel.querySelector(".python-code-editor pre");
      const initialHighlight = colored.innerHTML;
      const syncScroll = () => { preview.scrollTop = editor.scrollTop; preview.scrollLeft = editor.scrollLeft; };
      editor.addEventListener("input", () => { repaint(editor, colored); syncScroll(); });
      editor.addEventListener("scroll", syncScroll);
      editor.addEventListener("keydown", (event) => {
        if (event.key !== "Tab" || event.shiftKey) return;
        event.preventDefault();
        editor.setRangeText("    ", editor.selectionStart, editor.selectionEnd, "end");
        repaint(editor, colored);
        syncScroll();
      });
      panel.querySelector("[data-reset]").addEventListener("click", () => {
        if (active === panel) finish("Ejecución detenida.", undefined, true);
        editor.value = initial;
        colored.innerHTML = initialHighlight;
        editor.scrollTop = 0;
        editor.scrollLeft = 0;
        syncScroll();
        panel.querySelector("[data-status]").textContent = "Ejemplo restablecido.";
        panel.querySelector("[data-output]").textContent = "El resultado aparecerá aquí.";
      });
      panel.querySelector("[data-stop]").addEventListener("click", () => finish("Ejecución detenida.", undefined, true));
      panel.querySelector("[data-run]").addEventListener("click", () => {
        if (active) finish("Ejecución detenida para iniciar otro ejemplo.", undefined, true);
        active = panel;
        panel.querySelector("[data-run]").disabled = true;
        panel.querySelector("[data-stop]").disabled = false;
        panel.querySelector("[data-status]").textContent = "Preparando Python… La primera carga puede tardar unos segundos.";
        panel.querySelector("[data-output]").textContent = "";
        if (!worker) {
          try { worker = new Worker(workerURL, { type: "module" }); }
          catch (error) { finish("No se pudo iniciar Python.", error.message, true); return; }
          worker.onerror = () => finish("No se pudo cargar Python. Revisa la conexión y vuelve a intentar.", undefined, true);
          worker.onmessage = ({ data }) => {
            if (!active) return;
            if (data.type === "ready") {
              active.querySelector("[data-status]").textContent = "Ejecutando…";
              clearTimeout(timeout);
              timeout = setTimeout(() => finish("Ejecución detenida: superó 10 segundos. Prueba entradas más pequeñas.", undefined, true), 10000);
            } else if (data.type === "done") {
              finish(data.error ? "Revisa el error mostrado en el resultado." : "Ejecución completada.", data.output);
            }
          };
        }
        timeout = setTimeout(() => finish("La carga de Python tardó demasiado. Vuelve a intentar.", undefined, true), 90000);
        worker.postMessage({ code: editor.value });
      });
    });
  };
  if (typeof document$ !== "undefined") document$.subscribe(initialize);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initialize);
  else initialize();
})();
