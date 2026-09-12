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
      const lines = [...panel.querySelectorAll("[data-code-line]")];
      const editableLines = lines.filter(line => line.hasAttribute("data-editable"));
      const initial = editableLines.map(line => line.innerHTML);
      const source = () => lines.map(line => line.textContent).join("\n") + "\n";
      const refreshLine = (line) => {
        const selection = window.getSelection();
        const range = document.createRange();
        range.selectNodeContents(line);
        let offset = line.textContent.length;
        if (selection.rangeCount && line.contains(selection.anchorNode)) {
          range.setEnd(selection.anchorNode, selection.anchorOffset);
          offset = range.toString().length;
        }
        const value = line.textContent.replace(/[\r\n]/g, " ");
        repaint({ value }, line);
        const walker = document.createTreeWalker(line, NodeFilter.SHOW_TEXT);
        let node;
        while ((node = walker.nextNode())) {
          if (offset <= node.length) {
            selection.setBaseAndExtent(node, offset, node, offset);
            return;
          }
          offset -= node.length;
        }
      };
      editableLines.forEach(line => {
        line.addEventListener("beforeinput", event => {
          if (["insertParagraph", "insertLineBreak"].includes(event.inputType)) event.preventDefault();
        });
        line.addEventListener("keydown", event => {
          if (event.key === "Enter") event.preventDefault();
        });
        line.addEventListener("input", () => refreshLine(line));
        line.addEventListener("paste", event => {
          event.preventDefault();
          const selection = window.getSelection();
          if (!selection.rangeCount) return;
          const range = selection.getRangeAt(0);
          if (!line.contains(range.commonAncestorContainer)) return;
          range.deleteContents();
          const text = document.createTextNode(event.clipboardData.getData("text/plain").replace(/[\r\n]+/g, " "));
          range.insertNode(text);
          selection.setBaseAndExtent(text, text.length, text, text.length);
          refreshLine(line);
        });
      });
      panel.querySelector("[data-reset]").addEventListener("click", () => {
        if (active === panel) finish("Ejecución detenida.", undefined, true);
        editableLines.forEach((line, index) => { line.innerHTML = initial[index]; });
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
        worker.postMessage({ code: source() });
      });
    });
  };
  if (typeof document$ !== "undefined") document$.subscribe(initialize);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initialize);
  else initialize();
})();
