# Notacion Asintotica Representacion Generica

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 3</span>

### Notación \(O\)

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/notebooks/notacion_asintotica_representacion_generica.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

La notación \(O\) se utiliza para describir una **cota superior asintótica** para una función de interés. En análisis de algoritmos, esto permite establecer una referencia que crece al menos tan rápido como la función \(C(n)\) cuando el tamaño de la entrada es suficientemente grande. Por esta razón, suele emplearse para caracterizar el comportamiento en el **peor de los casos**.

Formalmente, una función \(C(n)\) pertenece a la clase \(O(g(n))\) si existe una constante positiva \(c\) y un valor \(n_0\) tales que:

\[
C(n) \in O(g(n)) \iff \exists c \in \mathbb{R}^{+} : C(n) \leq c \cdot g(n) \quad \forall n \geq n_0,\; n_0 \in \mathbb{Z}_0^{+}
\]

Donde:

- \(n\): tamaño de la entrada.
- \(C(n)\): función de complejidad de interés.
- \(g(n)\): función de referencia que describe el orden general de crecimiento.
- \(c\): constante positiva que escala a \(g(n)\) para que actúe como cota superior.
- \(n_0\): punto a partir del cual la desigualdad siempre se cumple.

En la representación genérica, la idea central es que el comportamiento previo a \(n_0\) no determina la notación. Las curvas pueden cruzarse, oscilar o crecer de forma distinta para valores pequeños de \(n\); sin embargo, a partir de \(n_0\), la función de referencia escalada \(c \cdot g(n)\) queda por encima de \(C(n)\) y mantiene esa relación de forma permanente.

### Notación \(\Omega\)

La notación \(\Omega\) se utiliza para describir una **cota inferior asintótica** de una función de interés. Su propósito es establecer una referencia que siempre quede por debajo de \(C(n)\) cuando \(n\) es suficientemente grande. En el contexto de algoritmos, esta notación suele asociarse con el comportamiento en el **mejor de los casos**.

Formalmente, una función \(C(n)\) pertenece a la clase \(\Omega(g(n))\) si existe una constante positiva \(c\) y un valor \(n_0\) tales que:

\[
C(n) \in \Omega(g(n)) \iff \exists c \in \mathbb{R}^{+} : C(n) \geq c \cdot g(n) \quad \forall n \geq n_0,\; n_0 \in \mathbb{Z}_0^{+}
\]

Donde:

- \(n\): tamaño de la entrada.
- \(C(n)\): función de complejidad de interés.
- \(g(n)\): función de referencia utilizada para comparar el crecimiento general.
- \(c\): constante positiva que ajusta la escala de \(g(n)\) para que funcione como cota inferior.
- \(n_0\): punto a partir del cual la desigualdad permanece siempre satisfecha.

Gráficamente, la representación genérica busca mostrar que lo importante no es cómo se comportan las curvas antes de \(n_0\), sino que, a partir de ese punto, la función \(C(n)\) quede por encima de la referencia escalada \(c \cdot g(n)\). En otras palabras, la función de interés crece al menos tan rápido como la referencia elegida cuando \(n\) tiende a infinito.

### Notación \(\Theta\)

La notación \(\Theta\) se utiliza cuando se desea establecer una **cota ajustada** para una función. A diferencia de las notaciones \(O\) y \(\Omega\), que consideran solo una dirección del crecimiento, la notación \(\Theta\) exige que la función de interés quede simultáneamente acotada por arriba y por abajo por múltiplos de una misma función de referencia. Por ello, suele interpretarse como una descripción del comportamiento **más representativo o más probable** de un algoritmo.

Formalmente, una función \(C(n)\) pertenece a la clase \(\Theta(g(n))\) si existen dos constantes positivas \(c_1\), \(c_2\) y un valor \(n_0\) tales que:

\[
C(n) \in \Theta(g(n)) \iff \exists (c_1, c_2) \in \mathbb{R}^{+} : c_1 \cdot g(n) \leq C(n) \leq c_2 \cdot g(n) \quad \forall n \geq n_0,\; n_0 \in \mathbb{Z}_0^{+}
\]

Esta definición puede leerse también como la combinación de una cota inferior y una cota superior:

\[
C(n) \in \Theta(g(n)) \iff C(n) \in \Omega(g(n)) \; \wedge \; C(n) \in O(g(n))
\]

Donde:

- \(n\): tamaño de la entrada.
- \(C(n)\): función de complejidad que se desea acotar.
- \(g(n)\): función de referencia con la que se compara el crecimiento.
- \(c_1, c_2\): constantes positivas que establecen, respectivamente, la cota inferior y la cota superior.
- \(n_0\): punto a partir del cual ambas desigualdades se cumplen al mismo tiempo.

En la representación genérica, esto significa que antes de \(n_0\) las curvas pueden no respetar todavía la relación deseada, pero para valores suficientemente grandes de \(n\), la función \(C(n)\) queda contenida entre \(c_1 \cdot g(n)\) y \(c_2 \cdot g(n)\). Esa es precisamente la razón por la que la región sombreada entre ambas referencias resulta útil para visualizar la idea de acotación doble.
