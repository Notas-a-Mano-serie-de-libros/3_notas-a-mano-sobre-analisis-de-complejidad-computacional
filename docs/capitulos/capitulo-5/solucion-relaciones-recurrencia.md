<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>

# 5.5 Solución de relaciones de recurrencia

<span class="chapter-kicker">Capítulo 5</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo5/notebooks/1_metodos_solucion_relaciones_recurrencia.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
</div>

Resolver una relación de recurrencia consiste en obtener una expresión para su función de costo a partir de la ecuación y de sus condiciones iniciales. No todas las relaciones tienen la misma forma; por ello, el libro presenta métodos con condiciones de aplicación diferentes.

### 5.5.1 Consideración previa

Antes de elegir un método, identifique el tipo de reducción, la cantidad de términos recursivos, el trabajo externo y las condiciones iniciales. Esta clasificación permite escoger un procedimiento compatible y comprobar después la solución obtenida.

<ul class="section-index-list">
<li><a href="../sustitucion-iterativa/"><strong>5.5.2 Sustitución iterativa</strong></a></li>
<li><a href="../arbol-recurrencia/"><strong>5.5.3 Árbol de recurrencia</strong></a></li>
<li><a href="../teorema-maestro/"><strong>5.5.4 Teorema maestro</strong></a></li>
<li><a href="../ecuacion-caracteristica/"><strong>5.5.5 Ecuación característica</strong></a></li>
</ul>

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Métodos para analizar relaciones de recurrencia | `jupyter lab simulaciones/capitulo5/notebooks/1_metodos_solucion_relaciones_recurrencia.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../formas-de-recurrencia/">← 5.4 Recurrencias y análisis de complejidad</a><a class="section-step__index" href="../">Capítulo 5</a><a class="section-step__next" href="../sustitucion-iterativa/">5.5.2 Sustitución iterativa →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>
