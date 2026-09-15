(() => {
  const javaURL = new URL("java-runtime.html", document.currentScript.src);
  let javaFrame = null;
  let javaJob = 0;
  const workerURL = new URL("python-worker.js", document.currentScript.src);
  const cWorkerURL = new URL("c-worker.js", document.currentScript.src);
  let cWorker = null;
  let cJob = 0;
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
      else if (editor.java && ["true", "false", "null"].includes(value)) kind = "kc";
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
  let activeLanguage = null;
  let pythonJob = 0;
  let timeout = null;
  const finish = (message, output, terminate = false) => {
    clearTimeout(timeout);
    if (active) {
      active.querySelector("[data-run]").disabled = false;
      active.querySelector("[data-stop]").disabled = true;
      const status = active.querySelector("[data-status]");
      if (message === "Resultado") {
        const label = document.createElement("strong");
        label.textContent = message;
        status.replaceChildren(label);
      } else status.textContent = message;
      if (output !== undefined) active.querySelector("[data-output]").textContent = output;
    }
    active = null;
    activeLanguage = null;
    if (terminate) { worker?.terminate(); worker = null; cWorker?.terminate(); cWorker = null; javaFrame?.remove(); javaFrame = null; javaJob++; }
  };
  window.addEventListener("message", ({ source, origin, data }) => {
    if (origin !== location.origin || source !== javaFrame?.contentWindow || !data || data.job !== javaJob || !active || activeLanguage !== "java") return;
    if (data.type === "java-loading") {
      active.querySelector("[data-status]").textContent = data.message;
    } else if (data.type === "java-ready") {
      active.querySelector("[data-status]").textContent = "Ejecutando Java…";
      clearTimeout(timeout);
      timeout = setTimeout(() => finish("Ejecución detenida: superó 10 segundos. Prueba entradas más pequeñas.", undefined, true), 10000);
    } else if (data.type === "java-done") {
      finish(data.error ? "Resultado" : "Ejecución completada.", data.output);
    }
  });
  const initialize = () => {
    if (active && !active.isConnected) finish("Ejecución detenida al cambiar de página.", undefined, true);
    document.querySelectorAll("[data-example-runner]").forEach((panel) => {
      if (panel.dataset.initialized) return;
      panel.dataset.initialized = "true";
      const simulationAction = panel.closest("article")?.querySelector(".lab-action");
      const simulationLink = simulationAction?.querySelector(".colab-button");
      if (simulationLink) {
        simulationLink.textContent = "Ejecutar simulación en Google Colab";
        simulationLink.classList.add("simulation-open-button");
        panel.querySelector("details").before(simulationLink);
        simulationAction.remove();
      }
      const editableLines = [...panel.querySelectorAll("[data-editable]")];
      const initial = editableLines.map(line => line.innerHTML);
      const language = panel.querySelector("[data-runner-language]");
      const source = () => [...panel.querySelectorAll('[data-language="python"] [data-code-line]')].map(line => line.textContent).join("\n") + "\n";
      const tabs = [...panel.querySelectorAll("[data-language-tab]")];
      const selectTab = (tab) => {
        language.value = tab.dataset.languageTab;
        language.dispatchEvent(new Event("change"));
      };
      tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => selectTab(tab));
        tab.addEventListener("keydown", event => {
          if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
          event.preventDefault();
          const next = event.key === "Home" ? 0 : event.key === "End" ? tabs.length - 1 : (index + (event.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
          tabs[next].focus();
          selectTab(tabs[next]);
        });
      });
      language.addEventListener("change", () => {
        tabs.forEach(tab => { const selected = tab.dataset.languageTab === language.value; tab.setAttribute("aria-selected", String(selected)); tab.tabIndex = selected ? 0 : -1; });
        if (active === panel) finish("Ejecución detenida al cambiar de lenguaje.", undefined, true);
        panel.querySelectorAll("[data-language]").forEach(editor => { editor.hidden = editor.dataset.language !== language.value; });
        panel.querySelectorAll("[data-runtime-credit]").forEach(note => { note.hidden = note.dataset.runtimeCredit !== language.value; });
        panel.querySelector("[data-status]").textContent = "Listo para ejecutar.";
        panel.querySelector("[data-output]").textContent = "El resultado aparecerá aquí.";
      });
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
        repaint({ value, java: line.hasAttribute("data-java-input") || line.hasAttribute("data-c-input") }, line);
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
        activeLanguage = language.value;
        panel.querySelector("[data-run]").disabled = true;
        panel.querySelector("[data-stop]").disabled = false;
        panel.querySelector("[data-status]").textContent = "Preparando " + ({java:"Java", python:"Python", c:"C"}[language.value]) + "… La primera carga puede tardar unos segundos.";
        panel.querySelector("[data-output]").textContent = "";
        if (language.value === "c") {
          const editor = panel.querySelector('[data-language="c"]');
          if (!cWorker) {
            try { cWorker = new Worker(cWorkerURL, {type:"module"}); }
            catch (error) { finish("Resultado", error.message, true); return; }
            const currentWorker = cWorker;
            cWorker.onerror = () => { if (cWorker !== currentWorker || activeLanguage !== "c") return; finish("Resultado", "No se pudo cargar C. Revisa la conexión y vuelve a intentar.", true); };
            cWorker.onmessage = ({data}) => {
              if (!active || activeLanguage !== "c" || !data || data.job !== cJob) return;
              if (data.type === "ready") {
                active.querySelector("[data-status]").textContent = "Ejecutando C…";
                clearTimeout(timeout);
                timeout = setTimeout(() => finish("Ejecución detenida: superó 10 segundos. Prueba entradas más pequeñas.", undefined, true), 10000);
              } else if (data.type === "done") finish(data.error ? "Resultado" : "Ejecución completada.", data.output);
            };
          }
          timeout = setTimeout(() => finish("Resultado", "No se pudo cargar el ejemplo C. Vuelve a intentar.", true), 30000);
          cWorker.postMessage({key:editor.dataset.cKey, args:[...editor.querySelectorAll("[data-c-input]")].map(input => input.textContent), job:++cJob});
          return;
        }
        if (language.value === "java") {
          const editor = panel.querySelector('[data-language="java"]');
          const encoded = [...editor.querySelectorAll("[data-java-input]")].map(line => line.textContent).join("\n");
          const job = ++javaJob;
          const payload = { type: "run-java", job, className: editor.dataset.javaClass, encoded };
          const send = () => javaFrame.contentWindow.postMessage(payload, location.origin);
          if (!javaFrame) {
            javaFrame = document.createElement("iframe");
            javaFrame.className = "java-runtime-frame";
            javaFrame.setAttribute("aria-hidden", "true");
            javaFrame.tabIndex = -1;
            javaFrame.title = "Entorno de ejecución Java";
            javaFrame.src = javaURL.href;
            javaFrame.addEventListener("load", send, { once: true });
            document.body.append(javaFrame);
          } else send();
          timeout = setTimeout(() => finish("La carga de Java tardó demasiado. Vuelve a intentar.", undefined, true), 90000);
          return;
        }
        if (!worker) {
          try { worker = new Worker(workerURL, { type: "module" }); }
          catch (error) { finish("No se pudo iniciar Python.", error.message, true); return; }
          const currentWorker = worker;
          worker.onerror = () => { if (worker !== currentWorker || activeLanguage !== "python") return; finish("No se pudo cargar Python. Revisa la conexión y vuelve a intentar.", undefined, true); };
          worker.onmessage = ({ data }) => {
            if (!active || activeLanguage !== "python" || !data || data.job !== pythonJob) return;
            if (data.type === "ready") {
              active.querySelector("[data-status]").textContent = "Ejecutando…";
              clearTimeout(timeout);
              timeout = setTimeout(() => finish("Ejecución detenida: superó 10 segundos. Prueba entradas más pequeñas.", undefined, true), 10000);
            } else if (data.type === "done") {
              finish(data.error ? "Resultado" : "Ejecución completada.", data.output);
            }
          };
        }
        timeout = setTimeout(() => finish("La carga de Python tardó demasiado. Vuelve a intentar.", undefined, true), 90000);
        worker.postMessage({ code: source(), job: ++pythonJob });
      });
    });
  };
  if (typeof document$ !== "undefined") document$.subscribe(initialize);
  else if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", initialize);
  else initialize();
})();
