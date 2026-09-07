# Simulación interactiva del límite asintótico para notación \(\Omega\)

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 3</span>

La notación \(\Omega\) se utiliza para mostrar que \(C(n)\) crece **al mismo ritmo o más rápido** que una función de referencia \(g(n)\). En este caso, \(g(n)\) actúa como una cota inferior asintótica para \(C(n)\), ignorando constantes multiplicativas y términos de menor orden.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/notebooks/3_notacion_big_omega.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

Formalmente, se analiza el cociente mediante el límite inferior:

\[
k=\liminf_{n\to\infty}\left(\frac{C(n)}{g(n)}\right), \qquad k\in\mathbb{R}^+
\]

Si este valor converge a una constante estrictamente positiva, entonces existe al menos una constante \(c\) que satisface:

\[
C(n)\ge c\cdot g(n)
\]

Cuando el cociente converge a \(k\), una elección válida para la constante debe cumplir:

\[
0\lt c\le k
\]

Finalmente, \(n_0\) se obtiene seleccionando un valor del conjunto de posibles umbrales asociados a un valor específico de \(c\):

\[
n_0\in\mathbb{R}^{+}: C(n)\ge c\cdot g(n)\qquad \forall n\ge n_0
\]

La simulación permite modificar las funciones, el intervalo visible, la constante y la escala. También permite arrastrar la línea de \(n_0\) para seleccionar cualquier umbral válido del intervalo solución.
