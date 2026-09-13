<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# 8.5 Ordenamiento por mezcla

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/5_ordenamiento_mezcla.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ordenamiento por mezcla (merge sort) divide el arreglo a la mitad de forma recursiva hasta obtener subarreglos de un solo elemento, que por definición están ordenados. Luego combina (mezcla) los subarreglos en orden creciente hasta reconstruir el arreglo completo.

Garantiza O(n log(n)) en todos los casos, lo que lo hace predecible y eficiente, aunque requiere O(n) de memoria auxiliar para la fase de mezcla.

### Implementación

<!-- book-code:start -->

#### Ordenamiento por mezcla y combinación

Implementación basada en el libro, página 341 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemplode54bf47e11a {
        public void ordenar(int[] arr, int a, int b) {
            if (a >= b)
                return;
            // Calcula el pivote que separa el arreglo en dos
            int m = a + (b - a) / 2;
            // Etapa de división
            ordenar(arr, a, m);
            ordenar(arr, m + 1, b);
            // Etapa de combinación
            combinar(arr, a, m, b);
        }
        public void combinar(int[] arr, int a, int m, int b) {
            int[] izquierda = Arrays.copyOfRange(arr, a, m + 1);
            int[] derecha = Arrays.copyOfRange(arr, m + 1, b + 1);
            int i = 0, j = 0, k = a;
            while (i < izquierda.length && j < derecha.length) {
                if (izquierda[i] <= derecha[j])
                    arr[k++] = izquierda[i++];
                else
                    arr[k++] = derecha[j++];
            }
            while (i < izquierda.length)
                arr[k++] = izquierda[i++];
            while (j < derecha.length)
                arr[k++] = derecha[j++];
        }

        public static void main(String[] args) {
            int[] arr = Entradas.arreglo(args, 0, new int[] {3, 1, 2});
            int a = Entradas.entero(args, 1, 0);
            int b = Entradas.entero(args, 2, 2);

            System.out.println("Arreglo inicial: " + Arrays.toString(arr));
            new Ejemplode54bf47e11a().ordenar(arr, a, b);
            System.out.println("Arreglo ordenado: " + Arrays.toString(arr));
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función ordenar(arr, a, b)
        si a >= b entonces
            retornar
        m ← a + (b - a) div 2
        ordenar(arr, a, m)
        ordenar(arr, m + 1, b)
        combinar(arr, a, m, b)


    función combinar(arr, a, m, b)
        izquierda ← arr[a:m + 1]
        derecha ← arr[m + 1:b + 1]
        i ← 0
        j ← 0
        k ← a
        mientras i < longitud(izquierda) y j < longitud(derecha)
            si izquierda[i] <= derecha[j] entonces
                arr[k] ← izquierda[i]
                i += 1
            si no
                arr[k] ← derecha[j]
                j += 1
            k += 1
        mientras i < longitud(izquierda)
            arr[k] ← izquierda[i]
            i += 1
            k += 1
        mientras j < longitud(derecha)
            arr[k] ← derecha[j]
            j += 1
            k += 1
    ```

=== "Python"

    ```python
    def ordenar(arr, a, b):
        if a >= b:
            return
        m = a + (b - a) // 2
        ordenar(arr, a, m)
        ordenar(arr, m + 1, b)
        combinar(arr, a, m, b)


    def combinar(arr, a, m, b):
        izquierda = arr[a:m + 1]
        derecha = arr[m + 1:b + 1]
        i = 0
        j = 0
        k = a
        while i < len(izquierda) and j < len(derecha):
            if izquierda[i] <= derecha[j]:
                arr[k] = izquierda[i]
                i += 1
            else:
                arr[k] = derecha[j]
                j += 1
            k += 1
        while i < len(izquierda):
            arr[k] = izquierda[i]
            i += 1
            k += 1
        while j < len(derecha):
            arr[k] = derecha[j]
            j += 1
            k += 1
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    void combinar(int arr[], int a, int m, int b);

    void ordenar(int arr[], int a, int b) {
        if (a >= b) {
            return;
        }
        int m = a + (b - a) / 2;
        ordenar(arr, a, m);
        ordenar(arr, m + 1, b);
        combinar(arr, a, m, b);
    }

    void combinar(int arr[], int a, int m, int b) {
        int ni = m - a + 1;
        int nd = b - m;
        int *izquierda = malloc((size_t) ni * sizeof(int));
        int *derecha = malloc((size_t) nd * sizeof(int));
        if (izquierda == NULL || derecha == NULL) {
            free(izquierda);
            free(derecha);
            abort();
        }
        for (int i = 0; i < ni; i++) {
            izquierda[i] = arr[a + i];
        }
        for (int j = 0; j < nd; j++) {
            derecha[j] = arr[m + 1 + j];
        }
        int i = 0, j = 0, k = a;
        while (i < ni && j < nd) {
            if (izquierda[i] <= derecha[j]) {
                arr[k++] = izquierda[i++];
            } else {
                arr[k++] = derecha[j++];
            }
        }
        while (i < ni) {
            arr[k++] = izquierda[i++];
        }
        while (j < nd) {
            arr[k++] = derecha[j++];
        }
        free(izquierda);
        free(derecha);
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo que se modifica. |
| `a, b` | Extremos inclusivos del intervalo. |
| `m` | Índice que separa las mitades. |
| `izquierda, derecha` | Copias temporales de las mitades. |
| `i, j, k` | Índices dentro de las copias y del destino. |

**Precondiciones:** arr no nulo; intervalo válido o vacío. Importar java.util.Arrays.

**Resultado:** Ordena arr[a..b] en orden ascendente; no devuelve un arreglo nuevo.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>El navegador facilita la ejecución de código Java y Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Java ni Python; el código se ejecuta en tu navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-de54bf47e11a">Lenguaje del ejemplo</label><select id="language-de54bf47e11a" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemplode54bf47e11a" aria-label="Código Java · Ordenamiento por mezcla y combinación"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemplode54bf47e11a</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">b</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">a</span><span class="w"> </span><span class="o">&gt;=</span><span class="w"> </span><span class="n">b</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="c1">// Calcula el pivote que separa el arreglo en dos</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="p">(</span><span class="n">b</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">a</span><span class="p">)</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="mi">2</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="c1">// Etapa de división</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">m</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="n">b</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="c1">// Etapa de combinación</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">combinar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">m</span><span class="p">,</span><span class="w"> </span><span class="n">b</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">combinar</span><span class="p">(</span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">m</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">b</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">izquierda</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Arrays</span><span class="p">.</span><span class="na">copyOfRange</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">derecha</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Arrays</span><span class="p">.</span><span class="na">copyOfRange</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="n">b</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">i</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span class="n">j</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span class="n">k</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">a</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">while</span><span class="w"> </span><span class="p">(</span><span class="n">i</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">izquierda</span><span class="p">.</span><span class="na">length</span><span class="w"> </span><span class="o">&amp;&amp;</span><span class="w"> </span><span class="n">j</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">derecha</span><span class="p">.</span><span class="na">length</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">izquierda</span><span class="o">[</span><span class="n">i</span><span class="o">]</span><span class="w"> </span><span class="o">&lt;=</span><span class="w"> </span><span class="n">derecha</span><span class="o">[</span><span class="n">j</span><span class="o">]</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="n">arr</span><span class="o">[</span><span class="n">k</span><span class="o">++]</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">izquierda</span><span class="o">[</span><span class="n">i</span><span class="o">++]</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">else</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="n">arr</span><span class="o">[</span><span class="n">k</span><span class="o">++]</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">derecha</span><span class="o">[</span><span class="n">j</span><span class="o">++]</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">while</span><span class="w"> </span><span class="p">(</span><span class="n">i</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">izquierda</span><span class="p">.</span><span class="na">length</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="n">arr</span><span class="o">[</span><span class="n">k</span><span class="o">++]</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">izquierda</span><span class="o">[</span><span class="n">i</span><span class="o">++]</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">while</span><span class="w"> </span><span class="p">(</span><span class="n">j</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">derecha</span><span class="p">.</span><span class="na">length</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="n">arr</span><span class="o">[</span><span class="n">k</span><span class="o">++]</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">derecha</span><span class="o">[</span><span class="n">j</span><span class="o">++]</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">arreglo</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: arr" spellcheck="false" data-editable data-java-input="arr"><span class="p">{</span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">}</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: a" spellcheck="false" data-editable data-java-input="a"><span class="mi">0</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">b</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: b" spellcheck="false" data-editable data-java-input="b"><span class="mi">2</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Arreglo inicial: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">Arrays</span><span class="p">.</span><span class="na">toString</span><span class="p">(</span><span class="n">arr</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">new</span><span class="w"> </span><span class="n">Ejemplode54bf47e11a</span><span class="p">().</span><span class="na">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">b</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Arreglo ordenado: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">Arrays</span><span class="p">.</span><span class="na">toString</span><span class="p">(</span><span class="n">arr</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-de54bf47e11a" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Ordenamiento por mezcla y combinación"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">a</span> <span class="o">&gt;=</span> <span class="n">b</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span></span><span class="python-code-line" data-code-line>    <span class="n">m</span> <span class="o">=</span> <span class="n">a</span> <span class="o">+</span> <span class="p">(</span><span class="n">b</span> <span class="o">-</span> <span class="n">a</span><span class="p">)</span> <span class="o">//</span> <span class="mi">2</span></span><span class="python-code-line" data-code-line>    <span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">m</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">m</span> <span class="o">+</span> <span class="mi">1</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="n">combinar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">m</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">combinar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">m</span><span class="p">,</span> <span class="n">b</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="n">izquierda</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">a</span><span class="p">:</span><span class="n">m</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]</span></span><span class="python-code-line" data-code-line>    <span class="n">derecha</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">m</span> <span class="o">+</span> <span class="mi">1</span><span class="p">:</span><span class="n">b</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]</span></span><span class="python-code-line" data-code-line>    <span class="n">i</span> <span class="o">=</span> <span class="mi">0</span></span><span class="python-code-line" data-code-line>    <span class="n">j</span> <span class="o">=</span> <span class="mi">0</span></span><span class="python-code-line" data-code-line>    <span class="n">k</span> <span class="o">=</span> <span class="n">a</span></span><span class="python-code-line" data-code-line>    <span class="k">while</span> <span class="n">i</span> <span class="o">&lt;</span> <span class="nb">len</span><span class="p">(</span><span class="n">izquierda</span><span class="p">)</span> <span class="ow">and</span> <span class="n">j</span> <span class="o">&lt;</span> <span class="nb">len</span><span class="p">(</span><span class="n">derecha</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="k">if</span> <span class="n">izquierda</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">&lt;=</span> <span class="n">derecha</span><span class="p">[</span><span class="n">j</span><span class="p">]:</span></span><span class="python-code-line" data-code-line>            <span class="n">arr</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="n">izquierda</span><span class="p">[</span><span class="n">i</span><span class="p">]</span></span><span class="python-code-line" data-code-line>            <span class="n">i</span> <span class="o">+=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>        <span class="k">else</span><span class="p">:</span></span><span class="python-code-line" data-code-line>            <span class="n">arr</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="n">derecha</span><span class="p">[</span><span class="n">j</span><span class="p">]</span></span><span class="python-code-line" data-code-line>            <span class="n">j</span> <span class="o">+=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>        <span class="n">k</span> <span class="o">+=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>    <span class="k">while</span> <span class="n">i</span> <span class="o">&lt;</span> <span class="nb">len</span><span class="p">(</span><span class="n">izquierda</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="n">arr</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="n">izquierda</span><span class="p">[</span><span class="n">i</span><span class="p">]</span></span><span class="python-code-line" data-code-line>        <span class="n">i</span> <span class="o">+=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>        <span class="n">k</span> <span class="o">+=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>    <span class="k">while</span> <span class="n">j</span> <span class="o">&lt;</span> <span class="nb">len</span><span class="p">(</span><span class="n">derecha</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="n">arr</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="n">derecha</span><span class="p">[</span><span class="n">j</span><span class="p">]</span></span><span class="python-code-line" data-code-line>        <span class="n">j</span> <span class="o">+=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>        <span class="n">k</span> <span class="o">+=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 34" spellcheck="false" data-editable><span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">3</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">]</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 35" spellcheck="false" data-editable><span class="n">a</span> <span class="o">=</span> <span class="mi">0</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 36" spellcheck="false" data-editable><span class="n">b</span> <span class="o">=</span> <span class="mi">2</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo inicial:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo ordenado:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

La animación y el contador son adaptaciones Python con operaciones instrumentadas. Incluyen comparaciones, movimientos y control del recorrido según el contador; no se deben interpretar todos los pasos como una sola clase de operación Java. Las opciones descendentes son ampliaciones: los listados del libro ordenan ascendentemente.

La adaptación usa copias temporales y representa el árbol de divisiones y combinaciones.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/core/sort/sort_algorithms.py).

<!-- book-code:end -->

### Complejidad

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
    <tr><td>Mejor caso</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>\(\Omega(n)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(\Theta(n \cdot \log_2(n))\)</td><td>\(\Theta(n)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(n \cdot \log_2(n))\)</td><td>\(O(n)\)</td></tr>
  </tbody>
</table>
</div>

Este resumen presenta los resultados generales. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.


---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y el orden deseado.
3. Use el botón `Ordenar` para ejecutar la animación paso a paso o de forma automática.
4. Observe las fases de división y mezcla del arreglo.

### Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento por mezcla sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios.

- **Línea sólida** — simulación empírica (n ≤ 2 000, 5 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 1 000 000
- **Checkbox** — superpone la función teórica n·log₂(n) normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva crece mucho más despacio que los algoritmos O(n²), lo que refleja la ventaja del enfoque divide y vencerás.

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
    <tr><td>Mejor caso</td><td>\(n\cdot\log_2(n)\)</td><td>\(\Omega(n\cdot\log_2(n))\)</td></tr>
    <tr><td>Caso promedio</td><td>\(n\cdot\log_2(n)\)</td><td>\(\Theta(n\cdot\log_2(n))\)</td></tr>
    <tr><td>Peor caso</td><td>\(n\cdot\log_2(n)\)</td><td>\(O(n\cdot\log_2(n))\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa la **función exacta para todos los escenarios**: ordenamiento por mezcla tiene complejidad uniforme porque siempre divide y mezcla con la misma estructura recursiva, independientemente del orden inicial.

\[
f(n) = n\cdot\log_2(n)
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_mezcla/ordenamiento_mezcla_1.png" alt="Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 1 de 4"><figcaption>Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_mezcla/ordenamiento_mezcla_7.png" alt="Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 2 de 4"><figcaption>Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 2 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_mezcla/ordenamiento_mezcla_13.png" alt="Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 3 de 4"><figcaption>Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 3 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_mezcla/ordenamiento_mezcla_20.png" alt="Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 4 de 4"><figcaption>Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 4 de 4.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../4-ordenamiento-shell/">← Ampliación · Ordenamiento Shell</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../6-ordenamiento-rapido/">8.6 Ordenamiento rápido →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
