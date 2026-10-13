<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>

# 3.3 Familias de funciones

<span class="chapter-kicker">Capítulo 3</span>

Una familia agrupa funciones que comparten una misma estructura algebraica y se diferencian por los valores de sus parámetros. No es, en principio, una lista de órdenes de complejidad. Por ejemplo, todas las expresiones \(f(x)=mx+b\) forman una familia de rectas al variar \(m\) y \(b\); de modo análogo, \(f(x)=ax^2+bx+c\), con \(a\neq0\), describe una familia de parábolas.

## 3.3.1 Definición

Sea \(\Lambda\) un conjunto no vacío de parámetros. Una familia de funciones es una colección de la forma:

\[
\mathcal{F}=\{f_\lambda:\lambda\in\Lambda\}.
\]

Cada \(\lambda\) identifica una función de la colección, mientras que todas las funciones conservan la estructura común que define a \(\mathcal{F}\). Para las funciones lineales puede tomarse \(\Lambda=\mathbb{R}^2\), con \(\lambda=(m,b)\), y escribir:

\[
\mathcal{F}=\{f_{(m,b)}:\mathbb{R}\to\mathbb{R}\mid(m,b)\in\mathbb{R}^2\},
\qquad f_{(m,b)}(x)=mx+b.
\]

Esta representación permite razonar sobre la colección completa sin estudiar por separado cada elección posible de parámetros.

## 3.3.2 Familias en el límite asintótico

Para una función de complejidad \(C:\mathbb{N}\to\mathbb{R}^{+}\), la obra reúne en una misma familia las funciones que presentan un comportamiento equivalente al de \(C(n)\) cuando \(n\to\infty\):

\[
\mathcal{F}(C(n))=\{f_\lambda:\mathbb{N}\to\mathbb{R}^{+}\mid
\lambda\in\Lambda,\ f_\lambda(n)\sim C(n)\}.
\]

El símbolo \(\sim\) expresa equivalencia en el límite. Por ejemplo, las funciones

\[
3 \cdot n+5,\qquad 7 \cdot n-2,\qquad n+\log(n)
\]

son asintóticamente lineales; por ello pertenecen a \(\mathcal{F}(n)\). Comparten el término dominante, aunque sus expresiones exactas y sus costos para entradas finitas sean diferentes.

## 3.3.3 Propiedades asintóticas

| Propiedad | Expresión | Lectura |
| --- | --- | --- |
| Invarianza frente a constantes | \(\mathcal{F}(c \cdot g(n))=\mathcal{F}(g(n)),\ c>0\) | Una constante positiva no cambia la familia asintótica. |
| Aditividad | \(\mathcal{F}(f(n))+\mathcal{F}(g(n))\subseteq \mathcal{F}(f(n)+g(n))\) | La suma conserva la combinación de comportamientos. |
| Multiplicatividad | \(\mathcal{F}(f(n))\cdot\mathcal{F}(g(n))\subseteq \mathcal{F}(f(n)\cdot g(n))\) | El producto combina los órdenes de ambas funciones. |
| Dominancia | Si \(\lim_{n\to\infty}g(n)/f(n)=0\), entonces \(\mathcal{F}(f(n)+g(n))=\mathcal{F}(f(n))\) | El término de menor crecimiento desaparece en el límite. |

## 3.3.4 Ejemplos

\[
\begin{aligned}
3 \cdot n+5 &\in \mathcal{F}(n)\\
n \cdot \log(n)+5 \cdot n &\in \mathcal{F}(n \cdot \log(n))\\
k \cdot n!+2^n &\in \mathcal{F}(n!)\\
3 \cdot n^2+7 \cdot n+1 &\in \mathcal{F}(n^2)\\
n^2 \cdot 2^n+n^3 &\in \mathcal{F}(n^2 \cdot 2^n)
\end{aligned}
\]

### Caso particular: funciones constantes

Si \(f(n)=k\), con \(k>0\), la invarianza frente a constantes permite escribir \(f(n)\in \mathcal{F}(1)\). Esta simplificación no significa que todas las constantes tengan el mismo costo real. Un algoritmo con \(T(n)=10^{10}\) sigue siendo constante respecto de \(n\), pero puede resultar impráctico. La familia describe crecimiento en el límite; no conserva el valor exacto de ejecución.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../notacion-asintotica-representacion-generica/">← 3.2 Comportamiento asintótico general</a><a class="section-step__index" href="../">Capítulo 3</a><a class="section-step__next" href="../ejemplos-concretos-notaciones/">3.4 Notación asintótica simplificada →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>
