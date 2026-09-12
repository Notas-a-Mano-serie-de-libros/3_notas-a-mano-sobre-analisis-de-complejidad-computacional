<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# 8.6 Ordenamiento rápido

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/6_ordenamiento_rapido.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ordenamiento rápido (quicksort) elige un elemento pivote y reorganiza el arreglo para que todos los elementos menores queden a su izquierda y los mayores a su derecha. Luego ordena recursivamente cada partición.

La partición puede realizarse mediante distintos esquemas. **Hoare** usa dos índices que avanzan desde extremos opuestos e intercambia pares ubicados en el lado incorrecto. **Lomuto** recorre el subarreglo en una dirección, mantiene el límite de los elementos que deben quedar antes del pivote y coloca el pivote en su posición definitiva al finalizar la pasada. La selección del pivote también puede variar: inicio, medio, fin, aleatorio, mediana de tres y mediana de medianas. La mediana de tres toma los valores ubicados al inicio, al centro y al final del subarreglo, y usa como pivote el valor central entre esos tres. La mediana de medianas divide el subarreglo en grupos pequeños, calcula la mediana de cada grupo y luego usa la mediana de esas medianas como pivote.

En el caso promedio logra O(n log(n)) con una constante menor que el ordenamiento por mezcla, lo que lo hace el algoritmo de propósito general más rápido en la práctica. El peor caso es O(n²) y ocurre cuando el pivote divide el arreglo de forma muy asimétrica.

### Implementación

<!-- book-code:start -->

#### Ordenamiento rápido con pivote inicial

Implementación basada en el libro, página 349 (Java).

=== "Java"

    ```java
    public void ordenar(int[] arr, int a, int b) {
        if (a >= b)
            return;
        int p = particionar(arr, a, b);
        ordenar(arr, a, p - 1);
        ordenar(arr, p + 1, b);
    }
    public int particionar(int[] arr, int a, int b) {
        int pivote = arr[a], i = a + 1, j = b;
        while (i <= j) {
            while (i <= j && arr[i] < pivote)
                i++;
            while (i <= j && arr[j] > pivote)
                j--;
            if (i <= j) {
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
                i++;
                j--;
            }
        }
        int temp = arr[a];
        arr[a] = arr[j];
        arr[j] = temp;
        return j;
    }
    ```

=== "Pseudocódigo"

    ```text
    función ordenar(arr, a, b)
        si a >= b entonces
            retornar
        p ← particionar(arr, a, b)
        ordenar(arr, a, p - 1)
        ordenar(arr, p + 1, b)


    función particionar(arr, a, b)
        pivote ← arr[a]
        i ← a + 1
        j ← b
        mientras i <= j
            mientras i <= j y arr[i] < pivote
                i += 1
            mientras i <= j y arr[j] > pivote
                j -= 1
            si i <= j entonces
                temp ← arr[i]
                arr[i] ← arr[j]
                arr[j] ← temp
                i += 1
                j -= 1
        temp ← arr[a]
        arr[a] ← arr[j]
        arr[j] ← temp
        retornar j
    ```

=== "Python"

    ```python
    def ordenar(arr, a, b):
        if a >= b:
            return
        p = particionar(arr, a, b)
        ordenar(arr, a, p - 1)
        ordenar(arr, p + 1, b)


    def particionar(arr, a, b):
        pivote = arr[a]
        i = a + 1
        j = b
        while i <= j:
            while i <= j and arr[i] < pivote:
                i += 1
            while i <= j and arr[j] > pivote:
                j -= 1
            if i <= j:
                temp = arr[i]
                arr[i] = arr[j]
                arr[j] = temp
                i += 1
                j -= 1
        temp = arr[a]
        arr[a] = arr[j]
        arr[j] = temp
        return j
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    int particionar(int arr[], int a, int b);

    void ordenar(int arr[], int a, int b) {
        if (a >= b) {
            return;
        }
        int p = particionar(arr, a, b);
        ordenar(arr, a, p - 1);
        ordenar(arr, p + 1, b);
    }
    int particionar(int arr[], int a, int b) {
        int pivote = arr[a], i = a + 1, j = b;
        while (i <= j) {
            while (i <= j && arr[i] < pivote) {
                i++;
            }
            while (i <= j && arr[j] > pivote) {
                j--;
            }
            if (i <= j) {
                int temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
                i++;
                j--;
            }
        }
        int temp = arr[a];
        arr[a] = arr[j];
        arr[j] = temp;
        return j;
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo que se modifica. |
| `a, b` | Extremos inclusivos del intervalo. |
| `p` | Posición final del pivote. |
| `pivote` | Valor original arr[a]. |
| `i, j` | Índices que recorren la partición. |
| `temp` | Auxiliar de intercambio. |

**Precondiciones:** arr no nulo; intervalo válido o vacío.

**Resultado:** Ordena arr[a..b] ascendentemente.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>El navegador facilita la ejecución de código Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Python; el código se ejecuta en tu navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-bd4876eac9d6">Código Python · Ordenamiento rápido con pivote inicial</label><div class="python-code-editor"><div class="highlight" aria-hidden="true"><pre><code><span class="k">def</span><span class="w"> </span><span class="nf">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">):</span>
    <span class="k">if</span> <span class="n">a</span> <span class="o">&gt;=</span> <span class="n">b</span><span class="p">:</span>
        <span class="k">return</span>
    <span class="n">p</span> <span class="o">=</span> <span class="n">particionar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span>
    <span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">p</span> <span class="o">-</span> <span class="mi">1</span><span class="p">)</span>
    <span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">p</span> <span class="o">+</span> <span class="mi">1</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span>


<span class="k">def</span><span class="w"> </span><span class="nf">particionar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">):</span>
    <span class="n">pivote</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">a</span><span class="p">]</span>
    <span class="n">i</span> <span class="o">=</span> <span class="n">a</span> <span class="o">+</span> <span class="mi">1</span>
    <span class="n">j</span> <span class="o">=</span> <span class="n">b</span>
    <span class="k">while</span> <span class="n">i</span> <span class="o">&lt;=</span> <span class="n">j</span><span class="p">:</span>
        <span class="k">while</span> <span class="n">i</span> <span class="o">&lt;=</span> <span class="n">j</span> <span class="ow">and</span> <span class="n">arr</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">&lt;</span> <span class="n">pivote</span><span class="p">:</span>
            <span class="n">i</span> <span class="o">+=</span> <span class="mi">1</span>
        <span class="k">while</span> <span class="n">i</span> <span class="o">&lt;=</span> <span class="n">j</span> <span class="ow">and</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">&gt;</span> <span class="n">pivote</span><span class="p">:</span>
            <span class="n">j</span> <span class="o">-=</span> <span class="mi">1</span>
        <span class="k">if</span> <span class="n">i</span> <span class="o">&lt;=</span> <span class="n">j</span><span class="p">:</span>
            <span class="n">temp</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">i</span><span class="p">]</span>
            <span class="n">arr</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span>
            <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">=</span> <span class="n">temp</span>
            <span class="n">i</span> <span class="o">+=</span> <span class="mi">1</span>
            <span class="n">j</span> <span class="o">-=</span> <span class="mi">1</span>
    <span class="n">temp</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">a</span><span class="p">]</span>
    <span class="n">arr</span><span class="p">[</span><span class="n">a</span><span class="p">]</span> <span class="o">=</span> <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span>
    <span class="n">arr</span><span class="p">[</span><span class="n">j</span><span class="p">]</span> <span class="o">=</span> <span class="n">temp</span>
    <span class="k">return</span> <span class="n">j</span>

<span class="c1"># Entradas editables del ejemplo.</span>
<span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">3</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">]</span>
<span class="n">a</span> <span class="o">=</span> <span class="mi">0</span>
<span class="n">b</span> <span class="o">=</span> <span class="mi">2</span>

<span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo inicial:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span>
<span class="n">ordenar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">a</span><span class="p">,</span> <span class="n">b</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">"Arreglo ordenado:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">)</span>
</code></pre></div><textarea id="runner-bd4876eac9d6" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" rows="14">def ordenar(arr, a, b):
    if a &gt;= b:
        return
    p = particionar(arr, a, b)
    ordenar(arr, a, p - 1)
    ordenar(arr, p + 1, b)


def particionar(arr, a, b):
    pivote = arr[a]
    i = a + 1
    j = b
    while i &lt;= j:
        while i &lt;= j and arr[i] &lt; pivote:
            i += 1
        while i &lt;= j and arr[j] &gt; pivote:
            j -= 1
        if i &lt;= j:
            temp = arr[i]
            arr[i] = arr[j]
            arr[j] = temp
            i += 1
            j -= 1
    temp = arr[a]
    arr[a] = arr[j]
    arr[j] = temp
    return j

# Entradas editables del ejemplo.
arr = [3, 1, 2]
a = 0
b = 2

print(&quot;Arreglo inicial:&quot;, arr)
ordenar(arr, a, b)
print(&quot;Arreglo ordenado:&quot;, arr)
</textarea></div></details><div class="example-runner-actions"><button type="button" data-run><span class="button-icon" aria-hidden="true">▶</span><span>Ejecutar</span></button><button type="button" data-stop disabled><span class="button-icon" aria-hidden="true">■</span><span>Detener</span></button><button type="button" data-reset><span class="button-icon" aria-hidden="true">↻</span><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

La animación y el contador son adaptaciones Python con operaciones instrumentadas. Incluyen comparaciones, movimientos y control del recorrido según el contador; no se deben interpretar todos los pasos como una sola clase de operación Java. Las opciones descendentes son ampliaciones: los listados del libro ordenan ascendentemente.

El laboratorio ofrece particiones Hoare y Lomuto y varias elecciones de pivote. El listado del libro fija `pivote = arr[a]`; la configuración predeterminada del laboratorio usa pivote medio y no reproduce la misma partición paso a paso.

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
    <tr><td>Mejor caso</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>\(\Omega(\log_2(n))\)</td></tr>
    <tr><td>Caso promedio</td><td>\(\Theta(n \cdot \log_2(n))\)</td><td>\(\Theta(\log_2(n))\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(n^2)\)</td><td>\(O(n)\)</td></tr>
  </tbody>
</table>
</div>

Este resumen presenta los resultados generales. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.


---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo, el orden, el esquema de partición y la estrategia de selección del pivote.
3. Use `Paso siguiente` o `Ejecución automática` para recorrer la animación.
4. Observe cómo cada esquema reorganiza el mismo tipo de subarreglo y genera las particiones recursivas.

### Comparación entre Hoare y Lomuto

Ambos esquemas producen particiones válidas para quicksort, aunque recorren y modifican el arreglo de manera diferente. Hoare inicia con dos índices fuera del intervalo activo: \(i\) avanza desde la izquierda hasta encontrar un valor que pertenece al lado derecho y \(j\) retrocede desde la derecha hasta encontrar uno que pertenece al lado izquierdo. Mientras \(i<j\), ambos elementos se intercambian. Cuando los índices se cruzan, \(j\) define el límite entre las dos particiones.

Lomuto mueve primero el pivote al extremo final. El índice \(j\) examina cada elemento y el índice \(i\) conserva el límite de la región cuyos valores deben quedar antes del pivote. Cada valor que satisface la relación con el pivote se intercambia con el elemento situado en \(i\); al terminar el recorrido, el pivote se coloca en esa frontera.

La siguiente animación ejecuta ambos esquemas en paralelo sobre el mismo arreglo, con el pivote tomado de la posición media. La columna **Pasos** permite comparar la cantidad de estados visibles que requiere cada estrategia. Esta medición incluye comparaciones e intercambios mostrados por la animación y permite observar la diferencia operativa entre los recorridos.

### Comparación entre estrategias de pivote

La selección del pivote modifica la forma en que se dividen los subarreglos. Cuando el pivote queda cerca del centro de los valores, las particiones tienden a ser más equilibradas y el recorrido recursivo reduce su profundidad. Cuando el pivote queda cerca de un extremo, una partición puede concentrar casi todos los elementos y el número de pasos aumenta.

La siguiente animación permite elegir el esquema de partición y compara, sobre el mismo arreglo, las estrategias de pivote usadas por la simulación: inicio, medio, fin, aleatorio, mediana de tres y mediana de medianas. La columna **Pasos** muestra cuántos estados visibles requiere cada estrategia para completar el ordenamiento con la misma configuración de orden y partición.

### Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento rápido sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios (caso promedio).

- **Línea sólida** — simulación empírica (n ≤ 2 000, 5 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 1 000 000
- **Checkbox** — superpone la función teórica n·log₂(n) normalizada

El gráfico usa escala logarítmica en ambos ejes. En arreglos aleatorios la constante práctica suele ser menor que la del ordenamiento por mezcla, lo que lo hace preferido en la práctica.

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
    <tr><td>Peor caso</td><td>\(n^2\)</td><td>\(O(n^2)\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio**: la simulación usa pivote aleatorio sobre arreglos aleatorios, condición bajo la cual las particiones son suficientemente equilibradas. El peor caso \(O(n^2)\) —pivote siempre mínimo o máximo— no se observa en condiciones normales.

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
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_rapido/ordenamiento_rapido_1.png" alt="Secuencia visual de 8.6 ordenamiento rápido · paso representativo 1 de 4"><figcaption>Secuencia visual de 8.6 ordenamiento rápido · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_rapido/ordenamiento_rapido_4.png" alt="Secuencia visual de 8.6 ordenamiento rápido · paso representativo 2 de 4"><figcaption>Secuencia visual de 8.6 ordenamiento rápido · paso representativo 2 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_rapido/ordenamiento_rapido_7.png" alt="Secuencia visual de 8.6 ordenamiento rápido · paso representativo 3 de 4"><figcaption>Secuencia visual de 8.6 ordenamiento rápido · paso representativo 3 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_rapido/ordenamiento_rapido_11.png" alt="Secuencia visual de 8.6 ordenamiento rápido · paso representativo 4 de 4"><figcaption>Secuencia visual de 8.6 ordenamiento rápido · paso representativo 4 de 4.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../5-ordenamiento-mezcla/">← 8.5 Ordenamiento por mezcla</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../7-ordenamiento-radix/">8.7 Ordenamiento radix →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
