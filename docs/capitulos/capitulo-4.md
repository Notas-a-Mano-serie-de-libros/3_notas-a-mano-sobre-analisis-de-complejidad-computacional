<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-5/">Capítulo 5 →</a></nav>

# Capítulo 4 · Análisis de algoritmos estructurados

<span class="chapter-kicker">Páginas 133–178</span>

## 4.1–4.4 Del algoritmo estructurado a su función de costo

El análisis comienza definiendo qué representa \(n\), qué escenario se estudia y qué operaciones dependen de la entrada. Las secuencias suman costos, los condicionales seleccionan recorridos y los ciclos multiplican el costo de su cuerpo por la cantidad real de iteraciones. En ciclos anidados debe establecerse si los límites son independientes o dependen unos de otros. Tiempo y espacio se derivan por separado y solo después se simplifican asintóticamente.

### Procedimiento para calcular la complejidad temporal

1. Defina el tamaño de entrada y el escenario: mejor, promedio o peor caso.
2. Elija una operación básica cuyo número de ejecuciones dependa de la entrada.
3. Sume los costos de las secuencias y construya una función para cada rama condicional.
4. Determine las iteraciones reales de cada ciclo; en ciclos anidados, escriba las sumas antes de inferir el orden.
5. Sustituya el costo de las funciones llamadas y simplifique únicamente al final mediante dominancia.

### Procedimiento para calcular la complejidad espacial

1. Separe la memoria de entrada de la memoria auxiliar creada por el algoritmo.
2. Cuente variables, estructuras dinámicas y copias temporales activas simultáneamente.
3. Relacione cada dimensión de las estructuras con el tamaño de entrada.
4. Exprese \(S(n)\) y conserve su término dominante. El espacio no se obtiene copiando la complejidad temporal.

<section class="chapter-sections" markdown="1">

### Ejemplos

- [**Sumar dos números**](capitulo-4/ejemplo1-sumar-numeros.md)
- [**Imprimir los elementos de un arreglo**](capitulo-4/ejemplo2-imprimir-elementos-arreglo.md)
- [**Imprimir los elementos de una matriz**](capitulo-4/ejemplo3-imprimir-elementos-matriz.md)
- [**Inicializar una matriz variable**](capitulo-4/ejemplo4-inicializar-matriz-variable.md)
- [**Ciclos con incremento no lineal**](capitulo-4/ejemplo5-ciclos-incremento-no-lineal.md)
- [**Algoritmo con estructura deliberadamente compleja**](capitulo-4/ejemplo6.md)
- [**Ciclo sin dependencia de la entrada**](capitulo-4/ejemplo7-ciclo-sin-dependencia.md)
- [**Ciclo con límite fijo y costo lineal**](capitulo-4/ejemplo8.md)
- [**Complejidad oculta**](capitulo-4/ejemplo9-complejidad-oculta.md)
- [**Algoritmo costoso por diseño**](capitulo-4/ejemplo10.md)

</section>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-5/">Capítulo 5 →</a></nav>
