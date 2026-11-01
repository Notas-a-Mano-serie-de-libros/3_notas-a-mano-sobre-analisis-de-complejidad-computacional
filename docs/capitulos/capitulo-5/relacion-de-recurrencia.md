<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>

# 5.2 Relación de recurrencia

<span class="chapter-kicker">Capítulo 5</span>

Una relación de recurrencia es una ecuación que expresa cada término de una sucesión mediante términos anteriores, a partir de condiciones iniciales bien definidas. Permite describir un proceso en el que cada estado depende de los anteriores.

## 5.2.1 Definición formal

Sea \(\{a_n\}_{n\in\mathbb{N}}\) una sucesión. Una recurrencia de orden \(k\) se expresa como:

\[
a_n=\begin{cases}
c_i & n=i,\quad 0\leq i<k \\
f(a_{n-1},a_{n-2},\ldots,a_{n-k}) & n\geq k
\end{cases}
\qquad n,k,i\in\mathbb{N},\quad k\geq 1
\]

Donde:

- **\(a_n\):** Término actual de la sucesión.
- **\(a_{n-1},\ldots,a_{n-k}\):** Términos anteriores que intervienen en la ecuación.
- **\(f\):** Regla que relaciona el término actual con los anteriores.
- **\(k\):** Orden de la relación; es la distancia entre el índice actual y el índice del término anterior más lejano que interviene.
- **\(c_i\):** Condiciones iniciales que fijan los primeros \(k\) términos y, junto con una regla bien definida, determinan una solución única.

\[
\begin{aligned}
a_n&=a_{n-1}+1 &&\text{(orden 1)} \\
a_n&=a_{n-1}+a_{n-2} &&\text{(orden 2)} \\
a_n&=a_{n-1}+a_{n-2}+\cdots+a_{n-k} &&\text{(orden }k\text{)}
\end{aligned}
\]

Por ejemplo, la regla \(a_n=a_{n-1}+a_{n-2}\) con \(a_0=0\) y \(a_1=1\) genera una única sucesión:

\[
(0,1,1,2,3,5,\ldots)
\]

Sin fijar los dos términos iniciales, la misma regla admite distintas soluciones según los valores elegidos para \(a_0\) y \(a_1\).

## 5.2.2 Ejemplos

- **Factorial:** El producto que define el factorial se separa en el factor actual y el factorial anterior.

    \[
    n!=\prod_{j=1}^{n}j=n\cdot(n-1)!
    \]

    \[
    \begin{aligned}
    5!&=5\cdot4! \\
       &=5\cdot4\cdot3! \\
       &=5\cdot4\cdot3\cdot2! \\
       &=5\cdot4\cdot3\cdot2\cdot1!
    \end{aligned}
    \]

    Al reunir la regla y las condiciones iniciales:

    \[
    a_n=\begin{cases}
    1 & n\in\{0,1\} \\
    n\cdot a_{n-1} & n>1
    \end{cases}
    \]

- **Sucesión de Fibonacci:** En la sucesión \((1,1,2,3,5,8,13,21,\ldots)\), cada término posterior a los dos primeros se obtiene sumando sus dos predecesores.

    \[
    a_n=\begin{cases}
    1 & n\in\{0,1\} \\
    a_{n-1}+a_{n-2} & n>1
    \end{cases}
    \]

**Discusión:** Las recurrencias aparecen en contextos matemáticos, físicos y computacionales donde un estado depende de estados anteriores. En algoritmos recursivos, describen la descomposición del problema en instancias más pequeñas hasta alcanzar un caso base.

## 5.3 Tipos de relaciones de recurrencia

Las relaciones se clasifican mediante criterios que pueden combinarse: linealidad, presencia de un término independiente y variación de los coeficientes.

### 5.3.1 Relaciones lineales y no lineales

Una relación es **lineal** cuando los términos anteriores aparecen mediante una suma ponderada, sin productos ni potencias entre ellos. La forma mostrada en el libro es:

\[
a_n=\sum_{i=1}^{k}c_i\cdot a_{n-i},\qquad c_i\in\mathbb{R}^{+}
\]

Si intervienen productos, cocientes o potencias de los propios términos de la sucesión, la relación es **no lineal**.

\[
\begin{aligned}
a_n&=2\cdot a_{n-1}+3\cdot a_{n-2} &&\text{(lineal)} \\
a_n&=a_{n-1}\cdot a_{n-2} &&\text{(no lineal)}
\end{aligned}
\]

**Discusión:** Muchos algoritmos recursivos clásicos generan relaciones lineales. Las relaciones no lineales requieren tratar las operaciones entre términos, no solo sumar sus contribuciones.

### 5.3.2 Relaciones homogéneas y no homogéneas

Una relación es **homogénea** cuando no incluye un término independiente. En el contexto de las relaciones lineales, solo contiene la suma ponderada de términos anteriores. Si se agrega un término \(g(n)\) no idénticamente nulo que no depende de esos términos, es **no homogénea**.

\[
\begin{aligned}
a_n&=a_{n-1}+a_{n-2} &&\text{(homogénea)} \\
a_n&=a_{n-1}+a_{n-2}+g(n) &&\text{(no homogénea)}
\end{aligned}
\]

**Discusión:** Las relaciones no homogéneas son frecuentes en el análisis de algoritmos porque el término independiente representa el trabajo realizado fuera de las llamadas recursivas. Las homogéneas aparecen en procesos como la sucesión de Fibonacci.

### 5.3.3 Relaciones con coeficientes variables

Los coeficientes son **variables** cuando los factores que ponderan los términos anteriores dependen de \(n\):

\[
a_n=\sum_{i=1}^{k}c_i(n)\cdot a_{n-i}
\]

**Discusión:** El factorial es un ejemplo representativo: en \(a_n=n\cdot a_{n-1}\), el coeficiente del término anterior cambia con el índice. Si los factores no dependen de \(n\), se habla de coeficientes constantes.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../sucesion-numerica/">← 5.1 Sucesión numérica</a><a class="section-step__index" href="../">Capítulo 5</a><a class="section-step__next" href="../formas-de-recurrencia/">5.4 Recurrencias y análisis de complejidad →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>
