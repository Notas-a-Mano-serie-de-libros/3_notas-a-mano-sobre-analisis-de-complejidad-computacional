# Recurrencias y análisis de complejidad

<span class="chapter-kicker">Capítulo 5</span>

A continuación, se presentan las relaciones de recurrencia más comunes que surgen en los algoritmos recursivos clásicos.

Donde:

- **\(C(n)\):** Función de complejidad asociada con el problema de tamaño \(n\).
- **\(a_i\):** Cantidad de subproblemas asociados al término recursivo \(i\).
- **\(b_i\):** Reducción aplicada al problema en el término recursivo \(i\).
- **\(m\):** Cantidad de términos distintos que conforman la relación.
- **\(f(n)\):** Costo de las operaciones realizadas en cada llamada, fuera de las llamadas recursivas.

## Relaciones de reducción

El tamaño del problema disminuye en una cantidad fija en cada llamada recursiva:

\[
C(n)=\left[\sum_{i=1}^{m}a_i\cdot C(n-b_i)\right]+f(n)\qquad\text{donde:}\quad
\begin{cases}
n,m\in\mathbb{N},\quad m\geq 1 \\
a_i\in\mathbb{R}^{+},\quad b_i\in\mathbb{N}^{+}
\end{cases}
\]

## Relaciones de división

El problema se descompone en subproblemas cuyos tamaños son fracciones del tamaño original:

\[
C(n)=\left[\sum_{i=1}^{m}a_i\cdot C(b_i\cdot n)\right]+f(n)\qquad\text{donde:}\quad
\begin{cases}
n,m\in\mathbb{N},\quad m\geq 1 \\
a_i,b_i\in\mathbb{R}^{+},\quad 0<b_i<1
\end{cases}
\]

## Caso particular: un solo término recursivo

Muchos problemas recursivos clásicos contienen un único término recursivo distinto, es decir, \(m=1\). En ese caso, la sumatoria contiene únicamente el término \(i=1\). Al escribir \(a=a_1\) y \(b=b_1\), se obtienen los dos casos particulares:

\[
\begin{aligned}
C(n)&=\sum_{i=1}^{1}a_i\cdot C(n-b_i)+f(n)
     =a\cdot C(n-b)+f(n) &&\text{(reducción simple)} \\
C(n)&=\sum_{i=1}^{1}a_i\cdot C(b_i\cdot n)+f(n)
     =a\cdot C(b\cdot n)+f(n) &&\text{(división simple)}
\end{aligned}
\]

Un solo término distinto no implica una sola llamada: la multiplicidad \(a\) determina cuántos subproblemas del mismo tamaño genera cada nodo.

Para representar su árbol:

- **\(n_k\):** Tamaño de cada subproblema en el nivel \(k\), tomando la raíz como nivel cero.
- **\(h\):** Profundidad total del árbol hasta alcanzar el caso base.
- **\(f(n_k)\):** Costo local de cada nodo del nivel \(k\). Si todos los nodos de ese nivel tienen el mismo tamaño, su costo conjunto es \(a^k\cdot f(n_k)\).

\[
\begin{aligned}
n_k&=n-k\cdot b &&\text{(reducción)} \\
n_k&=n\cdot b^k &&\text{(división)}
\end{aligned}
\]

## Multiplicidad y árbol asociado

Para interpretar \(a\) como número de hijos, se consideran multiplicidades enteras positivas. Las figuras siguientes ilustran la división por dos; la cantidad de hijos depende de \(a\), mientras que el tamaño de cada hijo depende del factor de reducción.

- **Cuando \(a=1\):** Cada llamada genera un único subproblema. El árbol es **degenerado**: se comporta como una lista simple y tiene un nodo por nivel.

    \[
    N_k=1^k=1
    \]

    <figure class="recurrence-tree-figure"><img src="../../../assets/images/capitulo-5/arbol_recurrencia_a1.png" alt="Árbol degenerado con un hijo por nodo"><figcaption>Árbol de recurrencia (\(a=1\)).</figcaption></figure>

- **Cuando \(a=2\):** Cada problema genera dos subproblemas del mismo tamaño, dando lugar a un **árbol binario balanceado** cuando todas las ramas siguen la misma reducción y el mismo caso base. El número de nodos se duplica en cada nivel.

    \[
    N_k=2^k
    \]

    <figure class="recurrence-tree-figure"><img src="../../../assets/images/capitulo-5/arbol_recurrencia_a2.png" alt="Árbol binario con dos hijos por nodo"><figcaption>Árbol de recurrencia (\(a=2\)).</figcaption></figure>

- **Cuando \(a=k\):** Cada nodo genera \(k\) subproblemas y forma un **árbol \(k\)-nario**. Para distinguir la cantidad de hijos del índice de nivel, se utiliza \(\ell\) para el nivel en esta expresión:

    \[
    N_\ell=k^\ell
    \]

    Si \(k>1\), el número de nodos por nivel crece exponencialmente con la profundidad. La figura ilustra el caso particular de cuatro hijos por nodo.

    <figure class="recurrence-tree-figure"><img src="../../../assets/images/capitulo-5/arbol_recurrencia_a4.png" alt="Árbol de cuatro hijos como ejemplo de árbol k-nario"><figcaption>Árbol de recurrencia (\(a=k\)).</figcaption></figure>

## Más de un término recursivo

Las relaciones con \(m=1\) permiten representar un patrón uniforme. Con \(m>1\), distintos factores de reducción pueden producir ramas que alcanzan el caso base en profundidades diferentes. Por ejemplo:

\[
C(n)=C\!\left(\frac{n}{2}\right)+2\cdot C\!\left(\frac{n}{3}\right)+1\qquad\text{donde:}\quad
\begin{cases}
a_1=1,\quad a_2=2 \\
b_1=1/2,\quad b_2=1/3
\end{cases}
\]

Cada nodo genera un subproblema de tamaño \(n/2\) y dos de tamaño \(n/3\). Si se sigue sucesivamente el primer tipo de rama, el tamaño en el nivel \(k\) es \(n/2^k\); si se sigue el segundo, es \(n/3^k\). Las rutas que combinan ambos tipos tienen otros tamaños, por lo que no existe un único tamaño común para todos los nodos de un nivel.

El árbol puede ser desbalanceado y no uniforme. Su representación ayuda a visualizar la recurrencia, pero el costo de cada nivel exige sumar los costos de sus distintos subproblemas.

---

## Ejecutar el laboratorio

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo5/notebooks/0_arboles_recursion.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Recurrencias y análisis de complejidad | `jupyter lab simulaciones/capitulo5/notebooks/0_arboles_recursion.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->
