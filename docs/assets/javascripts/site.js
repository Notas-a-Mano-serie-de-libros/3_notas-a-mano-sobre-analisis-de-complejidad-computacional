function prepareEditorialFigures(root = document) {
  const dialog = document.querySelector(".figure-lightbox");
  if (!dialog) return;

  const expanded = dialog.querySelector("img");
  const caption = dialog.querySelector("p");
  const close = dialog.querySelector(".figure-lightbox__close");

  root.querySelectorAll(".md-content figure:not(.author-qr):not(.author-photo) img").forEach((image) => {
    image.loading = "lazy";
    image.decoding = "async";
    image.tabIndex = 0;
    image.setAttribute("role", "button");
    image.setAttribute("aria-label", `${image.alt || "Figura"}. Ampliar imagen`);

    const open = () => {
      expanded.src = image.currentSrc || image.src;
      expanded.alt = image.alt;
      caption.textContent = image.closest("figure")?.querySelector("figcaption")?.textContent || image.alt;
      dialog.showModal();
    };

    image.addEventListener("click", open);
    image.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        open();
      }
    });
  });

  close.addEventListener("click", () => dialog.close());
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) dialog.close();
  });
}

function prepareReadingProgress(root = document) {
  root.querySelectorAll("[data-reading-progress]").forEach((panel) => {
    if (panel.dataset.initialized) return;
    panel.dataset.initialized = "true";

    const button = panel.querySelector("[data-reading-complete]");
    const buttonLabel = panel.querySelector("[data-reading-complete-label]");
    const summary = panel.querySelector("[data-reading-progress-summary]");
    const storageKey = `notas-a-mano:lectura:${panel.dataset.pageKey}`;

    const readState = () => {
      try {
        return localStorage.getItem(storageKey) === "complete";
      } catch (_error) {
        return panel.dataset.complete === "true";
      }
    };

    const writeState = (complete) => {
      panel.dataset.complete = String(complete);
      try {
        if (complete) localStorage.setItem(storageKey, "complete");
        else localStorage.removeItem(storageKey);
      } catch (_error) {
        // La interfaz conserva el estado durante la visita si el navegador
        // bloquea el almacenamiento local.
      }
    };

    const render = (complete) => {
      button.setAttribute("aria-pressed", String(complete));
      buttonLabel.textContent = complete ? "Leída" : "Marcar como leída";
      summary.textContent = complete ? "Lectura completada en este navegador" : "Progreso guardado en este navegador";
    };

    render(readState());
    button.addEventListener("click", () => {
      const complete = !readState();
      writeState(complete);
      render(complete);
    });
  });
}

function prepareAccessibleTables(root = document) {
  root.querySelectorAll(".md-content table").forEach((table, index) => {
    table.querySelectorAll("thead th").forEach((header) => {
      header.scope = "col";
    });

    if (!table.hasAttribute("aria-label")) {
      const article = table.closest("article, .md-content__inner") || root;
      const headings = Array.from(article.querySelectorAll("h1, h2, h3, h4"));
      const preceding = headings.filter(
        (heading) => heading.compareDocumentPosition(table) & Node.DOCUMENT_POSITION_FOLLOWING,
      );
      const context = preceding.at(-1)?.textContent?.trim();
      table.setAttribute("aria-label", context || `Tabla ${index + 1}`);
    }

    const viewport = table.closest(".md-typeset__scrollwrap");
    if (viewport) {
      viewport.tabIndex = 0;
      viewport.setAttribute("role", "region");
      viewport.setAttribute("aria-label", table.getAttribute("aria-label"));
    }
  });
}

function preparePageEnhancements() {
  prepareEditorialFigures();
  prepareReadingProgress();
  prepareAccessibleTables();
}

if (typeof document$ !== "undefined") {
  document$.subscribe(preparePageEnhancements);
} else {
  document.addEventListener("DOMContentLoaded", preparePageEnhancements);
}
