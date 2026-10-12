import { JupyterFrontEnd, JupyterFrontEndPlugin } from "@jupyterlab/application";
import {
  INotebookTracker,
  NotebookActions,
  NotebookPanel,
} from "@jupyterlab/notebook";

const WIDGET_NOTEBOOK_PATH =
  /(?:^|\/)simulaciones\/capitulo(?:2|4|5|6|7|8)\/notebooks\//;
const EMBEDDED_HEIGHT_MESSAGE = "notas-a-mano:jupyterlite-height";
const installedWidgetKernels = new Set<string>();

function prepareEmbeddedHeight(panel: NotebookPanel): () => void {
  if (window.parent === window) return () => undefined;

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

  const mutationObserver = new MutationObserver(scheduleHeightReport);
  mutationObserver.observe(panel.content.node, {
    attributes: true,
    childList: true,
    subtree: true,
  });
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

  let installationError: string | null = null;
  const future = kernel.requestExecute(
    {
      code: [
        "import piplite",
        "await piplite.install('ipywidgets==8.1.9')",
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
  installedWidgetKernels.add(kernel.id);
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
        await installWidgetPackage(panel);
        if (panel.isDisposed) return;
        await NotebookActions.runAll(panel.content, panel.context.sessionContext);
        scheduleHeightReport();
      })().catch((error: unknown) => {
        console.error("No fue posible ejecutar automáticamente la simulación JupyterLite.", error);
      });
    };

    tracker.widgetAdded.connect((_sender, panel) => runNotebook(panel));
    if (tracker.currentWidget) runNotebook(tracker.currentWidget);
  }
};

export default plugin;
