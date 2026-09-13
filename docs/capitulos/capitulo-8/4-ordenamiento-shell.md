<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# Ampliación · Ordenamiento Shell

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/4_ordenamiento_shell.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ordenamiento Shell generaliza la idea del ordenamiento por inserción. En lugar de comparar solo elementos contiguos, primero compara elementos separados por un valor h determinado. Después reduce progresivamente ese valor h hasta llegar a 1, momento en el que realiza una pasada equivalente a inserción sobre un arreglo que ya quedó parcialmente organizado.

La ventaja práctica aparece porque los elementos pueden desplazarse grandes distancias durante las primeras pasadas. Cuando h se vuelve pequeño, el arreglo suele estar mucho más cerca de su posición final y las pasadas restantes requieren menos movimientos.

### Implementación

<!-- book-code:start -->

#### Shell con separaciones divididas entre dos

Implementación de ampliación del sitio (Java); no es un listado del PDF.

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemplo3bd6cf69710c {
        public void ordenar(int[] arr) {
            int n = arr.length;
            for (int paso = n / 2; paso > 0; paso /= 2) {
                for (int i = paso; i < n; i++) {
                    int clave = arr[i];
                    int j = i;
                    while (j >= paso && arr[j - paso] > clave) {
                        arr[j] = arr[j - paso];
                        j -= paso;
                    }
                    arr[j] = clave;
                }
            }
        }

        public static void main(String[] args) {
            int[] arr = Entradas.arreglo(args, 0, new int[] {3, 1, 2});

            System.out.println("Arreglo inicial: " + Arrays.toString(arr));
            new Ejemplo3bd6cf69710c().ordenar(arr);
            System.out.println("Arreglo ordenado: " + Arrays.toString(arr));
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función ordenar(arr)
        n ← longitud(arr)
        paso ← n div 2
        mientras paso > 0
            para i en rango(paso, n)
                clave ← arr[i]
                j ← i
                mientras j >= paso y arr[j - paso] > clave
                    arr[j] ← arr[j - paso]
                    j -= paso
                arr[j] ← clave
            paso //= 2
    ```

=== "Python"

    ```python
    def ordenar(arr):
        n = len(arr)
        paso = n // 2
        while paso > 0:
            for i in range(paso, n):
                clave = arr[i]
                j = i
                while j >= paso and arr[j - paso] > clave:
                    arr[j] = arr[j - paso]
                    j -= paso
                arr[j] = clave
            paso //= 2
    ```

=== "C"

    ```c
    void ordenar(int arr[], int n) {
        for (int paso = n / 2; paso > 0; paso /= 2) {
            for (int i = paso; i < n; i++) {
                int clave = arr[i];
                int j = i;
                while (j >= paso && arr[j - paso] > clave) {
                    arr[j] = arr[j - paso];
                    j -= paso;
                }
                arr[j] = clave;
            }
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, `n` indica la longitud del arreglo y se recibe como parámetro.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo que se modifica durante el ordenamiento. |
| `n` | Longitud del arreglo. |
| `paso` | Separación entre los elementos comparados. |
| `i` | Posición del elemento que se inserta. |
| `clave` | Valor del elemento que se inserta. |
| `j` | Posición actual durante los desplazamientos. |

**Precondiciones:** arr no nulo.

**Resultado:** Ordena arr de menor a mayor; admite el arreglo vacío.

**Explicación:** Esta implementación es una ampliación del sitio; el PDF proporcionado no incluye un listado de Shell.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>El navegador facilita la ejecución de código Java y Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Java ni Python; el código se ejecuta en tu navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-3bd6cf69710c">Lenguaje del ejemplo</label><select id="language-3bd6cf69710c" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemplo3bd6cf69710c" aria-label="Código Java · Shell con separaciones divididas entre dos"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemplo3bd6cf69710c</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">arr</span><span class="p">.</span><span class="na">length</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">for</span><span class="w"> </span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">paso</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="mi">2</span><span class="p">;</span><span class="w"> </span><span class="n">paso</span><span class="w"> </span><span class="o">&gt;</span><span class="w"> </span><span class="mi">0</span><span class="p">;</span><span class="w"> </span><span class="n">paso</span><span class="w"> </span><span class="o">/=</span><span class="w"> </span><span class="mi">2</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">for</span><span class="w"> </span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">i</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">paso</span><span class="p">;</span><span class="w"> </span><span class="n">i</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">n</span><span class="p">;</span><span class="w"> </span><span class="n">i</span><span class="o">++</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="kt">int</span><span class="w"> </span><span class="n">clave</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">arr</span><span class="o">[</span><span class="n">i</span><span class="o">]</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="kt">int</span><span class="w"> </span><span class="n">j</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">i</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="k">while</span><span class="w"> </span><span class="p">(</span><span class="n">j</span><span class="w"> </span><span class="o">&gt;=</span><span class="w"> </span><span class="n">paso</span><span class="w"> </span><span class="o">&amp;&amp;</span><span class="w"> </span><span class="n">arr</span><span class="o">[</span><span class="n">j</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">paso</span><span class="o">]</span><span class="w"> </span><span class="o">&gt;</span><span class="w"> </span><span class="n">clave</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">                    </span><span class="n">arr</span><span class="o">[</span><span class="n">j</span><span class="o">]</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">arr</span><span class="o">[</span><span class="n">j</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="n">paso</span><span class="o">]</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">                    </span><span class="n">j</span><span class="w"> </span><span class="o">-=</span><span class="w"> </span><span class="n">paso</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="n">arr</span><span class="o">[</span><span class="n">j</span><span class="o">]</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">clave</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span class="n">arr</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">arreglo</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="kt">int</span><span class="o">[]</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: arr" spellcheck="false" data-editable data-java-input="arr"><span class="p">{</span><span class="mi">3</span><span class="p">,</span><span class="w"> </span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">}</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Arreglo inicial: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">Arrays</span><span class="p">.</span><span class="na">toString</span><span class="p">(</span><span class="n">arr</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">new</span><span class="w"> </span><span class="n">Ejemplo3bd6cf69710c</span><span class="p">().</span><span class="na">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Arreglo ordenado: "</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">Arrays</span><span class="p">.</span><span class="na">toString</span><span class="p">(</span><span class="n">arr</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-3bd6cf69710c" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Shell con separaciones divididas entre dos"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="n">n</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="n">paso</span> <span class="o">=</span> <span class="n">n</span> <span class="o">//</span> <span class="mi">2</span></span><span class="python-code-line" data-code-line>    <span class="k">while</span> <span class="n">paso</span> <span class="o">&gt;</span> <span class="mi">0</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">paso</span><span class="p">,</span> <span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>            <span class="n">clave</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">i</span><span class="p">]</span></span><span class="python-code-line" data-code-line>            <span class="n">j</span> <span class="o">=</span> <span class="n">i</span></span><span class="python-code-line" data-code-line>            <span class="k">while</span> <span class="n">j</span> <span class="o">&gt;=</span> <span class="n">paso</span> <span class="ow">and</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span> <span class="o">-</span> <span class="n">paso</span><span class="p">]</span> <span class="o">&gt;</span> <span class="n">clave</span><span class="p">:</span></span><span class="python-code-line" data-code-line>                <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span> <span class="o">-</span> <span class="n">paso</span><span class="p">]</span></span><span class="python-code-line" data-code-line>                <span class="n">j</span> <span class="o">-=</span> <span class="n">paso</span></span><span class="python-code-line" data-code-line>            <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">=</span> <span class="n">clave</span></span><span class="python-code-line" data-code-line>        <span class="n">paso</span> <span class="o">//=</span> <span class="mi">2</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 15" spellcheck="false" data-editable><span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">3</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">]</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo inicial:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo ordenado:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

La animación y el contador son adaptaciones Python con operaciones instrumentadas. Incluyen comparaciones, movimientos y control del recorrido según el contador; no se deben interpretar todos los pasos como una sola clase de operación Java. Las opciones descendentes son ampliaciones: los listados del libro ordenan ascendentemente.

Shell es una ampliación digital y no tiene un listado correspondiente en este libro.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/core/sort/sort_algorithms.py).

<!-- book-code:end -->

### Complejidad

<div style="display:flex; justify-content:center; margin:1.2em 0;">
<table style="margin: 0 auto; text-align: center;">
  <thead>
    <tr>
      <th>Secuencia de h</th>
      <th>Mejor caso</th>
      <th>Caso promedio</th>
      <th>Peor caso</th>
      <th>Espacio</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Shell: n/2, n/4, ..., 1</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>Depende de los datos</td><td>\(O(n^2)\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Hibbard: \(2^k - 1\)</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>Depende de los datos</td><td>\(O(n^{3/2})\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Sedgewick</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>Depende de los datos</td><td>Aproximadamente \(O(n^{4/3})\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Pratt: \(2^i3^j\)</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>Depende de los datos</td><td>\(O(n \cdot \log_2^2(n))\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

Shell sort no tiene una única complejidad temporal fija, porque el número de comparaciones y movimientos depende directamente de la secuencia de h. Con la secuencia original propuesta por Shell, el peor caso sigue siendo cuadrático. Con secuencias mejor diseñadas, como Hibbard, Sedgewick o Pratt, el comportamiento mejora de forma importante.

La complejidad espacial se mantiene constante, ya que el algoritmo opera directamente sobre el arreglo original y solo necesita variables auxiliares para el valor actual de \(h\), los índices y el intercambio de valores.


---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo, la vista, el orden y la secuencia de h.
3. Use `Paso siguiente` para avanzar una comparación o intercambio a la vez.
4. Use `Ejecución automática` para observar toda la ejecución.
5. Cambie el campo `h` para comparar cómo se modifica el recorrido interno del algoritmo.

### Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento Shell sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios usando la secuencia original de Shell.

- **Línea sólida** — simulación empírica sobre varios tamaños de arreglo.
- **Línea discontinua** — extrapolación analítica para observar la tendencia cuando el tamaño crece.
- **Checkbox** — superpone una referencia cuadrática normalizada para la secuencia original.

La comparación experimental debe interpretarse como una referencia para la secuencia seleccionada en la implementación. El análisis formal cambia cuando se modifica la secuencia de h, por eso el resumen anterior separa Shell, Hibbard, Sedgewick y Pratt.

#### Tabla de resultados

La tabla muestra, para cada tamaño de arreglo \(n\) evaluado:

- **Operaciones teóricas** y **Tiempo teórico**: calculados con la función de referencia usada para la curva superpuesta.
- **Operaciones obtenidas** y **Tiempo experimental**: valores medidos por la simulación.
- **Error absoluto** y **Error relativo**: diferencia entre la referencia teórica escalada y los resultados obtenidos.

### Comparación de secuencias de h

La siguiente animación ejecuta Shell sort en paralelo sobre el mismo arreglo usando las secuencias Shell, Hibbard, Sedgewick y Pratt. La columna **Pasos** permite comparar cuántas operaciones visibles necesita cada técnica para completar el ordenamiento bajo las mismas condiciones iniciales.

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../3-ordenamiento-insercion/">← 8.4 Ordenamiento por inserción</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../5-ordenamiento-mezcla/">8.5 Ordenamiento por mezcla →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
