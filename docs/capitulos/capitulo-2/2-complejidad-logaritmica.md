<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.2 Complejidad logarítmica

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/2_complejidad_logaritmica.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: búsqueda binaria en una lista ordenada

El ejemplo implementa una búsqueda binaria iterativa. En cada vuelta se calcula la posición media del rango activo y se compara el valor encontrado con el objetivo.

Si el valor central no es el buscado, la mitad que no puede contener la respuesta se descarta. La lista completa puede ser muy grande, pero el algoritmo solo conserva dos límites: `bajo` y `alto`. Esa reducción sucesiva explica el comportamiento logarítmico.


---

### Código del libro asociado

<!-- book-code:start -->

#### Búsqueda binaria iterativa

Implementación basada en el libro, página 268 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemploe7872d7f0991 {
        public boolean buscar(int[] arr, int a, int b, int x) {
            while (a <= b) {
                // Posición en la mitad del rango [a,b]
                int m = a + (b - a) / 2;
                if (arr[m] == x)
                    return true; // Elemento encontrado
                else if (x > arr[m])
                    a = m + 1; // Buscar en la mitad derecha
                else
                    b = m - 1; // Buscar en la mitad izquierda
            }
            return false; // Elemento no encontrado
        }

        public static void main(String[] args) {
            int[] arr = Entradas.arreglo(args, 0, new int[] {1, 3, 5, 7, 9});
            int a = Entradas.entero(args, 1, 0);
            int b = Entradas.entero(args, 2, 4);
            int x = Entradas.entero(args, 3, 7);

            System.out.println("Resultado: " + new Ejemploe7872d7f0991().buscar(arr, a, b, x));
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función buscar(arr, a, b, x)
        mientras a <= b
            m ← a + (b - a) div 2
            si arr[m] == x entonces
                retornar verdadero
            si x > arr[m] entonces
                a ← m + 1
            si no
                b ← m - 1
        retornar falso
    ```

=== "Python"

    ```python
    def buscar(arr, a, b, x):
        while a <= b:
            m = a + (b - a) // 2
            if arr[m] == x:
                return True
            if x > arr[m]:
                a = m + 1
            else:
                b = m - 1
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

    bool buscar(int arr[], int a, int b, int x) {
        while (a <= b) {
            // Posición en la mitad del rango [a,b]
            int m = a + (b - a) / 2;
            if (arr[m] == x) {
                return true; // Elemento encontrado
            }
            else if (x > arr[m]) {
                a = m + 1; // Buscar en la mitad derecha
            }
            else {
                b = m - 1; // Buscar en la mitad izquierda
            }
        }
        return false; // Elemento no encontrado
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo ordenado ascendentemente. |
| `a, b` | Límites inclusivos de búsqueda. |
| `x` | Valor buscado. |
| `m` | Índice del punto medio. |

**Precondiciones:** arr no nulo y ordenado; límites válidos para intervalo no vacío. Para el arreglo completo, `a = 0` y `b = arr.length - 1`.

**Resultado:** Devuelve true si encuentra x dentro del intervalo; false en caso contrario.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>El navegador facilita la ejecución de código Java y Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Java ni Python; el código se ejecuta en tu navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-e7872d7f0991">Lenguaje del ejemplo</label><select id="language-e7872d7f0991" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemploe7872d7f0991" aria-label="Código Java · Búsqueda binaria iterativa"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemploe7872d7f0991</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">buscar</span><span class="p">(</span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">b</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">x</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">while</span><span class="w"> </span><span class="p">(</span><span class="n">a</span><span class="w"> </span><span class="o">&lt;=</span><span class="w"> </span><span class="n">b</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="c1">// Posición en la mitad del rango [a,b]</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="kt">int</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="p">(</span><span class="n">b</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">a</span><span class="p">)</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="mi">2</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">arr</span><span class="o">[</span><span class="n">m</span><span class="o">]</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="k">return</span><span class="w"> </span><span class="kc">true</span><span class="p">;</span><span class="w"> </span><span class="c1">// Elemento encontrado</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">else</span><span class="w"> </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">x</span><span class="w"> </span><span class="o">&gt;</span><span class="w"> </span><span class="n">arr</span><span class="o">[</span><span class="n">m</span><span class="o">]</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="n">a</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="p">;</span><span class="w"> </span><span class="c1">// Buscar en la mitad derecha</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">else</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="n">b</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="mi">1</span><span class="p">;</span><span class="w"> </span><span class="c1">// Buscar en la mitad izquierda</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">return</span><span class="w"> </span><span class="kc">false</span><span class="p">;</span><span class="w"> </span><span class="c1">// Elemento no encontrado</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">arreglo</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: arr" spellcheck="false" data-editable data-java-input="arr"><span class="p">{</span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span class="mi">5</span><span class="p">,</span><span class="w"> </span><span class="mi">7</span><span class="p">,</span><span class="w"> </span><span class="mi">9</span><span class="p">}</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: a" spellcheck="false" data-editable data-java-input="a"><span class="mi">0</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">b</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: b" spellcheck="false" data-editable data-java-input="b"><span class="mi">4</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">x</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: x" spellcheck="false" data-editable data-java-input="x"><span class="mi">7</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Resultado: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="n">Ejemploe7872d7f0991</span><span class="p">().</span><span class="na">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">b</span><span class="p">,</span><span class="w"> </span><span class="n">x</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-e7872d7f0991" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Búsqueda binaria iterativa"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">x</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">while</span> <span class="n">a</span> <span class="o">&lt;=</span> <span class="n">b</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="n">m</span> <span class="o">=</span> <span class="n">a</span> <span class="o">+</span> <span class="p">(</span><span class="n">b</span> <span class="o">-</span> <span class="n">a</span><span class="p">)</span> <span class="o">//</span> <span class="mi">2</span></span><span class="python-code-line" data-code-line>        <span class="k">if</span> <span class="n">arr</span><span class="p">[</span><span class="n">m</span><span class="p">]</span> <span class="o">==</span> <span class="n">x</span><span class="p">:</span></span><span class="python-code-line" data-code-line>            <span class="k">return</span> <span class="kc">True</span></span><span class="python-code-line" data-code-line>        <span class="k">if</span> <span class="n">x</span> <span class="o">&gt;</span> <span class="n">arr</span><span class="p">[</span><span class="n">m</span><span class="p">]:</span></span><span class="python-code-line" data-code-line>            <span class="n">a</span> <span class="o">=</span> <span class="n">m</span> <span class="o">+</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>        <span class="k">else</span><span class="p">:</span></span><span class="python-code-line" data-code-line>            <span class="n">b</span> <span class="o">=</span> <span class="n">m</span> <span class="o">-</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 13" spellcheck="false" data-editable><span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">5</span><span class="p">,</span> <span class="mi">7</span><span class="p">,</span> <span class="mi">9</span><span class="p">]</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 14" spellcheck="false" data-editable><span class="n">a</span> <span class="o">=</span> <span class="mi">0</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 15" spellcheck="false" data-editable><span class="n">b</span> <span class="o">=</span> <span class="mi">4</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 16" spellcheck="false" data-editable><span class="n">x</span> <span class="o">=</span> <span class="mi">7</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">resultado</span> <span class="o">=</span> <span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Resultado:"</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

El listado Java procede de la página del libro indicada arriba. El laboratorio ejecuta una adaptación en Python; compara el patrón de crecimiento, no los tiempos de Java con los de Python.

El tiempo se promedia por ejecución; la preparación de las entradas se realiza antes de cronometrar. Las gráficas teóricas y las mediciones experimentales se identifican por separado.

El experimento busca n en el arreglo [0, …, n−1], por lo que mide una búsqueda binaria sin éxito. La función del notebook devuelve una posición o −1; el listado Java devuelve boolean.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/runtime/complexity_animations.py).

<!-- book-code:end -->

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad logarítmica describe algoritmos cuyo costo crece muy lentamente frente al tamaño de la entrada. En lugar de revisar todos los elementos, el algoritmo reduce el espacio de búsqueda en una fracción significativa en cada paso.

Este comportamiento aparece cuando cada decisión descarta una parte grande del problema. Por ejemplo, en una lista ordenada, la búsqueda binaria compara contra el elemento central y conserva únicamente la mitad donde todavía puede estar el valor buscado.

Por esa razón, aumentar mucho el tamaño de la entrada no produce un aumento proporcional en el número de pasos: duplicar n normalmente añade solo una decisión adicional.

Para una entrada de tamaño \(n\), una función de costo logarítmico puede expresarse como:

\[
T(n) = c \cdot \log_2(n)
\]

donde \(T(n)\) representa el costo de ejecución, \(c\) representa el costo constante de cada comparación o decisión, y \(\log_2(n)\) representa la cantidad aproximada de veces que la entrada puede dividirse entre dos.

La base del logaritmo no cambia la familia de crecimiento. En general, una función logarítmica puede expresarse como \(\log_\ell(n)\), donde \(\ell\) es la base del logaritmo. Si se desea expresar ese logaritmo usando otra base \(b\), se aplica el cambio de base:

\[
\log_\ell(n) = \frac{\log_b(n)}{\log_b(\ell)}
\]

El término \(\frac{1}{\log_b(\ell)}\) es una constante multiplicativa. Por eso, \(\log_2(n)\), \(\log_{10}(n)\) y \(\log_e(n)\) crecen con la misma forma general: cambian de escala vertical, pero pertenecen a la misma familia logarítmica.

La expresión muestra que el costo crece por niveles de división. Si \(n\) pasa de \(1.000\) a \(1.000.000\), el crecimiento no sigue la diferencia entre esos tamaños, sino la cantidad de divisiones necesarias para reducir el rango hasta encontrar o descartar el elemento.

Una característica especialmente importante de esta familia es que crece extremadamente lento. Incluso cuando el tamaño de entrada alcanza valores enormes, el número de pasos logarítmicos permanece manejable. Por ejemplo, si \(n=10^{100}\), entonces:

\[
\log_2(10^{100}) = 100 \cdot \log_2(10) \approx 332.19
\]

Esto significa que una entrada con cien órdenes de magnitud puede reducirse, en un modelo logarítmico base dos, a poco más de trescientas decisiones teóricas. Encontrar soluciones de orden constante suele ser una tarea bastante complicada, porque exige que el costo no dependa del tamaño de la entrada. Cuando eso no es posible, la siguiente mejor opción práctica suelen ser las soluciones logarítmicas: todavía dependen de \(n\), pero lo hacen de una manera muy lenta.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_logaritmica.png" alt="Representación gráfica de 2.1.2.2 complejidad logarítmica"><figcaption>Representación gráfica de 2.1.2.2 complejidad logarítmica.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../1-complejidad-constante/">← 2.1.2.1 Complejidad constante</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../3-complejidad-lineal/">2.1.2.3 Complejidad lineal →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
