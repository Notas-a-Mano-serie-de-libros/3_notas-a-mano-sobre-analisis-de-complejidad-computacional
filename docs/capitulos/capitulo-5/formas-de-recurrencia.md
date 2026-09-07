<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>

# 5.4 Formas de las relaciones de recurrencia

<span class="chapter-kicker">Capítulo 5</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo5/notebooks/0_arboles_recursion.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar notebook en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

Las relaciones de recurrencia describen el costo de un problema mediante el costo de instancias más pequeñas, donde:

- \(C(n)\) representa la función de complejidad para una entrada de tamaño \(n\).
- \(a\) indica cuántos subproblemas genera cada llamada recursiva.
- \(b\) determina cuánto se reduce el tamaño del problema.
- \(f(n)\) representa el costo de las operaciones realizadas fuera de las llamadas recursivas.
- \(h\) indica la altura del árbol o el número de niveles de expansión que se desean analizar.
- \(k\) representa el exponente cuando se selecciona una función de costo polinómica \(f(n)=n^k\).
- \(a_i\) pondera la cantidad de llamadas de cada tipo y \(b_i\) determina el factor de reducción de su argumento en una relación mixta.

### Relaciones de reducción

\[
C(n)=aC(n-b)+f(n),\qquad a,b,n\in\mathbb{N},\quad a\geq 1,\ b\geq 1.
\]

Cada llamada disminuye el tamaño del problema en una cantidad fija \(b\).


---

### Relaciones de división

\[
C(n)=aC\!\left(\frac{n}{b}\right)+f(n),\qquad a,b,n\in\mathbb{N},\quad a\geq 1,\ b>1.
\]

Cada llamada reduce el tamaño del problema al dividirlo por un factor constante \(b\).

### Relaciones mixtas

\[
C(n)=\sum_{i=1}^{k}a_iC(b_i n)+f(n),\qquad k\geq 2,\quad 0<b_i<1.
\]

Las llamadas generan subproblemas de tamaños distintos, por lo que sus ramas pueden alcanzar el caso base en niveles diferentes.

La simulación utiliza una forma particular de la relación mixta con \(a_i=1\) y factores de división consecutivos determinados por \(b\). Selecciona el tipo de relación, elige \(f(n)\) entre \(1\), \(\log_2(n)\), \(n\), \(n\log_2(n)\), \(n^2\), \(n^3\), \(n^k\), \(2^n\) y \(n!\), y modifica los parámetros para observar cómo cambia el árbol y el costo de cada nivel.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a class="section-step__index" href="../">Capítulo 5</a><a class="section-step__next" href="../sustitucion-iterativa/">5.5.1 Sustitución iterativa →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>
