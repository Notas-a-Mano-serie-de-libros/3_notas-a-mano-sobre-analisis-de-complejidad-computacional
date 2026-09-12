(() => {
  const workerURL = new URL("python-worker.js", document.currentScript.src);
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
      panel.querySelector("[data-reset]").addEventListener("click", () => {
        if (active === panel) finish("Ejecución detenida.", undefined, true);
        editor.value = initial;
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
