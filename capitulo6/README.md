<h1 style="text-align:center;">
  <strong>Capítulo 6: Análisis de algoritmos recursivos</strong>
</h1>

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
  <li><a href="#6-5">6.4.1 Ejercicios propuestos</a></li>
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

<pre><code>f(n) = { 1           si n ∈ [0, 1]
        { n · f(n−1)  si n &gt; 1</code></pre>

<p align="justify">
Y la sucesión de Fibonacci:
</p>

<pre><code>f(n) = { 1              si n ∈ [0, 1]
        { f(n−1)+f(n−2)  si n &gt; 1</code></pre>

---

<h2 id="6-2">⏱️ 6.2 Análisis temporal y espacial</h2>

<p align="justify">
El capítulo introduce una <b>metodología de 4 pasos</b> para construir la relación de recurrencia que modela el costo de un algoritmo recursivo:
</p>

<h3 id="6-2-1">🕐 6.2.1 Complejidad temporal</h3>

<ol>
  <li><b>Caracterizar el caso base:</b> determinar <code>T_base(n)</code>, el costo de ejecutar el algoritmo sin realizar llamadas recursivas.</li>
  <li><b>Sumar las llamadas recursivas:</b> <code>T_recursivo(n) = Σ aᵢ·Tᵢ(n)</code>, donde cada término representa una llamada con su coeficiente.</li>
  <li><b>Calcular el costo de las operaciones propias:</b> <code>f(n) = Σ Tⱼ(n)</code>, el costo de las instrucciones que no son llamadas recursivas.</li>
  <li><b>Construir la relación completa:</b> <code>T(n) = T_base(n) + T_recursivo(n) + f(n)</code>.</li>
</ol>

<h3 id="6-2-2">💾 6.2.2 Complejidad espacial</h3>

<p align="justify">
Para la complejidad espacial, el procedimiento es análogo pero modelando el consumo de la pila de llamadas (<i>call stack</i>):
</p>

<ol>
  <li>Identificar el espacio requerido por el caso base: <code>S_base(n) = s(n)</code>.</li>
  <li>Determinar la profundidad máxima de la recursión: <code>S_recursivo(n) = d(n)</code>.</li>
  <li>Sumar el costo de estructuras auxiliares declaradas en cada llamada: <code>f(n) = Σ Sⱼ(n)</code>.</li>
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

<pre><code>T(n) = { 1         si n ≤ 1
        { T(n−1)+1  si n &gt; 1</code></pre>

<p align="justify">
Los tres métodos del Capítulo 5 producen el mismo resultado:
</p>

<ul>
  <li><b>Sustitución iterativa:</b> <code>T(n) = 1 + 1 + ... + 1</code> (n veces) → <code>T(n) ∈ Θ(n)</code></li>
  <li><b>Árbol de recurrencia:</b> árbol lineal de profundidad <i>n</i>, costo 1 por nodo → <code>T(n) ∈ Θ(n)</code></li>
  <li><b>Ecuación característica:</b> raíz única <code>r = 1</code> → <code>T(n) ∈ Θ(n)</code></li>
</ul>

<p align="justify">
La complejidad espacial también es lineal porque la pila de llamadas acumula <i>n</i> marcos activos simultáneamente: <code>S(n) ∈ Θ(n)</code>.
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Escenario</th>
      <th style="padding:8px; border:1px solid #ccc;">T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">S(n)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Todos los casos</td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n)</b></td>
    </tr>
  </tbody>
</table>

<h3 id="6-3-2">🌀 6.3.2 Sucesión de Fibonacci</h3>

<p align="justify">
La sucesión de Fibonacci es el ejemplo paradigmático de la <b>explosión exponencial</b> en algoritmos recursivos ingenuos. Su relación de recurrencia es:
</p>

<pre><code>T(n) = { 1              si n ∈ [0, 1]
        { T(n−1)+T(n−2)+1  si n &gt; 1</code></pre>

<p align="justify">
Dado que la ecuación característica exacta produce raíces irracionales, el análisis se realiza en dos niveles:
</p>

<ul>
  <li><b>Cota superior aproximada:</b> aproximando el árbol de recursión por un árbol binario completo de profundidad <i>n</i>, se obtiene <code>T(n) ∈ O(2ⁿ)</code>.</li>
  <li><b>Resultado exacto:</b> la ecuación característica <code>r² − r − 1 = 0</code> produce la raíz <code>φ = (1+√5)/2 ≈ 1.618</code> (la proporción áurea), dando <code>T(n) ∈ Θ(φⁿ)</code>.</li>
</ul>

<p align="justify">
La implementación recursiva directa es <b>exponencialmente ineficiente</b>: recalcula los mismos subproblemas millones de veces. Esta ineficiencia se elimina con técnicas de programación dinámica o memoización, que reducen el costo a <code>Θ(n)</code>.
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Escenario</th>
      <th style="padding:8px; border:1px solid #ccc;">T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">S(n)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Todos los casos</td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(φⁿ)</b> ≈ <b>O(2ⁿ)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n)</b></td>
    </tr>
  </tbody>
</table>

<h3 id="6-3-3">⚡ 6.3.3 Potencia de un número entero positivo</h3>

<p align="justify">
El cálculo de <code>bⁿ</code> de forma recursiva puede implementarse de dos maneras con complejidades radicalmente distintas:
</p>

<ul>
  <li><b>Recursión simple:</b> <code>potencia(b, n) = b · potencia(b, n−1)</code>, con caso base <code>potencia(b, 0) = 1</code>. Genera una cadena lineal de <i>n</i> llamadas → <code>T(n) ∈ Θ(n)</code>, <code>S(n) ∈ Θ(n)</code>.</li>
  <li><b>Exponenciación rápida:</b> divide el exponente a la mitad en cada paso usando la identidad <code>bⁿ = (b^(n/2))²</code>. La recurrencia resultante es <code>T(n) = T(n/2) + 1</code>, cuya solución por teorema maestro (Caso 2: a=1, b=2, k=0, a=b⁰=1) da <code>T(n) ∈ Θ(log₂(n))</code>.</li>
</ul>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Implementación</th>
      <th style="padding:8px; border:1px solid #ccc;">T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">S(n)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Recursión simple</td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n)</b></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Exponenciación rápida</td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(log₂(n))</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(log₂(n))</b></td>
    </tr>
  </tbody>
</table>

<h3 id="6-3-4">🔀 6.3.4 Ordenamiento por mezcla</h3>

<p align="justify">
El <i>merge sort</i> es el ejemplo arquetípico de la estrategia <b>divide y vencerás</b> en ordenamiento. El algoritmo divide el arreglo en dos mitades, ordena cada una recursivamente y luego las fusiona en tiempo lineal:
</p>

<pre><code>T(n) = { 1             si n ≤ 1
        { 2T(n/2) + n   si n &gt; 1</code></pre>

<p align="justify">
Aplicando el <b>teorema maestro básico</b> con <code>a=2, b=2, f(n)∈O(n¹)</code>:
</p>

<ul>
  <li>Se compara <i>a</i> con <i>bᵏ</i>: <code>2 = 2¹</code> → Caso 2 (igualdad)</li>
  <li>Resultado: <code>T(n) ∈ Θ(n·log₂(n))</code></li>
</ul>

<p align="justify">
La complejidad espacial es lineal porque se requiere un arreglo auxiliar del mismo tamaño para la fase de mezcla: <code>S(n) ∈ Θ(n)</code>.
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Escenario</th>
      <th style="padding:8px; border:1px solid #ccc;">T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">S(n)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Todos los casos</td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n·log₂(n))</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n)</b></td>
    </tr>
  </tbody>
</table>

<h3 id="6-3-5">🌲 6.3.5 Búsqueda en árbol binario</h3>

<p align="justify">
La búsqueda recursiva en un árbol binario de búsqueda (BST) descarta la mitad de los nodos en cada llamada cuando el árbol está <b>balanceado</b>. La relación de recurrencia en ese caso es:
</p>

<pre><code>T(n) = { 1         si n = 0 (árbol vacío)
        { T(n/2)+1  si n &gt; 0 (árbol balanceado)</code></pre>

<p align="justify">
Esta es la misma recurrencia que la búsqueda binaria sobre arreglos. El teorema maestro (Caso 2 con <code>a=1, b=2, k=0</code>) da <code>T(n) ∈ Θ(log₂(n))</code>. Sin embargo, en el <b>peor caso</b> (árbol completamente degenerado, equivalente a una lista enlazada), la búsqueda visita todos los nodos: <code>T(n) ∈ O(n)</code>.
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Escenario</th>
      <th style="padding:8px; border:1px solid #ccc;">T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">S(n)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Mejor caso</td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Ω(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Ω(1)</b></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Caso promedio (balanceado)</td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(log₂(n))</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(log₂(n))</b></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Peor caso (degenerado)</td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(n)</b></td>
    </tr>
  </tbody>
</table>

---

<h2>📊 Resumen de complejidades</h2>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Algoritmo</th>
      <th style="padding:8px; border:1px solid #ccc;">Recurrencia</th>
      <th style="padding:8px; border:1px solid #ccc;">T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">S(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">Método de resolución</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Factorial</td>
      <td style="padding:8px; border:1px solid #ccc;"><code>T(n)=T(n−1)+1</code></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Sustitución, árbol, ec. característica</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Fibonacci (naïve)</td>
      <td style="padding:8px; border:1px solid #ccc;"><code>T(n)=T(n−1)+T(n−2)+1</code></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(φⁿ)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Ecuación característica</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Potencia simple</td>
      <td style="padding:8px; border:1px solid #ccc;"><code>T(n)=T(n−1)+1</code></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Sustitución iterativa</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Potencia rápida</td>
      <td style="padding:8px; border:1px solid #ccc;"><code>T(n)=T(n/2)+1</code></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(log₂(n))</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(log₂(n))</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Teorema maestro (Caso 2)</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">Merge sort</td>
      <td style="padding:8px; border:1px solid #ccc;"><code>T(n)=2T(n/2)+n</code></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n·log₂(n))</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Teorema maestro (Caso 2)</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">BST (balanceado)</td>
      <td style="padding:8px; border:1px solid #ccc;"><code>T(n)=T(n/2)+1</code></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(log₂(n))</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Θ(log₂(n))</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Teorema maestro (Caso 2)</td>
    </tr>
  </tbody>
</table>

---

<h2 id="6-4">💡 6.4 Consideraciones finales</h2>

<p align="justify">
El análisis de algoritmos recursivos pone en evidencia una tensión fundamental: la elegancia y claridad del código recursivo suelen contrastar con un mayor consumo de recursos. La pila de llamadas introduce un costo espacial implícito que los algoritmos iterativos no tienen. Esta observación es central al escoger entre implementaciones recursivas e iterativas de un mismo problema.
</p>

<p align="justify">
Asimismo, el capítulo subraya que identificar correctamente el tipo de relación de recurrencia (reducción, división o mixta) es el paso más crítico del análisis, pues determina qué método de resolución aplicar y qué comportamiento asintótico esperar.
</p>

---

<h2 id="6-5">📚 6.4.1 Ejercicios propuestos</h2>

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
