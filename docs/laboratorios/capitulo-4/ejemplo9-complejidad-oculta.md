# Ejemplo 9: Complejidad oculta

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 4</span>

El algoritmo de Fibonacci es iterativo, pero los enteros crecen con \(n\). La simulación permite observar el costo que introduce el tamaño creciente de esos valores.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo9_(complejidad_oculta).ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

## Código analizado


---

## Análisis esperado

### Complejidad temporal

El ciclo tiene \(n\) iteraciones, pero cada suma opera sobre enteros cada vez más grandes; el costo real puede superar el modelo unitario \(O(n)\).

### Complejidad espacial

Los enteros de Fibonacci necesitan más bits a medida que aumenta \(n\), por lo que la memoria observada también crece.

## Simulaciones experimentales

Cada experimento ejecuta el mismo algoritmo para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La preparación de la entrada se realiza fuera de la medición temporal. En memoria se reporta el espacio adicional utilizado durante la operación.
