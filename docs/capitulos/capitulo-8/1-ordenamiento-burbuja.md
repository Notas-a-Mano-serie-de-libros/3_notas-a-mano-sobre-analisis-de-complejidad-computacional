<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# 8.2 Ordenamiento burbuja

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/1_ordenamiento_burbuja.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ordenamiento burbuja compara pares de elementos adyacentes e intercambia los que están en orden incorrecto. Repite este proceso hasta que no hay más intercambios. En cada pasada, el elemento mayor no ordenado queda en su posición final.

Es el algoritmo de ordenamiento más intuitivo pero también el menos eficiente en la práctica para arreglos grandes, con complejidad cuadrática en el caso promedio y peor caso.

### Implementación

=== "Pseudocódigo"

    ```text
    para fin ← n-1 hasta 1
        para i ← 0 hasta fin-1
            si A[i] > A[i+1] intercambiar
    ```

=== "Python"

    ```python
    for end in range(len(a)-1, 0, -1):
        for i in range(end):
            if a[i] > a[i+1]: a[i], a[i+1] = a[i+1], a[i]
    ```

=== "Java"

    ```java
    for(int e=a.length-1;e>0;e--) for(int i=0;i<e;i++) if(a[i]>a[i+1]){int t=a[i];a[i]=a[i+1];a[i+1]=t;}
    ```

=== "C"

    ```c
    for(int e=n-1;e>0;e--) for(int i=0;i<e;i++) if(a[i]>a[i+1]){int t=a[i];a[i]=a[i+1];a[i+1]=t;}
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
4. Observe cómo el mayor elemento no ordenado migra hacia su posición final en cada pasada.

### Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento burbuja sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios.

- **Línea sólida** — simulación empírica (n ≤ 400, 5 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 50 000
- **Checkbox** — superpone la función teórica n²/2 normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva cuadrática crece rápidamente: duplicar n cuadruplica el número de operaciones.

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
    <tr><td>Caso promedio</td><td>\(n^2/2\)</td><td>\(\Theta(n^2)\)</td></tr>
    <tr><td>Peor caso</td><td>\(n \cdot (n-1)/2\)</td><td>\(O(n^2)\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio**: la simulación opera sobre arreglos en orden aleatorio. El mejor caso \(\Omega(n)\) corresponde a un arreglo ya ordenado y no aplica aquí.

\[
f(n) = \frac{n^2}{2}
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_burbuja/ordenamiento_burbuja_1.png" alt="Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 1 de 4"><figcaption>Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_burbuja/ordenamiento_burbuja_4.png" alt="Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 2 de 4"><figcaption>Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 2 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_burbuja/ordenamiento_burbuja_7.png" alt="Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 3 de 4"><figcaption>Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 3 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-8/ordenamiento_burbuja/ordenamiento_burbuja_11.png" alt="Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 4 de 4"><figcaption>Secuencia visual de 8.2 ordenamiento burbuja · paso representativo 4 de 4.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../0-comparacion-ordenamientos/">← 8.1 Comparación general</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../2-ordenamiento-seleccion/">8.3 Ordenamiento por selección →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
