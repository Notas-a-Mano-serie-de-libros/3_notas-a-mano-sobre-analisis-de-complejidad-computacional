window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"]],
    displayMath: [["\\[", "\\]"]],
    processEscapes: true,
    processEnvironments: true,
  },
  options: {
    // Procesa también fórmulas incluidas en tablas HTML. MathJax omite por
    // defecto los elementos code, pre, script, style, textarea y similares.
    ignoreHtmlClass: "tex2jax_ignore",
    processHtmlClass: "tex2jax_process|arithmatex",
  },
};

document$.subscribe(() => {
  document.querySelectorAll('a[href^="https://colab.research.google.com/"]').forEach((link) => {
    link.target = "_blank";
    link.rel = "noopener noreferrer";
  });
  MathJax.typesetPromise();
});
