<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-7/">Capítulo 7 →</a></nav>

# Capítulo 6 · Análisis de algoritmos recursivos

<span class="chapter-kicker">Páginas 223–258</span>

## 6.1 Estructura de una solución recursiva

Toda función recursiva necesita un caso base y una transformación que acerque cada llamada a ese caso. El seguimiento distingue tres momentos: apilamiento de llamadas, resolución del caso base y retorno de resultados. El tiempo cuenta todo el trabajo ejecutado; el espacio cuenta la máxima cantidad de marcos activos simultáneamente, no el total histórico de llamadas.

### Procedimiento para calcular el tiempo

1. Identifique el caso base y su costo.
2. Cuente las llamadas de un caso no base y el tamaño recibido por cada una.
3. Calcule el trabajo local realizado fuera de las llamadas.
4. Escriba \(T(n)\), resuélvala con un método compatible y compruebe el resultado.

### Procedimiento para calcular el espacio

1. Determine la memoria local de un marco de llamada.
2. Calcule la profundidad máxima de llamadas activas, no la cantidad total de nodos del árbol.
3. Añada estructuras auxiliares que sobrevivan mientras se resuelven los subproblemas.
4. Exprese la altura en función de \(n\) y simplifique \(S(n)\).

Las secciones siguientes aplican el procedimiento a factorial, Fibonacci, potencia, Merge Sort y búsqueda en árbol binario, siempre en el orden código, análisis y simulación.

<nav class="chapter-outline chapter-outline--pages" aria-label="Secciones del capítulo">
<strong>Secciones del capítulo</strong>
<ol class="chapter-section-list">
<li><a href="factorial/"><span>Ejemplo 1 · Factorial recursivo</span><small>Leer sección →</small></a></li>
<li><a href="fibonacci/"><span>Ejemplo 2 · Fibonacci recursivo ingenuo</span><small>Leer sección →</small></a></li>
<li><a href="potencia/"><span>Ejemplo 3 · Potencia de un número entero positivo</span><small>Leer sección →</small></a></li>
<li><a href="merge-sort/"><span>Ejemplo 4 · Ordenamiento por mezcla</span><small>Leer sección →</small></a></li>
<li><a href="arbol-binario/"><span>Ejemplo 5 · Búsqueda en árbol binario</span><small>Leer sección →</small></a></li>
<li><a href="ejercicios-propuestos/"><span>6.4.1 Ejercicios propuestos</span><small>Leer sección →</small></a></li>
</ol>
</nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-7/">Capítulo 7 →</a></nav>
