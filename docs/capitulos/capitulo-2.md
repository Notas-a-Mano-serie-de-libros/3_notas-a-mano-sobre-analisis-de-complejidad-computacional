<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../capitulo-1/">← Capítulo 1</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-3/">Capítulo 3 →</a></nav>

# Capítulo 2 · Fundamentos del análisis de algoritmos

<span class="chapter-kicker">Páginas 59–88</span>

## 2.1 Funciones de complejidad

Una función de complejidad relaciona el tamaño de entrada \(n\) con los recursos consumidos. El tiempo se representa mediante \(T(n)\) y el espacio mediante \(S(n)\). Estas funciones modelan crecimiento: no son segundos o bytes universales, pues la ejecución concreta depende de la máquina, el lenguaje y la implementación.

### Modelo de análisis y supuestos

Antes de calcular una complejidad, declare qué representa la entrada y qué recurso se está midiendo. En este portal se adopta, salvo indicación contraria, un modelo de costo uniforme semejante al modelo RAM: cada operación elemental sobre valores que caben en una palabra de máquina tiene costo constante. Este supuesto permite comparar algoritmos sin depender de una marca de procesador, pero no afirma que todas las operaciones tarden lo mismo en una ejecución real.

- **Tamaño de entrada:** \(n\) debe definirse para cada problema. Puede ser la cantidad de elementos, nodos, bits, dígitos o caracteres; no siempre coincide con el valor numérico recibido.
- **Operación elemental:** debe indicarse qué operación se contará. Una comparación, una asignación o un acceso a un arreglo pueden ser candidatos, siempre que el criterio se mantenga durante todo el análisis.
- **Tiempo teórico:** \(T(n)\) cuenta operaciones bajo el modelo escogido. El tiempo de reloj también depende del lenguaje, compilador, memoria caché, sistema operativo y equipo.
- **Espacio total y auxiliar:** el espacio total incluye la entrada; el auxiliar mide únicamente la memoria adicional utilizada por el algoritmo. En recursión debe contarse también la pila de llamadas.
- **Tamaño de palabra:** el costo constante solo es razonable mientras los operandos quepan en una palabra. Operaciones con enteros, cadenas o matrices de tamaño creciente requieren contabilizar su propio costo.
- **Casos de ejecución:** mejor, peor y promedio describen entradas distintas del mismo tamaño. Un caso promedio solo es válido cuando se declara una distribución de probabilidad sobre las entradas.
- **Correctitud antes que eficiencia:** una función de complejidad es útil únicamente después de establecer que el algoritmo termina y produce el resultado esperado.

El análisis asintótico explica la tendencia cuando \(n\) crece. Para estimar segundos o bytes deben añadirse constantes medibles y explicitarse las unidades, como se hace en los ejercicios del capítulo.

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

### Simulación · Crecimiento de las funciones

La diferencia entre estas familias puede parecer pequeña cuando el valor de \(n\) es reducido. Elige un valor de hasta \(1000\) y ejecuta la simulación para observar, en escala lineal real, cómo las funciones de crecimiento más rápido dejan atrás a las demás. La gráfica y la carrera de barras se actualizan simultáneamente para mostrar el mismo proceso desde dos perspectivas.

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Comparación del crecimiento de funciones | `jupyter lab simulaciones/capitulo2/notebooks/0_comparacion_crecimiento.ipynb` |
| Abrir Cálculo canónico de complejidad teórica | `jupyter lab simulaciones/capitulo2/notebooks/10_calculo_complejidad_canonica.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->

<!-- jupyterlite-demo:start -->
#### Simulación en el navegador

Este demo se ejecuta con **JupyterLite y Pyodide** dentro del navegador. La primera carga descarga el entorno de Python; las siguientes aperturas reutilizan los recursos almacenados por el navegador.

1. Espera a que el indicador del kernel muestre **Python (Pyodide)**.
2. La simulación se ejecuta automáticamente cuando el kernel esté listo.
3. Configura \(n\), la velocidad y las funciones visibles; luego utiliza **Reproducir** o **Reiniciar**. El valor actual avanza desde cero y el eje horizontal conserva el límite elegido.

<div class="jupyterlite-demo">
  <div class="jupyterlite-demo__toolbar">
    <span>Simulación interactiva</span>
  </div>
  <div class="jupyterlite-demo__actions">
    <a class="md-button colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo2/notebooks/0_comparacion_crecimiento.ipynb" target="_blank" rel="noopener noreferrer">Abrir en Colab</a>
    <a class="md-button jupyterlite-button" href="../../jupyterlite/graficas/notebooks/index.html?path=simulaciones%2Fcapitulo2%2Fnotebooks%2F0_comparacion_crecimiento.ipynb&revision=967221a2d71e" target="_blank" rel="noopener noreferrer">Abrir en pantalla completa</a>
  </div>
  <iframe
    class="jupyterlite-demo__frame"
    src="../../jupyterlite/graficas/notebooks/index.html?path=simulaciones%2Fcapitulo2%2Fnotebooks%2F0_comparacion_crecimiento.ipynb&revision=967221a2d71e"
    title="Comparación interactiva del crecimiento de funciones en JupyterLite"
    loading="lazy"
    scrolling="no"
    allow="clipboard-read; clipboard-write"
  ></iframe>
</div>
<!-- jupyterlite-demo:end -->

### Simulación · Cálculo canónico de complejidad teórica

El orden asintótico describe cómo crece el costo, pero no lo expresa todavía en una unidad concreta. Para obtener una estimación teórica comparable, el libro adopta una referencia canónica para el tiempo y otra para el espacio. La siguiente simulación aplica estas referencias a cada orden de magnitud de \(n\) y conserva \(c=1\) como valor inicial de la función constante.

\[
\begin{aligned}
t &\approx T_0 \cdot T(n), & T_0 &= 10^{-6}\,[\text{s}] = 1\,[\mu\text{s}], \\
s &\approx S_0 \cdot S(n), & S_0 &= 1\,[\text{byte}].
\end{aligned}
\]

<!-- jupyterlite-demo:start -->
#### Simulación en el navegador

Este demo se ejecuta con **JupyterLite y Pyodide** dentro del navegador. La primera carga descarga el entorno de Python; las siguientes aperturas reutilizan los recursos almacenados por el navegador.

1. Espera a que el indicador del kernel muestre **Python (Pyodide)**.
2. La simulación se ejecuta automáticamente cuando el kernel esté listo.
3. Elige complejidad **temporal** o **espacial**, la escala **lineal** o **logarítmica**, ajusta \(c\), el orden máximo y la velocidad, y pulsa **Reproducir**.
4. Observa simultáneamente las curvas y la carrera de crecimiento: la tabla incorpora una nueva fila solamente cuando \(n\) alcanza \(10^0,10^1,\ldots\), hasta el orden seleccionado.
5. Selecciona cualquier fila de la tabla para volver a mostrar la gráfica exactamente en ese orden de magnitud.

<div class="jupyterlite-demo">
  <div class="jupyterlite-demo__toolbar">
    <span>Simulación interactiva</span>
  </div>
  <div class="jupyterlite-demo__actions">
    <a class="md-button colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo2/notebooks/10_calculo_complejidad_canonica.ipynb" target="_blank" rel="noopener noreferrer">Abrir en Colab</a>
    <a class="md-button jupyterlite-button" href="../../jupyterlite/graficas/notebooks/index.html?path=simulaciones%2Fcapitulo2%2Fnotebooks%2F10_calculo_complejidad_canonica.ipynb&revision=967221a2d71e" target="_blank" rel="noopener noreferrer">Abrir en pantalla completa</a>
  </div>
  <iframe
    class="jupyterlite-demo__frame"
    src="../../jupyterlite/graficas/notebooks/index.html?path=simulaciones%2Fcapitulo2%2Fnotebooks%2F10_calculo_complejidad_canonica.ipynb&revision=967221a2d71e"
    title="Cálculo canónico de complejidad teórica en JupyterLite"
    loading="lazy"
    scrolling="no"
    allow="clipboard-read; clipboard-write"
  ></iframe>
</div>
<!-- jupyterlite-demo:end -->

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
<li><a href="practica-autocorregible/"><strong>Ejercicios complementarios</strong></a></li>
</ul>
</section>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-1/">← Capítulo 1</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-3/">Capítulo 3 →</a></nav>
