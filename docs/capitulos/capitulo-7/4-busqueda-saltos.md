<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>

# 7.5 Búsqueda por saltos

<span class="chapter-kicker">Capítulo 7</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/4_busqueda_saltos.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

La búsqueda por saltos avanza en bloques de tamaño √n hasta encontrar un elemento mayor que el objetivo o alcanzar el final del arreglo. Luego realiza una búsqueda secuencial hacia atrás dentro del bloque acotado. Requiere que el arreglo esté ordenado.

El bloque óptimo de tamaño √n balancea los saltos hacia adelante con la búsqueda secuencial hacia atrás, produciendo una complejidad de O(√n).

### Implementación

<!-- book-code:start -->

#### Búsqueda por saltos

Implementación corregida basada en el libro, página 290 (Java).

=== "Java"

    ```java
    public boolean buscar(int[] arr, int x) {
        int n = arr.length, anterior = 0;
        if (n == 0)
            return false;
        int paso = (int) Math.floor(Math.sqrt(n)), delta = paso;
        // Avanzar en saltos hasta encontrar el rango
        while (arr[Math.min(delta, n) - 1] < x) {
            anterior = delta;
            delta = (int) Math.min((long) delta + paso, n);
            if (anterior >= n)
                return false; // Elemento fuera del rango de búsqueda
        }
        // Realiza la búsqueda lineal en el rango identificado
        for (int i = anterior; i < Math.min(delta, n); i++) {
            if (arr[i] == x)
                return true; // Elemento encontrado
        }
        return false; // Elemento no encontrado
    }
    ```

=== "Pseudocódigo"

    ```text
    función buscar(arr, x)
        n ← longitud(arr)
        si n == 0 entonces
            retornar falso
        paso ← raízEntera(n)
        anterior ← 0
        delta ← paso
        mientras arr[min(delta, n) - 1] < x
            anterior ← delta
            delta ← min(delta + paso, n)
            si anterior >= n entonces
                retornar falso
        para i en rango(anterior, min(delta, n))
            si arr[i] == x entonces
                retornar verdadero
        retornar falso
    ```

=== "Python"

    ```python
    from math import isqrt


    def buscar(arr, x):
        n = len(arr)
        if n == 0:
            return False
        paso = isqrt(n)
        anterior = 0
        delta = paso
        while arr[min(delta, n) - 1] < x:
            anterior = delta
            delta = min(delta + paso, n)
            if anterior >= n:
                return False
        for i in range(anterior, min(delta, n)):
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

    int64_t minimo(int64_t a, int64_t b) {
        return a < b ? a : b;
    }

    bool buscar(int arr[], int n, int x) {
        int anterior = 0;
        if (n == 0) {
            return false;
        }
        int paso = (int) floor(sqrt(n)), delta = paso;
        // Avanzar en saltos hasta encontrar el rango
        while (arr[minimo(delta, n) - 1] < x) {
            anterior = delta;
            delta = (int) minimo((int64_t) delta + paso, n);
            if (anterior >= n) {
                return false; // Elemento fuera del rango de búsqueda
            }
        }
        // Realiza la búsqueda lineal en el rango identificado
        for (int i = anterior; i < minimo(delta, n); i++) {
            if (arr[i] == x) {
                return true; // Elemento encontrado
            }
        }
        return false; // Elemento no encontrado
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, `n` indica la longitud del arreglo y se recibe como parámetro.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo ordenado ascendentemente. |
| `x` | Valor buscado. |
| `paso` | Tamaño del salto, floor(sqrt(n)). |
| `anterior, delta` | Límites del bloque candidato. |
| `i` | Índice de la búsqueda lineal. |

**Precondiciones:** arr no nulo y ordenado de menor a mayor.

**Resultado:** Devuelve true si encuentra x; false si está ausente.

**Explicación:** El arreglo vacío devuelve false. La actualización del avance se calcula en long y se limita a arr.length antes de convertirla a int; no se exige que la suma o duplicación previa quepa en int.

??? example "Ejemplo paso a paso"
    Entrada: `arr = [1, 3, 5, 7, 9], x = 7`.

    **Prueba de escritorio**

    | Paso | Método | Profundidad | arr | x | n | paso | anterior | delta | i | Operación ejecutada | Retorno |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 1 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | — | — | — | — | — | Entrada a la llamada. | — |
    | 2 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | — | — | — | — | `n = len(arr)` | — |
    | 3 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | — | — | — | — | `if n == 0:` | — |
    | 4 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | — | — | — | `paso = isqrt(n)` | — |
    | 5 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | 0 | — | — | `anterior = 0` | — |
    | 6 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | 0 | 2 | — | `delta = paso` | — |
    | 7 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | 0 | 2 | — | `while arr[min(delta, n) - 1] < x:` | — |
    | 8 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | 2 | 2 | — | `anterior = delta` | — |
    | 9 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | 2 | 4 | — | `delta = min(delta + paso, n)` | — |
    | 10 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | 2 | 4 | — | `if anterior >= n:` | — |
    | 11 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | 2 | 4 | — | `while arr[min(delta, n) - 1] < x:` | — |
    | 12 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | 2 | 4 | 2 | `for i in range(anterior, min(delta, n)):` | — |
    | 13 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | 2 | 4 | 2 | `if arr[i] == x:` | — |
    | 14 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | 2 | 4 | 3 | `for i in range(anterior, min(delta, n)):` | — |
    | 15 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | 2 | 4 | 3 | `if arr[i] == x:` | — |
    | 16 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | 2 | 4 | 3 | `return True`; Termina la llamada. | true |

    Cada fila muestra el estado después de la operación indicada de la traducción Python de esta variante. «—» indica una variable aún no declarada en esa llamada o un retorno todavía pendiente. La profundidad inicial es 0; cada llamada anidada la incrementa en 1.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-57565cf91e1b">Código Python · Búsqueda por saltos</label><textarea id="runner-57565cf91e1b" spellcheck="false" wrap="off" rows="14">from math import isqrt


def buscar(arr, x):
    n = len(arr)
    if n == 0:
        return False
    paso = isqrt(n)
    anterior = 0
    delta = paso
    while arr[min(delta, n) - 1] &lt; x:
        anterior = delta
        delta = min(delta + paso, n)
        if anterior &gt;= n:
            return False
    for i in range(anterior, min(delta, n)):
        if arr[i] == x:
            return True
    return False

# Entradas editables del ejemplo.
arr = [1, 3, 5, 7, 9]
x = 7

resultado = buscar(arr, x)
print(&quot;Resultado:&quot;, resultado)
</textarea></details><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Restablecer ejemplo</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

La animación ejecuta una adaptación Python y registra estados visuales; sus pasos de interfaz no equivalen necesariamente a comparaciones del Java. El contador de eficiencia usa búsquedas sobre un objetivo presente y promedia ensayos. El tiempo teórico se estima a partir de una operación calibrada; no es una medición del listado Java.

El listado corregido incluye controles para los casos límite; el laboratorio usa su adaptación Python.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/core/search/search_metrics.py).

<!-- book-code:end -->

### Complejidad: versión iterativa y versión recursiva

La versión iterativa combina una fase de saltos por bloques con una fase secuencial dentro del bloque final. La versión recursiva puede modelar cada salto y cada avance lineal como llamadas sucesivas.

La diferencia principal entre ambas implementaciones aparece en el uso de memoria. La versión iterativa reutiliza el mismo marco de ejecución y conserva una cantidad constante de variables auxiliares. La versión recursiva crea un nuevo marco por cada llamada pendiente; por esa razón, la pila de ejecución puede crecer con la cantidad de divisiones, saltos o comparaciones acumuladas.

#### Resumen general

<div style="display:flex; justify-content:center; margin:1.2em 0;">
<table style="margin: 0 auto; text-align: center;">
  <thead>
    <tr>
      <th>Implementación</th>
      <th>Escenario</th>
      <th><i>T</i>(<i>n</i>)</th>
      <th><i>S</i>(<i>n</i>)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Iterativa</td><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Iterativa</td><td>Caso promedio</td><td>\(\Theta(\sqrt{n})\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Iterativa</td><td>Peor caso</td><td>\(O(\sqrt{n})\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Caso promedio</td><td>\(\Theta(\sqrt{n})\)</td><td>\(\Theta(\sqrt{n})\)</td></tr>
    <tr><td>Recursiva</td><td>Peor caso</td><td>\(O(\sqrt{n})\)</td><td>\(O(\sqrt{n})\)</td></tr>
  </tbody>
</table>
</div>

#### Versión iterativa

En la implementación iterativa, el tamaño del salto se elige como \(\lfloor\sqrt{n}\rfloor\). Así se equilibran las comparaciones de bloques y las comparaciones secuenciales del bloque final.

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
    <tr><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(\Theta(\sqrt{n})\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(\sqrt{n})\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** El objetivo se detecta al inicio del primer bloque o en la primera comparación relevante. El trabajo y el espacio son constantes.
- **Caso promedio.** Se recorren varios bloques y luego una parte del bloque final. Con salto \(\sqrt{n}\), ambas fases quedan acotadas por esa magnitud, así que \(T(n) \in \Theta(\sqrt{n})\).
- **Peor caso.** El objetivo está cerca del final del último bloque o está ausente dentro del rango permitido. El algoritmo hace hasta \(\sqrt{n}\) saltos y hasta \(\sqrt{n}\) comparaciones lineales, lo que produce \(O(\sqrt{n})\).

#### Versión recursiva (ampliación teórica)

El libro no incluye un listado recursivo de este algoritmo en las páginas citadas. Este apartado compara el costo de una posible formulación recursiva; no corresponde a otra implementación transcrita.

En la implementación recursiva, la estructura de fases se mantiene, pero cada salto o avance lineal puede quedar como una llamada pendiente. La pila crece con la cantidad de comparaciones realizadas antes de terminar.

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
    <tr><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(\Theta(\sqrt{n})\)</td><td>\(\Theta(\sqrt{n})\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(\sqrt{n})\)</td><td>\(O(\sqrt{n})\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** La primera llamada resuelve la búsqueda y la pila conserva tamaño constante.
- **Caso promedio.** Las llamadas acumuladas durante saltos y fase lineal crecen como \(\Theta(\sqrt{n})\), igual que el número de comparaciones.
- **Peor caso.** El encadenamiento de llamadas puede cubrir todos los saltos y todo el bloque final. El tiempo y la memoria de pila quedan en \(O(\sqrt{n})\).



---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y si el objetivo debe estar presente o ausente.
3. Use el botón `Buscar` para ejecutar la animación paso a paso o de forma automática.
4. Observe los saltos de bloque en bloque y la búsqueda secuencial final.

### Eficiencia por tamaño de arreglo

La siguiente celda simula la búsqueda por saltos sobre arreglos de tamaño creciente y mide el **número de operaciones** necesarias para encontrar el objetivo (siempre presente).

- **Línea sólida** — simulación empírica (n ≤ 5 000, 50 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 10 000 000
- **Checkbox** — superpone la función teórica 2·√(n) normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva crece más rápido que log(n) pero mucho más despacio que n, situando este algoritmo entre la búsqueda secuencial y los algoritmos logarítmicos.

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
    <tr><td>Mejor caso</td><td>\(1\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(2 \cdot \sqrt{n}\)</td><td>\(\Theta(\sqrt{n})\)</td></tr>
    <tr><td>Peor caso</td><td>\(2 \cdot \sqrt{n}\)</td><td>\(O(\sqrt{n})\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio y peor caso** (misma función). El factor \(2\) refleja las dos fases del algoritmo: \(\approx\sqrt{n}\) saltos entre bloques más hasta \(\sqrt{n}\) comparaciones lineales dentro del bloque. Esto distingue la función concreta del simple \(\sqrt{n}\) de la notación asintótica.

\[
f(n) = 2 \cdot \sqrt{n}
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-7/busqueda_salto/busqueda_salto_1.png" alt="Secuencia visual de 7.5 búsqueda por saltos · paso representativo 1 de 4"><figcaption>Secuencia visual de 7.5 búsqueda por saltos · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_salto/busqueda_salto_3.png" alt="Secuencia visual de 7.5 búsqueda por saltos · paso representativo 2 de 4"><figcaption>Secuencia visual de 7.5 búsqueda por saltos · paso representativo 2 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_salto/busqueda_salto_6.png" alt="Secuencia visual de 7.5 búsqueda por saltos · paso representativo 3 de 4"><figcaption>Secuencia visual de 7.5 búsqueda por saltos · paso representativo 3 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_salto/busqueda_salto_promedio_caso_4.png" alt="Visualización del caso promedio de 7.5 búsqueda por saltos"><figcaption>Visualización del caso promedio de 7.5 búsqueda por saltos.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-busquedas/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../3-busqueda-interpolacion/">← 7.4 Búsqueda por interpolación</a><a class="section-step__index" href="../">Capítulo 7</a><a class="section-step__next" href="../5-busqueda-exponencial/">7.6 Búsqueda exponencial →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>
