<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>

# 5.5.2 Sustitución iterativa

<span class="chapter-kicker">Capítulo 5</span>

La **sustitución iterativa** expande una recurrencia de forma sucesiva: reemplaza cada término recursivo por su definición hasta reconocer un patrón que pueda expresarse en función de \(n\) y de las condiciones iniciales.

## Procedimiento

1. Escriba la recurrencia y su condición inicial.
2. Expanda dos o tres niveles sin simplificar prematuramente.
3. Exprese los coeficientes, el argumento y la suma después de \(k\) sustituciones.
4. Resuelva \(k\) a partir del caso base.
5. Sustituya ese valor y simplifique la suma mediante dominancia.

Aplique este método a relaciones de reducción y división con un patrón analítico reconocible. Justifique el patrón general y verifique la condición inicial para completar la demostración.

## Ejemplo desarrollado

Resuelva la relación:

\[
C(n)=
\begin{cases}
1 & \text{si } n=1,\\
2 \cdot C(n/2)+n & \text{si } n>1.
\end{cases}
\]

### 1. Expandir hasta reconocer el patrón

\[
\begin{aligned}
C(n)
&=2 \cdot C(n/2)+n\\
&=2\left[2 \cdot C(n/4)+n/2\right]+n
 =4 \cdot C(n/4)+2 \cdot n\\
&=4\left[2 \cdot C(n/8)+n/4\right]+2 \cdot n
 =8 \cdot C(n/8)+3 \cdot n\\
&=16 \cdot C(n/16)+4 \cdot n=\cdots
\end{aligned}
\]

Después de \(k\) sustituciones, la forma observada es:

\[
C(n)=2^k \cdot C\!\left(\frac{n}{2^k}\right)+k \cdot n.
\]

La igualdad anterior no debe aceptarse solo por inspección: puede verificarse por inducción sobre \(k\). El caso \(k=1\) coincide con la recurrencia y, al sustituir una vez más, el exponente y el coeficiente de \(n\) aumentan exactamente como indica el patrón.

### 2. Alcanzar el caso base

El argumento de \(C\) debe ser igual a uno:

\[
\frac{n}{2^k}=1
\quad\Longrightarrow\quad
2^k=n
\quad\Longrightarrow\quad
k=\log_2(n).
\]

### 3. Sustituir y simplificar

\[
\begin{aligned}
C(n)
&=2^{\log_2(n)}C(1)+n \cdot \log_2(n)\\
&=n+n \cdot \log_2(n)\\
&=n\left(1+\log_2(n)\right).
\end{aligned}
\]

Por tanto, el crecimiento pertenece a la familia log-lineal:

\[
C(n)\in\mathcal{F}\!\left(n \cdot \log_2(n)\right).
\]

Este resultado describe el crecimiento de la función, pero por sí solo no determina si corresponde al mejor caso, al peor caso o al caso promedio de un algoritmo. Esa interpretación depende de cómo se obtuvo la recurrencia.

## Errores frecuentes

- Omitir el factor que multiplica al término recursivo durante una expansión.
- Confundir el número de sustituciones con el tamaño del subproblema.
- detener la expansión sin aplicar el caso base;
- presentar el patrón observado sin justificarlo;
- afirmar un caso de ejecución que la recurrencia no especifica.

## Compruebe su comprensión

1. Expanda tres veces \(C(n)=C(n/2)+1\) e identifique su patrón general.
2. ¿Qué cambia en el desarrollo anterior si \(C(1)=c\) en lugar de \(C(1)=1\)?
3. Explique por qué el método puede resultar difícil cuando los subproblemas no disminuyen de manera uniforme.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../solucion-relaciones-recurrencia/">← 5.5 Solución de relaciones de recurrencia</a><a class="section-step__index" href="../">Capítulo 5</a><a class="section-step__next" href="../arbol-recurrencia/">5.5.3 Árbol de recurrencia →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>
