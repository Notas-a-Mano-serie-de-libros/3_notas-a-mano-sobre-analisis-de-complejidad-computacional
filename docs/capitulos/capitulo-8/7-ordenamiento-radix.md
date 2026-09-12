<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# 8.7 Ordenamiento radix

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/7_ordenamiento_radix.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ordenamiento radix organiza enteros no negativos procesando sus dígitos de menor a mayor peso. En cada pasada distribuye los elementos en buckets según el dígito actual y luego reconstruye el arreglo conservando el orden relativo dentro de cada bucket.

La versión implementada aquí usa radix LSD en base 10. Su comportamiento depende de la cantidad de elementos `n`, de la cantidad de dígitos `d` del valor máximo y de la base `k` utilizada para los buckets.

### Implementación

<!-- book-code:start -->

#### Radix decimal para enteros con signo

Implementación basada en el libro, página 363 (Java).

=== "Java"

    ```java
    public void ordenar(int[] arr) {
        if (arr.length == 0)
            return;
        int min = Arrays.stream(arr).min().getAsInt();
        int max = Arrays.stream(arr).max().getAsInt();
        long rango = (long) max - min;
        int d = 1;
        while (rango >= 10) {
            rango /= 10;
            d++;
        }
        for (int i = 1; i <= d; i++)
            ordenarPorDigito(arr, i);
    }

    public void ordenarPorDigito(int[] arr, int i) {
        if (i < 1 || i > 10)
            throw new IllegalArgumentException("Dígito fuera del rango de int");
        if (arr.length == 0)
            return;
        int n = arr.length;
        int min = Arrays.stream(arr).min().getAsInt();
        long exp = 1;
        for (int j = 1; j < i; j++)
            exp *= 10;
        int[] conteo = new int[10];
        int[] salida = new int[n];
        for (int valor : arr)
            conteo[(int) (((long) valor - min) / exp % 10)]++;
        for (int j = 1; j < 10; j++)
            conteo[j] += conteo[j - 1];
        for (int j = n - 1; j >= 0; j--) {
            int d = (int) (((long) arr[j] - min) / exp % 10);
            salida[--conteo[d]] = arr[j];
        }
        System.arraycopy(salida, 0, arr, 0, n);
    }
    ```

=== "Pseudocódigo"

    ```text
    función ordenar(arr)
        si no arr entonces
            retornar
        minimo ← min(arr)
        maximo ← max(arr)
        rango ← maximo - minimo
        d ← 1
        mientras rango >= 10
            rango //= 10
            d += 1
        para i en rango(1, d + 1)
            ordenarPorDigito(arr, i)


    función ordenarPorDigito(arr, i)
        si no 1 <= i <= 10 entonces
            error ValueError("Dígito fuera del rango de int de Java")
        si no arr entonces
            retornar
        n ← longitud(arr)
        minimo ← min(arr)
        exp ← 1
        para j en rango(1, i)
            exp *= 10
        conteo ← [0] * 10
        salida ← [0] * n
        para valor en arr
            conteo[(valor - minimo) div exp % 10] += 1
        para j en rango(1, 10)
            conteo[j] += conteo[j - 1]
        para j en rango(n - 1, -1, -1)
            d ← (arr[j] - minimo) div exp % 10
            conteo[d] -= 1
            salida[conteo[d]] ← arr[j]
        arr[:] ← salida
    ```

=== "Python"

    ```python
    def ordenar(arr):
        if not arr:
            return
        minimo = min(arr)
        maximo = max(arr)
        rango = maximo - minimo
        d = 1
        while rango >= 10:
            rango //= 10
            d += 1
        for i in range(1, d + 1):
            ordenarPorDigito(arr, i)


    def ordenarPorDigito(arr, i):
        if not 1 <= i <= 10:
            raise ValueError("Dígito fuera del rango de int de Java")
        if not arr:
            return
        n = len(arr)
        minimo = min(arr)
        exp = 1
        for j in range(1, i):
            exp *= 10
        conteo = [0] * 10
        salida = [0] * n
        for valor in arr:
            conteo[(valor - minimo) // exp % 10] += 1
        for j in range(1, 10):
            conteo[j] += conteo[j - 1]
        for j in range(n - 1, -1, -1):
            d = (arr[j] - minimo) // exp % 10
            conteo[d] -= 1
            salida[conteo[d]] = arr[j]
        arr[:] = salida
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    void ordenarPorDigito(int arr[], int n, int i);

    void ordenar(int arr[], int n) {
        if (n == 0) {
            return;
        }
        int min = arr[0], max = arr[0];
        for (int j = 1; j < n; j++) {
            if (arr[j] < min) {
                min = arr[j];
            }
            if (arr[j] > max) {
                max = arr[j];
            }
        }
        int64_t rango = (int64_t) max - min;
        int d = 1;
        while (rango >= 10) {
            rango /= 10;
            d++;
        }
        for (int i = 1; i <= d; i++) {
            ordenarPorDigito(arr, n, i);
        }
    }

    void ordenarPorDigito(int arr[], int n, int i) {
        if (i < 1 || i > 10) {
            abort();
        }
        if (n == 0) {
            return;
        }
        int min = arr[0];
        for (int j = 1; j < n; j++) {
            if (arr[j] < min) {
                min = arr[j];
            }
        }
        int64_t exp = 1;
        for (int j = 1; j < i; j++) {
            exp *= 10;
        }
        int conteo[10] = {0};
        int *salida = malloc((size_t) n * sizeof(int));
        if (salida == NULL) {
            abort();
        }
        for (int j = 0; j < n; j++) {
            conteo[((int64_t) arr[j] - min) / exp % 10]++;
        }
        for (int j = 1; j < 10; j++) {
            conteo[j] += conteo[j - 1];
        }
        for (int j = n - 1; j >= 0; j--) {
            int d = (int) (((int64_t) arr[j] - min) / exp % 10);
            salida[--conteo[d]] = arr[j];
        }
        for (int j = 0; j < n; j++) {
            arr[j] = salida[j];
        }
        free(salida);
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, `n` indica la longitud del arreglo y se recibe como parámetro.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo que se modifica. |
| `max, d` | Máximo y cantidad de dígitos. |
| `i, exp` | Posición del dígito y potencia decimal calculada en long. |
| `conteo` | Diez buckets para los dígitos 0–9. |
| `salida` | Arreglo temporal de una pasada. |
| `min, max, d` | Extremos del arreglo y cantidad de dígitos del rango desplazado. |

**Precondiciones:** Arreglo no nulo de enteros, incluidos negativos. Se admite entrada vacía.

**Resultado:** Ordena enteros de todo el rango de int, incluidas entradas negativas y vacías, mediante claves desplazadas y pasadas estables.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>El navegador facilita la ejecución de código Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Python; el código se ejecuta en tu navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-96a3e8c5dc4e">Código Python · Radix decimal para enteros con signo</label><div class="python-code-editor"><div class="highlight" aria-hidden="true"><pre><code><span class="k">def</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">):</span>
    <span class="k">if</span> <span class="ow">not</span> <span class="n">arr</span><span class="p">:</span>
        <span class="k">return</span>
    <span class="n">minimo</span> <span class="o">=</span> <span class="nb">min</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span>
    <span class="n">maximo</span> <span class="o">=</span> <span class="nb">max</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span>
    <span class="n">rango</span> <span class="o">=</span> <span class="n">maximo</span> <span class="o">-</span> <span class="n">minimo</span>
    <span class="n">d</span> <span class="o">=</span> <span class="mi">1</span>
    <span class="k">while</span> <span class="n">rango</span> <span class="o">&gt;=</span> <span class="mi">10</span><span class="p">:</span>
        <span class="n">rango</span> <span class="o">//=</span> <span class="mi">10</span>
        <span class="n">d</span> <span class="o">+=</span> <span class="mi">1</span>
    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">d</span> <span class="o">+</span> <span class="mi">1</span><span class="p">):</span>
        <span class="n">ordenarPorDigito</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">i</span><span class="p">)</span>


<span class="k">def</span><span class="w"> </span><span class="nf">ordenarPorDigito</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span>
    <span class="k">if</span> <span class="ow">not</span> <span class="mi">1</span> <span class="o">&lt;=</span> <span class="n">i</span> <span class="o">&lt;=</span> <span class="mi">10</span><span class="p">:</span>
        <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s2">"Dígito fuera del rango de int de Java"</span><span class="p">)</span>
    <span class="k">if</span> <span class="ow">not</span> <span class="n">arr</span><span class="p">:</span>
        <span class="k">return</span>
    <span class="n">n</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span>
    <span class="n">minimo</span> <span class="o">=</span> <span class="nb">min</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span>
    <span class="n">exp</span> <span class="o">=</span> <span class="mi">1</span>
    <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="n">i</span><span class="p">):</span>
        <span class="n">exp</span> <span class="o">*=</span> <span class="mi">10</span>
    <span class="n">conteo</span> <span class="o">=</span> <span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">*</span> <span class="mi">10</span>
    <span class="n">salida</span> <span class="o">=</span> <span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">*</span> <span class="n">n</span>
    <span class="k">for</span> <span class="n">valor</span> <span class="ow">in</span> <span class="n">arr</span><span class="p">:</span>
        <span class="n">conteo</span><span class="p">[(</span><span class="n">valor</span> <span class="o">-</span> <span class="n">minimo</span><span class="p">)</span> <span class="o">//</span> <span class="n">exp</span> <span class="o">%</span> <span class="mi">10</span><span class="p">]</span> <span class="o">+=</span> <span class="mi">1</span>
    <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">10</span><span class="p">):</span>
        <span class="n">conteo</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">+=</span> <span class="n">conteo</span><span class="p">[</span><span class="n">j</span> <span class="o">-</span> <span class="mi">1</span><span class="p">]</span>
    <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">n</span> <span class="o">-</span> <span class="mi">1</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">):</span>
        <span class="n">d</span> <span class="o">=</span> <span class="p">(</span><span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">-</span> <span class="n">minimo</span><span class="p">)</span> <span class="o">//</span> <span class="n">exp</span> <span class="o">%</span> <span class="mi">10</span>
        <span class="n">conteo</span><span class="p">[</span><span class="n">d</span><span class="p">]</span> <span class="o">-=</span> <span class="mi">1</span>
        <span class="n">salida</span><span class="p">[</span><span class="n">conteo</span><span class="p">[</span><span class="n">d</span><span class="p">]]</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span>
    <span class="n">arr</span><span class="p">[:]</span> <span class="o">=</span> <span class="n">salida</span>

<span class="c1"># Entradas editables del ejemplo.</span>
<span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">21</span><span class="p">,</span> <span class="mi">13</span><span class="p">,</span> <span class="mi">12</span><span class="p">]</span>

<span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo inicial:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span>
<span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo ordenado:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span>
</code></pre></div><textarea id="runner-96a3e8c5dc4e" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" rows="14">def ordenar(arr):
    if not arr:
        return
    minimo = min(arr)
    maximo = max(arr)
    rango = maximo - minimo
    d = 1
    while rango &gt;= 10:
        rango //= 10
        d += 1
    for i in range(1, d + 1):
        ordenarPorDigito(arr, i)


def ordenarPorDigito(arr, i):
    if not 1 &lt;= i &lt;= 10:
        raise ValueError(&quot;Dígito fuera del rango de int de Java&quot;)
    if not arr:
        return
    n = len(arr)
    minimo = min(arr)
    exp = 1
    for j in range(1, i):
        exp *= 10
    conteo = [0] * 10
    salida = [0] * n
    for valor in arr:
        conteo[(valor - minimo) // exp % 10] += 1
    for j in range(1, 10):
        conteo[j] += conteo[j - 1]
    for j in range(n - 1, -1, -1):
        d = (arr[j] - minimo) // exp % 10
        conteo[d] -= 1
        salida[conteo[d]] = arr[j]
    arr[:] = salida

# Entradas editables del ejemplo.
arr = [21, 13, 12]

print(&quot;Arreglo inicial:&quot;, arr)
ordenar(arr)
print(&quot;Arreglo ordenado:&quot;, arr)
</textarea></div></details><div class="example-runner-actions"><button type="button" data-run><span class="button-icon" aria-hidden="true">▶</span><span>Ejecutar</span></button><button type="button" data-stop disabled><span class="button-icon" aria-hidden="true">■</span><span>Detener</span></button><button type="button" data-reset><span class="button-icon" aria-hidden="true">↻</span><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

La animación y el contador son adaptaciones Python con operaciones instrumentadas. Incluyen comparaciones, movimientos y control del recorrido según el contador; no se deben interpretar todos los pasos como una sola clase de operación Java. Las opciones descendentes son ampliaciones: los listados del libro ordenan ascendentemente.

El listado usa base decimal y desplaza las claves por el mínimo para admitir valores negativos. La adaptación del laboratorio puede representar esas claves de otra manera.

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
    <tr><td>Mejor caso</td><td>\(\Omega(d \cdot (n+k))\)</td><td>\(\Omega(n+k)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(\Theta(d \cdot (n+k))\)</td><td>\(\Theta(n+k)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(d \cdot (n+k))\)</td><td>\(O(n+k)\)</td></tr>
  </tbody>
</table>
</div>

En esta animación la base es fija, `k = 10`, por lo que el crecimiento se observa principalmente a través del número de elementos y la cantidad de dígitos procesados.


---

### Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento radix sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios de enteros no negativos.

- **Línea sólida** — simulación empírica.
- **Línea discontinua** — extrapolación analítica.
- **Checkbox** — superpone la función teórica asociada a \(d \cdot (n+k)\).

La gráfica usa el mismo formato de los análisis experimentales del capítulo 2 para mantener consistencia visual con el resto de la obra.

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../6-ordenamiento-rapido/">← 8.6 Ordenamiento rápido</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../ejercicios-propuestos/">8.9 Ejercicios propuestos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
