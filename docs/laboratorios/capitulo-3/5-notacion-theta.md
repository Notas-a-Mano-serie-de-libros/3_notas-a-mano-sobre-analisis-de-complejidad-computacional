# Simulación interactiva del límite asintótico para notación \(\Theta\)

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 3</span>

La notación \(\Theta\) define la familia de funciones que están acotadas simultáneamente por abajo y por arriba mediante múltiplos constantes de una misma función de referencia. Su propósito es establecer una **cota ajustada** sobre el crecimiento de \(C(n)\), ignorando constantes y términos de menor orden.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/notebooks/5_notacion_theta.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

Formalmente, una función \(C(n)\) pertenece a \(\Theta(g(n))\) si existen constantes positivas \(c_1\) y \(c_2\) tales que:

\[
c_1\cdot g(n)\le C(n)\le c_2\cdot g(n), \qquad \forall n\ge n_0
\]

Esta definición combina simultáneamente las ideas de cota inferior y cota superior:

\[
C(n)\in\Theta(g(n))\Longleftrightarrow C(n)\in\Omega(g(n))\land C(n)\in O(g(n))
\]

Si el cociente entre \(C(n)\) y \(g(n)\) converge a una constante positiva \(k\), entonces las constantes deben elegirse de forma que \(C(n)\) quede atrapada entre ambas cotas:

\[
0\lt c_1\le k\le c_2
\]

El valor de \(n_0\) se obtiene al seleccionar un elemento de la intersección de los intervalos que satisfacen ambas desigualdades:

\[
n_0\in\mathbb{R}^{+}: c_1\cdot g(n)\le C(n)\le c_2\cdot g(n)\qquad \forall n\ge n_0
\]

La simulación permite modificar \(C(n)\), \(g(n)\), \(c_1\), \(c_2\), el intervalo visible y la escala. También permite arrastrar la línea de \(n_0\) para seleccionar cualquier umbral válido de la intersección calculada.
