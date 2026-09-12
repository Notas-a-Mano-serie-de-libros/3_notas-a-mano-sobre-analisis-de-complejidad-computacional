<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.5 Ciclos con incremento no lineal

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo5_(ciclos_incremento_no_lineal).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ciclo interior avanza de dos en dos, pero continúa recorriendo una cantidad proporcional a \(n\) de posiciones por cada fila.

### Código analizado

<!-- book-code:start -->

#### Ciclo interior con paso dos

Implementación basada en el libro, página 158 (Java).

=== "Java"

    ```java
    public static void recorrerMatrizVacia(int m, int n) {
        int[][] matriz = new int[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j+=2) {
                // Sin operaciones internas en este ciclo
            }
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función recorrerMatrizVacia(m, n)
        matriz ← [[0] * n for _ in rango(m)]
        para i en rango(m)
            para j en rango(0, n, 2)
                sin operaciones  # Sin operaciones internas.
    ```

=== "Python"

    ```python
    def recorrerMatrizVacia(m, n):
        matriz = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(0, n, 2):
                pass  # Sin operaciones internas.
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    void recorrerMatrizVacia(int m, int n) {
        // malloc/calloc usa un bloque contiguo en esta adaptación.
        int *matriz = calloc((size_t) m * n, sizeof(int));
        if (m > 0 && n > 0 && matriz == NULL) {
            abort();
        }
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j += 2) {
                // Sin operaciones internas.
            }
        }
        free(matriz);
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `m, n` | Filas y columnas de la matriz nueva. |
| `i, j` | Fila actual y columna que avanza de dos en dos. |

**Precondiciones:** m y n no negativos; memoria suficiente.

**Resultado:** Crea una matriz; el cuerpo del ciclo interior no ejecuta operaciones.

??? example "Ejemplo paso a paso"
    Entrada: `m = 2, n = 3`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `new int[2][3]` | Reserva la matriz. |
    | `i = 0; j = 0, 2` | Ejecuta el control del ciclo, con cuerpo vacío. |
    | `i = 1; j = 0, 2` | Repite en la segunda fila. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Ver código y editar entradas</summary><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div id="runner-822a694e4b44" class="python-code-editor highlight" aria-label="Código Python · Ciclo interior con paso dos"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">recorrerMatrizVacia</span><span class="p">(</span><span class="n">m</span><span class="p">,</span> <span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="n">matriz</span> <span class="o">=</span> <span class="p">[[</span><span class="mi">0</span><span class="p">]</span> <span class="o">*</span> <span class="n">n</span> <span class="k">for</span> <span class="n">_</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">m</span><span class="p">)]</span></span><span class="python-code-line" data-code-line>    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">m</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="n">n</span><span class="p">,</span> <span class="mi">2</span><span class="p">):</span></span><span class="python-code-line" data-code-line>            <span class="k">pass</span>  <span class="c1"># Sin operaciones internas.</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 8" spellcheck="false" data-editable><span class="n">m</span> <span class="o">=</span> <span class="mi">2</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 9" spellcheck="false" data-editable><span class="n">n</span> <span class="o">=</span> <span class="mi">3</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">recorrerMatrizVacia</span><span class="p">(</span><span class="n">m</span><span class="p">,</span> <span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Ejemplo finalizado"</span><span class="p">)</span></span></code></pre></div></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

Los experimentos ejecutan adaptaciones Python. El tiempo excluye la preparación y se promedia por ejecución. La memoria representa el incremento de pico observado por tracemalloc durante la operación, sin incluir la entrada preparada; no es el tamaño de la memoria de una máquina Java.

El experimento fija \(m = n\), crea la matriz dentro de la operación y lee las posiciones pares. El Java tiene el cuerpo interior vacío.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/runtime/experimental_analysis.py).

<!-- book-code:end -->

### Análisis esperado

#### Complejidad temporal

El control del ciclo interior realiza \(m\cdot\lceil n/2\rceil\) iteraciones con cuerpo vacío. La reserva e inicialización de la matriz domina con \(\Theta(m\cdot n)\) para dimensiones positivas. Si \(m=n\), \(T(n)\in\Theta(n^2)\); avanzar de dos en dos modifica una constante.

#### Complejidad espacial

La matriz creada ocupa \(\Theta(1+m+m\cdot n)\). Para dimensiones positivas es \(\Theta(m\cdot n)\); si \(m=n\), \(S(n)\in\Theta(n^2)\).

### Simulaciones experimentales

Cada experimento ejecuta la adaptación Python descrita en «Laboratorio y medición» para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La entrada preparada se excluye de la medición. Las reservas realizadas dentro de la operación sí se incluyen; la memoria observada corresponde al incremento de pico de Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-4/ejemplos/recorrer_matriz_vacia_tiempo.png" alt="Comportamiento temporal experimental de 4.4.4.5 ciclos con incremento no lineal"><figcaption>Comportamiento temporal experimental de 4.4.4.5 ciclos con incremento no lineal.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-4/ejemplos/recorrer_matriz_vacia_espacio.png" alt="Comportamiento espacial experimental de 4.4.4.5 ciclos con incremento no lineal"><figcaption>Comportamiento espacial experimental de 4.4.4.5 ciclos con incremento no lineal.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo4-inicializar-matriz-variable/">← 4.4.4.4 Inicializar una matriz variable</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo6/">4.4.4.6 Algoritmo con estructura deliberadamente compleja →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
