<h1 style="text-align:center;">
  <strong>Capítulo 7: Análisis de algoritmos de búsqueda clásicos</strong>
</h1>

## Correspondencia con el libro

Este README sigue el Capítulo 7, páginas 255–312. Cada algoritmo del libro tiene un notebook propio; la comparación global y el laboratorio de ejercicios son ampliaciones ejecutables.

| Libro | Recurso | Simulación |
| :---: | :---: | :---: |
| 7.2 | Búsqueda secuencial | [Abrir](./1_busqueda_secuencial.ipynb) |
| 7.3 | Búsqueda binaria | [Abrir](./2_busqueda_binaria.ipynb) |
| 7.4 | Búsqueda por interpolación | [Abrir](./3_busqueda_interpolacion.ipynb) |
| 7.5 | Búsqueda por saltos | [Abrir](./4_busqueda_saltos.ipynb) |
| 7.6 | Búsqueda exponencial | [Abrir](./5_busqueda_exponencial.ipynb) |
| 7.7 | Búsqueda ternaria | [Abrir](./6_busqueda_ternaria.ipynb) |
| Adicional | Comparación de búsquedas | [Abrir](./0_comparacion_busquedas.ipynb) |
| 7.9 | Ejercicios propuestos | [Abrir](./ejercicios_propuestos.ipynb) |

> **Material adicional del repositorio:** el comparador, las mediciones para diferentes casos, las proyecciones teóricas y las soluciones de los ejercicios amplían el análisis impreso. Las proyecciones se identifican como tales y no representan ejecuciones reales.

---

<h2>🧭 Contenido del capítulo</h2>

<ul>
  <li><a href="#7-1">7.1 Consideraciones previas</a></li>
  <li><a href="#7-2">7.2 Búsqueda secuencial</a>
    <ul>
      <li>🎬 <a href="./1_busqueda_secuencial.ipynb">Animación interactiva – Búsqueda secuencial</a></li>
    </ul>
  </li>
  <li><a href="#7-3">7.3 Búsqueda binaria</a>
    <ul>
      <li>🎬 <a href="./2_busqueda_binaria.ipynb">Animación interactiva – Búsqueda binaria</a></li>
    </ul>
  </li>
  <li><a href="#7-4">7.4 Búsqueda por interpolación</a>
    <ul>
      <li>🎬 <a href="./3_busqueda_interpolacion.ipynb">Animación interactiva – Búsqueda por interpolación</a></li>
    </ul>
  </li>
  <li><a href="#7-5">7.5 Búsqueda por saltos</a>
    <ul>
      <li>🎬 <a href="./4_busqueda_saltos.ipynb">Animación interactiva – Búsqueda por saltos</a></li>
    </ul>
  </li>
  <li><a href="#7-6">7.6 Búsqueda exponencial</a>
    <ul>
      <li>🎬 <a href="./5_busqueda_exponencial.ipynb">Animación interactiva – Búsqueda exponencial</a></li>
    </ul>
  </li>
  <li><a href="#7-7">7.7 Búsqueda ternaria</a>
    <ul>
      <li>🎬 <a href="./6_busqueda_ternaria.ipynb">Animación interactiva – Búsqueda ternaria</a></li>
    </ul>
  </li>
  <li><a href="#7-comp">📊 Comparación de todos los algoritmos</a>
    <ul>
      <li>🎬 <a href="./0_comparacion_busquedas.ipynb">Comparación interactiva – Todos los algoritmos</a></li>
    </ul>
  </li>
  <li><a href="#7-8">7.8 Consideraciones finales</a></li>
  <li><a href="#7-9">7.9 Ejercicios propuestos</a></li>
</ul>

---

<h2 id="7-1">⚙️ 7.1 Consideraciones previas</h2>

<p align="justify">
Este capítulo aplica las herramientas formales desarrolladas en los capítulos anteriores al estudio de los algoritmos de búsqueda más utilizados en la práctica. Los algoritmos operan sobre <b>arreglos de enteros</b> y los resultados se generalizan a otras estructuras de datos indexadas.
</p>

<p align="justify">
Las animaciones utilizan la siguiente convención de colores para representar el estado de los elementos durante la búsqueda:
</p>

| Color | Significado |
| :---: | :---: |
| ⬜ Blanco | Elemento en estado de reposo (no evaluado aún) |
| 🔵 Azul | Elemento en evaluación activa (comparación actual) |
| ⬛ Gris | Elemento descartado del espacio de búsqueda |
| 🟢 Verde | Elemento encontrado (objetivo localizado) |

---

<h2 id="7-2">🔍 7.2 Búsqueda secuencial</h2>

<p align="center">
  🎬 <a href="./1_busqueda_secuencial.ipynb"><b>Abrir simulación</b></a>
</p>

<p align="justify">
La <b>búsqueda secuencial</b> (también llamada búsqueda lineal) es el algoritmo de búsqueda más simple: recorre la estructura de datos comparando cada elemento con el objetivo hasta encontrarlo o agotar el arreglo. No requiere que los datos estén ordenados.
</p>

<h3>Descripción del algoritmo</h3>
<p align="justify">
La implementación itera sobre el arreglo con un ciclo <code>for</code>, comparando en cada posición el elemento actual con el valor buscado. Al encontrar una coincidencia retorna <code>true</code>; al terminar el ciclo sin encontrarlo retorna <code>false</code>.
</p>

<h3>Análisis de complejidad</h3>

| Escenario | $T(n)$ | $S(n)$ | Descripción |
| :---: | :---: | :---: | :---: |
| **Mejor caso** | $\Omega(1)$ | $\Omega(1)$ | El objetivo está en la primera posición |
| **Caso promedio** | $\Theta(n)$ | $\Theta(1)$ | $E[X] = \frac{n+1}{2} \approx \frac{n}{2}$ comparaciones (fórmula de Gauss) |
| **Peor caso** | $O(n)$ | $O(1)$ | El objetivo está al final o no existe |

<p align="justify">
<b>Dato curioso:</b> Donald Knuth demostró formalmente que $O(n)$ es la cota óptima para cualquier algoritmo de búsqueda sobre datos no ordenados. No es posible hacer búsqueda sobre un conjunto desordenado en menos de <i>n</i> comparaciones en el peor caso.
</p>

<h3>Escenarios de aplicación</h3>
<ul>
  <li>Estructuras no ordenadas donde el orden de los datos no puede garantizarse.</li>
  <li>Búsquedas ocasionales sobre conjuntos pequeños donde el costo de ordenar supera el costo de buscar linealmente.</li>
  <li>Datos que llegan en tiempo real y no pueden pre-procesarse.</li>
</ul>

<h3>Ventajas y desventajas</h3>

| Ventajas | Desventajas |
| :---: | :---: |
| No requiere datos ordenados | Ineficiente para conjuntos grandes |
| Implementación trivial | No aprovecha ninguna propiedad estructural |
| Flexible: aplica a cualquier tipo de dato comparable | Costoso si se repite con frecuencia sobre conjuntos grandes |

---

<h2 id="7-3">⚡ 7.3 Búsqueda binaria</h2>

<p align="center">
  🎬 <a href="./2_busqueda_binaria.ipynb"><b>Abrir simulación</b></a>
</p>

<p align="justify">
La <b>búsqueda binaria</b> es uno de los algoritmos más eficientes para estructuras ordenadas. En cada iteración compara el objetivo con el elemento central del rango activo y descarta la mitad del espacio de búsqueda:
</p>

<p align="center"><code>medio = ⌊(inicio + fin) / 2⌋</code></p>

<h3>Ejemplo</h3>
<p align="justify">
Buscar el valor <b>10</b> en el arreglo <code>[2, 3, 5, 9, 10, 11, 21, 43]</code> (n=8):
</p>
<ul>
  <li>Iteración 1: medio = ⌊(0+7)/2⌋ = 3 → arr[3]=9 &lt; 10 → inicio = 4</li>
  <li>Iteración 2: medio = ⌊(4+7)/2⌋ = 5 → arr[5]=11 &gt; 10 → fin = 4</li>
  <li>Iteración 3: medio = ⌊(4+4)/2⌋ = 4 → arr[4]=10 ✓ <b>Encontrado</b></li>
</ul>

<h3>Análisis de complejidad</h3>

| Escenario | $T(n)$ | $S(n)$ | Descripción |
| :---: | :---: | :---: | :---: |
| **Mejor caso** | $\Omega(1)$ | $\Omega(1)$ | El objetivo está en la posición central |
| **Caso promedio** | $\Theta(\log_2 n)$ | $\Theta(1)$ | Derivado con la fórmula de Stirling: $\log_2(n!) \approx n(\log_2 n - \log_2 e)$ |
| **Peor caso** | $O(\log_2 (n))$ | $O(1)$ | El objetivo está en los extremos o no existe |

<p align="justify">
<b>Dato curioso:</b> La idea de buscar dividiendo el espacio a la mitad fue sugerida por <b>John Mauchly</b> en 1946, pero la primera implementación sin errores fue publicada por <b>Derrick Henry Lehmer</b> en 1960, 14 años después.
</p>

<h3>Escenarios de aplicación</h3>
<ul>
  <li>Estructuras de datos con acceso aleatorio en tiempo constante (arreglos, vectores).</li>
  <li>Datos que permanecen estáticos o se actualizan infrecuentemente.</li>
  <li>Índices ordenados en bases de datos y sistemas de archivos.</li>
</ul>

<h3>Ventajas y desventajas</h3>

| Ventajas | Desventajas |
| :---: | :---: |
| Alta eficiencia logarítmica incluso para n muy grande | Requiere que los datos estén ordenados |
| Bajo consumo de memoria | No es adecuado para estructuras dinámicas con inserciones frecuentes |

---

<h2 id="7-4">🎯 7.4 Búsqueda por interpolación</h2>

<p align="center">
  🎬 <a href="./3_busqueda_interpolacion.ipynb"><b>Abrir simulación</b></a>
</p>

<p align="justify">
La <b>búsqueda por interpolación</b> mejora la búsqueda binaria asumiendo que los datos siguen una distribución aproximadamente uniforme. En lugar de dividir el espacio en dos partes iguales, estima la posición del objetivo mediante interpolación lineal:
</p>

<p align="center"><code>pos = ⌊inicio + ((fin − inicio) · (elemento − arr[inicio])) / (arr[fin] − arr[inicio])⌋</code></p>

<h3>Ejemplo</h3>
<p align="justify">
Buscar el valor <b>60</b> en el arreglo <code>[0, 10, 20, 30, 40, 60, 80, 90]</code> (distribución uniforme, n=8):
</p>
<ul>
  <li>Iteración 1: pos = ⌊0 + (7·60)/90⌋ = ⌊4.67⌋ = 4 → arr[4]=40 &lt; 60 → inicio = 5</li>
  <li>Iteración 2: pos = ⌊5 + (2·20)/30⌋ = ⌊5+1.33⌋ = 5 → arr[5]=60 ✓ <b>Encontrado</b></li>
</ul>

<h3>Análisis de complejidad</h3>

| Escenario | $T(n)$ | $S(n)$ | Descripción |
| :---: | :---: | :---: | :---: |
| **Mejor caso** | $\Omega(1)$ | $\Omega(1)$ | La estimación apunta directamente al objetivo |
| **Caso promedio** | $\Theta(\log_2(\log_2 n))$ | $\Theta(1)$ | Distribución uniforme: cada iteración reduce el espacio por un factor $\sqrt{n}$ (Perl et al., 1978) |
| **Peor caso** | $O(n)$ | $O(1)$ | Distribución exponencial: la estimación siempre apunta al extremo |

<p align="justify">
<b>Dato curioso:</b> Fue descrito por <b>W. W. Peterson</b> en 1957 para localizar registros en almacenamiento de acceso aleatorio. Su complejidad promedio $O(\log\log n)$ fue demostrada formalmente 21 años después por <b>Yehoshua Perl, Alon Itai y Haim Avni</b> (1978).
</p>

<h3>Escenarios de aplicación</h3>
<ul>
  <li>Datos ordenados con distribución aproximadamente uniforme (precios, temperaturas, fechas consecutivas).</li>
  <li>Estructuras con acceso aleatorio en tiempo constante.</li>
</ul>

<h3>Ventajas y desventajas</h3>

| Ventajas | Desventajas |
| :---: | :---: |
| Extremadamente eficiente con datos uniformes: $O(\log\log n)$ | Se degrada a $O(n)$ con datos sesgados o exponenciales |
| Reduce drásticamente el número de comparaciones en distribuciones lineales | Requiere datos ordenados y acceso por posición |

---

<h2 id="7-5">🦘 7.5 Búsqueda por saltos</h2>

<p align="center">
  🎬 <a href="./4_busqueda_saltos.ipynb"><b>Abrir simulación</b></a>
</p>

<p align="justify">
La <b>búsqueda por saltos</b> (también llamada búsqueda por bloques) recorre la estructura en bloques de tamaño fijo δ hasta identificar el bloque que puede contener el objetivo, y luego aplica búsqueda lineal dentro de ese bloque.
</p>

<h3>Tamaño óptimo del bloque</h3>
<p align="justify">
El costo total en función de δ es <code>C(δ) = n/δ + δ</code>. Minimizando esta función mediante la primera derivada:
</p>
<p align="center">$\frac{dC}{d\delta}=0 \to \delta=\sqrt{n} \to \delta=\lfloor\sqrt{n}\rfloor$</p>

<h3>Ejemplo</h3>
<p align="justify">
Buscar el valor <b>6</b> en el arreglo <code>[1, 2, 3, 4, 5, 6, 7, 8]</code> (n=8, δ=⌊√8⌋=2):
</p>
<ul>
  <li>Bloque [1,2]: 2 &lt; 6 → siguiente bloque</li>
  <li>Bloque [3,4]: 4 &lt; 6 → siguiente bloque</li>
  <li>Bloque [5,6]: 6 ≤ 6 → búsqueda lineal dentro del bloque → arr[5]=6 ✓ <b>Encontrado</b></li>
</ul>

<h3>Análisis de complejidad</h3>

| Escenario | $T(n)$ | $S(n)$ | Descripción |
| :---: | :---: | :---: | :---: |
| **Mejor caso** | $\Omega(1)$ | $\Omega(1)$ | El objetivo está en la primera posición del primer bloque |
| **Caso promedio** | $\Theta(\sqrt{n})$ | $\Theta(1)$ | $E[X] = \sqrt{n}+1$ (fórmula de Gauss en ambas fases) |
| **Peor caso** | $O(\sqrt{n})$ | $O(1)$ | El objetivo está al final o no existe: $\sqrt{n}+\sqrt{n}=2\sqrt{n}$ iteraciones |

<p align="justify">
<b>Dato curioso:</b> <b>Ben Shneiderman</b> introdujo esta técnica en 1978 demostrando que el tamaño de los bloques puede ajustarse dinámicamente para optimizar cada salto, dando lugar a la <b>búsqueda por saltos multinivel</b>, cuya eficiencia puede competir con la búsqueda binaria en condiciones específicas.
</p>

<h3>Escenarios de aplicación</h3>
<ul>
  <li>Estructuras donde acceder a cada posición tiene un costo elevado (discos, memoria secundaria).</li>
  <li>Cuando no es posible apoyarse en índices o estructuras auxiliares.</li>
</ul>

<h3>Ventajas y desventajas</h3>

| Ventajas | Desventajas |
| :---: | :---: |
| Más eficiente que búsqueda lineal; punto medio entre $O(n)$ y $O(\log n)$ | Requiere datos ordenados |
| Reduce accesos a memoria en estructuras con acceso costoso | No ofrece ventajas sobre búsqueda secuencial en arreglos pequeños |

---

<h2 id="7-6">📈 7.6 Búsqueda exponencial</h2>

<p align="center">
  🎬 <a href="./5_busqueda_exponencial.ipynb"><b>Abrir simulación</b></a>
</p>

<p align="justify">
La <b>búsqueda exponencial</b> está diseñada para estructuras de datos ordenadas de longitud desconocida o muy grande. Primero duplica el índice de búsqueda en cada paso (<code>i = 2 * i</code>) hasta encontrar un valor mayor que el objetivo, y luego aplica búsqueda binaria sobre el rango acotado:
</p>

<p align="center"><code>rango = [i/2, mín(i, n−1)]</code></p>

<h3>Ejemplo</h3>
<p align="justify">
Buscar el valor <b>6</b> en el arreglo <code>[1, 2, 3, 4, 5, 6, 7, 8]</code> (n=8):
</p>
<ul>
  <li>Verificación inicial: arr[0]=1 ≠ 6</li>
  <li>i=1: arr[1]=2 ≤ 6 → i=2; i=2: arr[2]=3 ≤ 6 → i=4; i=4: arr[4]=5 ≤ 6 → i=8</li>
  <li>i=8: supera el límite → rango = [4, 7] → búsqueda binaria sobre [5,6,7,8] → arr[5]=6 ✓ <b>Encontrado</b></li>
</ul>

<h3>Análisis de complejidad</h3>

| Escenario | $T(n)$ | $S(n)$ | Descripción |
| :---: | :---: | :---: | :---: |
| **Mejor caso** | $\Omega(1)$ | $\Omega(1)$ | El objetivo está en la primera posición |
| **Caso promedio** | $\Theta(\log_2 n)$ | $\Theta(1)$ | Derivado con la fórmula de Stirling: $E[X] \approx \log_2 n - \log_2 e$ |
| **Peor caso** | $O(\log_2 n)$ | $O(1)$ | $T(n) \in O(\log_2 n+\log_2 n)=O(2\log_2 n)=O(\log_2 n)$ |

<p align="justify">
<b>Dato curioso:</b> Introducida por <b>Jon Bentley</b> y <b>Andrew Chi-Chih Yao</b> en 1976 como estrategia para operar sobre listas ordenadas potencialmente infinitas. Su ventaja sobre la búsqueda binaria es que no necesita conocer el tamaño de la estructura de antemano.
</p>

<h3>Escenarios de aplicación</h3>
<ul>
  <li>Estructuras de longitud desconocida (listas vinculadas ordenadas, streams).</li>
  <li>Conjuntos de datos muy grandes donde el objetivo suele estar cerca del inicio.</li>
  <li>Búsquedas donde el costo efectivo depende de la posición del elemento, no del tamaño total.</li>
</ul>

<h3>Ventajas y desventajas</h3>

| Ventajas | Desventajas |
| :---: | :---: |
| Funciona sin conocer el tamaño de la estructura | Dependencia de datos ordenados |
| Muy eficiente cuando el objetivo está cerca del inicio: $O(\log i)$ | Si el rango resultante no es eficiente para búsqueda binaria, la ventaja se diluye |

---

<h2 id="7-7">🔱 7.7 Búsqueda ternaria</h2>

<p align="center">
  🎬 <a href="./6_busqueda_ternaria.ipynb"><b>Abrir simulación</b></a>
</p>

<p align="justify">
La <b>búsqueda ternaria</b> extiende la lógica de la búsqueda binaria dividiendo el rango activo <code>[a, b]</code> en <b>tres segmentos iguales</b> mediante dos puntos de partición:
</p>

<p align="center"><code>m₁ = ⌊a + (b−a)/3⌋</code> &nbsp;&nbsp; <code>m₂ = ⌊b − (b−a)/3⌋</code></p>

<p align="justify">
En cada iteración el objetivo se compara con <code>arr[m₁]</code> y <code>arr[m₂]</code>, descartando dos tercios del espacio o encontrando el elemento en uno de los pivotes.
</p>

<h3>Ejemplo</h3>
<p align="justify">
Buscar el valor <b>8</b> en el arreglo <code>[1, 2, 3, 4, 5, 6, 7, 8]</code> (n=8, a=0, b=7):
</p>
<ul>
  <li>Iteración 1: m₁=2 (arr[2]=3), m₂=4 (arr[4]=5) → 8 &gt; arr[m₂] → [a,b]=[5,7]</li>
  <li>Iteración 2: m₁=5 (arr[5]=6), m₂=6 (arr[6]=7) → 8 &gt; arr[m₂] → [a,b]=[7,7]</li>
  <li>Iteración 3: m₁=m₂=7 (arr[7]=8) → 8 = arr[m₁] ✓ <b>Encontrado</b></li>
</ul>

<h3>Análisis de complejidad</h3>

<p align="justify">
La relación de recurrencia modela exactamente el mismo costo para tiempo y espacio porque el algoritmo es recursivo y el rango siempre se reduce a 1/3 de su tamaño:
</p>
<p align="center">$C(n) = C(n/3) + 1$</p>
<p align="justify">
Aplicando el teorema maestro básico con $a=1$, $b=3$ y $f(n)\in O(1)$ (Caso 2: $a=b^0=1$):
$C(n) \in O(\log_3 (n))$
</p>

| Escenario | $T(n)$ | $S(n)$ | Descripción |
| :---: | :---: | :---: | :---: |
| **Mejor caso** | $\Omega(1)$ | $\Omega(1)$ | El objetivo coincide con m₁ o m₂ en la primera iteración |
| **Caso promedio** | $\Theta(\log_3 (n))$ | $\Theta(\log_3 (n))$ | La reducción a 1/3 ocurre independientemente de la distribución |
| **Peor caso** | $O(\log_3 n)$ | $O(\log_3 n)$ | Máxima profundidad de recursión: $\log_3 n$ niveles |

<p align="justify">
<b>Consideración final del libro:</b> Aunque divide el espacio en tres partes en lugar de dos, la búsqueda ternaria no mejora asintóticamente a la búsqueda binaria. La razón es que $\log_3 (n) = \log_2 (n)/\log_2 (3)$, que solo introduce una constante multiplicativa que desaparece en el análisis asintótico. Dividir en más partes no reduce el orden de crecimiento del algoritmo.
</p>

<p align="justify">
<b>Dato curioso:</b> El origen de la búsqueda ternaria se remonta al análisis matemático de funciones unimodales, donde se emplea para localizar el máximo o mínimo de una función sin necesidad de derivarla (Knuth, 1973).
</p>

<h3>Escenarios de aplicación</h3>
<ul>
  <li>Optimización de funciones unimodales sin derivadas (análisis matemático).</li>
  <li>Algoritmos que aprovechan estrategias de paralelización con dos comparaciones simultáneas.</li>
</ul>

<h3>Ventajas y desventajas</h3>

| Ventajas | Desventajas |
| :---: | :---: |
| Reduce el rango más agresivamente por iteración | Realiza 2 comparaciones por iteración (vs 1 en búsqueda binaria) |
| Versátil: aplica tanto a arreglos como a funciones continuas | Menos eficiente en hardware moderno optimizado para operaciones binarias |

---

<h2 id="7-comp">📊 Comparación de todos los algoritmos</h2>

<p align="center">
  🎬 <a href="./0_comparacion_busquedas.ipynb"><b>Abrir simulación</b></a>
</p>

| Algoritmo | Mejor caso $T(n)$ | Caso promedio $T(n)$ | Peor caso $T(n)$ | $S(n)$ | Requiere orden |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **Secuencial** | $\Omega(1)$ | $\Theta(n)$ | $O(n)$ | $O(1)$ | No |
| **Binaria** | $\Omega(1)$ | $\Theta(\log_2 n)$ | $O(\log_2 n)$ | $O(1)$ | Sí |
| **Interpolación** | $\Omega(1)$ | $\Theta(\log_2 \log_2 n)$ | $O(n)$ | $O(1)$ | Sí + uniforme |
| **Saltos** | $\Omega(1)$ | $\Theta(\sqrt{n})$ | $O(\sqrt{n})$ | $O(1)$ | Sí |
| **Exponencial** | $\Omega(1)$ | $\Theta(\log_2 n)$ | $O(\log_2 n)$ | $O(1)$ | Sí |
| **Ternaria** | $\Omega(1)$ | $\Theta(\log_3 n)$ | $O(\log_3 n)$ | $O(\log_3 n)$ | Sí |

---

<h2 id="7-8">💡 7.8 Consideraciones finales</h2>

<p align="justify">
La elección del algoritmo de búsqueda depende de múltiples factores: el <b>orden y distribución de los datos</b>, la <b>frecuencia de las búsquedas</b> y el <b>tamaño del conjunto de datos</b>. Para conjuntos pequeños, la diferencia entre técnicas es despreciable. Para conjuntos grandes, la distancia entre $O(n)$, $O(\sqrt{n})$, $O(\log_2 n)$ y $O(\log_2\log_2 n)$ se hace enorme, y la elección correcta puede significar la diferencia entre una solución práctica y una impracticable.
</p>

<p align="justify">
Aunque los ejemplos del capítulo se centran en arreglos unidimensionales de enteros, los principios del análisis son directamente aplicables a otras estructuras: colas, pilas, listas, árboles, grafos y tablas hash, ajustando la lógica de cada técnica a las características específicas de la estructura.
</p>

---

<h2 id="7-9">📚 7.9 Ejercicios propuestos</h2>

<p align="justify">
El capítulo propone los siguientes ejercicios para consolidar el análisis de búsqueda:
</p>

<ol>
  <li>Implementar cada algoritmo en el lenguaje de su preferencia y graficar los resultados para los tres casos de complejidad.</li>
  <li>Graficar la función analítica teórica de cada algoritmo y comparar con los resultados experimentales.</li>
</ol>

<p><b>Ejercicios opcionales:</b></p>
<ol>
  <li>Determinar la complejidad temporal y espacial analítica de cada algoritmo usando las herramientas de los capítulos anteriores.</li>
  <li>Estudiar aplicaciones comunes de cada algoritmo de búsqueda.</li>
  <li>Consultar otros algoritmos de búsqueda conocidos y estudiar su complejidad espacial y temporal.</li>
  <li>Estudiar cómo cambia la complejidad de cada algoritmo si se aplica a matrices en lugar de arreglos.</li>
</ol>

<p align="justify">
Se sugiere utilizar entradas en el intervalo $n \in [1,10^{10}]$ para observar el comportamiento asintótico de cada función.
</p>

---

<h2>⚙️ Ejecución local</h2>

<p align="justify">
Para abrir las simulaciones interactivas en local con el código oculto mediante Voilà:
</p>

```bash
python3 capitulo7/runtime/abrir_busqueda.py secuencial
python3 capitulo7/runtime/abrir_busqueda.py binaria
python3 capitulo7/runtime/abrir_busqueda.py interpolacion
python3 capitulo7/runtime/abrir_busqueda.py saltos
python3 capitulo7/runtime/abrir_busqueda.py exponencial
python3 capitulo7/runtime/abrir_busqueda.py ternaria
```

<p align="justify">
También puede abrir los notebooks directamente con Jupyter:
</p>

```bash
jupyter notebook
```

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
