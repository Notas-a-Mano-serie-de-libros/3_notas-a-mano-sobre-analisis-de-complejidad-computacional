<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>

# 5.5.3 Árbol de recurrencia

<span class="chapter-kicker">Capítulo 5</span>

Represente cada llamada como un nodo y cada subproblema como una rama. Obtenga la complejidad sumando el costo de todos los niveles del árbol.

### Procedimiento

1. Determine el número y el tamaño de los hijos de cada llamada.
2. Calcule el costo individual de un nodo en el nivel \(i\).
3. Multiplique ese costo por la cantidad de nodos del nivel.
4. Determine la altura mediante el caso base.
5. Sume los costos de los nodos internos y de las hojas, e identifique el término dominante.

Use este método para visualizar y sumar los costos de árboles uniformes. En relaciones mixtas, contabilice por separado las ramas que alcanzan el caso base a diferentes alturas.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../sustitucion-iterativa/">← 5.5.2 Sustitución iterativa</a><a class="section-step__index" href="../">Capítulo 5</a><a class="section-step__next" href="../teorema-maestro/">5.5.4 Teorema maestro →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>
