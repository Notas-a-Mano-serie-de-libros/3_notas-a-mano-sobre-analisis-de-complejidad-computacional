<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>

# 5.5.4 Teorema maestro

<span class="chapter-kicker">Capítulo 5</span>

El teorema maestro permite resolver relaciones de recurrencia de algoritmos que siguen la estrategia de dividir y vencer. Proporciona una estimación asintótica de la complejidad, omitiendo los términos de menor magnitud.

Existen varias formulaciones porque los algoritmos no siempre generan subproblemas del mismo tamaño ni tienen el mismo costo externo. El teorema **básico** estudia costos polinómicos simples; el **extendido** incorpora factores polinómicos y logarítmicos; el **generalizado** permite abordar términos recursivos con tamaños distintos. Aunque la última versión tiene un alcance mayor, utilice la versión básica o la extendida cuando sus condiciones sean suficientes.

## Teorema maestro básico

Resuelva relaciones que tienen la forma:

\[
C(n)=a\cdot C\!\left(\frac{n}{b}\right)+f(n)
\qquad\text{donde:}\quad
\begin{cases}
f(n)\in\Theta(n^k),\quad k\geq 0 \\
a\geq1,\quad b>1 \\
C(1)\in\Theta(1)
\end{cases}
\]

Compare \(f(n)\) con el costo del último nivel del árbol. Para expresar ese costo, determine cuándo el tamaño del subproblema alcanza el caso base:

\[
\frac{n}{b^k}=1\quad\Longrightarrow\quad k=\log_b(n)
\]

Aquí \(k\) identifica el nivel del árbol; en la condición de \(f(n)\), identifica el exponente polinómico. Sustituya el nivel final en la cantidad de nodos \(a^k\):

\[
a^k=a^{\log_b(n)}
\]

Multiplique la cantidad de hojas por el costo constante del caso base:

\[
C_{\log_b(n)}\in O\!\left(a^{\log_b(n)}\right)\cdot O(1)
=O\!\left(a^{\log_b(n)}\right)
\]

Reescriba \(a=b^{\log_b(a)}\) y aplique las propiedades de las potencias:

\[
a^{\log_b(n)}
=\left(b^{\log_b(a)}\right)^{\log_b(n)}
=\left(b^{\log_b(n)}\right)^{\log_b(a)}
=n^{\log_b(a)}
\]

Compare ahora \(f(n)\) con \(n^{\log_b(a)}\) y seleccione el caso correspondiente:

- **Caso 1:** Si el costo externo crece con un orden polinómico menor que \(n^{\log_b(a)}\), identifique el costo del último nivel como dominante.

    \[
    f(n)\in O\!\left(n^{\log_b(a)-\varepsilon}\right),\quad\varepsilon>0
    \quad\Longrightarrow\quad C(n)\in\Theta\!\left(n^{\log_b(a)}\right)
    \]

- **Caso 2:** Si ambos costos tienen el mismo orden, sume las contribuciones de los niveles e incorpore el factor logarítmico.

    \[
    f(n)\in\Theta\!\left(n^{\log_b(a)}\right)
    \quad\Longrightarrow\quad C(n)\in\Theta\!\left(n^{\log_b(a)}\cdot\log_b(n)\right)
    \]

- **Caso 3:** Si el costo externo crece con un orden polinómico mayor, compruebe la regularidad antes de tomar \(f(n)\) como dominante.

    \[
    f(n)\in\Omega\!\left(n^{\log_b(a)+\varepsilon}\right),\quad\varepsilon>0
    \]

    \[
    a\cdot f\!\left(\frac{n}{b}\right)\leq c\cdot f(n),\quad0<c<1
    \quad\Longrightarrow\quad C(n)\in\Theta(f(n))
    \]

Compruebe la condición de regularidad para todo tamaño suficientemente grande. La separación polinómica de los casos 1 y 3 permite distinguirlos del caso de igualdad.

## Teorema maestro extendido

Resuelva relaciones que combinan factores polinómicos y logarítmicos:

\[
C(n)=a\cdot C\!\left(\frac{n}{b}\right)+f(n)
\qquad\text{donde:}\quad
\begin{cases}
f(n)\in\Theta\!\left(n^k\cdot\log_\ell^p(n)\right) \\
k\geq0,\quad p\in\mathbb{R},\quad\ell>1 \\
a\geq1,\quad b>1,\quad C(1)\in\Theta(1)
\end{cases}
\]

Compare \(a\) con \(b^k\). Para comprender esta comparación, cuente los \(a^i\) subproblemas del nivel \(i\) y calcule el costo local:

\[
f_i(n)=\left(\frac{n}{b^i}\right)^k\cdot\log_\ell^p\!\left(\frac{n}{b^i}\right)
\]

Multiplique por la cantidad de nodos y reorganice los factores:

\[
\begin{aligned}
C_i(n)&=a^i\cdot\left(\frac{n}{b^i}\right)^k\cdot\log_\ell^p\!\left(\frac{n}{b^i}\right) \\
&=\left(\frac{a}{b^k}\right)^i\cdot n^k\cdot\log_\ell^p\!\left(\frac{n}{b^i}\right)
\end{aligned}
\]

Sume las contribuciones de los niveles internos y añada las hojas. La razón \(a/b^k\) determina cómo cambia la contribución de cada nivel. Seleccione uno de los siguientes casos:

- **Caso 1 (\(a>b^k\)):** Identifique los niveles más profundos como la contribución dominante.

    \[
    C(n)\in\Theta\!\left(n^{\log_b(a)}\right)
    \]

- **Caso 2 (\(a=b^k\)):** Elimine el factor geométrico, que vale uno, y evalúe la suma de los factores logarítmicos según \(p\).

    \[
    C(n)\in\begin{cases}
    \Theta\!\left(n^k\cdot\log_\ell^{p+1}(n)\right) & p>-1 \\
    \Theta\!\left(n^k\cdot\log_\ell(\log_\ell(n))\right) & p=-1 \\
    \Theta(n^k) & p<-1
    \end{cases}
    \]

- **Caso 3 (\(a<b^k\)):** Identifique los niveles superiores como dominantes y conserve el costo externo.

    \[
    C(n)\in\Theta\!\left(n^k\cdot\log_\ell^p(n)\right)
    \]

Reconozca la forma de \(f(n)\) y el caso aplicable antes de utilizar las fórmulas. Los escenarios negativos de \(p\) requieren considerar los logaritmos fuera del caso base, para tamaños suficientemente grandes.

## Teorema maestro generalizado

Utilice el teorema Akra–Bazzi cuando los términos recursivos tengan distintas fracciones del tamaño original:

\[
C(n)=\left[\sum_{i=1}^{m}a_i\cdot C(b_i\cdot n)\right]+f(n)
\qquad\text{donde:}\quad
\begin{cases}
n,m\in\mathbb{N},\quad m\geq1 \\
a_i,b_i,c\in\mathbb{R}^{+},\quad0<b_i<1 \\
f(n)\geq0,\quad f(n)\in O(n^c)
\end{cases}
\]

- **\(a_i\):** Identifique el peso de cada término. Si representa una cantidad de llamadas del algoritmo, interprete su valor como un entero positivo.
- **\(b_i\):** Identifique la fracción del tamaño original que recibe cada subproblema.
- **\(f(n)\):** Identifique el trabajo externo y compruebe las condiciones de crecimiento y regularidad del teorema.

Aplique el procedimiento del libro:

1. Identifique los coeficientes \(a_i\) y \(b_i\) de cada término recursivo.
2. Construya la ecuación característica y despeje \(p\):

    \[
    \sum_{i=1}^{m}a_i\cdot b_i^p=1,\qquad p\in\mathbb{R}
    \]

3. Reemplace \(p\) y \(f(n)\) en \(I\) y resuelva la integral:

    \[
    I=\int_1^n\frac{f(u)}{u^{p+1}}\,du
    \]

4. Agrupe los términos y simplifique:

    \[
    C(n)\in\Theta\!\left(n^p\cdot(1+I)\right)
    \]

Esta formulación utiliza la ecuación característica y la integral; no divide la solución en los tres casos de las versiones básica y extendida.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../arbol-recurrencia/">← 5.5.3 Árbol de recurrencia</a><a class="section-step__index" href="../">Capítulo 5</a><a class="section-step__next" href="../ecuacion-caracteristica/">5.5.5 Ecuación característica →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>
