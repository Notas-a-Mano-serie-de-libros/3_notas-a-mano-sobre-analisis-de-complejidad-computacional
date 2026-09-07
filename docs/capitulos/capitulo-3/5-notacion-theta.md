<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>

# 3.3.6 Notación Θ

<span class="chapter-kicker">Capítulo 3</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/notebooks/5_notacion_theta.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar notebook en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

La notación \(\Theta\) define la familia de funciones que están acotadas simultáneamente por abajo y por arriba mediante múltiplos constantes de una misma función de referencia. Su propósito es establecer una **cota ajustada** sobre el crecimiento de \(C(n)\), ignorando constantes y términos de menor orden.

Formalmente, una función \(C(n)\) pertenece a \(\Theta(g(n))\) si existen constantes positivas \(c_1\) y \(c_2\) tales que:

\[
c_1\cdot g(n)\le C(n)\le c_2\cdot g(n), \qquad \forall n\ge n_0
\]

Esta definición combina simultáneamente las ideas de cota inferior y cota superior:

\[
C(n)\in\Theta(g(n))\Longleftrightarrow C(n)\in\Omega(g(n))\land C(n)\in O(g(n))
\]

Si el cociente entre \(C(n)\) y \(g(n)\) converge a una constante positiva \(k\), entonces las constantes deben elegirse de forma que \(C(n)\) quede atrapada entre ambas cotas:

\[
0\lt c_1\le k\le c_2
\]

El valor de \(n_0\) se obtiene al seleccionar un elemento de la intersección de los intervalos que satisfacen ambas desigualdades:

\[
n_0\in\mathbb{R}^{+}: c_1\cdot g(n)\le C(n)\le c_2\cdot g(n)\qquad \forall n\ge n_0
\]

La simulación permite modificar \(C(n)\), \(g(n)\), \(c_1\), \(c_2\), el intervalo visible y la escala. También permite arrastrar la línea de \(n_0\) para seleccionar cualquier umbral válido de la intersección calculada.

<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-3/comparacion_big_theta.png" alt="Ejemplo gráfico de una cota ajustada Theta"><figcaption>Dos múltiplos de \(g(n)\) encierran a \(C(n)\) desde \(n_0\).</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-3/comparacion_big_theta_2.png" alt="Segundo ejemplo gráfico de notación Theta"><figcaption>La cota ajustada combina una cota superior y una inferior del mismo orden.</figcaption></figure>
</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../4-notacion-little-omega/">← 3.5.4 Notación ω</a><a class="section-step__index" href="../">Capítulo 3</a><a class="section-step__next" href="../ejemplos-concretos-notaciones/">3.6 Ejemplos concretos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>
