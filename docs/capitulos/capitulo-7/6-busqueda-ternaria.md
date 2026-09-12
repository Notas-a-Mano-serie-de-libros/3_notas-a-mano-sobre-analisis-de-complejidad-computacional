<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>

# 7.7 Búsqueda ternaria

<span class="chapter-kicker">Capítulo 7</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/6_busqueda_ternaria.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

La búsqueda ternaria divide el espacio de búsqueda en tres partes iguales calculando dos puntos medios. Compara el objetivo con cada punto medio para descartar un tercio del arreglo en cada iteración. Requiere que el arreglo esté ordenado.

Aunque cada iteración descarta más que la búsqueda binaria (un tercio en vez de la mitad), necesita dos comparaciones por paso, por lo que en la práctica es ligeramente menos eficiente que la búsqueda binaria. En el análisis espacial se toma como referencia la formulación recursiva, donde la pila de llamadas crece con la profundidad de las divisiones.

### Implementación

<!-- book-code:start -->

#### Búsqueda ternaria recursiva

Implementación corregida basada en el libro, página 307 (Java).

=== "Java"

    ```java
    public boolean buscar(int[] arr, int a, int b, int x) {
         // Agota el espacio de búsqueda
        if (a > b)
            return false;
        int m1 = a + (b - a) / 3;
        int m2 = b - (int) Math.ceil((b - a) / 3.0);
        // Verificar si el valor está en los pivotes
        if (arr[m1] == x || arr[m2] == x)
            return true;
        if (x < arr[m1])
            return buscar(arr, a, m1 - 1, x);
        else if (x > arr[m2])
            return buscar(arr, m2 + 1, b, x);
        else
            return buscar(arr, m1 + 1, m2 - 1, x);
    }
    ```

=== "Pseudocódigo"

    ```text
    función buscar(arr, a, b, x)
        si a > b entonces
            retornar falso
        m1 ← a + (b - a) div 3
        m2 ← b - (b - a + 2) div 3
        si arr[m1] == x o arr[m2] == x entonces
            retornar verdadero
        si x < arr[m1] entonces
            retornar buscar(arr, a, m1 - 1, x)
        si x > arr[m2] entonces
            retornar buscar(arr, m2 + 1, b, x)
        retornar buscar(arr, m1 + 1, m2 - 1, x)
    ```

=== "Python"

    ```python
    def buscar(arr, a, b, x):
        if a > b:
            return False
        m1 = a + (b - a) // 3
        m2 = b - (b - a + 2) // 3
        if arr[m1] == x or arr[m2] == x:
            return True
        if x < arr[m1]:
            return buscar(arr, a, m1 - 1, x)
        if x > arr[m2]:
            return buscar(arr, m2 + 1, b, x)
        return buscar(arr, m1 + 1, m2 - 1, x)
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    bool buscar(int arr[], int a, int b, int x) {
         // Agota el espacio de búsqueda
        if (a > b) {
            return false;
        }
        int m1 = a + (b - a) / 3;
        int m2 = b - (int) ceil((b - a) / 3.0);
        // Verificar si el valor está en los pivotes
        if (arr[m1] == x || arr[m2] == x) {
            return true;
        }
        if (x < arr[m1]) {
            return buscar(arr, a, m1 - 1, x);
        }
        else if (x > arr[m2]) {
            return buscar(arr, m2 + 1, b, x);
        }
        else {
            return buscar(arr, m1 + 1, m2 - 1, x);
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo ordenado ascendentemente. |
| `a, b` | Límites inclusivos. |
| `x` | Valor buscado. |
| `m1, m2` | Dos pivotes del intervalo. |

**Precondiciones:** arr no nulo y ordenado; límites válidos para intervalo no vacío.

**Resultado:** Devuelve true si encuentra x; false al agotar el intervalo.

??? example "Ejemplo paso a paso"
    Entrada: `arr = [1, 3, 5, 7, 9], a = 0, b = 4, x = 7`.

    **Prueba de escritorio**

    | Paso | Método | Profundidad | arr | a | b | x | m1 | m2 | Operación ejecutada | Retorno |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 1 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | — | — | Entrada a la llamada. | — |
    | 2 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | — | — | `if a > b:` | — |
    | 3 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | 1 | — | `m1 = a + (b - a) // 3` | — |
    | 4 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | 1 | 2 | `m2 = b - (b - a + 2) // 3` | — |
    | 5 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | 1 | 2 | `if arr[m1] == x or arr[m2] == x:` | — |
    | 6 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | 1 | 2 | `if x < arr[m1]:` | — |
    | 7 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | 1 | 2 | `if x > arr[m2]:` | — |
    | 8 | buscar | 1 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | — | — | Entrada a la llamada. | — |
    | 9 | buscar | 1 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | — | — | `if a > b:` | — |
    | 10 | buscar | 1 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 3 | — | `m1 = a + (b - a) // 3` | — |
    | 11 | buscar | 1 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 3 | 3 | `m2 = b - (b - a + 2) // 3` | — |
    | 12 | buscar | 1 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 3 | 3 | `if arr[m1] == x or arr[m2] == x:` | — |
    | 13 | buscar | 1 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 3 | 3 | `return True`; Termina la llamada. | true |
    | 14 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | 1 | 2 | `return buscar(arr, m2 + 1, b, x)`; Termina la llamada. | true |

    Cada fila muestra el estado después de la operación indicada de la traducción Python de esta variante. «—» indica una variable aún no declarada en esa llamada o un retorno todavía pendiente. La profundidad inicial es 0; cada llamada anidada la incrementa en 1.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-9f32c04be81a">Código Python · Búsqueda ternaria recursiva</label><textarea id="runner-9f32c04be81a" spellcheck="false" wrap="off" rows="14">def buscar(arr, a, b, x):
    if a &gt; b:
        return False
    m1 = a + (b - a) // 3
    m2 = b - (b - a + 2) // 3
    if arr[m1] == x or arr[m2] == x:
        return True
    if x &lt; arr[m1]:
        return buscar(arr, a, m1 - 1, x)
    if x &gt; arr[m2]:
        return buscar(arr, m2 + 1, b, x)
    return buscar(arr, m1 + 1, m2 - 1, x)

# Entradas editables del ejemplo.
arr = [1, 3, 5, 7, 9]
a = 0
b = 4
x = 7

resultado = buscar(arr, a, b, x)
print(&quot;Resultado:&quot;, resultado)
</textarea></details><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Restablecer ejemplo</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Búsqueda ternaria iterativa

Implementación corregida basada en el libro, página 312 (Java).

=== "Java"

    ```java
    public boolean buscar(int[] arr, int a, int b, int x) {
        while (a <= b) {
            int m1 = a + (b - a) / 3;
            int m2 = b - (int) Math.ceil((b - a) / 3.0);
            if (arr[m1] == x || arr[m2] == x)
                return true;
            if (x < arr[m1])
                b = m1 - 1; // Buscar en el primer tercio
            else if (x > arr[m2])
                a = m2 + 1; // Buscar en el último tercio
            else {
                a = m1 + 1; // Buscar en el tercio central
                b = m2 - 1;
            }
        }
        // Elemento no encontrado
        return false;
    }
    ```

=== "Pseudocódigo"

    ```text
    función buscar(arr, a, b, x)
        mientras a <= b
            m1 ← a + (b - a) div 3
            m2 ← b - (b - a + 2) div 3
            si arr[m1] == x o arr[m2] == x entonces
                retornar verdadero
            si x < arr[m1] entonces
                b ← m1 - 1
            si no, si x > arr[m2] entonces
                a ← m2 + 1
            si no
                a ← m1 + 1
                b ← m2 - 1
        retornar falso
    ```

=== "Python"

    ```python
    def buscar(arr, a, b, x):
        while a <= b:
            m1 = a + (b - a) // 3
            m2 = b - (b - a + 2) // 3
            if arr[m1] == x or arr[m2] == x:
                return True
            if x < arr[m1]:
                b = m1 - 1
            elif x > arr[m2]:
                a = m2 + 1
            else:
                a = m1 + 1
                b = m2 - 1
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

    bool buscar(int arr[], int a, int b, int x) {
        while (a <= b) {
            int m1 = a + (b - a) / 3;
            int m2 = b - (int) ceil((b - a) / 3.0);
            if (arr[m1] == x || arr[m2] == x) {
                return true;
            }
            if (x < arr[m1]) {
                b = m1 - 1; // Buscar en el primer tercio
            }
            else if (x > arr[m2]) {
                a = m2 + 1; // Buscar en el último tercio
            }
            else {
                a = m1 + 1; // Buscar en el tercio central
                b = m2 - 1;
            }
        }
        // Elemento no encontrado
        return false;
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo ordenado ascendentemente. |
| `a, b` | Límites inclusivos. |
| `x` | Valor buscado. |
| `m1, m2` | Dos pivotes del intervalo. |

**Precondiciones:** arr no nulo y ordenado; límites válidos para intervalo no vacío.

**Resultado:** Devuelve true si encuentra x; false al agotar el intervalo.

??? example "Ejemplo paso a paso"
    Entrada: `arr = [1, 3, 5, 7, 9], a = 0, b = 4, x = 7`.

    **Prueba de escritorio**

    | Paso | Método | Profundidad | arr | a | b | x | m1 | m2 | Operación ejecutada | Retorno |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 1 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | — | — | Entrada a la llamada. | — |
    | 2 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | — | — | `while a <= b:` | — |
    | 3 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | 1 | — | `m1 = a + (b - a) // 3` | — |
    | 4 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | 1 | 2 | `m2 = b - (b - a + 2) // 3` | — |
    | 5 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | 1 | 2 | `if arr[m1] == x or arr[m2] == x:` | — |
    | 6 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | 1 | 2 | `if x < arr[m1]:` | — |
    | 7 | buscar | 0 | [1, 3, 5, 7, 9] | 0 | 4 | 7 | 1 | 2 | `elif x > arr[m2]:` | — |
    | 8 | buscar | 0 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 1 | 2 | `a = m2 + 1` | — |
    | 9 | buscar | 0 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 1 | 2 | `while a <= b:` | — |
    | 10 | buscar | 0 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 3 | 2 | `m1 = a + (b - a) // 3` | — |
    | 11 | buscar | 0 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 3 | 3 | `m2 = b - (b - a + 2) // 3` | — |
    | 12 | buscar | 0 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 3 | 3 | `if arr[m1] == x or arr[m2] == x:` | — |
    | 13 | buscar | 0 | [1, 3, 5, 7, 9] | 3 | 4 | 7 | 3 | 3 | `return True`; Termina la llamada. | true |

    Cada fila muestra el estado después de la operación indicada de la traducción Python de esta variante. «—» indica una variable aún no declarada en esa llamada o un retorno todavía pendiente. La profundidad inicial es 0; cada llamada anidada la incrementa en 1.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-a9fc79021755">Código Python · Búsqueda ternaria iterativa</label><textarea id="runner-a9fc79021755" spellcheck="false" wrap="off" rows="14">def buscar(arr, a, b, x):
    while a &lt;= b:
        m1 = a + (b - a) // 3
        m2 = b - (b - a + 2) // 3
        if arr[m1] == x or arr[m2] == x:
            return True
        if x &lt; arr[m1]:
            b = m1 - 1
        elif x &gt; arr[m2]:
            a = m2 + 1
        else:
            a = m1 + 1
            b = m2 - 1
    return False

# Entradas editables del ejemplo.
arr = [1, 3, 5, 7, 9]
a = 0
b = 4
x = 7

resultado = buscar(arr, a, b, x)
print(&quot;Resultado:&quot;, resultado)
</textarea></details><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Restablecer ejemplo</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

La animación ejecuta una adaptación Python y registra estados visuales; sus pasos de interfaz no equivalen necesariamente a comparaciones del Java. El contador de eficiencia usa búsquedas sobre un objetivo presente y promedia ensayos. El tiempo teórico se estima a partir de una operación calibrada; no es una medición del listado Java.

El contador de ternaria usa un ciclo: mide una adaptación iterativa y cuenta por separado las dos comparaciones con pivotes.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/core/search/search_metrics.py).

<!-- book-code:end -->

### Complejidad: versión iterativa y versión recursiva

La versión iterativa mantiene los límites del intervalo y calcula dos puntos internos en cada vuelta del ciclo. La versión recursiva hace la misma partición en tres segmentos y continúa con una llamada sobre el tercio que aún puede contener el objetivo.

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
    <tr><td>Iterativa</td><td>Caso promedio</td><td>\(\Theta(\log_3(n))\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Iterativa</td><td>Peor caso</td><td>\(O(\log_3(n))\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Caso promedio</td><td>\(\Theta(\log_3(n))\)</td><td>\(\Theta(\log_3(n))\)</td></tr>
    <tr><td>Recursiva</td><td>Peor caso</td><td>\(O(\log_3(n))\)</td><td>\(O(\log_3(n))\)</td></tr>
  </tbody>
</table>
</div>

#### Versión iterativa

En la implementación iterativa, cada paso calcula \(m_1\) y \(m_2\), compara el objetivo con esos puntos y conserva solo el tercio que puede contenerlo. El espacio auxiliar se mantiene constante porque los límites se actualizan en el mismo marco de ejecución.

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
    <tr><td>Caso promedio</td><td>\(\Theta(\log_3(n))\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(\log_3(n))\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** El objetivo coincide con \(m_1\) o \(m_2\) en la primera partición. Se ejecuta una cantidad constante de comparaciones.
- **Caso promedio.** El objetivo suele encontrarse después de varias particiones. La longitud del intervalo pasa de \(n\) a \(n/3\), luego a \(n/9\) y así sucesivamente, lo que produce \(T(n) \in \Theta(\log_3(n))\) con espacio constante.
- **Peor caso.** La búsqueda continúa hasta que el intervalo queda vacío o tiene un único elemento. La cantidad de niveles queda acotada por \(O(\log_3(n))\) y la memoria iterativa por \(O(1)\).

#### Versión recursiva

En la implementación recursiva, cada partición del arreglo genera una llamada sobre un tercio del intervalo anterior. La profundidad de esa cadena de llamadas es proporcional a \(\log_3(n)\).

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
    <tr><td>Caso promedio</td><td>\(\Theta(\log_3(n))\)</td><td>\(\Theta(\log_3(n))\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(\log_3(n))\)</td><td>\(O(\log_3(n))\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** La primera llamada encuentra el objetivo en uno de los puntos internos. La pila conserva profundidad constante.
- **Caso promedio.** La recursión avanza por una cadena de tercios hasta aproximarse al objetivo. La profundidad esperada es \(\Theta(\log_3(n))\), por eso el tiempo y la memoria de pila comparten esa forma.
- **Peor caso.** La recursión consume la máxima cantidad de particiones antes de terminar. El tiempo y el espacio pertenecen a \(O(\log_3(n))\).



---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y si el objetivo debe estar presente o ausente.
3. Use el botón `Buscar` para ejecutar la animación paso a paso o de forma automática.
4. Observe cómo se calculan dos puntos medios y se descarta un tercio del arreglo en cada paso.

### Eficiencia por tamaño de arreglo

La siguiente celda simula la búsqueda ternaria sobre arreglos de tamaño creciente y mide el **número de operaciones** necesarias para encontrar el objetivo (siempre presente).

- **Línea sólida** — simulación empírica (n ≤ 5 000, 50 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 10 000 000
- **Checkbox** — superpone la función teórica 2·log₃(n) normalizada

El gráfico usa escala logarítmica en ambos ejes. Aunque la base es 3, el doble de comparaciones por iteración la hace ligeramente menos eficiente que la búsqueda binaria.

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
    <tr><td>Caso promedio</td><td>\(2\cdot\log_3(n)\)</td><td>\(\Theta(\log_3(n))\)</td></tr>
    <tr><td>Peor caso</td><td>\(2\cdot\log_3(n)\)</td><td>\(O(\log_3(n))\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio y peor caso** (misma función). El factor \(2\) se debe a que cada iteración necesita **dos comparaciones** para determinar en cuál de los tres segmentos continuar, frente a la única comparación de la búsqueda binaria.

\[
f(n) = 2\cdot\log_3(n)
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.

### Equivalencia asintótica: \(\log_3(n)\) y \(\log_2(n)\)

Cuando se compara con la búsqueda binaria, el costo de la búsqueda ternaria es aproximadamente un **26.2 %** menos eficiente en número de comparaciones, ya que requiere \(2 \cdot \log_3(n)\) operaciones frente a \(\log_2(n)\) de la búsqueda binaria.

Aplicando el cambio de base:

\[
\log_3(n) = \frac{\log_2(n)}{\log_2(3)}
\]

se obtiene la función de la búsqueda ternaria expresada en base 2:

\[
2 \cdot \log_3(n) = \frac{2}{\log_2(3)} \cdot \log_2(n) = \frac{2}{1.585} \cdot \log_2(n) \approx 1.261 \cdot \log_2(n)
\]

Sin embargo, en el límite asintótico, el factor \(\frac{2}{\log_2(3)} \approx 1.261\) es una constante multiplicativa. Las constantes se absorben en la notación \(\Theta\), por lo que la diferencia se vuelve despreciable y ambas búsquedas pertenecen a la misma clase de complejidad:

\[
2 \cdot \log_3(n) \in \Theta(\log_2(n))
\]

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-7/busqueda_ternaria/busqueda_ternaria_ejemplo_1.png" alt="Secuencia visual de 7.7 búsqueda ternaria · paso representativo 1 de 4"><figcaption>Secuencia visual de 7.7 búsqueda ternaria · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_ternaria/busqueda_ternaria_ejemplo_2.png" alt="Secuencia visual de 7.7 búsqueda ternaria · paso representativo 2 de 4"><figcaption>Secuencia visual de 7.7 búsqueda ternaria · paso representativo 2 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_ternaria/busqueda_ternaria_ejemplo_4.png" alt="Secuencia visual de 7.7 búsqueda ternaria · paso representativo 3 de 4"><figcaption>Secuencia visual de 7.7 búsqueda ternaria · paso representativo 3 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_ternaria/busqueda_ternaria_caso_promedio_3.png" alt="Visualización del caso promedio de 7.7 búsqueda ternaria"><figcaption>Visualización del caso promedio de 7.7 búsqueda ternaria.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-busquedas/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../5-busqueda-exponencial/">← 7.6 Búsqueda exponencial</a><a class="section-step__index" href="../">Capítulo 7</a><a class="section-step__next" href="../ejercicios-propuestos/">7.9 Ejercicios propuestos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>
