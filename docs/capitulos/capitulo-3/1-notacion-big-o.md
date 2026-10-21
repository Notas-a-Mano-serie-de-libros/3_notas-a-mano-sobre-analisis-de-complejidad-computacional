<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>

# 3.5.1.1 Notación Big-O

<span class="chapter-kicker">Capítulo 3</span>

La notación \(O\) se utiliza para mostrar que \(C(n)\) crece **al mismo ritmo o más lento** que una función de referencia \(g(n)\). En otras palabras, para valores suficientemente grandes de \(n\), la función \(g(n)\) permite construir una cota superior para \(C(n)\), ignorando constantes multiplicativas y términos de menor orden.

## Definición formal

Para funciones de costo no negativas y una referencia \(g(n)\) positiva a partir de algún tamaño de entrada:

\[
C(n)\in O(g(n))\iff
\exists c>0\;\exists n_0\in\mathbb{R}^{+}\;\forall n\ge n_0:\quad 0\leq C(n)\leq c\cdot g(n)
\]

Donde:

- **\(n\):** Tamaño de entrada, expresado como un número natural no negativo.
- **\(C(n)\):** Función de costo cuyo crecimiento se estudia.
- **\(g(n)\):** Función de referencia con la que se compara el crecimiento.
- **\(c\):** Constante positiva que escala la referencia para formar una cota superior. Basta con encontrar una constante válida.
- **\(n_0\):** Umbral real positivo desde el que la desigualdad se cumple para todos los tamaños posteriores; puede depender de las constantes elegidas.
- **\(\forall n\ge n_0\):** La condición se mantiene para todo tamaño de entrada a partir del umbral, no solo para un valor aislado.

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Simulación interactiva del límite asintótico para notación \(O\) | `jupyter lab simulaciones/capitulo3/notebooks/1_notacion_big_o.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->

<!-- jupyterlite-demo:start -->
## Simulación en el navegador

Este demo se ejecuta con **JupyterLite y Pyodide** dentro del navegador: no abre Colab, no crea una sesión remota y no requiere iniciar sesión. La primera carga descarga el entorno de Python; las siguientes aperturas reutilizan los recursos almacenados por el navegador.

1. Espere a que el indicador del kernel muestre **Python (Pyodide)**.
2. La simulación se ejecuta automáticamente cuando el kernel **Python (Pyodide)** esté listo.
3. Use los controles de la simulación de Big-O que aparecen debajo de la celda.

<div class="jupyterlite-demo">
  <div class="jupyterlite-demo__toolbar">
    <span>Simulación interactiva</span>
  </div>
  <div class="jupyterlite-demo__actions">
    <a class="md-button colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo3/notebooks/1_notacion_big_o.ipynb" target="_blank" rel="noopener noreferrer">Abrir en Colab</a>
    <a class="md-button jupyterlite-button" href="../../../jupyterlite/graficas-cientificas/notebooks/index.html?path=simulaciones%2Fcapitulo3%2Fnotebooks%2F1_notacion_big_o.ipynb&revision=d4a4c56db0e1" target="_blank" rel="noopener noreferrer">Abrir en pantalla completa</a>
  </div>
  <iframe
    class="jupyterlite-demo__frame"
    src="../../../jupyterlite/graficas-cientificas/notebooks/index.html?path=simulaciones%2Fcapitulo3%2Fnotebooks%2F1_notacion_big_o.ipynb&revision=d4a4c56db0e1"
    title="Simulación interactiva de notación Big-O en JupyterLite"
    loading="lazy"
    scrolling="no"
    allow="clipboard-read; clipboard-write"
  ></iframe>

</div>
<!-- jupyterlite-demo:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../0-comparacion-notaciones-asintoticas/">← 3.5 Tipos de notación asintótica</a><a class="section-step__index" href="../">Capítulo 3</a><a class="section-step__next" href="../2-notacion-little-o/">3.5.1.2 Notación little-o →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>
