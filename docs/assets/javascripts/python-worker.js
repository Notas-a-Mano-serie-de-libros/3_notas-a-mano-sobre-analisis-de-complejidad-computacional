import { loadPyodide } from "https://cdn.jsdelivr.net/pyodide/v314.0.6/full/pyodide.mjs";

let ready;
self.onmessage = async ({ data }) => {
  let output = "";
  const capture = (line) => {
    if (output.length < 50000) output += line + "\n";
    else throw new Error("La salida superó el límite de este panel.");
  };
  let globals;
  try {
    ready ??= loadPyodide();
    const pyodide = await ready;
    self.postMessage({ type: "ready" });
    pyodide.setStdout({ batched: capture });
    pyodide.setStderr({ batched: capture });
    globals = pyodide.runPython("dict()");
    await pyodide.runPythonAsync(data.code, { globals });
    self.postMessage({ type: "done", output: output || "Ejecutado sin salida.", error: false });
  } catch (error) {
    self.postMessage({ type: "done", output: output + "\n" + error.message, error: true });
  } finally {
    globals?.destroy();
  }
};
