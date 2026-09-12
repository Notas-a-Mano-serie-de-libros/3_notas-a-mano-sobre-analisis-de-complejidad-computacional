<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.8 Ciclo con límite fijo y función de costo lineal

<span class="chapter-kicker">Capítulo 4</span>

El número de iteraciones es constante, pero la operación ejecutada dentro del ciclo depende de la entrada.

## Código analizado

<!-- book-code:start -->

#### Ciclo fijo con auxiliar

Implementación basada en el libro, página 166 (Java).

=== "Java"

    ```java
    public static void cicloFijo(int n) {
        for (int i = 0; i < 1000; i++) {
            foo(n);
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función cicloFijo(n)
        para i en rango(1000)
            foo(n)
    ```

=== "Python"

    ```python
    def cicloFijo(n):
        for i in range(1000):
            foo(n)
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    void foo(int n);

    void cicloFijo(int n) {
        for (int i = 0; i < 1000; i++) {
            foo(n);
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Entrada que se pasa a foo. |
| `i` | Contador de las 1000 repeticiones. |
| `foo` | Auxiliar de costo dependiente de n. |

**Precondiciones:** foo(n) definida y terminante.

**Resultado:** Invoca foo(n) exactamente 1000 veces.

??? example "Ejemplo paso a paso"
    Entrada: `n = 8`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `i = 0` | Primera llamada foo(8). |
    | `i = 999` | Última llamada foo(8). |
    | `i = 1000` | Termina; el costo depende de lo que haga foo. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-9c08a2cbe90d">Código Python · Ciclo fijo con auxiliar</label><div class="python-code-editor"><div class="highlight" aria-hidden="true"><pre><code><span class="k">def</span><span class="w"> </span><span class="nf">cicloFijo</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1000</span><span class="p">):</span>
        <span class="n">foo</span><span class="p">(</span><span class="n">n</span><span class="p">)</span>

<span class="c1"># Entradas editables del ejemplo.</span>
<span class="n">n</span> <span class="o">=</span> <span class="mi">8</span>

<span class="c1"># Completa estas auxiliares según el problema que estés analizando.</span>
<span class="k">def</span><span class="w"> </span><span class="nf">foo1</span><span class="p">():</span>
    <span class="k">raise</span> <span class="ne">NotImplementedError</span><span class="p">(</span><span class="s2">"Completa foo1 en el editor"</span><span class="p">)</span>


<span class="k">def</span><span class="w"> </span><span class="nf">foo2</span><span class="p">():</span>
    <span class="k">raise</span> <span class="ne">NotImplementedError</span><span class="p">(</span><span class="s2">"Completa foo2 en el editor"</span><span class="p">)</span>


<span class="k">def</span><span class="w"> </span><span class="nf">foo</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">raise</span> <span class="ne">NotImplementedError</span><span class="p">(</span><span class="s2">"Completa foo en el editor"</span><span class="p">)</span>

<span class="n">cicloFijo</span><span class="p">(</span><span class="n">n</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">"Ejemplo finalizado"</span><span class="p">)</span>
</code></pre></div><textarea id="runner-9c08a2cbe90d" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" rows="14">def cicloFijo(n):
    for i in range(1000):
        foo(n)

# Entradas editables del ejemplo.
n = 8

# Completa estas auxiliares según el problema que estés analizando.
def foo1():
    raise NotImplementedError(&quot;Completa foo1 en el editor&quot;)


def foo2():
    raise NotImplementedError(&quot;Completa foo2 en el editor&quot;)


def foo(n):
    raise NotImplementedError(&quot;Completa foo en el editor&quot;)

cicloFijo(n)
print(&quot;Ejemplo finalizado&quot;)
</textarea></div></details><div class="example-runner-actions"><button type="button" data-run><span class="button-icon" aria-hidden="true">▶</span><span>Ejecutar</span></button><button type="button" data-stop disabled><span class="button-icon" aria-hidden="true">■</span><span>Detener</span></button><button type="button" data-reset><span class="button-icon" aria-hidden="true">↻</span><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

Los experimentos ejecutan adaptaciones Python. El tiempo excluye la preparación y se promedia por ejecución. La memoria representa el incremento de pico observado por tracemalloc durante la operación, sin incluir la entrada preparada; no es el tamaño de la memoria de una máquina Java.

No hay un laboratorio enlazado para este fragmento. El costo de foo debe declararse antes de simplificar.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/runtime/experimental_analysis.py).

<!-- book-code:end -->

## Análisis esperado

Si \(T_{foo}(n)=n\), entonces \(T(n)=1000 \cdot n\in O(n)\). La constante del ciclo se absorbe, pero la dependencia de `foo` no. Si \(S_{foo}(n)=n\), el espacio también queda en \(O(n)\).

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo7-ciclo-sin-dependencia/">← 4.4.4.7 Ciclo sin dependencia de la entrada</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo9-complejidad-oculta/">4.4.4.9 Complejidad oculta →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
