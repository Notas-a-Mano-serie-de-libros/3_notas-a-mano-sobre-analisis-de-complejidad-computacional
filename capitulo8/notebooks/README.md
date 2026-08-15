<h1 style="text-align:center;">
  <strong>Capítulo 8: Análisis de algoritmos de ordenamiento clásicos</strong>
</h1>

## Correspondencia con el libro

Este README sigue el Capítulo 8, páginas 313–366. Los seis algoritmos impresos tienen un notebook propio. Shell Sort, el comparador y el laboratorio de ejercicios se presentan como ampliaciones.

| Libro | Recurso | Simulación |
| :---: | :---: | :---: |
| 8.2 | Ordenamiento burbuja | [Abrir](./1_ordenamiento_burbuja.ipynb) |
| 8.3 | Ordenamiento por selección | [Abrir](./2_ordenamiento_seleccion.ipynb) |
| 8.4 | Ordenamiento por inserción | [Abrir](./3_ordenamiento_insercion.ipynb) |
| 8.5 | Ordenamiento por mezcla | [Abrir](./5_ordenamiento_mezcla.ipynb) |
| 8.6 | Ordenamiento rápido | [Abrir](./6_ordenamiento_rapido.ipynb) |
| 8.7 | Ordenamiento Radix | [Abrir](./7_ordenamiento_radix.ipynb) |
| Adicional | Shell Sort | [Abrir](./4_ordenamiento_shell.ipynb) |
| Adicional | Comparación de ordenamientos | [Abrir](./0_comparacion_ordenamientos.ipynb) |
| 8.9 | Ejercicios propuestos | [Abrir](./ejercicios_propuestos.ipynb) |

> **Material adicional del repositorio:** Shell Sort, las comparaciones experimentales, las proyecciones y las soluciones amplían el contenido publicado sin alterar la secuencia del capítulo.

---

<h2>🧭 Contenido del capítulo</h2>

<ul>
  <li><a href="#8-1">8.1 Consideraciones previas</a></li>
  <li><a href="#8-2">8.2 Ordenamiento burbuja</a>
    <ul>
      <li>🎬 <a href="./1_ordenamiento_burbuja.ipynb">Animación interactiva – Ordenamiento burbuja</a></li>
    </ul>
  </li>
  <li><a href="#8-3">8.3 Ordenamiento por selección</a>
    <ul>
      <li>🎬 <a href="./2_ordenamiento_seleccion.ipynb">Animación interactiva – Ordenamiento por selección</a></li>
    </ul>
  </li>
  <li><a href="#8-4">8.4 Ordenamiento por inserción</a>
    <ul>
      <li>🎬 <a href="./3_ordenamiento_insercion.ipynb">Animación interactiva – Ordenamiento por inserción</a></li>
    </ul>
  </li>
  <li><a href="#8-5">8.5 Ordenamiento por mezcla</a>
    <ul>
      <li>🎬 <a href="./5_ordenamiento_mezcla.ipynb">Animación interactiva – Ordenamiento por mezcla</a></li>
    </ul>
  </li>
  <li><a href="#8-6">8.6 Ordenamiento rápido</a>
    <ul>
      <li>🎬 <a href="./6_ordenamiento_rapido.ipynb">Animación interactiva – Ordenamiento rápido</a></li>
    </ul>
  </li>
  <li><a href="#8-7">8.7 Ordenamiento radix</a>
    <ul>
      <li>🎬 <a href="./7_ordenamiento_radix.ipynb">Animación interactiva – Ordenamiento radix</a></li>
    </ul>
  </li>
  <li><a href="#8-shell">Material adicional: Shell Sort</a>
    <ul>
      <li>🎬 <a href="./4_ordenamiento_shell.ipynb">Animación interactiva – Shell Sort</a></li>
    </ul>
  </li>
  <li><a href="#8-comp">📊 Comparación de todos los algoritmos</a>
    <ul>
      <li>🎬 <a href="./0_comparacion_ordenamientos.ipynb">Comparación interactiva – Todos los algoritmos</a></li>
    </ul>
  </li>
  <li><a href="#8-8">8.8 Consideraciones finales</a></li>
  <li><a href="#8-9">8.9 Ejercicios propuestos</a></li>
</ul>

---

<h2 id="8-1">⚙️ 8.1 Consideraciones previas</h2>

<p align="justify">
Este capítulo aplica las herramientas desarrolladas en los capítulos anteriores —funciones de complejidad, notación asintótica, relaciones de recurrencia y análisis de algoritmos recursivos— al estudio de los algoritmos de ordenamiento más utilizados en la práctica. El ordenamiento es una de las operaciones más frecuentes en informática y la elección del algoritmo correcto tiene un impacto directo en el rendimiento de los sistemas.
</p>

<p align="justify">
El libro estudia seis algoritmos: tres de comportamiento cuadrático en sus casos promedio o peor (burbuja, selección e inserción), dos de comportamiento log-lineal en sus casos habituales (mezcla y rápido) y Radix, cuyo costo depende de la cantidad de elementos y dígitos procesados. El repositorio añade Shell Sort como ampliación.
</p>

<p align="justify">
Las animaciones utilizan dos modos de visualización intercambiables: representación con <b>cajas</b> (para seguir el valor de cada elemento) y representación con <b>barras</b> (para observar visualmente la evolución del ordenamiento). Los controles permiten elegir el <b>orden</b> (ascendente o descendente) y, en el caso del ordenamiento rápido, la <b>estrategia de selección del pivote</b>.
</p>

---

<h2 id="8-2">🫧 8.2 Ordenamiento burbuja</h2>

<p align="center">
  🎬 <a href="./1_ordenamiento_burbuja.ipynb"><b>Abrir simulación</b></a>
</p>

<p align="justify">
El <b>ordenamiento burbuja</b> recorre repetidamente el arreglo comparando pares de elementos adyacentes e intercambiándolos si están en el orden incorrecto. En cada pasada, el elemento más grande "burbujea" hasta su posición final al final del arreglo. Tras <i>n−1</i> pasadas, el arreglo queda ordenado.
</p>

<h3>Descripción del algoritmo</h3>
<p align="justify">
Se implementan dos ciclos anidados: el externo controla el número de pasadas (de 0 a n−2) y el interno realiza las comparaciones e intercambios (de 0 a n−2−i). Cada pasada garantiza que al menos el elemento más grande del subarreglo activo quede en su posición definitiva.
</p>

<h3>Análisis de complejidad</h3>

<p align="justify">
El número de comparaciones en la pasada <i>i</i>-ésima es <code>n−1−i</code>. Sumando para todas las pasadas: $Σᵢ₌₀^n⁻^2 (n-1-i) = n(n-1)/2$.
</p>

| Escenario | $T(n)$ | $S(n)$ | Descripción |
| :---: | :---: | :---: | :---: |
| **Mejor caso** | $\Omega(n)$ | $\Omega(1)$ | Arreglo ya ordenado (con optimización de bandera) |
| **Caso promedio** | $\Theta(n^2)$ | $\Theta(1)$ | $\frac{n^2}{2}$ comparaciones en promedio |
| **Peor caso** | $O(n^2)$ | $O(1)$ | Arreglo ordenado en orden inverso: $\frac{n(n-1)}{2}$ comparaciones |

<h3>Ventajas y desventajas</h3>

| Ventajas | Desventajas |
| :---: | :---: |
| Implementación simple y comprensible | Ineficiente para arreglos grandes |
| Ordenamiento <i>in-place</i> ($O(1)$ espacio adicional) | Alto número de intercambios comparado con otros métodos cuadráticos |
| Estable: preserva el orden relativo de elementos iguales | Desempeño consistentemente pobre en datos desordenados |

---

<h2 id="8-3">🎯 8.3 Ordenamiento por selección</h2>

<p align="center">
  🎬 <a href="./2_ordenamiento_seleccion.ipynb"><b>Abrir simulación</b></a>
</p>

<p align="justify">
El <b>ordenamiento por selección</b> divide el arreglo en dos partes: la porción ordenada (inicialmente vacía) y la porción no ordenada. En cada pasada selecciona el elemento mínimo de la porción no ordenada y lo intercambia con el primer elemento de dicha porción, ampliando la parte ordenada en una posición.
</p>

<h3>Análisis de complejidad</h3>

<p align="justify">
El número de comparaciones es siempre <code>n(n−1)/2</code> independientemente del estado inicial del arreglo, porque siempre debe recorrer toda la porción no ordenada para encontrar el mínimo. El número de intercambios es a lo sumo <i>n−1</i>.
</p>

| Escenario | $T(n)$ | $S(n)$ | Descripción |
| :---: | :---: | :---: | :---: |
| **Todos los casos** | $\Theta(n^2)$ | $\Theta(1)$ | $\frac{n(n-1)}{2}$ comparaciones en cualquier escenario; la disposición inicial no afecta el costo |

<h3>Ventajas y desventajas</h3>

| Ventajas | Desventajas |
| :---: | :---: |
| Número mínimo de intercambios: a lo sumo n−1 | Costo siempre cuadrático, no mejora con datos casi ordenados |
| Útil cuando el costo de los intercambios supera al de las comparaciones | No es estable en la implementación estándar |

---

<h2 id="8-4">🃏 8.4 Ordenamiento por inserción</h2>

<p align="center">
  🎬 <a href="./3_ordenamiento_insercion.ipynb"><b>Abrir simulación</b></a>
</p>

<p align="justify">
El <b>ordenamiento por inserción</b> construye el arreglo ordenado de izquierda a derecha, insertando cada nuevo elemento en su posición correcta dentro de la porción ya ordenada. Es la estrategia que usa intuitivamente un jugador de cartas al ordenar su mano.
</p>

<h3>Análisis de complejidad</h3>

<p align="justify">
En el mejor caso (arreglo ya ordenado), cada elemento solo requiere una comparación: $T(n)\in\Omega(n)$. En el caso promedio, el elemento se inserta en la posición media de la porción ordenada, dando $n^2/4$ comparaciones. En el peor caso (orden inverso), cada elemento se mueve hasta el inicio: $n(n-1)/2$ comparaciones.
</p>

| Escenario | $T(n)$ | $S(n)$ | Descripción |
| :---: | :---: | :---: | :---: |
| **Mejor caso** | $\Omega(n)$ | $\Omega(1)$ | Arreglo ya ordenado: solo $n-1$ comparaciones |
| **Caso promedio** | $\Theta(n^2)$ | $\Theta(1)$ | $\frac{n^2}{4}$ comparaciones en promedio |
| **Peor caso** | $O(n^2)$ | $O(1)$ | Arreglo en orden inverso: $\frac{n(n-1)}{2}$ comparaciones |

<h3>Ventajas y desventajas</h3>

| Ventajas | Desventajas |
| :---: | :---: |
| Eficiente para arreglos pequeños y casi ordenados | Cuadrático en el caso general |
| Estable y <i>in-place</i> | Muchos desplazamientos en el peor caso |
| Útil como paso final en algoritmos híbridos (ej. Timsort) | No escala bien para n grande |

---

<h2 id="8-5">🔀 8.5 Ordenamiento por mezcla</h2>

<p align="center">
  🎬 <a href="./5_ordenamiento_mezcla.ipynb"><b>Abrir simulación</b></a>
</p>

<p align="justify">
El <b>ordenamiento por mezcla</b> (merge sort) es un algoritmo <b>divide y vencerás</b>: divide el arreglo en dos mitades, ordena cada mitad recursivamente y luego las fusiona en una sola secuencia ordenada. Es el algoritmo de ordenamiento cuyo análisis se estudia en el Capítulo 6 como ejemplo de recurrencia de división.
</p>

<h3>Relación de recurrencia</h3>
$$
T(n)=
\begin{cases}
1, & \text{si } n\le 1,\\
2T(n/2)+n, & \text{si } n>1.
\end{cases}
$$

<p align="justify">
Aplicando el <b>teorema maestro básico</b> con $a=2$, $b=2$ y $f(n)\in O(n)$, se cumple $a=b^k$ (Caso 2); por tanto, $T(n)\in\Theta(n\log_2 n)$.
</p>

<h3>Análisis de complejidad</h3>

| Escenario | $T(n)$ | $S(n)$ | Descripción |
| :---: | :---: | :---: | :---: |
| **Todos los casos** | $\Theta(n\,\log_2 (n))$ | $\Theta(n)$ | La división y mezcla ocurren siempre en el mismo número de pasos, independientemente de los datos |

<h3>Ventajas y desventajas</h3>

| Ventajas | Desventajas |
| :---: | :---: |
| Complejidad $\Theta(n\log n)$ garantizada en todos los casos | Requiere $O(n)$ de memoria adicional para la fase de mezcla |
| Estable: preserva el orden relativo de elementos iguales | No es <i>in-place</i> en la implementación estándar |
| Paralelizable: las dos mitades se pueden ordenar de forma independiente | Mayor constante multiplicativa que quicksort en la práctica |

---

<h2 id="8-6">⚡ 8.6 Ordenamiento rápido</h2>

<p align="center">
  🎬 <a href="./6_ordenamiento_rapido.ipynb"><b>Abrir simulación</b></a>
</p>

<p align="justify">
El <b>ordenamiento rápido</b> (quicksort) es otro algoritmo divide y vencerás. Selecciona un elemento denominado <b>pivote</b>, reordena el arreglo de modo que todos los elementos menores al pivote queden a su izquierda y los mayores a su derecha (<i>partición</i>), y luego aplica el mismo proceso recursivamente sobre cada subpartición.
</p>

<h3>Estrategias de selección del pivote</h3>
<ul>
  <li><b>Primer elemento:</b> simple pero susceptible al peor caso con arreglos ya ordenados.</li>
  <li><b>Último elemento:</b> análogo al anterior.</li>
  <li><b>Elemento central:</b> reduce la probabilidad del peor caso.</li>
  <li><b>Mediana de tres:</b> selecciona la mediana entre el primero, el central y el último; mejor rendimiento promedio.</li>
  <li><b>Aleatorio:</b> garantiza estadísticamente el caso promedio independientemente de los datos.</li>
</ul>

<h3>Análisis de complejidad</h3>

| Escenario | $T(n)$ | $S(n)$ | Descripción |
| :---: | :---: | :---: | :---: |
| **Mejor caso** | $\Omega(n\,\log_2 n)$ | $\Omega(\log_2 n)$ | El pivote siempre divide el arreglo en dos mitades iguales: $T(n)=2T(n/2)+n$ |
| **Caso promedio** | $\Theta(n\,\log_2 (n))$ | $\Theta(\log_2 (n))$ | El pivote produce particiones razonablemente balanceadas en promedio |
| **Peor caso** | $O(n^2)$ | $O(n)$ | El pivote es siempre el mínimo o el máximo: $T(n)=T(n-1)+n$ (arreglo ordenado con pivote en extremo) |

<h3>Ventajas y desventajas</h3>

| Ventajas | Desventajas |
| :---: | :---: |
| Muy eficiente en la práctica: constante multiplicativa pequeña | Peor caso $O(n^2)$ si el pivote es siempre el extremo |
| Ordenamiento <i>in-place</i> ($O(\log n)$ espacio de pila) | No es estable en la implementación estándar |
| Altamente optimizable: pivote aleatorio elimina el peor caso en la práctica | Su análisis es más complejo que el del ordenamiento por mezcla |

---

<h2 id="8-7">🔢 8.7 Ordenamiento radix</h2>

<p align="center">
  🎬 <a href="./7_ordenamiento_radix.ipynb"><b>Abrir simulación</b></a>
</p>

<p align="justify">
El <b>ordenamiento radix</b> procesa las claves por posiciones, normalmente desde el dígito menos significativo hasta el más significativo. En cada pasada agrupa los elementos de acuerdo con el dígito actual y conserva su orden relativo. Si se procesan <i>k</i> dígitos de <i>n</i> elementos, su costo se expresa como $\Theta(nk)$ bajo una base fija.
</p>

<p align="justify">
No es un algoritmo de comparación: su eficiencia depende de la representación y del rango de las claves. La implementación del notebook trabaja con enteros no negativos y permite observar cada distribución y recolección de cubetas.
</p>

---

<h2 id="8-shell">➕ Material adicional: Shell Sort</h2>

<p align="justify"><b>Esta sección amplía el libro.</b> Shell Sort generaliza el ordenamiento por inserción comparando primero elementos separados por una distancia o <i>gap</i>. Su rendimiento depende de la secuencia de saltos elegida; por ello no debe asignársele una única complejidad ajustada sin indicar esa secuencia.</p>

<p align="center">
  🎬 <a href="./4_ordenamiento_shell.ipynb"><b>Abrir simulación</b></a>
</p>

---

<h2 id="8-comp">📊 Material adicional: comparación de todos los algoritmos</h2>

<p align="center">
  🎬 <a href="./0_comparacion_ordenamientos.ipynb"><b>Abrir simulación</b></a>
</p>

| Algoritmo | Mejor caso $T(n)$ | Caso promedio $T(n)$ | Peor caso $T(n)$ | $S(n)$ | Estable | In-place |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Burbuja** | $\Omega(n)$ | $\Theta(n^2)$ | $O(n^2)$ | $O(1)$ | Sí | Sí |
| **Selección** | $\Theta(n^2)$ | $\Theta(n^2)$ | $O(n^2)$ | $O(1)$ | No | Sí |
| **Inserción** | $\Omega(n)$ | $\Theta(n^2)$ | $O(n^2)$ | $O(1)$ | Sí | Sí |
| **Mezcla** | $\Theta(n\,\log_2 n)$ | $\Theta(n\,\log_2 n)$ | $O(n\,\log_2 n)$ | $O(n)$ | Sí | No |
| **Rápido** | $\Omega(n\,\log_2 n)$ | $\Theta(n\,\log_2 n)$ | $O(n^2)$ | $O(\log_2 n)$ | No | Sí |
| **Radix** | $\Theta(nk)$ | $\Theta(nk)$ | $\Theta(nk)$ | $\Theta(n + r)$ | Sí | No |

<p><small>En Radix, <i>k</i> es la cantidad de dígitos procesados y <i>r</i> es la base o cantidad de cubetas.</small></p>

---

<h2 id="8-8">💡 8.8 Consideraciones finales</h2>

<p align="justify">
La elección del algoritmo de ordenamiento depende del contexto de uso. Los algoritmos cuadráticos (burbuja, selección, inserción) son apropiados para conjuntos pequeños y situaciones donde la simplicidad de implementación prima sobre la eficiencia. El ordenamiento por inserción, en particular, es el más eficiente de los tres para arreglos casi ordenados y es utilizado en la fase final de algoritmos híbridos como Timsort.
</p>

<p align="justify">
Para conjuntos grandes, los algoritmos log-lineales suelen ser preferibles. El ordenamiento por mezcla garantiza $\Theta(n\log n)$ en todos los casos y es estable, al costo de memoria adicional lineal. El ordenamiento rápido tiene un comportamiento promedio $\Theta(n\log n)$ y buena localidad de memoria, aunque requiere una estrategia de selección de pivote adecuada para evitar el peor caso cuadrático. Radix puede resultar competitivo cuando las claves admiten procesamiento por dígitos y su representación satisface las condiciones del algoritmo.
</p>

---

<h2 id="8-9">📚 8.9 Ejercicios propuestos</h2>

<p>El libro propone implementar los algoritmos del capítulo, medir mejor caso, caso promedio y peor caso, y comparar los resultados experimentales con sus funciones analíticas. También presenta ejercicios opcionales sobre aplicaciones, algoritmos avanzados, distribución inicial de los datos y matrices.</p>

<p>El notebook <a href="./ejercicios_propuestos.ipynb"><code>ejercicios_propuestos.ipynb</code></a> desarrolla las actividades mediante mediciones y proyecciones claramente diferenciadas. Las explicaciones de aplicaciones, Heap Sort, Counting Sort, Radix Sort y distribución de entrada se identifican como <b>soluciones y material adicional</b>.</p>

---

<h2>⚙️ Ejecución local</h2>

<p align="justify">
Para abrir los notebooks directamente con Jupyter:
</p>

```bash
jupyter notebook
```

<p align="justify">
Abra el notebook del algoritmo que desee visualizar desde la carpeta <code>capitulo8/</code> y ejecute la celda de simulación.
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
