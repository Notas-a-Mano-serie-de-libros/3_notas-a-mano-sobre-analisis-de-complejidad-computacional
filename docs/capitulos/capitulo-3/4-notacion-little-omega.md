<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>

# 3.3.5 Notación ω

<span class="chapter-kicker">Capítulo 3</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/notebooks/4_notacion_little_omega.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

La notación \(\omega\) se utiliza para mostrar que \(C(n)\) crece **estrictamente más rápido** que una función de referencia \(g(n)\). Es la contraparte estricta de la notación \(\Omega\): no basta con que \(C(n)\) esté por encima de algún múltiplo de \(g(n)\), sino que el cociente debe crecer sin límite.

Formalmente, se exige que el cociente diverja hacia infinito:

\[
\lim_{n\to\infty}\left(\frac{C(n)}{g(n)}\right)=\infty
\]

Esto significa que, para cualquier constante positiva \(c\), existe un punto \(n_0\) a partir del cual se cumple:

\[
\left|\frac{C(n)}{g(n)}\right|\gt c, \qquad \forall n\ge n_0
\]

Despejando \(C(n)\), la condición se expresa como:

\[
C(n)\gt c\cdot g(n), \qquad \forall n\ge n_0
\]

Con relación a \(n_0\), su cálculo sigue el mismo razonamiento: se selecciona un valor del intervalo solución abierto que haga válida la desigualdad para todo \(n\ge n_0\):

\[
n_0\in\mathbb{R}^{+}: C(n)\gt c\cdot g(n)\qquad \forall n\ge n_0
\]

La simulación permite modificar \(\varepsilon\), cuyo valor establece el incremento mínimo respecto al extremo abierto del intervalo solución. Además, la línea de \(n_0\) se puede arrastrar para seleccionar cualquier umbral válido igual o mayor que dicho incremento.

<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-3/comparacion_little_omega.png" alt="Ejemplo gráfico de una cota inferior estricta little omega"><figcaption>En \(\omega(g(n))\), \(C(n)\) termina superando cualquier múltiplo positivo de la referencia.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-3/comparacion_little_omega_2.png" alt="Segundo ejemplo gráfico de notación little omega"><figcaption>El cociente \(C(n)/g(n)\) crece sin límite cuando la relación inferior es estricta.</figcaption></figure>
</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../3-notacion-big-omega/">← 3.5.3 Notación Ω</a><a class="section-step__index" href="../">Capítulo 3</a><a class="section-step__next" href="../5-notacion-theta/">3.5.5 Notación Θ →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>
