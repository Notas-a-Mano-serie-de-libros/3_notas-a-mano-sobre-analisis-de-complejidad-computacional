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

const reviewApiBase = "https://notas-a-mano-opiniones.carlos940807.chatgpt.site";
let reviewDataRequest;

function loadReviewData() {
  if (!reviewDataRequest) reviewDataRequest = fetch(`${reviewApiBase}/api/reviews`).then((response) => {
    if (!response.ok) throw new Error("reviews-unavailable");
    return response.json();
  });
  return reviewDataRequest;
}

function prepareGlobalReviewSummary(root = document) {
  const summaries = root.querySelectorAll("[data-global-review-summary]");
  if (!summaries.length) return;
  loadReviewData().then((data) => {
    summaries.forEach((summary) => {
      summary.querySelector("[data-global-review-average]").textContent = data.total ? Number(data.average).toFixed(1).replace(".", ",") : "—";
      summary.querySelector("[data-global-review-total]").textContent = data.total === 1 ? "1 valoración" : `${data.total || 0} valoraciones`;
    });
  }).catch(() => {
    summaries.forEach((summary) => { summary.querySelector("[data-global-review-total]").textContent = "Valoración"; });
  });
}

function prepareReaderFeedback(root = document) {
  root.querySelectorAll("[data-reader-feedback]").forEach(async (panel) => {
    if (panel.dataset.initialized) return;
    panel.dataset.initialized = "true";
    const api = panel.dataset.apiBase;
    const form = panel.querySelector("[data-review-form]");
    const submit = form.querySelector("button[type='submit']");
    const status = panel.querySelector("[data-review-status]");
    const anonymous = form.elements.isAnonymous;
    const name = form.elements.name;
    const reviewList = panel.querySelector("[data-review-list]");
    let turnstileWidget = null;

    reviewList.tabIndex = 0;
    reviewList.setAttribute("role", "region");
    reviewList.setAttribute("aria-label", "Comentarios publicados");

    const syncCommentsHeight = () => {
      panel.style.setProperty("--reader-feedback-form-height", `${Math.ceil(form.getBoundingClientRect().height)}px`);
    };
    const formResizeObserver = new ResizeObserver(syncCommentsHeight);
    formResizeObserver.observe(form);
    syncCommentsHeight();

    const renderReviews = (data) => {
      panel.querySelector("[data-review-average]").textContent = data.total ? Number(data.average).toFixed(1).replace(".", ",") : "—";
      panel.querySelector("[data-review-total]").textContent = data.total === 1 ? "1 valoración publicada" : `${data.total || 0} valoraciones publicadas`;
      panel.querySelector("[data-comments-count]").textContent = data.items?.length ? `${data.items.length} recientes` : "";
      const list = panel.querySelector("[data-review-list]");
      list.replaceChildren();
      if (!data.items?.length) {
        const empty = document.createElement("p"); empty.className = "reader-feedback__empty"; empty.textContent = "Todavía no hay comentarios publicados."; list.append(empty); return;
      }
      data.items.forEach((item) => {
        const article = document.createElement("article"); article.className = "reader-feedback__comment";
        const header = document.createElement("div");
        const author = document.createElement("strong"); author.textContent = item.name || "Anónimo";
        const stars = document.createElement("span"); stars.className = "reader-feedback__comment-stars"; stars.setAttribute("aria-label", `${item.rating} de 5 estrellas`); stars.textContent = `${"★".repeat(item.rating)}${"☆".repeat(5 - item.rating)}`;
        const comment = document.createElement("p"); comment.textContent = item.comment;
        const date = document.createElement("time"); date.dateTime = item.createdAt; date.textContent = new Intl.DateTimeFormat("es-CO", { dateStyle: "medium" }).format(new Date(item.createdAt));
        header.append(author, stars); article.append(header, comment, date); list.append(article);
      });
    };

    const loadReviews = async () => {
      try { renderReviews(await loadReviewData()); } catch (_error) { panel.querySelector("[data-review-list]").innerHTML = '<p class="reader-feedback__empty">Los comentarios no están disponibles temporalmente.</p>'; }
    };

    anonymous.addEventListener("change", () => { name.disabled = anonymous.checked; name.required = !anonymous.checked; if (anonymous.checked) name.value = ""; });
    await loadReviews();
    try {
      const configResponse = await fetch(`${api}/api/config`);
      const config = await configResponse.json();
      if (!configResponse.ok || !config.acceptingReviews || !config.turnstileSiteKey) throw new Error("unavailable");
      await new Promise((resolve, reject) => {
        if (window.turnstile) return resolve();
        const script = document.createElement("script"); script.src = "https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit"; script.async = true; script.defer = true; script.onload = resolve; script.onerror = reject; document.head.append(script);
      });
      turnstileWidget = window.turnstile.render(panel.querySelector("[data-turnstile]"), { sitekey: config.turnstileSiteKey, action: "book_review", theme: "auto" });
      submit.disabled = false; status.textContent = "Tu comentario no se publicará hasta que sea revisado.";
    } catch (_error) { status.textContent = "La recepción de comentarios estará disponible próximamente."; }

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (!form.reportValidity() || submit.disabled || turnstileWidget === null) return;
      const token = window.turnstile.getResponse(turnstileWidget);
      if (!token) { status.textContent = "Completa la verificación antes de enviar."; return; }
      const values = new FormData(form); submit.disabled = true; status.textContent = "Enviando para revisión…";
      try {
        const response = await fetch(`${api}/api/reviews`, { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ rating: Number(values.get("rating")), comment: values.get("comment"), name: values.get("name"), isAnonymous: values.get("isAnonymous") === "on", website: values.get("website"), turnstileToken: token }) });
        const data = await response.json(); status.textContent = data.message || "No fue posible procesar la solicitud.";
        if (response.ok) form.reset();
      } catch (_error) { status.textContent = "No fue posible enviar el comentario. Intenta nuevamente."; }
      window.turnstile.reset(turnstileWidget); submit.disabled = false;
    });
  });
}

function preparePageEnhancements() {
  prepareEditorialFigures();
  prepareReadingProgress();
  prepareAccessibleTables();
  prepareGlobalReviewSummary();
  prepareReaderFeedback();
}

if (typeof document$ !== "undefined") {
  document$.subscribe(preparePageEnhancements);
} else {
  document.addEventListener("DOMContentLoaded", preparePageEnhancements);
}
