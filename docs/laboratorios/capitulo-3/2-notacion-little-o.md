# Notación o

<span class="chapter-kicker">Capítulo 3</span>

La notación \(o\) se utiliza para mostrar que \(C(n)\) crece **estrictamente más lento** que una función de referencia \(g(n)\). A diferencia de \(O(g(n))\), aquí no basta con que \(C(n)\) esté acotada superiormente por algún múltiplo de \(g(n)\); el cociente entre ambas funciones debe hacerse arbitrariamente pequeño cuando \(n\) crece.

## Definición formal

Para funciones de costo no negativas y una referencia \(g(n)\) positiva a partir de algún tamaño de entrada:

\[
C(n)\in o(g(n))\iff
\forall c>0\;\exists n_0\in\mathbb{R}^{+}\;\forall n\ge n_0:\quad 0\leq C(n)<c\cdot g(n)
\]

Donde:

- **\(n\):** Tamaño de entrada, expresado como un número natural no negativo.
- **\(C(n)\):** Función de costo cuyo crecimiento se estudia.
- **\(g(n)\):** Función de referencia con la que se compara el crecimiento.
- **\(c\):** Constante positiva que escala la referencia para formar una cota superior estricta. La desigualdad debe poder cumplirse para cualquier constante positiva.
- **\(n_0\):** Umbral real positivo desde el que la desigualdad se cumple para todos los tamaños posteriores; puede depender de las constantes elegidas.
- **\(\forall n\ge n_0\):** La condición se mantiene para todo tamaño de entrada a partir del umbral, no solo para un valor aislado.

La condición equivale a que el cociente cumpla:

\[
\lim_{n\to\infty}\frac{C(n)}{g(n)}=0
\]

---

## Ejecutar el laboratorio

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo3/notebooks/2_notacion_little_o.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Simulación interactiva del límite asintótico para notación \(o\) | `jupyter lab simulaciones/capitulo3/notebooks/2_notacion_little_o.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->
