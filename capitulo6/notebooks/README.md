# Capítulo 6: Análisis de algoritmos recursivos

> **Libro:** páginas 223–258 · **Pregunta guía:** ¿cómo se traducen las llamadas recursivas en costos de tiempo y espacio?

Este capítulo conecta la ejecución de funciones recursivas con sus relaciones de recurrencia. El laboratorio permite observar el apilamiento, el caso base y el desapilamiento de cada llamada.

> [!IMPORTANT]
> **Complemento de lectura:** [síntesis del capítulo 6](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-6/) · [explicaciones de los laboratorios](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/laboratorios/capitulo-6/).

<p align="center"><a href="https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-6/"><img src="../../assets/qr/capitulo-6.png" width="132" alt="Código QR de la síntesis digital del capítulo 6"></a></p>

## Objetivos de aprendizaje

- Distinguir el caso base del caso recursivo.
- Construir relaciones de complejidad temporal y espacial.
- Seguir la pila de llamadas durante el apilamiento y el retorno.
- Analizar factorial, Fibonacci, potencia, Merge Sort y árboles binarios.
- Comparar implementaciones recursivas e iterativas.

## Contenido de la obra

| Sección | Contenido |
| :---: | --- |
| 6.1 | Programación recursiva, caso base y caso recursivo |
| 6.2 | Construcción de las relaciones de complejidad temporal y espacial |
| 6.3.1 | Factorial de un número natural |
| 6.3.2 | Sucesión de Fibonacci |
| 6.3.3 | Potencia de un número entero positivo |
| 6.3.4 | Ordenamiento por mezcla |
| 6.3.5 | Búsqueda en árbol binario |
| 6.4 | Consideraciones finales y ejercicios propuestos |

## Recursos interactivos

| Sección | Recurso | Abrir |
| :---: | --- | :---: |
| 6.1–6.3 | Laboratorio de análisis recursivo | [Notebook](./0_laboratorio_analisis_recursivo.ipynb) |
| Adicional | Comparación de Fibonacci | [Notebook](./comparacion_fibonacci.ipynb) |
| Adicional | Ejemplo general de recursión | [Notebook](./ejemplo_recursion.ipynb) |
| 6.4.1 | Ejercicios propuestos | [PDF](./ejercicios_propuestos.pdf) |

## Ruta recomendada

1. Identifica el caso base y comprueba que siempre sea alcanzable.
2. Describe cómo disminuye el tamaño del problema.
3. Cuenta las llamadas y el trabajo local de cada una.
4. Formula $T(n)$ y analiza la profundidad de la pila para $S(n)$.
5. Recorre la animación hasta el caso base y luego durante los retornos.
6. Compara la predicción con las métricas observadas.

## Síntesis conceptual

La obra propone cuatro pasos para analizar cualquier algoritmo recursivo:

1. Determinar si deben estudiarse casos de entrada diferentes.
2. Construir la relación de recurrencia con su caso base y su caso recursivo.
3. Resolverla con el método compatible con su estructura.
4. Expresar el resultado en el orden de complejidad correspondiente.

| Dimensión | Elementos que se construyen |
| --- | --- |
| Tiempo | Costo del caso base, cantidad y tamaño de llamadas por nivel, y operaciones adicionales $f(n)$. |
| Espacio | Costo del caso base, profundidad $d(n)$ de la pila y variables almacenadas en cada nivel. |

El caso base no equivale al mejor caso: el primero detiene la recursión, mientras que mejor, peor y promedio describen entradas de tamaño $n$ con costos diferentes. La forma ilustrativa de división no excluye las recurrencias de reducción estudiadas en el capítulo anterior.

Los ejemplos cubren reducción lineal (factorial), ramificación múltiple (Fibonacci), reducción logarítmica (potencia), división y combinación (ordenamiento por mezcla) y recorridos condicionados por la estructura de un árbol binario. Una solución recursiva puede compartir complejidad temporal con una versión iterativa y consumir más memoria por la pila de llamadas.

---

[← Capítulo 5](../../capitulo5/notebooks/README.md) · [Índice general](../../README.md) · [Capítulo 7 →](../../capitulo7/notebooks/README.md)
