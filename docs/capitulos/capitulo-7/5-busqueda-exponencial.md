<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>

# 7.6 Búsqueda exponencial

<span class="chapter-kicker">Capítulo 7</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/5_busqueda_exponencial.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

La búsqueda exponencial localiza el rango donde puede estar el objetivo duplicando el índice en cada paso (1, 2, 4, 8, 16, …) hasta encontrar un elemento mayor o igual al objetivo. Luego aplica búsqueda binaria sobre ese rango acotado. Requiere que el arreglo esté ordenado.

Es especialmente eficaz cuando el objetivo está cerca del inicio del arreglo, ya que la fase de duplicación llega rápidamente al rango correcto.

### Implementación

<!-- book-code:start -->

#### Búsqueda exponencial con búsqueda binaria auxiliar

Implementación corregida basada en el libro, página 298 (Java).

=== "Java"

    ```java
    public boolean buscar(int[] arr, int x) {
        int n = arr.length;
        if (n == 0)
            return false;
        // Verificar si el primer elemento es el buscado
        if (arr[0] == x)
            return true;
        // Encuentra el rango utilizando crecimiento exponencial
        int i = 1;
        while (i < n && arr[i] <= x)
            i = (int) Math.min((long) i * 2, n);
        // Determina los limites y ejecuta la búsqueda binaria
        int a = i/2;
        int b = Math.min(i, n - 1);
        // Invoca la función que aplica la búsqueda
        return busquedaBinaria(arr, a, b, x);
    }

    public boolean busquedaBinaria(int[] arr, int a, int b, int x) {
        while (a <= b) {
            // Posición en la mitad del rango [a,b]
            int m = a + (b - a) / 2;
            if (arr[m] == x)
                return true; // Elemento encontrado
            else if (x > arr[m])
                a = m + 1; // Buscar en la mitad derecha
            else
                b = m - 1; // Buscar en la mitad izquierda
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
        si arr[0] == x entonces
            retornar verdadero
        i ← 1
        mientras i < n y arr[i] <= x
            i ← min(i * 2, n)
        a ← i div 2
        b ← min(i, n - 1)
        retornar busquedaBinaria(arr, a, b, x)


    función busquedaBinaria(arr, a, b, x)
        mientras a <= b
            m ← a + (b - a) div 2
            si arr[m] == x entonces
                retornar verdadero
            si x > arr[m] entonces
                a ← m + 1
            si no
                b ← m - 1
        retornar falso
    ```

=== "Python"

    ```python
    def buscar(arr, x):
        n = len(arr)
        if n == 0:
            return False
        if arr[0] == x:
            return True
        i = 1
        while i < n and arr[i] <= x:
            i = min(i * 2, n)
        a = i // 2
        b = min(i, n - 1)
        return busquedaBinaria(arr, a, b, x)


    def busquedaBinaria(arr, a, b, x):
        while a <= b:
            m = a + (b - a) // 2
            if arr[m] == x:
                return True
            if x > arr[m]:
                a = m + 1
            else:
                b = m - 1
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

    bool busquedaBinaria(int arr[], int a, int b, int x);

    bool buscar(int arr[], int n, int x) {
            if (n == 0) {
            return false;
            }
        // Verificar si el primer elemento es el buscado
        if (arr[0] == x) {
            return true;
        }
        // Encuentra el rango utilizando crecimiento exponencial
        int i = 1;
        while (i < n && arr[i] <= x) {
            i = (int) minimo((int64_t) i * 2, n);
        }
        // Determina los limites y ejecuta la búsqueda binaria
        int a = i/2;
        int b = minimo(i, n - 1);
        // Invoca la función que aplica la búsqueda
        return busquedaBinaria(arr, a, b, x);
    }

    bool busquedaBinaria(int arr[], int a, int b, int x) {
        while (a <= b) {
            // Posición en la mitad del rango [a,b]
            int m = a + (b - a) / 2;
            if (arr[m] == x) {
                return true; // Elemento encontrado
            }
            else if (x > arr[m]) {
                a = m + 1; // Buscar en la mitad derecha
            }
            else {
                b = m - 1; // Buscar en la mitad izquierda
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
| `i` | Límite que se duplica. |
| `a, b` | Intervalo que se envía a la auxiliar. |
| `busquedaBinaria` | Auxiliar incluida en el listado corregido. |

**Precondiciones:** arr no nulo y ordenado de menor a mayor.

**Resultado:** Devuelve el resultado booleano de la búsqueda auxiliar.

**Explicación:** El arreglo vacío devuelve false. La actualización del avance se calcula en long y se limita a arr.length antes de convertirla a int; no se exige que la suma o duplicación previa quepa en int.

??? example "Ejemplo paso a paso"
    Entrada: `arr = [1, 3, 5, 7, 9], x = 7`.

    **Prueba de escritorio**

    | Paso | Método | Profundidad | arr | x | n | i | a | b | m | Operación ejecutada | Retorno |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 1 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | — | — | — | — | — | Entrada a la llamada. | — |
    | 2 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | — | — | — | — | `n = len(arr)` | — |
    | 3 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | — | — | — | — | `if n == 0:` | — |
    | 4 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | — | — | — | — | `if arr[0] == x:` | — |
    | 5 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 1 | — | — | — | `i = 1` | — |
    | 6 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 1 | — | — | — | `while i < n and arr[i] <= x:` | — |
    | 7 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | — | — | — | `i = min(i * 2, n)` | — |
    | 8 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 2 | — | — | — | `while i < n and arr[i] <= x:` | — |
    | 9 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 4 | — | — | — | `i = min(i * 2, n)` | — |
    | 10 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 4 | — | — | — | `while i < n and arr[i] <= x:` | — |
    | 11 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 4 | 2 | — | — | `a = i // 2` | — |
    | 12 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 4 | 2 | 4 | — | `b = min(i, n - 1)` | — |
    | 13 | busquedaBinaria | 1 | [1, 3, 5, 7, 9] | 7 | — | — | 2 | 4 | — | Entrada a la llamada. | — |
    | 14 | busquedaBinaria | 1 | [1, 3, 5, 7, 9] | 7 | — | — | 2 | 4 | — | `while a <= b:` | — |
    | 15 | busquedaBinaria | 1 | [1, 3, 5, 7, 9] | 7 | — | — | 2 | 4 | 3 | `m = a + (b - a) // 2` | — |
    | 16 | busquedaBinaria | 1 | [1, 3, 5, 7, 9] | 7 | — | — | 2 | 4 | 3 | `if arr[m] == x:` | — |
    | 17 | busquedaBinaria | 1 | [1, 3, 5, 7, 9] | 7 | — | — | 2 | 4 | 3 | `return True`; Termina la llamada. | true |
    | 18 | buscar | 0 | [1, 3, 5, 7, 9] | 7 | 5 | 4 | 2 | 4 | — | `return busquedaBinaria(arr, a, b, x)`; Termina la llamada. | true |

    Cada fila muestra el estado después de la operación indicada de la traducción Python de esta variante. «—» indica una variable aún no declarada en esa llamada o un retorno todavía pendiente. La profundidad inicial es 0; cada llamada anidada la incrementa en 1.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-64abd99494fb">Código Python · Búsqueda exponencial con búsqueda binaria auxiliar</label><textarea id="runner-64abd99494fb" spellcheck="false" wrap="off" rows="14">def buscar(arr, x):
    n = len(arr)
    if n == 0:
        return False
    if arr[0] == x:
        return True
    i = 1
    while i &lt; n and arr[i] &lt;= x:
        i = min(i * 2, n)
    a = i // 2
    b = min(i, n - 1)
    return busquedaBinaria(arr, a, b, x)


def busquedaBinaria(arr, a, b, x):
    while a &lt;= b:
        m = a + (b - a) // 2
        if arr[m] == x:
            return True
        if x &gt; arr[m]:
            a = m + 1
        else:
            b = m - 1
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

La versión iterativa primero duplica el índice para acotar el rango y luego ejecuta búsqueda binaria sobre ese intervalo. La versión recursiva puede expresar la duplicación y la búsqueda binaria final mediante llamadas sobre rangos cada vez más definidos.

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
    <tr><td>Iterativa</td><td>Caso promedio</td><td>\(\Theta(\log_2(n))\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Iterativa</td><td>Peor caso</td><td>\(O(\log_2(n))\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Caso promedio</td><td>\(\Theta(\log_2(n))\)</td><td>\(\Theta(\log_2(n))\)</td></tr>
    <tr><td>Recursiva</td><td>Peor caso</td><td>\(O(\log_2(n))\)</td><td>\(O(\log_2(n))\)</td></tr>
  </tbody>
</table>
</div>

#### Versión iterativa

En la implementación iterativa, la fase exponencial necesita pocas comparaciones para ubicar un intervalo cuyo extremo superior supera o alcanza el objetivo. La fase binaria final conserva el crecimiento logarítmico.

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
    <tr><td>Caso promedio</td><td>\(\Theta(\log_2(n))\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(\log_2(n))\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** El objetivo está en la primera posición revisada. La búsqueda termina con trabajo constante y espacio constante.
- **Caso promedio.** La fase de duplicación acota el rango en una cantidad logarítmica de pasos y la fase binaria consume otra cantidad logarítmica. La suma conserva \(T(n) \in \Theta(\log_2(n))\).
- **Peor caso.** El objetivo está hacia el final o está ausente. La expansión alcanza el límite superior y la búsqueda binaria explora el rango acotado, por lo que \(T(n) \in O(\log_2(n))\) y \(S(n) \in O(1)\).

#### Versión recursiva (ampliación teórica)

El libro no incluye un listado recursivo de este algoritmo en las páginas citadas. Este apartado compara el costo de una posible formulación recursiva; no corresponde a otra implementación transcrita.

En la implementación recursiva, la fase de expansión y la fase binaria pueden apilar llamadas. La cantidad total de niveles sigue siendo logarítmica porque los índices crecen por duplicación y el rango final se divide a la mitad.

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
    <tr><td>Caso promedio</td><td>\(\Theta(\log_2(n))\)</td><td>\(\Theta(\log_2(n))\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(\log_2(n))\)</td><td>\(O(\log_2(n))\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** La primera llamada confirma el objetivo y la profundidad de pila es constante.
- **Caso promedio.** Las llamadas de expansión más las llamadas de búsqueda binaria crecen de forma logarítmica. La pila pertenece a \(\Theta(\log_2(n))\) cuando las fases se implementan recursivamente.
- **Peor caso.** La recursión alcanza la mayor cantidad de duplicaciones y divisiones binarias. El tiempo y la memoria de pila quedan en \(O(\log_2(n))\).



---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y si el objetivo debe estar presente o ausente.
3. Use el botón `Buscar` para ejecutar la animación paso a paso o de forma automática.
4. Observe la fase de saltos exponenciales y la búsqueda binaria final.

### Eficiencia por tamaño de arreglo

La siguiente celda simula la búsqueda exponencial sobre arreglos de tamaño creciente y mide el **número de operaciones** necesarias para encontrar el objetivo (siempre presente).

- **Línea sólida** — simulación empírica (n ≤ 5 000, 50 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 10 000 000
- **Checkbox** — superpone la función teórica 1.6·log₂(n) normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva es logarítmica, igual que la búsqueda binaria, aunque con una constante ligeramente mayor por combinar dos fases.

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
    <tr><td>Caso promedio</td><td>\(1.6\cdot\log_2(n)\)</td><td>\(\Theta(\log_2(n))\)</td></tr>
    <tr><td>Peor caso</td><td>\(1.6\cdot\log_2(n)\)</td><td>\(O(\log_2(n))\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio y peor caso** (misma función). El factor \(1.6\) refleja que el algoritmo combina dos fases logarítmicas —exponencial y binaria—, resultando en la práctica en \(\approx 1.6\) veces más comparaciones que la búsqueda binaria pura.

\[
f(n) = 1.6\cdot\log_2(n)
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-7/busqueda_exponencial/busqueda_exponencial_ejemplo_1.png" alt="Secuencia visual de 7.6 búsqueda exponencial · paso representativo 1 de 4"><figcaption>Secuencia visual de 7.6 búsqueda exponencial · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_exponencial/busqueda_exponencial_ejemplo_3.png" alt="Secuencia visual de 7.6 búsqueda exponencial · paso representativo 2 de 4"><figcaption>Secuencia visual de 7.6 búsqueda exponencial · paso representativo 2 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_exponencial/busqueda_exponencial_ejemplo_6.png" alt="Secuencia visual de 7.6 búsqueda exponencial · paso representativo 3 de 4"><figcaption>Secuencia visual de 7.6 búsqueda exponencial · paso representativo 3 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_exponencial/busqueda_exponencial_caso_promedio.png" alt="Visualización del caso promedio de 7.6 búsqueda exponencial"><figcaption>Visualización del caso promedio de 7.6 búsqueda exponencial.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-busquedas/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../4-busqueda-saltos/">← 7.5 Búsqueda por saltos</a><a class="section-step__index" href="../">Capítulo 7</a><a class="section-step__next" href="../6-busqueda-ternaria/">7.7 Búsqueda ternaria →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>
