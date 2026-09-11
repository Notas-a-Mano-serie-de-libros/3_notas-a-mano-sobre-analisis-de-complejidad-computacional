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

<section class="chapter-sections" aria-labelledby="chapter-sections-title">
<h2 id="chapter-sections-title">Secciones del capítulo</h2>
<div class="chapter-index chapter-index--sections">
<a class="chapter-entry" href="factorial/"><span class="chapter-entry__number">01</span><strong>Factorial recursivo</strong><span>Relaciona una reducción unitaria con la profundidad de la pila de llamadas.</span></a>
<a class="chapter-entry" href="fibonacci/"><span class="chapter-entry__number">02</span><strong>Fibonacci recursivo ingenuo</strong><span>Expone la repetición de subproblemas y el crecimiento del árbol recursivo.</span></a>
<a class="chapter-entry" href="potencia/"><span class="chapter-entry__number">03</span><strong>Potencia de un entero positivo</strong><span>Compara reducción lineal y división del exponente mediante reutilización.</span></a>
<a class="chapter-entry" href="merge-sort/"><span class="chapter-entry__number">04</span><strong>Ordenamiento por mezcla</strong><span>Combina dos subproblemas por nivel y deriva su costo log-lineal.</span></a>
<a class="chapter-entry" href="arbol-binario/"><span class="chapter-entry__number">05</span><strong>Búsqueda en árbol binario</strong><span>Vincula el costo de búsqueda con la altura y el balance del árbol.</span></a>
<a class="chapter-entry" href="ejercicios-propuestos/"><span class="chapter-entry__number">6.4.1</span><strong>Ejercicios propuestos</strong><span>Propone análisis de tiempo, espacio y profundidad para algoritmos recursivos.</span></a>
</div>
</section>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-7/">Capítulo 7 →</a></nav>
