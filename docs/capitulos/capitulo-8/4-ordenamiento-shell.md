<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# Ampliación · Ordenamiento Shell

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/4_ordenamiento_shell.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ordenamiento Shell generaliza la idea del ordenamiento por inserción. En lugar de comparar solo elementos contiguos, primero compara elementos separados por un valor h determinado. Después reduce progresivamente ese valor h hasta llegar a 1, momento en el que realiza una pasada equivalente a inserción sobre un arreglo que ya quedó parcialmente organizado.

La ventaja práctica aparece porque los elementos pueden desplazarse grandes distancias durante las primeras pasadas. Cuando h se vuelve pequeño, el arreglo suele estar mucho más cerca de su posición final y las pasadas restantes requieren menos movimientos.

### Implementación

<!-- book-code:start -->

#### Shell con separaciones divididas entre dos

Implementación de ampliación del sitio (Java); no es un listado del PDF.

=== "Java"

    ```java
    public void ordenar(int[] arr) {
        int n = arr.length;
        for (int paso = n / 2; paso > 0; paso /= 2) {
            for (int i = paso; i < n; i++) {
                int clave = arr[i];
                int j = i;
                while (j >= paso && arr[j - paso] > clave) {
                    arr[j] = arr[j - paso];
                    j -= paso;
                }
                arr[j] = clave;
            }
        }
    }
    ```

=== "Pseudocódigo"

    ```text
    función ordenar(arr)
        n ← longitud(arr)
        paso ← n div 2
        mientras paso > 0
            para i en rango(paso, n)
                clave ← arr[i]
                j ← i
                mientras j >= paso y arr[j - paso] > clave
                    arr[j] ← arr[j - paso]
                    j -= paso
                arr[j] ← clave
            paso //= 2
    ```

=== "Python"

    ```python
    def ordenar(arr):
        n = len(arr)
        paso = n // 2
        while paso > 0:
            for i in range(paso, n):
                clave = arr[i]
                j = i
                while j >= paso and arr[j - paso] > clave:
                    arr[j] = arr[j - paso]
                    j -= paso
                arr[j] = clave
            paso //= 2
    ```

=== "C"

    ```c
    void ordenar(int arr[], int n) {
        for (int paso = n / 2; paso > 0; paso /= 2) {
            for (int i = paso; i < n; i++) {
                int clave = arr[i];
                int j = i;
                while (j >= paso && arr[j - paso] > clave) {
                    arr[j] = arr[j - paso];
                    j -= paso;
                }
                arr[j] = clave;
            }
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

En C, `n` indica la longitud del arreglo y se recibe como parámetro.

| Parámetro o variable | Significado |
| --- | --- |
| `arr` | Arreglo que se modifica durante el ordenamiento. |
| `n` | Longitud del arreglo. |
| `paso` | Separación entre los elementos comparados. |
| `i` | Posición del elemento que se inserta. |
| `clave` | Valor del elemento que se inserta. |
| `j` | Posición actual durante los desplazamientos. |

**Precondiciones:** arr no nulo.

**Resultado:** Ordena arr de menor a mayor; admite el arreglo vacío.

**Explicación:** Esta implementación es una ampliación del sitio; el PDF proporcionado no incluye un listado de Shell.

??? example "Ejemplo paso a paso"
    Entrada: `arr = [3, 1, 2]`.

    **Prueba de escritorio**

    | Paso | Método | Profundidad | arr | n | paso | i | clave | j | Operación ejecutada | Retorno |
    | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
    | 1 | ordenar | 0 | [3, 1, 2] | — | — | — | — | — | Entrada a la llamada. | — |
    | 2 | ordenar | 0 | [3, 1, 2] | 3 | — | — | — | — | `n = len(arr)` | — |
    | 3 | ordenar | 0 | [3, 1, 2] | 3 | 1 | — | — | — | `paso = n // 2` | — |
    | 4 | ordenar | 0 | [3, 1, 2] | 3 | 1 | — | — | — | `while paso > 0:` | — |
    | 5 | ordenar | 0 | [3, 1, 2] | 3 | 1 | 1 | — | — | `for i in range(paso, n):` | — |
    | 6 | ordenar | 0 | [3, 1, 2] | 3 | 1 | 1 | 1 | — | `clave = arr[i]` | — |
    | 7 | ordenar | 0 | [3, 1, 2] | 3 | 1 | 1 | 1 | 1 | `j = i` | — |
    | 8 | ordenar | 0 | [3, 1, 2] | 3 | 1 | 1 | 1 | 1 | `while j >= paso and arr[j - paso] > clave:` | — |
    | 9 | ordenar | 0 | [3, 3, 2] | 3 | 1 | 1 | 1 | 1 | `arr[j] = arr[j - paso]` | — |
    | 10 | ordenar | 0 | [3, 3, 2] | 3 | 1 | 1 | 1 | 0 | `j -= paso` | — |
    | 11 | ordenar | 0 | [3, 3, 2] | 3 | 1 | 1 | 1 | 0 | `while j >= paso and arr[j - paso] > clave:` | — |
    | 12 | ordenar | 0 | [1, 3, 2] | 3 | 1 | 1 | 1 | 0 | `arr[j] = clave` | — |
    | 13 | ordenar | 0 | [1, 3, 2] | 3 | 1 | 2 | 1 | 0 | `for i in range(paso, n):` | — |
    | 14 | ordenar | 0 | [1, 3, 2] | 3 | 1 | 2 | 2 | 0 | `clave = arr[i]` | — |
    | 15 | ordenar | 0 | [1, 3, 2] | 3 | 1 | 2 | 2 | 2 | `j = i` | — |
    | 16 | ordenar | 0 | [1, 3, 2] | 3 | 1 | 2 | 2 | 2 | `while j >= paso and arr[j - paso] > clave:` | — |
    | 17 | ordenar | 0 | [1, 3, 3] | 3 | 1 | 2 | 2 | 2 | `arr[j] = arr[j - paso]` | — |
    | 18 | ordenar | 0 | [1, 3, 3] | 3 | 1 | 2 | 2 | 1 | `j -= paso` | — |
    | 19 | ordenar | 0 | [1, 3, 3] | 3 | 1 | 2 | 2 | 1 | `while j >= paso and arr[j - paso] > clave:` | — |
    | 20 | ordenar | 0 | [1, 2, 3] | 3 | 1 | 2 | 2 | 1 | `arr[j] = clave` | — |
    | 21 | ordenar | 0 | [1, 2, 3] | 3 | 1 | 2 | 2 | 1 | `for i in range(paso, n):` | — |
    | 22 | ordenar | 0 | [1, 2, 3] | 3 | 0 | 2 | 2 | 1 | `paso //= 2` | — |
    | 23 | ordenar | 0 | [1, 2, 3] | 3 | 0 | 2 | 2 | 1 | `while paso > 0:`; Termina la llamada. | sin valor |

    Cada fila muestra el estado después de la operación indicada de la traducción Python de esta variante. «—» indica una variable aún no declarada en esa llamada o un retorno todavía pendiente. La profundidad inicial es 0; cada llamada anidada la incrementa en 1.

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-3bd6cf69710c">Código Python · Shell con separaciones divididas entre dos</label><textarea id="runner-3bd6cf69710c" spellcheck="false" wrap="off" rows="14">def ordenar(arr):
    n = len(arr)
    paso = n // 2
    while paso &gt; 0:
        for i in range(paso, n):
            clave = arr[i]
            j = i
            while j &gt;= paso and arr[j - paso] &gt; clave:
                arr[j] = arr[j - paso]
                j -= paso
            arr[j] = clave
        paso //= 2

# Entradas editables del ejemplo.
arr = [3, 1, 2]

print(&quot;Arreglo inicial:&quot;, arr)
ordenar(arr)
print(&quot;Arreglo ordenado:&quot;, arr)
</textarea></details><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Restablecer ejemplo</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

La animación y el contador son adaptaciones Python con operaciones instrumentadas. Incluyen comparaciones, movimientos y control del recorrido según el contador; no se deben interpretar todos los pasos como una sola clase de operación Java. Las opciones descendentes son ampliaciones: los listados del libro ordenan ascendentemente.

Shell es una ampliación digital y no tiene un listado correspondiente en este libro.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/core/sort/sort_algorithms.py).

<!-- book-code:end -->

### Complejidad

<div style="display:flex; justify-content:center; margin:1.2em 0;">
<table style="margin: 0 auto; text-align: center;">
  <thead>
    <tr>
      <th>Secuencia de h</th>
      <th>Mejor caso</th>
      <th>Caso promedio</th>
      <th>Peor caso</th>
      <th>Espacio</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Shell: n/2, n/4, ..., 1</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>Depende de los datos</td><td>\(O(n^2)\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Hibbard: \(2^k - 1\)</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>Depende de los datos</td><td>\(O(n^{3/2})\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Sedgewick</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>Depende de los datos</td><td>Aproximadamente \(O(n^{4/3})\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Pratt: \(2^i3^j\)</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>Depende de los datos</td><td>\(O(n \cdot \log_2^2(n))\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

Shell sort no tiene una única complejidad temporal fija, porque el número de comparaciones y movimientos depende directamente de la secuencia de h. Con la secuencia original propuesta por Shell, el peor caso sigue siendo cuadrático. Con secuencias mejor diseñadas, como Hibbard, Sedgewick o Pratt, el comportamiento mejora de forma importante.

La complejidad espacial se mantiene constante, ya que el algoritmo opera directamente sobre el arreglo original y solo necesita variables auxiliares para el valor actual de \(h\), los índices y el intercambio de valores.


---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo, la vista, el orden y la secuencia de h.
3. Use `Paso siguiente` para avanzar una comparación o intercambio a la vez.
4. Use `Ejecución automática` para observar toda la ejecución.
5. Cambie el campo `h` para comparar cómo se modifica el recorrido interno del algoritmo.

### Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento Shell sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios usando la secuencia original de Shell.

- **Línea sólida** — simulación empírica sobre varios tamaños de arreglo.
- **Línea discontinua** — extrapolación analítica para observar la tendencia cuando el tamaño crece.
- **Checkbox** — superpone una referencia cuadrática normalizada para la secuencia original.

La comparación experimental debe interpretarse como una referencia para la secuencia seleccionada en la implementación. El análisis formal cambia cuando se modifica la secuencia de h, por eso el resumen anterior separa Shell, Hibbard, Sedgewick y Pratt.

#### Tabla de resultados

La tabla muestra, para cada tamaño de arreglo \(n\) evaluado:

- **Operaciones teóricas** y **Tiempo teórico**: calculados con la función de referencia usada para la curva superpuesta.
- **Operaciones obtenidas** y **Tiempo experimental**: valores medidos por la simulación.
- **Error absoluto** y **Error relativo**: diferencia entre la referencia teórica escalada y los resultados obtenidos.

### Comparación de secuencias de h

La siguiente animación ejecuta Shell sort en paralelo sobre el mismo arreglo usando las secuencias Shell, Hibbard, Sedgewick y Pratt. La columna **Pasos** permite comparar cuántas operaciones visibles necesita cada técnica para completar el ordenamiento bajo las mismas condiciones iniciales.

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../3-ordenamiento-insercion/">← 8.4 Ordenamiento por inserción</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../5-ordenamiento-mezcla/">8.5 Ordenamiento por mezcla →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
