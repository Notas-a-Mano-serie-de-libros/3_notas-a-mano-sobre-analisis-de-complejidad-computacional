<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.4 Complejidad log-lineal

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/4_complejidad_log_lineal.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: ordenar una lista

El ejemplo usa la operación de ordenamiento del entorno para ordenar una colección. Aunque la implementación interna puede incluir optimizaciones, el comportamiento esperado de los ordenamientos eficientes se aproxima a una forma log-lineal.

La simulación se centra en observar cómo el costo crece al ordenar entradas cada vez mayores.


---

### Código del libro asociado

<!-- book-code:start -->

Listado original del libro, página 247 (Java).

```java
public void ordenar(int[] arr, int a, int b) {
    if (a >= b)
        return;
    int m = a + (b - a) / 2;
    ordenar(arr, a, m);
    ordenar(arr, m + 1, b);
    combinar(arr, a, m, b);
}
public void combinar(int[] arr, int a, int m, int b) {
    int[] izquierda = Arrays.copyOfRange(arr, a, m + 1);
    int[] derecha = Arrays.copyOfRange(arr, m + 1, b + 1);
    int i = 0, j = 0, k = a;
    while (i < izquierda.length && j < derecha.length) {
        if (izquierda[i] <= derecha[j])
            arr[k++] = izquierda[i++];
        else
            arr[k++] = derecha[j++];
    }
    while (i < izquierda.length)
        arr[k++] = izquierda[i++];
    while (j < derecha.length)
        arr[k++] = derecha[j++];
}
```

<!-- book-code:end -->

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad log-lineal aparece en algoritmos que combinan trabajo lineal con una estructura de división por niveles. Es frecuente en algoritmos eficientes de ordenamiento.

La entrada se procesa varias veces, pero no una cantidad lineal de niveles, sino una cantidad logarítmica. Por eso el costo queda entre el crecimiento lineal y el cuadrático.

Para una entrada de tamaño \(n\), una función de costo log-lineal puede expresarse como:

\[
T(n) = cn \log_2(n)
\]

donde \(n\) representa el trabajo realizado por nivel y \(\log_2(n)\) representa la cantidad de niveles de división o combinación.

Esta forma describe procedimientos que hacen trabajo proporcional a todos los elementos, pero repiten ese trabajo a lo largo de una cantidad logarítmica de etapas.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_log_lineal.png" alt="Representación gráfica de 2.1.2.4 complejidad log-lineal"><figcaption>Representación gráfica de 2.1.2.4 complejidad log-lineal.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../3-complejidad-lineal/">← 2.1.2.3 Complejidad lineal</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../5-complejidad-cuadratica/">2.1.2.5 Complejidad cuadrática →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
