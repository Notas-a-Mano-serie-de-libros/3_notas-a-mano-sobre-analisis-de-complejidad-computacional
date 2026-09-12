<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# 8.4 Ordenamiento por inserción

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/3_ordenamiento_insercion.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ordenamiento por inserción construye el arreglo ordenado de izquierda a derecha: toma cada elemento y lo inserta en su posición correcta dentro del subarreglo ya ordenado, desplazando los elementos mayores hacia la derecha.

Es muy eficiente para arreglos casi ordenados (O(n) en el mejor caso) y es el algoritmo preferido para arreglos pequeños dentro de implementaciones híbridas como Timsort.

### Implementación

=== "Pseudocódigo"

    ```text
    para i ← 1 hasta n-1
        clave ← A[i]; j ← i-1
        desplazar valores mayores que clave
        insertar clave en j+1
    ```

=== "Python"

    ```python
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0 and a[j] > key:
            a[j + 1], j = a[j], j - 1
        a[j + 1] = key
    ```

=== "Java"

    ```java
    for (int i = 1; i < a.length; i++) {
        int k = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > k) {
            a[j + 1] = a[j--];
        }
        a[j + 1] = k;
    }
    ```

=== "C"

    ```c
    for (int i = 1; i < n; i++) {
        int k = a[i];
        int j = i - 1;
        while (j >= 0 && a[j] > k) {
            a[j + 1] = a[j--];
        }
        a[j + 1] = k;
    }
    ```

### Complejidad

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
    <tr><td>Mejor caso</td><td>\(\Omega(n)\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(\Theta(n^2)\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(n^2)\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

Este resumen presenta los resultados generales. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.


---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y el orden deseado.
3. Use el botón `Ordenar` para ejecutar la animación paso a paso o de forma automática.
4. Observe cómo cada nuevo elemento se inserta en su lugar correcto dentro de la parte ya ordenada.

### Variante: inserción binaria

El ordenamiento por inserción localiza, para cada elemento, la posición que debe ocupar dentro del prefijo ya ordenado. En la versión clásica esa búsqueda se hace de derecha a izquierda mediante comparaciones consecutivas. La variante de **inserción binaria** aprovecha que el prefijo `arr[0:i]` ya está ordenado y usa búsqueda binaria para encontrar la posición de inserción.

La mejora principal está en la cantidad de comparaciones usadas para decidir la posición del elemento: en lugar de revisar linealmente el prefijo, la búsqueda binaria reduce el rango activo a la mitad en cada comparación. Esto puede bajar las comparaciones de búsqueda de un comportamiento lineal por iteración a uno logarítmico por iteración.

El desplazamiento de elementos sigue siendo necesario, porque insertar dentro de un arreglo exige mover una sección hacia la derecha para abrir espacio. Por eso la complejidad temporal total permanece cuadrática en el peor caso, aunque el número de comparaciones puede disminuir de forma importante.

### Comparación entre inserción clásica e inserción binaria

La siguiente animación ejecuta ambas variantes sobre el mismo arreglo. La columna **Pasos** permite observar cómo cambia el número de operaciones visibles cuando la posición de inserción se localiza mediante búsqueda lineal o mediante búsqueda binaria.

### Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento por inserción sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios.

- **Línea sólida** — simulación empírica (n ≤ 400, 5 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 50 000
- **Checkbox** — superpone la función teórica n²/4 normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva cuadrática es similar a la de burbuja, aunque con una constante menor que refleja que inserción hace menos movimientos en promedio.

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
    <tr><td>Mejor caso</td><td>\(n\)</td><td>\(\Omega(n)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(n^2/4\)</td><td>\(\Theta(n^2)\)</td></tr>
    <tr><td>Peor caso</td><td>\(n^2/2\)</td><td>\(O(n^2)\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio**: la simulación opera sobre arreglos aleatorios. El factor \(1/4\) (frente al \(1/2\) del peor caso) refleja que en promedio cada elemento recorre la mitad del subarreglo ya ordenado. El mejor caso \(\Omega(n)\) corresponde a un arreglo ya ordenado y no aplica aquí.

\[
f(n) = \frac{n^2}{4}
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_insercion/ordenamiento_insercion_1.png" alt="Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 1 de 4"><figcaption>Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_insercion/ordenamiento_insercion_4.png" alt="Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 2 de 4"><figcaption>Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 2 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_insercion/ordenamiento_insercion_7.png" alt="Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 3 de 4"><figcaption>Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 3 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_insercion/ordenamiento_insercion_11.png" alt="Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 4 de 4"><figcaption>Secuencia visual de 8.4 ordenamiento por inserción · paso representativo 4 de 4.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../2-ordenamiento-seleccion/">← 8.3 Ordenamiento por selección</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../4-ordenamiento-shell/">Ampliación · Ordenamiento Shell →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
