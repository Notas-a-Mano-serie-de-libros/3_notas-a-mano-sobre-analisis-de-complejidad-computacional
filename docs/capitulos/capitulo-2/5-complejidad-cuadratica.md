<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.5 Complejidad cuadrática

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/5_complejidad_cuadratica.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: recorrer una matriz

El ejemplo recorre todas las posiciones de una matriz. Si la matriz tiene \(n\) filas y \(n\) columnas, el cuerpo interno se ejecuta \(n \times n\) veces.

La estructura de dos ciclos anidados hace que el número de accesos crezca cuadráticamente con el tamaño lateral de la matriz.


---

### Código del libro asociado

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

El listado Java procede de la página del libro indicada arriba. El laboratorio ejecuta una adaptación en Python; compara el patrón de crecimiento, no los tiempos de Java con los de Python.

El tiempo se promedia por ejecución; la preparación de las entradas se realiza antes de cronometrar. Las gráficas teóricas y las mediciones experimentales se identifican por separado.

El laboratorio suma una matriz cuadrada; el listado del libro imprime una matriz rectangular. Ambos recorren las celdas. La medición omite la impresión y fija \(m = n\).

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/runtime/complexity_animations.py).

<!-- book-code:end -->

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad cuadrática describe algoritmos cuyo costo crece con el cuadrado del tamaño de entrada. Suele aparecer cuando dos ciclos anidados dependen de \(n\).

En estos casos, cada elemento puede relacionarse con muchos otros elementos, o se recorre una estructura bidimensional de tamaño \(n \times n\).

Para una entrada de tamaño \(n\), una función de costo cuadrático puede expresarse como:

\[
T(n) = cn^2
\]

donde \(c\) representa el costo constante de cada operación elemental y \(n^2\) representa la cantidad de combinaciones o posiciones evaluadas.

El crecimiento es mucho más rápido que el lineal: duplicar \(n\) puede multiplicar el trabajo aproximadamente por cuatro.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_cuadratica.png" alt="Representación gráfica de 2.1.2.5 complejidad cuadrática"><figcaption>Representación gráfica de 2.1.2.5 complejidad cuadrática.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../4-complejidad-log-lineal/">← 2.1.2.4 Complejidad log-lineal</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../6-complejidad-cubica/">2.1.2.6 Complejidad cúbica →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
