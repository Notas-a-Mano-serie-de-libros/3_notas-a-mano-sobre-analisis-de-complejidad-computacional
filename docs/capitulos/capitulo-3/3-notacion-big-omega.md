<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>

# 3.3.4 Notación Ω

<span class="chapter-kicker">Capítulo 3</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/notebooks/3_notacion_big_omega.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar notebook en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

La notación \(\Omega\) se utiliza para mostrar que \(C(n)\) crece **al mismo ritmo o más rápido** que una función de referencia \(g(n)\). En este caso, \(g(n)\) actúa como una cota inferior asintótica para \(C(n)\), ignorando constantes multiplicativas y términos de menor orden.

Formalmente, se analiza el cociente mediante el límite inferior:

\[
k=\liminf_{n\to\infty}\left(\frac{C(n)}{g(n)}\right), \qquad k\in\mathbb{R}^+
\]

Si este valor converge a una constante estrictamente positiva, entonces existe al menos una constante \(c\) que satisface:

\[
C(n)\ge c\cdot g(n)
\]

Cuando el cociente converge a \(k\), una elección válida para la constante debe cumplir:

\[
0\lt c\le k
\]

Finalmente, \(n_0\) se obtiene seleccionando un valor del conjunto de posibles umbrales asociados a un valor específico de \(c\):

\[
n_0\in\mathbb{R}^{+}: C(n)\ge c\cdot g(n)\qquad \forall n\ge n_0
\]

La simulación permite modificar las funciones, el intervalo visible, la constante y la escala. También permite arrastrar la línea de \(n_0\) para seleccionar cualquier umbral válido del intervalo solución.

<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-3/comparacion_big_omega.png" alt="Ejemplo gráfico de una cota inferior asintótica Omega"><figcaption>La referencia escalada queda por debajo de \(C(n)\) después del umbral.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-3/comparacion_big_omega_2.png" alt="Segundo ejemplo gráfico de notación Omega"><figcaption>Una cota inferior no afirma por sí sola que el crecimiento sea ajustado.</figcaption></figure>
</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../2-notacion-little-o/">← 3.5.2 Notación o</a><a class="section-step__index" href="../">Capítulo 3</a><a class="section-step__next" href="../4-notacion-little-omega/">3.5.4 Notación ω →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>
