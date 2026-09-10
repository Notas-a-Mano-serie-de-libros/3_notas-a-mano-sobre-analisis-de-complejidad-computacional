<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# 8.1 Comparación general

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/0_comparacion_ordenamientos.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

Esta sección muestra una animación general para comparar algoritmos de ordenamiento sobre el mismo arreglo, usando únicamente la vista de barras. La intención es observar, en una sola vista, cómo evoluciona cada algoritmo y cuántos pasos necesita para ordenar los mismos datos.

### Algoritmos incluidos

<div style="text-align: center;">
<table style="margin: 0 auto; text-align: center;">
  <thead>
    <tr>
      <th>Algoritmo</th>
      <th>Mejor caso</th>
      <th>Caso promedio</th>
      <th>Peor caso</th>
      <th>Animación</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Ordenamiento burbuja</td><td>\(\Omega(n)\)</td><td>\(\Theta(n^2)\)</td><td>\(O(n^2)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/1_ordenamiento_burbuja.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Ordenamiento por selección</td><td>\(\Omega(n^2)\)</td><td>\(\Theta(n^2)\)</td><td>\(O(n^2)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/2_ordenamiento_seleccion.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Ordenamiento por inserción</td><td>\(\Omega(n)\)</td><td>\(\Theta(n^2)\)</td><td>\(O(n^2)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/3_ordenamiento_insercion.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Ordenamiento Shell</td><td>\(\Omega(n \log_2(n))\)</td><td>Depende de la secuencia</td><td>\(O(n^2)\) con la secuencia original</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/4_ordenamiento_shell.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Ordenamiento por mezcla</td><td>\(\Omega(n \log_2(n))\)</td><td>\(\Theta(n \log_2(n))\)</td><td>\(O(n \log_2(n))\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/5_ordenamiento_mezcla.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Ordenamiento rápido</td><td>\(\Omega(n \log_2(n))\)</td><td>\(\Theta(n \log_2(n))\)</td><td>\(O(n^2)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/6_ordenamiento_rapido.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Ordenamiento radix</td><td>\(\Omega(nd)\)</td><td>\(\Theta(nd)\)</td><td>\(O(nd)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/7_ordenamiento_radix.ipynb" title="Abrir animación">🔗</a></td></tr>
  </tbody>
</table>
</div>

<br>

Este resumen presenta los resultados generales. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.


---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo.
3. Seleccione el orden: ascendente o descendente.
4. Seleccione la secuencia de saltos que usará Shell.
5. Active los algoritmos que se desean visualizar en `Algoritmos activos`.
6. Use el botón `Ordenar` para ejecutar los algoritmos seleccionados sobre el mismo arreglo.
7. Revise la columna `Pasos` para comparar la cantidad de acciones realizadas por cada algoritmo.

### Recomendación de ejecución local

Google Colab permite abrir y ejecutar la simulación rápidamente desde el navegador, aunque tiene límites de sesión, rendimiento, persistencia de archivos, estabilidad de widgets interactivos y tiempo disponible de ejecución. Para trabajar con mayor estabilidad, modificar el código, guardar resultados o repetir experimentos largos, se recomienda descargar el proyecto y ejecutarlo en local desde el repositorio.

### Eficiencia por tamaño de arreglo

La siguiente celda simula cada algoritmo sobre arreglos aleatorios de tamaño creciente y mide el **número de operaciones** que cada uno necesita para completar la ordenación. El análisis se enfoca exclusivamente en el conteo de operaciones del algoritmo, no en tiempos de ejecución reales.

- **Línea sólida** — simulación empírica (n ≤ 100, 5 ensayos por tamaño)
- **Línea punteada** — extrapolación analítica hasta n = 100 000
- **Checkbox** — superpone las funciones teóricas normalizadas para comparar la forma de cada curva con los datos experimentales
- **Algoritmos activos** — permite mostrar u ocultar algoritmos individuales para facilitar la comparación

El gráfico usa escala logarítmica en ambos ejes. La brecha entre O(n log(n)) y O(n²) se vuelve crítica a partir de unos pocos miles de elementos.

> **Tiempo de ejecución:** la celda puede demorar algunos minutos porque los algoritmos O(n²) como burbuja y selección requieren un número de operaciones que crece cuadráticamente con el tamaño del arreglo. En Colab el tiempo es mayor debido a las limitaciones del entorno. Para obtener resultados más rápidos y una ejecución más estable, se recomienda correr esta celda en local.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../1-ordenamiento-burbuja/">8.2 Ordenamiento burbuja →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
