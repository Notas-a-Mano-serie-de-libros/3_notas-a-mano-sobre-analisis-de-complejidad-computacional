<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# 8.5 Ordenamiento por mezcla

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/5_ordenamiento_mezcla.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ordenamiento por mezcla (merge sort) divide el arreglo a la mitad de forma recursiva hasta obtener subarreglos de un solo elemento, que por definición están ordenados. Luego combina (mezcla) los subarreglos en orden creciente hasta reconstruir el arreglo completo.

Garantiza O(n log(n)) en todos los casos, lo que lo hace predecible y eficiente, aunque requiere O(n) de memoria auxiliar para la fase de mezcla.

### Implementación

<!-- book-code:start -->

#### Ordenamiento por mezcla y combinación

Implementación corregida basada en el libro, página 341 (Java).

=== "Java"

    ```java
    public void ordenar(int[] arr, int a, int b) {
        if (a >= b)
            return;
        // Calcula el pivote que separa el arreglo en dos
        int m = a + (b - a) / 2;
        // Etapa de división
        ordenar(arr, a, m);
        ordenar(arr, m + 1, b);
        // Etapa de combinación
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

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-de54bf47e11a">Código Python · Ordenamiento por mezcla y combinación</label><textarea id="runner-de54bf47e11a" spellcheck="false" wrap="off" rows="14">def ordenar(arr, a, b):
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

#### Laboratorio y medición

La animación y el contador son adaptaciones Python con operaciones instrumentadas. Incluyen comparaciones, movimientos y control del recorrido según el contador; no se deben interpretar todos los pasos como una sola clase de operación Java. Las opciones descendentes son ampliaciones: los listados del libro ordenan ascendentemente.

La adaptación usa copias temporales y representa el árbol de divisiones y combinaciones.

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
    <tr><td>Mejor caso</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>\(\Omega(n)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(\Theta(n \cdot \log_2(n))\)</td><td>\(\Theta(n)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(n \cdot \log_2(n))\)</td><td>\(O(n)\)</td></tr>
  </tbody>
</table>
</div>

Este resumen presenta los resultados generales. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.


---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y el orden deseado.
3. Use el botón `Ordenar` para ejecutar la animación paso a paso o de forma automática.
4. Observe las fases de división y mezcla del arreglo.

### Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento por mezcla sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios.

- **Línea sólida** — simulación empírica (n ≤ 2 000, 5 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 1 000 000
- **Checkbox** — superpone la función teórica n·log₂(n) normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva crece mucho más despacio que los algoritmos O(n²), lo que refleja la ventaja del enfoque divide y vencerás.

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
    <tr><td>Peor caso</td><td>\(n\cdot\log_2(n)\)</td><td>\(O(n\cdot\log_2(n))\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa la **función exacta para todos los escenarios**: ordenamiento por mezcla tiene complejidad uniforme porque siempre divide y mezcla con la misma estructura recursiva, independientemente del orden inicial.

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
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_mezcla/ordenamiento_mezcla_1.png" alt="Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 1 de 4"><figcaption>Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_mezcla/ordenamiento_mezcla_7.png" alt="Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 2 de 4"><figcaption>Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 2 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_mezcla/ordenamiento_mezcla_13.png" alt="Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 3 de 4"><figcaption>Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 3 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_mezcla/ordenamiento_mezcla_20.png" alt="Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 4 de 4"><figcaption>Secuencia visual de 8.5 ordenamiento por mezcla · paso representativo 4 de 4.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../4-ordenamiento-shell/">← Ampliación · Ordenamiento Shell</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../6-ordenamiento-rapido/">8.6 Ordenamiento rápido →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
