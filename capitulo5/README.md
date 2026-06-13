<h1 style="text-align:center;">
  <strong>Capítulo 5: Relaciones de recurrencia y análisis de complejidad</strong>
</h1>

---

<h2>🧭 Contenido del capítulo</h2>

<ul>
  <li><a href="#5-1">5.1 Relación de recurrencia</a>
    <ul>
      <li><a href="#5-1-1">5.1.1 Contexto histórico</a></li>
      <li><a href="#5-1-2">5.1.2 Definición formal</a></li>
    </ul>
  </li>
  <li><a href="#5-2">5.2 Tipos de relaciones de recurrencia</a>
    <ul>
      <li><a href="#5-2-1">5.2.1 Relaciones lineales y no lineales</a></li>
      <li><a href="#5-2-2">5.2.2 Relaciones homogéneas y no homogéneas</a></li>
      <li><a href="#5-2-3">5.2.3 Relaciones con coeficientes variables</a></li>
    </ul>
  </li>
  <li><a href="#5-3">5.3 Recurrencias y análisis de complejidad</a></li>
  <li><a href="#5-4">5.4 Solución de relaciones de recurrencia</a>
    <ul>
      <li><a href="#5-4-1">5.4.1 Consideración previa</a></li>
      <li><a href="#5-4-2">5.4.2 Sustitución iterativa</a></li>
      <li><a href="#5-4-3">5.4.3 Árbol de recurrencia</a></li>
      <li><a href="#5-4-4">5.4.4 Teorema maestro</a></li>
      <li><a href="#5-4-5">5.4.5 Ecuación característica</a></li>
    </ul>
  </li>
  <li><a href="#5-5">5.5 Consideraciones finales</a></li>
  <li><a href="#5-6">5.5.1 Ejercicios propuestos</a></li>
</ul>

---

<h2 id="5-1">📜 5.1 Relación de recurrencia</h2>

<h3 id="5-1-1">🏛️ 5.1.1 Contexto histórico</h3>

<p align="justify">
Las relaciones de recurrencia tienen raíces profundas en la historia de las matemáticas. <b>Leonardo de Pisa</b> (Fibonacci, 1202) introdujo la sucesión que hoy lleva su nombre al modelar el crecimiento de una población de conejos. Siglos después, <b>Abraham de Moivre</b> (1730) formalizó herramientas para resolver este tipo de relaciones, y <b>Leonhard Euler</b> las aplicó de forma sistemática al estudio de series matemáticas. En la computación moderna, las relaciones de recurrencia se convirtieron en la herramienta natural para describir el costo de los algoritmos recursivos, enlazando la matemática discreta clásica con el análisis algorítmico contemporáneo.
</p>

<h3 id="5-1-2">📐 5.1.2 Definición formal</h3>

<p align="justify">
Una <b>relación de recurrencia</b> es una ecuación que define el término general de una sucesión en función de uno o varios términos anteriores:
</p>

<p align="center"><code>aₙ = f(aₙ₋₁, aₙ₋₂, ..., aₙ₋ₖ)</code></p>

<p align="justify">
La relación no está completamente determinada sin un conjunto de <b>condiciones iniciales</b> que establezcan los valores base de la sucesión. Los ejemplos más paradigmáticos son:
</p>

<ul>
  <li><b>Factorial:</b> <code>aₙ = n · aₙ₋₁</code>, con <code>a₀ = 1</code></li>
  <li><b>Fibonacci:</b> <code>aₙ = aₙ₋₁ + aₙ₋₂</code>, con <code>a₀ = a₁ = 1</code></li>
</ul>

---

<h2 id="5-2">🔣 5.2 Tipos de relaciones de recurrencia</h2>

<h3 id="5-2-1">🔹 5.2.1 Relaciones lineales y no lineales</h3>

<p align="justify">
Una relación es <b>lineal</b> cuando cada término de la sucesión aparece elevado a la primera potencia y los términos no se multiplican entre sí. En caso contrario, la relación es <b>no lineal</b>. El factorial y Fibonacci son ejemplos de relaciones lineales; una relación donde aparece <code>aₙ₋₁ · aₙ₋₂</code> sería no lineal.
</p>

<h3 id="5-2-2">🔹 5.2.2 Relaciones homogéneas y no homogéneas</h3>

<p align="justify">
Una relación lineal es <b>homogénea</b> si todos sus términos involucran la sucesión (no tiene término independiente). Es <b>no homogénea</b> cuando incluye un término adicional <code>g(n)</code> que depende únicamente de <i>n</i>:
</p>

<p align="center"><code>aₙ = a₁·aₙ₋₁ + a₂·aₙ₋₂ + ... + aₖ·aₙ₋ₖ + g(n)</code></p>

<p align="justify">
El caso homogéneo se analiza de forma más directa; el no homogéneo requiere encontrar una solución particular <code>Cₚ(n)</code> y sumarla a la solución homogénea <code>Cₕ(n)</code>.
</p>

<h3 id="5-2-3">🔹 5.2.3 Relaciones con coeficientes variables</h3>

<p align="justify">
Cuando los coeficientes que acompañan a los términos de la sucesión son funciones de <i>n</i> (no constantes), la relación se denomina de <b>coeficientes variables</b>. Estas relaciones son más difíciles de resolver y generalmente requieren técnicas especializadas.
</p>

---

<h2 id="5-3">⚙️ 5.3 Recurrencias y análisis de complejidad</h2>

<p align="justify">
Al analizar un algoritmo recursivo, su función de complejidad <code>C(n)</code> satisface naturalmente una relación de recurrencia. El libro distingue tres formas estructurales según la forma en que el problema se reduce en cada llamada recursiva:
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Tipo</th>
      <th style="padding:8px; border:1px solid #ccc;">Forma general</th>
      <th style="padding:8px; border:1px solid #ccc;">Descripción</th>
      <th style="padding:8px; border:1px solid #ccc;">Ejemplo típico</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Relaciones de reducción</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><code>C(n) = aC(n−b) + f(n)</code></td>
      <td style="padding:8px; border:1px solid #ccc;">El problema se reduce en <i>b</i> unidades en cada paso. Genera un árbol lineal (a=1) o ramificado (a>1).</td>
      <td style="padding:8px; border:1px solid #ccc;">Factorial, Fibonacci</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Relaciones de división</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><code>C(n) = aC(n/b) + f(n)</code></td>
      <td style="padding:8px; border:1px solid #ccc;">El problema se divide por un factor <i>b</i> en cada paso. Genera árboles logarítmicamente profundos.</td>
      <td style="padding:8px; border:1px solid #ccc;">Merge sort, búsqueda binaria</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Relaciones mixtas</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><code>C(n) = Σ aᵢC(bᵢ·n) + f(n)</code>, 0 &lt; bᵢ &lt; 1</td>
      <td style="padding:8px; border:1px solid #ccc;">Combinación de múltiples llamadas que dividen el problema en fracciones distintas.</td>
      <td style="padding:8px; border:1px solid #ccc;">Algoritmos divide y vencerás no uniformes</td>
    </tr>
  </tbody>
</table>

---

<h2 id="5-4">🧮 5.4 Solución de relaciones de recurrencia</h2>

<h3 id="5-4-1">⚠️ 5.4.1 Consideración previa</h3>

<p align="justify">
El libro presenta cuatro métodos para resolver relaciones de recurrencia. Cada uno tiene un dominio de aplicación diferente: la sustitución iterativa y el árbol de recurrencia son adecuados para obtener la solución exacta o una expresión cerrada; el teorema maestro proporciona únicamente el <b>comportamiento asintótico promedio</b> y aplica exclusivamente a relaciones de división; la ecuación característica es el método formal para relaciones de reducción lineales con coeficientes constantes.
</p>

<h3 id="5-4-2">🔁 5.4.2 Sustitución iterativa</h3>

<p align="justify">
La <b>sustitución iterativa</b> consiste en expandir la relación de recurrencia de forma progresiva hasta identificar un patrón general que pueda expresarse en función de <i>n</i> y las condiciones iniciales. El procedimiento tiene tres pasos:
</p>

<ol>
  <li><b>Expandir</b> la relación aplicando la definición recursiva sucesivamente.</li>
  <li><b>Identificar el patrón</b> que emerge tras <i>k</i> sustituciones.</li>
  <li><b>Aplicar la condición inicial</b> para determinar el valor de <i>k</i> en el que la recursión se detiene.</li>
</ol>

<p align="justify">
<b>Ejemplo:</b> Para <code>C(n) = 2C(n/2) + n</code> con <code>C(1) = 1</code>:
</p>

<ul>
  <li>Expansión: <code>C(n) = 2[2C(n/4) + n/2] + n = 4C(n/4) + 2n</code></li>
  <li>Patrón en <i>k</i> pasos: <code>C(n) = 2ᵏC(n/2ᵏ) + kn</code></li>
  <li>Condición inicial: <code>n/2ᵏ = 1 → k = log₂(n)</code></li>
  <li>Resultado: <code>C(n) = n + n·log₂(n) ∈ Θ(n·log₂(n))</code></li>
</ul>

<h3 id="5-4-3">🌳 5.4.3 Árbol de recurrencia</h3>

<p align="justify">
El <b>árbol de recurrencia</b> es una representación visual de la sustitución iterativa. Cada nodo corresponde a una llamada recursiva y sus hijos representan las subproblemas generados. El costo total del algoritmo es la suma de los costos de todos los nodos del árbol.
</p>

<ul>
  <li>Con <i>a = 1</i>: árbol degenerado (lista lineal de llamadas).</li>
  <li>Con <i>a = 2</i>: árbol binario balanceado.</li>
  <li>Con <i>a = k</i>: árbol k-ario.</li>
  <li>La profundidad del árbol es <code>h = log_b(n)</code> para relaciones de división.</li>
  <li>El número de nodos en el nivel <i>j</i> es <code>aʲ</code>.</li>
</ul>

<h3 id="5-4-4">👑 5.4.4 Teorema maestro</h3>

<p align="justify">
El <b>teorema maestro</b> proporciona una fórmula directa para determinar el orden asintótico de relaciones de división <code>C(n) = aC(n/b) + f(n)</code>. El libro presenta tres versiones:
</p>

<h4>Teorema maestro básico</h4>
<p align="justify">
Aplica cuando <code>f(n) ∈ O(nᵏ)</code>. Compara el crecimiento de <code>f(n)</code> con <code>n^(log_b(a))</code>:
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Caso</th>
      <th style="padding:8px; border:1px solid #ccc;">Condición</th>
      <th style="padding:8px; border:1px solid #ccc;">Resultado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Caso 1</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><code>a &gt; bᵏ</code> (recursión domina)</td>
      <td style="padding:8px; border:1px solid #ccc;"><code>C(n) ∈ Θ(n^log_b(a))</code></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Caso 2</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><code>a = bᵏ</code> (ambos iguales)</td>
      <td style="padding:8px; border:1px solid #ccc;"><code>C(n) ∈ Θ(nᵏ·log_b(n))</code></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Caso 3</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><code>a &lt; bᵏ</code> (función externa domina)</td>
      <td style="padding:8px; border:1px solid #ccc;"><code>C(n) ∈ Θ(nᵏ)</code></td>
    </tr>
  </tbody>
</table>

<h4>Teorema maestro extendido</h4>
<p align="justify">
Aplica cuando <code>f(n) ∈ O(nᵏ·log_ℓᵖ(n))</code>, introduciendo cinco casos adicionales que dependen del valor de <i>p</i> y la relación entre <i>a</i> y <i>bᵏ</i>.
</p>

<h4>Teorema maestro generalizado (Akra-Bazzi)</h4>
<p align="justify">
Extiende el teorema a relaciones mixtas de la forma <code>C(n) = Σaᵢ·C(bᵢ·n) + f(n)</code>. Se resuelve encontrando el exponente <i>p</i> tal que <code>Σaᵢ·bᵢᵖ = 1</code>, y luego:
</p>
<p align="center"><code>C(n) ∈ Θ(nᵖ·(1 + ∫₁ⁿ f(u)/u^(p+1) du))</code></p>

<h3 id="5-4-5">🔗 5.4.5 Ecuación característica</h3>

<p align="justify">
El método de la <b>ecuación característica</b> es el enfoque formal para resolver relaciones de reducción lineales con coeficientes constantes de la forma <code>C(n) = Σaᵢ·C(n−i) + g(n)</code>.
</p>

<p align="justify">
<b>Caso homogéneo</b> (<code>g(n) = 0</code>): Se construye la ecuación característica, se calculan sus raíces <code>r₁, r₂, ..., rₖ</code>, y la solución general es una combinación lineal de potencias de esas raíces. La complejidad queda determinada por la raíz de mayor módulo: <code>r* = max|rᵢ|</code>, con <code>C(n) ∈ Θ((r*)ⁿ)</code>.
</p>

<p align="justify">
<b>Caso no homogéneo</b> (<code>g(n) ≠ 0</code>): La solución se compone como <code>C(n) = Cₕ(n) + Cₚ(n)</code>, donde <code>Cₚ(n)</code> es una solución particular propuesta según la forma de <code>g(n)</code> (polinómica, exponencial o mixta, según la Tabla 5.1 del libro).
</p>

---

<h2 id="5-5">💡 5.5 Consideraciones finales</h2>

<p align="justify">
Los cuatro métodos presentados son complementarios. La siguiente tabla resume sus diferencias y criterios de elección:
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Método</th>
      <th style="padding:8px; border:1px solid #ccc;">Tipo de relación</th>
      <th style="padding:8px; border:1px solid #ccc;">Resultado</th>
      <th style="padding:8px; border:1px solid #ccc;">Observación</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Sustitución iterativa</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Reducción y división</td>
      <td style="padding:8px; border:1px solid #ccc;">Exacto</td>
      <td style="padding:8px; border:1px solid #ccc;">Requiere identificar el patrón manualmente</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Árbol de recurrencia</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Reducción y división</td>
      <td style="padding:8px; border:1px solid #ccc;">Exacto o aproximado</td>
      <td style="padding:8px; border:1px solid #ccc;">Visualmente intuitivo; útil para verificar otros métodos</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Teorema maestro</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Solo división</td>
      <td style="padding:8px; border:1px solid #ccc;">Asintótico</td>
      <td style="padding:8px; border:1px solid #ccc;">Rápido; no aplica en todos los casos</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Ecuación característica</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Solo reducción lineal</td>
      <td style="padding:8px; border:1px solid #ccc;">Exacto</td>
      <td style="padding:8px; border:1px solid #ccc;">Formal y riguroso; requiere resolver polinomios</td>
    </tr>
  </tbody>
</table>

---

<h2 id="5-6">📚 5.5.1 Ejercicios propuestos</h2>

<p align="justify">
El capítulo incluye <b>15 ejercicios propuestos</b> que cubren los cuatro métodos de solución. Los ejercicios están diseñados para que el lector practique:
</p>

<ul>
  <li>Plantear relaciones de recurrencia a partir de un algoritmo recursivo.</li>
  <li>Seleccionar el método de resolución adecuado para cada tipo de relación.</li>
  <li>Aplicar el teorema maestro básico, extendido y generalizado.</li>
  <li>Resolver ecuaciones características homogéneas y no homogéneas.</li>
  <li>Derivar la expresión cerrada de la complejidad y verificarla.</li>
</ul>

<p align="justify">
Se sugiere utilizar entradas en el intervalo <code>n ∈ [1, 10¹⁰]</code> para contrastar los resultados teóricos con comportamientos empíricos.
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
