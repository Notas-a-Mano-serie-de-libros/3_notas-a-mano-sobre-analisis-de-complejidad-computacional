# Complejidad exponencial

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 2</span>

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/8_complejidad_exponencial.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

## Algoritmo simulado: Fibonacci recursivo sin memoización

El ejemplo calcula Fibonacci mediante dos llamadas recursivas en cada paso no trivial. Muchas llamadas repiten los mismos subproblemas, lo que genera un árbol de ejecución grande.

Esta repetición explica por qué el tiempo crece de forma exponencial cuando \(n\) aumenta.


---

## Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

## Detalle teórico

La complejidad exponencial aparece cuando cada llamada o decisión abre múltiples ramas nuevas. El número de subproblemas crece de forma multiplicativa.

Este tipo de crecimiento se vuelve costoso muy rápido. Incluso incrementos pequeños en \(n\) pueden producir aumentos grandes en el tiempo de ejecución.

Para una entrada de tamaño \(n\), una función de costo exponencial puede expresarse como:

\[
T(n) = c2^n
\]

donde \(2^n\) representa un árbol de decisiones que duplica aproximadamente la cantidad de trabajo por cada incremento de \(n\).

La base puede cambiar según el algoritmo, pero la característica importante es que la variable aparece en el exponente.
