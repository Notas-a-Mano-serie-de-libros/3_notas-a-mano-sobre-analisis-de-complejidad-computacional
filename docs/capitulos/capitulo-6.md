<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-7/">Capítulo 7 →</a></nav>

# Capítulo 6 · Análisis de algoritmos recursivos

<span class="chapter-kicker">Páginas 223–258</span>

## 6.1 Procedimiento de análisis de algoritmos recursivos

Toda función recursiva necesita un caso base y una transformación que acerque cada llamada a ese caso. El seguimiento distingue tres momentos: apilamiento de llamadas, resolución del caso base y retorno de resultados. El tiempo cuenta todo el trabajo ejecutado; el espacio cuenta la máxima cantidad de marcos activos simultáneamente, no el total histórico de llamadas.

### Procedimiento para calcular el tiempo

1. Identifique el caso base y su costo.
2. Cuente las llamadas de un caso no base y el tamaño recibido por cada una.
3. Calcule el trabajo local realizado fuera de las llamadas.
4. Escriba \(T(n)\), resuélvala con un método compatible y compruebe el resultado.

### Procedimiento para calcular el espacio

1. Determine la memoria local de un marco de llamada.
2. Calcule la profundidad máxima de llamadas activas, no la cantidad total de nodos del árbol.
3. Añada estructuras auxiliares que sobrevivan mientras se resuelven los subproblemas.
4. Exprese la altura en función de \(n\) y simplifique \(S(n)\).

Las secciones siguientes aplican el procedimiento a factorial, Fibonacci, potencia, Merge Sort y búsqueda en árbol binario, siempre en el orden de código y análisis.

### Simulación interactiva del procedimiento

Utiliza este laboratorio para aplicar el procedimiento anterior antes de estudiar los ejemplos resueltos. Permite seleccionar factorial, Fibonacci, potencia rápida, Merge Sort o búsqueda en árbol binario y observar el caso base, las llamadas, el trabajo local, la recurrencia temporal y la profundidad de la pila.

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Laboratorio de análisis recursivo | `jupyter lab simulaciones/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->

<!-- jupyterlite-demo:start -->
Ejecuta el laboratorio integrado con **JupyterLite y Pyodide**. También puedes abrirlo en Google Colab o en una instancia local de Jupyter.

1. Espera a que el kernel indique **Python (Pyodide)**.
2. La simulación se ejecuta automáticamente cuando el kernel esté listo.
3. Selecciona un algoritmo y contrasta la animación con los pasos del procedimiento.

<div class="jupyterlite-demo">
  <div class="jupyterlite-demo__toolbar">
    <span>Simulación interactiva</span>
  </div>
  <div class="jupyterlite-demo__actions">
    <a class="md-button colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb" target="_blank" rel="noopener noreferrer">Abrir en Colab</a>
    <a class="md-button jupyterlite-button" href="../../jupyterlite/graficas/notebooks/index.html?path=simulaciones%2Fcapitulo6%2Fnotebooks%2F0_laboratorio_analisis_recursivo.ipynb&revision=b7c80d3ac081" target="_blank" rel="noopener noreferrer">Abrir en pantalla completa</a>
  </div>
  <iframe
    class="jupyterlite-demo__frame"
    src="../../jupyterlite/graficas/notebooks/index.html?path=simulaciones%2Fcapitulo6%2Fnotebooks%2F0_laboratorio_analisis_recursivo.ipynb&revision=b7c80d3ac081"
    title="Simulación interactiva del procedimiento de análisis recursivo en JupyterLite"
    loading="lazy"
    scrolling="no"
    allow="clipboard-read; clipboard-write"
  ></iframe>
</div>
<!-- jupyterlite-demo:end -->

<section class="chapter-sections" aria-labelledby="chapter-sections-title">
<h2 id="chapter-sections-title">Ejemplos</h2>
<ul class="chapter-section-list">
<li><a href="factorial/"><strong>Factorial de un número natural</strong></a></li>
<li><a href="fibonacci/"><strong>Sucesión de Fibonacci</strong></a></li>
<li><a href="potencia/"><strong>Potencia de un número entero positivo</strong></a></li>
<li><a href="merge-sort/"><strong>Ordenamiento por mezcla</strong></a></li>
<li><a href="arbol-binario/"><strong>Búsqueda en un árbol binario balanceado</strong></a></li>
</ul>
</section>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-7/">Capítulo 7 →</a></nav>
