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

if (typeof document$ !== "undefined") {
  document$.subscribe(() => prepareEditorialFigures());
} else {
  document.addEventListener("DOMContentLoaded", () => prepareEditorialFigures());
}
