<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.6 Complejidad cúbica

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/6_complejidad_cubica.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: multiplicación clásica de matrices

El ejemplo calcula cada posición de la matriz resultado mediante tres índices: fila, columna y posición interna de acumulación.

Como los tres recorridos dependen de \(n\), el número total de operaciones crece de acuerdo con \(n^3\).


---

### Código del libro asociado

<!-- book-code:start -->

#### Multiplicación de matrices cuadradas

Implementación basada en el libro, página 177 (Java).

=== "Java"

    ```java
    public int[][] multiplicar(int[][] a, int[][] b) {
        int n = a.length;
        int[][] resultado = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    resultado[i][j] = Math.addExact(resultado[i][j], Math.multiplyExact(a[i][k], b[k][j]));
                }
            }
        }
        return resultado;
    }
    ```

=== "Pseudocódigo"

    ```text
    función multiplicar(a, b)
        n ← longitud(a)
        resultado ← [[0] * n for _ in rango(n)]
        para i en rango(n)
            para j en rango(n)
                para k en rango(n)
                    producto ← a[i][k] * b[k][j]
                    si no -2147483648 <= producto <= 2147483647 entonces
                        error OverflowError("El producto no cabe en int de Java")
                    suma ← resultado[i][j] + producto
                    si no -2147483648 <= suma <= 2147483647 entonces
                        error OverflowError("La suma no cabe en int de Java")
                    resultado[i][j] ← suma
        retornar resultado
    ```

=== "Python"

    ```python
    def multiplicar(a, b):
        n = len(a)
        resultado = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    producto = a[i][k] * b[k][j]
                    if not -2147483648 <= producto <= 2147483647:
                        raise OverflowError("El producto no cabe en int de Java")
                    suma = resultado[i][j] + producto
                    if not -2147483648 <= suma <= 2147483647:
                        raise OverflowError("La suma no cabe en int de Java")
                    resultado[i][j] = suma
        return resultado
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    // resultado es una matriz de salida reservada por el llamador.
    void multiplicar(int n, int a[n][n], int b[n][n], int resultado[n][n]) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                resultado[i][j] = 0;
                for (int k = 0; k < n; k++) {
                    int64_t producto = (int64_t) a[i][k] * b[k][j];
                    if (producto < INT_MIN || producto > INT_MAX) {
                        abort();
                    }
                    int64_t suma = (int64_t) resultado[i][j] + producto;
                    if (suma < INT_MIN || suma > INT_MAX) {
                        abort();
                    }
                    resultado[i][j] = (int) suma;
                }
            }
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, las dimensiones se reciben como parámetros; las matrices de salida las reserva el llamador. La reserva de memoria se analiza por separado de los ciclos mostrados.

| Parámetro o variable | Significado |
| --- | --- |
| `a, b` | Matrices cuadradas de igual dimensión. |
| `n` | Cantidad de filas y columnas. |
| `resultado` | Matriz nueva. |
| `i, j, k` | Fila, columna e índice de acumulación. |

**Precondiciones:** Matrices no nulas, cuadradas y de igual dimensión; productos y sumas representables en int.

**Resultado:** Devuelve la matriz producto \(a \times b\).

??? example "Ejemplo paso a paso"
    Entrada: `a = [[1, 2], [3, 4]], b = [[2, 0], [1, 2]]`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `i = 0, j = 0; k = 0, 1` | Acumula \(1 \times 2 + 2 \times 1 = 4\). |
    | `i = 0, j = 1` | Acumula \(1 \times 0 + 2 \times 2 = 4\). |
    | `Segunda fila` | Obtiene 10 y 8; devuelve [[4, 4], [10, 8]]. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Ver código y editar entradas</summary><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div id="runner-f3bbc29baeb8" class="python-code-editor highlight" aria-label="Código Python · Multiplicación de matrices cuadradas"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">multiplicar</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="n">n</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">a</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="n">resultado</span> <span class="o">=</span> <span class="p">[[</span><span class="mi">0</span><span class="p">]</span> <span class="o">*</span> <span class="n">n</span> <span class="k">for</span> <span class="n">_</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">n</span><span class="p">)]</span></span><span class="python-code-line" data-code-line>    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>            <span class="k">for</span> <span class="n">k</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>                <span class="n">producto</span> <span class="o">=</span> <span class="n">a</span><span class="p">[</span><span class="n">i</span><span class="p">][</span><span class="n">k</span><span class="p">]</span> <span class="o">*</span> <span class="n">b</span><span class="p">[</span><span class="n">k</span><span class="p">][</span><span class="n">j</span><span class="p">]</span></span><span class="python-code-line" data-code-line>                <span class="k">if</span> <span class="ow">not</span> <span class="o">-</span><span class="mi">2147483648</span> <span class="o">&lt;=</span> <span class="n">producto</span> <span class="o">&lt;=</span> <span class="mi">2147483647</span><span class="p">:</span></span><span class="python-code-line" data-code-line>                    <span class="k">raise</span> <span class="ne">OverflowError</span><span class="p">(</span><span class="s2">"El producto no cabe en int de Java"</span><span class="p">)</span></span><span class="python-code-line" data-code-line>                <span class="n">suma</span> <span class="o">=</span> <span class="n">resultado</span><span class="p">[</span><span class="n">i</span><span class="p">][</span><span class="n">j</span><span class="p">]</span> <span class="o">+</span> <span class="n">producto</span></span><span class="python-code-line" data-code-line>                <span class="k">if</span> <span class="ow">not</span> <span class="o">-</span><span class="mi">2147483648</span> <span class="o">&lt;=</span> <span class="n">suma</span> <span class="o">&lt;=</span> <span class="mi">2147483647</span><span class="p">:</span></span><span class="python-code-line" data-code-line>                    <span class="k">raise</span> <span class="ne">OverflowError</span><span class="p">(</span><span class="s2">"La suma no cabe en int de Java"</span><span class="p">)</span></span><span class="python-code-line" data-code-line>                <span class="n">resultado</span><span class="p">[</span><span class="n">i</span><span class="p">][</span><span class="n">j</span><span class="p">]</span> <span class="o">=</span> <span class="n">suma</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="n">resultado</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 17" spellcheck="false" data-editable><span class="n">a</span> <span class="o">=</span> <span class="p">[[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">],</span> <span class="p">[</span><span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">]]</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 18" spellcheck="false" data-editable><span class="n">b</span> <span class="o">=</span> <span class="p">[[</span><span class="mi">2</span><span class="p">,</span> <span class="mi">0</span><span class="p">],</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">]]</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">resultado</span> <span class="o">=</span> <span class="n">multiplicar</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Resultado:"</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span></span></code></pre></div></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

El listado Java procede de la página del libro indicada arriba. El laboratorio ejecuta una adaptación en Python; compara el patrón de crecimiento, no los tiempos de Java con los de Python.

El tiempo se promedia por ejecución; la preparación de las entradas se realiza antes de cronometrar. Las gráficas teóricas y las mediciones experimentales se identifican por separado.

El experimento multiplica matrices \(n \times n\) y crea la matriz resultado dentro de la operación medida.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/runtime/complexity_animations.py).

<!-- book-code:end -->

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad cúbica aparece cuando tres recorridos anidados dependen del tamaño \(n\). Este patrón es común en algoritmos que combinan tres dimensiones o tres índices.

Un ejemplo representativo es la multiplicación clásica de matrices cuadradas, donde cada posición del resultado se calcula acumulando productos a lo largo de una tercera dimensión.

Para una entrada de tamaño \(n\), una función de costo cúbico puede expresarse como:

\[
T(n) = cn^3
\]

donde \(n^3\) representa la cantidad de iteraciones producidas por tres ciclos anidados.

El crecimiento es muy pronunciado: duplicar \(n\) puede multiplicar el trabajo aproximadamente por ocho.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_cubica.png" alt="Representación gráfica de 2.1.2.6 complejidad cúbica"><figcaption>Representación gráfica de 2.1.2.6 complejidad cúbica.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../5-complejidad-cuadratica/">← 2.1.2.5 Complejidad cuadrática</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../7-complejidad-polinomial-general/">2.1.2.7 Complejidad polinomial general →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
