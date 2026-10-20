import { JupyterFrontEnd, JupyterFrontEndPlugin } from "@jupyterlab/application";
import {
  INotebookTracker,
  NotebookActions,
  NotebookPanel,
} from "@jupyterlab/notebook";

const WIDGET_NOTEBOOK_PATH =
  /(?:^|\/)simulaciones\/capitulo(?:2|4|5|6|7|8)\/notebooks\//;
const SCIENTIFIC_NOTEBOOK_PATH =
  /(?:^|\/)simulaciones\/(?:capitulo(?:2|4|6)\/notebooks\/|capitulo8\/notebooks\/(?:0_comparacion_ordenamientos|ejercicios_propuestos)\.ipynb$)/;
const EMBEDDED_HEIGHT_MESSAGE = "notas-a-mano:jupyterlite-height";
const EMBEDDED_READY_MESSAGE = "notas-a-mano:jupyterlite-ready";
const EMBEDDED_ERROR_MESSAGE = "notas-a-mano:jupyterlite-error";
const EMBEDDED_LAYOUT_STYLE_ID = "notas-a-mano-embedded-layout";
const installedWidgetKernels = new Set<string>();
const keyboardEnhancedTabs = new WeakSet<HTMLElement>();
let accessibleId = 0;

function reportEmbeddedState(type: string, detail = ""): void {
  if (window.parent === window) return;
  window.parent.postMessage({ type, detail }, window.location.origin);
}

function enhanceSimulationAccessibility(root: HTMLElement): void {
  root.querySelectorAll<HTMLElement>('[class*="-subpanel-title"]').forEach((button) => {
    const content = button.nextElementSibling as HTMLElement | null;
    if (!content) return;
    if (!content.id) content.id = `simulation-panel-${++accessibleId}`;
    button.setAttribute("aria-controls", content.id);
    button.setAttribute("aria-expanded", String(content.style.display !== "none"));
  });

  root.querySelectorAll<HTMLElement>('[class*="-tab-panel"]').forEach((panel) => {
    const tabBar = panel.querySelector<HTMLElement>('[class*="-tab-bar"]');
    const contentBox = panel.querySelector<HTMLElement>('[class*="-tab-content"]');
    if (!tabBar || !contentBox) return;
    const tabs = Array.from(tabBar.querySelectorAll<HTMLElement>('[class*="-tab-button"]'));
    const contents = Array.from(contentBox.children) as HTMLElement[];
    tabBar.setAttribute("role", "tablist");
    tabBar.setAttribute("aria-label", "Vistas de la simulación");
    tabs.forEach((tab, index) => {
      const content = contents[index];
      if (!content) return;
      if (!tab.id) tab.id = `simulation-tab-${++accessibleId}`;
      if (!content.id) content.id = `simulation-tabpanel-${++accessibleId}`;
      const active = content.style.display !== "none";
      tab.setAttribute("role", "tab");
      tab.setAttribute("aria-controls", content.id);
      tab.setAttribute("aria-selected", String(active));
      tab.tabIndex = active ? 0 : -1;
      content.setAttribute("role", "tabpanel");
      content.setAttribute("aria-labelledby", tab.id);
      content.hidden = !active;
    });
    if (keyboardEnhancedTabs.has(tabBar)) return;
    keyboardEnhancedTabs.add(tabBar);
    tabBar.addEventListener("keydown", (event) => {
      if (!(event.target instanceof HTMLElement)) return;
      const index = tabs.indexOf(event.target);
      if (index < 0) return;
      let next = index;
      if (event.key === "ArrowRight" || event.key === "ArrowDown") next = (index + 1) % tabs.length;
      else if (event.key === "ArrowLeft" || event.key === "ArrowUp") next = (index - 1 + tabs.length) % tabs.length;
      else if (event.key === "Home") next = 0;
      else if (event.key === "End") next = tabs.length - 1;
      else return;
      event.preventDefault();
      tabs[next].focus();
      tabs[next].click();
    });
  });
}

function prepareEmbeddedHeight(panel: NotebookPanel): () => void {
  if (window.parent === window) return () => undefined;

  if (!document.getElementById(EMBEDDED_LAYOUT_STYLE_ID)) {
    const style = document.createElement("style");
    style.id = EMBEDDED_LAYOUT_STYLE_ID;
    style.textContent = `
      html, body { overflow: hidden !important; }
      .jp-NotebookPanel-notebook .jp-WindowedPanel-outer {
        box-sizing: border-box !important;
        width: 100% !important;
        padding: 0 !important;
        overflow: auto !important;
        scrollbar-width: none !important;
      }
      .jp-NotebookPanel-notebook .jp-WindowedPanel-outer::-webkit-scrollbar {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
      }
      .jp-NotebookPanel-notebook .jp-WindowedPanel-inner,
      .jp-NotebookPanel-notebook .jp-WindowedPanel-viewport {
        box-sizing: border-box !important;
        width: 100% !important;
        max-width: none !important;
      }
      .jp-NotebookPanel-notebook .jp-OutputPrompt { display: none !important; }
      .jp-NotebookPanel-notebook .jp-OutputArea-output {
        width: 100% !important;
        max-width: none !important;
        flex: 1 1 auto !important;
      }
    `;
    document.head.appendChild(style);
  }

  // El espacio para desplazar la última celda hasta la parte superior es útil
  // en el editor completo, pero deja un bloque vacío dentro de un iframe que
  // debe adoptar exactamente la altura de su contenido.
  panel.content.node.classList.remove("jp-mod-scrollPastEnd");

  let animationFrame = 0;
  let lastHeight = 0;

  const reportHeight = (): void => {
    animationFrame = 0;
    if (panel.isDisposed) return;
    panel.content.node.classList.remove("jp-mod-scrollPastEnd");

    const scrollContainer = panel.content.node.querySelector<HTMLElement>(
      ".jp-WindowedPanel-outer",
    );
    if (!scrollContainer) return;
    const scrollContent = panel.content.node.querySelector<HTMLElement>(
      ".jp-WindowedPanel-inner",
    );
    const scrollBounds = scrollContainer.getBoundingClientRect();
    const contentHeight = Array.from(scrollContainer.children).reduce(
      (maximum, child) =>
        Math.max(maximum, child.getBoundingClientRect().bottom - scrollBounds.top),
      scrollContent?.scrollHeight ?? 0,
    );

    const height = Math.ceil(
      Math.max(0, scrollBounds.top) +
        (contentHeight || scrollContainer.scrollHeight),
    );
    if (height <= 0 || Math.abs(height - lastHeight) < 1) return;

    lastHeight = height;
    window.parent.postMessage(
      { type: EMBEDDED_HEIGHT_MESSAGE, height },
      window.location.origin,
    );
  };

  const scheduleHeightReport = (): void => {
    if (animationFrame) window.cancelAnimationFrame(animationFrame);
    animationFrame = window.requestAnimationFrame(reportHeight);
  };

  const resizeObserver = new ResizeObserver(scheduleHeightReport);
  resizeObserver.observe(panel.content.node);
  const scrollContainer = panel.content.node.querySelector<HTMLElement>(
    ".jp-WindowedPanel-outer",
  );
  const scrollContent = panel.content.node.querySelector<HTMLElement>(
    ".jp-WindowedPanel-inner",
  );
  if (scrollContainer) resizeObserver.observe(scrollContainer);
  if (scrollContent) resizeObserver.observe(scrollContent);

  const mutationOptions: MutationObserverInit = {
    attributes: true,
    childList: true,
    subtree: true,
  };
  const mutationObserver = new MutationObserver(() => {
    // La mejora de accesibilidad escribe atributos ARIA en el mismo árbol que
    // observamos. Desconectamos temporalmente el observador para que esas
    // escrituras no vuelvan a disparar este callback en un bucle infinito que
    // terminaría bloqueando el hilo principal del navegador.
    mutationObserver.disconnect();
    enhanceSimulationAccessibility(panel.content.node);
    mutationObserver.observe(panel.content.node, mutationOptions);
    scheduleHeightReport();
  });
  enhanceSimulationAccessibility(panel.content.node);
  mutationObserver.observe(panel.content.node, mutationOptions);
  window.addEventListener("resize", scheduleHeightReport);
  panel.disposed.connect(() => {
    if (animationFrame) window.cancelAnimationFrame(animationFrame);
    resizeObserver.disconnect();
    mutationObserver.disconnect();
    window.removeEventListener("resize", scheduleHeightReport);
  });
  scheduleHeightReport();

  return scheduleHeightReport;
}

async function installWidgetPackage(panel: NotebookPanel): Promise<void> {
  if (!WIDGET_NOTEBOOK_PATH.test(panel.context.path)) return;

  const kernel = panel.context.sessionContext.session?.kernel;
  if (!kernel) {
    throw new Error(`No hay un kernel activo para ${panel.context.path}.`);
  }
  if (installedWidgetKernels.has(kernel.id)) return;
  // Se marca antes de esperar para no duplicar la instalación al reiniciar.
  installedWidgetKernels.add(kernel.id);

  let installationError: string | null = null;
  const future = kernel.requestExecute(
    {
      code: [
        "import piplite",
        SCIENTIFIC_NOTEBOOK_PATH.test(panel.context.path)
          ? "await piplite.install(['ipywidgets==8.1.9', 'matplotlib', 'numpy'])"
          : "await piplite.install('ipywidgets==8.1.9')",
        // Confirm the module is visible in this kernel before the notebook runs.
        "import ipywidgets",
      ].join("\n"),
      stop_on_error: true,
    },
    true,
  );
  future.onIOPub = (message) => {
    if (message.header.msg_type === "error" && "evalue" in message.content) {
      installationError = String(message.content.evalue);
    }
  };
  const reply = await future.done;
  if (installationError || reply.content.status === "error") {
    throw new Error(
      `No fue posible instalar ipywidgets antes de ejecutar ${panel.context.path}: ${
        installationError ?? "el kernel devolvió un error"
      }`,
    );
  }
}

const plugin: JupyterFrontEndPlugin<void> = {
  id: "@notas-a-mano/jupyterlite-auto-run:plugin",
  autoStart: true,
  requires: [INotebookTracker],
  activate: (app: JupyterFrontEnd, tracker: INotebookTracker) => {
    const scheduled = new WeakSet<NotebookPanel>();

    const runNotebook = (panel: NotebookPanel): void => {
      if (scheduled.has(panel)) return;
      scheduled.add(panel);
      const scheduleHeightReport = prepareEmbeddedHeight(panel);

      void (async () => {
        await panel.context.ready;
        await panel.context.sessionContext.ready;
        if (panel.isDisposed) return;
        // Un reinicio crea un kernel nuevo sin ipywidgets: se reinstala antes de
        // cualquier ejecución manual.
        panel.context.sessionContext.statusChanged.connect((_session, status) => {
          if (status !== "idle" && status !== "starting") return;
          installWidgetPackage(panel).catch((error: unknown) => {
            console.error("No fue posible reinstalar ipywidgets tras reiniciar el kernel.", error);
          });
        });
        await installWidgetPackage(panel);
        if (panel.isDisposed) return;
        await NotebookActions.runAll(panel.content, panel.context.sessionContext);
        scheduleHeightReport();
        reportEmbeddedState(EMBEDDED_READY_MESSAGE);
      })().catch((error: unknown) => {
        console.error("No fue posible ejecutar automáticamente la simulación JupyterLite.", error);
        reportEmbeddedState(
          EMBEDDED_ERROR_MESSAGE,
          error instanceof Error ? error.message : String(error),
        );
      });
    };

    tracker.widgetAdded.connect((_sender, panel) => runNotebook(panel));
    if (tracker.currentWidget) runNotebook(tracker.currentWidget);
  }
};

export default plugin;
