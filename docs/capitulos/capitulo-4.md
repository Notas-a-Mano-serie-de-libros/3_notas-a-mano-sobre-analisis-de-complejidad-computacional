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

## 4.4.4 Ejemplos desarrollados

Las páginas siguientes aplican este procedimiento a los diez ejemplos de la obra, en el orden código, análisis temporal, análisis espacial y simulación cuando existe un laboratorio asociado.

<nav class="chapter-outline chapter-outline--pages" aria-label="Secciones del capítulo">
<strong>Secciones del capítulo</strong>
<ol class="chapter-section-list">
<li><a href="ejemplo1-sumar-numeros/"><span>4.4.4.1 Sumar dos números</span><small>Leer sección →</small></a></li>
<li><a href="ejemplo2-imprimir-elementos-arreglo/"><span>4.4.4.2 Imprimir los elementos de un arreglo</span><small>Leer sección →</small></a></li>
<li><a href="ejemplo3-imprimir-elementos-matriz/"><span>4.4.4.3 Imprimir los elementos de una matriz</span><small>Leer sección →</small></a></li>
<li><a href="ejemplo4-inicializar-matriz-variable/"><span>4.4.4.4 Inicializar una matriz variable</span><small>Leer sección →</small></a></li>
<li><a href="ejemplo5-ciclos-incremento-no-lineal/"><span>4.4.4.5 Ciclos con incremento no lineal</span><small>Leer sección →</small></a></li>
<li><a href="ejemplo6/"><span>4.4.4.6 Algoritmo con estructura deliberadamente compleja</span><small>Leer sección →</small></a></li>
<li><a href="ejemplo7-ciclo-sin-dependencia/"><span>4.4.4.7 Ciclo sin dependencia de la entrada</span><small>Leer sección →</small></a></li>
<li><a href="ejemplo8/"><span>4.4.4.8 Ciclo con límite fijo y función de costo lineal</span><small>Leer sección →</small></a></li>
<li><a href="ejemplo9-complejidad-oculta/"><span>4.4.4.9 Complejidad oculta</span><small>Leer sección →</small></a></li>
<li><a href="ejemplo10/"><span>4.4.4.10 Algoritmo costoso por diseño</span><small>Leer sección →</small></a></li>
<li><a href="ejercicios-propuestos/"><span>4.6 Ejercicios propuestos</span><small>Leer sección →</small></a></li>
</ol>
</nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-5/">Capítulo 5 →</a></nav>
