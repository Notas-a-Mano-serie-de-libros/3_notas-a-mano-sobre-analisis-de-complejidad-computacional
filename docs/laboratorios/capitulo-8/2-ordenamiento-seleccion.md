# Ordenamiento por selección

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 8</span>

El ordenamiento por selección busca el elemento mínimo en el subarreglo no ordenado y lo coloca al inicio de ese subarreglo, expandiendo la parte ordenada en una posición con cada pasada. Siempre realiza el mismo número de comparaciones independientemente del orden inicial.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/2_ordenamiento_seleccion.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

## Complejidad

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
    <tr><td>Mejor caso</td><td>\(\Omega(n^2)\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(\Theta(n^2)\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(n^2)\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

Este resumen presenta los resultados generales. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.


---

## Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y el orden deseado.
3. Use el botón `Ordenar` para ejecutar la animación paso a paso o de forma automática.
4. Observe cómo se selecciona el mínimo del subarreglo no ordenado y se ubica al frente.

## Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento por selección sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios.

- **Línea sólida** — simulación empírica (n ≤ 400, 5 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 50 000
- **Checkbox** — superpone la función teórica n(n−1)/2 normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva es casi idéntica entre ejecuciones porque el número de comparaciones es determinístico.

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
    <tr><td>Mejor caso</td><td>\(n \cdot (n-1)/2\)</td><td>\(\Omega(n^2)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(n \cdot (n-1)/2\)</td><td>\(\Theta(n^2)\)</td></tr>
    <tr><td>Peor caso</td><td>\(n \cdot (n-1)/2\)</td><td>\(O(n^2)\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa la **función exacta para todos los escenarios**: selección siempre recorre el subarreglo completo para encontrar el mínimo sin importar el orden inicial, por lo que los tres casos comparten el mismo conteo de comparaciones.

\[
f(n) = \frac{n \cdot (n-1)}{2}
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.
