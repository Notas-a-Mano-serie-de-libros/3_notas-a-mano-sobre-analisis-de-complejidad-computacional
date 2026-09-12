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

Implementación corregida basada en el libro, página 363 (Java).

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

??? example "Ejemplo paso a paso"
    Entrada: `arr = [21, 13, 12]`.

    **Prueba de escritorio**

    | Paso | Método | Profundidad | arr | min | max | rango | d | i | n | exp | conteo | salida | valor | j | Operación ejecutada | Retorno |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 1 | ordenar | 0 | [21, 13, 12] | — | — | — | — | — | — | — | — | — | — | — | Entrada a la llamada. | — |
    | 2 | ordenar | 0 | [21, 13, 12] | — | — | — | — | — | — | — | — | — | — | — | `if not arr:` | — |
    | 3 | ordenar | 0 | [21, 13, 12] | 12 | — | — | — | — | — | — | — | — | — | — | `minimo = min(arr)` | — |
    | 4 | ordenar | 0 | [21, 13, 12] | 12 | 21 | — | — | — | — | — | — | — | — | — | `maximo = max(arr)` | — |
    | 5 | ordenar | 0 | [21, 13, 12] | 12 | 21 | 9 | — | — | — | — | — | — | — | — | `rango = maximo - minimo` | — |
    | 6 | ordenar | 0 | [21, 13, 12] | 12 | 21 | 9 | 1 | — | — | — | — | — | — | — | `d = 1` | — |
    | 7 | ordenar | 0 | [21, 13, 12] | 12 | 21 | 9 | 1 | — | — | — | — | — | — | — | `while rango >= 10:` | — |
    | 8 | ordenar | 0 | [21, 13, 12] | 12 | 21 | 9 | 1 | 1 | — | — | — | — | — | — | `for i in range(1, d + 1):` | — |
    | 9 | ordenarPorDigito | 1 | [21, 13, 12] | — | — | — | — | 1 | — | — | — | — | — | — | Entrada a la llamada. | — |
    | 10 | ordenarPorDigito | 1 | [21, 13, 12] | — | — | — | — | 1 | — | — | — | — | — | — | `if not 1 <= i <= 10:` | — |
    | 11 | ordenarPorDigito | 1 | [21, 13, 12] | — | — | — | — | 1 | — | — | — | — | — | — | `if not arr:` | — |
    | 12 | ordenarPorDigito | 1 | [21, 13, 12] | — | — | — | — | 1 | 3 | — | — | — | — | — | `n = len(arr)` | — |
    | 13 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | — | — | — | — | — | `minimo = min(arr)` | — |
    | 14 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | — | — | — | — | `exp = 1` | — |
    | 15 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | — | — | — | — | `for j in range(1, i):` | — |
    | 16 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] | — | — | — | `conteo = [0] * 10` | — |
    | 17 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] | [0, 0, 0] | — | — | `salida = [0] * n` | — |
    | 18 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [0, 0, 0, 0, 0, 0, 0, 0, 0, 0] | [0, 0, 0] | 21 | — | `for valor in arr:` | — |
    | 19 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [0, 0, 0, 0, 0, 0, 0, 0, 0, 1] | [0, 0, 0] | 21 | — | `conteo[(valor - minimo) // exp % 10] += 1` | — |
    | 20 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [0, 0, 0, 0, 0, 0, 0, 0, 0, 1] | [0, 0, 0] | 13 | — | `for valor in arr:` | — |
    | 21 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [0, 1, 0, 0, 0, 0, 0, 0, 0, 1] | [0, 0, 0] | 13 | — | `conteo[(valor - minimo) // exp % 10] += 1` | — |
    | 22 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [0, 1, 0, 0, 0, 0, 0, 0, 0, 1] | [0, 0, 0] | 12 | — | `for valor in arr:` | — |
    | 23 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 1, 0, 0, 0, 0, 0, 0, 0, 1] | [0, 0, 0] | 12 | — | `conteo[(valor - minimo) // exp % 10] += 1` | — |
    | 24 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 1, 0, 0, 0, 0, 0, 0, 0, 1] | [0, 0, 0] | 12 | — | `for valor in arr:` | — |
    | 25 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 1, 0, 0, 0, 0, 0, 0, 0, 1] | [0, 0, 0] | 12 | 1 | `for j in range(1, 10):` | — |
    | 26 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 0, 0, 0, 0, 0, 0, 0, 1] | [0, 0, 0] | 12 | 1 | `conteo[j] += conteo[j - 1]` | — |
    | 27 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 0, 0, 0, 0, 0, 0, 0, 1] | [0, 0, 0] | 12 | 2 | `for j in range(1, 10):` | — |
    | 28 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 0, 0, 0, 0, 0, 0, 1] | [0, 0, 0] | 12 | 2 | `conteo[j] += conteo[j - 1]` | — |
    | 29 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 0, 0, 0, 0, 0, 0, 1] | [0, 0, 0] | 12 | 3 | `for j in range(1, 10):` | — |
    | 30 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 0, 0, 0, 0, 0, 1] | [0, 0, 0] | 12 | 3 | `conteo[j] += conteo[j - 1]` | — |
    | 31 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 0, 0, 0, 0, 0, 1] | [0, 0, 0] | 12 | 4 | `for j in range(1, 10):` | — |
    | 32 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 2, 0, 0, 0, 0, 1] | [0, 0, 0] | 12 | 4 | `conteo[j] += conteo[j - 1]` | — |
    | 33 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 2, 0, 0, 0, 0, 1] | [0, 0, 0] | 12 | 5 | `for j in range(1, 10):` | — |
    | 34 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 2, 2, 0, 0, 0, 1] | [0, 0, 0] | 12 | 5 | `conteo[j] += conteo[j - 1]` | — |
    | 35 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 2, 2, 0, 0, 0, 1] | [0, 0, 0] | 12 | 6 | `for j in range(1, 10):` | — |
    | 36 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 2, 2, 2, 0, 0, 1] | [0, 0, 0] | 12 | 6 | `conteo[j] += conteo[j - 1]` | — |
    | 37 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 2, 2, 2, 0, 0, 1] | [0, 0, 0] | 12 | 7 | `for j in range(1, 10):` | — |
    | 38 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 2, 2, 2, 2, 0, 1] | [0, 0, 0] | 12 | 7 | `conteo[j] += conteo[j - 1]` | — |
    | 39 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 2, 2, 2, 2, 0, 1] | [0, 0, 0] | 12 | 8 | `for j in range(1, 10):` | — |
    | 40 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 2, 2, 2, 2, 2, 1] | [0, 0, 0] | 12 | 8 | `conteo[j] += conteo[j - 1]` | — |
    | 41 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 2, 2, 2, 2, 2, 1] | [0, 0, 0] | 12 | 9 | `for j in range(1, 10):` | — |
    | 42 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 2, 2, 2, 2, 2, 3] | [0, 0, 0] | 12 | 9 | `conteo[j] += conteo[j - 1]` | — |
    | 43 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 2, 2, 2, 2, 2, 3] | [0, 0, 0] | 12 | 9 | `for j in range(1, 10):` | — |
    | 44 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | — | 1 | 3 | 1 | [1, 2, 2, 2, 2, 2, 2, 2, 2, 3] | [0, 0, 0] | 12 | 2 | `for j in range(n - 1, -1, -1):` | — |
    | 45 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | 0 | 1 | 3 | 1 | [1, 2, 2, 2, 2, 2, 2, 2, 2, 3] | [0, 0, 0] | 12 | 2 | `d = (arr[j] - minimo) // exp % 10` | — |
    | 46 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | 0 | 1 | 3 | 1 | [0, 2, 2, 2, 2, 2, 2, 2, 2, 3] | [0, 0, 0] | 12 | 2 | `conteo[d] -= 1` | — |
    | 47 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | 0 | 1 | 3 | 1 | [0, 2, 2, 2, 2, 2, 2, 2, 2, 3] | [12, 0, 0] | 12 | 2 | `salida[conteo[d]] = arr[j]` | — |
    | 48 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | 0 | 1 | 3 | 1 | [0, 2, 2, 2, 2, 2, 2, 2, 2, 3] | [12, 0, 0] | 12 | 1 | `for j in range(n - 1, -1, -1):` | — |
    | 49 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | 1 | 1 | 3 | 1 | [0, 2, 2, 2, 2, 2, 2, 2, 2, 3] | [12, 0, 0] | 12 | 1 | `d = (arr[j] - minimo) // exp % 10` | — |
    | 50 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | 1 | 1 | 3 | 1 | [0, 1, 2, 2, 2, 2, 2, 2, 2, 3] | [12, 0, 0] | 12 | 1 | `conteo[d] -= 1` | — |
    | 51 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | 1 | 1 | 3 | 1 | [0, 1, 2, 2, 2, 2, 2, 2, 2, 3] | [12, 13, 0] | 12 | 1 | `salida[conteo[d]] = arr[j]` | — |
    | 52 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | 1 | 1 | 3 | 1 | [0, 1, 2, 2, 2, 2, 2, 2, 2, 3] | [12, 13, 0] | 12 | 0 | `for j in range(n - 1, -1, -1):` | — |
    | 53 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | 9 | 1 | 3 | 1 | [0, 1, 2, 2, 2, 2, 2, 2, 2, 3] | [12, 13, 0] | 12 | 0 | `d = (arr[j] - minimo) // exp % 10` | — |
    | 54 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | 9 | 1 | 3 | 1 | [0, 1, 2, 2, 2, 2, 2, 2, 2, 2] | [12, 13, 0] | 12 | 0 | `conteo[d] -= 1` | — |
    | 55 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | 9 | 1 | 3 | 1 | [0, 1, 2, 2, 2, 2, 2, 2, 2, 2] | [12, 13, 21] | 12 | 0 | `salida[conteo[d]] = arr[j]` | — |
    | 56 | ordenarPorDigito | 1 | [21, 13, 12] | 12 | — | — | 9 | 1 | 3 | 1 | [0, 1, 2, 2, 2, 2, 2, 2, 2, 2] | [12, 13, 21] | 12 | 0 | `for j in range(n - 1, -1, -1):` | — |
    | 57 | ordenarPorDigito | 1 | [12, 13, 21] | 12 | — | — | 9 | 1 | 3 | 1 | [0, 1, 2, 2, 2, 2, 2, 2, 2, 2] | [12, 13, 21] | 12 | 0 | `arr[:] = salida`; Termina la llamada. | sin valor |
    | 58 | ordenar | 0 | [12, 13, 21] | 12 | 21 | 9 | 1 | 1 | — | — | — | — | — | — | `ordenarPorDigito(arr, i)` | — |
    | 59 | ordenar | 0 | [12, 13, 21] | 12 | 21 | 9 | 1 | 1 | — | — | — | — | — | — | `for i in range(1, d + 1):`; Termina la llamada. | sin valor |

    Cada fila muestra el estado después de la operación indicada de la traducción Python de esta variante. «—» indica una variable aún no declarada en esa llamada o un retorno todavía pendiente. La profundidad inicial es 0; cada llamada anidada la incrementa en 1.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-96a3e8c5dc4e">Código Python · Radix decimal para enteros con signo</label><textarea id="runner-96a3e8c5dc4e" spellcheck="false" wrap="off" rows="14">def ordenar(arr):
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
</textarea></details><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Restablecer ejemplo</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

La animación y el contador son adaptaciones Python con operaciones instrumentadas. Incluyen comparaciones, movimientos y control del recorrido según el contador; no se deben interpretar todos los pasos como una sola clase de operación Java. Las opciones descendentes son ampliaciones: los listados del libro ordenan ascendentemente.

El listado corregido usa base decimal y desplaza las claves por el mínimo para admitir valores negativos. La adaptación del laboratorio puede representar esas claves de otra manera.

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
