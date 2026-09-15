# Complejidad cuadrática

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 2</span>

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo2/notebooks/5_complejidad_cuadratica.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Algoritmo simulado: recorrer una matriz

El ejemplo recorre todas las posiciones de una matriz. Si la matriz tiene \(n\) filas y \(n\) columnas, el cuerpo interno se ejecuta \(n \times n\) veces.

La estructura de dos ciclos anidados hace que el número de accesos crezca cuadráticamente con el tamaño lateral de la matriz.


---

## Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

## Detalle teórico

La complejidad cuadrática describe algoritmos cuyo costo crece con el cuadrado del tamaño de entrada. Suele aparecer cuando dos ciclos anidados dependen de \(n\).

En estos casos, cada elemento puede relacionarse con muchos otros elementos, o se recorre una estructura bidimensional de tamaño \(n \times n\).

Para una entrada de tamaño \(n\), una función de costo cuadrático puede expresarse como:

\[
T(n) = c \cdot n^2
\]

donde \(c\) representa el costo constante de cada operación elemental y \(n^2\) representa la cantidad de combinaciones o posiciones evaluadas.

El crecimiento es mucho más rápido que el lineal: duplicar \(n\) puede multiplicar el trabajo aproximadamente por cuatro.

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Complejidad cuadrática | `jupyter lab simulaciones/capitulo2/notebooks/5_complejidad_cuadratica.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->
