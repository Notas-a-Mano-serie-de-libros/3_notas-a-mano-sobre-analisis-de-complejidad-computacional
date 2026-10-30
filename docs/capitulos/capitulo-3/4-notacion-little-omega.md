<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>

# 3.5.2.2 Notación little-ω

<span class="chapter-kicker">Capítulo 3</span>

La notación \(\omega\) se utiliza para mostrar que \(C(n)\) crece **estrictamente más rápido** que una función de referencia \(g(n)\). Es la contraparte estricta de la notación \(\Omega\): no basta con que \(C(n)\) esté por encima de algún múltiplo de \(g(n)\), sino que el cociente debe crecer sin límite.

## Definición formal

Para funciones de costo no negativas y una referencia \(g(n)\) positiva a partir de algún tamaño de entrada:

\[
C(n)\in \omega(g(n))\iff
\forall c>0\;\exists n_0\in\mathbb{R}^{+}\;\forall n\ge n_0:\quad 0\leq c\cdot g(n)<C(n)
\]

Donde:

- **\(n\):** Tamaño de entrada, expresado como un número natural no negativo.
- **\(C(n)\):** Función de costo cuyo crecimiento se estudia.
- **\(g(n)\):** Función de referencia con la que se compara el crecimiento.
- **\(c\):** Constante positiva que escala la referencia para formar una cota inferior estricta. La desigualdad debe poder cumplirse para cualquier constante positiva.
- **\(n_0\):** Umbral real positivo desde el que la desigualdad se cumple para todos los tamaños posteriores; puede depender de las constantes elegidas.
- **\(\forall n\ge n_0\):** La condición se mantiene para todo tamaño de entrada a partir del umbral, no solo para un valor aislado.

La condición equivale a que el cociente cumpla:

\[
\lim_{n\to\infty}\frac{C(n)}{g(n)}=+\infty
\]

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Simulación interactiva del límite asintótico para notación \(\omega\) | `jupyter lab simulaciones/capitulo3/notebooks/4_notacion_little_omega.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->

<!-- jupyterlite-demo:start -->
## Simulación en el navegador

Este demo se ejecuta con **JupyterLite y Pyodide** dentro del navegador: no abre Colab, no crea una sesión remota y no requiere iniciar sesión. La primera carga descarga el entorno de Python; las siguientes aperturas reutilizan los recursos almacenados por el navegador.

1. Espere a que el indicador del kernel muestre **Python (Pyodide)**.
2. La simulación se ejecuta automáticamente cuando el kernel **Python (Pyodide)** esté listo.
3. Use los controles de la simulación de little-ω que aparecen debajo de la celda.

<div class="jupyterlite-demo">
  <div class="jupyterlite-demo__toolbar">
    <span>Simulación interactiva</span>
  </div>
  <div class="jupyterlite-demo__actions">
    <a class="md-button colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo3/notebooks/4_notacion_little_omega.ipynb" target="_blank" rel="noopener noreferrer">Abrir en Colab</a>
    <a class="md-button jupyterlite-button" href="../../../jupyterlite/graficas-cientificas/notebooks/index.html?path=simulaciones%2Fcapitulo3%2Fnotebooks%2F4_notacion_little_omega.ipynb&revision=3b8d7e8e929f" target="_blank" rel="noopener noreferrer">Abrir en pantalla completa</a>
  </div>
  <iframe
    class="jupyterlite-demo__frame"
    src="../../../jupyterlite/graficas-cientificas/notebooks/index.html?path=simulaciones%2Fcapitulo3%2Fnotebooks%2F4_notacion_little_omega.ipynb&revision=3b8d7e8e929f"
    title="Simulación interactiva de notación little-ω en JupyterLite"
    loading="lazy"
    scrolling="no"
    allow="clipboard-read; clipboard-write"
  ></iframe>

</div>
<!-- jupyterlite-demo:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../3-notacion-big-omega/">← 3.5.2.1 Notación Big-Ω</a><a class="section-step__index" href="../">Capítulo 3</a><a class="section-step__next" href="../5-notacion-theta/">3.5.3 Notación Θ →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>
