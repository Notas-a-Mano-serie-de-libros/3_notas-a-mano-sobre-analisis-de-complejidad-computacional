# Laboratorio de análisis recursivo

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 6</span>

Esta simulación aplica la metodología del capítulo para construir y analizar la complejidad de un algoritmo recursivo. Permite comparar cuatro estructuras: **factorial**, **Fibonacci ingenuo**, **potencia simple** y **exponenciación rápida**.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

## Metodología

Para cada algoritmo se identifican:

1. el caso de análisis;
2. el costo del caso base;
3. las llamadas recursivas realizadas por cada invocación;
4. el trabajo adicional ejecutado fuera de esas llamadas.

La relación temporal cuenta todas las llamadas y operaciones realizadas. La relación espacial estudia los marcos que permanecen **activos simultáneamente** en la pila. La simulación muestra cómo cada llamada se apila sobre el problema original y cómo, al alcanzar el caso base, los marcos se desapilan en orden inverso.


---

## Uso

1. Ejecuta la celda de simulación.
2. Selecciona un algoritmo y un tamaño de entrada \(n\).
3. Usa **Anterior** y **Siguiente** para recorrer las llamadas y los retornos.
4. Observa el crecimiento de la pila y el proceso inverso de retorno desde el caso base.
5. Observa cómo cambian el número de llamadas y la profundidad máxima.

## Análisis de ejemplos

Esta sección contrasta el análisis formal de los cinco ejemplos desarrollados en el capítulo con mediciones experimentales de tiempo y memoria. Selecciona un ejemplo y el tipo de análisis para observar cómo cambia el costo cuando aumenta el tamaño de entrada \(n\).

La tabla presenta los valores medidos en los puntos de control y la gráfica compara la tendencia experimental con la función teórica ajustada. Las fluctuaciones aisladas pueden depender del intérprete, la memoria disponible y otros procesos del sistema; por ello, debe interpretarse la forma general de crecimiento.

Los ejemplos disponibles son **factorial recursivo**, **Fibonacci recursivo**, **exponenciación rápida**, **ordenamiento por mezcla** y **búsqueda en árbol binario**. Para esta última, la medición representa el caso promedio sobre un árbol balanceado.
