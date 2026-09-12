<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.9 Complejidad factorial

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/9_complejidad_factorial.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: contar permutaciones

El ejemplo cuenta las permutaciones explorando cada posible elección del primer elemento y repitiendo el proceso con los elementos restantes.

La cantidad de ramas generadas sigue la forma factorial, porque cada nivel reduce la lista en un elemento pero multiplica las posibilidades acumuladas.


---

### Código del libro asociado

<!-- book-code:start -->

El libro no incluye un listado de implementación para este tema.

#### Laboratorio y medición

El listado Java procede de la página del libro indicada arriba. El laboratorio ejecuta una adaptación en Python; compara el patrón de crecimiento, no los tiempos de Java con los de Python.

El tiempo se promedia por ejecución; la preparación de las entradas se realiza antes de cronometrar. Las gráficas teóricas y las mediciones experimentales se identifican por separado.

El laboratorio cuenta permutaciones en Python. No existe un listado equivalente en el libro y no se presenta como transcripción de este.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/runtime/complexity_animations.py).

<!-- book-code:end -->

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad factorial aparece cuando el algoritmo explora todas las permutaciones posibles de una colección. Para \(n\) elementos existen \(n!\) ordenamientos diferentes.

Este crecimiento es incluso más agresivo que muchas formas exponenciales. Por eso estos algoritmos solo son viables para entradas muy pequeñas.

Para una entrada de tamaño \(n\), una función de costo factorial puede expresarse como:

\[
T(n) = cn!
\]

donde \(n!\) representa el producto \(n \times (n-1) \times (n-2) \times \cdots \times 1\).

Cada nuevo elemento multiplica la cantidad de permutaciones posibles, por lo que el costo se dispara rápidamente.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_factorial.png" alt="Secuencia visual de 2.1.2.9 complejidad factorial · paso representativo 1 de 5"><figcaption>Secuencia visual de 2.1.2.9 complejidad factorial · paso representativo 1 de 5.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-2/analisis_eficiencia/complejidad_temporal/complejidad_factorial_1.png" alt="Secuencia visual de 2.1.2.9 complejidad factorial · paso representativo 2 de 5"><figcaption>Secuencia visual de 2.1.2.9 complejidad factorial · paso representativo 2 de 5.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-2/analisis_eficiencia/complejidad_temporal/complejidad_factorial_2.png" alt="Secuencia visual de 2.1.2.9 complejidad factorial · paso representativo 3 de 5"><figcaption>Secuencia visual de 2.1.2.9 complejidad factorial · paso representativo 3 de 5.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-2/analisis_eficiencia/complejidad_espacial/complejidad_factorial_1.png" alt="Secuencia visual de 2.1.2.9 complejidad factorial · paso representativo 4 de 5"><figcaption>Secuencia visual de 2.1.2.9 complejidad factorial · paso representativo 4 de 5.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-2/analisis_eficiencia/complejidad_espacial/complejidad_factorial_2.png" alt="Secuencia visual de 2.1.2.9 complejidad factorial · paso representativo 5 de 5"><figcaption>Secuencia visual de 2.1.2.9 complejidad factorial · paso representativo 5 de 5.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../8-complejidad-exponencial/">← 2.1.2.8 Complejidad exponencial</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../ejercicios-propuestos/">2.2 Ejercicios propuestos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
