<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.3 Complejidad lineal

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/3_complejidad_lineal.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: búsqueda secuencial en una lista

El ejemplo recorre la lista de izquierda a derecha hasta encontrar el objetivo o agotar la entrada. En el peor caso, el elemento no aparece y la función revisa todos los valores.

Cada elemento se evalúa una vez. Por eso el tiempo de ejecución observado tiende a crecer junto con la cantidad de datos.


---

### Código del libro asociado

<!-- book-code:start -->

#### Búsqueda secuencial iterativa

Implementación corregida basada en el libro, página 262 (Java).

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

??? example "Ejemplo paso a paso"
    Entrada: `arr = [4, 8, 12], x = 8`.

    **Prueba de escritorio**

    | Paso | Método | Profundidad | arr | x | i | Operación ejecutada | Retorno |
    | --- | --- | --- | --- | --- | --- | --- | --- |
    | 1 | buscar | 0 | [4, 8, 12] | 8 | — | Entrada a la llamada. | — |
    | 2 | buscar | 0 | [4, 8, 12] | 8 | 0 | `for i in range(len(arr)):` | — |
    | 3 | buscar | 0 | [4, 8, 12] | 8 | 0 | `if arr[i] == x:` | — |
    | 4 | buscar | 0 | [4, 8, 12] | 8 | 1 | `for i in range(len(arr)):` | — |
    | 5 | buscar | 0 | [4, 8, 12] | 8 | 1 | `if arr[i] == x:` | — |
    | 6 | buscar | 0 | [4, 8, 12] | 8 | 1 | `return True`; Termina la llamada. | true |

    Cada fila muestra el estado después de la operación indicada de la traducción Python de esta variante. «—» indica una variable aún no declarada en esa llamada o un retorno todavía pendiente. La profundidad inicial es 0; cada llamada anidada la incrementa en 1.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-dfd9f906a528">Código Python · Búsqueda secuencial iterativa</label><textarea id="runner-dfd9f906a528" spellcheck="false" wrap="off" rows="14">def buscar(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return True
    return False

# Entradas editables del ejemplo.
arr = [4, 8, 12]
x = 8

resultado = buscar(arr, x)
print(&quot;Resultado:&quot;, resultado)
</textarea></details><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Restablecer ejemplo</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

El listado Java procede de la página del libro indicada arriba. El laboratorio ejecuta una adaptación en Python; compara el patrón de crecimiento, no los tiempos de Java con los de Python.

El tiempo se promedia por ejecución; la preparación de las entradas se realiza antes de cronometrar. Las gráficas teóricas y las mediciones experimentales se identifican por separado.

El experimento busca n en [0, …, n−1], con resultado ausente y recorrido completo. La función del notebook devuelve un índice o −1; el Java devuelve boolean.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/runtime/complexity_animations.py).

<!-- book-code:end -->

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad lineal describe algoritmos cuyo costo crece de forma proporcional al tamaño de la entrada. Si la entrada tiene más elementos, el algoritmo puede necesitar más pasos en la misma proporción.

Este comportamiento aparece cuando el procedimiento debe inspeccionar cada elemento o avanzar secuencialmente hasta encontrar una condición. La forma del trabajo no cambia, pero se repite una vez por cada dato disponible.

Para una entrada de tamaño \(n\), una función de costo lineal puede expresarse como:

\[
T(n) = cn
\]

donde \(c\) representa el costo constante de procesar un elemento y \(n\) representa la cantidad de elementos de la entrada.

La expresión indica que el costo aumenta al mismo ritmo que la entrada. Si se duplican los elementos, el número esperado de operaciones también se duplica aproximadamente.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_lineal.png" alt="Representación gráfica de 2.1.2.3 complejidad lineal"><figcaption>Representación gráfica de 2.1.2.3 complejidad lineal.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../2-complejidad-logaritmica/">← 2.1.2.2 Complejidad logarítmica</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../4-complejidad-log-lineal/">2.1.2.4 Complejidad log-lineal →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
