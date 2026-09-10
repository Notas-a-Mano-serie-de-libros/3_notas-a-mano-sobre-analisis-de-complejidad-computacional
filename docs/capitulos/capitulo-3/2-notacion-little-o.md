<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>

# 3.3.3 Notación o

<span class="chapter-kicker">Capítulo 3</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/notebooks/2_notacion_little_o.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

La notación \(o\) se utiliza para mostrar que \(C(n)\) crece **estrictamente más lento** que una función de referencia \(g(n)\). A diferencia de \(O(g(n))\), aquí no basta con que \(C(n)\) esté acotada superiormente por algún múltiplo de \(g(n)\); el cociente entre ambas funciones debe hacerse arbitrariamente pequeño cuando \(n\) crece.

Formalmente, se exige que el límite del cociente sea cero:

\[
\lim_{n\to\infty}\left(\frac{C(n)}{g(n)}\right)=0
\]

Esto significa que, para cualquier constante positiva \(c\), existe un punto \(n_0\) a partir del cual se cumple:

\[
\left|\frac{C(n)}{g(n)}\right|\lt c, \qquad \forall n\ge n_0
\]

Despejando \(C(n)\), la condición se expresa como:

\[
C(n)\lt c\cdot g(n), \qquad \forall n\ge n_0
\]

Con relación a \(n_0\), su cálculo sigue el mismo razonamiento: se selecciona un valor del intervalo solución abierto que haga válida la desigualdad para todo \(n\ge n_0\):

\[
n_0\in\mathbb{R}^{+}: C(n)\lt c\cdot g(n)\qquad \forall n\ge n_0
\]

La simulación permite modificar \(\varepsilon\), cuyo valor establece el incremento mínimo respecto al extremo abierto del intervalo solución. Además, la línea de \(n_0\) se puede arrastrar para seleccionar cualquier umbral válido igual o mayor que dicho incremento.

<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-3/comparacion_little_o.png" alt="Ejemplo gráfico de una cota superior estricta little o"><figcaption>En \(o(g(n))\), la referencia termina dominando a \(C(n)\) para cualquier constante positiva.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-3/comparacion_little_o2.png" alt="Segundo ejemplo gráfico de notación little o"><figcaption>El cociente \(C(n)/g(n)\) tiende a cero cuando la relación superior es estricta.</figcaption></figure>
</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../1-notacion-big-o/">← 3.5.1 Notación O</a><a class="section-step__index" href="../">Capítulo 3</a><a class="section-step__next" href="../3-notacion-big-omega/">3.5.3 Notación Ω →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>
