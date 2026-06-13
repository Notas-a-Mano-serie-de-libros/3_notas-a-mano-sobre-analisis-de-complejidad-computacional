# Capítulo 8: Algoritmos de ordenamiento clásicos

> **Libro:** páginas 317–370 · **Pregunta guía:** ¿cómo cambia el costo de ordenar según la estrategia, la entrada y la memoria disponible?

Este capítulo compara algoritmos de ordenamiento mediante animaciones, trazas y métricas. Cada notebook permite cambiar el orden, el caso de entrada y la representación visual.

> [!IMPORTANT]
> **Complemento de lectura:** [consultar la síntesis del capítulo 8 en GitHub Pages](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-8/).

<a href="https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-8/"><img src="../../assets/qr/capitulo-8.png" width="132" alt="Código QR de la síntesis digital del capítulo 8"></a>

## Objetivos de aprendizaje

- Analizar comparaciones, intercambios, movimientos y memoria adicional.
- Distinguir los casos mejor, promedio y peor.
- Comparar algoritmos cuadráticos, log-lineales y no comparativos.
- Reconocer estabilidad, trabajo en el lugar y sensibilidad a la entrada.
- Elegir una estrategia según el tamaño y las propiedades de los datos.

## Contenido de la obra

| Sección | Contenido |
| :---: | --- |
| 8.1 | Consideraciones previas y convenciones de representación |
| 8.2 | Ordenamiento burbuja |
| 8.3 | Ordenamiento por selección |
| 8.4 | Ordenamiento por inserción |
| 8.5 | Ordenamiento por mezcla |
| 8.6 | Ordenamiento rápido |
| 8.7 | Ordenamiento radix |
| 8.8–8.9 | Consideraciones finales y ejercicios propuestos |

Cada algoritmo se presenta mediante su descripción, implementación, análisis de complejidad, escenarios de aplicación, ventajas y desventajas. Los códigos QR de la obra enlazan con las animaciones correspondientes.

## 1. Comparación general

El comparador reúne todos los algoritmos en un mismo entorno. Permite aplicar la misma entrada, observar sus trazas y contrastar comparaciones, movimientos, tiempo y memoria.

| Recurso | Contenido | Abrir |
| --- | --- | :---: |
| Comparación de algoritmos de ordenamiento | Complejidad, casos de entrada, operaciones, tiempos y memoria | [Notebook](./0_comparacion_ordenamientos.ipynb) |

## 2. Algoritmos específicos

Cada notebook desarrolla un algoritmo por separado y permite seguir el ordenamiento paso a paso mediante cajas o barras.

| Sección | Algoritmo | Tiempo característico | Abrir |
| :---: | --- | :---: | :---: |
| 8.2 | Burbuja | $O(n^2)$ | [Notebook](./1_ordenamiento_burbuja.ipynb) |
| 8.3 | Selección | $O(n^2)$ | [Notebook](./2_ordenamiento_seleccion.ipynb) |
| 8.4 | Inserción | $O(n^2)$ | [Notebook](./3_ordenamiento_insercion.ipynb) |
| 8.5 | Ordenamiento por mezcla | $O(n\log n)$ | [Notebook](./5_ordenamiento_mezcla.ipynb) |
| 8.6 | Ordenamiento rápido | $O(n\log n)$ promedio | [Notebook](./6_ordenamiento_rapido.ipynb) |
| 8.7 | Ordenamiento radix | $O(d(n+k))$ | [Notebook](./7_ordenamiento_radix.ipynb) |
| Adicional | Shell Sort | Depende de la secuencia de saltos | [Notebook](./4_ordenamiento_shell.ipynb) |

Shell Sort amplía los algoritmos presentados en la obra impresa. Las mediciones y proyecciones del comparador se identifican para no confundir una estimación teórica con una ejecución real.

## 3. Solución de los ejercicios propuestos

El PDF contiene los enunciados y el notebook desarrolla las soluciones en un laboratorio ejecutable.

| Recurso | Formato | Abrir |
| --- | :---: | :---: |
| Enunciados de los ejercicios propuestos | PDF | [Consultar](./ejercicios_propuestos.pdf) |
| Solución de los ejercicios propuestos | Notebook | [Ejecutar](./ejercicios_propuestos.ipynb) |

## Ruta recomendada

1. Identifica el estado inicial: ordenado, inverso, aleatorio o con duplicados.
2. Predice comparaciones, movimientos y memoria adicional.
3. Ejecuta el algoritmo paso a paso en modo cajas o barras.
4. Cambia el tamaño y el orden de salida.
5. Compara todos los algoritmos con la misma entrada.
6. Explica los resultados usando la estrategia del algoritmo, no solo el tiempo medido.

## Síntesis conceptual

| Algoritmo | Estrategia estudiada | Complejidad destacada en la obra |
| --- | --- | --- |
| Burbuja | Compara e intercambia elementos adyacentes en pasadas sucesivas. | Tiempo cuadrático y espacio constante; se discute una variante optimizada con mejor caso lineal. |
| Selección | Busca el elemento extremo del segmento restante y lo ubica en su posición. | Tiempo cuadrático en todos los casos y espacio constante. |
| Inserción | Inserta cada elemento dentro del segmento ya ordenado. | Mejor caso lineal, promedio y peor caso cuadráticos; espacio constante. |
| Mezcla | Divide, ordena recursivamente y combina subarreglos. | Tiempo log-lineal en todos los casos y espacio lineal. |
| Rápido | Particiona alrededor de un pivote. | Mejor y promedio log-lineales; peor caso cuadrático; la profundidad también cambia el espacio. |
| Radix | Distribuye por dígitos con ordenamiento por conteo, sin comparar pares. | $\Theta(d(n+b))$ en tiempo y $\Theta(n+b)$ en espacio para el caso ajustado. |

La obra organiza los métodos en tres familias: los procedimientos cuadráticos e intuitivos (burbuja, selección e inserción), los algoritmos de dividir y vencer (mezcla y rápido), y el enfoque no comparativo de radix. Para cada uno presenta descripción, implementación, análisis por casos, escenarios, ventajas y desventajas. Shell Sort se incorpora en el repositorio como ampliación y no como parte de los seis algoritmos desarrollados en el libro.

## Criterios de comparación

| Criterio | Pregunta |
| --- | --- |
| Tiempo | ¿Cómo crece el número de operaciones? |
| Espacio | ¿Necesita memoria proporcional a la entrada? |
| Estabilidad | ¿Conserva el orden relativo de valores iguales? |
| En el lugar | ¿Reorganiza los datos con memoria adicional constante? |
| Adaptabilidad | ¿Aprovecha que la entrada ya esté parcialmente ordenada? |

> [!IMPORTANT]
> No existe un algoritmo universalmente mejor. La elección depende de la entrada, las garantías necesarias, la memoria y el entorno de ejecución.

---

[← Capítulo 7](../../capitulo7/notebooks/README.md) · [Índice general](../../README.md)
