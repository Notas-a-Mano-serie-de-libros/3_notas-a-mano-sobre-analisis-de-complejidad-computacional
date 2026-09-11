# Búsqueda por saltos

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 7</span>

La búsqueda por saltos avanza en bloques de tamaño √n hasta encontrar un elemento mayor que el objetivo o alcanzar el final del arreglo. Luego realiza una búsqueda secuencial hacia atrás dentro del bloque acotado. Requiere que el arreglo esté ordenado.

El bloque óptimo de tamaño √n balancea los saltos hacia adelante con la búsqueda secuencial hacia atrás, produciendo una complejidad de O(√n).

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/4_busqueda_saltos.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

## Complejidad: versión iterativa y versión recursiva

La versión iterativa combina una fase de saltos por bloques con una fase secuencial dentro del bloque final. La versión recursiva puede modelar cada salto y cada avance lineal como llamadas sucesivas.

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
    <tr><td>Iterativa</td><td>Caso promedio</td><td>\(\Theta(\sqrt{n})\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Iterativa</td><td>Peor caso</td><td>\(O(\sqrt{n})\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Caso promedio</td><td>\(\Theta(\sqrt{n})\)</td><td>\(\Theta(\sqrt{n})\)</td></tr>
    <tr><td>Recursiva</td><td>Peor caso</td><td>\(O(\sqrt{n})\)</td><td>\(O(\sqrt{n})\)</td></tr>
  </tbody>
</table>
</div>

### Versión iterativa

En la implementación iterativa, el tamaño del salto se elige como \(\lfloor\sqrt{n}\rfloor\). Así se equilibran las comparaciones de bloques y las comparaciones secuenciales del bloque final.

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
    <tr><td>Caso promedio</td><td>\(\Theta(\sqrt{n})\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(\sqrt{n})\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** El objetivo se detecta al inicio del primer bloque o en la primera comparación relevante. El trabajo y el espacio son constantes.
- **Caso promedio.** Se recorren varios bloques y luego una parte del bloque final. Con salto \(\sqrt{n}\), ambas fases quedan acotadas por esa magnitud, así que \(T(n) \in \Theta(\sqrt{n})\).
- **Peor caso.** El objetivo está cerca del final del último bloque o está ausente dentro del rango permitido. El algoritmo hace hasta \(\sqrt{n}\) saltos y hasta \(\sqrt{n}\) comparaciones lineales, lo que produce \(O(\sqrt{n})\).

### Versión recursiva

En la implementación recursiva, la estructura de fases se mantiene, pero cada salto o avance lineal puede quedar como una llamada pendiente. La pila crece con la cantidad de comparaciones realizadas antes de terminar.

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
    <tr><td>Caso promedio</td><td>\(\Theta(\sqrt{n})\)</td><td>\(\Theta(\sqrt{n})\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(\sqrt{n})\)</td><td>\(O(\sqrt{n})\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** La primera llamada resuelve la búsqueda y la pila conserva tamaño constante.
- **Caso promedio.** Las llamadas acumuladas durante saltos y fase lineal crecen como \(\Theta(\sqrt{n})\), igual que el número de comparaciones.
- **Peor caso.** El encadenamiento de llamadas puede cubrir todos los saltos y todo el bloque final. El tiempo y la memoria de pila quedan en \(O(\sqrt{n})\).

Este resumen presenta los resultados generales para las dos formas de implementación. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.


---

## Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y si el objetivo debe estar presente o ausente.
3. Use el botón `Buscar` para ejecutar la animación paso a paso o de forma automática.
4. Observe los saltos de bloque en bloque y la búsqueda secuencial final.

## Eficiencia por tamaño de arreglo

La siguiente celda simula la búsqueda por saltos sobre arreglos de tamaño creciente y mide el **número de operaciones** necesarias para encontrar el objetivo (siempre presente).

- **Línea sólida** — simulación empírica (n ≤ 5 000, 50 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 10 000 000
- **Checkbox** — superpone la función teórica 2·√(n) normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva crece más rápido que log(n) pero mucho más despacio que n, situando este algoritmo entre la búsqueda secuencial y los algoritmos logarítmicos.

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
    <tr><td>Caso promedio</td><td>\(2 \cdot \sqrt{n}\)</td><td>\(\Theta(\sqrt{n})\)</td></tr>
    <tr><td>Peor caso</td><td>\(2 \cdot \sqrt{n}\)</td><td>\(O(\sqrt{n})\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio y peor caso** (misma función). El factor \(2\) refleja las dos fases del algoritmo: \(\approx\sqrt{n}\) saltos entre bloques más hasta \(\sqrt{n}\) comparaciones lineales dentro del bloque. Esto distingue la función concreta del simple \(\sqrt{n}\) de la notación asintótica.

\[
f(n) = 2 \cdot \sqrt{n}
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.
