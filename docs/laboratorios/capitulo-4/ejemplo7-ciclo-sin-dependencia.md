# Ejemplo 7: Ciclo sin dependencia de la entrada

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 4</span>

El ciclo ejecuta siempre \(10\,000\) iteraciones. Esa cantidad es fija y no cambia con el valor de \(n\).

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo7_(ciclo_sin_dependencia).ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

## Código analizado


---

## Análisis esperado

### Complejidad temporal

\(T(n)\in O(1)\) respecto a \(n\), aunque la constante de trabajo sea grande.

### Complejidad espacial

\(S(n)\in O(1)\) porque el ciclo utiliza una cantidad fija de variables.

## Simulaciones experimentales

Cada experimento ejecuta el mismo algoritmo para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La preparación de la entrada se realiza fuera de la medición temporal. En memoria se reporta el espacio adicional utilizado durante la operación.
