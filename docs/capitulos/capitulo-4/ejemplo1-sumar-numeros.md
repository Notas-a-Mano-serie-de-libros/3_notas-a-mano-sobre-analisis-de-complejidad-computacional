<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.1 Sumar dos números

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo1_(sumar_numeros).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

Este ejemplo analiza una secuencia de una sola operación aritmética. El tamaño de referencia \(n\) cambia, pero la cantidad de instrucciones ejecutadas permanece fija.

### Código analizado

<!-- book-code:start -->

#### Suma de dos enteros

Implementación corregida basada en el libro, página 150 (Java).

=== "Java"

    ```java
    public static int sumar(int a, int b) {
        return Math.addExact(a, b);
    }
    ```

=== "Pseudocódigo"

    ```text
    función sumar(a, b)
        resultado ← a + b
        si no -2147483648 <= resultado <= 2147483647 entonces
            error OverflowError("El resultado no cabe en int de Java")
        retornar resultado
    ```

=== "Python"

    ```python
    def sumar(a, b):
        resultado = a + b
        if not -2147483648 <= resultado <= 2147483647:
            raise OverflowError("El resultado no cabe en int de Java")
        return resultado
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    int sumaExacta(int a, int b) {
        int64_t resultado = (int64_t) a + b;
        if (resultado < INT_MIN || resultado > INT_MAX) {
            abort();
        }
        return (int) resultado;
    }

    int sumar(int a, int b) {
        return sumaExacta(a, b);
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `a, b` | Enteros que se suman. |

**Precondiciones:** La suma matemática debe caber en int si se espera un resultado exacto.

**Resultado:** Devuelve a + b.

??? example "Ejemplo paso a paso"
    Entrada: `a = 2, b = 3`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `a = 2, b = 3` | Se reciben los operandos. |
    | `a + b` | Se devuelve 5. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-be0f6b02d91f">Código Python · Suma de dos enteros</label><textarea id="runner-be0f6b02d91f" spellcheck="false" wrap="off" rows="14">def sumar(a, b):
    resultado = a + b
    if not -2147483648 &lt;= resultado &lt;= 2147483647:
        raise OverflowError(&quot;El resultado no cabe en int de Java&quot;)
    return resultado

# Entradas editables del ejemplo.
a = 2
b = 3

resultado = sumar(a, b)
print(&quot;Resultado:&quot;, resultado)
</textarea></details><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Restablecer ejemplo</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

Los experimentos ejecutan adaptaciones Python. El tiempo excluye la preparación y se promedia por ejecución. La memoria representa el incremento de pico observado por tracemalloc durante la operación, sin incluir la entrada preparada; no es el tamaño de la memoria de una máquina Java.

La suma se mide sobre dos operandos preparados.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/runtime/experimental_analysis.py).

<!-- book-code:end -->

### Análisis esperado

#### Complejidad temporal

\(T(n)\in O(1)\) porque la suma ejecuta una cantidad constante de operaciones para cada valor de \(n\).

#### Complejidad espacial

\(S(n)\in O(1)\) porque solo se mantienen dos operandos y el resultado.

### Simulaciones experimentales

Cada experimento ejecuta la adaptación Python descrita en «Laboratorio y medición» para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La entrada preparada se excluye de la medición. Las reservas realizadas dentro de la operación sí se incluyen; la memoria observada corresponde al incremento de pico de Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_suma_dos_numeros_tiempo.png" alt="Comportamiento temporal experimental de 4.4.4.1 sumar dos números"><figcaption>Comportamiento temporal experimental de 4.4.4.1 sumar dos números.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_suma_dos_numeros_espacio.png" alt="Comportamiento espacial experimental de 4.4.4.1 sumar dos números"><figcaption>Comportamiento espacial experimental de 4.4.4.1 sumar dos números.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo2-imprimir-elementos-arreglo/">4.4.4.2 Imprimir los elementos de un arreglo →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
