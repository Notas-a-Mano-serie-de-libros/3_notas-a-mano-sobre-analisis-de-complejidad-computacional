<h1 style="text-align:center;">
  <strong>Capítulo 3: Notación asintótica</strong>
</h1>

<p align="justify">
La <b>notación asintótica</b> es un método matemático que analiza el comportamiento de una función cuando sus variables se aproximan a valores límite, típicamente el infinito (Bachmann, 1894), con el fin de caracterizar su orden de magnitud e identificar el término dominante que rige su tendencia de crecimiento. En el contexto computacional, este método actúa como marco de referencia que facilita la comparación y clasificación de problemas según su complejidad teórica (Knuth, 1976).
</p>

---

<h2>🧭 Contenido del capítulo</h2>

<ul>
  <li><a href="#3-1">3.1 Contexto histórico</a>
    <ul>
      <li><a href="#3-1-1">3.1.1 Análisis del comportamiento límite</a></li>
      <li><a href="#3-1-2">3.1.2 El trabajo de Bachmann y Landau</a></li>
      <li><a href="#3-1-3">3.1.3 El salto a la computación</a></li>
      <li><a href="#3-1-4">3.1.4 Consolidación y uso moderno</a></li>
    </ul>
  </li>
  <li><a href="#3-2">3.2 Comportamiento asintótico general</a>
    <ul>
      <li><a href="#3-2-1">3.2.1 Función polinómica</a></li>
      <li><a href="#3-2-2">3.2.2 Función exponencial</a></li>
      <li><a href="#3-2-3">3.2.3 Jerarquía funcional asintótica</a></li>
    </ul>
  </li>
  <li><a href="#3-3">3.3 Familias de funciones</a>
    <ul>
      <li><a href="#3-3-1">3.3.1 Definición</a></li>
      <li><a href="#3-3-2">3.3.2 Familias de funciones en el límite asintótico</a></li>
      <li><a href="#3-3-3">3.3.3 Propiedades asintóticas de F</a></li>
      <li><a href="#3-3-4">3.3.4 Ejemplos</a></li>
    </ul>
  </li>
  <li><a href="#3-4">3.4 Notación asintótica simplificada</a></li>
  <li><a href="#3-5">3.5 Tipos de notación asintótica</a>
    <ul>
      <li><a href="#3-5-1">3.5.1 Notación O (Big-O y little-o)</a></li>
      <li><a href="#3-5-2">3.5.2 Notación Ω (Big-Ω y little-ω)</a></li>
      <li><a href="#3-5-3">3.5.3 Notación Θ (Theta)</a></li>
      <li><a href="#3-5-4">3.5.4 Propiedades de las notaciones</a></li>
    </ul>
  </li>
  <li><a href="#3-6">3.6 Ejercicios propuestos</a></li>
</ul>

---

<h2 id="3-1">📜 3.1 Contexto histórico</h2>

<p align="justify">
El análisis de algoritmos modernos recurre con frecuencia a la notación asintótica para describir el comportamiento esperado de las funciones de complejidad. Este lenguaje formal tiene sus raíces en varios estudios realizados durante los siglos XVIII y XIX.
</p>

<h3 id="3-1-1">3.1.1 Análisis del comportamiento límite</h3>
<p align="justify">
Los primeros antecedentes se encuentran en el trabajo de los matemáticos <b>Leonhard Euler</b> y <b>Augustin-Louis Cauchy</b>, quienes estudiaron el comportamiento de funciones y series en torno a valores extremos, sentando las bases del análisis infinitesimal y del estudio de los límites (Cauchy, 1821; Kleiner, 2007).
</p>

<h3 id="3-1-2">3.1.2 El trabajo de Bachmann y Landau</h3>
<p align="justify">
El primer uso formal documentado de una notación destinada a acotar el crecimiento de funciones se remonta al año <b>1894</b>, con el trabajo del matemático alemán <b>Paul Bachmann</b>, quien introdujo la notación Big-O en el contexto de la teoría de números. Posteriormente, <b>Edmund Landau</b> retomó y extendió este formalismo en su obra <i>"Handbuch der Lehre von der Verteilung der Primzahlen"</i>, donde introdujo la notación little-o y consolidó el uso de ambas notaciones (Bachmann, 1894; Landau, 1909).
</p>

<h3 id="3-1-3">3.1.3 El salto a la computación</h3>
<p align="justify">
La incorporación de la notación asintótica al análisis de algoritmos tuvo lugar en el siglo XX, particularmente durante las décadas de 1960 y 1970. Durante esta época, <b>Donald E. Knuth</b> organizó y extendió el uso de estas ideas en su artículo <i>"Big Omicron and Big Omega and Big Theta"</i> (Knuth, 1976), formalizando las notaciones <b>O, Ω</b> y <b>Θ</b> como herramientas de análisis y clasificación de problemas computacionales.
</p>

<h3 id="3-1-4">3.1.4 Consolidación y uso moderno</h3>
<p align="justify">
Desde la década de 1980, la notación asintótica se consolidó como una convención ampliamente adoptada en el análisis de algoritmos. Su aplicación permite abstraer detalles de implementación y enfocar el estudio en el crecimiento funcional, facilitando el análisis teórico de las soluciones computacionales en diferentes contextos (Cormen et al., 2009).
</p>

---

<h2 id="3-2">⚙️ 3.2 Comportamiento asintótico general</h2>

<p align="justify">
Una función de complejidad que cumpla las propiedades básicas (restricción del dominio, crecimiento monótono, representación asintótica) puede expresarse como la superposición de m funciones cuyo crecimiento está estrictamente ordenado de menor a mayor:
</p>

<p style="text-align:center; font-family:monospace;">
f(n) = f₁(n) + f₂(n) + f₃(n) + ··· + f<sub>m</sub>(n) &nbsp;&nbsp;&nbsp; donde &nbsp;&nbsp;&nbsp; f₁(n) ≺ f₂(n) ≺ ··· ≺ f<sub>m</sub>(n)
</p>

<p align="justify">
Analizando el comportamiento asintótico mediante el límite de la razón f(n)/f<sub>m</sub>(n) cuando n → ∞, todos los términos de menor orden se vuelven despreciables frente al término dominante:
</p>

<p style="text-align:center; font-family:monospace;">lim<sub>n→∞</sub> (f(n)/f<sub>m</sub>(n)) = 1 &nbsp;&nbsp;⟹&nbsp;&nbsp; f(n) ~ f<sub>m</sub>(n); n → ∞</p>

<p align="justify">
El símbolo "~" expresa que ambas funciones son <b>asintóticamente equivalentes</b>: su comportamiento de crecimiento se vuelve indistinguible cuando n → ∞.
</p>

<h3 id="3-2-1">3.2.1 Caso particular: función polinómica</h3>

<p align="justify">
Considerando f(n) = aₖnᵏ + a<sub>k-1</sub>n<sup>k-1</sup> + ··· + a₁n + a₀, donde {aₖ, ..., a₀} ⊂ ℝ son coeficientes constantes y k ∈ ℤ₀⁺. Cuando n tiende a infinito, el término de mayor orden (aₖnᵏ) domina el comportamiento. Aplicando el análisis de límites:
</p>

<p style="text-align:center; font-family:monospace;">
lim<sub>n→∞</sub> (f(n)/aₖnᵏ) = 1 &nbsp;&nbsp;⟹&nbsp;&nbsp; f(n) ~ aₖnᵏ; n → ∞ &nbsp;&nbsp;⟹&nbsp;&nbsp; f(n) ~ nᵏ; n → ∞
</p>

<h3 id="3-2-2">3.2.2 Caso particular: función exponencial</h3>

<p align="justify">
Considerando g(n) = aⁿ + cₖnᵏ + c<sub>k-1</sub>n<sup>k-1</sup> + ··· + c₁n + c₀, donde {a, cₖ, ..., c₀} ⊂ ℝ y k ∈ ℤ₀⁺. El término de mayor orden (aⁿ) domina. Aplicando el mismo procedimiento:
</p>

<p style="text-align:center; font-family:monospace;">
lim<sub>n→∞</sub> (g(n)/aⁿ) = 1 &nbsp;&nbsp;⟹&nbsp;&nbsp; g(n) ~ aⁿ; n → ∞
</p>

<h3 id="3-2-3">3.2.3 Jerarquía funcional asintótica</h3>

<p align="justify">
Aplicando los resultados anteriores a las funciones comunes del Capítulo 2, se establece la siguiente <b>jerarquía funcional asintótica</b>, útil para clasificar las funciones de complejidad de acuerdo con su comportamiento teórico:
</p>

<p style="text-align:center; font-size:1.05em; font-family:monospace;">
1 ≺ log<sub>ℓ</sub>(n) ≺ n ≺ n·log<sub>ℓ</sub>(n) ≺ n² ≺ n³ ≺ ··· ≺ nᵏ ≺ 2ⁿ ≺ n!
</p>

<p align="justify">
Las funciones con tasas de crecimiento más lentas, como C(1), C(log(n)) y C(n), son estables incluso cuando n es muy grande. Las funciones de tipo log-lineal, polinómico general, exponencial y factorial crecen de manera explosiva, superando rápidamente cualquier umbral razonable de operaciones.
</p>

<p style="margin-top:0.8em;">
  🔗 <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/notacion_asintotica_representacion_generica.ipynb"><b>Notebook – Representación genérica de la notación asintótica (Figuras 3.2, 3.7, 3.12)</b></a>
</p>

---

<h2 id="3-3">🗂️ 3.3 Familias de funciones</h2>

<h3 id="3-3-1">3.3.1 Definición</h3>

<p align="justify">
Una <b>familia de funciones</b> es un conjunto de funciones que comparten una misma estructura general, cuya forma concreta queda determinada por el valor que se asigna a los parámetros que tiene asociados. Sea Λ un conjunto no vacío de parámetros. Una <b>familia de funciones</b> es una colección de la forma:
</p>

<p style="text-align:center; font-family:monospace;">𝓕 = {f<sub>λ</sub> : λ ∈ Λ}</p>

<p align="justify">
Donde <b>Λ</b> es el conjunto de parámetros que indexa la familia, y <b>f<sub>λ</sub> : A → B</b> es la función asociada al parámetro λ. Distintos valores de λ producen funciones distintas, pero todas comparten la misma estructura general.
</p>

<p align="justify">
<b>Ejemplo:</b> Las funciones f(x) = mx + b forman la familia de funciones lineales: 𝓕 = {f<sub>(m,b)</sub> : ℝ → ℝ | (m, b) ∈ ℝ²}. Esta familia abstrae todas las funciones lineales posibles, permitiendo razonar sobre todas ellas simultáneamente.
</p>

<h3 id="3-3-2">3.3.2 Familias de funciones en el límite asintótico</h3>

<p align="justify">
En el análisis asintótico, el interés recae sobre el comportamiento de una función cuando el argumento crece sin cota. Dada una función de complejidad C : ℕ → ℝ⁺, n ↦ C(n), la <b>familia de funciones con comportamiento asintótico equivalente a C</b> se define como:
</p>

<p style="text-align:center; font-family:monospace;">𝓕(C(n)) = {f<sub>λ</sub> : ℕ → ℝ⁺ | λ ∈ Λ, f<sub>λ</sub>(n) ~ C(n)}</p>

<p align="justify">
<b>Ejemplo:</b> Las funciones 3n + 5, 7n − 2 y n + log(n) pertenecen todas a 𝓕(n), ya que en el límite asintótico todas describen un comportamiento lineal: n ~ 3n+5 ~ 7n−2 ~ n+log(n).
</p>

<h3 id="3-3-3">3.3.3 Propiedades asintóticas de 𝓕</h3>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Propiedad</th>
      <th style="padding:8px; border:1px solid #ccc;">Formal</th>
      <th style="padding:8px; border:1px solid #ccc;">Significado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Invarianza frente a constantes</b></td>
      <td style="padding:8px; border:1px solid #ccc; font-family:monospace;">c ∈ ℝ⁺ ⟹ 𝓕(c · g(n)) = 𝓕(g(n))</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Multiplicar una función por una constante positiva no cambia su comportamiento asintótico.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Aditividad</b></td>
      <td style="padding:8px; border:1px solid #ccc; font-family:monospace;">𝓕(f(n)) + 𝓕(g(n)) ⊆ 𝓕(f(n) + g(n))</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">La familia de la suma de dos funciones contiene a la suma de sus familias.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Multiplicatividad</b></td>
      <td style="padding:8px; border:1px solid #ccc; font-family:monospace;">𝓕(f(n)) · 𝓕(g(n)) ⊆ 𝓕(f(n) · g(n))</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">La familia del producto entre dos funciones contiene al producto de sus familias.</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Dominancia</b></td>
      <td style="padding:8px; border:1px solid #ccc; font-family:monospace;">lim g(n)/f(n) = 0 ⟹ 𝓕(f(n)+g(n)) = 𝓕(f(n))</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">Si f(n) crece más rápido que g(n), el comportamiento asintótico conjunto queda determinado por f(n).</td>
    </tr>
  </tbody>
</table>

<h3 id="3-3-4">3.3.4 Ejemplos de clasificación en familias</h3>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Función f(n)</th>
      <th style="padding:8px; border:1px solid #ccc; text-align:center;">Familia asintótica</th>
    </tr>
  </thead>
  <tbody>
    <tr><td style="padding:7px; border:1px solid #ccc; font-family:monospace;">f(n) = k (constante)</td><td style="padding:7px; border:1px solid #ccc; text-align:center; font-family:monospace;">𝓕(1)</td></tr>
    <tr><td style="padding:7px; border:1px solid #ccc; font-family:monospace;">f(n) = 3n + 5</td><td style="padding:7px; border:1px solid #ccc; text-align:center; font-family:monospace;">𝓕(n)</td></tr>
    <tr><td style="padding:7px; border:1px solid #ccc; font-family:monospace;">f(n) = n · log(n) + 5n</td><td style="padding:7px; border:1px solid #ccc; text-align:center; font-family:monospace;">𝓕(n · log(n))</td></tr>
    <tr><td style="padding:7px; border:1px solid #ccc; font-family:monospace;">f(n) = k · n! + 2ⁿ</td><td style="padding:7px; border:1px solid #ccc; text-align:center; font-family:monospace;">𝓕(n!)</td></tr>
    <tr><td style="padding:7px; border:1px solid #ccc; font-family:monospace;">f(n) = 3n² + 7n + 1</td><td style="padding:7px; border:1px solid #ccc; text-align:center; font-family:monospace;">𝓕(n²)</td></tr>
    <tr><td style="padding:7px; border:1px solid #ccc; font-family:monospace;">f(n) = 2ⁿ + n³</td><td style="padding:7px; border:1px solid #ccc; text-align:center; font-family:monospace;">𝓕(2ⁿ)</td></tr>
  </tbody>
</table>

---

<h2 id="3-4">✏️ 3.4 Notación asintótica simplificada</h2>

<p align="justify">
La mayoría de los textos modernos adoptan la convención establecida en la obra <i>"Introduction to Algorithms"</i> (Cormen et al., 2022), donde la pertenencia a una familia asintótica se expresa utilizando el signo de igualdad "=" o desigualdad en lugar del símbolo de pertenencia "∈". Se utiliza el símbolo ⊙ ∈ {=, ≤, ≥, &lt;, &gt;} para denotar el conjunto de operadores relacionales más comunes en el análisis de complejidad.
</p>

<p align="justify">
<b>Caso 1:</b> Cuando el término 𝓕(h(n)) aparece solo en el lado derecho, el operador ⊙ debe interpretarse como pertenencia: f(n) ⊙ 𝓕(g(n)) ≡ f(n) ∈ 𝓕(g(n)).
</p>

<p align="justify">
<b>Caso 2:</b> Cuando el lado derecho contiene un término cuyo detalle es irrelevante para el análisis, es posible reemplazarlo por la familia asintótica a la que pertenece; por ejemplo, si r(n) ∈ 𝓕(h(n)) es el término que se desea omitir: f(n) ⊙ g(n) + r(n) se expresa como f(n) ⊙ g(n) + 𝓕(h(n)).
</p>

<p align="justify">
<b>Ejemplo:</b> Para f(n) = 2n² + 3n + 1, aplicando Caso 2 iterativamente: f(n) = 2n² + 𝓕(n) = 𝓕(n²) + 𝓕(n) = 𝓕(n²) (por dominancia, ya que n ≺ n²). Lo cual corresponde al Caso 1: f(n) ∈ 𝓕(n²).
</p>

---

<h2 id="3-5">🔢 3.5 Tipos de notación asintótica</h2>

<p align="justify">
Al extender el formalismo de familias de funciones al análisis de complejidad, surgen familias concretas que caracterizan el comportamiento asintótico de C(n) para casos de ejecución específicos:
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc; text-align:center;">Notación</th>
      <th style="padding:8px; border:1px solid #ccc;">Tipo de cota</th>
      <th style="padding:8px; border:1px solid #ccc;">Interpretación</th>
      <th style="padding:8px; border:1px solid #ccc; text-align:center;">Notebook</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold; font-size:1.1em;">O</td>
      <td style="padding:8px; border:1px solid #ccc;">Cota superior</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">El algoritmo <b>no tardará más</b> que esto. Caracteriza la complejidad en el <b>peor caso</b>.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/1_notacion_big_o.ipynb">📗 Big-O</a></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold; font-size:1.1em;">o</td>
      <td style="padding:8px; border:1px solid #ccc;">Cota superior estricta</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">C(n) crece <b>estrictamente más lento</b> que g(n), de forma incondicional para toda constante c.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/2_notacion_little_o.ipynb">📗 little-o</a></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold; font-size:1.1em;">Ω</td>
      <td style="padding:8px; border:1px solid #ccc;">Cota inferior</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">El algoritmo <b>no podrá ser más rápido</b> que esto. Caracteriza la complejidad en el <b>mejor caso</b>.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/3_notacion_big_omega.ipynb">📘 Big-Ω</a></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold; font-size:1.1em;">ω</td>
      <td style="padding:8px; border:1px solid #ccc;">Cota inferior estricta</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">C(n) crece <b>estrictamente más rápido</b> que g(n), de forma incondicional para toda constante c.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/4_notacion_little_omega.ipynb">📘 little-ω</a></td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold; font-size:1.1em;">Θ</td>
      <td style="padding:8px; border:1px solid #ccc;">Cota ajustada</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">El algoritmo crece <b>exactamente a este ritmo</b>. Es la caracterización más precisa del costo computacional.</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/5_notacion_theta.ipynb">📙 Theta</a></td>
    </tr>
  </tbody>
</table>

<h3 id="3-5-1">⚪ 3.5.1 Notación O (Big-O y little-o)</h3>

<p align="justify">
La <b>notación O</b> define la familia de funciones acotadas superiormente por un múltiplo constante de una función de referencia. Formalmente, una función C(n) arbitraria se expresa en notación Big-O y little-o de la siguiente manera:
</p>

<p style="text-align:center; font-family:monospace;">
C(n) ∈ O(g(n)) &nbsp;⟺&nbsp; ∃c ∈ ℝ⁺ : C(n) ≤ c·g(n) &nbsp;∀n ≥ n₀, n₀ ∈ ℕ<br/>
C(n) ∈ o(g(n)) &nbsp;⟺&nbsp; ∀c ∈ ℝ⁺ : C(n) &lt; c·g(n) &nbsp;∀n ≥ n₀, n₀ ∈ ℕ
</p>

<p align="justify">
Equivalentemente, usando el análisis de límites:
</p>

<p style="text-align:center; font-family:monospace;">
C(n) ∈ O(g(n)) &nbsp;⟺&nbsp; lim sup<sub>n→∞</sub> (C(n)/g(n)) = k, &nbsp; k ∈ ℝ₀⁺ &nbsp; (límite finito)<br/>
C(n) ∈ o(g(n)) &nbsp;⟺&nbsp; lim<sub>n→∞</sub> (C(n)/g(n)) = 0
</p>

<p align="justify">
<b>Ejemplo del libro (Ejemplo 1):</b> Para C(n) = n³ + 2n² + n + 5 y g(n) = n³:
</p>

<p style="text-align:center; font-family:monospace;">lim sup (C(n)/n³) = lim sup (1 + 2/n + 1/n² + 5/n³) = 1 &nbsp;⟹&nbsp; C(n) ∈ O(n³), para algún c ≥ 1</p>

<p align="justify">
Con c = 2 se obtiene n₀ = ⌈2,93⌉ = 3. <b>Ejemplo 2:</b> Para g(n) = n², el límite diverge a ∞, por lo tanto C(n) ∉ O(n²). Para little-o, g(n) = n⁴ da lim = 0, por lo tanto C(n) ∈ o(n⁴).
</p>

<p align="justify">
<b>Corolario:</b> o(g(n)) ⊆ O(g(n)). Todo función en little-o también está en Big-O, pero no viceversa.
</p>

<h3 id="3-5-2">🟢 3.5.2 Notación Ω (Big-Ω y little-ω)</h3>

<p align="justify">
La <b>notación Ω</b> define la familia de funciones acotadas inferiormente por un múltiplo constante de una función de referencia. Formalmente:
</p>

<p style="text-align:center; font-family:monospace;">
C(n) ∈ Ω(g(n)) &nbsp;⟺&nbsp; ∃c ∈ ℝ⁺ : C(n) ≥ c·g(n) &nbsp;∀n ≥ n₀, n₀ ∈ ℕ<br/>
C(n) ∈ ω(g(n)) &nbsp;⟺&nbsp; ∀c ∈ ℝ⁺ : C(n) &gt; c·g(n) &nbsp;∀n ≥ n₀, n₀ ∈ ℕ
</p>

<p align="justify">
Equivalentemente mediante límites:
</p>

<p style="text-align:center; font-family:monospace;">
C(n) ∈ Ω(g(n)) &nbsp;⟺&nbsp; lim inf<sub>n→∞</sub> (C(n)/g(n)) = k, &nbsp; k ∈ ℝ⁺ &nbsp; (k > 0 finito)<br/>
C(n) ∈ ω(g(n)) &nbsp;⟺&nbsp; lim<sub>n→∞</sub> (C(n)/g(n)) = ∞
</p>

<p align="justify">
<b>Ejemplo del libro (Ejemplo 1):</b> Para C(n) = n³ + 2n² + n + 5 y g(n) = n³:
</p>

<p style="text-align:center; font-family:monospace;">lim inf (C(n)/n³) = 1 &nbsp;⟹&nbsp; C(n) ∈ Ω(n³), para algún c ≤ 1</p>

<p align="justify">
Con c = 0,5 se obtiene n₀ = 0. <b>Ejemplo 2:</b> Para g(n) = n⁴, el límite es 0 (no cumple k > 0), por lo tanto C(n) ∉ Ω(n⁴). Para little-ω, g(n) = n² da lim = ∞, por lo tanto C(n) ∈ ω(n²).
</p>

<h3 id="3-5-3">🟣 3.5.3 Notación Θ (Theta)</h3>

<p align="justify">
La <b>notación Θ</b> define la familia de funciones que poseen tanto cota superior como inferior en g(n), es decir, la función crece al mismo orden que g(n) dentro de factores constantes:
</p>

<p style="text-align:center; font-family:monospace;">
C(n) ∈ Θ(g(n)) &nbsp;⟺&nbsp; C(n) ∈ O(g(n)) &nbsp;∧&nbsp; C(n) ∈ Ω(g(n))<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;⟺&nbsp; ∃c₁,c₂ ∈ ℝ⁺ : c₁·g(n) ≤ C(n) ≤ c₂·g(n) &nbsp;∀n ≥ n₀
</p>

<p align="justify">
Equivalentemente: C(n) ∈ Θ(g(n)) ⟺ lim<sub>n→∞</sub> (C(n)/g(n)) = k, donde 0 &lt; k &lt; ∞.
</p>

<p align="justify">
<b>Ejemplo:</b> Para C(n) = n³ + 2n² + n + 5, el límite con g(n) = n³ es 1 (finito y positivo), por lo tanto C(n) ∈ Θ(n³). Esto significa que el algoritmo crece exactamente al ritmo de n³, confirmando que esta es la caracterización más precisa de su comportamiento.
</p>

<h3 id="3-5-4">📋 3.5.4 Resumen de propiedades</h3>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc; text-align:center;">Notación</th>
      <th style="padding:8px; border:1px solid #ccc; text-align:center;">Condición de límite</th>
      <th style="padding:8px; border:1px solid #ccc; text-align:center;">Relación con O</th>
      <th style="padding:8px; border:1px solid #ccc;">Caso de análisis</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">O(g(n))</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-family:monospace;">lim sup C/g = k ∈ [0, ∞)</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;">—</td>
      <td style="padding:8px; border:1px solid #ccc;">Peor caso (cota superior)</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">o(g(n))</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-family:monospace;">lim C/g = 0</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;">o ⊆ O</td>
      <td style="padding:8px; border:1px solid #ccc;">Cota superior estricta</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">Ω(g(n))</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-family:monospace;">lim inf C/g = k ∈ (0, ∞)</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;">—</td>
      <td style="padding:8px; border:1px solid #ccc;">Mejor caso (cota inferior)</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">ω(g(n))</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-family:monospace;">lim C/g = ∞</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;">ω ⊆ Ω</td>
      <td style="padding:8px; border:1px solid #ccc;">Cota inferior estricta</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-weight:bold;">Θ(g(n))</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center; font-family:monospace;">lim C/g = k ∈ (0, ∞)</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;">Θ = O ∩ Ω</td>
      <td style="padding:8px; border:1px solid #ccc;">Cota ajustada (exacta)</td>
    </tr>
  </tbody>
</table>

---

<h2 id="3-6">🧠 3.6 Ejercicios propuestos</h2>

<p align="justify">
Los ejercicios propuestos para este capítulo permiten afianzar la comprensión de la notación asintótica mediante comparación de funciones, demostraciones formales y análisis de límites. El objetivo es que el lector aprenda a identificar la cota superior, inferior y ajustada de manera analítica, aplicando la jerarquía funcional asintótica y las definiciones formales de cada notación.
</p>

<p align="center">
  <a href="https://drive.google.com/file/d/175Q_ze2udbV-mJwqsI34MmwCeHKvs3qP/view" target="_blank">
    <b>📄 Ver soluciones – Ejercicios propuestos del Capítulo 3</b>
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
