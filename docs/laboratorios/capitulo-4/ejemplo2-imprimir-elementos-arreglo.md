# Ejemplo 2: Recorrer los elementos de un arreglo

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 4</span>

El algoritmo visita una vez cada posición de un arreglo de tamaño \(n\). La simulación prepara la entrada antes de medir la operación.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo2_(imprimir_elementos_arreglo).ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

## Código analizado


---

## Análisis esperado

### Complejidad temporal

\(T(n)\in O(n)\) porque el cuerpo del ciclo se ejecuta una vez por cada elemento.

### Complejidad espacial

\(S(n)\in O(1)\) en espacio adicional: el arreglo se considera la entrada y el recorrido solo conserva la referencia actual.

## Simulaciones experimentales

Cada experimento ejecuta el mismo algoritmo para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La preparación de la entrada se realiza fuera de la medición temporal. En memoria se reporta el espacio adicional utilizado durante la operación.
