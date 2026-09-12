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

Listado original del libro, página 298 (Java).

```java
public boolean buscar(int[] arr, int x) {
    int n = arr.length;
    // Verificar si el primer elemento es el buscado
    if (arr[0] == x)
        return true;
    // Encuentra el rango utilizando crecimiento exponencial
    int i = 1;
    while (i < n && arr[i] <= x)
        i *= 2;
    // Determina los limites y ejecuta la búsqueda binaria
    int a = i/2;
    int b = Math.min(i, n - 1);
    // Invoca la función que aplica la búsqueda
    return busquedaBinaria(arr, a, b, x);
}
```

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

#### Versión recursiva

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
