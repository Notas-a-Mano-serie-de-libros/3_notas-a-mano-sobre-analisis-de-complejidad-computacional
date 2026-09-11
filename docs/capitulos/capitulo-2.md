<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../capitulo-1/">← Capítulo 1</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-3/">Capítulo 3 →</a></nav>

# Capítulo 2 · Fundamentos del análisis de algoritmos

<span class="chapter-kicker">Páginas 59–88</span>

## 2.1 Funciones de complejidad

Una función de complejidad relaciona el tamaño de entrada \(n\) con los recursos consumidos. El tiempo se representa mediante \(T(n)\) y el espacio mediante \(S(n)\). Estas funciones modelan crecimiento: no son segundos o bytes universales, pues la ejecución concreta depende de la máquina, el lenguaje y la implementación.

### 2.1.1 Propiedades básicas

El dominio contiene tamaños de entrada válidos y el costo es no negativo. La monotonía permite estudiar cómo cambia el consumo al aumentar \(n\). En el análisis se identifican la operación básica, la frecuencia con que se ejecuta y la memoria que permanece activa; después se separa el término dominante de constantes y términos menores.

### 2.1.2 Familias de crecimiento

Las familias corresponden a estructuras de ejecución distintas. \(O(1)\) no depende de \(n\); \(O(\log_2(n))\) reduce el problema por factores; \(O(n)\) recorre la entrada; \(O(n \cdot \log_2(n))\) combina niveles logarítmicos con trabajo lineal; y \(O(n^k)\) suele aparecer en recorridos anidados. Los crecimientos \(O(2^n)\) y \(O(n!)\) enumeran combinaciones o permutaciones y dejan de ser prácticos rápidamente.

<div class="chapter-figures">
<figure>
<img src="../../assets/images/complejidad-teorica.png" alt="Comparación de las funciones constante, logarítmica, lineal, log-lineal, cuadrática, cúbica, exponencial y factorial">
<figcaption><strong>Comparación teórica.</strong> La escala vertical logarítmica permite observar en una misma gráfica familias cuyos valores se separan por varios órdenes de magnitud.</figcaption>
</figure>
<figure>
<img src="../../assets/images/complejidad-teorica-zonas.png" alt="Comparación de las funciones de complejidad sobre zonas coloreadas desde excelente hasta pésimo">
<figcaption><strong>Zonas de crecimiento.</strong> El color ofrece una lectura cualitativa del costo para el intervalo representado; no constituye una clasificación universal independiente del tamaño de entrada.</figcaption>
</figure>
</div>

Esta página establece el marco teórico. Cada sección hija realiza el análisis experimental de una familia: identifica un algoritmo representativo, presenta sus implementaciones, formula tiempo y espacio y enlaza la simulación con la que se contrasta la curva.

<nav class="chapter-outline chapter-outline--pages" aria-label="Secciones del capítulo">
<strong>Secciones del capítulo</strong>
<ol class="chapter-section-list">
<li><a href="0-complejidad-sublineal/"><span>2.1.2.0 Complejidad sublineal</span><small>Leer sección →</small></a></li>
<li><a href="1-complejidad-constante/"><span>2.1.2.1 Complejidad constante</span><small>Leer sección →</small></a></li>
<li><a href="2-complejidad-logaritmica/"><span>2.1.2.2 Complejidad logarítmica</span><small>Leer sección →</small></a></li>
<li><a href="3-complejidad-lineal/"><span>2.1.2.3 Complejidad lineal</span><small>Leer sección →</small></a></li>
<li><a href="4-complejidad-log-lineal/"><span>2.1.2.4 Complejidad log-lineal</span><small>Leer sección →</small></a></li>
<li><a href="5-complejidad-cuadratica/"><span>2.1.2.5 Complejidad cuadrática</span><small>Leer sección →</small></a></li>
<li><a href="6-complejidad-cubica/"><span>2.1.2.6 Complejidad cúbica</span><small>Leer sección →</small></a></li>
<li><a href="7-complejidad-polinomial-general/"><span>2.1.2.7 Complejidad polinomial general</span><small>Leer sección →</small></a></li>
<li><a href="8-complejidad-exponencial/"><span>2.1.2.8 Complejidad exponencial</span><small>Leer sección →</small></a></li>
<li><a href="9-complejidad-factorial/"><span>2.1.2.9 Complejidad factorial</span><small>Leer sección →</small></a></li>
<li><a href="ejercicios-propuestos/"><span>2.2 Ejercicios propuestos</span><small>Consultar PDF →</small></a></li>
</ol>
</nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-1/">← Capítulo 1</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-3/">Capítulo 3 →</a></nav>
