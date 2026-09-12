<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.4 Inicializar una matriz variable

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo4_(inicializar_matriz_variable).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

Este algoritmo recibe \(m\) y \(n\), crea una matriz rectangular de \(m\times n\) y escribe 1 en cada celda. La simulación estudia el caso cuadrado \(m=n\).

### Código analizado

<!-- book-code:start -->

#### Inicialización de una matriz rectangular

Implementación corregida basada en el libro, página 156 (Java).

=== "Java"

    ```java
    public static int[][] inicializarMatriz(int m, int n) {
        int[][] matriz = new int[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                matriz[i][j] = 1;
            }
        }
        return matriz;
    }
    ```

=== "Pseudocódigo"

    ```text
    función inicializarMatriz(m, n)
        matriz ← [[0] * n for _ in rango(m)]
        para i en rango(m)
            para j en rango(n)
                matriz[i][j] ← 1
        retornar matriz
    ```

=== "Python"

    ```python
    def inicializarMatriz(m, n):
        matriz = [[0] * n for _ in range(m)]
        for i in range(m):
            for j in range(n):
                matriz[i][j] = 1
        return matriz
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    // El llamador proporciona espacio para m * n enteros.
    void inicializarMatriz(int m, int n, int matriz[m][n]) {
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                matriz[i][j] = 1;
            }
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, las dimensiones se reciben como parámetros; las matrices de salida las reserva el llamador. La reserva de memoria se analiza por separado de los ciclos mostrados.

| Parámetro o variable | Significado |
| --- | --- |
| `m, n` | Cantidad de filas y columnas a crear. |
| `matriz` | Matriz nueva que se devuelve. |
| `i, j` | Índices de fila y columna. |

**Precondiciones:** m y n no negativos; memoria suficiente para la matriz.

**Resultado:** Devuelve una matriz \(m \times n\) cuyos elementos valen 1.

??? example "Ejemplo paso a paso"
    Entrada: `m = 2, n = 3`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `matriz = new int[2][3]` | Reserva dos filas de tres columnas, inicialmente en cero. |
    | `i = 0; j = 0, 1, 2` | Escribe 1 en la primera fila. |
    | `i = 1; j = 0, 1, 2` | Escribe 1 en la segunda fila. |
    | `return matriz` | Devuelve [[1, 1, 1], [1, 1, 1]]. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-7d3e0b987ac9">Código Python · Inicialización de una matriz rectangular</label><textarea id="runner-7d3e0b987ac9" spellcheck="false" wrap="off" rows="14">def inicializarMatriz(m, n):
    matriz = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            matriz[i][j] = 1
    return matriz

# Entradas editables del ejemplo.
m = 2
n = 3

resultado = inicializarMatriz(m, n)
print(&quot;Resultado:&quot;, resultado)
</textarea></details><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Restablecer ejemplo</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

Los experimentos ejecutan adaptaciones Python. El tiempo excluye la preparación y se promedia por ejecución. La memoria representa el incremento de pico observado por tracemalloc durante la operación, sin incluir la entrada preparada; no es el tamaño de la memoria de una máquina Java.

El experimento fija \(m = n\), reserva una matriz de ceros dentro de la operación y la recorre. Modela el costo de crear y recorrer, pero no escribe los unos ni devuelve la matriz como el Java.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/runtime/experimental_analysis.py).

<!-- book-code:end -->

### Análisis esperado

#### Complejidad temporal

Para dimensiones positivas, \(T(m,n)\in\Theta(m\cdot n)\) por reservar e inicializar todas las celdas y recorrerlas para escribir 1. La reserva de Java también inicializa la memoria; no se considera constante. Incluyendo dimensiones vacías, \(T(m,n)\in\Theta(1+m+m\cdot n)\). Si \(m=n\), el costo es \(\Theta(n^2)\).

#### Complejidad espacial

La matriz nueva ocupa \(S(m,n)\in\Theta(1+m+m\cdot n)\), incluidas las referencias a filas. Para dimensiones positivas se simplifica a \(\Theta(m\cdot n)\), y cuando \(m=n\) es \(\Theta(n^2)\). Este espacio incluye el resultado; excluyéndolo, los índices usan \(O(1)\).

### Simulaciones experimentales

Cada experimento ejecuta la adaptación Python descrita en «Laboratorio y medición» para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La entrada preparada se excluye de la medición. Las reservas realizadas dentro de la operación sí se incluyen; la memoria observada corresponde al incremento de pico de Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_inicializar_matriz_tiempo.png" alt="Comportamiento temporal experimental de 4.4.4.4 inicializar una matriz variable"><figcaption>Comportamiento temporal experimental de 4.4.4.4 inicializar una matriz variable.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_inicializar_matriz_espacio.png" alt="Comportamiento espacial experimental de 4.4.4.4 inicializar una matriz variable"><figcaption>Comportamiento espacial experimental de 4.4.4.4 inicializar una matriz variable.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo3-imprimir-elementos-matriz/">← 4.4.4.3 Imprimir los elementos de una matriz</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo5-ciclos-incremento-no-lineal/">4.4.4.5 Ciclos con incremento no lineal →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
