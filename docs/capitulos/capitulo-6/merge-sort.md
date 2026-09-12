<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 4 · Ordenamiento por mezcla

<span class="chapter-kicker">Capítulo 6</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

#### Código

<!-- book-code:start -->

##### Ordenamiento por mezcla y combinación

Implementación corregida basada en el libro, página 247 (Java).

=== "Java"

    ```java
    public void ordenar(int[] arr, int a, int b) {
        if (a >= b)
            return;
        int m = a + (b - a) / 2;
        ordenar(arr, a, m);
        ordenar(arr, m + 1, b);
        combinar(arr, a, m, b);
    }
    public void combinar(int[] arr, int a, int m, int b) {
        int[] izquierda = Arrays.copyOfRange(arr, a, m + 1);
        int[] derecha = Arrays.copyOfRange(arr, m + 1, b + 1);
        int i = 0, j = 0, k = a;
        while (i < izquierda.length && j < derecha.length) {
            if (izquierda[i] <= derecha[j])
                arr[k++] = izquierda[i++];
            else
                arr[k++] = derecha[j++];
        }
        while (i < izquierda.length)
            arr[k++] = izquierda[i++];
        while (j < derecha.length)
            arr[k++] = derecha[j++];
    }
    ```

=== "Pseudocódigo"

    ```text
    función ordenar(arr, a, b)
        si a >= b entonces
            retornar
        m ← a + (b - a) div 2
        ordenar(arr, a, m)
        ordenar(arr, m + 1, b)
        combinar(arr, a, m, b)


    función combinar(arr, a, m, b)
        izquierda ← arr[a:m + 1]
        derecha ← arr[m + 1:b + 1]
        i ← 0
        j ← 0
        k ← a
        mientras i < longitud(izquierda) y j < longitud(derecha)
            si izquierda[i] <= derecha[j] entonces
                arr[k] ← izquierda[i]
                i += 1
            si no
                arr[k] ← derecha[j]
                j += 1
            k += 1
        mientras i < longitud(izquierda)
            arr[k] ← izquierda[i]
            i += 1
            k += 1
        mientras j < longitud(derecha)
            arr[k] ← derecha[j]
            j += 1
            k += 1
    ```

=== "Python"

    ```python
    def ordenar(arr, a, b):
        if a >= b:
            return
        m = a + (b - a) // 2
        ordenar(arr, a, m)
        ordenar(arr, m + 1, b)
        combinar(arr, a, m, b)


    def combinar(arr, a, m, b):
        izquierda = arr[a:m + 1]
        derecha = arr[m + 1:b + 1]
        i = 0
        j = 0
        k = a
        while i < len(izquierda) and j < len(derecha):
            if izquierda[i] <= derecha[j]:
                arr[k] = izquierda[i]
                i += 1
            else:
                arr[k] = derecha[j]
                j += 1
            k += 1
        while i < len(izquierda):
            arr[k] = izquierda[i]
            i += 1
            k += 1
        while j < len(derecha):
            arr[k] = derecha[j]
            j += 1
            k += 1
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    void combinar(int arr[], int a, int m, int b);

    void ordenar(int arr[], int a, int b) {
        if (a >= b) {
            return;
        }
        int m = a + (b - a) / 2;
        ordenar(arr, a, m);
        ordenar(arr, m + 1, b);
        combinar(arr, a, m, b);
    }

    void combinar(int arr[], int a, int m, int b) {
        int ni = m - a + 1;
        int nd = b - m;
        int *izquierda = malloc((size_t) ni * sizeof(int));
        int *derecha = malloc((size_t) nd * sizeof(int));
        if (izquierda == NULL || derecha == NULL) {
            free(izquierda);
            free(derecha);
            abort();
        }
        for (int i = 0; i < ni; i++) {
            izquierda[i] = arr[a + i];
        }
        for (int j = 0; j < nd; j++) {
            derecha[j] = arr[m + 1 + j];
        }
        int i = 0, j = 0, k = a;
        while (i < ni && j < nd) {
            if (izquierda[i] <= derecha[j]) {
                arr[k++] = izquierda[i++];
            } else {
                arr[k++] = derecha[j++];
            }
        }
        while (i < ni) {
            arr[k++] = izquierda[i++];
        }
        while (j < nd) {
            arr[k++] = derecha[j++];
        }
        free(izquierda);
        free(derecha);
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo que se modifica. |
| `a, b` | Extremos inclusivos del intervalo. |
| `m` | Índice que separa las mitades. |
| `izquierda, derecha` | Copias temporales de las mitades. |
| `i, j, k` | Índices dentro de las copias y del destino. |

**Precondiciones:** arr no nulo; intervalo válido o vacío. Importar java.util.Arrays.

**Resultado:** Ordena arr[a..b] en orden ascendente; no devuelve un arreglo nuevo.

??? example "Ejemplo paso a paso"
    Entrada: `arr = [3, 1, 2], a = 0, b = 2`.

    **Prueba de escritorio**

    | Paso | Método | Profundidad | arr | a | b | m | izquierda | derecha | i | j | k | Operación ejecutada | Retorno |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 1 | ordenar | 0 | [3, 1, 2] | 0 | 2 | — | — | — | — | — | — | Entrada a la llamada. | — |
    | 2 | ordenar | 0 | [3, 1, 2] | 0 | 2 | — | — | — | — | — | — | `if a >= b:` | — |
    | 3 | ordenar | 0 | [3, 1, 2] | 0 | 2 | 1 | — | — | — | — | — | `m = a + (b - a) // 2` | — |
    | 4 | ordenar | 1 | [3, 1, 2] | 0 | 1 | — | — | — | — | — | — | Entrada a la llamada. | — |
    | 5 | ordenar | 1 | [3, 1, 2] | 0 | 1 | — | — | — | — | — | — | `if a >= b:` | — |
    | 6 | ordenar | 1 | [3, 1, 2] | 0 | 1 | 0 | — | — | — | — | — | `m = a + (b - a) // 2` | — |
    | 7 | ordenar | 2 | [3, 1, 2] | 0 | 0 | — | — | — | — | — | — | Entrada a la llamada. | — |
    | 8 | ordenar | 2 | [3, 1, 2] | 0 | 0 | — | — | — | — | — | — | `if a >= b:` | — |
    | 9 | ordenar | 2 | [3, 1, 2] | 0 | 0 | — | — | — | — | — | — | `return`; Termina la llamada. | sin valor |
    | 10 | ordenar | 1 | [3, 1, 2] | 0 | 1 | 0 | — | — | — | — | — | `ordenar(arr, a, m)` | — |
    | 11 | ordenar | 2 | [3, 1, 2] | 1 | 1 | — | — | — | — | — | — | Entrada a la llamada. | — |
    | 12 | ordenar | 2 | [3, 1, 2] | 1 | 1 | — | — | — | — | — | — | `if a >= b:` | — |
    | 13 | ordenar | 2 | [3, 1, 2] | 1 | 1 | — | — | — | — | — | — | `return`; Termina la llamada. | sin valor |
    | 14 | ordenar | 1 | [3, 1, 2] | 0 | 1 | 0 | — | — | — | — | — | `ordenar(arr, m + 1, b)` | — |
    | 15 | combinar | 2 | [3, 1, 2] | 0 | 1 | 0 | — | — | — | — | — | Entrada a la llamada. | — |
    | 16 | combinar | 2 | [3, 1, 2] | 0 | 1 | 0 | [3] | — | — | — | — | `izquierda = arr[a:m + 1]` | — |
    | 17 | combinar | 2 | [3, 1, 2] | 0 | 1 | 0 | [3] | [1] | — | — | — | `derecha = arr[m + 1:b + 1]` | — |
    | 18 | combinar | 2 | [3, 1, 2] | 0 | 1 | 0 | [3] | [1] | 0 | — | — | `i = 0` | — |
    | 19 | combinar | 2 | [3, 1, 2] | 0 | 1 | 0 | [3] | [1] | 0 | 0 | — | `j = 0` | — |
    | 20 | combinar | 2 | [3, 1, 2] | 0 | 1 | 0 | [3] | [1] | 0 | 0 | 0 | `k = a` | — |
    | 21 | combinar | 2 | [3, 1, 2] | 0 | 1 | 0 | [3] | [1] | 0 | 0 | 0 | `while i < len(izquierda) and j < len(derecha):` | — |
    | 22 | combinar | 2 | [3, 1, 2] | 0 | 1 | 0 | [3] | [1] | 0 | 0 | 0 | `if izquierda[i] <= derecha[j]:` | — |
    | 23 | combinar | 2 | [1, 1, 2] | 0 | 1 | 0 | [3] | [1] | 0 | 0 | 0 | `arr[k] = derecha[j]` | — |
    | 24 | combinar | 2 | [1, 1, 2] | 0 | 1 | 0 | [3] | [1] | 0 | 1 | 0 | `j += 1` | — |
    | 25 | combinar | 2 | [1, 1, 2] | 0 | 1 | 0 | [3] | [1] | 0 | 1 | 1 | `k += 1` | — |
    | 26 | combinar | 2 | [1, 1, 2] | 0 | 1 | 0 | [3] | [1] | 0 | 1 | 1 | `while i < len(izquierda) and j < len(derecha):` | — |
    | 27 | combinar | 2 | [1, 1, 2] | 0 | 1 | 0 | [3] | [1] | 0 | 1 | 1 | `while i < len(izquierda):` | — |
    | 28 | combinar | 2 | [1, 3, 2] | 0 | 1 | 0 | [3] | [1] | 0 | 1 | 1 | `arr[k] = izquierda[i]` | — |
    | 29 | combinar | 2 | [1, 3, 2] | 0 | 1 | 0 | [3] | [1] | 1 | 1 | 1 | `i += 1` | — |
    | 30 | combinar | 2 | [1, 3, 2] | 0 | 1 | 0 | [3] | [1] | 1 | 1 | 2 | `k += 1` | — |
    | 31 | combinar | 2 | [1, 3, 2] | 0 | 1 | 0 | [3] | [1] | 1 | 1 | 2 | `while i < len(izquierda):` | — |
    | 32 | combinar | 2 | [1, 3, 2] | 0 | 1 | 0 | [3] | [1] | 1 | 1 | 2 | `while j < len(derecha):`; Termina la llamada. | sin valor |
    | 33 | ordenar | 1 | [1, 3, 2] | 0 | 1 | 0 | — | — | — | — | — | `combinar(arr, a, m, b)`; Termina la llamada. | sin valor |
    | 34 | ordenar | 0 | [1, 3, 2] | 0 | 2 | 1 | — | — | — | — | — | `ordenar(arr, a, m)` | — |
    | 35 | ordenar | 1 | [1, 3, 2] | 2 | 2 | — | — | — | — | — | — | Entrada a la llamada. | — |
    | 36 | ordenar | 1 | [1, 3, 2] | 2 | 2 | — | — | — | — | — | — | `if a >= b:` | — |
    | 37 | ordenar | 1 | [1, 3, 2] | 2 | 2 | — | — | — | — | — | — | `return`; Termina la llamada. | sin valor |
    | 38 | ordenar | 0 | [1, 3, 2] | 0 | 2 | 1 | — | — | — | — | — | `ordenar(arr, m + 1, b)` | — |
    | 39 | combinar | 1 | [1, 3, 2] | 0 | 2 | 1 | — | — | — | — | — | Entrada a la llamada. | — |
    | 40 | combinar | 1 | [1, 3, 2] | 0 | 2 | 1 | [1, 3] | — | — | — | — | `izquierda = arr[a:m + 1]` | — |
    | 41 | combinar | 1 | [1, 3, 2] | 0 | 2 | 1 | [1, 3] | [2] | — | — | — | `derecha = arr[m + 1:b + 1]` | — |
    | 42 | combinar | 1 | [1, 3, 2] | 0 | 2 | 1 | [1, 3] | [2] | 0 | — | — | `i = 0` | — |
    | 43 | combinar | 1 | [1, 3, 2] | 0 | 2 | 1 | [1, 3] | [2] | 0 | 0 | — | `j = 0` | — |
    | 44 | combinar | 1 | [1, 3, 2] | 0 | 2 | 1 | [1, 3] | [2] | 0 | 0 | 0 | `k = a` | — |
    | 45 | combinar | 1 | [1, 3, 2] | 0 | 2 | 1 | [1, 3] | [2] | 0 | 0 | 0 | `while i < len(izquierda) and j < len(derecha):` | — |
    | 46 | combinar | 1 | [1, 3, 2] | 0 | 2 | 1 | [1, 3] | [2] | 0 | 0 | 0 | `if izquierda[i] <= derecha[j]:` | — |
    | 47 | combinar | 1 | [1, 3, 2] | 0 | 2 | 1 | [1, 3] | [2] | 0 | 0 | 0 | `arr[k] = izquierda[i]` | — |
    | 48 | combinar | 1 | [1, 3, 2] | 0 | 2 | 1 | [1, 3] | [2] | 1 | 0 | 0 | `i += 1` | — |
    | 49 | combinar | 1 | [1, 3, 2] | 0 | 2 | 1 | [1, 3] | [2] | 1 | 0 | 1 | `k += 1` | — |
    | 50 | combinar | 1 | [1, 3, 2] | 0 | 2 | 1 | [1, 3] | [2] | 1 | 0 | 1 | `while i < len(izquierda) and j < len(derecha):` | — |
    | 51 | combinar | 1 | [1, 3, 2] | 0 | 2 | 1 | [1, 3] | [2] | 1 | 0 | 1 | `if izquierda[i] <= derecha[j]:` | — |
    | 52 | combinar | 1 | [1, 2, 2] | 0 | 2 | 1 | [1, 3] | [2] | 1 | 0 | 1 | `arr[k] = derecha[j]` | — |
    | 53 | combinar | 1 | [1, 2, 2] | 0 | 2 | 1 | [1, 3] | [2] | 1 | 1 | 1 | `j += 1` | — |
    | 54 | combinar | 1 | [1, 2, 2] | 0 | 2 | 1 | [1, 3] | [2] | 1 | 1 | 2 | `k += 1` | — |
    | 55 | combinar | 1 | [1, 2, 2] | 0 | 2 | 1 | [1, 3] | [2] | 1 | 1 | 2 | `while i < len(izquierda) and j < len(derecha):` | — |
    | 56 | combinar | 1 | [1, 2, 2] | 0 | 2 | 1 | [1, 3] | [2] | 1 | 1 | 2 | `while i < len(izquierda):` | — |
    | 57 | combinar | 1 | [1, 2, 3] | 0 | 2 | 1 | [1, 3] | [2] | 1 | 1 | 2 | `arr[k] = izquierda[i]` | — |
    | 58 | combinar | 1 | [1, 2, 3] | 0 | 2 | 1 | [1, 3] | [2] | 2 | 1 | 2 | `i += 1` | — |
    | 59 | combinar | 1 | [1, 2, 3] | 0 | 2 | 1 | [1, 3] | [2] | 2 | 1 | 3 | `k += 1` | — |
    | 60 | combinar | 1 | [1, 2, 3] | 0 | 2 | 1 | [1, 3] | [2] | 2 | 1 | 3 | `while i < len(izquierda):` | — |
    | 61 | combinar | 1 | [1, 2, 3] | 0 | 2 | 1 | [1, 3] | [2] | 2 | 1 | 3 | `while j < len(derecha):`; Termina la llamada. | sin valor |
    | 62 | ordenar | 0 | [1, 2, 3] | 0 | 2 | 1 | — | — | — | — | — | `combinar(arr, a, m, b)`; Termina la llamada. | sin valor |

    Cada fila muestra el estado después de la operación indicada de la traducción Python de esta variante. «—» indica una variable aún no declarada en esa llamada o un retorno todavía pendiente. La profundidad inicial es 0; cada llamada anidada la incrementa en 1.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-e32ce151575f">Código Python · Ordenamiento por mezcla y combinación</label><textarea id="runner-e32ce151575f" spellcheck="false" wrap="off" rows="14">def ordenar(arr, a, b):
    if a &gt;= b:
        return
    m = a + (b - a) // 2
    ordenar(arr, a, m)
    ordenar(arr, m + 1, b)
    combinar(arr, a, m, b)


def combinar(arr, a, m, b):
    izquierda = arr[a:m + 1]
    derecha = arr[m + 1:b + 1]
    i = 0
    j = 0
    k = a
    while i &lt; len(izquierda) and j &lt; len(derecha):
        if izquierda[i] &lt;= derecha[j]:
            arr[k] = izquierda[i]
            i += 1
        else:
            arr[k] = derecha[j]
            j += 1
        k += 1
    while i &lt; len(izquierda):
        arr[k] = izquierda[i]
        i += 1
        k += 1
    while j &lt; len(derecha):
        arr[k] = derecha[j]
        j += 1
        k += 1

# Entradas editables del ejemplo.
arr = [3, 1, 2]
a = 0
b = 2

print(&quot;Arreglo inicial:&quot;, arr)
ordenar(arr, a, b)
print(&quot;Arreglo ordenado:&quot;, arr)
</textarea></details><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Restablecer ejemplo</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

##### Laboratorio y medición

La animación permite observar la estructura recursiva. El panel experimental ejecuta funciones Python: el tiempo y la memoria de ese panel corresponden a esas funciones y no a una ejecución del listado Java. La memoria se obtiene con tracemalloc; no mide directamente la pila de una JVM.

El panel ejecuta mezcla con listas y copias temporales de Python; la entrada descendente se prepara fuera de la medición.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/runtime/recursive_examples_analysis.py).

<!-- book-code:end -->

#### Análisis

La división genera dos subproblemas de tamaño \(n/2\) y la combinación recorre los \(n\) elementos. Por tanto, \(T(n)=2 \cdot T(n/2)+\Theta(n)\in\Theta(n \cdot \log_2(n))\). Los arreglos auxiliares de combinación requieren \(\Theta(n)\) memoria; la pila añade \(\Theta(\log_2(n))\), que queda dominada por el almacenamiento lineal.

#### Simulación

La vista experimental muestra las divisiones, el retorno de cada mitad y la combinación ordenada por niveles.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-6/ejemplos/arbol_recursion_mezcla.png" alt="Árbol de llamadas de ejemplo 4 · ordenamiento por mezcla"><figcaption>Árbol de llamadas de ejemplo 4 · ordenamiento por mezcla.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/arbol_recursion_mecla_2.png" alt="Árbol de llamadas de ejemplo 4 · ordenamiento por mezcla"><figcaption>Árbol de llamadas de ejemplo 4 · ordenamiento por mezcla.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../potencia/">← Ejemplo 3 · Potencia de un número entero positivo</a><a class="section-step__index" href="../">Capítulo 6</a><a class="section-step__next" href="../arbol-binario/">Ejemplo 5 · Búsqueda en árbol binario →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>
