<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>

# 3.3.2 Notación O

<span class="chapter-kicker">Capítulo 3</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/notebooks/1_notacion_big_o.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar notebook en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

La notación \(O\) se utiliza para mostrar que \(C(n)\) crece **al mismo ritmo o más lento** que una función de referencia \(g(n)\). En otras palabras, para valores suficientemente grandes de \(n\), la función \(g(n)\) permite construir una cota superior para \(C(n)\), ignorando constantes multiplicativas y términos de menor orden.

Formalmente, se analiza el cociente entre ambas funciones mediante el límite superior:

\[
k=\limsup_{n\to\infty}\left(\frac{C(n)}{g(n)}\right), \qquad k\in\mathbb{R}_0^+
\]

Si este valor es finito, entonces existe al menos una constante \(c\) que satisface la desigualdad:

\[
C(n)\le c\cdot g(n)
\]

Cuando el cociente converge a una constante positiva \(k\), una elección válida para la constante debe cumplir:

\[
c\gt k
\]

Finalmente, \(n_0\) se obtiene seleccionando un valor del conjunto de posibles umbrales asociados a un valor específico de \(c\):

\[
n_0\in\mathbb{R}^{+}: C(n)\le c\cdot g(n)\qquad \forall n\ge n_0
\]

La simulación permite modificar \(C(n)\), \(g(n)\), el intervalo visible, la constante \(c\) y la escala de la gráfica. También permite arrastrar la línea de \(n_0\) para seleccionar cualquier umbral válido del intervalo solución.

<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-3/comparacion_big_O.png" alt="Ejemplo gráfico de una función perteneciente a O de n cúbica"><figcaption>Una referencia escalada que actúa como cota superior a partir de \(n_0\).</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-3/comparacion_big_O_2.png" alt="Segundo ejemplo gráfico de notación O"><figcaption>La pertenencia a \(O(g(n))\) no exige que ambas funciones crezcan al mismo ritmo.</figcaption></figure>
</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../0-comparacion-notaciones-asintoticas/">← 3.2 Comparación de las notaciones</a><a class="section-step__index" href="../">Capítulo 3</a><a class="section-step__next" href="../2-notacion-little-o/">3.5.2 Notación o →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>
