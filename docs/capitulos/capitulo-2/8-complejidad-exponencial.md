<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.8 Complejidad exponencial

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/8_complejidad_exponencial.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: Fibonacci recursivo sin memoización

El ejemplo calcula Fibonacci mediante dos llamadas recursivas en cada paso no trivial. Muchas llamadas repiten los mismos subproblemas, lo que genera un árbol de ejecución grande.

Esta repetición explica por qué el tiempo crece de forma exponencial cuando \(n\) aumenta.


---

### Código del libro asociado

<!-- book-code:start -->

#### Fibonacci recursivo

Implementación basada en el libro, página 234 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemplo28ef7b871b47 {
        public static int fibonacci(int n) {
            if (n < 0)
                throw new IllegalArgumentException("n debe ser no negativo");
            if (n > 46)
                throw new ArithmeticException("El resultado no cabe en int");
            if (n == 0)
                return 0;
            else if (n == 1)
                return 1;
            else
                return fibonacci(n-1) + fibonacci(n-2);
        }

        public static void main(String[] args) {
            int n = Entradas.entero(args, 0, 3);

            System.out.println("Resultado: " + Ejemplo28ef7b871b47.fibonacci(n));
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función fibonacci(n)
        si n < 0 entonces
            error ValueError("n debe ser no negativo")
        si n > 46 entonces
            error OverflowError("El resultado no cabe en int de Java")
        si n == 0 entonces
            retornar 0
        si n == 1 entonces
            retornar 1
        retornar fibonacci(n - 1) + fibonacci(n - 2)
    ```

=== "Python"

    ```python
    def fibonacci(n):
        if n < 0:
            raise ValueError("n debe ser no negativo")
        if n > 46:
            raise OverflowError("El resultado no cabe en int de Java")
        if n == 0:
            return 0
        if n == 1:
            return 1
        return fibonacci(n - 1) + fibonacci(n - 2)
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    int fibonacci(int n) {
        if (n < 0) {
            abort();
        }
        if (n > 46) {
            abort();
        }
        if (n == 0) {
            return 0;
        }
        else if (n == 1) {
            return 1;
        }
        else {
            return fibonacci(n-1) + fibonacci(n-2);
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Índice de Fibonacci. |
| `fibonacci(n-1), fibonacci(n-2)` | Dos llamadas recursivas. |

**Precondiciones:** n no negativo. Si el resultado no cabe en int, se lanza ArithmeticException en lugar de devolver un valor desbordado.

**Resultado:** Devuelve F(n).

??? example "Ejemplo paso a paso"
    Entrada: `n = 3`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `fibonacci(3)` | Calcula fibonacci(2) + fibonacci(1). |
    | `fibonacci(2)` | Calcula fibonacci(1) + fibonacci(0) = 1. |
    | `Retorno` | \(1 + 1 = 2\). |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga el entorno del lenguaje elegido en el navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-28ef7b871b47">Lenguaje del ejemplo</label><select id="language-28ef7b871b47" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemplo28ef7b871b47" aria-label="Código Java · Fibonacci recursivo"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemplo28ef7b871b47</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="nf">fibonacci</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">n</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="mi">0</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">throw</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="n">IllegalArgumentException</span><span class="p">(</span><span class="s">"n debe ser no negativo"</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">n</span><span class="w"> </span><span class="o">&gt;</span><span class="w"> </span><span class="mi">46</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">throw</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="n">ArithmeticException</span><span class="p">(</span><span class="s">"El resultado no cabe en int"</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">n</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="mi">0</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="mi">0</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">else</span><span class="w"> </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">n</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="mi">1</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="mi">1</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">else</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="n">fibonacci</span><span class="p">(</span><span class="n">n</span><span class="o">-</span><span class="mi">1</span><span class="p">)</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">fibonacci</span><span class="p">(</span><span class="n">n</span><span class="o">-</span><span class="mi">2</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: n" spellcheck="false" data-editable data-java-input="n"><span class="mi">3</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Resultado: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">Ejemplo28ef7b871b47</span><span class="p">.</span><span class="na">fibonacci</span><span class="p">(</span><span class="n">n</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-28ef7b871b47" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Fibonacci recursivo"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">fibonacci</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">n</span> <span class="o">&lt;</span> <span class="mi">0</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s2">"n debe ser no negativo"</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">n</span> <span class="o">&gt;</span> <span class="mi">46</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">raise</span> <span class="ne">OverflowError</span><span class="p">(</span><span class="s2">"El resultado no cabe en int de Java"</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">n</span> <span class="o">==</span> <span class="mi">0</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span> <span class="mi">0</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">n</span> <span class="o">==</span> <span class="mi">1</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="n">fibonacci</span><span class="p">(</span><span class="n">n</span> <span class="o">-</span> <span class="mi">1</span><span class="p">)</span> <span class="o">+</span> <span class="n">fibonacci</span><span class="p">(</span><span class="n">n</span> <span class="o">-</span> <span class="mi">2</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 13" spellcheck="false" data-editable><span class="n">n</span> <span class="o">=</span> <span class="mi">3</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">resultado</span> <span class="o">=</span> <span class="n">fibonacci</span><span class="p">(</span><span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Resultado:"</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

El listado Java procede de la página del libro indicada arriba. El laboratorio ejecuta una adaptación en Python; compara el patrón de crecimiento, no los tiempos de Java con los de Python.

El tiempo se promedia por ejecución; la preparación de las entradas se realiza antes de cronometrar. Las gráficas teóricas y las mediciones experimentales se identifican por separado.

El experimento ejecuta Fibonacci recursivo sin memoización. La preparación solo fija n; las llamadas se ejecutan dentro de la medición.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/runtime/complexity_animations.py).

<!-- book-code:end -->

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad exponencial aparece cuando cada llamada o decisión abre múltiples ramas nuevas. El número de subproblemas crece de forma multiplicativa.

Este tipo de crecimiento se vuelve costoso muy rápido. Incluso incrementos pequeños en \(n\) pueden producir aumentos grandes en el tiempo de ejecución.

Para una entrada de tamaño \(n\), una función de costo exponencial puede expresarse como:

\[
T(n) = c2^n
\]

donde \(2^n\) representa un árbol de decisiones que duplica aproximadamente la cantidad de trabajo por cada incremento de \(n\).

La base puede cambiar según el algoritmo, pero la característica importante es que la variable aparece en el exponente.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_exponencial.png" alt="Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 1 de 5"><figcaption>Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 1 de 5.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-2/analisis_eficiencia/complejidad_temporal/complejidad_exponencial_1.png" alt="Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 2 de 5"><figcaption>Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 2 de 5.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-2/analisis_eficiencia/complejidad_temporal/complejidad_exponencial_2.png" alt="Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 3 de 5"><figcaption>Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 3 de 5.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-2/analisis_eficiencia/complejidad_espacial/complejidad_exponencial_1.png" alt="Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 4 de 5"><figcaption>Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 4 de 5.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-2/analisis_eficiencia/complejidad_espacial/complejidad_exponencial_2.png" alt="Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 5 de 5"><figcaption>Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 5 de 5.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../7-complejidad-polinomial-general/">← 2.1.2.7 Complejidad polinomial general</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../9-complejidad-factorial/">2.1.2.9 Complejidad factorial →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
