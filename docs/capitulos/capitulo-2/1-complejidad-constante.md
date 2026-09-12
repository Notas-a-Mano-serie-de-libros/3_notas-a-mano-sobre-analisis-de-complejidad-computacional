<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.1 Complejidad constante

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/1_complejidad_constante.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: acceder a una posición de un arreglo

El ejemplo implementa el acceso a una posición específica de una lista o arreglo. En el listado del libro, `arr` representa el arreglo e `i` la posición que se desea consultar.

El acceso por índice tiene comportamiento constante porque la posición del elemento se calcula directamente. La ejecución requiere conocer la referencia inicial de la estructura y el desplazamiento asociado al índice. Con esa información, el entorno de ejecución puede ubicar el elemento solicitado mediante una operación directa de acceso.

La lista puede contener muchos elementos, pero el acceso a `arr[i]` consulta una sola posición. La operación realizada para leer el elemento central de una lista de 100 posiciones tiene la misma forma que la operación realizada para leer el elemento central de una lista de 1.000.000 de posiciones: se identifica un índice válido y se recupera el dato ubicado en esa posición.

La diferencia entre listas pequeñas y grandes aparece en otras operaciones, como construir la lista, recorrerla completa, copiarla o buscar un valor desconocido. En cambio, cuando el índice ya está determinado, el acceso se concentra en una única ubicación.


---

### Código del libro asociado

<!-- book-code:start -->

#### Acceso directo a un elemento

Implementación basada en el libro, página 148 (Java).

=== "Java"

    ```java
    arr[i]; //Accede al elemento i del arreglo "arr"
    m[i][j]; //Accede al elemento i,j del de la matriz "m"
    ```

=== "Pseudocódigo"

    ```text
    arr[i]  # Acceso al elemento i del arreglo.
    m[i][j]  # Acceso al elemento i, j de la matriz.
    ```

=== "Python"

    ```python
    arr[i]  # Acceso al elemento i del arreglo.
    m[i][j]  # Acceso al elemento i, j de la matriz.
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    arr[i];  // Acceso al elemento i del arreglo.
    m[i][j];  // Acceso al elemento i, j de la matriz.
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `arr, m` | Arreglo y matriz de entrada. |
| `i, j` | Índices válidos, comenzando en cero. |

**Precondiciones:** Estructuras no nulas e índices dentro de sus dimensiones.

**Resultado:** Lee un elemento; son expresiones de acceso, no métodos completos.

??? example "Ejemplo paso a paso"
    Entrada: `arr = [4, 8, 12], i = 1`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `i = 1` | Identifica la segunda posición. |
    | `arr[i]` | El valor leído es 8. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Ver código y editar entradas</summary><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div id="runner-dd0399c316f2" class="python-code-editor highlight" aria-label="Código Python · Acceso directo a un elemento"><pre><code><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 1" spellcheck="false" data-editable><span class="n">arr</span> <span class="o">=</span> <span class="p">[</span><span class="mi">4</span><span class="p">,</span> <span class="mi">8</span><span class="p">,</span> <span class="mi">12</span><span class="p">]</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 2" spellcheck="false" data-editable><span class="n">i</span> <span class="o">=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 3" spellcheck="false" data-editable><span class="n">m</span> <span class="o">=</span> <span class="p">[[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">],</span> <span class="p">[</span><span class="mi">3</span><span class="p">,</span> <span class="mi">4</span><span class="p">]]</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 4" spellcheck="false" data-editable><span class="n">j</span> <span class="o">=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">arr</span><span class="p">[</span><span class="n">i</span><span class="p">]</span>  <span class="c1"># Acceso al elemento i del arreglo.</span></span><span class="python-code-line" data-code-line><span class="n">m</span><span class="p">[</span><span class="n">i</span><span class="p">][</span><span class="n">j</span><span class="p">]</span>  <span class="c1"># Acceso al elemento i, j de la matriz.</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"arr[i]:"</span><span class="p">,</span> <span class="n">arr</span><span class="p">[</span><span class="n">i</span><span class="p">])</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"m[i][j]:"</span><span class="p">,</span> <span class="n">m</span><span class="p">[</span><span class="n">i</span><span class="p">][</span><span class="n">j</span><span class="p">])</span></span></code></pre></div></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

El listado Java procede de la página del libro indicada arriba. El laboratorio ejecuta una adaptación en Python; compara el patrón de crecimiento, no los tiempos de Java con los de Python.

El tiempo se promedia por ejecución; la preparación de las entradas se realiza antes de cronometrar. Las gráficas teóricas y las mediciones experimentales se identifican por separado.

El experimento consulta una posición; la estructura de entrada ya existe antes de medir.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/runtime/constant_animation.py).

<!-- book-code:end -->

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo entre \(10^0\) y ese máximo se divide en múltiples tamaños para conservar la curva experimental, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor mostrado en la tabla y en la figura es el promedio de esas repeticiones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones y las fluctuaciones aleatorias pierden influencia. Esto no obliga al valor experimental a coincidir exactamente con la constante teórica, pero permite observar con mayor claridad que no existe una tendencia de crecimiento asociada a \(n\).

#### Complejidad temporal experimental

### Detalle teórico

La complejidad constante describe operaciones cuyo costo permanece estable frente a cambios en el tamaño de la entrada. El tamaño de la entrada se representa con \(n\) y suele indicar la cantidad de elementos disponibles para procesar: por ejemplo, la longitud de una lista, la cantidad de registros en una tabla o el número de posiciones de un arreglo.

Una operación de costo constante realiza una cantidad fija de acciones elementales. Esa cantidad puede ser pequeña o grande, dependiendo de la operación concreta y de la máquina que la ejecuta, pero conserva una característica esencial: al aumentar \(n\), el procedimiento ejecutado mantiene la misma estructura y la misma cantidad básica de trabajo.

Este tipo de comportamiento aparece en instrucciones puntuales como leer una variable, asignar un valor, comparar dos datos simples o acceder a una posición conocida dentro de una estructura con acceso directo.

Para una entrada de tamaño \(n\), una función de costo constante puede expresarse como:

\[
T(n) = c
\]

donde \(T(n)\) representa el costo de ejecutar la operación sobre una entrada de tamaño \(n\), y \(c\) representa una cantidad fija de trabajo. Ese valor puede interpretarse como tiempo, número de instrucciones, número de accesos a memoria o cualquier unidad de medición definida para el análisis.

La expresión \(T(n)=c\) indica que el costo se mantiene en el mismo nivel para diferentes valores de \(n\). Si \(n=10\), \(n=10.000\) o \(n=10.000.000\), el modelo teórico asigna el mismo costo a la operación estudiada.

Esto ocurre cuando el algoritmo llega directamente a la información requerida. La operación evaluada tiene una ruta de ejecución fija: recibe la entrada, identifica la posición o dato requerido, realiza la acción y termina. El número total de elementos disponibles modifica el tamaño de la estructura, pero la operación puntual sigue ocupando el mismo lugar dentro del proceso.

En una gráfica, una función constante se representa mediante una línea horizontal. La altura de esa línea corresponde al valor de \(c\). Si la línea está más arriba, la operación tarda más en términos absolutos; si está más abajo, tarda menos. En ambos casos, el rasgo importante es la ausencia de crecimiento sostenido al aumentar \(n\).

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_constante.png" alt="Representación gráfica de 2.1.2.1 complejidad constante"><figcaption>Representación gráfica de 2.1.2.1 complejidad constante.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../0-complejidad-sublineal/">← 2.1.2.0 Complejidad sublineal</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../2-complejidad-logaritmica/">2.1.2.2 Complejidad logarítmica →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
