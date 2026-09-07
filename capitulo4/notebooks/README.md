# Capítulo 4: Análisis de algoritmos estructurados

> **Libro:** páginas 133–178 · **Pregunta guía:** ¿cómo determinan las estructuras de control el costo temporal y espacial?

Este capítulo aplica las funciones de complejidad y la notación asintótica a algoritmos construidos con secuencias, condicionales y ciclos.

> [!IMPORTANT]
> **Complemento de lectura:** [síntesis del capítulo 4](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-4/) · [explicaciones de los laboratorios](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/laboratorios/capitulo-4/).

<p align="center"><a href="https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-4/"><img src="../../assets/qr/capitulo-4.png" width="132" alt="Código QR de la síntesis digital del capítulo 4"></a></p>

## Objetivos de aprendizaje

- Definir el tamaño de entrada adecuado para un algoritmo.
- Contar operaciones en secuencias, condicionales y ciclos.
- Obtener y simplificar las funciones $T(n)$ y $S(n)$.
- Reconocer ciclos independientes, anidados y no lineales.
- Contrastar el análisis formal con mediciones experimentales.

## Contenido de la obra

| Sección | Contenido |
| :---: | --- |
| 4.1 | Aspectos preliminares y clasificación de complejidad |
| 4.2 | Análisis de complejidad temporal |
| 4.3 | Análisis de complejidad espacial |
| 4.4.1–4.4.3 | Consideraciones y costos de operaciones comunes |
| 4.4.4 | Diez ejemplos de análisis de algoritmos estructurados |
| 4.5–4.6 | Consideraciones finales y ejercicios propuestos |

## Recursos interactivos

| Ejemplo | Recurso | Complejidad esperada | Laboratorio | Gráficas |
| :---: | --- | :---: | :---: | :---: |
| 1 | Sumar dos números | $O(1)$ | [Abrir](<./ejemplo1_(sumar_numeros).ipynb>) | [Reproducir](<./graficas/ejemplo1_(sumar_numeros)_graficas.ipynb>) |
| 2 | Recorrer un arreglo | $O(n)$ | [Abrir](<./ejemplo2_(imprimir_elementos_arreglo).ipynb>) | [Reproducir](<./graficas/ejemplo2_(imprimir_elementos_arreglo)_graficas.ipynb>) |
| 3 | Recorrer una matriz | $O(n^2)$ | [Abrir](<./ejemplo3_(imprimir_elementos_matriz).ipynb>) | [Reproducir](<./graficas/ejemplo3_(imprimir_elementos_matriz)_graficas.ipynb>) |
| 4 | Inicializar una matriz variable | $O(n^2)$ | [Abrir](<./ejemplo4_(inicializar_matriz_variable).ipynb>) | [Reproducir](<./graficas/ejemplo4_(inicializar_matriz_variable)_graficas.ipynb>) |
| 5 | Incremento no lineal | $O(n^2)$ | [Abrir](<./ejemplo5_(ciclos_incremento_no_lineal).ipynb>) | [Reproducir](<./graficas/ejemplo5_(ciclos_incremento_no_lineal)_graficas.ipynb>) |
| 7 | Ciclo sin dependencia de $n$ | $O(1)$ | [Abrir](<./ejemplo7_(ciclo_sin_dependencia).ipynb>) | [Reproducir](<./graficas/ejemplo7_(ciclo_sin_dependencia)_graficas.ipynb>) |
| 9 | Complejidad oculta | $O(n^2)$ | [Abrir](<./ejemplo9_(complejidad_oculta).ipynb>) | [Reproducir](<./graficas/ejemplo9_(complejidad_oculta)_graficas.ipynb>) |
| 4.6 | Ejercicios propuestos | — | [PDF](./ejercicios_propuestos.pdf) | — |

La numeración conserva los ejemplos de la obra impresa; por eso la secuencia disponible no es consecutiva. El libro contiene diez ejemplos y el repositorio ofrece laboratorios para los ejemplos 1, 2, 3, 4, 5, 7 y 9. Las mediciones temporales y espaciales complementan su análisis formal.

## Ruta recomendada

1. Define qué representa $n$.
2. Cuenta cuántas veces se ejecuta cada instrucción.
3. Construye $T(n)$ y $S(n)$.
4. Identifica el término dominante.
5. Predice las curvas antes de ejecutar el laboratorio.
6. Compara la predicción con las mediciones y explica el ruido observado.

## Síntesis conceptual

El análisis parte de una clasificación por casos y separa $T(n)$ de $S(n)$. Después asigna costos a operaciones comunes y descompone cada algoritmo hasta obtener una función analítica que pueda expresarse mediante notación asintótica.

| Estructura | Tratamiento general |
| --- | --- |
| Secuencia | Los costos de las instrucciones se suman. |
| Condicional | Se estudia el camino que corresponde al mejor, peor o caso promedio. |
| Ciclo | Se multiplica el costo del cuerpo por el número de iteraciones. |
| Ciclos anidados | Se combinan los rangos de iteración; no siempre basta con contar niveles sintácticos. |
| Función invocada | Se incorpora su costo real, incluso cuando queda oculto detrás de una llamada simple. |
| Memoria | Se contabilizan variables, arreglos, matrices y estructuras creadas durante la ejecución. |

Los diez ejemplos muestran costos constantes, lineales, cuadráticos, logarítmicos y combinados; también presentan incrementos no unitarios, límites fijos, funciones anidadas, complejidad adicional oculta y algoritmos deliberadamente costosos. La notación asintótica simplifica el resultado, pero puede omitir información relevante para un entorno concreto.

---

[← Capítulo 3](../../capitulo3/notebooks/README.md) · [Índice general](../../README.md) · [Capítulo 5 →](../../capitulo5/notebooks/README.md)
