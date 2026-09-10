<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>

# 5.5.1 Sustitución iterativa

<span class="chapter-kicker">Capítulo 5</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo5/notebooks/1_metodos_solucion_relaciones_recurrencia.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

La sustitución iterativa expande la recurrencia hasta reconocer un patrón. Primero se reemplaza el término recursivo por su definición; después se repite la operación \(k\) veces, se identifica cuándo el argumento alcanza el caso base y se suma el trabajo acumulado.

### Procedimiento

1. Escriba la recurrencia y su condición inicial.
2. Expanda dos o tres niveles sin simplificar prematuramente.
3. Exprese coeficientes, argumento y suma después de \(k\) sustituciones.
4. Resuelva \(k\) a partir del caso base.
5. Sustituya ese valor y simplifique la suma mediante dominancia.

Es apropiado para relaciones de reducción y división con un patrón analítico reconocible. La expansión no es una demostración completa hasta justificar el patrón general y verificar la condición inicial.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../formas-de-recurrencia/">← 5.4 Formas de las relaciones de recurrencia</a><a class="section-step__index" href="../">Capítulo 5</a><a class="section-step__next" href="../arbol-recurrencia/">5.5.2 Árbol de recurrencia →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>
