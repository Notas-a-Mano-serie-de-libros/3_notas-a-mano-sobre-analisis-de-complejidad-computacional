# Búsqueda secuencial

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 7</span>

La búsqueda secuencial (o lineal) recorre el arreglo posición por posición, comparando cada elemento con el objetivo. No requiere que el arreglo esté ordenado; basta con acceder a los elementos en cualquier orden. Si el arreglo está ordenado, la búsqueda puede detenerse anticipadamente al encontrar un elemento mayor que el objetivo, aunque esto no mejora el peor caso.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/1_busqueda_secuencial.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

## Complejidad: versión iterativa y versión recursiva

La versión iterativa usa un ciclo que avanza desde la primera posición hasta encontrar el objetivo o agotar el arreglo. La versión recursiva reemplaza ese ciclo por llamadas sucesivas que revisan una posición y delegan el resto del recorrido a la siguiente llamada.

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
    <tr><td>Iterativa</td><td>Caso promedio</td><td>\(\Theta(n)\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Iterativa</td><td>Peor caso</td><td>\(O(n)\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Caso promedio</td><td>\(\Theta(n)\)</td><td>\(\Theta(n)\)</td></tr>
    <tr><td>Recursiva</td><td>Peor caso</td><td>\(O(n)\)</td><td>\(O(n)\)</td></tr>
  </tbody>
</table>
</div>

### Versión iterativa

En la implementación iterativa, el algoritmo mantiene únicamente el índice de avance y algunas variables auxiliares constantes. El número de comparaciones depende de la posición del objetivo dentro del arreglo.

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
    <tr><td>Caso promedio</td><td>\(\Theta(n)\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(n)\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** El objetivo está en la primera posición. Se realiza una comparación y el recorrido termina de inmediato, por eso \(T(n) \in \Omega(1)\) y \(S(n) \in \Theta(1)\).
- **Caso promedio.** Si el objetivo puede aparecer con la misma probabilidad en cualquier posición, el algoritmo revisa aproximadamente la mitad del arreglo. El costo esperado es proporcional a \(n/2\), por lo que \(T(n) \in \Theta(n)\) y el espacio auxiliar permanece constante.
- **Peor caso.** El objetivo está en la última posición o está ausente. Se revisan las \(n\) posiciones, de modo que \(T(n) \in O(n)\) y \(S(n) \in O(1)\).

### Versión recursiva

En la implementación recursiva, cada llamada representa la comparación de una posición. La cantidad de comparaciones se conserva, pero cada llamada queda registrada temporalmente en la pila de ejecución hasta que se alcanza el caso base.

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
    <tr><td>Caso promedio</td><td>\(\Theta(n)\)</td><td>\(\Theta(n)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(n)\)</td><td>\(O(n)\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** La primera llamada encuentra el objetivo. La pila contiene una cantidad constante de llamadas activas, así que el tiempo y el espacio son constantes.
- **Caso promedio.** La llamada exitosa suele aparecer alrededor de la mitad del arreglo. Se acumulan alrededor de \(n/2\) llamadas, por eso el tiempo y la pila crecen linealmente.
- **Peor caso.** La recursión avanza hasta la última posición o hasta el caso base de ausencia. Se realizan \(n\) comparaciones y se acumulan \(n\) niveles de pila, de modo que \(T(n) \in O(n)\) y \(S(n) \in O(n)\).

Este resumen presenta los resultados generales para las dos formas de implementación. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.


---

## Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y si el objetivo debe estar presente o ausente.
3. Use el botón `Buscar` para ejecutar la animación paso a paso o de forma automática.
4. Observe cómo el algoritmo revisa cada posición en orden.

## Eficiencia por tamaño de arreglo

La siguiente celda simula la búsqueda secuencial sobre arreglos de tamaño creciente y mide el **número de operaciones** necesarias para encontrar el objetivo (siempre presente).

- **Línea sólida** — simulación empírica (n ≤ 5 000, 50 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 10 000 000
- **Checkbox** — superpone la función teórica n/2 normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva crece linealmente: duplicar n duplica el número de pasos.

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
    <tr><td>Caso promedio</td><td>\(n/2\)</td><td>\(\Theta(n)\)</td></tr>
    <tr><td>Peor caso</td><td>\(n\)</td><td>\(O(n)\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio**: la simulación busca un elemento siempre presente en una posición aleatoria uniforme, por lo que en promedio se recorre la mitad del arreglo. El mejor caso \(\Omega(1)\) es demasiado infrecuente para ser representativo.

\[
f(n) = \frac{n}{2}
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.
