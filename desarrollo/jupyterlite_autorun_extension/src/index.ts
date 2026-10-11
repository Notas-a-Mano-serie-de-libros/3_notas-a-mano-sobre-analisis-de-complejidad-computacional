import { JupyterFrontEnd, JupyterFrontEndPlugin } from "@jupyterlab/application";
import {
  INotebookTracker,
  NotebookActions,
  NotebookPanel,
} from "@jupyterlab/notebook";

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
