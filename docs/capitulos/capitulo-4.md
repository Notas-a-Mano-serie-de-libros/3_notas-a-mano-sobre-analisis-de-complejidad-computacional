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

<section class="chapter-sections" aria-labelledby="chapter-sections-title">
<h2 id="chapter-sections-title">Secciones del capítulo</h2>
<div class="chapter-index chapter-index--sections">
<a class="chapter-entry" href="ejemplo1-sumar-numeros/"><span class="chapter-entry__number">4.4.4.1</span><strong>Sumar dos números</strong><span>Separa el tamaño de entrada del costo fijo de una operación aritmética.</span></a>
<a class="chapter-entry" href="ejemplo2-imprimir-elementos-arreglo/"><span class="chapter-entry__number">4.4.4.2</span><strong>Imprimir los elementos de un arreglo</strong><span>Deriva el costo temporal y espacial de un recorrido lineal.</span></a>
<a class="chapter-entry" href="ejemplo3-imprimir-elementos-matriz/"><span class="chapter-entry__number">4.4.4.3</span><strong>Imprimir los elementos de una matriz</strong><span>Analiza un recorrido completo sobre una matriz cuadrada.</span></a>
<a class="chapter-entry" href="ejemplo4-inicializar-matriz-variable/"><span class="chapter-entry__number">4.4.4.4</span><strong>Inicializar una matriz variable</strong><span>Incluye en el análisis el costo de construir y recorrer una matriz.</span></a>
<a class="chapter-entry" href="ejemplo5-ciclos-incremento-no-lineal/"><span class="chapter-entry__number">4.4.4.5</span><strong>Ciclos con incremento no lineal</strong><span>Muestra cómo el incremento modifica constantes sin cambiar siempre el orden.</span></a>
<a class="chapter-entry" href="ejemplo6/"><span class="chapter-entry__number">4.4.4.6</span><strong>Algoritmo con estructura deliberadamente compleja</strong><span>Sustituye ciclos y llamadas por sus costos antes de simplificar el resultado.</span></a>
<a class="chapter-entry" href="ejemplo7-ciclo-sin-dependencia/"><span class="chapter-entry__number">4.4.4.7</span><strong>Ciclo sin dependencia de la entrada</strong><span>Diferencia un límite fijo de otro que crece con el tamaño de entrada.</span></a>
<a class="chapter-entry" href="ejemplo8/"><span class="chapter-entry__number">4.4.4.8</span><strong>Ciclo con límite fijo y costo lineal</strong><span>Explica por qué una operación dependiente de n domina dentro de un ciclo fijo.</span></a>
<a class="chapter-entry" href="ejemplo9-complejidad-oculta/"><span class="chapter-entry__number">4.4.4.9</span><strong>Complejidad oculta</strong><span>Revela costos que no son evidentes al contar solamente las iteraciones.</span></a>
<a class="chapter-entry" href="ejemplo10/"><span class="chapter-entry__number">4.4.4.10</span><strong>Algoritmo costoso por diseño</strong><span>Evalúa cómo el orden de condiciones altera el costo de los casos posibles.</span></a>
<a class="chapter-entry" href="ejercicios-propuestos/"><span class="chapter-entry__number">4.6</span><strong>Ejercicios propuestos</strong><span>Permite practicar el análisis de secuencias, condiciones, ciclos y memoria.</span></a>
</div>
</section>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-5/">Capítulo 5 →</a></nav>
