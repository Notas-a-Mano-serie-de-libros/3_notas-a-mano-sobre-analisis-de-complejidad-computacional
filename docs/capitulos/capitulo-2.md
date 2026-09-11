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

<section class="chapter-sections" aria-labelledby="chapter-sections-title">
<h2 id="chapter-sections-title">Secciones del capítulo</h2>
<div class="chapter-index chapter-index--sections">
<a class="chapter-entry" href="0-complejidad-sublineal/"><span class="chapter-entry__number">2.1.2.0</span><strong>Complejidad sublineal</strong><span>Distingue los crecimientos que avanzan más lentamente que una función lineal.</span></a>
<a class="chapter-entry" href="1-complejidad-constante/"><span class="chapter-entry__number">2.1.2.1</span><strong>Complejidad constante</strong><span>Analiza operaciones cuyo costo no cambia cuando aumenta el tamaño de entrada.</span></a>
<a class="chapter-entry" href="2-complejidad-logaritmica/"><span class="chapter-entry__number">2.1.2.2</span><strong>Complejidad logarítmica</strong><span>Explica cómo la reducción sucesiva del problema produce crecimiento logarítmico.</span></a>
<a class="chapter-entry" href="3-complejidad-lineal/"><span class="chapter-entry__number">2.1.2.3</span><strong>Complejidad lineal</strong><span>Estudia recorridos cuyo trabajo crece en proporción directa al tamaño de entrada.</span></a>
<a class="chapter-entry" href="4-complejidad-log-lineal/"><span class="chapter-entry__number">2.1.2.4</span><strong>Complejidad log-lineal</strong><span>Relaciona el trabajo lineal por nivel con una cantidad logarítmica de niveles.</span></a>
<a class="chapter-entry" href="5-complejidad-cuadratica/"><span class="chapter-entry__number">2.1.2.5</span><strong>Complejidad cuadrática</strong><span>Muestra el costo de recorrer dos dimensiones o combinar pares de elementos.</span></a>
<a class="chapter-entry" href="6-complejidad-cubica/"><span class="chapter-entry__number">2.1.2.6</span><strong>Complejidad cúbica</strong><span>Examina algoritmos con tres dimensiones de trabajo dependientes de la entrada.</span></a>
<a class="chapter-entry" href="7-complejidad-polinomial-general/"><span class="chapter-entry__number">2.1.2.7</span><strong>Complejidad polinomial general</strong><span>Compara funciones de la forma n elevado a k y el efecto de cambiar su grado.</span></a>
<a class="chapter-entry" href="8-complejidad-exponencial/"><span class="chapter-entry__number">2.1.2.8</span><strong>Complejidad exponencial</strong><span>Observa cómo la ramificación recursiva multiplica rápidamente el trabajo.</span></a>
<a class="chapter-entry" href="9-complejidad-factorial/"><span class="chapter-entry__number">2.1.2.9</span><strong>Complejidad factorial</strong><span>Estudia la enumeración de permutaciones y su crecimiento extremadamente rápido.</span></a>
<a class="chapter-entry" href="ejercicios-propuestos/"><span class="chapter-entry__number">2.2</span><strong>Ejercicios propuestos</strong><span>Reúne problemas para aplicar y contrastar las familias de complejidad estudiadas.</span></a>
</div>
</section>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-1/">← Capítulo 1</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-3/">Capítulo 3 →</a></nav>
