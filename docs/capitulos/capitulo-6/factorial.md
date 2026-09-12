<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 1 · Factorial recursivo

<span class="chapter-kicker">Capítulo 6</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

#### Código

<!-- book-code:start -->

##### Factorial recursivo

Implementación corregida basada en el libro, página 229 (Java).

=== "Java"

    ```java
    public static int factorial(int n) {
        if (n < 0)
            throw new IllegalArgumentException("n debe ser no negativo");
        if (n > 12)
            throw new ArithmeticException("El factorial no cabe en int");
        if (n <= 1)
            return 1;
        else
            return Math.multiplyExact(n, factorial(n - 1));
    }
    ```

=== "Pseudocódigo"

    ```text
    función factorial(n)
        si n < 0 entonces
            error ValueError("n debe ser no negativo")
        si n > 12 entonces
            error OverflowError("El factorial no cabe en int de Java")
        si n <= 1 entonces
            retornar 1
        retornar n * factorial(n - 1)
    ```

=== "Python"

    ```python
    def factorial(n):
        if n < 0:
            raise ValueError("n debe ser no negativo")
        if n > 12:
            raise OverflowError("El factorial no cabe en int de Java")
        if n <= 1:
            return 1
        return n * factorial(n - 1)
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    int productoExacto(int a, int b) {
        int64_t resultado = (int64_t) a * b;
        if (resultado < INT_MIN || resultado > INT_MAX) {
            abort();
        }
        return (int) resultado;
    }

    int factorial(int n) {
        if (n < 0) {
            abort();
        }
        if (n > 12) {
            abort();
        }
        if (n <= 1) {
            return 1;
        }
        else {
            return productoExacto(n, factorial(n - 1));
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Entero no negativo. |
| `factorial(n-1)` | Resultado del subproblema. |

**Precondiciones:** n no negativo. Si el resultado no cabe en int, se lanza ArithmeticException en lugar de devolver un valor desbordado.

**Resultado:** Devuelve n!.

??? example "Ejemplo paso a paso"
    Entrada: `n = 3`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `factorial(3)` | Espera \(3 \times \operatorname{factorial}(2)\). |
    | `factorial(2)` | Espera \(2 \times \operatorname{factorial}(1)\). |
    | `factorial(1) = 1` | Caso base. |
    | `Retorno` | \(2 \times 1 = 2\); luego \(3 \times 2 = 6\). |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-c8aa4c6cf900">Código Python · Factorial recursivo</label><textarea id="runner-c8aa4c6cf900" spellcheck="false" wrap="off" rows="14">def factorial(n):
    if n &lt; 0:
        raise ValueError(&quot;n debe ser no negativo&quot;)
    if n &gt; 12:
        raise OverflowError(&quot;El factorial no cabe en int de Java&quot;)
    if n &lt;= 1:
        return 1
    return n * factorial(n - 1)

# Entradas editables del ejemplo.
n = 3

resultado = factorial(n)
print(&quot;Resultado:&quot;, resultado)
</textarea></details><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Restablecer ejemplo</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

##### Laboratorio y medición

La animación permite observar la estructura recursiva. El panel experimental ejecuta funciones Python: el tiempo y la memoria de ese panel corresponden a esas funciones y no a una ejecución del listado Java. La memoria se obtiene con tracemalloc; no mide directamente la pila de una JVM.

El experimento suma las llamadas del recorrido recursivo; no multiplica para calcular n!. Esto permite medir la cadena de llamadas sin introducir enteros factoriales de tamaño creciente.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/runtime/recursive_examples_analysis.py).

<!-- book-code:end -->

#### Análisis

Cada llamada reduce \(n\) en una unidad y realiza una multiplicación adicional:

\[
T(n)=T(n-1)+\Theta(1),\qquad T(1)=\Theta(1).
\]

Después de \(n-1\) expansiones se alcanza el caso base, de modo que \(T(n)\in\Theta(n)\). Las llamadas pendientes forman una cadena de profundidad \(n\), por lo que \(S(n)\in\Theta(n)\).

#### Simulación

El recorrido muestra cómo se apilan los valores \(n,n-1,\ldots,1\) y cómo los productos se resuelven durante el retorno.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-6/ejemplos/arbol_recursion_factorial.png" alt="Árbol de llamadas de ejemplo 1 · factorial recursivo"><figcaption>Árbol de llamadas de ejemplo 1 · factorial recursivo.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/comparacion_complejidad_for.png" alt="Comparación de crecimiento para ejemplo 1 · factorial recursivo"><figcaption>Comparación de crecimiento para ejemplo 1 · factorial recursivo.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a class="section-step__index" href="../">Capítulo 6</a><a class="section-step__next" href="../fibonacci/">Ejemplo 2 · Fibonacci recursivo ingenuo →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>
