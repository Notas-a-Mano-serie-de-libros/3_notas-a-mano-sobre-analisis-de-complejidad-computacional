<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# 8.1 Comparación general

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/0_comparacion_ordenamientos.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
</div>

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
    <tr><td>Ordenamiento burbuja</td><td>\(\Omega(n)\)</td><td>\(\Theta(n^2)\)</td><td>\(O(n^2)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/1_ordenamiento_burbuja.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Ordenamiento por selección</td><td>\(\Omega(n^2)\)</td><td>\(\Theta(n^2)\)</td><td>\(O(n^2)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/2_ordenamiento_seleccion.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Ordenamiento por inserción</td><td>\(\Omega(n)\)</td><td>\(\Theta(n^2)\)</td><td>\(O(n^2)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/3_ordenamiento_insercion.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Ordenamiento Shell</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>Depende de la secuencia</td><td>\(O(n^2)\) con la secuencia original</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/4_ordenamiento_shell.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Ordenamiento por mezcla</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>\(\Theta(n \cdot \log_2(n))\)</td><td>\(O(n \cdot \log_2(n))\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/5_ordenamiento_mezcla.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Ordenamiento rápido</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>\(\Theta(n \cdot \log_2(n))\)</td><td>\(O(n^2)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/6_ordenamiento_rapido.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Ordenamiento radix</td><td>\(\Omega(n \cdot d)\)</td><td>\(\Theta(n \cdot d)\)</td><td>\(O(n \cdot d)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/7_ordenamiento_radix.ipynb" title="Abrir animación">🔗</a></td></tr>
  </tbody>
</table>
</div>

<br>

Este resumen presenta los resultados generales. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.

---

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

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../1-ordenamiento-burbuja/">8.2 Ordenamiento burbuja →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
