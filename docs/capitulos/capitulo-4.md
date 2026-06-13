<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-5/">Capítulo 5 →</a></nav>

# Capítulo 4 · Análisis de algoritmos estructurados

**Páginas 133–178.** El capítulo pasa de las funciones abstractas al cálculo manual del costo de secuencias, condiciones, ciclos, datos y llamadas externas.

## Método de análisis

1. Definir qué representa el tamaño \(n\).
2. Elegir el caso de ejecución que se estudiará.
3. Descomponer el algoritmo en operaciones y estructuras de control.
4. Construir por separado \(T(n)\) y \(S(n)\).
5. Expresar el resultado con la notación asintótica apropiada.

| Sección | Desarrollo |
| :---: | --- |
| 4.1–4.3 | Clasificación, tiempo y espacio. |
| 4.4.2 | Costos temporales de operaciones comunes. |
| 4.4.3 | Costos espaciales de tipos y estructuras. |
| 4.4.4 | Diez ejemplos progresivos de análisis estructurado. |
| 4.5–4.6 | Consideraciones finales y ejercicios. |

Los ejemplos incluyen costos constantes, recorridos de arreglos y matrices, incrementos no unitarios, estructuras deliberadamente complejas, ciclos de límite fijo, funciones anidadas y complejidad oculta.

El repositorio ofrece laboratorios para los ejemplos 1, 2, 3, 4, 5, 7 y 9, con mediciones temporales y espaciales complementarias.

[Ver los laboratorios](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/tree/main/capitulo4/notebooks){ .md-button .md-button--primary }

!!! note
    La cantidad de ciclos visibles no determina por sí sola la complejidad: importan sus límites, dependencias, incrementos y el costo de las funciones invocadas.

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-5/">Capítulo 5 →</a></nav>
