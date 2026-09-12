<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.3 Imprimir los elementos de una matriz

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo3_(imprimir_elementos_matriz).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El código recibe una matriz rectangular de \(m\) filas y \(n\) columnas. El laboratorio usa el caso particular \(m=n\), con la entrada preparada antes de medir.

### Código analizado

<!-- book-code:start -->

#### Recorrido de una matriz rectangular

Implementación corregida basada en el libro, página 153 (Java).

=== "Java"

    ```java
    public static void imprimirMatriz(int[][] matriz) {
        int m = matriz.length;
        int n = m > 0 ? matriz[0].length : 0;
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                System.out.println(matriz[i][j]);
            }
            System.out.println();
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función imprimirMatriz(matriz)
        m ← longitud(matriz)
        n ← longitud(matriz[0]) if m > 0 else 0
        para i en rango(m)
            para j en rango(n)
                imprimir(matriz[i][j])
            imprimir()
    ```

=== "Python"

    ```python
    def imprimirMatriz(matriz):
        m = len(matriz)
        n = len(matriz[0]) if m > 0 else 0
        for i in range(m):
            for j in range(n):
                print(matriz[i][j])
            print()
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    void imprimirMatriz(int m, int n, int matriz[m][n]) {
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                printf("%d\n", matriz[i][j]);
            }
            printf("\n");
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, las dimensiones se reciben como parámetros; las matrices de salida las reserva el llamador. La reserva de memoria se analiza por separado de los ciclos mostrados.

| Parámetro o variable | Significado |
| --- | --- |
| `matriz` | Matriz de enteros. |
| `m, n` | Cantidad de filas y columnas. |
| `i, j` | Índices de fila y columna. |

**Precondiciones:** Matriz no nula, con filas no nulas y todas de la misma longitud.

**Resultado:** Imprime los elementos y un salto al terminar cada fila.

??? example "Ejemplo paso a paso"
    Entrada: `matriz = [[1, 2, 3], [4, 5, 6]]`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `m = 2, n = 3` | Determina las dimensiones. |
    | `i = 0; j = 0, 1, 2` | Imprime 1, 2 y 3; después un salto. |
    | `i = 1; j = 0, 1, 2` | Imprime 4, 5 y 6; después un salto. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-e73ca84ca782">Código Python · Recorrido de una matriz rectangular</label><textarea id="runner-e73ca84ca782" spellcheck="false" wrap="off" rows="14">def imprimirMatriz(matriz):
    m = len(matriz)
    n = len(matriz[0]) if m &gt; 0 else 0
    for i in range(m):
        for j in range(n):
            print(matriz[i][j])
        print()

# Entradas editables del ejemplo.
matriz = [[1, 2, 3], [4, 5, 6]]

imprimirMatriz(matriz)
print(&quot;Ejemplo finalizado&quot;)
</textarea></details><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Restablecer ejemplo</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

Los experimentos ejecutan adaptaciones Python. El tiempo excluye la preparación y se promedia por ejecución. La memoria representa el incremento de pico observado por tracemalloc durante la operación, sin incluir la entrada preparada; no es el tamaño de la memoria de una máquina Java.

La medición usa matrices cuadradas (\(m = n\)), recorre sus valores y omite la impresión.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/runtime/experimental_analysis.py).

<!-- book-code:end -->

### Análisis esperado

#### Complejidad temporal

Para dimensiones positivas, \(T(m,n)\in\Theta(m\cdot n)\): se visitan todas las celdas y se imprimen \(m\) saltos adicionales. Incluyendo dimensiones vacías, el costo es \(\Theta(1+m+m\cdot n)\). Cuando \(m=n\), se obtiene \(T(n)\in\Theta(n^2)\).

#### Complejidad espacial

\(S(n)\in O(1)\) en espacio adicional porque la matriz pertenece a la entrada.

### Simulaciones experimentales

Cada experimento ejecuta la adaptación Python descrita en «Laboratorio y medición» para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La entrada preparada se excluye de la medición. Las reservas realizadas dentro de la operación sí se incluyen; la memoria observada corresponde al incremento de pico de Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_imprimir_matriz_tiempo.png" alt="Comportamiento temporal experimental de 4.4.4.3 imprimir los elementos de una matriz"><figcaption>Comportamiento temporal experimental de 4.4.4.3 imprimir los elementos de una matriz.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_imprimir_matriz_espacio.png" alt="Comportamiento espacial experimental de 4.4.4.3 imprimir los elementos de una matriz"><figcaption>Comportamiento espacial experimental de 4.4.4.3 imprimir los elementos de una matriz.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo2-imprimir-elementos-arreglo/">← 4.4.4.2 Imprimir los elementos de un arreglo</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo4-inicializar-matriz-variable/">4.4.4.4 Inicializar una matriz variable →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
