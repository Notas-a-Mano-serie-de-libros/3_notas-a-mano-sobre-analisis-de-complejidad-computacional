# Complejidad lineal

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 2</span>

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo2/notebooks/3_complejidad_lineal.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Algoritmo simulado: búsqueda secuencial en una lista

El ejemplo recorre la lista de izquierda a derecha hasta encontrar el objetivo o agotar la entrada. En el peor caso, el elemento no aparece y la función revisa todos los valores.

Cada elemento se evalúa una vez. Por eso el tiempo de ejecución observado tiende a crecer junto con la cantidad de datos.


---

## Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

## Detalle teórico

La complejidad lineal describe algoritmos cuyo costo crece de forma proporcional al tamaño de la entrada. Si la entrada tiene más elementos, el algoritmo puede necesitar más pasos en la misma proporción.

Este comportamiento aparece cuando el procedimiento debe inspeccionar cada elemento o avanzar secuencialmente hasta encontrar una condición. La forma del trabajo no cambia, pero se repite una vez por cada dato disponible.

Para una entrada de tamaño \(n\), una función de costo lineal puede expresarse como:

\[
T(n) = c \cdot n
\]

donde \(c\) representa el costo constante de procesar un elemento y \(n\) representa la cantidad de elementos de la entrada.

La expresión indica que el costo aumenta al mismo ritmo que la entrada. Si se duplican los elementos, el número esperado de operaciones también se duplica aproximadamente.

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Complejidad lineal | `jupyter lab simulaciones/capitulo2/notebooks/3_complejidad_lineal.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->
