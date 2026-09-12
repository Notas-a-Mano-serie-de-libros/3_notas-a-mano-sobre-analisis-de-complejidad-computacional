<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.1 Sumar dos números

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo1_(sumar_numeros).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

Este ejemplo analiza una secuencia de una sola operación aritmética. El tamaño de referencia \(n\) cambia, pero la cantidad de instrucciones ejecutadas permanece fija.

### Código analizado

<!-- book-code:start -->

#### Suma de dos enteros

Implementación basada en el libro, página 150 (Java).

=== "Java"

    ```java
    public static int sumar(int a, int b) {
        return Math.addExact(a, b);
    }
    ```

=== "Pseudocódigo"

    ```text
    función sumar(a, b)
        resultado ← a + b
        si no -2147483648 <= resultado <= 2147483647 entonces
            error OverflowError("El resultado no cabe en int de Java")
        retornar resultado
    ```

=== "Python"

    ```python
    def sumar(a, b):
        resultado = a + b
        if not -2147483648 <= resultado <= 2147483647:
            raise OverflowError("El resultado no cabe en int de Java")
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

    int sumaExacta(int a, int b) {
        int64_t resultado = (int64_t) a + b;
        if (resultado < INT_MIN || resultado > INT_MAX) {
            abort();
        }
        return (int) resultado;
    }

    int sumar(int a, int b) {
        return sumaExacta(a, b);
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `a, b` | Enteros que se suman. |

**Precondiciones:** La suma matemática debe caber en int si se espera un resultado exacto.

**Resultado:** Devuelve a + b.

??? example "Ejemplo paso a paso"
    Entrada: `a = 2, b = 3`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `a = 2, b = 3` | Se reciben los operandos. |
    | `a + b` | Se devuelve 5. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Ver código y editar entradas</summary><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div id="runner-be0f6b02d91f" class="python-code-editor highlight" aria-label="Código Python · Suma de dos enteros"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">sumar</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="n">resultado</span> <span class="o">=</span> <span class="n">a</span> <span class="o">+</span> <span class="n">b</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="ow">not</span> <span class="o">-</span><span class="mi">2147483648</span> <span class="o">&lt;=</span> <span class="n">resultado</span> <span class="o">&lt;=</span> <span class="mi">2147483647</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">raise</span> <span class="ne">OverflowError</span><span class="p">(</span><span class="s2">"El resultado no cabe en int de Java"</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="n">resultado</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 8" spellcheck="false" data-editable><span class="n">a</span> <span class="o">=</span> <span class="mi">2</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 9" spellcheck="false" data-editable><span class="n">b</span> <span class="o">=</span> <span class="mi">3</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">resultado</span> <span class="o">=</span> <span class="n">sumar</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Resultado:"</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span></span></code></pre></div></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

Los experimentos ejecutan adaptaciones Python. El tiempo excluye la preparación y se promedia por ejecución. La memoria representa el incremento de pico observado por tracemalloc durante la operación, sin incluir la entrada preparada; no es el tamaño de la memoria de una máquina Java.

La suma se mide sobre dos operandos preparados.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/runtime/experimental_analysis.py).

<!-- book-code:end -->

### Análisis esperado

#### Complejidad temporal

\(T(n)\in O(1)\) porque la suma ejecuta una cantidad constante de operaciones para cada valor de \(n\).

#### Complejidad espacial

\(S(n)\in O(1)\) porque solo se mantienen dos operandos y el resultado.

### Simulaciones experimentales

Cada experimento ejecuta la adaptación Python descrita en «Laboratorio y medición» para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La entrada preparada se excluye de la medición. Las reservas realizadas dentro de la operación sí se incluyen; la memoria observada corresponde al incremento de pico de Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_suma_dos_numeros_tiempo.png" alt="Comportamiento temporal experimental de 4.4.4.1 sumar dos números"><figcaption>Comportamiento temporal experimental de 4.4.4.1 sumar dos números.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_suma_dos_numeros_espacio.png" alt="Comportamiento espacial experimental de 4.4.4.1 sumar dos números"><figcaption>Comportamiento espacial experimental de 4.4.4.1 sumar dos números.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo2-imprimir-elementos-arreglo/">4.4.4.2 Imprimir los elementos de un arreglo →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
