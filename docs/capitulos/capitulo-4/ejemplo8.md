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
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemplo9c08a2cbe90d {
        public static void cicloFijo(int n) {
            for (int i = 0; i < 1000; i++) {
                foo(n);
            }
        }

        public static void main(String[] args) {
            int n = Entradas.entero(args, 0, 8);

            Ejemplo9c08a2cbe90d.cicloFijo(n);
            System.out.println("Ejemplo finalizado");
        }

        private static void foo1() { throw new UnsupportedOperationException("El libro no define foo1; depende del problema analizado."); }
        private static void foo2() { throw new UnsupportedOperationException("El libro no define foo2; depende del problema analizado."); }
        private static void foo(int n) { throw new UnsupportedOperationException("El libro no define foo; depende del problema analizado."); }
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

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga el entorno del lenguaje elegido en el navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-9c08a2cbe90d">Lenguaje del ejemplo</label><select id="language-9c08a2cbe90d" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemplo9c08a2cbe90d" aria-label="Código Java · Ciclo fijo con auxiliar"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemplo9c08a2cbe90d</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">cicloFijo</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">for</span><span class="w"> </span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">i</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="mi">0</span><span class="p">;</span><span class="w"> </span><span class="n">i</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="mi">1000</span><span class="p">;</span><span class="w"> </span><span class="n">i</span><span class="o">++</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="n">foo</span><span class="p">(</span><span class="n">n</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: n" spellcheck="false" data-editable data-java-input="n"><span class="mi">8</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemplo9c08a2cbe90d</span><span class="p">.</span><span class="na">cicloFijo</span><span class="p">(</span><span class="n">n</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Ejemplo finalizado"</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">foo1</span><span class="p">()</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="k">throw</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="n">UnsupportedOperationException</span><span class="p">(</span><span class="s">"El libro no define foo1; depende del problema analizado."</span><span class="p">);</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">foo2</span><span class="p">()</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="k">throw</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="n">UnsupportedOperationException</span><span class="p">(</span><span class="s">"El libro no define foo2; depende del problema analizado."</span><span class="p">);</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">foo</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="k">throw</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="n">UnsupportedOperationException</span><span class="p">(</span><span class="s">"El libro no define foo; depende del problema analizado."</span><span class="p">);</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-9c08a2cbe90d" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Ciclo fijo con auxiliar"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">cicloFijo</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1000</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="n">foo</span><span class="p">(</span><span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 6" spellcheck="false" data-editable><span class="n">n</span> <span class="o">=</span> <span class="mi">8</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Estas auxiliares dependen del problema y no están definidas en el libro.</span></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">foo1</span><span class="p">():</span></span><span class="python-code-line" data-code-line>    <span class="k">raise</span> <span class="ne">NotImplementedError</span><span class="p">(</span><span class="s2">"El libro no define foo1; depende del problema analizado."</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">foo2</span><span class="p">():</span></span><span class="python-code-line" data-code-line>    <span class="k">raise</span> <span class="ne">NotImplementedError</span><span class="p">(</span><span class="s2">"El libro no define foo2; depende del problema analizado."</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">foo</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">raise</span> <span class="ne">NotImplementedError</span><span class="p">(</span><span class="s2">"El libro no define foo; depende del problema analizado."</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">cicloFijo</span><span class="p">(</span><span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Ejemplo finalizado"</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

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
