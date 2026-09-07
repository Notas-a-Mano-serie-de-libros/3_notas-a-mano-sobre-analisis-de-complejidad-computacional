# Complejidad polinomial general

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 2</span>

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/7_complejidad_polinomial_general.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

## Simulación teórica interactiva

En esta simulación no se realizan ejecuciones experimentales. El objetivo es observar únicamente el comportamiento teórico de la familia \(C(n)=n^k\).

El valor máximo de \(n\) se mantiene fijo y de solo lectura en \(10\). El control editable visualmente es \(k\), pero se modifica con los botones laterales para conservar el mismo formato de las animaciones anteriores. Al cambiar el valor de \(k\), la figura se actualiza automáticamente y muestra todas las curvas desde \(n^0\) hasta \(n^k\). De esta forma se puede ver gráficamente cómo cada nuevo grado hace que la curva dominante crezca con mayor rapidez.

La tabla siempre muestra el valor teórico calculado hasta \(k=5\) usando el máximo fijo \(n=10\), porque esos valores no dependen del grado seleccionado para la figura. La magnitud principal es la cantidad adimensional de operaciones teóricas, expresada directamente en notación científica compacta.


---

## Detalle teórico

La complejidad polinomial describe familias de funciones cuyo costo puede expresarse como una potencia de la entrada. En lugar de estudiar únicamente un caso fijo, como \(n^2\) o \(n^3\), esta sección considera la forma general \(n^k\), donde \(k\) representa el grado del polinomio.

Para una entrada de tamaño \(n\), una función de costo polinomial general puede expresarse como:

\[
C(n)=n^k
\]

donde \(C(n)\) representa el costo teórico, \(n\) representa el tamaño de la entrada y \(k\) representa el grado de la función. Cuando \(k=0\), la función se comporta como una constante, porque \(n^0=1\). Cuando \(k=1\), la función es lineal. Para \(k=2\) aparece el crecimiento cuadrático, para \(k=3\) el cúbico, y así sucesivamente.

La familia polinomial permite observar una transición progresiva: todas las curvas pertenecen a una misma forma general, pero cada aumento en \(k\) vuelve la pendiente más pronunciada. Esto significa que, para el mismo tamaño de entrada, una función de mayor grado produce un costo teórico mucho más grande.

En términos asintóticos, las funciones polinomiales suelen considerarse más manejables que las exponenciales o factoriales, pero eso no significa que todas sean igualmente prácticas. Un algoritmo \(O(n^2)\) puede ser razonable para entradas medianas, mientras que uno \(O(n^{10})\) puede volverse inviable con tamaños relativamente pequeños. Por eso, al hablar de algoritmos polinomiales, el valor de \(k\) importa tanto como la pertenencia a la familia.

La siguiente figura muestra el comportamiento teórico de \(C(n)=n^k\) para \(k\in[0,4]\). En ese rango se ve cómo las curvas pasan de una línea constante a crecimientos cada vez más inclinados.
