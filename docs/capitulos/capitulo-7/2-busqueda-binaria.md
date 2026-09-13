<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>

# 7.3 Búsqueda binaria

<span class="chapter-kicker">Capítulo 7</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/2_busqueda_binaria.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

La búsqueda binaria compara el elemento central del arreglo con el objetivo. Si no coincide, descarta la mitad donde el objetivo no puede estar y repite el proceso sobre la mitad restante. Requiere que el arreglo esté ordenado.

Cada comparación reduce el espacio de búsqueda a la mitad, lo que produce una complejidad temporal logarítmica: con un millón de elementos basta con unos 20 pasos.

### Implementación

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

#### Búsqueda binaria recursiva

Implementación basada en el libro, página 273 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemplo8309d0152ea4 {
        public boolean buscar(int[] arr, int a, int b, int x) {
            if (a > b)
                return false; // Elemento no encontrado
            int m = a + (b - a) / 2;
            if (arr[m] == x)
                return true; // Elemento encontrado
            else if (x > arr[m])
                return buscar(arr, m + 1, b, x); // Busca a la derecha
            else
                return buscar(arr, a, m - 1, x); // Busca a la izquierda
        }

        public static void main(String[] args) {
            int[] arr = Entradas.arreglo(args, 0, new int[] {1, 3, 5, 7, 9});
            int a = Entradas.entero(args, 1, 0);
            int b = Entradas.entero(args, 2, 4);
            int x = Entradas.entero(args, 3, 7);

            System.out.println("Resultado: " + new Ejemplo8309d0152ea4().buscar(arr, a, b, x));
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función buscar(arr, a, b, x)
        si a > b entonces
            retornar falso
        m ← a + (b - a) div 2
        si arr[m] == x entonces
            retornar verdadero
        si x > arr[m] entonces
            retornar buscar(arr, m + 1, b, x)
        retornar buscar(arr, a, m - 1, x)
    ```

=== "Python"

    ```python
    def buscar(arr, a, b, x):
        if a > b:
            return False
        m = a + (b - a) // 2
        if arr[m] == x:
            return True
        if x > arr[m]:
            return buscar(arr, m + 1, b, x)
        return buscar(arr, a, m - 1, x)
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
        if (a > b) {
            return false; // Elemento no encontrado
        }
        int m = a + (b - a) / 2;
        if (arr[m] == x) {
            return true; // Elemento encontrado
        }
        else if (x > arr[m]) {
            return buscar(arr, m + 1, b, x); // Busca a la derecha
        }
        else {
            return buscar(arr, a, m - 1, x); // Busca a la izquierda
        }
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

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>El navegador facilita la ejecución de código Java y Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Java ni Python; el código se ejecuta en tu navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-8309d0152ea4">Lenguaje del ejemplo</label><select id="language-8309d0152ea4" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemplo8309d0152ea4" aria-label="Código Java · Búsqueda binaria recursiva"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemplo8309d0152ea4</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kt">boolean</span><span class="w"> </span><span class="nf">buscar</span><span class="p">(</span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">b</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">x</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">a</span><span class="w"> </span><span class="o">&gt;</span><span class="w"> </span><span class="n">b</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="kc">false</span><span class="p">;</span><span class="w"> </span><span class="c1">// Elemento no encontrado</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="p">(</span><span class="n">b</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">a</span><span class="p">)</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="mi">2</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">arr</span><span class="o">[</span><span class="n">m</span><span class="o">]</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="kc">true</span><span class="p">;</span><span class="w"> </span><span class="c1">// Elemento encontrado</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">else</span><span class="w"> </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">x</span><span class="w"> </span><span class="o">&gt;</span><span class="w"> </span><span class="n">arr</span><span class="o">[</span><span class="n">m</span><span class="o">]</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="n">b</span><span class="p">,</span><span class="w"> </span><span class="n">x</span><span class="p">);</span><span class="w"> </span><span class="c1">// Busca a la derecha</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">else</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="n">x</span><span class="p">);</span><span class="w"> </span><span class="c1">// Busca a la izquierda</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">arreglo</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: arr" spellcheck="false" data-editable data-java-input="arr"><span class="p">{</span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span class="mi">5</span><span class="p">,</span><span class="w"> </span><span class="mi">7</span><span class="p">,</span><span class="w"> </span><span class="mi">9</span><span class="p">}</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: a" spellcheck="false" data-editable data-java-input="a"><span class="mi">0</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">b</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: b" spellcheck="false" data-editable data-java-input="b"><span class="mi">4</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">x</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">entero</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: x" spellcheck="false" data-editable data-java-input="x"><span class="mi">7</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Resultado: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="n">Ejemplo8309d0152ea4</span><span class="p">().</span><span class="na">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">b</span><span class="p">,</span><span class="w"> </span><span class="n">x</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-8309d0152ea4" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Búsqueda binaria recursiva"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">x</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">a</span> <span class="o">&gt;</span> <span class="n">b</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line>    <span class="n">m</span> <span class="o">=</span> <span class="n">a</span> <span class="o">+</span> <span class="p">(</span><span class="n">b</span> <span class="o">-</span> <span class="n">a</span><span class="p">)</span> <span class="o">//</span> <span class="mi">2</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">arr</span><span class="p">[</span><span class="n">m</span><span class="p">]</span> <span class="o">==</span> <span class="n">x</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span> <span class="kc">True</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">x</span> <span class="o">&gt;</span> <span class="n">arr</span><span class="p">[</span><span class="n">m</span><span class="p">]:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span> <span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">m</span> <span class="o">+</span> <span class="mi">1</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">m</span> <span class="o">-</span> <span class="mi">1</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 12" spellcheck="false" data-editable><span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">3</span><span class="p">,</span> <span class="mi">5</span><span class="p">,</span> <span class="mi">7</span><span class="p">,</span> <span class="mi">9</span><span class="p">]</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 13" spellcheck="false" data-editable><span class="n">a</span> <span class="o">=</span> <span class="mi">0</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 14" spellcheck="false" data-editable><span class="n">b</span> <span class="o">=</span> <span class="mi">4</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 15" spellcheck="false" data-editable><span class="n">x</span> <span class="o">=</span> <span class="mi">7</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">resultado</span> <span class="o">=</span> <span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Resultado:"</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

La animación ejecuta una adaptación Python y registra estados visuales; sus pasos de interfaz no equivalen necesariamente a comparaciones del Java. El contador de eficiencia usa búsquedas sobre un objetivo presente y promedia ensayos. El tiempo teórico se estima a partir de una operación calibrada; no es una medición del listado Java.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/core/search/search_metrics.py).

<!-- book-code:end -->

### Complejidad: versión iterativa y versión recursiva

La versión iterativa actualiza los límites del intervalo activo dentro de un ciclo. La versión recursiva expresa la misma reducción del intervalo mediante llamadas que reciben los límites actualizados.

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
    <tr><td>Iterativa</td><td>Caso promedio</td><td>\(\Theta(\log_2(n))\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Iterativa</td><td>Peor caso</td><td>\(O(\log_2(n))\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Caso promedio</td><td>\(\Theta(\log_2(n))\)</td><td>\(\Theta(\log_2(n))\)</td></tr>
    <tr><td>Recursiva</td><td>Peor caso</td><td>\(O(\log_2(n))\)</td><td>\(O(\log_2(n))\)</td></tr>
  </tbody>
</table>
</div>

#### Versión iterativa

En la implementación iterativa, cada comparación calcula el índice medio y conserva solo los límites \(a\) y \(b\). Cada descarte reduce el intervalo activo a la mitad.

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
    <tr><td>Caso promedio</td><td>\(\Theta(\log_2(n))\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(\log_2(n))\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** El objetivo coincide con el primer índice medio. Se ejecuta una comparación efectiva, entonces \(T(n) \in \Omega(1)\) y el espacio auxiliar es constante.
- **Caso promedio.** El objetivo aparece en un nivel intermedio del árbol de decisiones. La cantidad esperada de divisiones es proporcional a \(\log_2(n)\), por lo que \(T(n) \in \Theta(\log_2(n))\).
- **Peor caso.** El intervalo se divide hasta quedar vacío o hasta alcanzar un único elemento. La profundidad máxima es \(\lceil \log_2(n) \rceil\), por eso \(T(n) \in O(\log_2(n))\) y \(S(n) \in O(1)\).

#### Versión recursiva

En la implementación recursiva, cada llamada recibe un intervalo cuya longitud es aproximadamente la mitad de la anterior. El número de comparaciones es el mismo orden que en la versión iterativa, pero la pila crece con la profundidad de divisiones.

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
    <tr><td>Caso promedio</td><td>\(\Theta(\log_2(n))\)</td><td>\(\Theta(\log_2(n))\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(\log_2(n))\)</td><td>\(O(\log_2(n))\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** La primera llamada encuentra el objetivo en el medio. La pila activa conserva una profundidad constante.
- **Caso promedio.** La búsqueda desciende por varios niveles del árbol binario de decisiones. El tiempo esperado y el número de llamadas activas crecen como \(\Theta(\log_2(n))\).
- **Peor caso.** La recursión alcanza la máxima profundidad antes de encontrar el objetivo o confirmar su ausencia. El tiempo y la memoria de pila pertenecen a \(O(\log_2(n))\).



---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y si el objetivo debe estar presente o ausente.
3. Use el botón `Buscar` para ejecutar la animación paso a paso o de forma automática.
4. Observe cómo el algoritmo descarta la mitad del arreglo en cada paso.

### Eficiencia por tamaño de arreglo

La siguiente celda simula la búsqueda binaria sobre arreglos de tamaño creciente y mide el **número de operaciones** necesarias para encontrar el objetivo (siempre presente).

- **Línea sólida** — simulación empírica (n ≤ 5 000, 50 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 10 000 000
- **Checkbox** — superpone la función teórica log₂(n) normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva crece muy despacio: pasar de n = 1 000 a n = 1 000 000 solo duplica el número de pasos.

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
    <tr><td>Caso promedio</td><td>\(\log_2(n)\)</td><td>\(\Theta(\log_2(n))\)</td></tr>
    <tr><td>Peor caso</td><td>\(\log_2(n)\)</td><td>\(O(\log_2(n))\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio** (equivalente al peor caso en orden asintótico): la simulación busca un elemento en posición aleatoria. El mejor caso \(\Omega(1)\) se descarta por ser infrecuente.

\[
f(n) = \log_2(n)
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-7/busqueda_binaria/busqueda_binaria_ejemplo_1.png" alt="Secuencia visual de 7.3 búsqueda binaria · paso representativo 1 de 4"><figcaption>Secuencia visual de 7.3 búsqueda binaria · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_binaria/busqueda_binaria_ejemplo_2.png" alt="Secuencia visual de 7.3 búsqueda binaria · paso representativo 2 de 4"><figcaption>Secuencia visual de 7.3 búsqueda binaria · paso representativo 2 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_binaria/busqueda_binaria_ejemplo_3.png" alt="Secuencia visual de 7.3 búsqueda binaria · paso representativo 3 de 4"><figcaption>Secuencia visual de 7.3 búsqueda binaria · paso representativo 3 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_binaria/busqueda_binaria_ejemplo_caso_promedio_2.png" alt="Visualización del caso promedio de 7.3 búsqueda binaria"><figcaption>Visualización del caso promedio de 7.3 búsqueda binaria.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-busquedas/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../1-busqueda-secuencial/">← 7.2 Búsqueda secuencial</a><a class="section-step__index" href="../">Capítulo 7</a><a class="section-step__next" href="../3-busqueda-interpolacion/">7.4 Búsqueda por interpolación →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>
