<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>

# 7.7 Búsqueda ternaria

<span class="chapter-kicker">Capítulo 7</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/6_busqueda_ternaria.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

La búsqueda ternaria divide el espacio de búsqueda en tres partes iguales calculando dos puntos medios. Compara el objetivo con cada punto medio para descartar un tercio del arreglo en cada iteración. Requiere que el arreglo esté ordenado.

Aunque cada iteración descarta más que la búsqueda binaria (un tercio en vez de la mitad), necesita dos comparaciones por paso, por lo que en la práctica es ligeramente menos eficiente que la búsqueda binaria. En el análisis espacial se toma como referencia la formulación recursiva, donde la pila de llamadas crece con la profundidad de las divisiones.

### Implementación

<!-- book-code:start -->

#### Búsqueda ternaria recursiva

Implementación basada en el libro, página 307 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemplo9f32c04be81a {
        public boolean buscar(int[] arr, int a, int b, int x) {
             // Agota el espacio de búsqueda
            if (a > b)
                return false;
            int m1 = a + (b - a) / 3;
            int m2 = b - (int) Math.ceil((b - a) / 3.0);
            // Verificar si el valor está en los pivotes
            if (arr[m1] == x || arr[m2] == x)
                return true;
            if (x < arr[m1])
                return buscar(arr, a, m1 - 1, x);
            else if (x > arr[m2])
                return buscar(arr, m2 + 1, b, x);
            else
                return buscar(arr, m1 + 1, m2 - 1, x);
        }

        public static void main(String[] args) {
            int[] arr = Entradas.arreglo(args, 0, new int[] {1, 3, 5, 7, 9});
            int a = Entradas.entero(args, 1, 0);
            int b = Entradas.entero(args, 2, 4);
            int x = Entradas.entero(args, 3, 7);

            System.out.println("Resultado: " + new Ejemplo9f32c04be81a().buscar(arr, a, b, x));
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función buscar(arr, a, b, x)
        si a > b entonces
            retornar falso
        m1 ← a + (b - a) div 3
        m2 ← b - (b - a + 2) div 3
        si arr[m1] == x o arr[m2] == x entonces
            retornar verdadero
        si x < arr[m1] entonces
            retornar buscar(arr, a, m1 - 1, x)
        si x > arr[m2] entonces
            retornar buscar(arr, m2 + 1, b, x)
        retornar buscar(arr, m1 + 1, m2 - 1, x)
    ```

=== "Python"

    ```python
    def buscar(arr, a, b, x):
        if a > b:
            return False
        m1 = a + (b - a) // 3
        m2 = b - (b - a + 2) // 3
        if arr[m1] == x or arr[m2] == x:
            return True
        if x < arr[m1]:
            return buscar(arr, a, m1 - 1, x)
        if x > arr[m2]:
            return buscar(arr, m2 + 1, b, x)
        return buscar(arr, m1 + 1, m2 - 1, x)
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
         // Agota el espacio de búsqueda
        if (a > b) {
            return false;
        }
        int m1 = a + (b - a) / 3;
        int m2 = b - (int) ceil((b - a) / 3.0);
        // Verificar si el valor está en los pivotes
        if (arr[m1] == x || arr[m2] == x) {
            return true;
        }
        if (x < arr[m1]) {
            return buscar(arr, a, m1 - 1, x);
        }
        else if (x > arr[m2]) {
            return buscar(arr, m2 + 1, b, x);
        }
        else {
            return buscar(arr, m1 + 1, m2 - 1, x);
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo ordenado ascendentemente. |
| `a, b` | Límites inclusivos. |
| `x` | Valor buscado. |
| `m1, m2` | Dos pivotes del intervalo. |

**Precondiciones:** arr no nulo y ordenado; límites válidos para intervalo no vacío.

**Resultado:** Devuelve true si encuentra x; false al agotar el intervalo.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>El navegador facilita la ejecución de código Java y Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Java ni Python; el código se ejecuta en tu navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-9f32c04be81a">Lenguaje del ejemplo</label><select id="language-9f32c04be81a" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemplo9f32c04be81a" aria-label="Código Java · Búsqueda ternaria recursiva"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemplo9f32c04be81a</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">buscar</span><span class="p">(</span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">b</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">x</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">         </span><span class="c1">// Agota el espacio de búsqueda</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">a</span><span class="w"> </span><span class="o">&gt;</span><span class="w"> </span><span class="n">b</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="kc">false</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">m1</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="p">(</span><span class="n">b</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">a</span><span class="p">)</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="mi">3</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">m2</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">b</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="p">(</span><span class="kt">int</span><span class="p">)</span><span class="w"> </span><span class="n">Math</span><span class="p">.</span><span class="na">ceil</span><span class="p">((</span><span class="n">b</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">a</span><span class="p">)</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="mf">3.0</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="c1">// Verificar si el valor está en los pivotes</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">arr</span><span class="o">[</span><span class="n">m1</span><span class="o">]</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="n">x</span><span class="w"> </span><span class="o">||</span><span class="w"> </span><span class="n">arr</span><span class="o">[</span><span class="n">m2</span><span class="o">]</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="kc">true</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">x</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">arr</span><span class="o">[</span><span class="n">m1</span><span class="o">]</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">m1</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="n">x</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">else</span><span class="w"> </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">x</span><span class="w"> </span><span class="o">&gt;</span><span class="w"> </span><span class="n">arr</span><span class="o">[</span><span class="n">m2</span><span class="o">]</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">m2</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="n">b</span><span class="p">,</span><span class="w"> </span><span class="n">x</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">else</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">m1</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="n">m2</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="n">x</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">arreglo</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: arr" spellcheck="false" data-editable data-java-input="arr"><span class="p">{</span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span class="mi">5</span><span class="p">,</span><span class="w"> </span><span class="mi">7</span><span class="p">,</span><span class="w"> </span><span class="mi">9</span><span class="p">}</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: a" spellcheck="false" data-editable data-java-input="a"><span class="mi">0</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">b</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: b" spellcheck="false" data-editable data-java-input="b"><span class="mi">4</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">x</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: x" spellcheck="false" data-editable data-java-input="x"><span class="mi">7</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Resultado: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="n">Ejemplo9f32c04be81a</span><span class="p">().</span><span class="na">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">b</span><span class="p">,</span><span class="w"> </span><span class="n">x</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-9f32c04be81a" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Búsqueda ternaria recursiva"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">x</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">a</span> <span class="o">&gt;</span> <span class="n">b</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line>    <span class="n">m1</span> <span class="o">=</span> <span class="n">a</span> <span class="o">+</span> <span class="p">(</span><span class="n">b</span> <span class="o">-</span> <span class="n">a</span><span class="p">)</span> <span class="o">//</span> <span class="mi">3</span></span><span class="python-code-line" data-code-line>    <span class="n">m2</span> <span class="o">=</span> <span class="n">b</span> <span class="o">-</span> <span class="p">(</span><span class="n">b</span> <span class="o">-</span> <span class="n">a</span> <span class="o">+</span> <span class="mi">2</span><span class="p">)</span> <span class="o">//</span> <span class="mi">3</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">arr</span><span class="p">[</span><span class="n">m1</span><span class="p">]</span> <span class="o">==</span> <span class="n">x</span> <span class="ow">or</span> <span class="n">arr</span><span class="p">[</span><span class="n">m2</span><span class="p">]</span> <span class="o">==</span> <span class="n">x</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span> <span class="kc">True</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">x</span> <span class="o">&lt;</span> <span class="n">arr</span><span class="p">[</span><span class="n">m1</span><span class="p">]:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span> <span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">m1</span> <span class="o">-</span> <span class="mi">1</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">x</span> <span class="o">&gt;</span> <span class="n">arr</span><span class="p">[</span><span class="n">m2</span><span class="p">]:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span> <span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">m2</span> <span class="o">+</span> <span class="mi">1</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">m1</span> <span class="o">+</span> <span class="mi">1</span><span class="p">,</span> <span class="n">m2</span> <span class="o">-</span> <span class="mi">1</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 15" spellcheck="false" data-editable><span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">5</span><span class="p">,</span> <span class="mi">7</span><span class="p">,</span> <span class="mi">9</span><span class="p">]</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 16" spellcheck="false" data-editable><span class="n">a</span> <span class="o">=</span> <span class="mi">0</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 17" spellcheck="false" data-editable><span class="n">b</span> <span class="o">=</span> <span class="mi">4</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 18" spellcheck="false" data-editable><span class="n">x</span> <span class="o">=</span> <span class="mi">7</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">resultado</span> <span class="o">=</span> <span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Resultado:"</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Búsqueda ternaria iterativa

Implementación basada en el libro, página 312 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemploa9fc79021755 {
        public boolean buscar(int[] arr, int a, int b, int x) {
            while (a <= b) {
                int m1 = a + (b - a) / 3;
                int m2 = b - (int) Math.ceil((b - a) / 3.0);
                if (arr[m1] == x || arr[m2] == x)
                    return true;
                if (x < arr[m1])
                    b = m1 - 1; // Buscar en el primer tercio
                else if (x > arr[m2])
                    a = m2 + 1; // Buscar en el último tercio
                else {
                    a = m1 + 1; // Buscar en el tercio central
                    b = m2 - 1;
                }
            }
            // Elemento no encontrado
            return false;
        }

        public static void main(String[] args) {
            int[] arr = Entradas.arreglo(args, 0, new int[] {1, 3, 5, 7, 9});
            int a = Entradas.entero(args, 1, 0);
            int b = Entradas.entero(args, 2, 4);
            int x = Entradas.entero(args, 3, 7);

            System.out.println("Resultado: " + new Ejemploa9fc79021755().buscar(arr, a, b, x));
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función buscar(arr, a, b, x)
        mientras a <= b
            m1 ← a + (b - a) div 3
            m2 ← b - (b - a + 2) div 3
            si arr[m1] == x o arr[m2] == x entonces
                retornar verdadero
            si x < arr[m1] entonces
                b ← m1 - 1
            si no, si x > arr[m2] entonces
                a ← m2 + 1
            si no
                a ← m1 + 1
                b ← m2 - 1
        retornar falso
    ```

=== "Python"

    ```python
    def buscar(arr, a, b, x):
        while a <= b:
            m1 = a + (b - a) // 3
            m2 = b - (b - a + 2) // 3
            if arr[m1] == x or arr[m2] == x:
                return True
            if x < arr[m1]:
                b = m1 - 1
            elif x > arr[m2]:
                a = m2 + 1
            else:
                a = m1 + 1
                b = m2 - 1
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
            int m1 = a + (b - a) / 3;
            int m2 = b - (int) ceil((b - a) / 3.0);
            if (arr[m1] == x || arr[m2] == x) {
                return true;
            }
            if (x < arr[m1]) {
                b = m1 - 1; // Buscar en el primer tercio
            }
            else if (x > arr[m2]) {
                a = m2 + 1; // Buscar en el último tercio
            }
            else {
                a = m1 + 1; // Buscar en el tercio central
                b = m2 - 1;
            }
        }
        // Elemento no encontrado
        return false;
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo ordenado ascendentemente. |
| `a, b` | Límites inclusivos. |
| `x` | Valor buscado. |
| `m1, m2` | Dos pivotes del intervalo. |

**Precondiciones:** arr no nulo y ordenado; límites válidos para intervalo no vacío.

**Resultado:** Devuelve true si encuentra x; false al agotar el intervalo.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>El navegador facilita la ejecución de código Java y Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Java ni Python; el código se ejecuta en tu navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-a9fc79021755">Lenguaje del ejemplo</label><select id="language-a9fc79021755" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemploa9fc79021755" aria-label="Código Java · Búsqueda ternaria iterativa"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemploa9fc79021755</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">buscar</span><span class="p">(</span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">b</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">x</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">while</span><span class="w"> </span><span class="p">(</span><span class="n">a</span><span class="w"> </span><span class="o">&lt;=</span><span class="w"> </span><span class="n">b</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="kt">int</span><span class="w"> </span><span class="n">m1</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="p">(</span><span class="n">b</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">a</span><span class="p">)</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="mi">3</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="kt">int</span><span class="w"> </span><span class="n">m2</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">b</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="p">(</span><span class="kt">int</span><span class="p">)</span><span class="w"> </span><span class="n">Math</span><span class="p">.</span><span class="na">ceil</span><span class="p">((</span><span class="n">b</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">a</span><span class="p">)</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="mf">3.0</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">arr</span><span class="o">[</span><span class="n">m1</span><span class="o">]</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="n">x</span><span class="w"> </span><span class="o">||</span><span class="w"> </span><span class="n">arr</span><span class="o">[</span><span class="n">m2</span><span class="o">]</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="k">return</span><span class="w"> </span><span class="kc">true</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">x</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">arr</span><span class="o">[</span><span class="n">m1</span><span class="o">]</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="n">b</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">m1</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="mi">1</span><span class="p">;</span><span class="w"> </span><span class="c1">// Buscar en el primer tercio</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">else</span><span class="w"> </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">x</span><span class="w"> </span><span class="o">&gt;</span><span class="w"> </span><span class="n">arr</span><span class="o">[</span><span class="n">m2</span><span class="o">]</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="n">a</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">m2</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="p">;</span><span class="w"> </span><span class="c1">// Buscar en el último tercio</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">else</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="n">a</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">m1</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="p">;</span><span class="w"> </span><span class="c1">// Buscar en el tercio central</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="n">b</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">m2</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="mi">1</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="c1">// Elemento no encontrado</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">return</span><span class="w"> </span><span class="kc">false</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">arreglo</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: arr" spellcheck="false" data-editable data-java-input="arr"><span class="p">{</span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span class="mi">5</span><span class="p">,</span><span class="w"> </span><span class="mi">7</span><span class="p">,</span><span class="w"> </span><span class="mi">9</span><span class="p">}</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: a" spellcheck="false" data-editable data-java-input="a"><span class="mi">0</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">b</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: b" spellcheck="false" data-editable data-java-input="b"><span class="mi">4</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">x</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: x" spellcheck="false" data-editable data-java-input="x"><span class="mi">7</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Resultado: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="n">Ejemploa9fc79021755</span><span class="p">().</span><span class="na">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">b</span><span class="p">,</span><span class="w"> </span><span class="n">x</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-a9fc79021755" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Búsqueda ternaria iterativa"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">x</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">while</span> <span class="n">a</span> <span class="o">&lt;=</span> <span class="n">b</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="n">m1</span> <span class="o">=</span> <span class="n">a</span> <span class="o">+</span> <span class="p">(</span><span class="n">b</span> <span class="o">-</span> <span class="n">a</span><span class="p">)</span> <span class="o">//</span> <span class="mi">3</span></span><span class="python-code-line" data-code-line>        <span class="n">m2</span> <span class="o">=</span> <span class="n">b</span> <span class="o">-</span> <span class="p">(</span><span class="n">b</span> <span class="o">-</span> <span class="n">a</span> <span class="o">+</span> <span class="mi">2</span><span class="p">)</span> <span class="o">//</span> <span class="mi">3</span></span><span class="python-code-line" data-code-line>        <span class="k">if</span> <span class="n">arr</span><span class="p">[</span><span class="n">m1</span><span class="p">]</span> <span class="o">==</span> <span class="n">x</span> <span class="ow">or</span> <span class="n">arr</span><span class="p">[</span><span class="n">m2</span><span class="p">]</span> <span class="o">==</span> <span class="n">x</span><span class="p">:</span></span><span class="python-code-line" data-code-line>            <span class="k">return</span> <span class="kc">True</span></span><span class="python-code-line" data-code-line>        <span class="k">if</span> <span class="n">x</span> <span class="o">&lt;</span> <span class="n">arr</span><span class="p">[</span><span class="n">m1</span><span class="p">]:</span></span><span class="python-code-line" data-code-line>            <span class="n">b</span> <span class="o">=</span> <span class="n">m1</span> <span class="o">-</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>        <span class="k">elif</span> <span class="n">x</span> <span class="o">&gt;</span> <span class="n">arr</span><span class="p">[</span><span class="n">m2</span><span class="p">]:</span></span><span class="python-code-line" data-code-line>            <span class="n">a</span> <span class="o">=</span> <span class="n">m2</span> <span class="o">+</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>        <span class="k">else</span><span class="p">:</span></span><span class="python-code-line" data-code-line>            <span class="n">a</span> <span class="o">=</span> <span class="n">m1</span> <span class="o">+</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>            <span class="n">b</span> <span class="o">=</span> <span class="n">m2</span> <span class="o">-</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 17" spellcheck="false" data-editable><span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">5</span><span class="p">,</span> <span class="mi">7</span><span class="p">,</span> <span class="mi">9</span><span class="p">]</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 18" spellcheck="false" data-editable><span class="n">a</span> <span class="o">=</span> <span class="mi">0</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 19" spellcheck="false" data-editable><span class="n">b</span> <span class="o">=</span> <span class="mi">4</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 20" spellcheck="false" data-editable><span class="n">x</span> <span class="o">=</span> <span class="mi">7</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">resultado</span> <span class="o">=</span> <span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Resultado:"</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

La animación ejecuta una adaptación Python y registra estados visuales; sus pasos de interfaz no equivalen necesariamente a comparaciones del Java. El contador de eficiencia usa búsquedas sobre un objetivo presente y promedia ensayos. El tiempo teórico se estima a partir de una operación calibrada; no es una medición del listado Java.

El contador de ternaria usa un ciclo: mide una adaptación iterativa y cuenta por separado las dos comparaciones con pivotes.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/core/search/search_metrics.py).

<!-- book-code:end -->

### Complejidad: versión iterativa y versión recursiva

La versión iterativa mantiene los límites del intervalo y calcula dos puntos internos en cada vuelta del ciclo. La versión recursiva hace la misma partición en tres segmentos y continúa con una llamada sobre el tercio que aún puede contener el objetivo.

La diferencia principal entre ambas implementaciones aparece en el uso de memoria. La versión iterativa reutiliza el mismo marco de ejecución y conserva una cantidad constante de variables auxiliares. La versión recursiva crea un nuevo marco por cada llamada pendiente; por esa razón, la pila de ejecución puede crecer con la cantidad de divisiones, saltos o comparaciones acumuladas.

#### Resumen general

<div style="display:flex; justify-content:center; margin:1.2em 0;">
<table style="margin: 0 auto; text-align: center;">
  <thead>
    <tr>
      <th>Implementación</th>
      <th>Escenario</th>
      <th><i>T</i>(<i>n</i>)</th>
      <th><i>S</i>(<i>n</i>)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Iterativa</td><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Iterativa</td><td>Caso promedio</td><td>\(\Theta(\log_3(n))\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Iterativa</td><td>Peor caso</td><td>\(O(\log_3(n))\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Caso promedio</td><td>\(\Theta(\log_3(n))\)</td><td>\(\Theta(\log_3(n))\)</td></tr>
    <tr><td>Recursiva</td><td>Peor caso</td><td>\(O(\log_3(n))\)</td><td>\(O(\log_3(n))\)</td></tr>
  </tbody>
</table>
</div>

#### Versión iterativa

En la implementación iterativa, cada paso calcula \(m_1\) y \(m_2\), compara el objetivo con esos puntos y conserva solo el tercio que puede contenerlo. El espacio auxiliar se mantiene constante porque los límites se actualizan en el mismo marco de ejecución.

<div style="display:flex; justify-content:center; margin:1.2em 0;">
<table style="margin: 0 auto; text-align: center;">
  <thead>
    <tr>
      <th>Escenario</th>
      <th><i>T</i>(<i>n</i>)</th>
      <th><i>S</i>(<i>n</i>)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(\Theta(\log_3(n))\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(\log_3(n))\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** El objetivo coincide con \(m_1\) o \(m_2\) en la primera partición. Se ejecuta una cantidad constante de comparaciones.
- **Caso promedio.** El objetivo suele encontrarse después de varias particiones. La longitud del intervalo pasa de \(n\) a \(n/3\), luego a \(n/9\) y así sucesivamente, lo que produce \(T(n) \in \Theta(\log_3(n))\) con espacio constante.
- **Peor caso.** La búsqueda continúa hasta que el intervalo queda vacío o tiene un único elemento. La cantidad de niveles queda acotada por \(O(\log_3(n))\) y la memoria iterativa por \(O(1)\).

#### Versión recursiva

En la implementación recursiva, cada partición del arreglo genera una llamada sobre un tercio del intervalo anterior. La profundidad de esa cadena de llamadas es proporcional a \(\log_3(n)\).

<div style="display:flex; justify-content:center; margin:1.2em 0;">
<table style="margin: 0 auto; text-align: center;">
  <thead>
    <tr>
      <th>Escenario</th>
      <th><i>T</i>(<i>n</i>)</th>
      <th><i>S</i>(<i>n</i>)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(\Theta(\log_3(n))\)</td><td>\(\Theta(\log_3(n))\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(\log_3(n))\)</td><td>\(O(\log_3(n))\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** La primera llamada encuentra el objetivo en uno de los puntos internos. La pila conserva profundidad constante.
- **Caso promedio.** La recursión avanza por una cadena de tercios hasta aproximarse al objetivo. La profundidad esperada es \(\Theta(\log_3(n))\), por eso el tiempo y la memoria de pila comparten esa forma.
- **Peor caso.** La recursión consume la máxima cantidad de particiones antes de terminar. El tiempo y el espacio pertenecen a \(O(\log_3(n))\).



---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y si el objetivo debe estar presente o ausente.
3. Use el botón `Buscar` para ejecutar la animación paso a paso o de forma automática.
4. Observe cómo se calculan dos puntos medios y se descarta un tercio del arreglo en cada paso.

### Eficiencia por tamaño de arreglo

La siguiente celda simula la búsqueda ternaria sobre arreglos de tamaño creciente y mide el **número de operaciones** necesarias para encontrar el objetivo (siempre presente).

- **Línea sólida** — simulación empírica (n ≤ 5 000, 50 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 10 000 000
- **Checkbox** — superpone la función teórica 2·log₃(n) normalizada

El gráfico usa escala logarítmica en ambos ejes. Aunque la base es 3, el doble de comparaciones por iteración la hace ligeramente menos eficiente que la búsqueda binaria.

#### Tabla de resultados

La tabla muestra, para cada tamaño de arreglo \(n\) evaluado:

- **Operaciones teóricas** y **Tiempo teórico**: calculados con la función \(f(n)\) descrita abajo.
- **Operaciones obtenidas** y **Tiempo (s)**: medidos directamente en la simulación.

---

Complejidad temporal por escenario:

<div style="display:flex; justify-content:center; margin:1.2em 0;">
<table style="margin: 0 auto; text-align: center;">
  <thead>
    <tr><th>Escenario</th><th>Función exacta</th><th>Notación asintótica</th></tr>
  </thead>
  <tbody>
    <tr><td>Mejor caso</td><td>\(1\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(2\cdot\log_3(n)\)</td><td>\(\Theta(\log_3(n))\)</td></tr>
    <tr><td>Peor caso</td><td>\(2\cdot\log_3(n)\)</td><td>\(O(\log_3(n))\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio y peor caso** (misma función). El factor \(2\) se debe a que cada iteración necesita **dos comparaciones** para determinar en cuál de los tres segmentos continuar, frente a la única comparación de la búsqueda binaria.

\[
f(n) = 2\cdot\log_3(n)
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.

### Equivalencia asintótica: \(\log_3(n)\) y \(\log_2(n)\)

Cuando se compara con la búsqueda binaria, el costo de la búsqueda ternaria es aproximadamente un **26.2 %** menos eficiente en número de comparaciones, ya que requiere \(2 \cdot \log_3(n)\) operaciones frente a \(\log_2(n)\) de la búsqueda binaria.

Aplicando el cambio de base:

\[
\log_3(n) = \frac{\log_2(n)}{\log_2(3)}
\]

se obtiene la función de la búsqueda ternaria expresada en base 2:

\[
2 \cdot \log_3(n) = \frac{2}{\log_2(3)} \cdot \log_2(n) = \frac{2}{1.585} \cdot \log_2(n) \approx 1.261 \cdot \log_2(n)
\]

Sin embargo, en el límite asintótico, el factor \(\frac{2}{\log_2(3)} \approx 1.261\) es una constante multiplicativa. Las constantes se absorben en la notación \(\Theta\), por lo que la diferencia se vuelve despreciable y ambas búsquedas pertenecen a la misma clase de complejidad:

\[
2 \cdot \log_3(n) \in \Theta(\log_2(n))
\]

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-7/busqueda_ternaria/busqueda_ternaria_ejemplo_1.png" alt="Secuencia visual de 7.7 búsqueda ternaria · paso representativo 1 de 4"><figcaption>Secuencia visual de 7.7 búsqueda ternaria · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_ternaria/busqueda_ternaria_ejemplo_2.png" alt="Secuencia visual de 7.7 búsqueda ternaria · paso representativo 2 de 4"><figcaption>Secuencia visual de 7.7 búsqueda ternaria · paso representativo 2 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_ternaria/busqueda_ternaria_ejemplo_4.png" alt="Secuencia visual de 7.7 búsqueda ternaria · paso representativo 3 de 4"><figcaption>Secuencia visual de 7.7 búsqueda ternaria · paso representativo 3 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_ternaria/busqueda_ternaria_caso_promedio_3.png" alt="Visualización del caso promedio de 7.7 búsqueda ternaria"><figcaption>Visualización del caso promedio de 7.7 búsqueda ternaria.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-busquedas/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../5-busqueda-exponencial/">← 7.6 Búsqueda exponencial</a><a class="section-step__index" href="../">Capítulo 7</a><a class="section-step__next" href="../ejercicios-propuestos/">7.9 Ejercicios propuestos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>
