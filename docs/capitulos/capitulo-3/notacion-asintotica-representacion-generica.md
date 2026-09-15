<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>

# 3.2 Comportamiento asintótico general

<span class="chapter-kicker">Capítulo 3</span>

La obra parte de una función compuesta por términos ordenados de menor a mayor crecimiento:

\[
f(n)=\sum_{i=1}^{m}f_i(n),
\qquad
f_1(n)\prec f_2(n)\prec\cdots\prec f_m(n)
\]

Al dividir por el término dominante y llevar la razón al límite se obtiene:

\[
\lim_{n\to\infty}\frac{f(n)}{f_m(n)}
=1+\sum_{i=1}^{m-1}\lim_{n\to\infty}\frac{f_i(n)}{f_m(n)}=1
\]

Por tanto, \(f(n)\sim f_m(n)\): para entradas suficientemente grandes, su comportamiento está determinado por el término de mayor crecimiento. En un polinomio domina el término de mayor grado; en una suma que contiene un término exponencial y términos polinómicos, domina el exponencial.

Este razonamiento produce la jerarquía funcional asintótica:

\[
1\prec\log_\ell(n)\prec n\prec n \cdot \log_\ell(n)\prec n^2\prec n^3
\prec\cdots\prec n^k\prec2^n\prec n!
\]

La jerarquía compara tendencias teóricas y no sustituye el costo exacto de una implementación.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../">Capítulo 3</a><a class="section-step__index" href="../">Capítulo 3</a><a class="section-step__next" href="../familias-de-funciones/">3.3 Familias de funciones →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>
