<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../capitulo-1/">← Capítulo 1</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-3/">Capítulo 3 →</a></nav>

# Capítulo 2 · Fundamentos del análisis de algoritmos

<span class="chapter-kicker">Páginas 59–88</span>

## 2.1 Funciones de complejidad

Una función de complejidad relaciona el tamaño de entrada \(n\) con los recursos consumidos. El tiempo se representa mediante \(T(n)\) y el espacio mediante \(S(n)\). Estas funciones modelan crecimiento: no son segundos o bytes universales, pues la ejecución concreta depende de la máquina, el lenguaje y la implementación.

### 2.1.1 Propiedades básicas

- **Restricción del dominio:** El tamaño de entrada \(n\) es un número natural no negativo; puede representar elementos, bits o nodos.
- **No negatividad:** El costo modelado satisface \(C(n)\geq 0\); el tiempo y el consumo de recursos no pueden ser negativos.
- **Crecimiento monótono:** En el modelo presentado por el libro, el costo no disminuye al aumentar el tamaño de entrada: \(n_1\leq n_2\Rightarrow C(n_1)\leq C(n_2)\).
- **Representación asintótica:** La función describe el comportamiento del algoritmo cuando \(n\) tiende a infinito, mediante la notación asintótica.

### 2.1.2 Familias de crecimiento

La notación \(C(n)\) representa de forma general una función de costo temporal o espacial. La tabla resume las funciones comunes presentadas en el libro.

| \(C(n)\) | Tipo de función | Descripción |
| --- | --- | --- |
| \(c\) | Constante | No depende del tamaño de entrada, con \(c\in\mathbb{R}_0^+\). |
| \(\log_{\ell}(n)\) | Logarítmica | Crece logarítmicamente con el tamaño de entrada, con \(\ell\in\mathbb{R}^+\) y \(\ell\neq 1\). |
| \(n\) | Lineal | Crece en proporción directa al tamaño de entrada. |
| \(n\cdot\log_{\ell}(n)\) | Log-lineal | Combina un factor lineal con otro logarítmico, con \(\ell\in\mathbb{R}^+\) y \(\ell\neq 1\). |
| \(n^2\) | Cuadrática | Crece con el cuadrado del tamaño de entrada. |
| \(n^3\) | Cúbica | Crece con el cubo del tamaño de entrada. |
| \(n^k\) | Polinomial | Crece con una potencia de la entrada, con \(k\in\mathbb{R}_0^+\); incluye los casos constante, lineal, cuadrático y cúbico. |
| \(2^n\) | Exponencial | Se duplica por cada incremento unitario del tamaño de entrada. |
| \(a^n\) | Exponencial general | Aumenta por un factor constante \(a\) por cada incremento unitario, con \(a>1\). |
| \(n!\) | Factorial | Crece con el factorial del tamaño de entrada. |

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

Cada sección presenta el código del libro y enlaza su simulación. Las instrucciones de uso y la interpretación de los experimentos se encuentran en el notebook asociado.

<section class="chapter-sections" aria-labelledby="chapter-sections-title">
<h2 id="chapter-sections-title">Secciones del capítulo</h2>
<ul class="chapter-section-list">
<li><a href="0-complejidad-sublineal/"><strong>Complejidad sublineal</strong></a></li>
<li><a href="1-complejidad-constante/"><strong>Complejidad constante</strong></a></li>
<li><a href="2-complejidad-logaritmica/"><strong>Complejidad logarítmica</strong></a></li>
<li><a href="3-complejidad-lineal/"><strong>Complejidad lineal</strong></a></li>
<li><a href="4-complejidad-log-lineal/"><strong>Complejidad log-lineal</strong></a></li>
<li><a href="5-complejidad-cuadratica/"><strong>Complejidad cuadrática</strong></a></li>
<li><a href="6-complejidad-cubica/"><strong>Complejidad cúbica</strong></a></li>
<li><a href="7-complejidad-polinomial-general/"><strong>Complejidad polinomial general</strong></a></li>
<li><a href="8-complejidad-exponencial/"><strong>Complejidad exponencial</strong></a></li>
<li><a href="9-complejidad-factorial/"><strong>Complejidad factorial</strong></a></li>
<li><a href="ejercicios-propuestos/"><strong>Ejercicios propuestos</strong></a></li>
</ul>
</section>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-1/">← Capítulo 1</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-3/">Capítulo 3 →</a></nav>
