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

=== "Pseudocódigo"

    ```text
    mientras izq ≤ der
        m1 ← izq+(der-izq)/3; m2 ← der-(der-izq)/3
        comparar x con A[m1] y A[m2]
        conservar uno de los tres intervalos
    retornar -1
    ```

=== "Python"

    ```python
    lo, hi = 0, len(a)-1
    while lo <= hi:
        third = (hi-lo)//3; m1, m2 = lo+third, hi-third
        if a[m1] == x: return m1
        if a[m2] == x: return m2
        if x < a[m1]: hi = m1-1
        elif x > a[m2]: lo = m2+1
        else: lo, hi = m1+1, m2-1
    return -1
    ```

=== "Java"

    ```java
    int lo=0,hi=a.length-1; while(lo<=hi){int t=(hi-lo)/3,m1=lo+t,m2=hi-t;if(a[m1]==x)return m1;if(a[m2]==x)return m2;if(x<a[m1])hi=m1-1;else if(x>a[m2])lo=m2+1;else{lo=m1+1;hi=m2-1;}}return -1;
    ```

=== "C"

    ```c
    int lo=0,hi=n-1; while(lo<=hi){int t=(hi-lo)/3,m1=lo+t,m2=hi-t;if(a[m1]==x)return m1;if(a[m2]==x)return m2;if(x<a[m1])hi=m1-1;else if(x>a[m2])lo=m2+1;else{lo=m1+1;hi=m2-1;}}return -1;
    ```

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
