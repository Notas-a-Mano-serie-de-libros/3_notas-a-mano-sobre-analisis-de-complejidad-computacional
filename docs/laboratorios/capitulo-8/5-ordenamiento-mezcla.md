# Ordenamiento por mezcla

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 8</span>

El ordenamiento por mezcla (merge sort) divide el arreglo a la mitad de forma recursiva hasta obtener subarreglos de un solo elemento, que por definición están ordenados. Luego combina (mezcla) los subarreglos en orden creciente hasta reconstruir el arreglo completo.

Garantiza O(n log(n)) en todos los casos, lo que lo hace predecible y eficiente, aunque requiere O(n) de memoria auxiliar para la fase de mezcla.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/5_ordenamiento_mezcla.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

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
    <tr><td>Mejor caso</td><td>\(\Omega(n \cdot \log_2(n))\)</td><td>\(\Omega(n)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(\Theta(n \cdot \log_2(n))\)</td><td>\(\Theta(n)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(n \cdot \log_2(n))\)</td><td>\(O(n)\)</td></tr>
  </tbody>
</table>
</div>

Este resumen presenta los resultados generales. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.


---

## Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y el orden deseado.
3. Use el botón `Ordenar` para ejecutar la animación paso a paso o de forma automática.
4. Observe las fases de división y mezcla del arreglo.

## Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento por mezcla sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios.

- **Línea sólida** — simulación empírica (n ≤ 2 000, 5 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 1 000 000
- **Checkbox** — superpone la función teórica n·log₂(n) normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva crece mucho más despacio que los algoritmos O(n²), lo que refleja la ventaja del enfoque divide y vencerás.

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
    <tr><td>Mejor caso</td><td>\(n\cdot\log_2(n)\)</td><td>\(\Omega(n\cdot\log_2(n))\)</td></tr>
    <tr><td>Caso promedio</td><td>\(n\cdot\log_2(n)\)</td><td>\(\Theta(n\cdot\log_2(n))\)</td></tr>
    <tr><td>Peor caso</td><td>\(n\cdot\log_2(n)\)</td><td>\(O(n\cdot\log_2(n))\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa la **función exacta para todos los escenarios**: ordenamiento por mezcla tiene complejidad uniforme porque siempre divide y mezcla con la misma estructura recursiva, independientemente del orden inicial.

\[
f(n) = n\cdot\log_2(n)
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.
