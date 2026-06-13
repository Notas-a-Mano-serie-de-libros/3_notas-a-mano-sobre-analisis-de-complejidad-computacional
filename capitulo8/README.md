<h1 style="text-align:center;">
  <strong>Capítulo 8: Análisis de algoritmos de ordenamiento clásicos</strong>
</h1>

---

<h2>🧭 Contenido del capítulo</h2>

<ul>
  <li><a href="#8-1">8.1 Consideraciones previas</a></li>
  <li><a href="#8-2">8.2 Ordenamiento burbuja</a>
    <ul>
      <li>🎬 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/1_ordenamiento_burbuja.ipynb">Animación interactiva – Ordenamiento burbuja</a></li>
    </ul>
  </li>
  <li><a href="#8-3">8.3 Ordenamiento por selección</a>
    <ul>
      <li>🎬 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/2_ordenamiento_seleccion.ipynb">Animación interactiva – Ordenamiento por selección</a></li>
    </ul>
  </li>
  <li><a href="#8-4">8.4 Ordenamiento por inserción</a>
    <ul>
      <li>🎬 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/3_ordenamiento_insercion.ipynb">Animación interactiva – Ordenamiento por inserción</a></li>
    </ul>
  </li>
  <li><a href="#8-5">8.5 Ordenamiento por mezcla</a>
    <ul>
      <li>🎬 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/5_ordenamiento_mezcla.ipynb">Animación interactiva – Ordenamiento por mezcla</a></li>
    </ul>
  </li>
  <li><a href="#8-6">8.6 Ordenamiento rápido</a>
    <ul>
      <li>🎬 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/6_ordenamiento_rapido.ipynb">Animación interactiva – Ordenamiento rápido</a></li>
    </ul>
  </li>
  <li><a href="#8-comp">📊 Comparación de todos los algoritmos</a>
    <ul>
      <li>🎬 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/0_comparacion_ordenamientos.ipynb">Comparación interactiva – Todos los algoritmos</a></li>
    </ul>
  </li>
  <li><a href="#8-7">8.7 Consideraciones finales</a></li>
</ul>

---

<h2 id="8-1">⚙️ 8.1 Consideraciones previas</h2>

<p align="justify">
Este capítulo aplica las herramientas desarrolladas en los capítulos anteriores —funciones de complejidad, notación asintótica, relaciones de recurrencia y análisis de algoritmos recursivos— al estudio de los algoritmos de ordenamiento más utilizados en la práctica. El ordenamiento es una de las operaciones más frecuentes en informática y la elección del algoritmo correcto tiene un impacto directo en el rendimiento de los sistemas.
</p>

<p align="justify">
El capítulo estudia cinco algoritmos: tres <b>cuadráticos</b> (burbuja, selección, inserción) apropiados para conjuntos pequeños por su simplicidad de implementación, y dos <b>logarítmicos</b> (mezcla y rápido) que escalan eficientemente a grandes volúmenes de datos.
</p>

<p align="justify">
Las animaciones utilizan dos modos de visualización intercambiables: representación con <b>cajas</b> (para seguir el valor de cada elemento) y representación con <b>barras</b> (para observar visualmente la evolución del ordenamiento). Los controles permiten elegir el <b>orden</b> (ascendente o descendente) y, en el caso del ordenamiento rápido, la <b>estrategia de selección del pivote</b>.
</p>

---

<h2 id="8-2">🫧 8.2 Ordenamiento burbuja</h2>

<p align="center">
  🎬 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/1_ordenamiento_burbuja.ipynb"><b>Abrir animación interactiva en Google Colab</b></a>
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
El número de comparaciones en la pasada <i>i</i>-ésima es <code>n−1−i</code>. Sumando para todas las pasadas: <code>Σᵢ₌₀ⁿ⁻² (n−1−i) = n(n−1)/2</code>.
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Escenario</th>
      <th style="padding:8px; border:1px solid #ccc;">T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">S(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">Descripción</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Mejor caso</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Ω(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Ω(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Arreglo ya ordenado (con optimización de bandera)</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Caso promedio</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n²)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">n²/2 comparaciones en promedio</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Peor caso</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(n²)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Arreglo ordenado en orden inverso: n(n−1)/2 comparaciones</td>
    </tr>
  </tbody>
</table>

<h3>Ventajas y desventajas</h3>
<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Ventajas</th>
      <th style="padding:8px; border:1px solid #ccc;">Desventajas</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Implementación simple y comprensible</td>
      <td style="padding:8px; border:1px solid #ccc;">Ineficiente para arreglos grandes</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Ordenamiento <i>in-place</i> (O(1) espacio adicional)</td>
      <td style="padding:8px; border:1px solid #ccc;">Alto número de intercambios comparado con otros métodos cuadráticos</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Estable: preserva el orden relativo de elementos iguales</td>
      <td style="padding:8px; border:1px solid #ccc;">Desempeño consistentemente pobre en datos desordenados</td>
    </tr>
  </tbody>
</table>

---

<h2 id="8-3">🎯 8.3 Ordenamiento por selección</h2>

<p align="center">
  🎬 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/2_ordenamiento_seleccion.ipynb"><b>Abrir animación interactiva en Google Colab</b></a>
</p>

<p align="justify">
El <b>ordenamiento por selección</b> divide el arreglo en dos partes: la porción ordenada (inicialmente vacía) y la porción no ordenada. En cada pasada selecciona el elemento mínimo de la porción no ordenada y lo intercambia con el primer elemento de dicha porción, ampliando la parte ordenada en una posición.
</p>

<h3>Análisis de complejidad</h3>

<p align="justify">
El número de comparaciones es siempre <code>n(n−1)/2</code> independientemente del estado inicial del arreglo, porque siempre debe recorrer toda la porción no ordenada para encontrar el mínimo. El número de intercambios es a lo sumo <i>n−1</i>.
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Escenario</th>
      <th style="padding:8px; border:1px solid #ccc;">T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">S(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">Descripción</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Todos los casos</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n²)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">n(n−1)/2 comparaciones en cualquier escenario; la disposición inicial no afecta el costo</td>
    </tr>
  </tbody>
</table>

<h3>Ventajas y desventajas</h3>
<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Ventajas</th>
      <th style="padding:8px; border:1px solid #ccc;">Desventajas</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Número mínimo de intercambios: a lo sumo n−1</td>
      <td style="padding:8px; border:1px solid #ccc;">Costo siempre cuadrático, no mejora con datos casi ordenados</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Útil cuando el costo de los intercambios supera al de las comparaciones</td>
      <td style="padding:8px; border:1px solid #ccc;">No es estable en la implementación estándar</td>
    </tr>
  </tbody>
</table>

---

<h2 id="8-4">🃏 8.4 Ordenamiento por inserción</h2>

<p align="center">
  🎬 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/3_ordenamiento_insercion.ipynb"><b>Abrir animación interactiva en Google Colab</b></a>
</p>

<p align="justify">
El <b>ordenamiento por inserción</b> construye el arreglo ordenado de izquierda a derecha, insertando cada nuevo elemento en su posición correcta dentro de la porción ya ordenada. Es la estrategia que usa intuitivamente un jugador de cartas al ordenar su mano.
</p>

<h3>Análisis de complejidad</h3>

<p align="justify">
En el mejor caso (arreglo ya ordenado), cada elemento solo requiere una comparación: <code>T(n) ∈ Ω(n)</code>. En el caso promedio, el elemento se inserta en la posición media de la porción ordenada, dando <code>n²/4</code> comparaciones. En el peor caso (orden inverso), cada elemento se mueve hasta el inicio: <code>n(n−1)/2</code> comparaciones.
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Escenario</th>
      <th style="padding:8px; border:1px solid #ccc;">T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">S(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">Descripción</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Mejor caso</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Ω(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Ω(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Arreglo ya ordenado: solo n−1 comparaciones</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Caso promedio</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n²)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">n²/4 comparaciones en promedio</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Peor caso</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(n²)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Arreglo en orden inverso: n(n−1)/2 comparaciones</td>
    </tr>
  </tbody>
</table>

<h3>Ventajas y desventajas</h3>
<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Ventajas</th>
      <th style="padding:8px; border:1px solid #ccc;">Desventajas</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Eficiente para arreglos pequeños y casi ordenados</td>
      <td style="padding:8px; border:1px solid #ccc;">Cuadrático en el caso general</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Estable y <i>in-place</i></td>
      <td style="padding:8px; border:1px solid #ccc;">Muchos desplazamientos en el peor caso</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Útil como paso final en algoritmos híbridos (ej. Timsort)</td>
      <td style="padding:8px; border:1px solid #ccc;">No escala bien para n grande</td>
    </tr>
  </tbody>
</table>

---

<h2 id="8-5">🔀 8.5 Ordenamiento por mezcla</h2>

<p align="center">
  🎬 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/5_ordenamiento_mezcla.ipynb"><b>Abrir animación interactiva en Google Colab</b></a>
</p>

<p align="justify">
El <b>ordenamiento por mezcla</b> (merge sort) es un algoritmo <b>divide y vencerás</b>: divide el arreglo en dos mitades, ordena cada mitad recursivamente y luego las fusiona en una sola secuencia ordenada. Es el algoritmo de ordenamiento cuyo análisis se estudia en el Capítulo 6 como ejemplo de recurrencia de división.
</p>

<h3>Relación de recurrencia</h3>
<pre><code>T(n) = { 1             si n ≤ 1
        { 2T(n/2) + n   si n &gt; 1</code></pre>

<p align="justify">
Aplicando el <b>teorema maestro básico</b> con <code>a=2, b=2, f(n)∈O(n¹)</code> → <code>a = bᵏ</code> (Caso 2) → <code>T(n) ∈ Θ(n·log₂(n))</code>.
</p>

<h3>Análisis de complejidad</h3>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Escenario</th>
      <th style="padding:8px; border:1px solid #ccc;">T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">S(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">Descripción</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Todos los casos</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n·log₂(n))</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">La división y mezcla ocurren siempre en el mismo número de pasos, independientemente de los datos</td>
    </tr>
  </tbody>
</table>

<h3>Ventajas y desventajas</h3>
<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Ventajas</th>
      <th style="padding:8px; border:1px solid #ccc;">Desventajas</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Complejidad Θ(n log n) garantizada en todos los casos</td>
      <td style="padding:8px; border:1px solid #ccc;">Requiere O(n) de memoria adicional para la fase de mezcla</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Estable: preserva el orden relativo de elementos iguales</td>
      <td style="padding:8px; border:1px solid #ccc;">No es <i>in-place</i> en la implementación estándar</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Paralelizable: las dos mitades se pueden ordenar de forma independiente</td>
      <td style="padding:8px; border:1px solid #ccc;">Mayor constante multiplicativa que quicksort en la práctica</td>
    </tr>
  </tbody>
</table>

---

<h2 id="8-6">⚡ 8.6 Ordenamiento rápido</h2>

<p align="center">
  🎬 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/6_ordenamiento_rapido.ipynb"><b>Abrir animación interactiva en Google Colab</b></a>
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

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Escenario</th>
      <th style="padding:8px; border:1px solid #ccc;">T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">S(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">Descripción</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Mejor caso</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Ω(n·log₂(n))</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Ω(log₂(n))</b></td>
      <td style="padding:8px; border:1px solid #ccc;">El pivote siempre divide el arreglo en dos mitades iguales: T(n)=2T(n/2)+n</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Caso promedio</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n·log₂(n))</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(log₂(n))</b></td>
      <td style="padding:8px; border:1px solid #ccc;">El pivote produce particiones razonablemente balanceadas en promedio</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Peor caso</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(n²)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">El pivote es siempre el mínimo o el máximo: T(n)=T(n−1)+n (arreglo ordenado con pivote en extremo)</td>
    </tr>
  </tbody>
</table>

<h3>Ventajas y desventajas</h3>
<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Ventajas</th>
      <th style="padding:8px; border:1px solid #ccc;">Desventajas</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Muy eficiente en la práctica: constante multiplicativa pequeña</td>
      <td style="padding:8px; border:1px solid #ccc;">Peor caso O(n²) si el pivote es siempre el extremo</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Ordenamiento <i>in-place</i> (O(log n) espacio de pila)</td>
      <td style="padding:8px; border:1px solid #ccc;">No es estable en la implementación estándar</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Altamente optimizable: pivote aleatorio elimina el peor caso en la práctica</td>
      <td style="padding:8px; border:1px solid #ccc;">Su análisis es más complejo que el del ordenamiento por mezcla</td>
    </tr>
  </tbody>
</table>

---

<h2 id="8-comp">📊 Comparación de todos los algoritmos</h2>

<p align="center">
  🎬 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/0_comparacion_ordenamientos.ipynb"><b>Abrir comparación interactiva en Google Colab</b></a>
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Algoritmo</th>
      <th style="padding:8px; border:1px solid #ccc;">Mejor caso T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">Caso promedio T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">Peor caso T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">S(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">Estable</th>
      <th style="padding:8px; border:1px solid #ccc;">In-place</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Burbuja</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Ω(n)</td>
      <td style="padding:8px; border:1px solid #ccc;">Θ(n²)</td>
      <td style="padding:8px; border:1px solid #ccc;">O(n²)</td>
      <td style="padding:8px; border:1px solid #ccc;">O(1)</td>
      <td style="padding:8px; border:1px solid #ccc;">Sí</td>
      <td style="padding:8px; border:1px solid #ccc;">Sí</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Selección</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Θ(n²)</td>
      <td style="padding:8px; border:1px solid #ccc;">Θ(n²)</td>
      <td style="padding:8px; border:1px solid #ccc;">O(n²)</td>
      <td style="padding:8px; border:1px solid #ccc;">O(1)</td>
      <td style="padding:8px; border:1px solid #ccc;">No</td>
      <td style="padding:8px; border:1px solid #ccc;">Sí</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Inserción</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Ω(n)</td>
      <td style="padding:8px; border:1px solid #ccc;">Θ(n²)</td>
      <td style="padding:8px; border:1px solid #ccc;">O(n²)</td>
      <td style="padding:8px; border:1px solid #ccc;">O(1)</td>
      <td style="padding:8px; border:1px solid #ccc;">Sí</td>
      <td style="padding:8px; border:1px solid #ccc;">Sí</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Mezcla</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Θ(n·log₂n)</td>
      <td style="padding:8px; border:1px solid #ccc;">Θ(n·log₂n)</td>
      <td style="padding:8px; border:1px solid #ccc;">O(n·log₂n)</td>
      <td style="padding:8px; border:1px solid #ccc;">O(n)</td>
      <td style="padding:8px; border:1px solid #ccc;">Sí</td>
      <td style="padding:8px; border:1px solid #ccc;">No</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Rápido</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Ω(n·log₂n)</td>
      <td style="padding:8px; border:1px solid #ccc;">Θ(n·log₂n)</td>
      <td style="padding:8px; border:1px solid #ccc;">O(n²)</td>
      <td style="padding:8px; border:1px solid #ccc;">O(log₂n)</td>
      <td style="padding:8px; border:1px solid #ccc;">No</td>
      <td style="padding:8px; border:1px solid #ccc;">Sí</td>
    </tr>
  </tbody>
</table>

---

<h2 id="8-7">💡 8.7 Consideraciones finales</h2>

<p align="justify">
La elección del algoritmo de ordenamiento depende del contexto de uso. Los algoritmos cuadráticos (burbuja, selección, inserción) son apropiados para conjuntos pequeños y situaciones donde la simplicidad de implementación prima sobre la eficiencia. El ordenamiento por inserción, en particular, es el más eficiente de los tres para arreglos casi ordenados y es utilizado en la fase final de algoritmos híbridos como Timsort.
</p>

<p align="justify">
Para conjuntos grandes, los algoritmos logarítmicos son imprescindibles. El ordenamiento por mezcla garantiza <code>Θ(n log n)</code> en todos los casos y es estable, al costo de memoria adicional lineal. El ordenamiento rápido es en la práctica el más veloz por su pequeña constante multiplicativa y su naturaleza <i>in-place</i>, aunque requiere una estrategia de selección de pivote adecuada para evitar el peor caso cuadrático.
</p>

---

<h2>⚙️ Ejecución local</h2>

<p align="justify">
Para abrir los notebooks directamente con Jupyter:
</p>

```bash
jupyter notebook
```

<p align="justify">
Abra el notebook del algoritmo que desee visualizar desde la carpeta <code>capitulo8/notebooks/</code> y ejecute la celda de simulación.
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
