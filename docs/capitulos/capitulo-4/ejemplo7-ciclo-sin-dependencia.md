<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.7 Ciclo sin dependencia de la entrada

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo7_(ciclo_sin_dependencia).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ciclo ejecuta siempre \(10\,000\) iteraciones. Esa cantidad es fija y no cambia con el valor de \(n\).

### Código analizado

<!-- book-code:start -->

#### Ciclo con límite fijo

Implementación basada en el libro, página 164 (Java).

=== "Java"

    ```java
    public static void iterar() {
        for (int i = 0; i < 10000000; i++) {
            System.out.println(i);
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función iterar()
        para i en rango(10000000)
            imprimir(i)
    ```

=== "Python"

    ```python
    def iterar():
        for i in range(10000000):
            print(i)
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    void iterar() {
        for (int i = 0; i < 10000000; i++) {
            printf("%d\n", i);
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `i` | Índice desde cero hasta 9 999 999. |

**Precondiciones:** No recibe parámetros; dispone de una salida para imprimir.

**Resultado:** Imprime diez millones de valores.

??? example "Ejemplo paso a paso"
    Entrada: `Inicio del recorrido`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `i = 0` | Imprime 0. |
    | `i = 1` | Imprime 1; continúa hasta 9 999 999. |
    | `i = 10000000` | Termina. El límite no depende de una entrada n. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Ver código y editar entradas</summary><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div id="runner-201992ad7ecd" class="python-code-editor highlight" aria-label="Código Python · Ciclo con límite fijo"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">iterar</span><span class="p">():</span></span><span class="python-code-line" data-code-line>    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">10000000</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="nb">print</span><span class="p">(</span><span class="n">i</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">iterar</span><span class="p">()</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Ejemplo finalizado"</span><span class="p">)</span></span></code></pre></div></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

Los experimentos ejecutan adaptaciones Python. El tiempo excluye la preparación y se promedia por ejecución. La memoria representa el incremento de pico observado por tracemalloc durante la operación, sin incluir la entrada preparada; no es el tamaño de la memoria de una máquina Java.

El Java imprime 10 000 000 valores. El experimento realiza 10 000 iteraciones sin impresión, para aislar el crecimiento constante respecto del tamaño de entrada.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/runtime/experimental_analysis.py).

<!-- book-code:end -->

### Análisis esperado

#### Complejidad temporal

\(T(n)\in O(1)\) respecto a \(n\), aunque la constante de trabajo sea grande.

#### Complejidad espacial

\(S(n)\in O(1)\) porque el ciclo utiliza una cantidad fija de variables.

### Simulaciones experimentales

Cada experimento ejecuta la adaptación Python descrita en «Laboratorio y medición» para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La entrada preparada se excluye de la medición. Las reservas realizadas dentro de la operación sí se incluyen; la memoria observada corresponde al incremento de pico de Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ciclo_sin_dependencia_tiempo.png" alt="Comportamiento temporal experimental de 4.4.4.7 ciclo sin dependencia de la entrada"><figcaption>Comportamiento temporal experimental de 4.4.4.7 ciclo sin dependencia de la entrada.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ciclo_sin_dependencia_espacio.png" alt="Comportamiento espacial experimental de 4.4.4.7 ciclo sin dependencia de la entrada"><figcaption>Comportamiento espacial experimental de 4.4.4.7 ciclo sin dependencia de la entrada.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo6/">← 4.4.4.6 Algoritmo con estructura deliberadamente compleja</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo8/">4.4.4.8 Ciclo con límite fijo y función de costo lineal →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
