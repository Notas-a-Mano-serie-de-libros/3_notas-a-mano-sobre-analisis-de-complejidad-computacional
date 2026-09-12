<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>

# 7.2 Búsqueda secuencial

<span class="chapter-kicker">Capítulo 7</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/1_busqueda_secuencial.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

La búsqueda secuencial (o lineal) recorre el arreglo posición por posición, comparando cada elemento con el objetivo. No requiere que el arreglo esté ordenado; basta con acceder a los elementos en cualquier orden. Si el arreglo está ordenado, la búsqueda puede detenerse anticipadamente al encontrar un elemento mayor que el objetivo, aunque esto no mejora el peor caso.

### Implementación

<!-- book-code:start -->

#### Búsqueda secuencial iterativa

Implementación basada en el libro, página 262 (Java).

=== "Java"

    ```java
    public boolean buscar(int[] arr, int x) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == x)
                return true;
        }
        return false;
    }
    ```

=== "Pseudocódigo"

    ```text
    función buscar(arr, x)
        para i en rango(longitud(arr))
            si arr[i] == x entonces
                retornar verdadero
        retornar falso
    ```

=== "Python"

    ```python
    def buscar(arr, x):
        for i in range(len(arr)):
            if arr[i] == x:
                return True
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

    bool buscar(int arr[], int n, int x) {
        for (int i = 0; i < n; i++) {
            if (arr[i] == x) {
                return true;
            }
        }
        return false;
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, `n` indica la longitud del arreglo y se recibe como parámetro.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo de enteros. |
| `x` | Valor buscado. |
| `i` | Posición examinada. |

**Precondiciones:** arr no nulo; no requiere orden previo.

**Resultado:** Devuelve true si existe x y false si no existe.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>El navegador facilita la ejecución de código Python desde Pages. Puedes usar el ejemplo de forma remota, modificar sus entradas y ver los resultados sin instalar Python; el código se ejecuta en tu navegador.</p><details><summary>Ver código y editar entradas</summary><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div id="runner-dfd9f906a528" class="python-code-editor highlight" aria-label="Código Python · Búsqueda secuencial iterativa"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">x</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">arr</span><span class="p">)):</span></span><span class="python-code-line" data-code-line>        <span class="k">if</span> <span class="n">arr</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">==</span> <span class="n">x</span><span class="p">:</span></span><span class="python-code-line" data-code-line>            <span class="k">return</span> <span class="kc">True</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="kc">False</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 8" spellcheck="false" data-editable><span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">4</span><span class="p">,</span> <span class="mi">8</span><span class="p">,</span> <span class="mi">12</span><span class="p">]</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 9" spellcheck="false" data-editable><span class="n">x</span> <span class="o">=</span> <span class="mi">8</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">resultado</span> <span class="o">=</span> <span class="n">buscar</span><span class="p">(</span><span class="n">arr</span><span class="p">,</span> <span class="n">x</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Resultado:"</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span></span></code></pre></div></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

La animación ejecuta una adaptación Python y registra estados visuales; sus pasos de interfaz no equivalen necesariamente a comparaciones del Java. El contador de eficiencia usa búsquedas sobre un objetivo presente y promedia ensayos. El tiempo teórico se estima a partir de una operación calibrada; no es una medición del listado Java.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/core/search/search_metrics.py).

<!-- book-code:end -->

### Complejidad: versión iterativa y versión recursiva

La versión iterativa usa un ciclo que avanza desde la primera posición hasta encontrar el objetivo o agotar el arreglo. La versión recursiva reemplaza ese ciclo por llamadas sucesivas que revisan una posición y delegan el resto del recorrido a la siguiente llamada.

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
    <tr><td>Iterativa</td><td>Caso promedio</td><td>\(\Theta(n)\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Iterativa</td><td>Peor caso</td><td>\(O(n)\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Caso promedio</td><td>\(\Theta(n)\)</td><td>\(\Theta(n)\)</td></tr>
    <tr><td>Recursiva</td><td>Peor caso</td><td>\(O(n)\)</td><td>\(O(n)\)</td></tr>
  </tbody>
</table>
</div>

#### Versión iterativa

En la implementación iterativa, el algoritmo mantiene únicamente el índice de avance y algunas variables auxiliares constantes. El número de comparaciones depende de la posición del objetivo dentro del arreglo.

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
    <tr><td>Caso promedio</td><td>\(\Theta(n)\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(n)\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** El objetivo está en la primera posición. Se realiza una comparación y el recorrido termina de inmediato, por eso \(T(n) \in \Omega(1)\) y \(S(n) \in \Theta(1)\).
- **Caso promedio.** Si el objetivo puede aparecer con la misma probabilidad en cualquier posición, el algoritmo revisa aproximadamente la mitad del arreglo. El costo esperado es proporcional a \(n/2\), por lo que \(T(n) \in \Theta(n)\) y el espacio auxiliar permanece constante.
- **Peor caso.** El objetivo está en la última posición o está ausente. Se revisan las \(n\) posiciones, de modo que \(T(n) \in O(n)\) y \(S(n) \in O(1)\).

#### Versión recursiva (ampliación teórica)

El libro no incluye un listado recursivo de este algoritmo en las páginas citadas. Este apartado compara el costo de una posible formulación recursiva; no corresponde a otra implementación transcrita.

En la implementación recursiva, cada llamada representa la comparación de una posición. La cantidad de comparaciones se conserva, pero cada llamada queda registrada temporalmente en la pila de ejecución hasta que se alcanza el caso base.

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
    <tr><td>Caso promedio</td><td>\(\Theta(n)\)</td><td>\(\Theta(n)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(n)\)</td><td>\(O(n)\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** La primera llamada encuentra el objetivo. La pila contiene una cantidad constante de llamadas activas, así que el tiempo y el espacio son constantes.
- **Caso promedio.** La llamada exitosa suele aparecer alrededor de la mitad del arreglo. Se acumulan alrededor de \(n/2\) llamadas, por eso el tiempo y la pila crecen linealmente.
- **Peor caso.** La recursión avanza hasta la última posición o hasta el caso base de ausencia. Se realizan \(n\) comparaciones y se acumulan \(n\) niveles de pila, de modo que \(T(n) \in O(n)\) y \(S(n) \in O(n)\).



---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y si el objetivo debe estar presente o ausente.
3. Use el botón `Buscar` para ejecutar la animación paso a paso o de forma automática.
4. Observe cómo el algoritmo revisa cada posición en orden.

### Eficiencia por tamaño de arreglo

La siguiente celda simula la búsqueda secuencial sobre arreglos de tamaño creciente y mide el **número de operaciones** necesarias para encontrar el objetivo (siempre presente).

- **Línea sólida** — simulación empírica (n ≤ 5 000, 50 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 10 000 000
- **Checkbox** — superpone la función teórica n/2 normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva crece linealmente: duplicar n duplica el número de pasos.

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
    <tr><td>Caso promedio</td><td>\(n/2\)</td><td>\(\Theta(n)\)</td></tr>
    <tr><td>Peor caso</td><td>\(n\)</td><td>\(O(n)\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio**: la simulación busca un elemento siempre presente en una posición aleatoria uniforme, por lo que en promedio se recorre la mitad del arreglo. El mejor caso \(\Omega(1)\) es demasiado infrecuente para ser representativo.

\[
f(n) = \frac{n}{2}
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-7/busqueda_lineal/busqueda_lineal_ejemplo.png" alt="Secuencia visual de 7.2 búsqueda secuencial · paso representativo 1 de 4"><figcaption>Secuencia visual de 7.2 búsqueda secuencial · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_lineal/busqueda_lineal_ejemplo_mejor_caso.png" alt="Visualización del mejor caso de 7.2 búsqueda secuencial"><figcaption>Visualización del mejor caso de 7.2 búsqueda secuencial.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_lineal/busqueda_lineal_ejemplo_caso_promedio.png" alt="Visualización del caso promedio de 7.2 búsqueda secuencial"><figcaption>Visualización del caso promedio de 7.2 búsqueda secuencial.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_lineal/busqueda_lineal_ejemplo_peor_caso_2.png" alt="Visualización del peor caso de 7.2 búsqueda secuencial"><figcaption>Visualización del peor caso de 7.2 búsqueda secuencial.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-busquedas/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../0-comparacion-busquedas/">← 7.1 Comparación general</a><a class="section-step__index" href="../">Capítulo 7</a><a class="section-step__next" href="../2-busqueda-binaria/">7.3 Búsqueda binaria →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>
