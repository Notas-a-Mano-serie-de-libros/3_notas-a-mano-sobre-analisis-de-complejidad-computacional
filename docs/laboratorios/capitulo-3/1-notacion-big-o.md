# Simulación interactiva del límite asintótico para notación \(O\)

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 3</span>

La notación \(O\) se utiliza para mostrar que \(C(n)\) crece **al mismo ritmo o más lento** que una función de referencia \(g(n)\). En otras palabras, para valores suficientemente grandes de \(n\), la función \(g(n)\) permite construir una cota superior para \(C(n)\), ignorando constantes multiplicativas y términos de menor orden.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/notebooks/1_notacion_big_o.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

Formalmente, se analiza el cociente entre ambas funciones mediante el límite superior:

\[
k=\limsup_{n\to\infty}\left(\frac{C(n)}{g(n)}\right), \qquad k\in\mathbb{R}_0^+
\]

Si este valor es finito, entonces existe al menos una constante \(c\) que satisface la desigualdad:

\[
C(n)\le c\cdot g(n)
\]

Cuando el cociente converge a una constante positiva \(k\), una elección válida para la constante debe cumplir:

\[
c\gt k
\]

Finalmente, \(n_0\) se obtiene seleccionando un valor del conjunto de posibles umbrales asociados a un valor específico de \(c\):

\[
n_0\in\mathbb{R}^{+}: C(n)\le c\cdot g(n)\qquad \forall n\ge n_0
\]

La simulación permite modificar \(C(n)\), \(g(n)\), el intervalo visible, la constante \(c\) y la escala de la gráfica. También permite arrastrar la línea de \(n_0\) para seleccionar cualquier umbral válido del intervalo solución.
