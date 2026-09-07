# Simulación interactiva del límite asintótico para notación \(\omega\)

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 3</span>

La notación \(\omega\) se utiliza para mostrar que \(C(n)\) crece **estrictamente más rápido** que una función de referencia \(g(n)\). Es la contraparte estricta de la notación \(\Omega\): no basta con que \(C(n)\) esté por encima de algún múltiplo de \(g(n)\), sino que el cociente debe crecer sin límite.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/notebooks/4_notacion_little_omega.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

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
