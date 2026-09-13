<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# 8.4 Ordenamiento por inserción

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/3_ordenamiento_insercion.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ordenamiento por inserción construye el arreglo ordenado de izquierda a derecha: toma cada elemento y lo inserta en su posición correcta dentro del subarreglo ya ordenado, desplazando los elementos mayores hacia la derecha.

Es muy eficiente para arreglos casi ordenados (O(n) en el mejor caso) y es el algoritmo preferido para arreglos pequeños dentro de implementaciones híbridas como Timsort.

### Implementación

<!-- book-code:start -->

#### Inserción mediante desplazamientos

Implementación basada en el libro, página 333 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemplofc52378a9813 {
        public static void ordenar(int[] arr) {
            for (int i = 1; i < arr.length; i++) {
                int clave = arr[i], j = i - 1;
                 // Aplica el criterio
                while (j >= 0 && arr[j] > clave) {
                    arr[j + 1] = arr[j];
                    j--;
                }
                arr[j + 1] = clave;
            }
        }

        public static void main(String[] args) {
            int[] arr = Entradas.arreglo(args, 0, new int[] {3, 1, 2});

            System.out.println("Arreglo inicial: " + Arrays.toString(arr));
            Ejemplofc52378a9813.ordenar(arr);
            System.out.println("Arreglo ordenado: " + Arrays.toString(arr));
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función ordenar(arr)
        para i en rango(1, longitud(arr))
            clave ← arr[i]
            j ← i - 1
            mientras j >= 0 y arr[j] > clave
                arr[j + 1] ← arr[j]
                j -= 1
            arr[j + 1] ← clave
    ```

=== "Python"

    ```python
    def ordenar(arr):
        for i in range(1, len(arr)):
            clave = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > clave:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = clave
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    void ordenar(int arr[], int n) {
        for (int i = 1; i < n; i++) {
            int clave = arr[i], j = i - 1;
             // Aplica el criterio
            while (j >= 0 && arr[j] > clave) {
                arr[j + 1] = arr[j];
                j--;
            }
            arr[j + 1] = clave;
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, `n` indica la longitud del arreglo y se recibe como parámetro.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo que se modifica. |
| `i` | Posición que se inserta. |
| `clave` | Valor conservado durante los desplazamientos. |
| `j` | Índice que retrocede por el prefijo ordenado. |

**Precondiciones:** arr no nulo.

**Resultado:** Ordena ascendentemente, conservando el orden de valores iguales.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>El navegador facilita la ejecución de código Java y Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Java ni Python; el código se ejecuta en tu navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-fc52378a9813">Lenguaje del ejemplo</label><select id="language-fc52378a9813" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemplofc52378a9813" aria-label="Código Java · Inserción mediante desplazamientos"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemplofc52378a9813</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">for</span><span class="w"> </span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">i</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="mi">1</span><span class="p">;</span><span class="w"> </span><span class="n">i</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">arr</span><span class="p">.</span><span class="na">length</span><span class="p">;</span><span class="w"> </span><span class="n">i</span><span class="o">++</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="kt">int</span><span class="w"> </span><span class="n">clave</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">arr</span><span class="o">[</span><span class="n">i</span><span class="o">]</span><span class="p">,</span><span class="w"> </span><span class="n">j</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">i</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="mi">1</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">             </span><span class="c1">// Aplica el criterio</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">while</span><span class="w"> </span><span class="p">(</span><span class="n">j</span><span class="w"> </span><span class="o">&gt;=</span><span class="w"> </span><span class="mi">0</span><span class="w"> </span><span class="o">&amp;&amp;</span><span class="w"> </span><span class="n">arr</span><span class="o">[</span><span class="n">j</span><span class="o">]</span><span class="w"> </span><span class="o">&gt;</span><span class="w"> </span><span class="n">clave</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="n">arr</span><span class="o">[</span><span class="n">j</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="o">]</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">arr</span><span class="o">[</span><span class="n">j</span><span class="o">]</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="n">j</span><span class="o">--</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="n">arr</span><span class="o">[</span><span class="n">j</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="mi">1</span><span class="o">]</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">clave</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">arreglo</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: arr" spellcheck="false" data-editable data-java-input="arr"><span class="p">{</span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">}</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Arreglo inicial: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">Arrays</span><span class="p">.</span><span class="na">toString</span><span class="p">(</span><span class="n">arr</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemplofc52378a9813</span><span class="p">.</span><span class="na">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Arreglo ordenado: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">Arrays</span><span class="p">.</span><span class="na">toString</span><span class="p">(</span><span class="n">arr</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-fc52378a9813" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Inserción mediante desplazamientos"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="nb">len</span><span class="p">(</span><span class="n">arr</span><span class="p">)):</span></span><span class="python-code-line" data-code-line>        <span class="n">clave</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">i</span><span class="p">]</span></span><span class="python-code-line" data-code-line>        <span class="n">j</span> <span class="o">=</span> <span class="n">i</span> <span class="o">-</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>        <span class="k">while</span> <span class="n">j</span> <span class="o">&gt;=</span> <span class="mi">0</span> <span class="ow">and</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">&gt;</span> <span class="n">clave</span><span class="p">:</span></span><span class="python-code-line" data-code-line>            <span class="n">arr</span><span class="p">[</span><span class="n">j</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span></span><span class="python-code-line" data-code-line>            <span class="n">j</span> <span class="o">-=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>        <span class="n">arr</span><span class="p">[</span><span class="n">j</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]</span> <span class="o">=</span> <span class="n">clave</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 11" spellcheck="false" data-editable><span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">3</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">]</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo inicial:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo ordenado:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

La animación y el contador son adaptaciones Python con operaciones instrumentadas. Incluyen comparaciones, movimientos y control del recorrido según el contador; no se deben interpretar todos los pasos como una sola clase de operación Java. Las opciones descendentes son ampliaciones: los listados del libro ordenan ascendentemente.

La adaptación animada emplea intercambios contiguos; el Java conserva clave y desplaza elementos. No tienen el mismo conteo de escrituras.

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
    <tr><td>Mejor caso</td><td>\(\Omega(n)\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(\Theta(n^2)\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(n^2)\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

Este resumen presenta los resultados generales. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.


---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y el orden deseado.
3. Use el botón `Ordenar` para ejecutar la animación paso a paso o de forma automática.
4. Observe cómo cada nuevo elemento se inserta en su lugar correcto dentro de la parte ya ordenada.

### Variante: inserción binaria

El ordenamiento por inserción localiza, para cada elemento, la posición que debe ocupar dentro del prefijo ya ordenado. En la versión clásica esa búsqueda se hace de derecha a izquierda mediante comparaciones consecutivas. La variante de **inserción binaria** aprovecha que el prefijo `arr[0:i]` ya está ordenado y usa búsqueda binaria para encontrar la posición de inserción.

La mejora principal está en la cantidad de comparaciones usadas para decidir la posición del elemento: en lugar de revisar linealmente el prefijo, la búsqueda binaria reduce el rango activo a la mitad en cada comparación. Esto puede bajar las comparaciones de búsqueda de un comportamiento lineal por iteración a uno logarítmico por iteración.

El desplazamiento de elementos sigue siendo necesario, porque insertar dentro de un arreglo exige mover una sección hacia la derecha para abrir espacio. Por eso la complejidad temporal total permanece cuadrática en el peor caso, aunque el número de comparaciones puede disminuir de forma importante.

### Comparación entre inserción clásica e inserción binaria

La siguiente animación ejecuta ambas variantes sobre el mismo arreglo. La columna **Pasos** permite observar cómo cambia el número de operaciones visibles cuando la posición de inserción se localiza mediante búsqueda lineal o mediante búsqueda binaria.

### Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento por inserción sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios.

- **Línea sólida** — simulación empírica (n ≤ 400, 5 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 50 000
- **Checkbox** — superpone la función teórica n²/4 normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva cuadrática es similar a la de burbuja, aunque con una constante menor que refleja que inserción hace menos movimientos en promedio.

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
    <tr><td>Mejor caso</td><td>\(n\)</td><td>\(\Omega(n)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(n^2/4\)</td><td>\(\Theta(n^2)\)</td></tr>
    <tr><td>Peor caso</td><td>\(n^2/2\)</td><td>\(O(n^2)\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio**: la simulación opera sobre arreglos aleatorios. El factor \(1/4\) (frente al \(1/2\) del peor caso) refleja que en promedio cada elemento recorre la mitad del subarreglo ya ordenado. El mejor caso \(\Omega(n)\) corresponde a un arreglo ya ordenado y no aplica aquí.

\[
f(n) = \frac{n^2}{4}
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_insercion/ordenamiento_insercion_1.png" alt="Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 1 de 4"><figcaption>Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_insercion/ordenamiento_insercion_4.png" alt="Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 2 de 4"><figcaption>Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 2 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_insercion/ordenamiento_insercion_7.png" alt="Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 3 de 4"><figcaption>Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 3 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_insercion/ordenamiento_insercion_11.png" alt="Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 4 de 4"><figcaption>Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 4 de 4.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../2-ordenamiento-seleccion/">← 8.3 Ordenamiento por selección</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../4-ordenamiento-shell/">Ampliación · Ordenamiento Shell →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
