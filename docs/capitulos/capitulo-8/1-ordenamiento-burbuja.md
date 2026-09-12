<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# 8.2 Ordenamiento burbuja

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/1_ordenamiento_burbuja.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ordenamiento burbuja compara pares de elementos adyacentes e intercambia los que están en orden incorrecto. Repite este proceso hasta que no hay más intercambios. En cada pasada, el elemento mayor no ordenado queda en su posición final.

Es el algoritmo de ordenamiento más intuitivo pero también el menos eficiente en la práctica para arreglos grandes, con complejidad cuadrática en el caso promedio y peor caso.

### Implementación

<!-- book-code:start -->

#### Burbuja: versión básica

Implementación basada en el libro, página 321 (Java).

=== "Java"

    ```java
    public void ordenar(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
            for (int j = 0; j < arr.length - 1 - i; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función ordenar(arr)
        para i en rango(longitud(arr) - 1)
            para j en rango(longitud(arr) - 1 - i)
                si arr[j] > arr[j + 1] entonces
                    temp ← arr[j]
                    arr[j] ← arr[j + 1]
                    arr[j + 1] ← temp
    ```

=== "Python"

    ```python
    def ordenar(arr):
        for i in range(len(arr) - 1):
            for j in range(len(arr) - 1 - i):
                if arr[j] > arr[j + 1]:
                    temp = arr[j]
                    arr[j] = arr[j + 1]
                    arr[j + 1] = temp
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
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - 1 - i; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                }
            }
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, `n` indica la longitud del arreglo y se recibe como parámetro.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo de enteros que se modifica. |
| `i, j` | Contadores de pasadas y comparaciones. |
| `temp` | Auxiliar del intercambio. |
| `intercambiado` | Bandera de la versión con parada anticipada. |

**Precondiciones:** arr no nulo.

**Resultado:** Ordena el arreglo ascendentemente, en el mismo arreglo.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>El navegador facilita la ejecución de código Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Python; el código se ejecuta en tu navegador.</p><details><summary>Ver código y editar entradas</summary><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div id="runner-c5e3619ce0cd" class="python-code-editor highlight" aria-label="Código Python · Burbuja: versión básica"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span> <span class="o">-</span> <span class="mi">1</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span> <span class="o">-</span> <span class="mi">1</span> <span class="o">-</span> <span class="n">i</span><span class="p">):</span></span><span class="python-code-line" data-code-line>            <span class="k">if</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">&gt;</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]:</span></span><span class="python-code-line" data-code-line>                <span class="n">temp</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span></span><span class="python-code-line" data-code-line>                <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]</span></span><span class="python-code-line" data-code-line>                <span class="n">arr</span><span class="p">[</span><span class="n">j</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]</span> <span class="o">=</span> <span class="n">temp</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 10" spellcheck="false" data-editable><span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">3</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">]</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo inicial:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo ordenado:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span></span></code></pre></div></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Burbuja: versión con parada anticipada

Implementación basada en el libro, página 323 (Java).

=== "Java"

    ```java
    public void ordenar(int[] arr) {
        for (int i = arr.length - 1; i > 0; i--) {
            boolean intercambiado = false; // Bandera de control
            for (int j = 0; j < i; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    intercambiado = true;
                }
            }
            // El arreglo se considera ordenado
            if (!intercambiado)
                break;
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función ordenar(arr)
        para i en rango(longitud(arr) - 1, 0, -1)
            intercambiado ← falso
            para j en rango(i)
                si arr[j] > arr[j + 1] entonces
                    temp ← arr[j]
                    arr[j] ← arr[j + 1]
                    arr[j + 1] ← temp
                    intercambiado ← verdadero
            si no intercambiado entonces
                break
    ```

=== "Python"

    ```python
    def ordenar(arr):
        for i in range(len(arr) - 1, 0, -1):
            intercambiado = False
            for j in range(i):
                if arr[j] > arr[j + 1]:
                    temp = arr[j]
                    arr[j] = arr[j + 1]
                    arr[j + 1] = temp
                    intercambiado = True
            if not intercambiado:
                break
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
        for (int i = n - 1; i > 0; i--) {
            bool intercambiado = false; // Bandera de control
            for (int j = 0; j < i; j++) {
                if (arr[j] > arr[j + 1]) {
                    int temp = arr[j];
                    arr[j] = arr[j + 1];
                    arr[j + 1] = temp;
                    intercambiado = true;
                }
            }
            // El arreglo se considera ordenado
            if (!intercambiado) {
                break;
            }
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, `n` indica la longitud del arreglo y se recibe como parámetro.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo de enteros que se modifica. |
| `i, j` | Contadores de pasadas y comparaciones. |
| `temp` | Auxiliar del intercambio. |
| `intercambiado` | Bandera de la versión con parada anticipada. |

**Precondiciones:** arr no nulo.

**Resultado:** Ordena el arreglo ascendentemente, en el mismo arreglo.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>El navegador facilita la ejecución de código Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Python; el código se ejecuta en tu navegador.</p><details><summary>Ver código y editar entradas</summary><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div id="runner-17e3ea01be52" class="python-code-editor highlight" aria-label="Código Python · Burbuja: versión con parada anticipada"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span> <span class="o">-</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">0</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="n">intercambiado</span> <span class="o">=</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line>        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">i</span><span class="p">):</span></span><span class="python-code-line" data-code-line>            <span class="k">if</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">&gt;</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]:</span></span><span class="python-code-line" data-code-line>                <span class="n">temp</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span></span><span class="python-code-line" data-code-line>                <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]</span></span><span class="python-code-line" data-code-line>                <span class="n">arr</span><span class="p">[</span><span class="n">j</span> <span class="o">+</span> <span class="mi">1</span><span class="p">]</span> <span class="o">=</span> <span class="n">temp</span></span><span class="python-code-line" data-code-line>                <span class="n">intercambiado</span> <span class="o">=</span> <span class="kc">True</span></span><span class="python-code-line" data-code-line>        <span class="k">if</span> <span class="ow">not</span> <span class="n">intercambiado</span><span class="p">:</span></span><span class="python-code-line" data-code-line>            <span class="k">break</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 14" spellcheck="false" data-editable><span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">3</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">]</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo inicial:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo ordenado:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span></span></code></pre></div></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

La animación y el contador son adaptaciones Python con operaciones instrumentadas. Incluyen comparaciones, movimientos y control del recorrido según el contador; no se deben interpretar todos los pasos como una sola clase de operación Java. Las opciones descendentes son ampliaciones: los listados del libro ordenan ascendentemente.

La animación usa parada anticipada; se relaciona con la versión con bandera, no con la versión básica.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/core/sort/sort_algorithms.py).

<!-- book-code:end -->

### Complejidad

| Variante | Mejor caso | Caso promedio | Peor caso | Espacio auxiliar |
| --- | --- | --- | --- | --- |
| Básica, página 321 | \(\Theta(n^2)\) | \(\Theta(n^2)\) | \(\Theta(n^2)\) | \(\Theta(1)\) |
| Con bandera, página 323 | \(\Theta(n)\) | \(\Theta(n^2)\) | \(\Theta(n^2)\) | \(\Theta(1)\) |

La versión básica realiza \(n\cdot(n-1)/2\) comparaciones incluso si el arreglo ya está ordenado. La versión con bandera puede terminar tras una pasada sin intercambios. El resumen siguiente y la animación corresponden a la variante con parada anticipada.

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
4. Observe cómo el mayor elemento no ordenado migra hacia su posición final en cada pasada.

### Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento burbuja sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios.

- **Línea sólida** — simulación empírica (n ≤ 400, 5 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 50 000
- **Checkbox** — superpone la función teórica n²/2 normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva cuadrática crece rápidamente: duplicar n cuadruplica el número de operaciones.

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
    <tr><td>Caso promedio</td><td>\(n^2/2\)</td><td>\(\Theta(n^2)\)</td></tr>
    <tr><td>Peor caso</td><td>\(n \cdot (n-1)/2\)</td><td>\(O(n^2)\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio**: la simulación opera sobre arreglos en orden aleatorio. El mejor caso \(\Omega(n)\) corresponde a un arreglo ya ordenado y no aplica aquí.

\[
f(n) = \frac{n^2}{2}
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_burbuja/ordenamiento_burbuja_1.png" alt="Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 1 de 4"><figcaption>Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_burbuja/ordenamiento_burbuja_4.png" alt="Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 2 de 4"><figcaption>Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 2 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_burbuja/ordenamiento_burbuja_7.png" alt="Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 3 de 4"><figcaption>Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 3 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_burbuja/ordenamiento_burbuja_11.png" alt="Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 4 de 4"><figcaption>Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 4 de 4.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../0-comparacion-ordenamientos/">← 8.1 Comparación general</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../2-ordenamiento-seleccion/">8.3 Ordenamiento por selección →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
