<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.5 Complejidad cuadrática

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/5_complejidad_cuadratica.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: recorrer una matriz

El ejemplo recorre todas las posiciones de una matriz. Si la matriz tiene \(n\) filas y \(n\) columnas, el cuerpo interno se ejecuta \(n \times n\) veces.

La estructura de dos ciclos anidados hace que el número de accesos crezca cuadráticamente con el tamaño lateral de la matriz.


---

### Código del libro asociado

<!-- book-code:start -->

#### Recorrido de una matriz rectangular

Implementación basada en el libro, página 153 (Java).

=== "Java"

    ```java
    import java.util.*;
    import java.math.*;
    import ejemplos.Entradas;

    public class Ejemploe73ca84ca782 {
        public static void imprimirMatriz(int[][] matriz) {
            int m = matriz.length;
            int n = m > 0 ? matriz[0].length : 0;
            for (int i = 0; i < m; i++) {
                for (int j = 0; j < n; j++) {
                    System.out.println(matriz[i][j]);
                }
                System.out.println();
            }
        }

        public static void main(String[] args) {
            int[][] matriz = Entradas.matriz(args, 0, new int[][] {{1, 2, 3}, {4, 5, 6}});

            Ejemploe73ca84ca782.imprimirMatriz(matriz);
            System.out.println("Ejemplo finalizado");
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función imprimirMatriz(matriz)
        m ← longitud(matriz)
        n ← longitud(matriz[0]) if m > 0 else 0
        para i en rango(m)
            para j en rango(n)
                imprimir(matriz[i][j])
            imprimir()
    ```

=== "Python"

    ```python
    def imprimirMatriz(matriz):
        m = len(matriz)
        n = len(matriz[0]) if m > 0 else 0
        for i in range(m):
            for j in range(n):
                print(matriz[i][j])
            print()
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    void imprimirMatriz(int m, int n, int matriz[m][n]) {
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                printf("%d\n", matriz[i][j]);
            }
            printf("\n");
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, las dimensiones se reciben como parámetros; las matrices de salida las reserva el llamador. La reserva de memoria se analiza por separado de los ciclos mostrados.

| Parámetro o variable | Significado |
| --- | --- |
| `matriz` | Matriz de enteros. |
| `m, n` | Cantidad de filas y columnas. |
| `i, j` | Índices de fila y columna. |

**Precondiciones:** Matriz no nula, con filas no nulas y todas de la misma longitud.

**Resultado:** Imprime los elementos y un salto al terminar cada fila.

??? example "Ejemplo paso a paso"
    Entrada: `matriz = [[1, 2, 3], [4, 5, 6]]`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `m = 2, n = 3` | Determina las dimensiones. |
    | `i = 0; j = 0, 1, 2` | Imprime 1, 2 y 3; después un salto. |
    | `i = 1; j = 0, 1, 2` | Imprime 4, 5 y 6; después un salto. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Java / Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga el entorno del lenguaje elegido en el navegador.</p><details><summary>Ver código y editar entradas</summary><label for="language-e73ca84ca782">Lenguaje del ejemplo</label><select id="language-e73ca84ca782" data-runner-language><option value="java">Java</option><option value="python">Python</option></select><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div class="python-code-editor highlight" data-language="java" data-java-class="Ejemploe73ca84ca782" aria-label="Código Java · Recorrido de una matriz rectangular"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">ejemplos.Entradas</span><span class="p">;</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Ejemploe73ca84ca782</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">imprimirMatriz</span><span class="p">(</span><span class="kt">int</span><span class="o">[][]</span><span class="w"> </span><span class="n">matriz</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">matriz</span><span class="p">.</span><span class="na">length</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">m</span><span class="w"> </span><span class="o">&gt;</span><span class="w"> </span><span class="mi">0</span><span class="w"> </span><span class="o">?</span><span class="w"> </span><span class="n">matriz</span><span class="o">[</span><span class="mi">0</span><span class="o">]</span><span class="p">.</span><span class="na">length</span><span class="w"> </span><span class="p">:</span><span class="w"> </span><span class="mi">0</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">for</span><span class="w"> </span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">i</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="mi">0</span><span class="p">;</span><span class="w"> </span><span class="n">i</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">m</span><span class="p">;</span><span class="w"> </span><span class="n">i</span><span class="o">++</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">for</span><span class="w"> </span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">j</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="mi">0</span><span class="p">;</span><span class="w"> </span><span class="n">j</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="n">n</span><span class="p">;</span><span class="w"> </span><span class="n">j</span><span class="o">++</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">                </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="n">matriz</span><span class="o">[</span><span class="n">i</span><span class="o">][</span><span class="n">j</span><span class="o">]</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">();</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="o">[][]</span><span class="w"> </span><span class="n">matriz</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Entradas</span><span class="p">.</span><span class="na">matriz</span><span class="p">(</span><span class="n">args</span><span class="p">,</span><span class="w"> </span><span class="mi">0</span><span class="p">,</span><span class="w"> </span><span class="k">new</span><span class="w"> </span><span class="kt">int</span><span class="o">[][]</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: matriz" spellcheck="false" data-editable data-java-input="matriz"><span class="p">{{</span><span class="mi">1</span><span class="p">,</span><span class="w"> </span><span class="mi">2</span><span class="p">,</span><span class="w"> </span><span class="mi">3</span><span class="p">},</span><span class="w"> </span><span class="p">{</span><span class="mi">4</span><span class="p">,</span><span class="w"> </span><span class="mi">5</span><span class="p">,</span><span class="w"> </span><span class="mi">6</span><span class="p">}}</span></span><span class="p">);</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">Ejemploe73ca84ca782</span><span class="p">.</span><span class="na">imprimirMatriz</span><span class="p">(</span><span class="n">matriz</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">"Ejemplo finalizado"</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-e73ca84ca782" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Recorrido de una matriz rectangular"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">imprimirMatriz</span><span class="p">(</span><span class="n">matriz</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="n">m</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">matriz</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="n">n</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">matriz</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span> <span class="k">if</span> <span class="n">m</span> <span class="o">&gt;</span> <span class="mi">0</span> <span class="k">else</span> <span class="mi">0</span></span><span class="python-code-line" data-code-line>    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">m</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>            <span class="nb">print</span><span class="p">(</span><span class="n">matriz</span><span class="p">[</span><span class="n">i</span><span class="p">][</span><span class="n">j</span><span class="p">])</span></span><span class="python-code-line" data-code-line>        <span class="nb">print</span><span class="p">()</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 10" spellcheck="false" data-editable><span class="n">matriz</span> <span class="o">=</span> <span class="p">[[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">],</span> <span class="p">[</span><span class="mi">4</span><span class="p">,</span> <span class="mi">5</span><span class="p">,</span> <span class="mi">6</span><span class="p">]]</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">imprimirMatriz</span><span class="p">(</span><span class="n">matriz</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Ejemplo finalizado"</span><span class="p">)</span></span></code></pre></div><p class="java-runtime-credit">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>. Las funciones auxiliares Entradas leen los valores del main.</p></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

El listado Java procede de la página del libro indicada arriba. El laboratorio ejecuta una adaptación en Python; compara el patrón de crecimiento, no los tiempos de Java con los de Python.

El tiempo se promedia por ejecución; la preparación de las entradas se realiza antes de cronometrar. Las gráficas teóricas y las mediciones experimentales se identifican por separado.

El laboratorio suma una matriz cuadrada; el listado del libro imprime una matriz rectangular. Ambos recorren las celdas. La medición omite la impresión y fija \(m = n\).

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/runtime/complexity_animations.py).

<!-- book-code:end -->

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad cuadrática describe algoritmos cuyo costo crece con el cuadrado del tamaño de entrada. Suele aparecer cuando dos ciclos anidados dependen de \(n\).

En estos casos, cada elemento puede relacionarse con muchos otros elementos, o se recorre una estructura bidimensional de tamaño \(n \times n\).

Para una entrada de tamaño \(n\), una función de costo cuadrático puede expresarse como:

\[
T(n) = cn^2
\]

donde \(c\) representa el costo constante de cada operación elemental y \(n^2\) representa la cantidad de combinaciones o posiciones evaluadas.

El crecimiento es mucho más rápido que el lineal: duplicar \(n\) puede multiplicar el trabajo aproximadamente por cuatro.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_cuadratica.png" alt="Representación gráfica de 2.1.2.5 complejidad cuadrática"><figcaption>Representación gráfica de 2.1.2.5 complejidad cuadrática.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../4-complejidad-log-lineal/">← 2.1.2.4 Complejidad log-lineal</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../6-complejidad-cubica/">2.1.2.6 Complejidad cúbica →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
