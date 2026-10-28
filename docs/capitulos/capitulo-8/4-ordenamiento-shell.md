<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# Ampliación · Ordenamiento Shell

<span class="chapter-kicker">Capítulo 8</span>

<!-- algorithm-learning-guide:start -->
<section class="algorithm-learning-guide" aria-labelledby="guia-4-ordenamiento-shell">
  <h2 id="guia-4-ordenamiento-shell">Guía de aprendizaje</h2>
  <dl>
    <dt>Objetivo</dt><dd>Explicar cómo los saltos reducen desplazamientos antes de la inserción final.</dd>
    <dt>Prerrequisitos</dt><dd>Ordenamiento por inserción y secuencias decrecientes de saltos.</dd>
    <dt>Invariante que debe observar</dt><dd>Después de procesar un salto h, cada subsecuencia separada por h queda ordenada.</dd>
    <dt>Cuándo usarlo</dt><dd>Úselo como alternativa in situ para tamaños medianos cuando una implementación sencilla sea prioritaria.</dd>
    <dt>Cuándo evitarlo</dt><dd>Evítelo cuando se necesiten estabilidad o garantías asintóticas independientes de la secuencia de saltos.</dd>
    <dt>Propiedades</dt><dd>Es in situ, no estable y su complejidad depende de la secuencia de saltos.</dd>
    <dt>Error frecuente</dt><dd>Asignar una única complejidad a Shell sin indicar qué secuencia de saltos se analiza.</dd>
  </dl>
  <h3>Compruebe su comprensión</h3>
  <ol><li>¿Qué significa que el arreglo esté h-ordenado?</li><li>¿Por qué la última pasada usa h = 1?</li></ol>
</section>
<!-- algorithm-learning-guide:end -->

El ordenamiento Shell generaliza la idea del ordenamiento por inserción. En lugar de comparar solo elementos contiguos, primero compara elementos separados por un valor h determinado. Después reduce progresivamente ese valor h hasta llegar a 1, momento en el que realiza una pasada equivalente a inserción sobre un arreglo que ya quedó parcialmente organizado.

La ventaja práctica aparece porque los elementos pueden desplazarse grandes distancias durante las primeras pasadas. Cuando h se vuelve pequeño, el arreglo suele estar mucho más cerca de su posición final y las pasadas restantes requieren menos movimientos.

<!-- book-code:start -->

El libro no incluye un listado de implementación para este tema.

<!-- book-code:end -->

## Análisis de complejidad

### Resumen general

Shell ordena mediante inserciones entre elementos separados por saltos decrecientes. El tiempo depende de la secuencia de saltos y del orden de los datos; el espacio auxiliar permanece constante.

### Versión iterativa

La tabla corresponde a la secuencia original de Shell: \(\lfloor n/2\rfloor\), \(\lfloor n/4\rfloor\), hasta \(1\). Otras secuencias pueden modificar las cotas temporales.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Theta(n\cdot\log_2(n))\) | \(\Theta(1)\) | El arreglo ya está ordenado y cada pasada verifica los elementos sin desplazarlos. |
| Caso promedio | Depende de la distribución de los datos | \(\Theta(1)\) | Las pasadas realizan distintos números de desplazamientos según el orden inicial; no se presupone una única cota ajustada. |
| Peor caso | \(O(n^2)\) | \(O(1)\) | Un orden desfavorable requiere numerosos desplazamientos con la secuencia original de saltos. |

## Comparación de secuencias de h

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y abra la carpeta de notebooks del capítulo con Jupyter Lab:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir el laboratorio del capítulo 8 | `jupyter lab simulaciones/capitulo8/notebooks/` |

Jupyter Lab abrirá la carpeta; elija una simulación y ejecute todas sus celdas.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->

<!-- jupyterlite-demo:start -->
## Simulación en el navegador

Ejecuta este laboratorio interactivo integrado con **JupyterLite y Pyodide**. También puedes abrir el notebook en Google Colab o en una instancia local de Jupyter.

1. Espera a que el kernel indique **Python (Pyodide)**.
2. La simulación se ejecuta automáticamente cuando el kernel **Python (Pyodide)** esté listo.
3. Interactúa con los controles de **Ordenamiento Shell**.

<div class="jupyterlite-demo">
  <div class="jupyterlite-demo__toolbar">
    <span>Simulación interactiva</span>
  </div>
  <div class="jupyterlite-demo__actions">
    <a class="md-button colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/4_ordenamiento_shell.ipynb" target="_blank" rel="noopener noreferrer">Abrir en Colab</a>
    <a class="md-button jupyterlite-button" href="../../../jupyterlite/graficas/notebooks/index.html?path=simulaciones%2Fcapitulo8%2Fnotebooks%2F4_ordenamiento_shell.ipynb&revision=2c97aaea5a5f" target="_blank" rel="noopener noreferrer">Abrir en pantalla completa</a>
  </div>
  <iframe
    class="jupyterlite-demo__frame"
    src="../../../jupyterlite/graficas/notebooks/index.html?path=simulaciones%2Fcapitulo8%2Fnotebooks%2F4_ordenamiento_shell.ipynb&revision=2c97aaea5a5f"
    title="Simulación interactiva de Ordenamiento Shell en JupyterLite"
    loading="lazy"
    scrolling="no"
    allow="clipboard-read; clipboard-write"
  ></iframe>

</div>
<!-- jupyterlite-demo:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../3-ordenamiento-insercion/">← 8.4 Ordenamiento por inserción</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../5-ordenamiento-mezcla/">8.5 Ordenamiento por mezcla →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
