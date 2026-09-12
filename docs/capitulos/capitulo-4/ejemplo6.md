<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.6 Algoritmo con estructura deliberadamente compleja

<span class="chapter-kicker">Capítulo 4</span>

Este ejemplo combina un ciclo externo, dos ciclos internos y llamadas a funciones con costos propios. Su propósito es mostrar que la apariencia del anidamiento no basta: cada cuerpo debe sustituirse por su función de costo antes de aplicar dominancia.

## Código analizado

<!-- book-code:start -->

#### Ciclos secuenciales dentro de un ciclo

Implementación basada en el libro, página 161 (Java).

=== "Java"

    ```java
    public static void imprimirElementos(int m, int n) {
        for (int i = 0; i < m; i++) {
            System.out.println(i);
            for (int j = 0; j < n; j++) {
                System.out.println(j);
            }
            for (int k = n; k > 1; k = k/2) {
                System.out.println(k);
                foo2();
            }
            foo1();
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función imprimirElementos(m, n)
        para i en rango(m)
            imprimir(i)
            para j en rango(n)
                imprimir(j)
            k ← n
            mientras k > 1
                imprimir(k)
                foo2()
                k //= 2
            foo1()
    ```

=== "Python"

    ```python
    def imprimirElementos(m, n):
        for i in range(m):
            print(i)
            for j in range(n):
                print(j)
            k = n
            while k > 1:
                print(k)
                foo2()
                k //= 2
            foo1()
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    void foo1(void);
    void foo2(void);

    void imprimirElementos(int m, int n) {
        for (int i = 0; i < m; i++) {
            printf("%d\n", i);
            for (int j = 0; j < n; j++) {
                printf("%d\n", j);
            }
            for (int k = n; k > 1; k /= 2) {
                printf("%d\n", k);
                foo2();
            }
            foo1();
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `m` | Número de repeticiones exteriores. |
| `n` | Límite del ciclo lineal e inicio del ciclo de división. |
| `i, j, k` | Variables de control. |
| `foo1, foo2` | Operaciones auxiliares cuyo costo debe especificarse. |

**Precondiciones:** m y n no negativos; foo1 y foo2 definidas.

**Resultado:** Imprime los índices y ejecuta las auxiliares; no devuelve un valor.

??? example "Ejemplo paso a paso"
    Entrada: `m = 1, n = 4`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `i = 0` | Imprime 0. |
    | `j = 0, 1, 2, 3` | Imprime los cuatro valores. |
    | `k = 4, 2` | Imprime cada k y llama a foo2 dos veces. |
    | `foo1()` | Ejecuta una llamada al terminar la repetición exterior. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Ver código y editar entradas</summary><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div id="runner-db7ad92b2a9a" class="python-code-editor highlight" aria-label="Código Python · Ciclos secuenciales dentro de un ciclo"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">imprimirElementos</span><span class="p">(</span><span class="n">m</span><span class="p">,</span> <span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">m</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="nb">print</span><span class="p">(</span><span class="n">i</span><span class="p">)</span></span><span class="python-code-line" data-code-line>        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>            <span class="nb">print</span><span class="p">(</span><span class="n">j</span><span class="p">)</span></span><span class="python-code-line" data-code-line>        <span class="n">k</span> <span class="o">=</span> <span class="n">n</span></span><span class="python-code-line" data-code-line>        <span class="k">while</span> <span class="n">k</span> <span class="o">&gt;</span> <span class="mi">1</span><span class="p">:</span></span><span class="python-code-line" data-code-line>            <span class="nb">print</span><span class="p">(</span><span class="n">k</span><span class="p">)</span></span><span class="python-code-line" data-code-line>            <span class="n">foo2</span><span class="p">()</span></span><span class="python-code-line" data-code-line>            <span class="n">k</span> <span class="o">//=</span> <span class="mi">2</span></span><span class="python-code-line" data-code-line>        <span class="n">foo1</span><span class="p">()</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 14" spellcheck="false" data-editable><span class="n">m</span> <span class="o">=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 15" spellcheck="false" data-editable><span class="n">n</span> <span class="o">=</span> <span class="mi">4</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Completa estas auxiliares según el problema que estés analizando.</span></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">foo1</span><span class="p">():</span></span><span class="python-code-line" data-code-line>    <span class="k">raise</span> <span class="ne">NotImplementedError</span><span class="p">(</span><span class="s2">"Completa foo1 en el editor"</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">foo2</span><span class="p">():</span></span><span class="python-code-line" data-code-line>    <span class="k">raise</span> <span class="ne">NotImplementedError</span><span class="p">(</span><span class="s2">"Completa foo2 en el editor"</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">foo</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">raise</span> <span class="ne">NotImplementedError</span><span class="p">(</span><span class="s2">"Completa foo en el editor"</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">imprimirElementos</span><span class="p">(</span><span class="n">m</span><span class="p">,</span> <span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Ejemplo finalizado"</span><span class="p">)</span></span></code></pre></div></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

Los experimentos ejecutan adaptaciones Python. El tiempo excluye la preparación y se promedia por ejecución. La memoria representa el incremento de pico observado por tracemalloc durante la operación, sin incluir la entrada preparada; no es el tamaño de la memoria de una máquina Java.

El libro no propone simulación para este ejemplo; los costos de foo1 y foo2 se conservan simbólicamente.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/runtime/experimental_analysis.py).

<!-- book-code:end -->

## Análisis esperado

El conteo debe conservar los costos de las funciones llamadas. Antes de simplificar, la forma general es \(T(m,n)\in O\!\left(m\cdot[n+\log_2(n) \cdot (1+T_{foo2}(n))+T_{foo1}(n)]\right)\). Solo después se sustituyen \(T_{foo1}\) y \(T_{foo2}\) y se aplica dominancia. La memoria suma las variables constantes y el costo lineal de `foo2`, por lo que \(S(n)\in O(n)\). La obra no propone simulación para este caso por su crecimiento deliberadamente poco habitual.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo5-ciclos-incremento-no-lineal/">← 4.4.4.5 Ciclos con incremento no lineal</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo7-ciclo-sin-dependencia/">4.4.4.7 Ciclo sin dependencia de la entrada →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
