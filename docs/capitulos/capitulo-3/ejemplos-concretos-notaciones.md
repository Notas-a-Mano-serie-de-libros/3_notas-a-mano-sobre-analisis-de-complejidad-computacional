<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>

# 3.4 Notación asintótica simplificada

<span class="chapter-kicker">Capítulo 3</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo3/notebooks/ejemplos_concretos_notaciones.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
</div>

La notación asintótica simplificada conserva el término que determina el crecimiento de una función cuando \(n\) aumenta y omite constantes multiplicativas y términos de menor orden. Los ejemplos siguientes muestran cómo esa simplificación se relaciona con las cotas formales.

En todos los ejemplos se analiza la misma función:

\[
C(n)=n^3+2 \cdot n^2+n+5
\]

El propósito es mostrar que la función de referencia cambia según la relación que se quiere demostrar. No basta con observar que ambas curvas parecen próximas: deben exhibirse constantes y un umbral, o calcular el límite correspondiente.

### Ejemplo 1 · Cota superior \(O(n^3)\)

Se toma \(g(n)=n^3\). Para \(n\geq 1\), se cumplen \(n^2\leq n^3\), \(n\leq n^3\) y \(1\leq n^3\). Por tanto:

\[
C(n)\leq n^3+2 \cdot n^3+n^3+5 \cdot n^3=9 \cdot n^3.
\]

Al elegir \(c=9\) y \(n_0=1\), queda demostrada la desigualdad \(C(n)\leq c \cdot g(n)\) para todo \(n\geq n_0\). En consecuencia, \(C(n)\in O(n^3)\). El valor de \(c\) no tiene que ser mínimo: cualquier constante válida prueba la cota.

### Ejemplo 2 · Cota superior estricta \(o(n^4)\)

Ahora se compara con \(g(n)=n^4\). La relación es estricta porque:

\[
\lim_{n\to\infty}\frac{C(n)}{n^4}
=\lim_{n\to\infty}\left(\frac1n+\frac2{n^2}+\frac1{n^3}+\frac5{n^4}\right)=0.
\]

El límite cero significa que, para cualquier constante \(c>0\), existe un umbral \(n_0\) a partir del cual \(C(n)<c n^4\). Por eso \(C(n)\in o(n^4)\). Esta afirmación es más fuerte que decir solamente \(C(n)\in O(n^4)\).

### Ejemplo 3 · Cota inferior \(\Omega(n^3)\)

Como todos los términos adicionales son no negativos para \(n\geq1\):

\[
C(n)=n^3+2 \cdot n^2+n+5\geq n^3
\]

Con \(c=1\) y \(n_0=1\) se satisface \(C(n)\geq c \cdot g(n)\). Así, \(C(n)\in\Omega(n^3)\). Esta cota garantiza que el crecimiento de \(C\) no puede quedar asintóticamente por debajo del cúbico.

### Ejemplo 4 · Cota inferior estricta \(\omega(n^2)\)

Al usar \(g(n)=n^2\), el cociente es:

\[
\frac{C(n)}{n^2}=n+2+\frac1n+\frac5{n^2}.
\]

Como este cociente tiende a infinito, para cualquier \(c>0\) se puede encontrar un \(n_0\) tal que \(C(n)>c n^2\) cuando \(n\geq n_0\). En consecuencia, \(C(n)\in\omega(n^2)\).

### Ejemplo 5 · Cota ajustada \(\Theta(n^3)\)

Las pruebas de los ejemplos 1 y 3 pueden combinarse:

\[
n^3\leq C(n)\leq9n^3,\qquad n\geq1.
\]

Con \(c_1=1\), \(c_2=9\) y \(n_0=1\), la función queda encerrada entre dos múltiplos positivos de \(n^3\). Por ello, \(C(n)\in\Theta(n^3)\). Esta es la clasificación ajustada: \(n^3\) es simultáneamente cota superior e inferior del mismo orden.

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Ejemplos concretos del libro para notaciones asintóticas | `jupyter lab simulaciones/capitulo3/notebooks/ejemplos_concretos_notaciones.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../familias-de-funciones/">← 3.3 Familias de funciones</a><a class="section-step__index" href="../">Capítulo 3</a><a class="section-step__next" href="../0-comparacion-notaciones-asintoticas/">3.5 Tipos de notación asintótica →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>
