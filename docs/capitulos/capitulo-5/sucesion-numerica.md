<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>

# 5.1 Sucesión numérica

<span class="chapter-kicker">Capítulo 5</span>

Antes de estudiar las relaciones de recurrencia, es necesario introducir el concepto de sucesión numérica: una lista ordenada de términos en la que cada término ocupa una posición específica indicada por un índice \(n\in\mathbb{N}\).

## 5.1.1 Definición

Una sucesión se modela como una función con dominio en los números naturales y codominio en un conjunto \(S\) de interés:

\[
\begin{aligned}
a:\mathbb{N}&\longrightarrow S \\
n&\longmapsto a_n
\end{aligned}
\]

Donde:

- **\(n\):** Índice que identifica la posición de un término.
- **\(a_n\):** Término de la sucesión situado en la posición \(n\).
- **\(S\):** Conjunto al que pertenecen los valores de la sucesión.

Las notaciones habituales son:

\[
\begin{aligned}
(a_0,a_1,a_2,\ldots,a_n)&\qquad\text{(lista explícita de términos)} \\
a_n,\quad n\in\mathbb{N}&\qquad\text{(término general indexado)} \\
\{a_n\}_{n\in\mathbb{N}}&\qquad\text{(sucesión indexada)}
\end{aligned}
\]

## 5.1.2 Tipos de sucesiones numéricas

Las sucesiones se clasifican según el patrón o la relación entre sus términos:

- **Sucesión aritmética:** La diferencia entre términos consecutivos es constante.

    \[
    (2,5,8,11,\ldots)\qquad a_n-a_{n-1}=3
    \]

- **Sucesión geométrica:** El cociente entre términos consecutivos es constante.

    \[
    (3,6,12,24,\ldots)\qquad\frac{a_n}{a_{n-1}}=2
    \]

- **Sucesión constante:** Todos los términos son iguales.

    \[
    (5,5,5,5,\ldots)\qquad a_n=a_{n-1}
    \]

- **Sucesión alternante:** El signo de los términos cambia de forma alternada.

    \[
    (-1,2,-3,4,-5,\ldots)\qquad a_n\cdot a_{n-1}<0
    \]

- **Sucesión periódica:** Los términos se repiten cada cierto número fijo de posiciones.

    \[
    (1,2,3,1,2,3,\ldots)\qquad a_n=a_{n+3}
    \]

- **Sucesión recursiva:** Cada término se define mediante uno o más términos anteriores.

    \[
    (1,3,7,15,31,\ldots)\qquad a_n=2\cdot a_{n-1}+1,\quad n\geq 1
    \]

Estas categorías pueden coincidir: una sucesión puede ser, por ejemplo, geométrica y estar definida recursivamente.

## 5.1.3 Convergencia y divergencia

Una sucesión numérica es **convergente** si sus términos se aproximan a un límite finito \(L\) cuando el índice crece indefinidamente:

\[
\lim_{n\to\infty}a_n=L
\]

Si no existe un límite finito, la sucesión es **divergente**. Puede crecer sin límite o seguir oscilando sin aproximarse a un único valor.

- **Ejemplo convergente:** Los términos se aproximan a cero.

    \[
    a_n=\frac{1}{n},\quad n\geq 1
    \qquad\Longrightarrow\qquad
    \lim_{n\to\infty}a_n=0
    \]

- **Ejemplo divergente:** Los términos crecen sin límite.

    \[
    a_n=3\cdot n+2
    \qquad\Longrightarrow\qquad
    \lim_{n\to\infty}a_n=+\infty
    \]

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a class="section-step__index" href="../">Capítulo 5</a><a class="section-step__next" href="../relacion-de-recurrencia/">5.2 Relación de recurrencia →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>
