<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.2 Imprimir los elementos de un arreglo

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo2_(imprimir_elementos_arreglo).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El algoritmo visita una vez cada posición de un arreglo de tamaño \(n\). La simulación prepara la entrada antes de medir la operación.

### Código analizado

<!-- book-code:start -->

#### Recorrido de un arreglo

Implementación corregida basada en el libro, página 151 (Java).

=== "Java"

    ```java
    public static void imprimirElementos(int[] arr) {
        for (int i = 0; i < arr.length; i++) {
            System.out.println(arr[i]);
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función imprimirElementos(arr)
        para i en rango(longitud(arr))
            imprimir(arr[i])
    ```

=== "Python"

    ```python
    def imprimirElementos(arr):
        for i in range(len(arr)):
            print(arr[i])
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    void imprimirElementos(int arr[], int n) {
        for (int i = 0; i < n; i++) {
            printf("%d\n", arr[i]);
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, `n` indica la longitud del arreglo y se recibe como parámetro.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo de enteros. |
| `i` | Índice del recorrido. |

**Precondiciones:** arr no nulo.

**Resultado:** Imprime cada elemento; no devuelve un valor.

??? example "Ejemplo paso a paso"
    Entrada: `arr = [4, 8]`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `i = 0` | Imprime arr[0] = 4. |
    | `i = 1` | Imprime arr[1] = 8. |
    | `i = 2` | Termina porque `i = arr.length`. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-600c8cbef08a">Código Python · Recorrido de un arreglo</label><textarea id="runner-600c8cbef08a" spellcheck="false" wrap="off" rows="14">def imprimirElementos(arr):
    for i in range(len(arr)):
        print(arr[i])

# Entradas editables del ejemplo.
arr = [4, 8]

imprimirElementos(arr)
print(&quot;Ejemplo finalizado&quot;)
</textarea></details><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Restablecer ejemplo</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

Los experimentos ejecutan adaptaciones Python. El tiempo excluye la preparación y se promedia por ejecución. La memoria representa el incremento de pico observado por tracemalloc durante la operación, sin incluir la entrada preparada; no es el tamaño de la memoria de una máquina Java.

El experimento recorre el arreglo y omite la salida por consola del Java.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/runtime/experimental_analysis.py).

<!-- book-code:end -->

### Análisis esperado

#### Complejidad temporal

\(T(n)\in O(n)\) porque el cuerpo del ciclo se ejecuta una vez por cada elemento.

#### Complejidad espacial

\(S(n)\in O(1)\) en espacio adicional: el arreglo se considera la entrada y el recorrido solo conserva la referencia actual.

### Simulaciones experimentales

Cada experimento ejecuta la adaptación Python descrita en «Laboratorio y medición» para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La entrada preparada se excluye de la medición. Las reservas realizadas dentro de la operación sí se incluyen; la memoria observada corresponde al incremento de pico de Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_imprimir_elementos_tiempo.png" alt="Comportamiento temporal experimental de 4.4.4.2 imprimir los elementos de un arreglo"><figcaption>Comportamiento temporal experimental de 4.4.4.2 imprimir los elementos de un arreglo.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_imprimir_elementos_espacio.png" alt="Comportamiento espacial experimental de 4.4.4.2 imprimir los elementos de un arreglo"><figcaption>Comportamiento espacial experimental de 4.4.4.2 imprimir los elementos de un arreglo.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo1-sumar-numeros/">← 4.4.4.1 Sumar dos números</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo3-imprimir-elementos-matriz/">4.4.4.3 Imprimir los elementos de una matriz →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
