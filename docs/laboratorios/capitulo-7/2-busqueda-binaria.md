# Búsqueda binaria

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 7</span>

La búsqueda binaria compara el elemento central del arreglo con el objetivo. Si no coincide, descarta la mitad donde el objetivo no puede estar y repite el proceso sobre la mitad restante. Requiere que el arreglo esté ordenado.

Cada comparación reduce el espacio de búsqueda a la mitad, lo que produce una complejidad temporal logarítmica: con un millón de elementos basta con unos 20 pasos.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/2_busqueda_binaria.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

## Complejidad: versión iterativa y versión recursiva

La versión iterativa actualiza los límites del intervalo activo dentro de un ciclo. La versión recursiva expresa la misma reducción del intervalo mediante llamadas que reciben los límites actualizados.

La diferencia principal entre ambas implementaciones aparece en el uso de memoria. La versión iterativa reutiliza el mismo marco de ejecución y conserva una cantidad constante de variables auxiliares. La versión recursiva crea un nuevo marco por cada llamada pendiente; por esa razón, la pila de ejecución puede crecer con la cantidad de divisiones, saltos o comparaciones acumuladas.

### Resumen general

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

### Versión iterativa

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

### Versión recursiva

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

Este resumen presenta los resultados generales para las dos formas de implementación. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.


---

## Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y si el objetivo debe estar presente o ausente.
3. Use el botón `Buscar` para ejecutar la animación paso a paso o de forma automática.
4. Observe cómo el algoritmo descarta la mitad del arreglo en cada paso.

## Eficiencia por tamaño de arreglo

La siguiente celda simula la búsqueda binaria sobre arreglos de tamaño creciente y mide el **número de operaciones** necesarias para encontrar el objetivo (siempre presente).

- **Línea sólida** — simulación empírica (n ≤ 5 000, 50 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 10 000 000
- **Checkbox** — superpone la función teórica log₂(n) normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva crece muy despacio: pasar de n = 1 000 a n = 1 000 000 solo duplica el número de pasos.

### Tabla de resultados

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
