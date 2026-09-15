# Complejidad exponencial

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 2</span>

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo2/notebooks/8_complejidad_exponencial.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

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
T(n) = c \cdot 2^n
\]

donde \(2^n\) representa un árbol de decisiones que duplica aproximadamente la cantidad de trabajo por cada incremento de \(n\).

La base puede cambiar según el algoritmo, pero la característica importante es que la variable aparece en el exponente.

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Complejidad exponencial | `jupyter lab simulaciones/capitulo2/notebooks/8_complejidad_exponencial.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->
