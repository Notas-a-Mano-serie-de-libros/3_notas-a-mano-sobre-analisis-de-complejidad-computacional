<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>

# 5.5.5 Ecuación característica

<span class="chapter-kicker">Capítulo 5</span>

Resuelva relaciones de recurrencia lineales con coeficientes constantes mediante una técnica algebraica. Parta de la forma general:

\[
a_n=\left[\sum_{i=1}^{k}c_i\cdot a_{n-i}\right]+f(n)
\]

Separe la solución en una parte homogénea y una particular:

\[
\underbrace{a_n}_{\text{solución general}}
=\underbrace{a_n^{(h)}}_{\text{solución homogénea}}
+\underbrace{a_n^{(p)}}_{\text{solución particular}}
\]

Use la parte homogénea para resolver la recurrencia sin el término independiente. Si \(f(n)\neq0\), encuentre además una solución particular y aplique las condiciones iniciales a la solución completa.

## Construya la ecuación característica

Haga \(f(n)=0\) y lleve los términos a un mismo lado:

\[
a_n-\sum_{i=1}^{k}c_i\cdot a_{n-i}=0
\]

Expanda la sumatoria:

\[
a_n-c_1\cdot a_{n-1}-c_2\cdot a_{n-2}-\cdots-c_k\cdot a_{n-k}=0
\]

Proponga \(a_n=r^n\), con \(r\neq0\), y sustituya:

\[
r^n-c_1\cdot r^{n-1}-c_2\cdot r^{n-2}-\cdots-c_k\cdot r^{n-k}=0
\]

Divida entre \(r^{n-k}\) para obtener el polinomio característico de grado \(k\):

\[
P(r)=r^k-c_1\cdot r^{k-1}-c_2\cdot r^{k-2}-\cdots-c_k=0
\]

Encuentre sus raíces mediante factorización o una técnica algebraica apropiada. Compruebe cada raíz \(r_i\) sustituyéndola en \(P(r_i)=0\).

## Construya la solución homogénea

- **Raíces distintas:** Combine las potencias asociadas a las \(k\) raíces.

    \[
    a_n^{(h)}=\sum_{i=1}^{k}A_i\cdot r_i^n
    \]

- **Raíces repetidas:** Si una raíz \(r_i\) tiene multiplicidad \(m\), multiplique su potencia por un polinomio de grado \(m-1\). Incluya todos sus términos para obtener soluciones independientes.

    \[
    \left(A_{i,0}+A_{i,1}\cdot n+\cdots+A_{i,m-1}\cdot n^{m-1}\right)\cdot r_i^n
    \]

Determine las constantes usando los primeros \(k\) valores de la sucesión. Para raíces distintas y una relación homogénea, forme el sistema:

\[
\begin{pmatrix}
a_0\\a_1\\\vdots\\a_{k-1}
\end{pmatrix}
=
\begin{pmatrix}
r_1^0&r_2^0&\cdots&r_k^0\\
r_1^1&r_2^1&\cdots&r_k^1\\
\vdots&\vdots&\ddots&\vdots\\
r_1^{k-1}&r_2^{k-1}&\cdots&r_k^{k-1}
\end{pmatrix}
\begin{pmatrix}
A_1\\A_2\\\vdots\\A_k
\end{pmatrix}
\]

Si hay raíces repetidas, construya las columnas con los términos polinómicos correspondientes. Si la recurrencia no es homogénea, reste el valor de la solución particular a cada condición inicial antes de resolver las constantes homogéneas.

### Ejemplos del libro

- **Dos raíces distintas:** Resuelva \(C(n)=3\cdot C(n-1)-2\cdot C(n-2)\), con \(C(0)=0\) y \(C(1)=1\).

    \[
    r^2-3\cdot r+2=(r-1)\cdot(r-2)=0
    \]

    Construya la solución y aplique las condiciones iniciales:

    \[
    C(n)=A_1+A_2\cdot2^n,\qquad
    \begin{cases}
    A_1+A_2=0\\
    A_1+2\cdot A_2=1
    \end{cases}
    \]

    Resuelva \(A_1=-1\), \(A_2=1\) y sustituya:

    \[
    C(n)=2^n-1\qquad\Longrightarrow\qquad C(n)\in\mathcal{F}(2^n)
    \]

- **Una raíz repetida:** Resuelva \(C(n)=4\cdot C(n-1)-4\cdot C(n-2)\), con las mismas condiciones iniciales.

    \[
    r^2-4\cdot r+4=(r-2)^2=0
    \]

    Incorpore la multiplicidad dos y determine las constantes:

    \[
    C(n)=(A_1+A_2\cdot n)\cdot2^n,\qquad A_1=0,\quad A_2=\frac12
    \]

    \[
    C(n)=n\cdot2^{n-1}\qquad\Longrightarrow\qquad C(n)\in\mathcal{F}(n\cdot2^n)
    \]

## Encuentre la solución particular

Use el método de **coeficientes indeterminados**, como en el libro, cuando \(f(n)\) sea un polinomio, una exponencial o una combinación de ambos. Proponga una función de la misma forma y determine sus coeficientes.

| \(f(n)\) | Forma propuesta para \(a_n^{(p)}\) |
| --- | --- |
| \(d\) | \(A\) |
| \(d\cdot n^m\) | \(A_m\cdot n^m+A_{m-1}\cdot n^{m-1}+\cdots+A_0\) |
| \(d\cdot\beta^n\) | \(A\cdot\beta^n\) |
| \(d\cdot n^m\cdot\beta^n\) | \((A_m\cdot n^m+\cdots+A_0)\cdot\beta^n\) |

Compruebe si \(\beta\), o \(r=1\) en el caso polinómico, es una raíz característica. Si tiene multiplicidad \(s\), multiplique la propuesta por \(n^s\) para evitar que coincida con un término de la solución homogénea.

Sustituya la propuesta en la recurrencia original:

\[
a_n^{(p)}=\sum_{i=1}^{k}c_i\cdot a_{n-i}^{(p)}+f(n)
\]

1. Simplifique y agrupe los términos semejantes a ambos lados.
2. Iguale sus coeficientes para construir un sistema algebraico.
3. Resuelva el sistema y obtenga los coeficientes de la solución particular.
4. Sume las soluciones homogénea y particular, y aplique las condiciones iniciales.
5. Verifique la recurrencia y conserve el término dominante para expresar su crecimiento asintótico.

### Ejemplo no homogéneo del libro

Resuelva \(C(n)=2\cdot C(n-1)+n\), con \(C(0)=1\). Obtenga la raíz \(r=2\) y proponga una solución particular lineal:

\[
C_h(n)=A\cdot2^n,\qquad C_p(n)=B\cdot n+D
\]

Sustituya la propuesta e iguale coeficientes:

\[
B\cdot n+D=2\cdot\left(B\cdot(n-1)+D\right)+n
\]

\[
\begin{cases}
B=2\cdot B+1\\
D=-2\cdot B+2\cdot D
\end{cases}
\quad\Longrightarrow\quad B=-1,\quad D=-2
\]

Reúna las dos soluciones y use \(C(0)=1\) para obtener \(A=3\):

\[
C(n)=3\cdot2^n-n-2\qquad\Longrightarrow\qquad C(n)\in\mathcal{F}(2^n)
\]

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../teorema-maestro/">← 5.5.4 Teorema maestro</a><a class="section-step__index" href="../">Capítulo 5</a><a class="section-step__next" href="../ejercicios-propuestos/">5.6.1 Ejercicios propuestos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>
