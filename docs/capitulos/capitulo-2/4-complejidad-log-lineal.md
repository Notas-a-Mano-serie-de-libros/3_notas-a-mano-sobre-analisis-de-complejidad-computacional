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

#### Ordenamiento por mezcla y combinación

Implementación basada en el libro, página 247 (Java).

=== "Java"

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

=== "Pseudocódigo"

    ```text
    función ordenar(arr, a, b)
        si a >= b entonces
            retornar
        m ← a + (b - a) div 2
        ordenar(arr, a, m)
        ordenar(arr, m + 1, b)
        combinar(arr, a, m, b)


    función combinar(arr, a, m, b)
        izquierda ← arr[a:m + 1]
        derecha ← arr[m + 1:b + 1]
        i ← 0
        j ← 0
        k ← a
        mientras i < longitud(izquierda) y j < longitud(derecha)
            si izquierda[i] <= derecha[j] entonces
                arr[k] ← izquierda[i]
                i += 1
            si no
                arr[k] ← derecha[j]
                j += 1
            k += 1
        mientras i < longitud(izquierda)
            arr[k] ← izquierda[i]
            i += 1
            k += 1
        mientras j < longitud(derecha)
            arr[k] ← derecha[j]
            j += 1
            k += 1
    ```

=== "Python"

    ```python
    def ordenar(arr, a, b):
        if a >= b:
            return
        m = a + (b - a) // 2
        ordenar(arr, a, m)
        ordenar(arr, m + 1, b)
        combinar(arr, a, m, b)


    def combinar(arr, a, m, b):
        izquierda = arr[a:m + 1]
        derecha = arr[m + 1:b + 1]
        i = 0
        j = 0
        k = a
        while i < len(izquierda) and j < len(derecha):
            if izquierda[i] <= derecha[j]:
                arr[k] = izquierda[i]
                i += 1
            else:
                arr[k] = derecha[j]
                j += 1
            k += 1
        while i < len(izquierda):
            arr[k] = izquierda[i]
            i += 1
            k += 1
        while j < len(derecha):
            arr[k] = derecha[j]
            j += 1
            k += 1
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    void combinar(int arr[], int a, int m, int b);

    void ordenar(int arr[], int a, int b) {
        if (a >= b) {
            return;
        }
        int m = a + (b - a) / 2;
        ordenar(arr, a, m);
        ordenar(arr, m + 1, b);
        combinar(arr, a, m, b);
    }

    void combinar(int arr[], int a, int m, int b) {
        int ni = m - a + 1;
        int nd = b - m;
        int *izquierda = malloc((size_t) ni * sizeof(int));
        int *derecha = malloc((size_t) nd * sizeof(int));
        if (izquierda == NULL || derecha == NULL) {
            free(izquierda);
            free(derecha);
            abort();
        }
        for (int i = 0; i < ni; i++) {
            izquierda[i] = arr[a + i];
        }
        for (int j = 0; j < nd; j++) {
            derecha[j] = arr[m + 1 + j];
        }
        int i = 0, j = 0, k = a;
        while (i < ni && j < nd) {
            if (izquierda[i] <= derecha[j]) {
                arr[k++] = izquierda[i++];
            } else {
                arr[k++] = derecha[j++];
            }
        }
        while (i < ni) {
            arr[k++] = izquierda[i++];
        }
        while (j < nd) {
            arr[k++] = derecha[j++];
        }
        free(izquierda);
        free(derecha);
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo que se modifica. |
| `a, b` | Extremos inclusivos del intervalo. |
| `m` | Índice que separa las mitades. |
| `izquierda, derecha` | Copias temporales de las mitades. |
| `i, j, k` | Índices dentro de las copias y del destino. |

**Precondiciones:** arr no nulo; intervalo válido o vacío. Importar java.util.Arrays.

**Resultado:** Ordena arr[a..b] en orden ascendente; no devuelve un arreglo nuevo.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>El navegador facilita la ejecución de código Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Python; el código se ejecuta en tu navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-e32ce151575f">Código Python · Ordenamiento por mezcla y combinación</label><div class="python-code-editor"><div class="highlight" aria-hidden="true"><pre><code><span class="k">def</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">):</span>
    <span class="k">if</span> <span class="n">a</span> <span class="o">&gt;=</span> <span class="n">b</span><span class="p">:</span>
        <span class="k">return</span>
    <span class="n">m</span> <span class="o">=</span> <span class="n">a</span> <span class="o">+</span> <span class="p">(</span><span class="n">b</span> <span class="o">-</span> <span class="n">a</span><span class="p">)</span> <span class="o">//</span> <span class="mi">2</span>
    <span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">m</span><span class="p">)</span>
    <span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">m</span> <span class="o">+</span> <span class="mi">1</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span>
    <span class="n">combinar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">m</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span>


<span class="k">def</span><span class="w"> </span><span class="nf">combinar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">m</span><span class="p">,</span> <span class="n">b</span><span class="p">):</span>
    <span class="n">izquierda</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">a</span><span class="p">:</span><span class="n">m</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]</span>
    <span class="n">derecha</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">m</span> <span class="o">+</span> <span class="mi">1</span><span class="p">:</span><span class="n">b</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]</span>
    <span class="n">i</span> <span class="o">=</span> <span class="mi">0</span>
    <span class="n">j</span> <span class="o">=</span> <span class="mi">0</span>
    <span class="n">k</span> <span class="o">=</span> <span class="n">a</span>
    <span class="k">while</span> <span class="n">i</span> <span class="o">&lt;</span> <span class="nb">len</span><span class="p">(</span><span class="n">izquierda</span><span class="p">)</span> <span class="ow">and</span> <span class="n">j</span> <span class="o">&lt;</span> <span class="nb">len</span><span class="p">(</span><span class="n">derecha</span><span class="p">):</span>
        <span class="k">if</span> <span class="n">izquierda</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">&lt;=</span> <span class="n">derecha</span><span class="p">[</span><span class="n">j</span><span class="p">]:</span>
            <span class="n">arr</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="n">izquierda</span><span class="p">[</span><span class="n">i</span><span class="p">]</span>
            <span class="n">i</span> <span class="o">+=</span> <span class="mi">1</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="n">arr</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="n">derecha</span><span class="p">[</span><span class="n">j</span><span class="p">]</span>
            <span class="n">j</span> <span class="o">+=</span> <span class="mi">1</span>
        <span class="n">k</span> <span class="o">+=</span> <span class="mi">1</span>
    <span class="k">while</span> <span class="n">i</span> <span class="o">&lt;</span> <span class="nb">len</span><span class="p">(</span><span class="n">izquierda</span><span class="p">):</span>
        <span class="n">arr</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="n">izquierda</span><span class="p">[</span><span class="n">i</span><span class="p">]</span>
        <span class="n">i</span> <span class="o">+=</span> <span class="mi">1</span>
        <span class="n">k</span> <span class="o">+=</span> <span class="mi">1</span>
    <span class="k">while</span> <span class="n">j</span> <span class="o">&lt;</span> <span class="nb">len</span><span class="p">(</span><span class="n">derecha</span><span class="p">):</span>
        <span class="n">arr</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="n">derecha</span><span class="p">[</span><span class="n">j</span><span class="p">]</span>
        <span class="n">j</span> <span class="o">+=</span> <span class="mi">1</span>
        <span class="n">k</span> <span class="o">+=</span> <span class="mi">1</span>

<span class="c1"># Entradas editables del ejemplo.</span>
<span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">3</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">]</span>
<span class="n">a</span> <span class="o">=</span> <span class="mi">0</span>
<span class="n">b</span> <span class="o">=</span> <span class="mi">2</span>

<span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo inicial:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span>
<span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo ordenado:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span>
</code></pre></div><textarea id="runner-e32ce151575f" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" rows="14">def ordenar(arr, a, b):
    if a &gt;= b:
        return
    m = a + (b - a) // 2
    ordenar(arr, a, m)
    ordenar(arr, m + 1, b)
    combinar(arr, a, m, b)


def combinar(arr, a, m, b):
    izquierda = arr[a:m + 1]
    derecha = arr[m + 1:b + 1]
    i = 0
    j = 0
    k = a
    while i &lt; len(izquierda) and j &lt; len(derecha):
        if izquierda[i] &lt;= derecha[j]:
            arr[k] = izquierda[i]
            i += 1
        else:
            arr[k] = derecha[j]
            j += 1
        k += 1
    while i &lt; len(izquierda):
        arr[k] = izquierda[i]
        i += 1
        k += 1
    while j &lt; len(derecha):
        arr[k] = derecha[j]
        j += 1
        k += 1

# Entradas editables del ejemplo.
arr = [3, 1, 2]
a = 0
b = 2

print(&quot;Arreglo inicial:&quot;, arr)
ordenar(arr, a, b)
print(&quot;Arreglo ordenado:&quot;, arr)
</textarea></div></details><div class="example-runner-actions"><button type="button" data-run><span class="button-icon" aria-hidden="true">▶</span><span>Ejecutar</span></button><button type="button" data-stop disabled><span class="button-icon" aria-hidden="true">■</span><span>Detener</span></button><button type="button" data-reset><span class="button-icon" aria-hidden="true">↻</span><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

El listado Java procede de la página del libro indicada arriba. El laboratorio ejecuta una adaptación en Python; compara el patrón de crecimiento, no los tiempos de Java con los de Python.

El tiempo se promedia por ejecución; la preparación de las entradas se realiza antes de cronometrar. Las gráficas teóricas y las mediciones experimentales se identifican por separado.

El experimento usa sorted de Python, no el método de mezcla del libro. Ambos permiten estudiar el crecimiento n log n, pero sus operaciones y constantes difieren.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/runtime/complexity_animations.py).

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
