<h1 style="text-align:center;">
  <strong>Capítulo 6: Análisis de algoritmos recursivos</strong>
</h1>

## Correspondencia con el libro

Este README acompaña el Capítulo 6, páginas 219–254. Los cinco ejemplos conservan la secuencia y el propósito del libro; el laboratorio general permite aplicar la metodología a nuevas funciones.

| Libro | Recurso | Simulación |
| :---: | :---: | :---: |
| 6.1–6.3 | Laboratorio de análisis recursivo | [Abrir](./0_laboratorio_analisis_recursivo.ipynb) |
| Adicional | Comparación de Fibonacci | [Abrir](./comparacion_fibonacci.ipynb) |
| Adicional | Ejemplo general de recursión | [Abrir](./ejemplo_recursion.ipynb) |

> **Material adicional del repositorio:** el laboratorio permite construir algoritmos recursivos distintos de los cinco ejemplos impresos y observar por separado el apilamiento, el desapilamiento, el tiempo y el espacio.

---

<h2>🧪 Laboratorios interactivos</h2>

| Laboratorio | Propósito | Simulación |
| :---: | :---: | :---: |
| **Análisis recursivo** | Construye las relaciones temporal y espacial y muestra cómo se apilan las llamadas y se desapilan en orden inverso desde el caso base. | [Abrir](./0_laboratorio_analisis_recursivo.ipynb) |

Los notebooks empleados como apoyo para gráficas estáticas se encuentran en <a href="../runtime/recursos/referencias/"><code>referencias/</code></a>.

---

<h2>🧭 Contenido del capítulo</h2>

<ul>
  <li><a href="#6-1">6.1 Programación recursiva</a></li>
  <li><a href="#6-2">6.2 Análisis temporal y espacial</a>
    <ul>
      <li><a href="#6-2-1">6.2.1 Complejidad temporal</a></li>
      <li><a href="#6-2-2">6.2.2 Complejidad espacial</a></li>
    </ul>
  </li>
  <li><a href="#6-3">6.3 Ejemplos</a>
    <ul>
      <li><a href="#6-3-1">6.3.1 Factorial de un número natural</a></li>
      <li><a href="#6-3-2">6.3.2 Sucesión de Fibonacci</a></li>
      <li><a href="#6-3-3">6.3.3 Potencia de un número entero positivo</a></li>
      <li><a href="#6-3-4">6.3.4 Ordenamiento por mezcla</a></li>
      <li><a href="#6-3-5">6.3.5 Búsqueda en árbol binario</a></li>
    </ul>
  </li>
  <li><a href="#6-4">6.4 Consideraciones finales</a></li>
  <li><a href="#6-4-1">6.4.1 Ejercicios propuestos</a></li>
</ul>

---

<h2 id="6-1">🔁 6.1 Programación recursiva</h2>

<p align="justify">
Un algoritmo es <b>recursivo</b> cuando se llama a sí mismo para resolver instancias más pequeñas del mismo problema. Toda función recursiva correctamente diseñada tiene dos componentes esenciales:
</p>

<ul>
  <li><b>Caso base:</b> la condición que detiene la recursión y devuelve un valor conocido sin realizar una nueva llamada.</li>
  <li><b>Caso recursivo:</b> la reducción del problema hacia el caso base, aplicando la misma función sobre una entrada más pequeña.</li>
</ul>

<p align="justify">
Si el caso base no está bien definido o la reducción no converge hacia él, la función entra en recursión infinita. En términos formales, la función recursiva que calcula el factorial se define como:
</p>

$$
f(n)=
\begin{cases}
1, & \text{si } n\in[0,1],\\
n\,f(n-1), & \text{si } n>1.
\end{cases}
$$

<p align="justify">
Y la sucesión de Fibonacci:
</p>

$$
f(n)=
\begin{cases}
1, & \text{si } n\in[0,1],\\
f(n-1)+f(n-2), & \text{si } n>1.
\end{cases}
$$

---

<h2 id="6-2">⏱️ 6.2 Análisis temporal y espacial</h2>

<p align="justify">
El capítulo introduce una <b>metodología de 4 pasos</b> para construir la relación de recurrencia que modela el costo de un algoritmo recursivo:
</p>

<h3 id="6-2-1">🕐 6.2.1 Complejidad temporal</h3>

<ol>
  <li><b>Caracterizar el caso base:</b> determinar <code>T_base(n)</code>, el costo de ejecutar el algoritmo sin realizar llamadas recursivas.</li>
  <li><b>Sumar las llamadas recursivas:</b> $T_recursivo(n) = Σ aᵢ\cdot Tᵢ(n)$, donde cada término representa una llamada con su coeficiente.</li>
  <li><b>Calcular el costo de las operaciones propias:</b> $f(n) = Σ Tⱼ(n)$, el costo de las instrucciones que no son llamadas recursivas.</li>
  <li><b>Construir la relación completa:</b> $T(n) = T_base(n) + T_recursivo(n) + f(n)$.</li>
</ol>

<h3 id="6-2-2">💾 6.2.2 Complejidad espacial</h3>

<p align="justify">
Para la complejidad espacial, el procedimiento es análogo pero modelando el consumo de la pila de llamadas (<i>call stack</i>):
</p>

<ol>
  <li>Identificar el espacio requerido por el caso base: <code>S_base(n) = s(n)</code>.</li>
  <li>Determinar la profundidad máxima de la recursión: <code>S_recursivo(n) = d(n)</code>.</li>
  <li>Sumar el costo de estructuras auxiliares declaradas en cada llamada: $f(n) = Σ Sⱼ(n)$.</li>
</ol>

<p align="justify">
A diferencia de los algoritmos iterativos, los recursivos consumen espacio proporcional a la profundidad de la pila de llamadas incluso cuando no declaran estructuras de datos adicionales.
</p>

---

<h2 id="6-3">🔬 6.3 Ejemplos</h2>

<h3 id="6-3-1">🔢 6.3.1 Factorial de un número natural</h3>

<p align="justify">
El factorial ilustra el caso más simple de recursión lineal. Su relación de recurrencia es:
</p>

$$
T(n)=
\begin{cases}
1, & \text{si } n\le 1,\\
T(n-1)+1, & \text{si } n>1.
\end{cases}
$$

<p align="justify">
Los tres métodos del Capítulo 5 producen el mismo resultado:
</p>

<ul>
  <li><b>Sustitución iterativa:</b> $T(n) = 1 + 1 + ... + 1$ (n veces) → $T(n) \in \Theta(n)$</li>
  <li><b>Árbol de recurrencia:</b> árbol lineal de profundidad <i>n</i>, costo 1 por nodo → $T(n) \in \Theta(n)$</li>
  <li><b>Ecuación característica:</b> raíz única $r = 1$ → $T(n) \in \Theta(n)$</li>
</ul>

<p align="justify">
La complejidad espacial también es lineal porque la pila de llamadas acumula <i>n</i> marcos activos simultáneamente: $S(n) \in \Theta(n)$.
</p>

| Escenario | $T(n)$ | $S(n)$ |
| :---: | :---: | :---: |
| Todos los casos | $\Theta(n)$ | $\Theta(n)$ |

<h3 id="6-3-2">🌀 6.3.2 Sucesión de Fibonacci</h3>

<p align="justify">
La sucesión de Fibonacci es el ejemplo paradigmático de la <b>explosión exponencial</b> en algoritmos recursivos ingenuos. Su relación de recurrencia es:
</p>

$$
T(n)=
\begin{cases}
1, & \text{si } n\in[0,1],\\
T(n-1)+T(n-2)+1, & \text{si } n>1.
\end{cases}
$$

<p align="justify">
Dado que la ecuación característica exacta produce raíces irracionales, el análisis se realiza en dos niveles:
</p>

<ul>
  <li><b>Cota superior aproximada:</b> aproximando el árbol de recursión por un árbol binario completo de profundidad <i>n</i>, se obtiene $T(n) \in O(2^n)$.</li>
  <li><b>Resultado exacto:</b> la ecuación característica $r^2-r-1=0$ produce la raíz $\varphi = (1+\sqrt{5})/2 \approx 1.618$ (la proporción áurea), dando $T(n) \in \Theta(\varphi^n)$.</li>
</ul>

<p align="justify">
La implementación recursiva directa es <b>exponencialmente ineficiente</b>: recalcula los mismos subproblemas millones de veces. Esta ineficiencia se elimina con técnicas de programación dinámica o memoización, que reducen el costo a $\Theta(n)$.
</p>

| Escenario | $T(n)$ | $S(n)$ |
| :---: | :---: | :---: |
| Todos los casos | $\Theta(\varphi^n)$ ≈ $O(2^n)$ | $\Theta(n)$ |

<h3 id="6-3-3">⚡ 6.3.3 Potencia de un número entero positivo</h3>

<p align="justify">
El cálculo de $b^n$ de forma recursiva puede implementarse de dos maneras con complejidades radicalmente distintas:
</p>

<ul>
  <li><b>Recursión simple:</b> <code>potencia(b, n) = b · potencia(b, n−1)</code>, con caso base <code>potencia(b, 0) = 1</code>. Genera una cadena lineal de <i>n</i> llamadas → $T(n) \in \Theta(n)$, $S(n) \in \Theta(n)$.</li>
  <li><b>Exponenciación rápida:</b> divide el exponente a la mitad en cada paso usando la identidad $b^n=(b^{n/2})^2$. La recurrencia resultante es $T(n)=T(n/2)+1$, cuya solución por el teorema maestro (Caso 2: $a=1$, $b=2$, $k=0$ y $a=b^0=1$) da $T(n)\in\Theta(\log_2 n)$.</li>
</ul>

| Implementación | $T(n)$ | $S(n)$ |
| :---: | :---: | :---: |
| Recursión simple | $\Theta(n)$ | $\Theta(n)$ |
| Exponenciación rápida | $\Theta(\log_2 (n))$ | $\Theta(\log_2 (n))$ |

<h3 id="6-3-4">🔀 6.3.4 Ordenamiento por mezcla</h3>

<p align="justify">
El <i>merge sort</i> es el ejemplo arquetípico de la estrategia <b>divide y vencerás</b> en ordenamiento. El algoritmo divide el arreglo en dos mitades, ordena cada una recursivamente y luego las fusiona en tiempo lineal:
</p>

$$
T(n)=
\begin{cases}
1, & \text{si } n\le 1,\\
2T(n/2)+n, & \text{si } n>1.
\end{cases}
$$

<p align="justify">
Aplicando el <b>teorema maestro básico</b> con $a=2$, $b=2$ y $f(n)\in O(n)$:
</p>

<ul>
  <li>Se compara $a$ con $b^k$: $2=2^1$ → Caso 2 (igualdad)</li>
  <li>Resultado: $T(n) \in \Theta(n\cdot \log_2 (n))$</li>
</ul>

<p align="justify">
La complejidad espacial es lineal porque se requiere un arreglo auxiliar del mismo tamaño para la fase de mezcla: $S(n) \in \Theta(n)$.
</p>

| Escenario | $T(n)$ | $S(n)$ |
| :---: | :---: | :---: |
| Todos los casos | $\Theta(n\,\log_2 (n))$ | $\Theta(n)$ |

<h3 id="6-3-5">🌲 6.3.5 Búsqueda en árbol binario</h3>

<p align="justify">
La búsqueda recursiva en un árbol binario de búsqueda (BST) descarta la mitad de los nodos en cada llamada cuando el árbol está <b>balanceado</b>. La relación de recurrencia en ese caso es:
</p>

$$
T(n)=
\begin{cases}
1, & \text{si } n=0,\\
T(n/2)+1, & \text{si } n>0 \text{ y el árbol está balanceado}.
\end{cases}
$$

<p align="justify">
Esta es la misma recurrencia que la búsqueda binaria sobre arreglos. El teorema maestro (Caso 2 con $a=1, b=2, k=0$) da $T(n) \in \Theta(\log_2 (n))$. Sin embargo, en el <b>peor caso</b> (árbol completamente degenerado, equivalente a una lista enlazada), la búsqueda visita todos los nodos: $T(n) \in O(n)$.
</p>

| Escenario | $T(n)$ | $S(n)$ |
| :---: | :---: | :---: |
| Mejor caso | $\Omega(1)$ | $\Omega(1)$ |
| Caso promedio (balanceado) | $\Theta(\log_2 (n))$ | $\Theta(\log_2 (n))$ |
| Peor caso (degenerado) | $O(n)$ | $O(n)$ |

---

<h2>📊 Resumen de complejidades</h2>

| Algoritmo | Recurrencia | $T(n)$ | $S(n)$ | Método de resolución |
| :---: | :---: | :---: | :---: | :---: |
| Factorial | `$T(n)$=T(n−1)+1` | $\Theta(n)$ | $\Theta(n)$ | Sustitución, árbol, ec. característica |
| Fibonacci (naïve) | `$T(n)$=T(n−1)+T(n−2)+1` | $\Theta(\varphi^n)$ | $\Theta(n)$ | Ecuación característica |
| Potencia simple | `$T(n)$=T(n−1)+1` | $\Theta(n)$ | $\Theta(n)$ | Sustitución iterativa |
| Potencia rápida | `$T(n)$=T(n/2)+1` | $\Theta(\log_2 (n))$ | $\Theta(\log_2 (n))$ | Teorema maestro (Caso 2) |
| Merge sort | `$T(n)$=2T(n/2)+n` | $\Theta(n\,\log_2 (n))$ | $\Theta(n)$ | Teorema maestro (Caso 2) |
| BST (balanceado) | `$T(n)$=T(n/2)+1` | $\Theta(\log_2 (n))$ | $\Theta(\log_2 (n))$ | Teorema maestro (Caso 2) |

---

<h2 id="6-4">💡 6.4 Consideraciones finales</h2>

<p align="justify">
El análisis de algoritmos recursivos pone en evidencia una tensión fundamental: la elegancia y claridad del código recursivo suelen contrastar con un mayor consumo de recursos. La pila de llamadas introduce un costo espacial implícito que los algoritmos iterativos no tienen. Esta observación es central al escoger entre implementaciones recursivas e iterativas de un mismo problema.
</p>

<p align="justify">
Asimismo, el capítulo subraya que identificar correctamente el tipo de relación de recurrencia (reducción, división o mixta) es el paso más crítico del análisis, pues determina qué método de resolución aplicar y qué comportamiento asintótico esperar.
</p>

---

<h2 id="6-4-1">📚 6.4.1 Ejercicios propuestos</h2>

<p align="justify">
El capítulo incluye <b>8 ejercicios propuestos</b> para consolidar la metodología de análisis sobre algoritmos recursivos reales:
</p>

<ol>
  <li>Búsqueda binaria recursiva</li>
  <li>Máximo común divisor (MCD – Algoritmo de Euclides)</li>
  <li>Cálculo de combinaciones C(n, k)</li>
  <li>Suma de los elementos de un arreglo</li>
  <li>Torre de Hanói</li>
  <li>Inversión de una cadena de caracteres</li>
  <li>Suma de los dígitos de un número</li>
  <li>Verificación de número primo</li>
</ol>

<p align="justify">
Para cada ejercicio se pide construir la relación de recurrencia, seleccionar el método de solución más adecuado y derivar la complejidad temporal y espacial en los casos mejor, peor y promedio.
</p>

---

<h2>🧾 Licencia</h2>

<div style="border-left:4px solid #999; padding:1em; background-color:#fafafa; border-radius:6px;">
<p style="text-align:justify; color:#333;">
El contenido de este capítulo se distribuye bajo la licencia
<b>Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)</b>.
Se autoriza su uso con fines académicos citando la fuente original.
</p>
<p style="text-align:center; font-weight:600; margin-top:0.5em;">
© 2026 Carlos Eduardo Orozco Garcés, César Jesús Pardo Calvache, Mauro Callejas Cuervo
</p>
</div>
