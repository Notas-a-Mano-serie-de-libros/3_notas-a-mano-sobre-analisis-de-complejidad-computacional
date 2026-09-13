(() => {
  let runtime;
  const load = () => runtime ||= (async () => {
    await cheerpjInit({ version: 8, status: "none" });
    const jar = new URL("../java/ejemplos.jar", location.href);
    return cheerpjRunLibrary("/app" + jar.pathname);
  })();
  window.addEventListener("message", async ({ source, origin, data }) => {
    if (source !== parent || origin !== location.origin || data.type !== "run-java") return;
    const reply = message => parent.postMessage({ ...message, job: data.job }, origin);
    try {
      reply({ type: "java-loading", message: "Cargando la máquina virtual Java…" });
      const lib = await load();
      reply({ type: "java-loading", message: "Cargando los algoritmos Java…" });
      const Runner = await lib.ejemplos.Runner;
      reply({ type: "java-ready" });
      const response = String(await Runner.execute(data.className, data.encoded));
      const separator = response.indexOf("\n");
      reply({ type: "java-done", error: response.startsWith("ERROR\n"), output: response.slice(separator + 1) });
    } catch (error) {
      const message = await error.getMessage?.() || error.message || String(error);
      reply({ type: "java-done", error: true, output: message });
    }
  });
})();
