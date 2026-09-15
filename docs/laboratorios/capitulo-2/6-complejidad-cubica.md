# Complejidad cúbica

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 2</span>

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo2/notebooks/6_complejidad_cubica.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Algoritmo simulado: multiplicación clásica de matrices

El ejemplo calcula cada posición de la matriz resultado mediante tres índices: fila, columna y posición interna de acumulación.

Como los tres recorridos dependen de \(n\), el número total de operaciones crece de acuerdo con \(n^3\).


---

## Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

## Detalle teórico

La complejidad cúbica aparece cuando tres recorridos anidados dependen del tamaño \(n\). Este patrón es común en algoritmos que combinan tres dimensiones o tres índices.

Un ejemplo representativo es la multiplicación clásica de matrices cuadradas, donde cada posición del resultado se calcula acumulando productos a lo largo de una tercera dimensión.

Para una entrada de tamaño \(n\), una función de costo cúbico puede expresarse como:

\[
T(n) = c \cdot n^3
\]

donde \(n^3\) representa la cantidad de iteraciones producidas por tres ciclos anidados.

El crecimiento es muy pronunciado: duplicar \(n\) puede multiplicar el trabajo aproximadamente por ocho.

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Complejidad cúbica | `jupyter lab simulaciones/capitulo2/notebooks/6_complejidad_cubica.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->
