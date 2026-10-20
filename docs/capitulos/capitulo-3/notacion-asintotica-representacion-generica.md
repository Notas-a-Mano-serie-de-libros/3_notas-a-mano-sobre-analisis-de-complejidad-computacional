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

## Ejemplos razonados

Para \(f(n)=7 \cdot n^3+4 \cdot n^2+20\), divida entre \(n^3\):

\[
\frac{f(n)}{n^3}=7+\frac{4}{n}+\frac{20}{n^3}
\xrightarrow[n\to\infty]{}7.
\]

El límite es una constante positiva y finita, por lo que \(f(n)\in\Theta(n^3)\). La constante no tiene que ser uno: basta con que ninguno de los dos términos crezca asintóticamente más rápido que el otro.

Para \(g(n)=2^n+n^5\), compare el término polinómico con el exponencial:

\[
\lim_{n\to\infty}\frac{n^5}{2^n}=0.
\]

Así, \(g(n)\in\Theta(2^n)\). Que \(n^5\) pueda ser mayor para ciertos valores pequeños no contradice la conclusión, porque la notación asintótica estudia el comportamiento después de algún umbral.

## Qué no puede concluirse

- El término dominante no entrega el tiempo exacto de ejecución.
- Dos funciones de la misma familia pueden diferir notablemente para entradas pequeñas.
- Simplificar una expresión no determina por sí solo si representa mejor, peor o caso promedio.
- La jerarquía no permite descartar constantes cuando se hace una estimación física en segundos o bytes.

## Compruebe su comprensión

1. Determine el término dominante de \(3 \cdot n^2 \cdot \log(n)+8 \cdot n^2+n\).
2. Justifique mediante un límite que \(n \cdot \log(n)\in o(n^{3/2})\).
3. Explique por qué \(1000 \cdot n\) puede superar a \(n^2\) para algunas entradas aunque \(n^2\) tenga mayor crecimiento asintótico.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../">Capítulo 3</a><a class="section-step__index" href="../">Capítulo 3</a><a class="section-step__next" href="../familias-de-funciones/">3.3 Familias de funciones →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>
