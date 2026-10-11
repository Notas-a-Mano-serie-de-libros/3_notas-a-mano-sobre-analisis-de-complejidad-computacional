import { JupyterFrontEnd, JupyterFrontEndPlugin } from "@jupyterlab/application";
import {
  INotebookTracker,
  NotebookActions,
  NotebookPanel,
} from "@jupyterlab/notebook";

const WIDGET_NOTEBOOK_PATH =
  /(?:^|\/)simulaciones\/capitulo(?:2|4|5|6|7|8)\/notebooks\//;
const installedWidgetKernels = new Set<string>();

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
      code: "import piplite\nawait piplite.install('ipywidgets==8.1.9')",
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

      void (async () => {
        await panel.context.ready;
        await panel.context.sessionContext.ready;
        if (panel.isDisposed) return;
        await installWidgetPackage(panel);
        if (panel.isDisposed) return;
        await NotebookActions.runAll(panel.content, panel.context.sessionContext);
      })().catch((error: unknown) => {
        console.error("No fue posible ejecutar automáticamente la simulación JupyterLite.", error);
      });
    };

    tracker.widgetAdded.connect((_sender, panel) => runNotebook(panel));
    if (tracker.currentWidget) runNotebook(tracker.currentWidget);
  }
};

export default plugin;
