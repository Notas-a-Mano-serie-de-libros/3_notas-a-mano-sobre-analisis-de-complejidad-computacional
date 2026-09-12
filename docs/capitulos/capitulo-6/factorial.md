<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 1 · Factorial recursivo

<span class="chapter-kicker">Capítulo 6</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

#### Código

<!-- book-code:start -->

##### Factorial recursivo

Implementación basada en el libro, página 229 (Java).

=== "Java"

    ```java
    public static int factorial(int n) {
        if (n < 0)
            throw new IllegalArgumentException("n debe ser no negativo");
        if (n > 12)
            throw new ArithmeticException("El factorial no cabe en int");
        if (n <= 1)
            return 1;
        else
            return Math.multiplyExact(n, factorial(n - 1));
    }
    ```

=== "Pseudocódigo"

    ```text
    función factorial(n)
        si n < 0 entonces
            error ValueError("n debe ser no negativo")
        si n > 12 entonces
            error OverflowError("El factorial no cabe en int de Java")
        si n <= 1 entonces
            retornar 1
        retornar n * factorial(n - 1)
    ```

=== "Python"

    ```python
    def factorial(n):
        if n < 0:
            raise ValueError("n debe ser no negativo")
        if n > 12:
            raise OverflowError("El factorial no cabe en int de Java")
        if n <= 1:
            return 1
        return n * factorial(n - 1)
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    int productoExacto(int a, int b) {
        int64_t resultado = (int64_t) a * b;
        if (resultado < INT_MIN || resultado > INT_MAX) {
            abort();
        }
        return (int) resultado;
    }

    int factorial(int n) {
        if (n < 0) {
            abort();
        }
        if (n > 12) {
            abort();
        }
        if (n <= 1) {
            return 1;
        }
        else {
            return productoExacto(n, factorial(n - 1));
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Entero no negativo. |
| `factorial(n-1)` | Resultado del subproblema. |

**Precondiciones:** n no negativo. Si el resultado no cabe en int, se lanza ArithmeticException en lugar de devolver un valor desbordado.

**Resultado:** Devuelve n!.

??? example "Ejemplo paso a paso"
    Entrada: `n = 3`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `factorial(3)` | Espera \(3 \times \operatorname{factorial}(2)\). |
    | `factorial(2)` | Espera \(2 \times \operatorname{factorial}(1)\). |
    | `factorial(1) = 1` | Caso base. |
    | `Retorno` | \(2 \times 1 = 2\); luego \(3 \times 2 = 6\). |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Ver código y editar entradas</summary><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div id="runner-c8aa4c6cf900" class="python-code-editor highlight" aria-label="Código Python · Factorial recursivo"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">factorial</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">n</span> <span class="o">&lt;</span> <span class="mi">0</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s2">"n debe ser no negativo"</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">n</span> <span class="o">&gt;</span> <span class="mi">12</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">raise</span> <span class="ne">OverflowError</span><span class="p">(</span><span class="s2">"El factorial no cabe en int de Java"</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">n</span> <span class="o">&lt;=</span> <span class="mi">1</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="n">n</span> <span class="o">*</span> <span class="n">factorial</span><span class="p">(</span><span class="n">n</span> <span class="o">-</span> <span class="mi">1</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 11" spellcheck="false" data-editable><span class="n">n</span> <span class="o">=</span> <span class="mi">3</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">resultado</span> <span class="o">=</span> <span class="n">factorial</span><span class="p">(</span><span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Resultado:"</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span></span></code></pre></div></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

##### Laboratorio y medición

La animación permite observar la estructura recursiva. El panel experimental ejecuta funciones Python: el tiempo y la memoria de ese panel corresponden a esas funciones y no a una ejecución del listado Java. La memoria se obtiene con tracemalloc; no mide directamente la pila de una JVM.

El experimento suma las llamadas del recorrido recursivo; no multiplica para calcular n!. Esto permite medir la cadena de llamadas sin introducir enteros factoriales de tamaño creciente.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/runtime/recursive_examples_analysis.py).

<!-- book-code:end -->

#### Análisis

Cada llamada reduce \(n\) en una unidad y realiza una multiplicación adicional:

\[
T(n)=T(n-1)+\Theta(1),\qquad T(1)=\Theta(1).
\]

Después de \(n-1\) expansiones se alcanza el caso base, de modo que \(T(n)\in\Theta(n)\). Las llamadas pendientes forman una cadena de profundidad \(n\), por lo que \(S(n)\in\Theta(n)\).

#### Simulación

El recorrido muestra cómo se apilan los valores \(n,n-1,\ldots,1\) y cómo los productos se resuelven durante el retorno.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-6/ejemplos/arbol_recursion_factorial.png" alt="Árbol de llamadas de ejemplo 1 · factorial recursivo"><figcaption>Árbol de llamadas de ejemplo 1 · factorial recursivo.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/comparacion_complejidad_for.png" alt="Comparación de crecimiento para ejemplo 1 · factorial recursivo"><figcaption>Comparación de crecimiento para ejemplo 1 · factorial recursivo.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a class="section-step__index" href="../">Capítulo 6</a><a class="section-step__next" href="../fibonacci/">Ejemplo 2 · Fibonacci recursivo ingenuo →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>
