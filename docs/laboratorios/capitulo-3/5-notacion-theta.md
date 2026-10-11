# Notación \Theta

<span class="chapter-kicker">Capítulo 3</span>

La notación \(\Theta\) define la familia de funciones que están acotadas simultáneamente por abajo y por arriba mediante múltiplos constantes de una misma función de referencia. Su propósito es establecer una **cota ajustada** sobre el crecimiento de \(C(n)\), ignorando constantes y términos de menor orden.

## Definición formal

Para funciones de costo no negativas y una referencia \(g(n)\) positiva a partir de algún tamaño de entrada:

\[
C(n)\in \Theta(g(n))\iff
\exists c_1,c_2>0\;\exists n_0\in\mathbb{R}^{+}\;\forall n\ge n_0:\quad 0\leq c_1\cdot g(n)\leq C(n)\leq c_2\cdot g(n)
\]

Donde:

- **\(n\):** Tamaño de entrada, expresado como un número natural no negativo.
- **\(C(n)\):** Función de costo cuyo crecimiento se estudia.
- **\(g(n)\):** Función de referencia con la que se compara el crecimiento.
- **\(c_1,c_2\):** Constantes positivas que escalan la referencia para formar la cota inferior y la superior. Basta con encontrar un par válido.
- **\(n_0\):** Umbral real positivo desde el que la desigualdad se cumple para todos los tamaños posteriores; puede depender de las constantes elegidas.
- **\(\forall n\ge n_0\):** La condición se mantiene para todo tamaño de entrada a partir del umbral, no solo para un valor aislado.

## Por qué no existe una notación little-theta

La notación \(\Theta\) combina una cota superior y una inferior del mismo orden:

\[
\Theta(g(n))=O(g(n))\cap\Omega(g(n))
\]

Una versión little-theta análoga tendría que combinar las dos relaciones estrictas: crecer estrictamente más lento y, a la vez, estrictamente más rápido que la misma referencia. Sin embargo, estas condiciones son incompatibles.

**Demostración por contradicción.** Supongamos que existe una función \(C(n)\) que pertenece a ambas familias:

\[
C(n)\in o(g(n))\cap\omega(g(n))
\]

Por la definición de \(o\), tomando la constante positiva \(c=1\), existe un umbral \(n_1\) tal que:

\[
C(n)<g(n)\quad\forall n\ge n_1
\]

Por la definición de \(\omega\), tomando también \(c=1\), existe un umbral \(n_2\) tal que:

\[
C(n)>g(n)\quad\forall n\ge n_2
\]

Para cualquier tamaño de entrada a partir de \(\max\{n_1,n_2\}\), ambas desigualdades tendrían que cumplirse simultáneamente:

\[
g(n)<C(n)<g(n)
\]

Esto es una contradicción. Por tanto:

\[
o(g(n))\cap\omega(g(n))=\varnothing
\]

También se observa al comparar los límites exigidos por cada notación: el mismo cociente no puede tender simultáneamente a cero y a infinito.

\[
\begin{cases}
\displaystyle\lim_{n\to\infty}\frac{C(n)}{g(n)}=0 & \text{si }C(n)\in o(g(n)) \\
\displaystyle\lim_{n\to\infty}\frac{C(n)}{g(n)}=+\infty & \text{si }C(n)\in\omega(g(n))
\end{cases}
\]

Por eso no se utiliza una notación little-theta como contraparte de \(\Theta\). Cambiar únicamente las desigualdades de \(\Theta\) por desigualdades estrictas, manteniendo la existencia de las constantes, tampoco crea una nueva familia: cualquier cota de \(\Theta\) puede hacerse estricta reduciendo la constante inferior y aumentando la superior.

---

## Ejecutar el laboratorio

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo3/notebooks/5_notacion_theta.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Simulación interactiva del límite asintótico para notación \(\Theta\) | `jupyter lab simulaciones/capitulo3/notebooks/5_notacion_theta.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->
