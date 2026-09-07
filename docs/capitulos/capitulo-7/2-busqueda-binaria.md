<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>

# 7.3 Búsqueda binaria

<span class="chapter-kicker">Capítulo 7</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/2_busqueda_binaria.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar notebook en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

La búsqueda binaria compara el elemento central del arreglo con el objetivo. Si no coincide, descarta la mitad donde el objetivo no puede estar y repite el proceso sobre la mitad restante. Requiere que el arreglo esté ordenado.

Cada comparación reduce el espacio de búsqueda a la mitad, lo que produce una complejidad temporal logarítmica: con un millón de elementos basta con unos 20 pasos.

### Implementación

=== "Pseudocódigo"

    ```text
    izq ← 0; der ← longitud(A)-1
    mientras izq ≤ der
        m ← ⌊(izq+der)/2⌋
        si A[m] = x retornar m
        si A[m] < x: izq ← m+1; si no: der ← m-1
    retornar -1
    ```

=== "Python"

    ```python
    lo, hi = 0, len(a)-1
    while lo <= hi:
        m = (lo+hi)//2
        if a[m] == x: return m
        if a[m] < x: lo = m+1
        else: hi = m-1
    return -1
    ```

=== "Java"

    ```java
    int lo=0, hi=a.length-1;
    while(lo<=hi){ int m=lo+(hi-lo)/2; if(a[m]==x)return m; if(a[m]<x)lo=m+1; else hi=m-1; }
    return -1;
    ```

=== "C"

    ```c
    int lo=0, hi=n-1;
    while(lo<=hi){ int m=lo+(hi-lo)/2; if(a[m]==x)return m; if(a[m]<x)lo=m+1; else hi=m-1; }
    return -1;
    ```

### Complejidad: versión iterativa y versión recursiva

La versión iterativa actualiza los límites del intervalo activo dentro de un ciclo. La versión recursiva expresa la misma reducción del intervalo mediante llamadas que reciben los límites actualizados.

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

En la implementación iterativa, cada comparación calcula el índice medio y conserva solo los límites \(a\) y \(b\). Cada descarte reduce el intervalo activo a la mitad.

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

- **Mejor caso.** El objetivo coincide con el primer índice medio. Se ejecuta una comparación efectiva, entonces \(T(n) \in \Omega(1)\) y el espacio auxiliar es constante.
- **Caso promedio.** El objetivo aparece en un nivel intermedio del árbol de decisiones. La cantidad esperada de divisiones es proporcional a \(\log_2(n)\), por lo que \(T(n) \in \Theta(\log_2(n))\).
- **Peor caso.** El intervalo se divide hasta quedar vacío o hasta alcanzar un único elemento. La profundidad máxima es \(\lceil \log_2(n) \rceil\), por eso \(T(n) \in O(\log_2(n))\) y \(S(n) \in O(1)\).

#### Versión recursiva

En la implementación recursiva, cada llamada recibe un intervalo cuya longitud es aproximadamente la mitad de la anterior. El número de comparaciones es el mismo orden que en la versión iterativa, pero la pila crece con la profundidad de divisiones.

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

- **Mejor caso.** La primera llamada encuentra el objetivo en el medio. La pila activa conserva una profundidad constante.
- **Caso promedio.** La búsqueda desciende por varios niveles del árbol binario de decisiones. El tiempo esperado y el número de llamadas activas crecen como \(\Theta(\log_2(n))\).
- **Peor caso.** La recursión alcanza la máxima profundidad antes de encontrar el objetivo o confirmar su ausencia. El tiempo y la memoria de pila pertenecen a \(O(\log_2(n))\).



---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y si el objetivo debe estar presente o ausente.
3. Use el botón `Buscar` para ejecutar la animación paso a paso o de forma automática.
4. Observe cómo el algoritmo descarta la mitad del arreglo en cada paso.

### Eficiencia por tamaño de arreglo

La siguiente celda simula la búsqueda binaria sobre arreglos de tamaño creciente y mide el **número de operaciones** necesarias para encontrar el objetivo (siempre presente).

- **Línea sólida** — simulación empírica (n ≤ 5 000, 50 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 10 000 000
- **Checkbox** — superpone la función teórica log₂(n) normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva crece muy despacio: pasar de n = 1 000 a n = 1 000 000 solo duplica el número de pasos.

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
    <tr><td>Caso promedio</td><td>\(\log_2(n)\)</td><td>\(\Theta(\log_2(n))\)</td></tr>
    <tr><td>Peor caso</td><td>\(\log_2(n)\)</td><td>\(O(\log_2(n))\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio** (equivalente al peor caso en orden asintótico): la simulación busca un elemento en posición aleatoria. El mejor caso \(\Omega(1)\) se descarta por ser infrecuente.

\[
f(n) = \log_2(n)
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-7/busqueda_binaria/busqueda_binaria_ejemplo_1.png" alt="Secuencia visual de 7.3 búsqueda binaria · paso representativo 1 de 4"><figcaption>Secuencia visual de 7.3 búsqueda binaria · paso representativo 1 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_binaria/busqueda_binaria_ejemplo_2.png" alt="Secuencia visual de 7.3 búsqueda binaria · paso representativo 2 de 4"><figcaption>Secuencia visual de 7.3 búsqueda binaria · paso representativo 2 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_binaria/busqueda_binaria_ejemplo_3.png" alt="Secuencia visual de 7.3 búsqueda binaria · paso representativo 3 de 4"><figcaption>Secuencia visual de 7.3 búsqueda binaria · paso representativo 3 de 4.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-7/busqueda_binaria/busqueda_binaria_ejemplo_caso_promedio_2.png" alt="Visualización del caso promedio de 7.3 búsqueda binaria"><figcaption>Visualización del caso promedio de 7.3 búsqueda binaria.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-busquedas/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../1-busqueda-secuencial/">← 7.2 Búsqueda secuencial</a><a class="section-step__index" href="../">Capítulo 7</a><a class="section-step__next" href="../3-busqueda-interpolacion/">7.4 Búsqueda por interpolación →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>
