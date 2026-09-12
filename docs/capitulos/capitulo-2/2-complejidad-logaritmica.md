<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.2 Complejidad logarítmica

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/2_complejidad_logaritmica.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: búsqueda binaria en una lista ordenada

El ejemplo implementa una búsqueda binaria iterativa. En cada vuelta se calcula la posición media del rango activo y se compara el valor encontrado con el objetivo.

Si el valor central no es el buscado, la mitad que no puede contener la respuesta se descarta. La lista completa puede ser muy grande, pero el algoritmo solo conserva dos límites: `bajo` y `alto`. Esa reducción sucesiva explica el comportamiento logarítmico.


---

### Código del libro asociado

<!-- book-code:start -->

#### Búsqueda binaria iterativa

Implementación corregida basada en el libro, página 268 (Java).

=== "Java"

    ```java
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

??? example "Ejemplo paso a paso"
    Entrada: `arr = [1, 3, 5, 7, 9], a = 0, b = 4, x = 7`.

    **Prueba de escritorio**

    | Paso | Método | Profundidad | arr | a | b | x | m | Operación ejecutada | Retorno |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 1 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | — | Entrada a la llamada. | — |
    | 2 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | — | `while a <= b:` | — |
    | 3 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | 2 | `m = a + (b - a) // 2` | — |
    | 4 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | 2 | `if arr[m] == x:` | — |
    | 5 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | 2 | `if x > arr[m]:` | — |
    | 6 | buscar | 0 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 2 | `a = m + 1` | — |
    | 7 | buscar | 0 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 2 | `while a <= b:` | — |
    | 8 | buscar | 0 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 3 | `m = a + (b - a) // 2` | — |
    | 9 | buscar | 0 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 3 | `if arr[m] == x:` | — |
    | 10 | buscar | 0 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 3 | `return True`; Termina la llamada. | true |

    Cada fila muestra el estado después de la operación indicada de la traducción Python de esta variante. «—» indica una variable aún no declarada en esa llamada o un retorno todavía pendiente. La profundidad inicial es 0; cada llamada anidada la incrementa en 1.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-e7872d7f0991">Código Python · Búsqueda binaria iterativa</label><textarea id="runner-e7872d7f0991" spellcheck="false" wrap="off" rows="14">def buscar(arr, a, b, x):
    while a &lt;= b:
        m = a + (b - a) // 2
        if arr[m] == x:
            return True
        if x &gt; arr[m]:
            a = m + 1
        else:
            b = m - 1
    return False

# Entradas editables del ejemplo.
arr = [1, 3, 5, 7, 9]
a = 0
b = 4
x = 7

resultado = buscar(arr, a, b, x)
print(&quot;Resultado:&quot;, resultado)
</textarea></details><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Restablecer ejemplo</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

El listado Java procede de la página del libro indicada arriba. El laboratorio ejecuta una adaptación en Python; compara el patrón de crecimiento, no los tiempos de Java con los de Python.

El tiempo se promedia por ejecución; la preparación de las entradas se realiza antes de cronometrar. Las gráficas teóricas y las mediciones experimentales se identifican por separado.

El experimento busca n en el arreglo [0, …, n−1], por lo que mide una búsqueda binaria sin éxito. La función del notebook devuelve una posición o −1; el listado Java devuelve boolean.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/runtime/complexity_animations.py).

<!-- book-code:end -->

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad logarítmica describe algoritmos cuyo costo crece muy lentamente frente al tamaño de la entrada. En lugar de revisar todos los elementos, el algoritmo reduce el espacio de búsqueda en una fracción significativa en cada paso.

Este comportamiento aparece cuando cada decisión descarta una parte grande del problema. Por ejemplo, en una lista ordenada, la búsqueda binaria compara contra el elemento central y conserva únicamente la mitad donde todavía puede estar el valor buscado.

Por esa razón, aumentar mucho el tamaño de la entrada no produce un aumento proporcional en el número de pasos: duplicar n normalmente añade solo una decisión adicional.

Para una entrada de tamaño \(n\), una función de costo logarítmico puede expresarse como:

\[
T(n) = c \cdot \log_2(n)
\]

donde \(T(n)\) representa el costo de ejecución, \(c\) representa el costo constante de cada comparación o decisión, y \(\log_2(n)\) representa la cantidad aproximada de veces que la entrada puede dividirse entre dos.

La base del logaritmo no cambia la familia de crecimiento. En general, una función logarítmica puede expresarse como \(\log_\ell(n)\), donde \(\ell\) es la base del logaritmo. Si se desea expresar ese logaritmo usando otra base \(b\), se aplica el cambio de base:

\[
\log_\ell(n) = \frac{\log_b(n)}{\log_b(\ell)}
\]

El término \(\frac{1}{\log_b(\ell)}\) es una constante multiplicativa. Por eso, \(\log_2(n)\), \(\log_{10}(n)\) y \(\log_e(n)\) crecen con la misma forma general: cambian de escala vertical, pero pertenecen a la misma familia logarítmica.

La expresión muestra que el costo crece por niveles de división. Si \(n\) pasa de \(1.000\) a \(1.000.000\), el crecimiento no sigue la diferencia entre esos tamaños, sino la cantidad de divisiones necesarias para reducir el rango hasta encontrar o descartar el elemento.

Una característica especialmente importante de esta familia es que crece extremadamente lento. Incluso cuando el tamaño de entrada alcanza valores enormes, el número de pasos logarítmicos permanece manejable. Por ejemplo, si \(n=10^{100}\), entonces:

\[
\log_2(10^{100}) = 100 \cdot \log_2(10) \approx 332.19
\]

Esto significa que una entrada con cien órdenes de magnitud puede reducirse, en un modelo logarítmico base dos, a poco más de trescientas decisiones teóricas. Encontrar soluciones de orden constante suele ser una tarea bastante complicada, porque exige que el costo no dependa del tamaño de la entrada. Cuando eso no es posible, la siguiente mejor opción práctica suelen ser las soluciones logarítmicas: todavía dependen de \(n\), pero lo hacen de una manera muy lenta.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_logaritmica.png" alt="Representación gráfica de 2.1.2.2 complejidad logarítmica"><figcaption>Representación gráfica de 2.1.2.2 complejidad logarítmica.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../1-complejidad-constante/">← 2.1.2.1 Complejidad constante</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../3-complejidad-lineal/">2.1.2.3 Complejidad lineal →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
