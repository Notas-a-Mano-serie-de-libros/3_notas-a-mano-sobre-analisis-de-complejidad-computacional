<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 4 · Ordenamiento por mezcla

<span class="chapter-kicker">Capítulo 6</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

#### Código

<!-- book-code:start -->

##### Ordenamiento por mezcla y combinación

Implementación basada en el libro, página 247 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemploe32ce151575f {
        public void ordenar(int[] arr, int a, int b) {
            if (a >= b)
                return;
            int m = a + (b - a) / 2;
            ordenar(arr, a, m);
            ordenar(arr, m + 1, b);
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
            new Ejemploe32ce151575f().ordenar(arr, a, b);
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

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>El navegador facilita la ejecución de código Java y Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Java ni Python; el código se ejecuta en tu navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-e32ce151575f">Lenguaje del ejemplo</label><select id="language-e32ce151575f" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemploe32ce151575f" aria-label="Código Java · Ordenamiento por mezcla y combinación"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemploe32ce151575f</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">b</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">a</span><span class="w"> </span><span class="o">&gt;=</span><span class="w"> </span><span class="n">b</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="p">(</span><span class="n">b</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">a</span><span class="p">)</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="mi">2</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">m</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="n">b</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">combinar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">m</span><span class="p">,</span><span class="w"> </span><span class="n">b</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">combinar</span><span class="p">(</span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">m</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">b</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">izquierda</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Arrays</span><span class="p">.</span><span class="na">copyOfRange</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">derecha</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Arrays</span><span class="p">.</span><span class="na">copyOfRange</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="n">b</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">i</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span class="n">j</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span class="n">k</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">a</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">while</span><span class="w"> </span><span class="p">(</span><span class="n">i</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">izquierda</span><span class="p">.</span><span class="na">length</span><span class="w"> </span><span class="o">&amp;&amp;</span><span class="w"> </span><span class="n">j</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">derecha</span><span class="p">.</span><span class="na">length</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">izquierda</span><span class="o">[</span><span class="n">i</span><span class="o">]</span><span class="w"> </span><span class="o">&lt;=</span><span class="w"> </span><span class="n">derecha</span><span class="o">[</span><span class="n">j</span><span class="o">]</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="n">arr</span><span class="o">[</span><span class="n">k</span><span class="o">++]</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">izquierda</span><span class="o">[</span><span class="n">i</span><span class="o">++]</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">else</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="n">arr</span><span class="o">[</span><span class="n">k</span><span class="o">++]</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">derecha</span><span class="o">[</span><span class="n">j</span><span class="o">++]</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">while</span><span class="w"> </span><span class="p">(</span><span class="n">i</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">izquierda</span><span class="p">.</span><span class="na">length</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="n">arr</span><span class="o">[</span><span class="n">k</span><span class="o">++]</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">izquierda</span><span class="o">[</span><span class="n">i</span><span class="o">++]</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">while</span><span class="w"> </span><span class="p">(</span><span class="n">j</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">derecha</span><span class="p">.</span><span class="na">length</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="n">arr</span><span class="o">[</span><span class="n">k</span><span class="o">++]</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">derecha</span><span class="o">[</span><span class="n">j</span><span class="o">++]</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">arreglo</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: arr" spellcheck="false" data-editable data-java-input="arr"><span class="p">{</span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">}</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: a" spellcheck="false" data-editable data-java-input="a"><span class="mi">0</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">b</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: b" spellcheck="false" data-editable data-java-input="b"><span class="mi">2</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Arreglo inicial: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">Arrays</span><span class="p">.</span><span class="na">toString</span><span class="p">(</span><span class="n">arr</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">new</span><span class="w"> </span><span class="n">Ejemploe32ce151575f</span><span class="p">().</span><span class="na">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">b</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Arreglo ordenado: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">Arrays</span><span class="p">.</span><span class="na">toString</span><span class="p">(</span><span class="n">arr</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-e32ce151575f" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Ordenamiento por mezcla y combinación"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">a</span> <span class="o">&gt;=</span> <span class="n">b</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span></span><span class="python-code-line" data-code-line>    <span class="n">m</span> <span class="o">=</span> <span class="n">a</span> <span class="o">+</span> <span class="p">(</span><span class="n">b</span> <span class="o">-</span> <span class="n">a</span><span class="p">)</span> <span class="o">//</span> <span class="mi">2</span></span><span class="python-code-line" data-code-line>    <span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">m</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">m</span> <span class="o">+</span> <span class="mi">1</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="n">combinar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">m</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">combinar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">m</span><span class="p">,</span> <span class="n">b</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="n">izquierda</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">a</span><span class="p">:</span><span class="n">m</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]</span></span><span class="python-code-line" data-code-line>    <span class="n">derecha</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">m</span> <span class="o">+</span> <span class="mi">1</span><span class="p">:</span><span class="n">b</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]</span></span><span class="python-code-line" data-code-line>    <span class="n">i</span> <span class="o">=</span> <span class="mi">0</span></span><span class="python-code-line" data-code-line>    <span class="n">j</span> <span class="o">=</span> <span class="mi">0</span></span><span class="python-code-line" data-code-line>    <span class="n">k</span> <span class="o">=</span> <span class="n">a</span></span><span class="python-code-line" data-code-line>    <span class="k">while</span> <span class="n">i</span> <span class="o">&lt;</span> <span class="nb">len</span><span class="p">(</span><span class="n">izquierda</span><span class="p">)</span> <span class="ow">and</span> <span class="n">j</span> <span class="o">&lt;</span> <span class="nb">len</span><span class="p">(</span><span class="n">derecha</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="k">if</span> <span class="n">izquierda</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">&lt;=</span> <span class="n">derecha</span><span class="p">[</span><span class="n">j</span><span class="p">]:</span></span><span class="python-code-line" data-code-line>            <span class="n">arr</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="n">izquierda</span><span class="p">[</span><span class="n">i</span><span class="p">]</span></span><span class="python-code-line" data-code-line>            <span class="n">i</span> <span class="o">+=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>        <span class="k">else</span><span class="p">:</span></span><span class="python-code-line" data-code-line>            <span class="n">arr</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="n">derecha</span><span class="p">[</span><span class="n">j</span><span class="p">]</span></span><span class="python-code-line" data-code-line>            <span class="n">j</span> <span class="o">+=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>        <span class="n">k</span> <span class="o">+=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>    <span class="k">while</span> <span class="n">i</span> <span class="o">&lt;</span> <span class="nb">len</span><span class="p">(</span><span class="n">izquierda</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="n">arr</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="n">izquierda</span><span class="p">[</span><span class="n">i</span><span class="p">]</span></span><span class="python-code-line" data-code-line>        <span class="n">i</span> <span class="o">+=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>        <span class="n">k</span> <span class="o">+=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>    <span class="k">while</span> <span class="n">j</span> <span class="o">&lt;</span> <span class="nb">len</span><span class="p">(</span><span class="n">derecha</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="n">arr</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="n">derecha</span><span class="p">[</span><span class="n">j</span><span class="p">]</span></span><span class="python-code-line" data-code-line>        <span class="n">j</span> <span class="o">+=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>        <span class="n">k</span> <span class="o">+=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 34" spellcheck="false" data-editable><span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">3</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">]</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 35" spellcheck="false" data-editable><span class="n">a</span> <span class="o">=</span> <span class="mi">0</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 36" spellcheck="false" data-editable><span class="n">b</span> <span class="o">=</span> <span class="mi">2</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo inicial:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo ordenado:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

##### Laboratorio y medición

La animación permite observar la estructura recursiva. El panel experimental ejecuta funciones Python: el tiempo y la memoria de ese panel corresponden a esas funciones y no a una ejecución del listado Java. La memoria se obtiene con tracemalloc; no mide directamente la pila de una JVM.

El panel ejecuta mezcla con listas y copias temporales de Python; la entrada descendente se prepara fuera de la medición.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/runtime/recursive_examples_analysis.py).

<!-- book-code:end -->

#### Análisis

La división genera dos subproblemas de tamaño \(n/2\) y la combinación recorre los \(n\) elementos. Por tanto, \(T(n)=2 \cdot T(n/2)+\Theta(n)\in\Theta(n \cdot \log_2(n))\). Los arreglos auxiliares de combinación requieren \(\Theta(n)\) memoria; la pila añade \(\Theta(\log_2(n))\), que queda dominada por el almacenamiento lineal.

#### Simulación

La vista experimental muestra las divisiones, el retorno de cada mitad y la combinación ordenada por niveles.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-6/ejemplos/arbol_recursion_mezcla.png" alt="Árbol de llamadas de ejemplo 4 · ordenamiento por mezcla"><figcaption>Árbol de llamadas de ejemplo 4 · ordenamiento por mezcla.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/arbol_recursion_mecla_2.png" alt="Árbol de llamadas de ejemplo 4 · ordenamiento por mezcla"><figcaption>Árbol de llamadas de ejemplo 4 · ordenamiento por mezcla.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../potencia/">← Ejemplo 3 · Potencia de un número entero positivo</a><a class="section-step__index" href="../">Capítulo 6</a><a class="section-step__next" href="../arbol-binario/">Ejemplo 5 · Búsqueda en árbol binario →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>
