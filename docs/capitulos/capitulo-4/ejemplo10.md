<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.10 Algoritmo costoso por diseño

<span class="chapter-kicker">Capítulo 4</span>

Este ejemplo estudia cómo el orden de evaluación de condiciones modifica los casos observados cuando las funciones tienen costos distintos.

## Código analizado

<!-- book-code:start -->

#### Evaluación de condiciones y ruta alternativa: orden original

Implementación basada en el libro, página 170 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemploe6aa5726127a {
        public static void evaluar(int n, boolean var) {
            if (g(n)) {
                // Se cumple g(n)
            } else if (h(n)) {
                // Se cumple h(n)
            } else {
                r(n);
            }
        }

        public static void main(String[] args) {
            int n = Entradas.entero(args, 0, 3);
            boolean var = Entradas.logico(args, 1, false);
            boolean gValor = Entradas.logico(args, 2, false);
            boolean hValor = Entradas.logico(args, 3, true);

            Ejemploe6aa5726127a.gValor = gValor;
            Ejemploe6aa5726127a.hValor = hValor;
            Ejemploe6aa5726127a.evaluar(n, var);
            System.out.println("Ejemplo finalizado");
        }

        private static boolean gValor, hValor;
        private static boolean g(int n) { return gValor; }
        private static boolean h(int n) { return hValor; }
        private static void r(int n) { System.out.println("Se ejecuta la alternativa r(n)"); }
        private static void s(int n) { System.out.println("Se ejecuta la alternativa s(n)"); }
    }
    ```

=== "Pseudocódigo"

    ```text
    si g(n) entonces
        sin operaciones  # Se cumple g(n)
    si no, si h(n) entonces
        sin operaciones  # Se cumple h(n)
    si no
        r(n)
    ```

=== "Python"

    ```python
    if g(n):
        pass  # Se cumple g(n)
    elif h(n):
        pass  # Se cumple h(n)
    else:
        r(n)
    ```

=== "C"

    ```c
    if (g(n)) {
        // Se cumple g(n)
    } else if (h(n)) {
        // Se cumple h(n)
    } else {
        r(n);
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Tamaño de la entrada. |
| `g, h` | Predicados con costos diferentes. |
| `r, s` | Operaciones de la ruta alternativa. |
| `var` | Resultado booleano disponible en la variante de la página 173. |

**Precondiciones:** Predicados y auxiliares definidos; considerar sus costos y posibles efectos laterales.

**Resultado:** Ejecuta la primera rama cuya condición se cumple. Es un fragmento de control, no un método completo.

??? example "Ejemplo paso a paso"
    Entrada: `h(n) = true, g(n) = false`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `g(n) = false` | No toma la primera rama. |
    | `h(n) = true` | Selecciona la segunda rama. |
    | `r(n)` | No se ejecuta. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga el entorno del lenguaje elegido en el navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-e6aa5726127a">Lenguaje del ejemplo</label><select id="language-e6aa5726127a" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemploe6aa5726127a" aria-label="Código Java · Evaluación de condiciones y ruta alternativa: orden original"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemploe6aa5726127a</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">evaluar</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">,</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="n">var</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">))</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="c1">// Se cumple g(n)</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span><span class="w"> </span><span class="k">else</span><span class="w"> </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">))</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="c1">// Se cumple h(n)</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span><span class="w"> </span><span class="k">else</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="n">r</span><span class="p">(</span><span class="n">n</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: n" spellcheck="false" data-editable data-java-input="n"><span class="mi">3</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="kd">var</span><span class="w"> </span><span class="err">= </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: var" spellcheck="false" data-editable data-java-input="var"><span class="kc">false</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="n">gValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: gValor" spellcheck="false" data-editable data-java-input="gValor"><span class="kc">false</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="n">hValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: hValor" spellcheck="false" data-editable data-java-input="hValor"><span class="kc">true</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemploe6aa5726127a</span><span class="p">.</span><span class="na">gValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">gValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemploe6aa5726127a</span><span class="p">.</span><span class="na">hValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemploe6aa5726127a</span><span class="p">.</span><span class="na">evaluar</span><span class="p">(</span><span class="n">n</span><span class="p">,</span><span class="w"> </span><span class="n">var</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Ejemplo finalizado"</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="n">gValor</span><span class="p">,</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="k">return</span><span class="w"> </span><span class="n">gValor</span><span class="p">;</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="k">return</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Se ejecuta la alternativa r(n)"</span><span class="p">);</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Se ejecuta la alternativa s(n)"</span><span class="p">);</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-e6aa5726127a" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Evaluación de condiciones y ruta alternativa: orden original"><pre><code><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 1" spellcheck="false" data-editable><span class="n">n</span> <span class="o">=</span> <span class="mi">3</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 2" spellcheck="false" data-editable><span class="n">var</span> <span class="o">=</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Valores de los predicados para esta prueba de escritorio.</span></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="kc">True</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa r(n)"</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa s(n)"</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">if</span> <span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">pass</span>  <span class="c1"># Se cumple g(n)</span></span><span class="python-code-line" data-code-line><span class="k">elif</span> <span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">pass</span>  <span class="c1"># Se cumple h(n)</span></span><span class="python-code-line" data-code-line><span class="k">else</span><span class="p">:</span></span><span class="python-code-line" data-code-line>    <span class="n">r</span><span class="p">(</span><span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Evaluación de condiciones completada"</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Evaluación de condiciones y ruta alternativa: condiciones reordenadas

Implementación basada en el libro, página 170 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemplo7dadf59bf6e8 {
        public static void evaluar(int n, boolean var) {
            if (h(n)) {
                // Se cumple h(n)
            } else if (g(n)) {
                // Se cumple g(n)
            } else {
                r(n);
            }
        }

        public static void main(String[] args) {
            int n = Entradas.entero(args, 0, 3);
            boolean var = Entradas.logico(args, 1, false);
            boolean gValor = Entradas.logico(args, 2, false);
            boolean hValor = Entradas.logico(args, 3, true);

            Ejemplo7dadf59bf6e8.gValor = gValor;
            Ejemplo7dadf59bf6e8.hValor = hValor;
            Ejemplo7dadf59bf6e8.evaluar(n, var);
            System.out.println("Ejemplo finalizado");
        }

        private static boolean gValor, hValor;
        private static boolean g(int n) { return gValor; }
        private static boolean h(int n) { return hValor; }
        private static void r(int n) { System.out.println("Se ejecuta la alternativa r(n)"); }
        private static void s(int n) { System.out.println("Se ejecuta la alternativa s(n)"); }
    }
    ```

=== "Pseudocódigo"

    ```text
    si h(n) entonces
        sin operaciones  # Se cumple h(n)
    si no, si g(n) entonces
        sin operaciones  # Se cumple g(n)
    si no
        r(n)
    ```

=== "Python"

    ```python
    if h(n):
        pass  # Se cumple h(n)
    elif g(n):
        pass  # Se cumple g(n)
    else:
        r(n)
    ```

=== "C"

    ```c
    if (h(n)) {
        // Se cumple h(n)
    } else if (g(n)) {
        // Se cumple g(n)
    } else {
        r(n);
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Tamaño de la entrada. |
| `g, h` | Predicados con costos diferentes. |
| `r, s` | Operaciones de la ruta alternativa. |
| `var` | Resultado booleano disponible en la variante de la página 173. |

**Precondiciones:** Predicados y auxiliares definidos; considerar sus costos y posibles efectos laterales.

**Resultado:** Ejecuta la primera rama cuya condición se cumple. Es un fragmento de control, no un método completo.

??? example "Ejemplo paso a paso"
    Entrada: `h(n) = true, g(n) = false`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `h(n) = true` | Selecciona la primera rama. |
    | `g(n), r(n)` | No se evalúan ni ejecutan en esta ruta. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga el entorno del lenguaje elegido en el navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-7dadf59bf6e8">Lenguaje del ejemplo</label><select id="language-7dadf59bf6e8" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemplo7dadf59bf6e8" aria-label="Código Java · Evaluación de condiciones y ruta alternativa: condiciones reordenadas"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemplo7dadf59bf6e8</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">evaluar</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">,</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="n">var</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">))</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="c1">// Se cumple h(n)</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span><span class="w"> </span><span class="k">else</span><span class="w"> </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">))</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="c1">// Se cumple g(n)</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span><span class="w"> </span><span class="k">else</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="n">r</span><span class="p">(</span><span class="n">n</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: n" spellcheck="false" data-editable data-java-input="n"><span class="mi">3</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="kd">var</span><span class="w"> </span><span class="err">= </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: var" spellcheck="false" data-editable data-java-input="var"><span class="kc">false</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="n">gValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: gValor" spellcheck="false" data-editable data-java-input="gValor"><span class="kc">false</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="n">hValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: hValor" spellcheck="false" data-editable data-java-input="hValor"><span class="kc">true</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemplo7dadf59bf6e8</span><span class="p">.</span><span class="na">gValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">gValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemplo7dadf59bf6e8</span><span class="p">.</span><span class="na">hValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemplo7dadf59bf6e8</span><span class="p">.</span><span class="na">evaluar</span><span class="p">(</span><span class="n">n</span><span class="p">,</span><span class="w"> </span><span class="n">var</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Ejemplo finalizado"</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="n">gValor</span><span class="p">,</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="k">return</span><span class="w"> </span><span class="n">gValor</span><span class="p">;</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="k">return</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Se ejecuta la alternativa r(n)"</span><span class="p">);</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Se ejecuta la alternativa s(n)"</span><span class="p">);</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-7dadf59bf6e8" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Evaluación de condiciones y ruta alternativa: condiciones reordenadas"><pre><code><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 1" spellcheck="false" data-editable><span class="n">n</span> <span class="o">=</span> <span class="mi">3</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 2" spellcheck="false" data-editable><span class="n">var</span> <span class="o">=</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Valores de los predicados para esta prueba de escritorio.</span></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="kc">True</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa r(n)"</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa s(n)"</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">if</span> <span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">pass</span>  <span class="c1"># Se cumple h(n)</span></span><span class="python-code-line" data-code-line><span class="k">elif</span> <span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">pass</span>  <span class="c1"># Se cumple g(n)</span></span><span class="python-code-line" data-code-line><span class="k">else</span><span class="p">:</span></span><span class="python-code-line" data-code-line>    <span class="n">r</span><span class="p">(</span><span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Evaluación de condiciones completada"</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Evaluación de condiciones y ruta alternativa

Implementación basada en el libro, página 171 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemplo14c69ffc07a3 {
        public static void evaluar(int n, boolean var) {
            if (h(n)) {
                // Se cumple h(n)
            } else if (g(n)) {
                // Se cumple g(n)
            } else {
                s(n); // O(1)
            }
        }

        public static void main(String[] args) {
            int n = Entradas.entero(args, 0, 3);
            boolean var = Entradas.logico(args, 1, false);
            boolean gValor = Entradas.logico(args, 2, false);
            boolean hValor = Entradas.logico(args, 3, true);

            Ejemplo14c69ffc07a3.gValor = gValor;
            Ejemplo14c69ffc07a3.hValor = hValor;
            Ejemplo14c69ffc07a3.evaluar(n, var);
            System.out.println("Ejemplo finalizado");
        }

        private static boolean gValor, hValor;
        private static boolean g(int n) { return gValor; }
        private static boolean h(int n) { return hValor; }
        private static void r(int n) { System.out.println("Se ejecuta la alternativa r(n)"); }
        private static void s(int n) { System.out.println("Se ejecuta la alternativa s(n)"); }
    }
    ```

=== "Pseudocódigo"

    ```text
    si h(n) entonces
        sin operaciones  # Se cumple h(n)
    si no, si g(n) entonces
        sin operaciones  # Se cumple g(n)
    si no
        s(n)
    ```

=== "Python"

    ```python
    if h(n):
        pass  # Se cumple h(n)
    elif g(n):
        pass  # Se cumple g(n)
    else:
        s(n)
    ```

=== "C"

    ```c
    if (h(n)) {
        // Se cumple h(n)
    } else if (g(n)) {
        // Se cumple g(n)
    } else {
        s(n); // O(1)
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Tamaño de la entrada. |
| `g, h` | Predicados con costos diferentes. |
| `r, s` | Operaciones de la ruta alternativa. |
| `var` | Resultado booleano disponible en la variante de la página 173. |

**Precondiciones:** Predicados y auxiliares definidos; considerar sus costos y posibles efectos laterales.

**Resultado:** Ejecuta la primera rama cuya condición se cumple. Es un fragmento de control, no un método completo.

??? example "Ejemplo paso a paso"
    Entrada: `h(n) = true, g(n) = false`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `h(n) = true` | Selecciona la primera rama. |
    | `g(n), s(n)` | No se evalúan ni ejecutan en esta ruta. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga el entorno del lenguaje elegido en el navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-14c69ffc07a3">Lenguaje del ejemplo</label><select id="language-14c69ffc07a3" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemplo14c69ffc07a3" aria-label="Código Java · Evaluación de condiciones y ruta alternativa"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemplo14c69ffc07a3</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">evaluar</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">,</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="n">var</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">))</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="c1">// Se cumple h(n)</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span><span class="w"> </span><span class="k">else</span><span class="w"> </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">))</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="c1">// Se cumple g(n)</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span><span class="w"> </span><span class="k">else</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="n">s</span><span class="p">(</span><span class="n">n</span><span class="p">);</span><span class="w"> </span><span class="c1">// O(1)</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: n" spellcheck="false" data-editable data-java-input="n"><span class="mi">3</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="kd">var</span><span class="w"> </span><span class="err">= </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: var" spellcheck="false" data-editable data-java-input="var"><span class="kc">false</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="n">gValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: gValor" spellcheck="false" data-editable data-java-input="gValor"><span class="kc">false</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="n">hValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: hValor" spellcheck="false" data-editable data-java-input="hValor"><span class="kc">true</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemplo14c69ffc07a3</span><span class="p">.</span><span class="na">gValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">gValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemplo14c69ffc07a3</span><span class="p">.</span><span class="na">hValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemplo14c69ffc07a3</span><span class="p">.</span><span class="na">evaluar</span><span class="p">(</span><span class="n">n</span><span class="p">,</span><span class="w"> </span><span class="n">var</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Ejemplo finalizado"</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="n">gValor</span><span class="p">,</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="k">return</span><span class="w"> </span><span class="n">gValor</span><span class="p">;</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="k">return</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Se ejecuta la alternativa r(n)"</span><span class="p">);</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Se ejecuta la alternativa s(n)"</span><span class="p">);</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-14c69ffc07a3" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Evaluación de condiciones y ruta alternativa"><pre><code><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 1" spellcheck="false" data-editable><span class="n">n</span> <span class="o">=</span> <span class="mi">3</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 2" spellcheck="false" data-editable><span class="n">var</span> <span class="o">=</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Valores de los predicados para esta prueba de escritorio.</span></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="kc">True</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa r(n)"</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa s(n)"</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">if</span> <span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">pass</span>  <span class="c1"># Se cumple h(n)</span></span><span class="python-code-line" data-code-line><span class="k">elif</span> <span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">pass</span>  <span class="c1"># Se cumple g(n)</span></span><span class="python-code-line" data-code-line><span class="k">else</span><span class="p">:</span></span><span class="python-code-line" data-code-line>    <span class="n">s</span><span class="p">(</span><span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Evaluación de condiciones completada"</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Evaluación de condiciones y ruta alternativa

Implementación basada en el libro, página 172 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemplo3ce31ecc35dd {
        public static void evaluar(int n, boolean var) {
            if (!h(n) && !g(n)) {
                s(n);
            } else if (h(n)) {
                // Se cumple h(n)
            } else if (g(n)) {
                // Se cumple g(n)
            }
        }

        public static void main(String[] args) {
            int n = Entradas.entero(args, 0, 3);
            boolean var = Entradas.logico(args, 1, false);
            boolean gValor = Entradas.logico(args, 2, false);
            boolean hValor = Entradas.logico(args, 3, true);

            Ejemplo3ce31ecc35dd.gValor = gValor;
            Ejemplo3ce31ecc35dd.hValor = hValor;
            Ejemplo3ce31ecc35dd.evaluar(n, var);
            System.out.println("Ejemplo finalizado");
        }

        private static boolean gValor, hValor;
        private static boolean g(int n) { return gValor; }
        private static boolean h(int n) { return hValor; }
        private static void r(int n) { System.out.println("Se ejecuta la alternativa r(n)"); }
        private static void s(int n) { System.out.println("Se ejecuta la alternativa s(n)"); }
    }
    ```

=== "Pseudocódigo"

    ```text
    si no h(n) y no g(n) entonces
        s(n)
    si no, si h(n) entonces
        sin operaciones  # Se cumple h(n)
    si no, si g(n) entonces
        sin operaciones  # Se cumple g(n)
    ```

=== "Python"

    ```python
    if not h(n) and not g(n):
        s(n)
    elif h(n):
        pass  # Se cumple h(n)
    elif g(n):
        pass  # Se cumple g(n)
    ```

=== "C"

    ```c
    if (!h(n) && !g(n)) {
        s(n);
    } else if (h(n)) {
        // Se cumple h(n)
    } else if (g(n)) {
        // Se cumple g(n)
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Tamaño de la entrada. |
| `g, h` | Predicados con costos diferentes. |
| `r, s` | Operaciones de la ruta alternativa. |
| `var` | Resultado booleano disponible en la variante de la página 173. |

**Precondiciones:** Predicados y auxiliares definidos; considerar sus costos y posibles efectos laterales.

**Resultado:** Ejecuta la primera rama cuya condición se cumple. Es un fragmento de control, no un método completo.

??? example "Ejemplo paso a paso"
    Entrada: `h(n) = true, g(n) = false`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `!h(n) = false` | La primera condición no se cumple; && evita evaluar !g(n). |
    | `h(n) = true` | Vuelve a evaluar h(n) y toma su rama. |
    | `s(n)` | No se ejecuta. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga el entorno del lenguaje elegido en el navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-3ce31ecc35dd">Lenguaje del ejemplo</label><select id="language-3ce31ecc35dd" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemplo3ce31ecc35dd" aria-label="Código Java · Evaluación de condiciones y ruta alternativa"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemplo3ce31ecc35dd</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">evaluar</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">,</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="n">var</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="o">!</span><span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="o">&amp;&amp;</span><span class="w"> </span><span class="o">!</span><span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">))</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="n">s</span><span class="p">(</span><span class="n">n</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span><span class="w"> </span><span class="k">else</span><span class="w"> </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">))</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="c1">// Se cumple h(n)</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span><span class="w"> </span><span class="k">else</span><span class="w"> </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">))</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="c1">// Se cumple g(n)</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: n" spellcheck="false" data-editable data-java-input="n"><span class="mi">3</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="kd">var</span><span class="w"> </span><span class="err">= </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: var" spellcheck="false" data-editable data-java-input="var"><span class="kc">false</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="n">gValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: gValor" spellcheck="false" data-editable data-java-input="gValor"><span class="kc">false</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="n">hValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: hValor" spellcheck="false" data-editable data-java-input="hValor"><span class="kc">true</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemplo3ce31ecc35dd</span><span class="p">.</span><span class="na">gValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">gValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemplo3ce31ecc35dd</span><span class="p">.</span><span class="na">hValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemplo3ce31ecc35dd</span><span class="p">.</span><span class="na">evaluar</span><span class="p">(</span><span class="n">n</span><span class="p">,</span><span class="w"> </span><span class="n">var</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Ejemplo finalizado"</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="n">gValor</span><span class="p">,</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="k">return</span><span class="w"> </span><span class="n">gValor</span><span class="p">;</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="k">return</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Se ejecuta la alternativa r(n)"</span><span class="p">);</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Se ejecuta la alternativa s(n)"</span><span class="p">);</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-3ce31ecc35dd" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Evaluación de condiciones y ruta alternativa"><pre><code><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 1" spellcheck="false" data-editable><span class="n">n</span> <span class="o">=</span> <span class="mi">3</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 2" spellcheck="false" data-editable><span class="n">var</span> <span class="o">=</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Valores de los predicados para esta prueba de escritorio.</span></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="kc">True</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa r(n)"</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa s(n)"</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">if</span> <span class="ow">not</span> <span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">)</span> <span class="ow">and</span> <span class="ow">not</span> <span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="n">s</span><span class="p">(</span><span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="k">elif</span> <span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">pass</span>  <span class="c1"># Se cumple h(n)</span></span><span class="python-code-line" data-code-line><span class="k">elif</span> <span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">pass</span>  <span class="c1"># Se cumple g(n)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Evaluación de condiciones completada"</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Evaluación de condiciones y ruta alternativa

Implementación basada en el libro, página 173 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemplod5912a571cd2 {
        public static void evaluar(int n, boolean var) {
            if (var) {
                s(n);
            } else if (h(n)) {
                // Se cumple h(n)
            } else if (g(n)) {
                // Se cumple g(n)
            }
        }

        public static void main(String[] args) {
            int n = Entradas.entero(args, 0, 3);
            boolean var = Entradas.logico(args, 1, false);
            boolean gValor = Entradas.logico(args, 2, false);
            boolean hValor = Entradas.logico(args, 3, true);

            Ejemplod5912a571cd2.gValor = gValor;
            Ejemplod5912a571cd2.hValor = hValor;
            Ejemplod5912a571cd2.evaluar(n, var);
            System.out.println("Ejemplo finalizado");
        }

        private static boolean gValor, hValor;
        private static boolean g(int n) { return gValor; }
        private static boolean h(int n) { return hValor; }
        private static void r(int n) { System.out.println("Se ejecuta la alternativa r(n)"); }
        private static void s(int n) { System.out.println("Se ejecuta la alternativa s(n)"); }
    }
    ```

=== "Pseudocódigo"

    ```text
    si var entonces
        s(n)
    si no, si h(n) entonces
        sin operaciones  # Se cumple h(n)
    si no, si g(n) entonces
        sin operaciones  # Se cumple g(n)
    ```

=== "Python"

    ```python
    if var:
        s(n)
    elif h(n):
        pass  # Se cumple h(n)
    elif g(n):
        pass  # Se cumple g(n)
    ```

=== "C"

    ```c
    if (var) {
        s(n);
    } else if (h(n)) {
        // Se cumple h(n)
    } else if (g(n)) {
        // Se cumple g(n)
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Tamaño de la entrada. |
| `g, h` | Predicados con costos diferentes. |
| `r, s` | Operaciones de la ruta alternativa. |
| `var` | Resultado booleano disponible en la variante de la página 173. |

**Precondiciones:** Predicados y auxiliares definidos; considerar sus costos y posibles efectos laterales.

**Resultado:** Ejecuta la primera rama cuya condición se cumple. Es un fragmento de control, no un método completo.

??? example "Ejemplo paso a paso"
    Entrada: `var = false, h(n) = true, g(n) = false`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `var = false` | No ejecuta s(n). |
    | `h(n) = true` | Selecciona la rama de h(n). |
    | `g(n)` | No se evalúa en esta ruta. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga el entorno del lenguaje elegido en el navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-d5912a571cd2">Lenguaje del ejemplo</label><select id="language-d5912a571cd2" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemplod5912a571cd2" aria-label="Código Java · Evaluación de condiciones y ruta alternativa"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemplod5912a571cd2</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">evaluar</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">,</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="n">var</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">var</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="n">s</span><span class="p">(</span><span class="n">n</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span><span class="w"> </span><span class="k">else</span><span class="w"> </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">))</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="c1">// Se cumple h(n)</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span><span class="w"> </span><span class="k">else</span><span class="w"> </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">))</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="c1">// Se cumple g(n)</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: n" spellcheck="false" data-editable data-java-input="n"><span class="mi">3</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="kd">var</span><span class="w"> </span><span class="err">= </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: var" spellcheck="false" data-editable data-java-input="var"><span class="kc">false</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="n">gValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: gValor" spellcheck="false" data-editable data-java-input="gValor"><span class="kc">false</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">boolean</span><span class="w"> </span><span class="n">hValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">logico</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: hValor" spellcheck="false" data-editable data-java-input="hValor"><span class="kc">true</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemplod5912a571cd2</span><span class="p">.</span><span class="na">gValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">gValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemplod5912a571cd2</span><span class="p">.</span><span class="na">hValor</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemplod5912a571cd2</span><span class="p">.</span><span class="na">evaluar</span><span class="p">(</span><span class="n">n</span><span class="p">,</span><span class="w"> </span><span class="n">var</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Ejemplo finalizado"</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="n">gValor</span><span class="p">,</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="k">return</span><span class="w"> </span><span class="n">gValor</span><span class="p">;</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="k">return</span><span class="w"> </span><span class="n">hValor</span><span class="p">;</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Se ejecuta la alternativa r(n)"</span><span class="p">);</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span><span class="w"> </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Se ejecuta la alternativa s(n)"</span><span class="p">);</span><span class="w"> </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-d5912a571cd2" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Evaluación de condiciones y ruta alternativa"><pre><code><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 1" spellcheck="false" data-editable><span class="n">n</span> <span class="o">=</span> <span class="mi">3</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 2" spellcheck="false" data-editable><span class="n">var</span> <span class="o">=</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Valores de los predicados para esta prueba de escritorio.</span></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="kc">True</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa r(n)"</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa s(n)"</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">if</span> <span class="n">var</span><span class="p">:</span></span><span class="python-code-line" data-code-line>    <span class="n">s</span><span class="p">(</span><span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="k">elif</span> <span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">pass</span>  <span class="c1"># Se cumple h(n)</span></span><span class="python-code-line" data-code-line><span class="k">elif</span> <span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">pass</span>  <span class="c1"># Se cumple g(n)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Evaluación de condiciones completada"</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

Los experimentos ejecutan adaptaciones Python. El tiempo excluye la preparación y se promedia por ejecución. La memoria representa el incremento de pico observado por tracemalloc durante la operación, sin incluir la entrada preparada; no es el tamaño de la memoria de una máquina Java.

Estas variantes se analizan simbólicamente; no tienen simulación enlazada.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/runtime/experimental_analysis.py).

<!-- book-code:end -->

## Análisis esperado

Si \(h(n)\in\Theta(\log_2(n))\) es el caso más frecuente, evaluarla antes que \(g(n)\in\Theta(n)\) reduce el caso promedio a \(\Theta(\log_2(n))\). El peor caso continúa incluyendo \(r(n)\in\Theta(2^n)\); reordenar condiciones mejora la ruta habitual, pero no elimina el cuello de botella exponencial.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo9-complejidad-oculta/">← 4.4.4.9 Complejidad oculta</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejercicios-propuestos/">4.6 Ejercicios propuestos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
