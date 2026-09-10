<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>

# 3.2 Familias de funciones

<span class="chapter-kicker">Capítulo 3</span>

<div class="lab-action"><a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/notebooks/notacion_asintotica_representacion_generica.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a><small class="lab-action__note">Se abrirá en una pestaña nueva.</small></div>

Una familia agrupa funciones que comparten una misma estructura algebraica y se diferencian por los valores de sus parámetros. No es, en principio, una lista de órdenes de complejidad. Por ejemplo, todas las expresiones \(f(x)=mx+b\) forman una familia de rectas al variar \(m\) y \(b\); de modo análogo, \(f(x)=ax^2+bx+c\), con \(a\neq0\), describe una familia de parábolas.

## 3.2.1 Definición

Sea \(\Lambda\) un conjunto no vacío de parámetros. Una familia de funciones es una colección de la forma:

\[
F=\{f_\lambda:\lambda\in\Lambda\}.
\]

Cada \(\lambda\) identifica una función de la colección, mientras que todas las funciones conservan la estructura común que define a \(F\). Para las funciones lineales puede tomarse \(\Lambda=\mathbb{R}^2\), con \(\lambda=(m,b)\), y escribir:

\[
F=\{f_{(m,b)}:\mathbb{R}\to\mathbb{R}\mid(m,b)\in\mathbb{R}^2\},
\qquad f_{(m,b)}(x)=mx+b.
\]

Esta representación permite razonar sobre la colección completa sin estudiar por separado cada elección posible de parámetros.

## 3.2.2 Familias en el límite asintótico

Para una función de complejidad \(C:\mathbb{N}\to\mathbb{R}^{+}\), la obra reúne en una misma familia las funciones que presentan un comportamiento equivalente al de \(C(n)\) cuando \(n\to\infty\):

\[
F(C(n))=\{f_\lambda:\mathbb{N}\to\mathbb{R}^{+}\mid
\lambda\in\Lambda,\ f_\lambda(n)\sim C(n)\}.
\]

El símbolo \(\sim\) expresa equivalencia en el límite. Por ejemplo, las funciones

\[
3n+5,\qquad 7n-2,\qquad n+\log(n)
\]

son asintóticamente lineales; por ello pertenecen a \(F(n)\). Comparten el término dominante, aunque sus expresiones exactas y sus costos para entradas finitas sean diferentes.

## 3.2.3 Propiedades asintóticas

| Propiedad | Expresión | Lectura |
| --- | --- | --- |
| Invarianza frente a constantes | \(F(c\,g(n))=F(g(n)),\ c>0\) | Una constante positiva no cambia la familia asintótica. |
| Aditividad | \(F(f(n))+F(g(n))\subseteq F(f(n)+g(n))\) | La suma conserva la combinación de comportamientos. |
| Multiplicatividad | \(F(f(n))F(g(n))\subseteq F(f(n)g(n))\) | El producto combina los órdenes de ambas funciones. |
| Dominancia | Si \(\lim_{n\to\infty}g(n)/f(n)=0\), entonces \(F(f(n)+g(n))=F(f(n))\) | El término de menor crecimiento desaparece en el límite. |

## 3.2.4 Ejemplos

\[
\begin{aligned}
3n+5 &\in F(n),\\
n\log(n)+5n &\in F(n\log(n)),\\
k\,n!+2^n &\in F(n!),\\
3n^2+7n+1 &\in F(n^2),\\
n^2 2^n+n^3 &\in F(n^2 2^n).
\end{aligned}
\]

### Caso particular: funciones constantes

Si \(f(n)=k\), con \(k>0\), la invarianza frente a constantes permite escribir \(f(n)\in F(1)\). Esta simplificación no significa que todas las constantes tengan el mismo costo real. Un algoritmo con \(T(n)=10^{10}\) sigue siendo constante respecto de \(n\), pero puede resultar impráctico. La familia describe crecimiento en el límite; no conserva el valor exacto de ejecución.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../">Capítulo 3</a><a class="section-step__index" href="../">Capítulo 3</a><a class="section-step__next" href="../notacion-asintotica-representacion-generica/">3.3 Representación general →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>
