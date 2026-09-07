# Complejidad factorial

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 2</span>

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/9_complejidad_factorial.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

## Algoritmo simulado: contar permutaciones

El ejemplo cuenta las permutaciones explorando cada posible elección del primer elemento y repitiendo el proceso con los elementos restantes.

La cantidad de ramas generadas sigue la forma factorial, porque cada nivel reduce la lista en un elemento pero multiplica las posibilidades acumuladas.


---

## Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

## Detalle teórico

La complejidad factorial aparece cuando el algoritmo explora todas las permutaciones posibles de una colección. Para \(n\) elementos existen \(n!\) ordenamientos diferentes.

Este crecimiento es incluso más agresivo que muchas formas exponenciales. Por eso estos algoritmos solo son viables para entradas muy pequeñas.

Para una entrada de tamaño \(n\), una función de costo factorial puede expresarse como:

\[
T(n) = cn!
\]

donde \(n!\) representa el producto \(n 	imes (n-1) 	imes (n-2) 	imes \cdots 	imes 1\).

Cada nuevo elemento multiplica la cantidad de permutaciones posibles, por lo que el costo se dispara rápidamente.
