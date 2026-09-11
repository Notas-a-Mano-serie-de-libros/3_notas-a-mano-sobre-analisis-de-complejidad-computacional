# Visualización de la fórmula de interpolación

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 7</span>

La interpolación lineal es una técnica para estimar el valor \(y\) que corresponde a un punto \(x\) dentro de un intervalo \([x_0, x_1]\), conociendo únicamente los valores de la función en sus extremos: \((x_0,\,y_0)\) y \((x_1,\,y_1)\).

El principio es geométrico: se traza una línea recta entre ambos puntos de referencia y se evalúa esa recta en \(x\). La fórmula que expresa esta idea es:

\[
y = y_0 + \frac{(y_1 - y_0) \cdot (x - x_0)}{x_1 - x_0}
\]

El cociente \(\dfrac{x - x_0}{x_1 - x_0}\) mide la posición relativa de \(x\) dentro del intervalo: vale \(0\) cuando \(x = x_0\) y vale \(1\) cuando \(x = x_1\). En cualquier punto intermedio, representa la fracción del recorrido horizontal ya completado.

Multiplicar esa fracción por \((y_1 - y_0)\) escala el cambio vertical total del intervalo según cuánto avanzó \(x\) desde \(x_0\). Sumar \(y_0\) al resultado desplaza el cálculo para que parta desde el primer punto de referencia.

El valor obtenido es el punto sobre la recta que une \((x_0, y_0)\) con \((x_1, y_1)\), no necesariamente el valor real de la función en \(x\). La diferencia entre ambos constituye el **error de aproximación**, y depende de la curvatura de la función y de qué tan separados se encuentren los extremos del intervalo.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/3_busqueda_interpolacion.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

## Simulación interactiva

La siguiente simulación permite explorar visualmente cómo se comporta la fórmula sobre diferentes funciones.

La **curva azul** es la función real \(f(x)\) evaluada sobre el dominio \([0, n]\). La **línea roja discontinua** es la recta de interpolación: la secante que une los puntos \((x_0, y_0)\) y \((x_1, y_1)\), que actúan como extremos del intervalo de estimación. El **punto rojo** sobre esa recta es el valor estimado \(y\) para el \(x\) seleccionado; el **punto verde** es el valor real \(f(x)\).

La **barra naranja** vertical entre ambos puntos representa el error de la aproximación. Cuando la función es lineal, la recta de interpolación coincide exactamente con la curva y el error es nulo. A medida que la función presenta mayor curvatura, o a medida que el intervalo \([x_0, x_1]\) se amplía, el error crece.

Los controles permiten cambiar la función \(f(x)\), ajustar el dominio total mediante \(n\) —lo que reposiciona automáticamente los extremos a \((0,\,f(0))\) y \((n,\,f(n))\)—, mover los extremos del intervalo con los deslizadores \(x_0\) y \(x_1\), y seleccionar el punto de consulta \(x\) con el deslizador central o arrastrando directamente sobre la gráfica.


---

## Búsqueda por interpolación

La búsqueda por interpolación estima la posición del objetivo usando interpolación lineal: en vez de ir siempre al centro, salta a una posición proporcional al valor buscado. Requiere que el arreglo esté ordenado.

Para distribuciones uniformes alcanza O(log(log(n))) en el caso promedio, lo que la hace sublogarítmica. Sin embargo, si la distribución no es uniforme el peor caso es O(n).

## Complejidad: versión iterativa y versión recursiva

La versión iterativa recalcula la posición estimada dentro de un ciclo mientras el objetivo permanezca dentro del rango de valores activo. La versión recursiva convierte cada estimación fallida en una llamada sobre el subrango restante.

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
    <tr><td>Iterativa</td><td>Caso promedio</td><td>\(\Theta(\log_2(\log_2(n)))\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Iterativa</td><td>Peor caso</td><td>\(O(n)\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Mejor caso</td><td>\(\Omega(1)\)</td><td>\(\Omega(1)\)</td></tr>
    <tr><td>Recursiva</td><td>Caso promedio</td><td>\(\Theta(\log_2(\log_2(n)))\)</td><td>\(\Theta(\log_2(\log_2(n)))\)</td></tr>
    <tr><td>Recursiva</td><td>Peor caso</td><td>\(O(n)\)</td><td>\(O(n)\)</td></tr>
  </tbody>
</table>
</div>

### Versión iterativa

En la implementación iterativa, la estimación usa los valores de los extremos para saltar a una posición proporcional al objetivo. El caso promedio doblemente logarítmico depende de una distribución aproximadamente uniforme.

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
    <tr><td>Caso promedio</td><td>\(\Theta(\log_2(\log_2(n)))\)</td><td>\(\Theta(1)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(n)\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** La primera estimación coincide con el objetivo. Se realiza una cantidad constante de trabajo y \(T(n) \in \Omega(1)\).
- **Caso promedio.** Con datos uniformemente distribuidos, la estimación queda cerca de la posición real y el intervalo se reduce muy rápido. Ese comportamiento lleva a \(T(n) \in \Theta(\log_2(\log_2(n)))\) con espacio constante.
- **Peor caso.** Cuando los valores están muy desbalanceados, la estimación puede avanzar muy poco en cada iteración. En ese escenario se pueden revisar muchos candidatos y \(T(n) \in O(n)\).

### Versión recursiva

En la implementación recursiva, cada llamada calcula una posición estimada y continúa sobre el subrango que aún puede contener el objetivo. La memoria adicional queda determinada por la cantidad de estimaciones encadenadas.

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
    <tr><td>Caso promedio</td><td>\(\Theta(\log_2(\log_2(n)))\)</td><td>\(\Theta(\log_2(\log_2(n)))\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(n)\)</td><td>\(O(n)\)</td></tr>
  </tbody>
</table>
</div>

- **Mejor caso.** La primera llamada estima la posición exacta. La pila mantiene una profundidad constante.
- **Caso promedio.** En distribución uniforme, la profundidad esperada de llamadas sigue la misma forma doblemente logarítmica del tiempo: \(\Theta(\log_2(\log_2(n)))\).
- **Peor caso.** Con una distribución adversa, la recursión puede encadenar una cantidad lineal de llamadas. Por eso el tiempo y la pila pertenecen a \(O(n)\).

Este resumen presenta los resultados generales para las dos formas de implementación. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.

## Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo y si el objetivo debe estar presente o ausente.
3. Use el botón `Buscar` para ejecutar la animación paso a paso o de forma automática.
4. Observe cómo el algoritmo salta a posiciones distintas del centro según el valor buscado.

## Eficiencia por tamaño de arreglo

La siguiente celda simula la búsqueda por interpolación sobre arreglos de tamaño creciente con distribución **uniforme** y mide el **número de operaciones** necesarias para encontrar el objetivo.

- **Línea sólida** — simulación empírica (n ≤ 5 000, 50 ensayos por tamaño)
- **Línea discontinua** — extrapolación analítica hasta n = 10 000 000
- **Checkbox** — superpone la función teórica log₂(log₂(n)) + 1 normalizada

El gráfico usa escala logarítmica en ambos ejes. La curva es la más plana de todos los algoritmos, lo que refleja su crecimiento doblemente sublogarítmico bajo distribución uniforme.

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
    <tr><td>Caso promedio</td><td>\(\log_2(\log_2(n))\)</td><td>\(\Theta(\log_2(\log_2(n)))\)</td></tr>
    <tr><td>Peor caso</td><td>\(n\)</td><td>\(O(n)\)</td></tr>
  </tbody>
</table>
</div>

> El desarrollo que lleva a estas funciones exactas está documentado en la obra.

La tabla usa el **caso promedio**: la simulación genera arreglos con distribución uniforme, condición bajo la cual la interpolación converge de forma doblemente logarítmica. El \(+1\) estabiliza la función para valores pequeños de \(n\). El peor caso \(O(n)\) —distribución no uniforme— no se observa aquí.

\[
f(n) = \log_2(\log_2(n)) + 1
\]

El tiempo teórico se estima como:

\[
T_{\text{teórico}}(n) = T_0 \times f(n)
\]

donde \(T_0\) es el tiempo promedio de una comparación entera básica, medido automáticamente: se cronometran \(10^6\) iteraciones de una comparación simple y se divide el tiempo total entre el número de iteraciones.

> El tiempo teórico asume una implementación eficiente de bajo nivel; por eso es varios órdenes de magnitud menor que el tiempo de simulación en Python.

## Análisis experimental del caso promedio: medición original

La búsqueda por interpolación aprovecha una propiedad adicional del arreglo ordenado: la relación entre el valor buscado y su posición. Cuando los valores están distribuidos de manera aproximadamente uniforme, un valor cercano al inicio del rango suele aparecer cerca del inicio del arreglo, un valor cercano al final suele aparecer cerca del final y un valor intermedio suele ubicarse alrededor de una posición intermedia.

La estimación de la posición usa esa relación proporcional. En cada iteración se calcula una posición tentativa dentro del intervalo activo y, si el objetivo no aparece allí, el intervalo se reduce. Bajo una distribución uniforme, esa estimación tiende a quedar cerca de la posición real, por lo que el número promedio de reducciones crece muy lentamente. Ese comportamiento se resume con:

\[
T(n) \in \Theta(\log_2(\log_2(n)))
\]

La celda siguiente reproduce el experimento base. Para cada valor conceptual de \(n\), se construye un arreglo uniformemente distribuido con `50000` elementos entre `1` y `n`. Luego se seleccionan `1000` objetivos pertenecientes al arreglo y se mide el tiempo promedio requerido para encontrarlos. El uso de `timeit.repeat` ayuda a reducir el efecto de mediciones atípicas causadas por el entorno de ejecución, y la semilla fija permite repetir el experimento con el mismo conjunto de muestras aleatorias.

El tamaño físico del arreglo se mantiene constante para que el experimento se concentre en el efecto del rango de valores y en la calidad de la interpolación. A medida que \(n\) aumenta, los datos siguen siendo uniformes, pero las posiciones estimadas dependen de valores cada vez más separados. La gráfica permite observar si la tendencia experimental conserva la forma de crecimiento esperada para el caso promedio.

## Función ajustada

Después de obtener los tiempos experimentales, se ajusta una función con la misma forma del crecimiento promedio esperado:

\[
f(n) = a\cdot\log_2(\log_2(n)) + b
\]

El parámetro \(a\) escala la curva para adaptarla a la unidad de tiempo medida en la máquina donde se ejecuta el notebook. El parámetro \(b\) representa un desplazamiento vertical asociado con costos constantes, como llamadas a función, comparaciones, acceso al arreglo y sobrecarga del temporizador. Estos parámetros permiten comparar la forma de la curva teórica con los datos reales sin exigir que ambas coincidan exactamente en magnitud.

El ajuste cumple una función empírica: permite verificar si los datos medidos siguen una tendencia compatible con el crecimiento doblemente logarítmico. Una coincidencia visual razonable y errores pequeños sugieren que el experimento refleja el comportamiento promedio esperado para datos uniformemente distribuidos.

## Comparación entre medición y ajuste

La siguiente gráfica superpone los tiempos experimentales y la curva ajustada. La escala logarítmica en ambos ejes facilita observar cambios pequeños cuando los tamaños conceptuales crecen varios órdenes de magnitud. En una búsqueda por interpolación con datos uniformes, la curva ajustada debe avanzar lentamente y acompañar la dirección general de los puntos medidos.

Las diferencias entre los puntos y la curva forman parte normal de una medición experimental. El tiempo observado puede variar por caché, planificación del sistema operativo, estado del intérprete, ruido del entorno local o de Colab y precisión del temporizador. Por esa razón, la lectura principal debe centrarse en la tendencia global, acompañada luego por métricas de error.

Si la curva roja se mantiene cerca de los datos experimentales en la mayor parte del rango, el resultado respalda que la función \(\log_2(\log_2(n))\) describe de manera adecuada el crecimiento promedio observado en este escenario controlado.

## Error cuadrático medio

El error cuadrático medio (`MSE`) resume la distancia entre los tiempos medidos y los tiempos estimados por la función ajustada. Para cada tamaño \(n\), se calcula la diferencia entre el dato experimental y el valor de la curva; luego esa diferencia se eleva al cuadrado y se promedia sobre todas las mediciones.

\[
MSE = \frac{1}{k}\sum_{i=1}^{k}(t_i - \hat{t}_i)^2
\]

Aquí, \(t_i\) representa el tiempo medido para el tamaño \(n_i\), \(\hat{t}_i\) representa el tiempo estimado por la función ajustada y \(k\) es la cantidad de mediciones. Como el error se eleva al cuadrado, las desviaciones grandes pesan más que las pequeñas. Además, la unidad del `MSE` queda expresada en segundos cuadrados, por lo que conviene complementarlo con métricas en segundos y con una gráfica de residuos.

## Residuos y calidad del ajuste

Los residuos permiten ver el error de manera localizada. Cada residuo se calcula como:

\[
r_i = t_i - \hat{t}_i
\]

Un residuo positivo indica que la medición fue mayor que la estimación de la curva. Un residuo negativo indica que la medición fue menor que la estimación. Cuando los residuos quedan cerca de cero y no muestran una tendencia creciente clara, el ajuste describe bien el patrón general de los datos.

Además del `MSE`, se calculan métricas complementarias:

- `RMSE`: raíz del error cuadrático medio. Mantiene la unidad original de los tiempos, segundos.
- `MAE`: error absoluto medio. Mide el tamaño promedio del error sin elevarlo al cuadrado.
- `R²`: proporción de variación explicada por la curva ajustada. Un valor cercano a `1` indica mejor ajuste global.
- Error relativo medio: compara el error absoluto con el tamaño de la medición correspondiente.

Estas métricas ayudan a separar dos preguntas distintas: qué tan bien sigue la curva la tendencia general y qué tan grandes son los errores en la escala de los tiempos medidos.
