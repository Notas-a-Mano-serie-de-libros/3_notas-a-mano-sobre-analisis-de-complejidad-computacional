<h1 style="text-align:center;">
  <strong>Capítulo 2: Fundamentos del análisis de algoritmos</strong>
</h1>

<p align="justify">
El <b>análisis de complejidad computacional</b> es una rama de la informática dedicada a estudiar la dificultad intrínseca de los problemas computacionales, clasificándolos según los recursos necesarios para resolverlos de forma eficiente. En términos generales, esta herramienta resulta poderosa en múltiples contextos: <b>evaluación de eficiencia</b>, <b>comparación entre algoritmos</b> y <b>detección temprana de problemas</b>. Para el enfoque introductorio de esta obra, el análisis se centrará en dos aspectos específicos: <b>tiempo</b> y <b>consumo de recursos</b>.
</p>

---

<h2>🧭 Contenido del capítulo</h2>

<ul>
  <li><a href="#2-1">2.1 Función de complejidad</a>
    <ul>
      <li><a href="#2-1-1">2.1.1 Propiedades básicas</a></li>
      <li><a href="#2-1-2">2.1.2 Funciones de complejidad teóricas comunes</a></li>
      <li><a href="#2-1-3">2.1.3 Análisis teórico de complejidad</a></li>
      <li><a href="#2-1-4">2.1.4 Análisis práctico de complejidad temporal</a></li>
      <li><a href="#2-1-5">2.1.5 Errores comunes en el análisis de complejidad</a></li>
      <li><a href="#2-1-6">2.1.6 Consideraciones finales</a></li>
    </ul>
  </li>
  <li><a href="#2-2">2.2 Ejercicios propuestos</a></li>
</ul>

---

<h2 id="2-1">📐 2.1 Función de complejidad</h2>

<p align="justify">
En términos generales, la complejidad computacional de un problema se describe a través de una relación que determina el comportamiento de un parámetro de interés a medida que cambia la cantidad de datos que recibe como entrada. El análisis se enfoca en dos dimensiones:
</p>

<ul>
  <li><b>Complejidad temporal:</b> analiza cómo varía el tiempo de ejecución:
    <p style="text-align:center; font-family:monospace;">T : ℕ → ℝ₀⁺, &nbsp;&nbsp; n ↦ T(n)</p>
  </li>
  <li><b>Complejidad espacial:</b> estudia cómo varía el consumo de memoria:
    <p style="text-align:center; font-family:monospace;">S : ℕ → ℝ₀⁺, &nbsp;&nbsp; n ↦ S(n)</p>
  </li>
</ul>

<p align="justify">
Donde <b>n ∈ ℕ</b> representa la cantidad de datos que recibe el algoritmo (longitud de la representación en bits, número de elementos, número de nodos, tamaño de entrada). Las funciones <b>T(n)</b> y <b>S(n)</b> son adimensionales y describen cómo varían el tiempo de ejecución y el consumo de memoria, respectivamente. Para generalizar, se introduce la notación unificada:
</p>

<p style="text-align:center; font-family:monospace;">C(n) = T(n) : Complejidad temporal &nbsp;|&nbsp; C(n) = S(n) : Complejidad espacial</p>

---

<h2 id="2-1-1">🔢 2.1.1 Propiedades básicas</h2>

<p align="justify">
Las funciones de complejidad describen una evolución ordenada y sin fluctuaciones bruscas. Para ello deben cumplir tres propiedades:
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Propiedad</th>
      <th style="padding:8px; border:1px solid #ccc;">Definición formal</th>
      <th style="padding:8px; border:1px solid #ccc;">Significado práctico</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Restricción del dominio</b></td>
      <td style="padding:8px; border:1px solid #ccc; font-family:monospace;">C : ℕ → ℝ₀⁺, n ↦ C(n) para n ≥ 0</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">El análisis se limita a escenarios válidos. No tiene sentido hablar de n = −2 elementos o n = 3,7 nodos.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Crecimiento monótono</b></td>
      <td style="padding:8px; border:1px solid #ccc; font-family:monospace;">∀n₁,n₂ ∈ ℕ : n₁ ≤ n₂ ⟹ C(n₁) ≤ C(n₂)</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">El costo no disminuye al aumentar la entrada. Funciones decrecientes como sin(x) o e⁻ˣ no tienen sentido en este contexto.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Representación asintótica</b></td>
      <td style="padding:8px; border:1px solid #ccc; font-family:monospace;">C(n) debe reflejar el crecimiento cuando n → ∞</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Habilita el uso de la notación asintótica (Capítulo 3) para comparar algoritmos independientemente del hardware.</td>
    </tr>
  </tbody>
</table>

---

<h2 id="2-1-2">📊 2.1.2 Funciones de complejidad teóricas comunes</h2>

<p align="justify">
En la Tabla 2.1 se presentan las funciones de complejidad más comunes. Para funciones con factor logarítmico se asume generalmente ℓ = 2, ya que muchos procesos computacionales se apoyan en representaciones binarias.
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc; text-align:center;">C(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">Tipo</th>
      <th style="padding:8px; border:1px solid #ccc;">Descripción</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">1</td>
      <td style="padding:8px; border:1px solid #ccc;">Constante</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">La función no depende del tamaño de la entrada.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">log<sub>ℓ</sub>(n)</td>
      <td style="padding:8px; border:1px solid #ccc;">Logarítmico</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">La función crece logarítmicamente con el tamaño de la entrada, donde ℓ ∈ ℝ⁺, ℓ ≠ 1.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">n</td>
      <td style="padding:8px; border:1px solid #ccc;">Lineal</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">La función es proporcional al tamaño de la entrada.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">n·log<sub>ℓ</sub>(n)</td>
      <td style="padding:8px; border:1px solid #ccc;">Log-lineal</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Combinación entre un factor lineal y uno logarítmico, donde ℓ ∈ ℝ⁺, ℓ ≠ 1.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">n²</td>
      <td style="padding:8px; border:1px solid #ccc;">Cuadrático</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">La función crece con el cuadrado del tamaño de la entrada.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">n³</td>
      <td style="padding:8px; border:1px solid #ccc;">Cúbico</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">La función crece con el cubo del tamaño de la entrada.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">n<sup>k</sup></td>
      <td style="padding:8px; border:1px solid #ccc;">Polinomial</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Crece con la potencia k-ésima del tamaño de entrada, donde k ∈ ℝ₀⁺. Los casos constante (n⁰), lineal (n¹), cuadrático (n²) y cúbico (n³) son casos particulares.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">2<sup>n</sup></td>
      <td style="padding:8px; border:1px solid #ccc;">Exponencial</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">La función crece exponencialmente, duplicándose por cada incremento unitario en n.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">a<sup>n</sup></td>
      <td style="padding:8px; border:1px solid #ccc;">Exponencial general</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Crece exponencialmente con base a, aumentando en un factor constante a por cada incremento unitario, donde a ∈ ℝ⁺, a > 1.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">n!</td>
      <td style="padding:8px; border:1px solid #ccc;">Factorial</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">La función crece factorialmente con el tamaño de la entrada.</td>
    </tr>
  </tbody>
</table>

<p style="margin-top:0.8em;">
  🔗 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/general/comparacion_complejidades_teoricas.ipynb"><b>Notebook – Comparación de complejidades teóricas (Figura 2.1 y 2.2)</b></a><br/>
  🔗 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/general/complejidad_polinomica.ipynb"><b>Notebook – Complejidad polinómica (Figuras 2.21 y 2.22)</b></a>
</p>

---

<h2 id="2-1-3">🧮 2.1.3 Análisis teórico de complejidad</h2>

<p align="justify">
El análisis teórico establece que el tiempo de ejecución y el consumo de recursos se expresan como el producto de una medida constante por la función de complejidad asociada:
</p>

<p style="text-align:center; font-family:monospace;">
  t ≈ T₀ · T(n) &nbsp;&nbsp; donde T₀ = 10⁻⁶ [s] = 1 [μs]<br/>
  s ≈ S₀ · S(n) &nbsp;&nbsp; donde S₀ = 1 [byte]
</p>

<p align="justify">
Las unidades de medida fueron elegidas de manera intencional: una instrucción simple toma aproximadamente 1 microsegundo en ejecutarse, mientras que el byte es la unidad estándar para cuantificar la información en un sistema. Esta simplificación tiene un propósito ilustrativo; en la práctica, el costo real depende de múltiples factores (arquitectura del procesador, sistema operativo, distribución de los datos, entre otros).
</p>

<h3>⏱️ Complejidad temporal teórica — Tabla 2.2 y 2.3</h3>

<table style="width:100%; border-collapse:collapse; margin-top:0.5em; font-size:0.93em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:7px; border:1px solid #ccc;">n (datos)</th>
      <th style="padding:7px; border:1px solid #ccc; text-align:center;">T(n) = 1</th>
      <th style="padding:7px; border:1px solid #ccc; text-align:center;">T(n) = log₂(n)</th>
      <th style="padding:7px; border:1px solid #ccc; text-align:center;">T(n) = n</th>
      <th style="padding:7px; border:1px solid #ccc; text-align:center;">T(n) = n·log₂(n)</th>
      <th style="padding:7px; border:1px solid #ccc; text-align:center;">T(n) = n²</th>
      <th style="padding:7px; border:1px solid #ccc; text-align:center;">T(n) = n³</th>
      <th style="padding:7px; border:1px solid #ccc; text-align:center;">T(n) = 2ⁿ</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁰</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻⁶ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">0</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻⁶ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">0</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻⁶ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻⁶ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">2·10⁻⁶ s</td>
    </tr>
    <tr>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10¹</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻⁶ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">3,32·10⁻⁶ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻⁵ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">3,32·10⁻⁵ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻⁴ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻³ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">1,02·10⁻³ s</td>
    </tr>
    <tr>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10²</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻⁶ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">6,64·10⁻⁶ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻⁴ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">6,64·10⁻⁴ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻² s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">1 s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">1,27·10²⁴ s</td>
    </tr>
    <tr>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10³</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻⁶ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">9,97·10⁻⁶ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻³ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">9,97·10⁻³ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">1 s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10³ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">1,07·10²⁹⁵ s</td>
    </tr>
    <tr>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁴</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻⁶ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">1,33·10⁻⁵ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻² s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">1,33·10⁻¹ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10² s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁶ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">2,00·10³⁰⁰⁴ s</td>
    </tr>
    <tr>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁷</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10⁻⁶ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">2,33·10⁻⁵ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">10¹ s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">2,33·10² s</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">— ∞ —</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">— ∞ —</td>
      <td style="padding:7px; border:1px solid #ccc; text-align:center;">— ∞ —</td>
    </tr>
  </tbody>
</table>

<blockquote>
💡 <b>Dato curioso:</b> T(n) = 2ⁿ supera la edad estimada del universo (4,17·10¹⁷ [s] ≈ 13 800 millones de años) para apenas n = 100 datos. Los problemas exponenciales son, en la práctica, computacionalmente inabordables más allá de entradas pequeñas.
</blockquote>

<p style="margin-top:0.8em;">
  🔗 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_eficiencia/complejidad_temporal/analisis_alta_complejidad.ipynb"><b>Notebook – Análisis de alta complejidad temporal (Figuras 2.3–2.6)</b></a><br/>
  🔗 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_eficiencia/complejidad_espacial/analisis_alta_complejidad.ipynb"><b>Notebook – Análisis de alta complejidad espacial (Figuras 2.7–2.10)</b></a>
</p>

---

<h2 id="2-1-4">🔬 2.1.4 Análisis práctico de complejidad temporal</h2>

<p align="justify">
Las siguientes subsecciones presentan ejemplos que evalúan el tiempo de ejecución experimental de varios problemas comunes. Con el objetivo de obtener mediciones representativas, todas las soluciones se ejecutaron un número fijo de veces para cada tamaño de entrada específico; los tiempos reportados corresponden al promedio aritmético de dichas ejecuciones.
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Subsección</th>
      <th style="padding:8px; border:1px solid #ccc;">Ejemplo canónico</th>
      <th style="padding:8px; border:1px solid #ccc; text-align:center;">T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">Notebook Colab</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>2.1.4.1</b> Constante</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Acceso a la posición i-ésima de un arreglo. La máquina calcula la dirección de memoria en una sola instrucción gracias a la dirección base, el tipo de dato y la cantidad de elementos.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><b>O(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/1_complejidad_constante.ipynb">🔗 Abrir</a></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>2.1.4.2</b> Logarítmica</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Búsqueda binaria en un arreglo ordenado. El algoritmo reduce el tamaño del problema a la mitad en cada paso, alcanzando T(n) = log₂(n). Eficiente incluso para entradas de tamaño 10¹⁰⁰ (un googol).</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><b>O(log₂ n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/2_complejidad_logaritmica.ipynb">🔗 Abrir</a></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>2.1.4.3</b> Lineal</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Búsqueda secuencial en una lista desordenada. En el peor caso, el algoritmo debe recorrer toda la estructura para encontrar el valor o confirmar su ausencia: n operaciones totales.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><b>O(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/3_complejidad_lineal.ipynb">🔗 Abrir</a></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>2.1.4.4</b> Log-lineal</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Ordenamiento basado en montículos (heap sort iterativo). Convierte el arreglo en un montículo y extrae el elemento máximo o mínimo repetidamente. Un montículo es una estructura de datos no lineal con orden parcial.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><b>O(n·log₂ n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/4_complejidad_log_lineal.ipynb">🔗 Abrir</a></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>2.1.4.5–6</b> Cuadrática</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Recorrido de una matriz cuadrada n × n. Requiere dos ciclos anidados: uno para las filas y otro para las columnas. El número de operaciones crece como el cuadrado del tamaño de la entrada.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><b>O(n²)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/5_complejidad_cuadratica.ipynb">🔗 Abrir</a></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>2.1.4.7</b> Cúbica</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Multiplicación de matrices A<sub>m×p</sub> · B<sub>p×n</sub>. Requiere tres ciclos anidados: recorrer filas de A, columnas de B y acumular el producto punto entre la fila i y la columna j. C<sub>ij</sub> = Σ a<sub>ik</sub>·b<sub>kj</sub>.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><b>O(n³)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/6_complejidad_cubica.ipynb">🔗 Abrir</a></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>2.1.4.8</b> Exponencial</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Sucesión de Fibonacci recursiva. Cada llamada genera dos llamadas adicionales; la cadena de invocaciones crece de forma binaria hasta alcanzar el caso base. Se puede demostrar que el algoritmo realiza como máximo 2ⁿ operaciones.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><b>O(2ⁿ)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/7_complejidad_exponencial.ipynb">🔗 Abrir</a></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>2.1.4.9</b> Factorial</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Generación de todas las permutaciones posibles de una lista. El algoritmo genera cada posible reordenamiento de los n elementos, explorando todas las configuraciones posibles de la lista. El tiempo alcanza los 12 segundos para apenas 10 datos.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><b>O(n!)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/8_complejidad_factorial.ipynb">🔗 Abrir</a></td>
    </tr>
  </tbody>
</table>

<blockquote>
💡 <b>Dato curioso:</b> El número 10¹⁰⁰, conocido como <b>gúgol</b> o <b>googol</b>, fue definido por el matemático <b>Edward Kasner</b> para ilustrar que cualquier número, sin importar su magnitud, sigue siendo finito. Años más tarde, los fundadores de <b>Google</b> tomaron el término como inspiración para nombrar a su motor de búsqueda.
</blockquote>

<blockquote>
💡 <b>Dato curioso:</b> El número de partidas posibles en el ajedrez, conocido como el <b>número de Shannon</b>, es del orden de 10¹²⁰ (Shannon, 1950). Una cadena de ADN de 250 bases puede generar 4²⁵⁰ ≈ 1,8×10¹⁵⁰ combinaciones posibles, ya que cada posición admite cuatro posibles bases: A, C, G o T.
</blockquote>

---

<h2 id="2-1-5">⚠️ 2.1.5 Errores comunes en el análisis de complejidad</h2>

<p align="justify">
El análisis de problemas suele estar sujeto a errores sutiles que pueden conducir a conclusiones equivocadas. A continuación se detallan los más frecuentes:
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Error</th>
      <th style="padding:8px; border:1px solid #ccc;">Descripción</th>
      <th style="padding:8px; border:1px solid #ccc;">Consecuencia</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Subestimar el tiempo de ejecución</b></td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Los avances en hardware generan la falsa impresión de que las limitaciones algorítmicas siempre pueden resolverse con más recursos.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Soluciones inviables en entornos con restricciones de procesamiento.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Ignorar la complejidad espacial</b></td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Muchos cometen el error de pensar que la capacidad de procesamiento actual justifica ignorar el análisis espacial.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Un uso ineficiente de los recursos puede tener consecuencias significativas para un sistema.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Descuidar los efectos del entorno</b></td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">La arquitectura del procesador, la jerarquía de memoria o el sistema operativo pueden influir significativamente en el rendimiento.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Análisis incompletos o conclusiones erróneas al no considerar el entorno real.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Asumir que el comportamiento promedio es representativo</b></td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Muchos problemas presentan diferencias marcadas cuando la cantidad o distribución de datos cambia, lo que puede impactar decisiones críticas.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Ignorar casos extremos que determinan la viabilidad real del algoritmo.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Priorizar resultados empíricos sobre el análisis teórico</b></td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Confiar exclusivamente en pruebas experimentales sin respaldo teórico puede ser riesgoso, ya que los resultados están condicionados por múltiples factores del entorno.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Conclusiones de carácter general limitadas o incorrectas.</td>
    </tr>
  </tbody>
</table>

---

<h2 id="2-1-6">💡 2.1.6 Consideraciones finales</h2>

<p align="justify">
Este capítulo ha introducido los principios básicos del análisis de complejidad computacional, tanto temporal como espacial, proporcionando las herramientas necesarias para entender cómo varía el costo de un problema cuando la cantidad de datos que recibe como entrada cambia.
</p>

<p align="justify">
El <b>análisis temporal</b> permite anticipar la eficiencia del algoritmo y predecir su comportamiento en distintos escenarios. El <b>análisis espacial</b> cobra relevancia en sistemas con recursos limitados, como dispositivos embebidos o aplicaciones en tiempo real. Ambos tipos de complejidad se estudiaron bajo la suposición de un consumo constante de tiempo y recursos (T₀, S₀), una aproximación conveniente para simplificar el análisis funcional desde una perspectiva teórica.
</p>

<p align="justify">
Como se verá más adelante (Capítulo 3), calcular el tiempo de ejecución y el uso de recursos de un algoritmo implica considerar factores adicionales, lo que da lugar a expresiones analíticas menos triviales expresadas mediante <b>notación asintótica</b>.
</p>

---

<h2 id="2-2">🧠 2.2 Ejercicios propuestos</h2>

<p align="justify">
Los ejercicios han sido diseñados para resolver problemas de cálculo de complejidad utilizando valores canónicos de tiempo y recursos. Para facilitar los cálculos, se puede apoyar en las expresiones simplificadas <b>t = T₀ · T(n)</b> y <b>s = S₀ · S(n)</b>.
</p>

<ol>
  <li>Una máquina consume 0,001 [s] por operación y 8 [bytes] de memoria por instrucción. Calcular el tiempo total y el consumo total para T(n) = n, S(n) = n; T(n) = n log₂(n), S(n) = log₂(n); T(n) = √n, S(n) = log₂(n) con n = 10⁶.</li>
  <li>Una operación básica toma en promedio 0,002 [s] y T(n) = n³. Para n = 500, determinar: (i) tiempo total de ejecución; (ii) cuántas instrucciones puede ejecutar antes de consumir 1 [GB] si consume 16 [bytes] por operación.</li>
  <li>Un algoritmo tiene T(n) = 2ⁿ y S(n) = n!. Con T₀ = 0,0005 [s] y S₀ = 4 [bytes], determinar tiempo y consumo para n ∈ {1, 10, 100, 1000, 10000} y discutir los resultados.</li>
  <li>Un sistema necesita procesar n = 10⁶ datos en menos de 10 [s]. La máquina ejecuta instrucciones a 0,001 [s] por instrucción. Determinar la función de complejidad temporal más adecuada que cumpla con estas restricciones.</li>
  <li>Suponga que tiene tres algoritmos: A₁(n) → T₁(n) = n log₂(n), A₂(n) → T₂(n) = n², A₃(n) → T₃(n) = 10n². Si n = 10⁵ y T₀ = 0,002 [s], determinar el tiempo de ejecución de cada algoritmo y cuál demora menos en procesar 5000 datos.</li>
  <li>Diseñar un algoritmo que procese 10⁷ datos en menos de 5 [s]. Determinar un conjunto de funciones de complejidad que cumplan con esta restricción.</li>
  <li>Por restricciones físicas, una máquina solo cuenta con 128 [MB] de memoria. Determinar la complejidad tentativa que debe tener un algoritmo capaz de procesar 10⁵ datos en esta máquina.</li>
  <li>Estimar el tiempo de ejecución para procesar 10⁶ datos usando T(n) = n!, asumiendo que cada instrucción toma 10⁻⁵ [s].</li>
  <li>Un algoritmo con S(n) = n log₂(n) consume 16 [bytes] en cada operación. Determinar cuántos kilobytes y kibibytes consume si recibe 10000 datos como entrada.</li>
  <li>Calcular cuánto tiempo tomaría procesar 20 datos en un algoritmo con T(n) = 2ⁿ, asumiendo que cada instrucción toma 1 [s]. ¿Es útil en la práctica?</li>
  <li>Un algoritmo con T(n) = n² tarda 0,01 [s] en procesar 1000 datos. Estimar el tiempo para procesar 100000 datos, asumiendo que el comportamiento se mantiene estable.</li>
  <li>Se requiere implementar un algoritmo que procese 10000 datos en menos de 1 [s]. Identificar qué órdenes de complejidad temporal lo permitirían en una máquina que ejecuta 10⁷ instrucciones por segundo.</li>
  <li>Un sistema de distribución utiliza S(n) = 2ⁿ y logra procesar 20 datos sin inconvenientes. Determinar cuánta memoria requeriría para 25 datos, expresando el resultado en una unidad adecuada.</li>
  <li>Un sistema embebido es capaz de realizar 10⁶ operaciones por segundo, con solo 1 [MB] de memoria. Determinar qué órdenes de complejidad temporal y espacial permitirían procesar 5000 datos de forma eficiente.</li>
  <li>Un algoritmo con T(n) = n log₂(n) tarda 2 [s] en procesar 1000 datos. Estimar si es posible procesar 10000 datos en menos de 10 [s] bajo el mismo modelo.</li>
</ol>

<p align="center">
  <a href="https://drive.google.com/file/d/16_BOFsSW8auL9230VSRZU79gesjlDzpW/view" target="_blank">
    <b>📄 Ver soluciones – Ejercicios propuestos del Capítulo 2</b>
  </a>
</p>

---

<h2>🧾 Licencia</h2>

<div style="border-left:4px solid #999; padding:1em; background-color:#fafafa; border-radius:6px;">
<p style="text-align:justify; color:#333;">
El contenido de este capítulo se distribuye bajo la licencia
<b>Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)</b>.
Se autoriza su uso y adaptación con fines académicos siempre que se cite la fuente original.
</p>
<p style="text-align:center; font-weight:600; margin-top:0.5em;">
© 2026 Carlos Eduardo Orozco Garcés, César Jesús Pardo Calvache, Mauro Callejas Cuervo
</p>
</div>
