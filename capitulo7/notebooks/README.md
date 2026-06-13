# Capítulo 7: Algoritmos de búsqueda clásicos

> **Libro:** páginas 259–316 · **Pregunta guía:** ¿qué estrategia localiza un elemento con menos trabajo según la organización de los datos?

Este capítulo aplica el análisis temporal y espacial a seis algoritmos de búsqueda. Las animaciones muestran el intervalo activo, las comparaciones y los elementos descartados en cada paso.

> [!IMPORTANT]
> **Complemento de lectura:** [consultar la síntesis del capítulo 7 en GitHub Pages](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-7/).

<a href="https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-7/"><img src="../../assets/qr/capitulo-7.png" width="132" alt="Código QR de la síntesis digital del capítulo 7"></a>

## Objetivos de aprendizaje

- Distinguir búsquedas sobre datos ordenados y no ordenados.
- Analizar los casos mejor, promedio y peor.
- Comparar búsquedas secuencial, binaria, por interpolación, por saltos, exponencial y ternaria.
- Relacionar comparaciones, posiciones visitadas y tiempo de ejecución.
- Elegir un algoritmo según la distribución y organización de los datos.

## Contenido de la obra

| Sección | Contenido |
| :---: | --- |
| 7.1 | Consideraciones previas y convenciones de representación |
| 7.2 | Búsqueda secuencial |
| 7.3 | Búsqueda binaria iterativa y recursiva |
| 7.4 | Búsqueda por interpolación |
| 7.5 | Búsqueda por saltos |
| 7.6 | Búsqueda exponencial |
| 7.7 | Búsqueda ternaria recursiva e iterativa |
| 7.8–7.9 | Consideraciones finales y ejercicios propuestos |

Cada algoritmo se estudia mediante su descripción, implementación, análisis de complejidad, escenarios de aplicación, ventajas y desventajas. Los códigos QR de la obra enlazan con las animaciones que este repositorio desarrolla.

## 1. Comparación general

El comparador reúne los seis algoritmos en un mismo entorno. Permite aplicar las mismas condiciones de entrada, contrastar sus recorridos y estudiar sus métricas sin confundir las proyecciones teóricas con ejecuciones reales.

| Recurso | Contenido | Abrir |
| --- | --- | :---: |
| Comparación de algoritmos de búsqueda | Complejidad, casos de prueba, recorridos, comparaciones y tiempos | [Notebook](./0_comparacion_busquedas.ipynb) |

## 2. Algoritmos específicos

Cada notebook desarrolla un algoritmo por separado y permite observar su ejecución paso a paso.

| Sección | Algoritmo | Requisito principal | Complejidad típica | Abrir |
| :---: | --- | --- | :---: | :---: |
| 7.2 | Búsqueda secuencial | Ninguno | $O(n)$ | [Notebook](./1_busqueda_secuencial.ipynb) |
| 7.3 | Búsqueda binaria | Datos ordenados | $O(\log n)$ | [Notebook](./2_busqueda_binaria.ipynb) |
| 7.4 | Búsqueda por interpolación | Datos ordenados y aproximadamente uniformes | $O(\log\log n)$ promedio | [Notebook](./3_busqueda_interpolacion.ipynb) |
| 7.5 | Búsqueda por saltos | Datos ordenados | $O(\sqrt n)$ | [Notebook](./4_busqueda_saltos.ipynb) |
| 7.6 | Búsqueda exponencial | Datos ordenados | $O(\log n)$ | [Notebook](./5_busqueda_exponencial.ipynb) |
| 7.7 | Búsqueda ternaria | Datos ordenados | $O(\log n)$ | [Notebook](./6_busqueda_ternaria.ipynb) |

## 3. Solución de los ejercicios propuestos

El PDF contiene los enunciados y el notebook desarrolla las soluciones en un laboratorio ejecutable.

| Recurso | Formato | Abrir |
| --- | :---: | :---: |
| Enunciados de los ejercicios propuestos | PDF | [Consultar](./ejercicios_propuestos.pdf) |
| Solución de los ejercicios propuestos | Notebook | [Ejecutar](./ejercicios_propuestos.ipynb) |

## Ruta recomendada

1. Determina si los datos están ordenados y cómo se distribuyen.
2. Predice el mejor y el peor caso del algoritmo.
3. Ejecuta una búsqueda paso a paso y registra comparaciones y posiciones visitadas.
4. Cambia el tamaño, el objetivo y el caso de prueba.
5. Usa el comparador global bajo las mismas condiciones.
6. Justifica qué algoritmo elegirías y qué costo previo exige su requisito de ordenación.

## Síntesis conceptual

| Algoritmo | Estrategia estudiada | Condición y comportamiento |
| --- | --- | --- |
| Secuencial | Examina los elementos uno a uno. | No exige orden; resulta útil en colecciones pequeñas o sin información previa. |
| Binaria | Divide el intervalo de búsqueda en dos. | Exige orden; la obra analiza implementaciones iterativa y recursiva. |
| Interpolación | Estima la posición mediante el valor buscado y los extremos. | Es especialmente efectiva con datos ordenados y uniformemente distribuidos. |
| Saltos | Avanza por bloques y luego realiza una búsqueda local. | Exige orden y equilibra el tamaño del salto con el recorrido final. |
| Exponencial | Amplía el intervalo en potencias y aplica una búsqueda secundaria. | Es útil cuando la posición probable o el tamaño efectivo no se conocen de antemano. |
| Ternaria | Divide el intervalo en tres regiones. | Exige orden; se estudian versiones recursiva e iterativa. |

Para cada técnica, la obra desarrolla descripción, implementación, análisis temporal y espacial por casos, escenarios de aplicación, ventajas y desventajas. La elección depende del orden y distribución de los datos, la frecuencia de búsqueda y el tamaño de la colección; si es necesario ordenar primero, ese costo también forma parte de la decisión.

## Convención visual

| Estado | Representación |
| --- | :---: |
| Sin evaluar | ⬜ Blanco |
| Comparación actual | 🔵 Azul |
| Elemento descartado | ⬛ Gris |
| Objetivo encontrado | 🟢 Verde |

> [!IMPORTANT]
> Un mejor orden asintótico no garantiza por sí solo el menor tiempo para toda entrada: también importan el tamaño, la distribución, las constantes y el costo de preparar los datos.

---

[← Capítulo 6](../../capitulo6/notebooks/README.md) · [Índice general](../../README.md) · [Capítulo 8 →](../../capitulo8/notebooks/README.md)
