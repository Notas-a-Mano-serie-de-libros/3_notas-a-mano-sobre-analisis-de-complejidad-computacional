<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# 8.3 Ordenamiento por selección

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/2_ordenamiento_seleccion.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ordenamiento por selección busca el elemento mínimo en el subarreglo no ordenado y lo coloca al inicio de ese subarreglo, expandiendo la parte ordenada en una posición con cada pasada. Siempre realiza el mismo número de comparaciones independientemente del orden inicial.

### Implementación

<!-- book-code:start -->

#### Selección: máximo hacia el extremo derecho

Implementación basada en el libro, página 327 (Java).

=== "Java"

    ```java
    public static void ordenar(int[] arr) {
        for (int i = 0; i < arr.length - 1; i++) {
             // Candidato inicial
            int max = 0;
            for (int j = 1; j < arr.length - i; j++) {
                if (arr[j] > arr[max]) { // Aplica el criterio
                    max = j;
                }
            }
            // Intercambia el candidato con el extremo derecho
            int temp = arr[max];
            arr[max] = arr[arr.length - 1 - i];
            arr[arr.length - 1 - i] = temp;
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función ordenar(arr)
        para i en rango(longitud(arr) - 1)
            max ← 0
            para j en rango(1, longitud(arr) - i)
                si arr[j] > arr[max] entonces
                    max ← j
            temp ← arr[max]
            arr[max] ← arr[longitud(arr) - 1 - i]
            arr[longitud(arr) - 1 - i] ← temp
    ```

=== "Python"

    ```python
    def ordenar(arr):
        for i in range(len(arr) - 1):
            max = 0
            for j in range(1, len(arr) - i):
                if arr[j] > arr[max]:
                    max = j
            temp = arr[max]
            arr[max] = arr[len(arr) - 1 - i]
            arr[len(arr) - 1 - i] = temp
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
             // Candidato inicial
            int max = 0;
            for (int j = 1; j < n - i; j++) {
                if (arr[j] > arr[max]) { // Aplica el criterio
                    max = j;
                }
            }
            // Intercambia el candidato con el extremo derecho
            int temp = arr[max];
            arr[max] = arr[n - 1 - i];
            arr[n - 1 - i] = temp;
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, `n` indica la longitud del arreglo y se recibe como parámetro.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo que se modifica. |
| `i` | Cantidad de posiciones finales fijadas. |
| `j, max` | Índice examinado e índice del máximo. |
| `temp` | Auxiliar de intercambio. |

**Precondiciones:** arr no nulo.

**Resultado:** Ordena el arreglo ascendentemente.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>El navegador facilita la ejecución de código Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Python; el código se ejecuta en tu navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-4990a158436a">Código Python · Selección: máximo hacia el extremo derecho</label><div class="python-code-editor"><div class="highlight" aria-hidden="true"><pre><code><span class="k">def</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">):</span>
    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span> <span class="o">-</span> <span class="mi">1</span><span class="p">):</span>
        <span class="nb">max</span> <span class="o">=</span> <span class="mi">0</span>
        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="nb">len</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span> <span class="o">-</span> <span class="n">i</span><span class="p">):</span>
            <span class="k">if</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">&gt;</span> <span class="n">arr</span><span class="p">[</span><span class="nb">max</span><span class="p">]:</span>
                <span class="nb">max</span> <span class="o">=</span> <span class="n">j</span>
        <span class="n">temp</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="nb">max</span><span class="p">]</span>
        <span class="n">arr</span><span class="p">[</span><span class="nb">max</span><span class="p">]</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="nb">len</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span> <span class="o">-</span> <span class="mi">1</span> <span class="o">-</span> <span class="n">i</span><span class="p">]</span>
        <span class="n">arr</span><span class="p">[</span><span class="nb">len</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span> <span class="o">-</span> <span class="mi">1</span> <span class="o">-</span> <span class="n">i</span><span class="p">]</span> <span class="o">=</span> <span class="n">temp</span>

<span class="c1"># Entradas editables del ejemplo.</span>
<span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">3</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">]</span>

<span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo inicial:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span>
<span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo ordenado:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span>
</code></pre></div><textarea id="runner-4990a158436a" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" rows="14">def ordenar(arr):
    for i in range(len(arr) - 1):
        max = 0
        for j in range(1, len(arr) - i):
            if arr[j] &gt; arr[max]:
                max = j
        temp = arr[max]
        arr[max] = arr[len(arr) - 1 - i]
        arr[len(arr) - 1 - i] = temp

# Entradas editables del ejemplo.
arr = [3, 1, 2]

print(&quot;Arreglo inicial:&quot;, arr)
ordenar(arr)
print(&quot;Arreglo ordenado:&quot;, arr)
</textarea></div></details><div class="example-runner-actions"><button type="button" data-run><span class="button-icon" aria-hidden="true">▶</span><span>Ejecutar</span></button><button type="button" data-stop disabled><span class="button-icon" aria-hidden="true">■</span><span>Detener</span></button><button type="button" data-reset><span class="button-icon" aria-hidden="true">↻</span><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Selección: mínimo y máximo en cada pasada

Implementación basada en el libro, página 329 (Java).

=== "Java"

    ```java
    public static void ordenar(int[] arr) {
        int a = 0, b = arr.length - 1;
        while (a < b) {
            int min = a, max = a;
            for (int j = a; j <= b; j++) {
                if (arr[j] < arr[min])
                    min = j;
                if (arr[j] > arr[max])
                    max = j;
            }
            // Intercambia el mínimo con el extremo izquierdo
            int temp = arr[a];
            arr[a] = arr[min];
            arr[min] = temp;
            if (max == a)
                max = min;
            // Intercambia el máximo con el extremo derecho
            temp = arr[b];
            arr[b] = arr[max];
            arr[max] = temp;
            a++;
            b--;
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función ordenar(arr)
        a ← 0
        b ← longitud(arr) - 1
        mientras a < b
            min ← a
            max ← a
            para j en rango(a, b + 1)
                si arr[j] < arr[min] entonces
                    min ← j
                si arr[j] > arr[max] entonces
                    max ← j
            temp ← arr[a]
            arr[a] ← arr[min]
            arr[min] ← temp
            si max == a entonces
                max ← min
            temp ← arr[b]
            arr[b] ← arr[max]
            arr[max] ← temp
            a += 1
            b -= 1
    ```

=== "Python"

    ```python
    def ordenar(arr):
        a = 0
        b = len(arr) - 1
        while a < b:
            min = a
            max = a
            for j in range(a, b + 1):
                if arr[j] < arr[min]:
                    min = j
                if arr[j] > arr[max]:
                    max = j
            temp = arr[a]
            arr[a] = arr[min]
            arr[min] = temp
            if max == a:
                max = min
            temp = arr[b]
            arr[b] = arr[max]
            arr[max] = temp
            a += 1
            b -= 1
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
        int a = 0, b = n - 1;
        while (a < b) {
            int min = a, max = a;
            for (int j = a; j <= b; j++) {
                if (arr[j] < arr[min]) {
                    min = j;
                }
                if (arr[j] > arr[max]) {
                    max = j;
                }
            }
            // Intercambia el mínimo con el extremo izquierdo
            int temp = arr[a];
            arr[a] = arr[min];
            arr[min] = temp;
            if (max == a) {
                max = min;
            }
            // Intercambia el máximo con el extremo derecho
            temp = arr[b];
            arr[b] = arr[max];
            arr[max] = temp;
            a++;
            b--;
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, `n` indica la longitud del arreglo y se recibe como parámetro.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo que se modifica. |
| `a, b` | Extremos del intervalo pendiente. |
| `min, max` | Índices del mínimo y máximo. |
| `j, temp` | Índice examinado y auxiliar de intercambio. |

**Precondiciones:** arr no nulo.

**Resultado:** Fija un mínimo a la izquierda y un máximo a la derecha.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>El navegador facilita la ejecución de código Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Python; el código se ejecuta en tu navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-31cc71510d45">Código Python · Selección: mínimo y máximo en cada pasada</label><div class="python-code-editor"><div class="highlight" aria-hidden="true"><pre><code><span class="k">def</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">):</span>
    <span class="n">a</span> <span class="o">=</span> <span class="mi">0</span>
    <span class="n">b</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span> <span class="o">-</span> <span class="mi">1</span>
    <span class="k">while</span> <span class="n">a</span> <span class="o">&lt;</span> <span class="n">b</span><span class="p">:</span>
        <span class="nb">min</span> <span class="o">=</span> <span class="n">a</span>
        <span class="nb">max</span> <span class="o">=</span> <span class="n">a</span>
        <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">b</span> <span class="o">+</span> <span class="mi">1</span><span class="p">):</span>
            <span class="k">if</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">arr</span><span class="p">[</span><span class="nb">min</span><span class="p">]:</span>
                <span class="nb">min</span> <span class="o">=</span> <span class="n">j</span>
            <span class="k">if</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">&gt;</span> <span class="n">arr</span><span class="p">[</span><span class="nb">max</span><span class="p">]:</span>
                <span class="nb">max</span> <span class="o">=</span> <span class="n">j</span>
        <span class="n">temp</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">a</span><span class="p">]</span>
        <span class="n">arr</span><span class="p">[</span><span class="n">a</span><span class="p">]</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="nb">min</span><span class="p">]</span>
        <span class="n">arr</span><span class="p">[</span><span class="nb">min</span><span class="p">]</span> <span class="o">=</span> <span class="n">temp</span>
        <span class="k">if</span> <span class="nb">max</span> <span class="o">==</span> <span class="n">a</span><span class="p">:</span>
            <span class="nb">max</span> <span class="o">=</span> <span class="nb">min</span>
        <span class="n">temp</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">b</span><span class="p">]</span>
        <span class="n">arr</span><span class="p">[</span><span class="n">b</span><span class="p">]</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="nb">max</span><span class="p">]</span>
        <span class="n">arr</span><span class="p">[</span><span class="nb">max</span><span class="p">]</span> <span class="o">=</span> <span class="n">temp</span>
        <span class="n">a</span> <span class="o">+=</span> <span class="mi">1</span>
        <span class="n">b</span> <span class="o">-=</span> <span class="mi">1</span>

<span class="c1"># Entradas editables del ejemplo.</span>
<span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">3</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">]</span>

<span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo inicial:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span>
<span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo ordenado:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span>
</code></pre></div><textarea id="runner-31cc71510d45" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" rows="14">def ordenar(arr):
    a = 0
    b = len(arr) - 1
    while a &lt; b:
        min = a
        max = a
        for j in range(a, b + 1):
            if arr[j] &lt; arr[min]:
                min = j
            if arr[j] &gt; arr[max]:
                max = j
        temp = arr[a]
        arr[a] = arr[min]
        arr[min] = temp
        if max == a:
            max = min
        temp = arr[b]
        arr[b] = arr[max]
        arr[max] = temp
        a += 1
        b -= 1

# Entradas editables del ejemplo.
arr = [3, 1, 2]

print(&quot;Arreglo inicial:&quot;, arr)
ordenar(arr)
print(&quot;Arreglo ordenado:&quot;, arr)
</textarea></div></details><div class="example-runner-actions"><button type="button" data-run><span class="button-icon" aria-hidden="true">▶</span><span>Ejecutar</span></button><button type="button" data-stop disabled><span class="button-icon" aria-hidden="true">■</span><span>Detener</span></button><button type="button" data-reset><span class="button-icon" aria-hidden="true">↻</span><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

La animación y el contador son adaptaciones Python con operaciones instrumentadas. Incluyen comparaciones, movimientos y control del recorrido según el contador; no se deben interpretar todos los pasos como una sola clase de operación Java. Las opciones descendentes son ampliaciones: los listados del libro ordenan ascendentemente.

La animación fija un extremo por pasada. La variante de mínimo y máximo del libro se presenta como comparación, no es la simulada por defecto.

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
    <tr><td>Mejor caso</td><td>\(\Omega(n^2)\)</td><td>\(\Omega(1)\)</td></tr>
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
4. Observe cómo se selecciona el mínimo del subarreglo no ordenado y se ubica al frente.

### Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento por selección sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios.

- **Línea sólida** — simulación empírica (n ≤ 400, 5 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 50 000
- **Checkbox** — superpone la función teórica n(n−1)/2 normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva es casi idéntica entre ejecuciones porque el número de comparaciones es determinístico.

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
    <tr><td>Mejor caso</td><td>\(n \cdot (n-1)/2\)</td><td>\(\Omega(n^2)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(n \cdot (n-1)/2\)</td><td>\(\Theta(n^2)\)</td></tr>
    <tr><td>Peor caso</td><td>\(n \cdot (n-1)/2\)</td><td>\(O(n^2)\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa la **función exacta para todos los escenarios**: selección siempre recorre el subarreglo completo para encontrar el mínimo sin importar el orden inicial, por lo que los tres casos comparten el mismo conteo de comparaciones.

\[
f(n) = \frac{n \cdot (n-1)}{2}
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_seleccion/ordenamiento_seleccion_1.png" alt="Secuencia visual de 8.3 ordenamiento por selección · paso representativo 1 de 4"><figcaption>Secuencia visual de 8.3 ordenamiento por selección · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_seleccion/ordenamiento_seleccion_4.png" alt="Secuencia visual de 8.3 ordenamiento por selección · paso representativo 2 de 4"><figcaption>Secuencia visual de 8.3 ordenamiento por selección · paso representativo 2 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_seleccion/ordenamiento_seleccion_7.png" alt="Secuencia visual de 8.3 ordenamiento por selección · paso representativo 3 de 4"><figcaption>Secuencia visual de 8.3 ordenamiento por selección · paso representativo 3 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_seleccion/ordenamiento_seleccion_11.png" alt="Secuencia visual de 8.3 ordenamiento por selección · paso representativo 4 de 4"><figcaption>Secuencia visual de 8.3 ordenamiento por selección · paso representativo 4 de 4.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../1-ordenamiento-burbuja/">← 8.2 Ordenamiento burbuja</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../3-ordenamiento-insercion/">8.4 Ordenamiento por inserción →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
