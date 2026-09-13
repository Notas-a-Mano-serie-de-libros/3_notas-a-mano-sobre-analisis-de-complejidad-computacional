<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.3 Complejidad lineal

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/3_complejidad_lineal.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: búsqueda secuencial en una lista

El ejemplo recorre la lista de izquierda a derecha hasta encontrar el objetivo o agotar la entrada. En el peor caso, el elemento no aparece y la función revisa todos los valores.

Cada elemento se evalúa una vez. Por eso el tiempo de ejecución observado tiende a crecer junto con la cantidad de datos.


---

### Código del libro asociado

<!-- book-code:start -->

#### Búsqueda secuencial iterativa

Implementación basada en el libro, página 262 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemplodfd9f906a528 {
        public boolean buscar(int[] arr, int x) {
            for (int i = 0; i < arr.length; i++) {
                if (arr[i] == x)
                    return true;
            }
            return false;
        }

        public static void main(String[] args) {
            int[] arr = Entradas.arreglo(args, 0, new int[] {4, 8, 12});
            int x = Entradas.entero(args, 1, 8);

            System.out.println("Resultado: " + new Ejemplodfd9f906a528().buscar(arr, x));
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función buscar(arr, x)
        para i en rango(longitud(arr))
            si arr[i] == x entonces
                retornar verdadero
        retornar falso
    ```

=== "Python"

    ```python
    def buscar(arr, x):
        for i in range(len(arr)):
            if arr[i] == x:
                return True
        return False
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    bool buscar(int arr[], int n, int x) {
        for (int i = 0; i < n; i++) {
            if (arr[i] == x) {
                return true;
            }
        }
        return false;
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, `n` indica la longitud del arreglo y se recibe como parámetro.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo de enteros. |
| `x` | Valor buscado. |
| `i` | Posición examinada. |

**Precondiciones:** arr no nulo; no requiere orden previo.

**Resultado:** Devuelve true si existe x y false si no existe.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>El navegador facilita la ejecución de código Java y Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Java ni Python; el código se ejecuta en tu navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-dfd9f906a528">Lenguaje del ejemplo</label><select id="language-dfd9f906a528" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemplodfd9f906a528" aria-label="Código Java · Búsqueda secuencial iterativa"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemplodfd9f906a528</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">buscar</span><span class="p">(</span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">x</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">for</span><span class="w"> </span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">i</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="mi">0</span><span class="p">;</span><span class="w"> </span><span class="n">i</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">arr</span><span class="p">.</span><span class="na">length</span><span class="p">;</span><span class="w"> </span><span class="n">i</span><span class="o">++</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">arr</span><span class="o">[</span><span class="n">i</span><span class="o">]</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="k">return</span><span class="w"> </span><span class="kc">true</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">return</span><span class="w"> </span><span class="kc">false</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">arreglo</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: arr" spellcheck="false" data-editable data-java-input="arr"><span class="p">{</span><span class="mi">4</span><span class="p">,</span><span class="w"> </span><span class="mi">8</span><span class="p">,</span><span class="w"> </span><span class="mi">12</span><span class="p">}</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">x</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: x" spellcheck="false" data-editable data-java-input="x"><span class="mi">8</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Resultado: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="n">Ejemplodfd9f906a528</span><span class="p">().</span><span class="na">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">x</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-dfd9f906a528" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Búsqueda secuencial iterativa"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">x</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">arr</span><span class="p">)):</span></span><span class="python-code-line" data-code-line>        <span class="k">if</span> <span class="n">arr</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">==</span> <span class="n">x</span><span class="p">:</span></span><span class="python-code-line" data-code-line>            <span class="k">return</span> <span class="kc">True</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 8" spellcheck="false" data-editable><span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">4</span><span class="p">,</span> <span class="mi">8</span><span class="p">,</span> <span class="mi">12</span><span class="p">]</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 9" spellcheck="false" data-editable><span class="n">x</span> <span class="o">=</span> <span class="mi">8</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">resultado</span> <span class="o">=</span> <span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Resultado:"</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

El listado Java procede de la página del libro indicada arriba. El laboratorio ejecuta una adaptación en Python; compara el patrón de crecimiento, no los tiempos de Java con los de Python.

El tiempo se promedia por ejecución; la preparación de las entradas se realiza antes de cronometrar. Las gráficas teóricas y las mediciones experimentales se identifican por separado.

El experimento busca n en [0, …, n−1], con resultado ausente y recorrido completo. La función del notebook devuelve un índice o −1; el Java devuelve boolean.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/runtime/complexity_animations.py).

<!-- book-code:end -->

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad lineal describe algoritmos cuyo costo crece de forma proporcional al tamaño de la entrada. Si la entrada tiene más elementos, el algoritmo puede necesitar más pasos en la misma proporción.

Este comportamiento aparece cuando el procedimiento debe inspeccionar cada elemento o avanzar secuencialmente hasta encontrar una condición. La forma del trabajo no cambia, pero se repite una vez por cada dato disponible.

Para una entrada de tamaño \(n\), una función de costo lineal puede expresarse como:

\[
T(n) = cn
\]

donde \(c\) representa el costo constante de procesar un elemento y \(n\) representa la cantidad de elementos de la entrada.

La expresión indica que el costo aumenta al mismo ritmo que la entrada. Si se duplican los elementos, el número esperado de operaciones también se duplica aproximadamente.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_lineal.png" alt="Representación gráfica de 2.1.2.3 complejidad lineal"><figcaption>Representación gráfica de 2.1.2.3 complejidad lineal.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../2-complejidad-logaritmica/">← 2.1.2.2 Complejidad logarítmica</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../4-complejidad-log-lineal/">2.1.2.4 Complejidad log-lineal →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
