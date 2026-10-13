<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-8/">Capítulo 8 →</a></nav>

# Capítulo 7 · Análisis de algoritmos de búsqueda clásicos

<span class="chapter-kicker">Páginas 259–316</span>

## Cómo leer este capítulo

Los algoritmos de búsqueda se comparan a partir de sus precondiciones, la forma en que descartan candidatos, sus casos mejor, promedio y peor, y la memoria adicional que requieren. Cada sección desarrolla el procedimiento y su análisis y cada sección desarrolla el procedimiento y su análisis.

## 7.1 Comparación general

<span class="chapter-kicker">Capítulo 7</span>

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
    <tr><td>Búsqueda binaria</td><td>\(\Omega(1)\)</td><td>\(\Theta(\log_2(n))\)</td><td>\(O(\log_2(n))\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/2_busqueda_binaria.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda ternaria</td><td>\(\Omega(1)\)</td><td>\(\Theta(\log_2(n))\)</td><td>\(O(\log_2(n))\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/6_busqueda_ternaria.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda exponencial</td><td>\(\Omega(1)\)</td><td>\(\Theta(\log_2(n))\)</td><td>\(O(\log_2(n))\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/5_busqueda_exponencial.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda por interpolación</td><td>\(\Omega(1)\)</td><td>\(\Theta(\log_2(\log_2(n)))\)</td><td>\(O(n)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/3_busqueda_interpolacion.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda por saltos</td><td>\(\Omega(1)\)</td><td>\(\Theta(\sqrt n)\)</td><td>\(O(\sqrt n)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/4_busqueda_saltos.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda secuencial</td><td>\(\Omega(1)\)</td><td>\(\Theta(n)\)</td><td>\(O(n)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/1_busqueda_secuencial.ipynb" title="Abrir animación">🔗</a></td></tr>
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
| Abrir el laboratorio del capítulo 7 | `jupyter lab simulaciones/capitulo7/notebooks/` |

Jupyter Lab abrirá la carpeta; elija una simulación y ejecute todas sus celdas.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->

<!-- jupyterlite-demo:start -->
### Simulación en el navegador

Ejecuta este laboratorio interactivo integrado con **JupyterLite y Pyodide**. También puedes abrir el notebook en Google Colab o en una instancia local de Jupyter.

1. Espera a que el kernel indique **Python (Pyodide)**.
2. La simulación se ejecuta automáticamente cuando el kernel **Python (Pyodide)** esté listo.
3. Interactúa con los controles de **Comparación de algoritmos de búsqueda**.

<div class="jupyterlite-demo">
  <div class="jupyterlite-demo__toolbar">
    <span>Simulación interactiva</span>
  </div>
  <div class="jupyterlite-demo__actions">
    <a class="md-button colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/0_comparacion_busquedas.ipynb" target="_blank" rel="noopener noreferrer">Abrir en Colab</a>
    <a class="md-button jupyterlite-button" href="../../jupyterlite/analisis-completo/notebooks/index.html?path=simulaciones%2Fcapitulo7%2Fnotebooks%2F0_comparacion_busquedas.ipynb" target="_blank" rel="noopener noreferrer">Abrir en pantalla completa</a>
  </div>
  <iframe
    class="jupyterlite-demo__frame"
    src="../../jupyterlite/analisis-completo/notebooks/index.html?path=simulaciones%2Fcapitulo7%2Fnotebooks%2F0_comparacion_busquedas.ipynb"
    title="Simulación interactiva de Comparación de algoritmos de búsqueda en JupyterLite"
    loading="lazy"
    allow="clipboard-read; clipboard-write"
  ></iframe>

</div>
<!-- jupyterlite-demo:end -->

<section class="chapter-sections" aria-labelledby="chapter-sections-title">
<h2 id="chapter-sections-title">Secciones del capítulo</h2>
<ul class="chapter-section-list">
<li><a href="0-comparacion-busquedas/"><strong>Comparación general</strong></a></li>
<li><a href="1-busqueda-secuencial/"><strong>Búsqueda secuencial</strong></a></li>
<li><a href="2-busqueda-binaria/"><strong>Búsqueda binaria</strong></a></li>
<li><a href="3-busqueda-interpolacion/"><strong>Búsqueda por interpolación</strong></a></li>
<li><a href="4-busqueda-saltos/"><strong>Búsqueda por saltos</strong></a></li>
<li><a href="5-busqueda-exponencial/"><strong>Búsqueda exponencial</strong></a></li>
<li><a href="6-busqueda-ternaria/"><strong>Búsqueda ternaria</strong></a></li>
<li><a href="ejercicios-propuestos/"><strong>Ejercicios propuestos</strong></a></li>
</ul>
</section>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-8/">Capítulo 8 →</a></nav>
