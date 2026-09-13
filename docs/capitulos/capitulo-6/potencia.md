<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 3 · Potencia de un número entero positivo

<span class="chapter-kicker">Capítulo 6</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

#### Código

<!-- book-code:start -->

##### Potencia por división del exponente

Implementación basada en el libro, página 243 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemplo0f3471be4e4e {
        public static double potencia(int a, int n) {
            if (a == 0 && n < 0)
                throw new ArithmeticException("Cero no admite exponente negativo");
            long absExponente = Math.abs((long) n);
            double base = n < 0 ? 1.0 / a : a;
            return potenciaAbsoluta(base, absExponente);
        }

        private static double potenciaAbsoluta(double a, long n) {
            if (n == 0)
                return 1;
            double mitad = potenciaAbsoluta(a, n / 2);
            mitad = mitad * mitad;
            return n % 2 == 0 ? mitad : mitad * a;
        }

        public static void main(String[] args) {
            int a = Entradas.entero(args, 0, 2);
            int n = Entradas.entero(args, 1, -3);

            System.out.println("Resultado: " + Ejemplo0f3471be4e4e.potencia(a, n));
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función potencia(a, n)
        si a == 0 y n < 0 entonces
            error ZeroDivisionError("Cero no admite exponente negativo")
        absExponente ← abs(n)
        base ← 1.0 / a if n < 0 else float(a)
        retornar potenciaAbsoluta(base, absExponente)


    función potenciaAbsoluta(a, n)
        si n == 0 entonces
            retornar 1.0
        mitad ← potenciaAbsoluta(a, n div 2)
        mitad ← mitad * mitad
        retornar mitad if n % 2 == 0 else mitad * a
    ```

=== "Python"

    ```python
    def potencia(a, n):
        if a == 0 and n < 0:
            raise ZeroDivisionError("Cero no admite exponente negativo")
        absExponente = abs(n)
        base = 1.0 / a if n < 0 else float(a)
        return potenciaAbsoluta(base, absExponente)


    def potenciaAbsoluta(a, n):
        if n == 0:
            return 1.0
        mitad = potenciaAbsoluta(a, n // 2)
        mitad = mitad * mitad
        return mitad if n % 2 == 0 else mitad * a
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    double potenciaAbsoluta(double a, int64_t n);

    double potencia(int a, int n) {
        if (a == 0 && n < 0) {
            abort();
        }
        int64_t absExponente = llabs((long long) n);
        double base = n < 0 ? 1.0 / a : (double) a;
        return potenciaAbsoluta(base, absExponente);
    }

    double potenciaAbsoluta(double a, int64_t n) {
        if (n == 0) {
            return 1;
        }
        double mitad = potenciaAbsoluta(a, n / 2);
        mitad = mitad * mitad;
        return n % 2 == 0 ? mitad : mitad * a;
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `a` | Base entera. |
| `n` | Exponente, que puede ser negativo. |
| `absExponente` | Valor absoluto del exponente. |
| `mitad` | Resultado de una llamada recursiva de la auxiliar potenciaAbsoluta. |

**Precondiciones:** Si n es negativo, a debe ser distinto de cero.

**Resultado:** Devuelve a elevado a n mediante una base recíproca cuando n es negativo.

**Explicación:** El valor absoluto del exponente se calcula en long para admitir también Integer.MIN_VALUE. El resultado se representa en double y está sujeto a su rango y redondeo.

??? example "Ejemplo paso a paso"
    Entrada: `a = 2, n = -3`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `base = 0.5, absExponente = 3` | Convierte el exponente negativo en una potencia de la base recíproca. |
    | `potenciaAbsoluta(0.5, 1) = 0.5` | Resuelve la mitad. |
    | \(0.5 \times 0.5 \times 0.5\) | Devuelve 0.125. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga el entorno del lenguaje elegido en el navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-0f3471be4e4e">Lenguaje del ejemplo</label><select id="language-0f3471be4e4e" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemplo0f3471be4e4e" aria-label="Código Java · Potencia por división del exponente"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemplo0f3471be4e4e</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">double</span><span class="w"> </span><span class="nf">potencia</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">a</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="mi">0</span><span class="w"> </span><span class="o">&amp;&amp;</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="mi">0</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">throw</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="n">ArithmeticException</span><span class="p">(</span><span class="s">"Cero no admite exponente negativo"</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">long</span><span class="w"> </span><span class="n">absExponente</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Math</span><span class="p">.</span><span class="na">abs</span><span class="p">((</span><span class="kt">long</span><span class="p">)</span><span class="w"> </span><span class="n">n</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">double</span><span class="w"> </span><span class="n">base</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="mi">0</span><span class="w"> </span><span class="o">?</span><span class="w"> </span><span class="mf">1.0</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="p">:</span><span class="w"> </span><span class="n">a</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">return</span><span class="w"> </span><span class="n">potenciaAbsoluta</span><span class="p">(</span><span class="n">base</span><span class="p">,</span><span class="w"> </span><span class="n">absExponente</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">private</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">double</span><span class="w"> </span><span class="nf">potenciaAbsoluta</span><span class="p">(</span><span class="kt">double</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="kt">long</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">n</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="mi">0</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="mi">1</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">double</span><span class="w"> </span><span class="n">mitad</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">potenciaAbsoluta</span><span class="p">(</span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="mi">2</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">mitad</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">mitad</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="n">mitad</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">return</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">%</span><span class="w"> </span><span class="mi">2</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="mi">0</span><span class="w"> </span><span class="o">?</span><span class="w"> </span><span class="n">mitad</span><span class="w"> </span><span class="p">:</span><span class="w"> </span><span class="n">mitad</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="n">a</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: a" spellcheck="false" data-editable data-java-input="a"><span class="mi">2</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: n" spellcheck="false" data-editable data-java-input="n"><span class="o">-</span><span class="mi">3</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Resultado: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">Ejemplo0f3471be4e4e</span><span class="p">.</span><span class="na">potencia</span><span class="p">(</span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">n</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-0f3471be4e4e" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Potencia por división del exponente"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">potencia</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">a</span> <span class="o">==</span> <span class="mi">0</span> <span class="ow">and</span> <span class="n">n</span> <span class="o">&lt;</span> <span class="mi">0</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">raise</span> <span class="ne">ZeroDivisionError</span><span class="p">(</span><span class="s2">"Cero no admite exponente negativo"</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="n">absExponente</span> <span class="o">=</span> <span class="nb">abs</span><span class="p">(</span><span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="n">base</span> <span class="o">=</span> <span class="mf">1.0</span> <span class="o">/</span> <span class="n">a</span> <span class="k">if</span> <span class="n">n</span> <span class="o">&lt;</span> <span class="mi">0</span> <span class="k">else</span> <span class="nb">float</span><span class="p">(</span><span class="n">a</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="n">potenciaAbsoluta</span><span class="p">(</span><span class="n">base</span><span class="p">,</span> <span class="n">absExponente</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">potenciaAbsoluta</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">n</span> <span class="o">==</span> <span class="mi">0</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span> <span class="mf">1.0</span></span><span class="python-code-line" data-code-line>    <span class="n">mitad</span> <span class="o">=</span> <span class="n">potenciaAbsoluta</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">n</span> <span class="o">//</span> <span class="mi">2</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="n">mitad</span> <span class="o">=</span> <span class="n">mitad</span> <span class="o">*</span> <span class="n">mitad</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="n">mitad</span> <span class="k">if</span> <span class="n">n</span> <span class="o">%</span> <span class="mi">2</span> <span class="o">==</span> <span class="mi">0</span> <span class="k">else</span> <span class="n">mitad</span> <span class="o">*</span> <span class="n">a</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 17" spellcheck="false" data-editable><span class="n">a</span> <span class="o">=</span> <span class="mi">2</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 18" spellcheck="false" data-editable><span class="n">n</span> <span class="o">=</span> <span class="o">-</span><span class="mi">3</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">resultado</span> <span class="o">=</span> <span class="n">potencia</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Resultado:"</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

##### Laboratorio y medición

La animación permite observar la estructura recursiva. El panel experimental ejecuta funciones Python: el tiempo y la memoria de ese panel corresponden a esas funciones y no a una ejecución del listado Java. La memoria se obtiene con tracemalloc; no mide directamente la pila de una JVM.

El experimento cuenta llamadas al dividir n entre dos; no evalúa la base ni calcula el resultado numérico de la potencia.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/runtime/recursive_examples_analysis.py).

<!-- book-code:end -->

#### Análisis

El resultado recursivo se calcula una sola vez y se reutiliza. Para analizar exponentes positivos y negativos se define \(e=|n|\), calculando el valor absoluto en long para admitir también Integer.MIN_VALUE. El subproblema divide \(e\) entre dos:

\[
T(e)=T(\lfloor e/2\rfloor)+\Theta(1)\in\Theta(\log_2(2+e)).
\]

La profundidad de llamadas sigue la misma cantidad de divisiones, de modo que \(S(e)\in\Theta(\log_2(2+e))\). Llamar dos veces a `potencia(a, absExponente / 2)` cambiaría radicalmente el árbol y desperdiciaría el resultado compartido.

#### Simulación

La animación muestra la reducción por mitades del exponente. El panel experimental amplía la comparación a factorial, Fibonacci, Merge Sort y búsqueda en árbol binario, mostrando tiempo, memoria y función teórica ajustada.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-6/ejemplos/arbol_recursion_potencia.png" alt="Árbol de llamadas de ejemplo 3 · potencia de un número entero positivo"><figcaption>Árbol de llamadas de ejemplo 3 · potencia de un número entero positivo.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/comparacion_teorema_maestro_potencia.png" alt="Comparación de crecimiento para ejemplo 3 · potencia de un número entero positivo"><figcaption>Comparación de crecimiento para ejemplo 3 · potencia de un número entero positivo.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../fibonacci/">← Ejemplo 2 · Fibonacci recursivo ingenuo</a><a class="section-step__index" href="../">Capítulo 6</a><a class="section-step__next" href="../merge-sort/">Ejemplo 4 · Ordenamiento por mezcla →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>
