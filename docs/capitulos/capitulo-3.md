<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-4/">Capítulo 4 →</a></nav>

# Capítulo 3 · Notación asintótica

<span class="chapter-kicker">Páginas 89–132</span>

## 3.1 Contexto y propósito

La notación asintótica compara tasas de crecimiento cuando \(n\) tiende a infinito. Su utilidad consiste en abstraer constantes de implementación sin perder la relación formal entre una función de costo \(C(n)\) y una función de referencia \(g(n)\). Las cotas pueden ser superiores, inferiores, ajustadas o estrictas; por eso los cinco símbolos no son intercambiables.

<section class="chapter-sections" aria-labelledby="chapter-sections-title">
<h2 id="chapter-sections-title">Secciones del capítulo</h2>
<div class="chapter-index chapter-index--sections">
<a class="chapter-entry" href="familias-de-funciones/"><span class="chapter-entry__number">3.2</span><strong>Familias de funciones</strong><span>Organiza las funciones de referencia usadas para comparar órdenes de crecimiento.</span></a>
<a class="chapter-entry" href="notacion-asintotica-representacion-generica/"><span class="chapter-entry__number">3.3</span><strong>Representación general</strong><span>Presenta gráficamente las relaciones entre una función y sus cotas asintóticas.</span></a>
<a class="chapter-entry" href="0-comparacion-notaciones-asintoticas/"><span class="chapter-entry__number">3.3.1</span><strong>Comparación de las notaciones</strong><span>Contrasta en una sola vista las cinco relaciones asintóticas fundamentales.</span></a>
<a class="chapter-entry" href="1-notacion-big-o/"><span class="chapter-entry__number">3.3.2</span><strong>Notación O</strong><span>Formaliza una cota superior asintótica mediante constantes y un umbral.</span></a>
<a class="chapter-entry" href="2-notacion-little-o/"><span class="chapter-entry__number">3.3.3</span><strong>Notación o</strong><span>Expresa que una función crece estrictamente más lento que otra.</span></a>
<a class="chapter-entry" href="3-notacion-big-omega/"><span class="chapter-entry__number">3.3.4</span><strong>Notación Ω</strong><span>Formaliza una cota inferior asintótica mediante constantes y un umbral.</span></a>
<a class="chapter-entry" href="4-notacion-little-omega/"><span class="chapter-entry__number">3.3.5</span><strong>Notación ω</strong><span>Expresa que una función crece estrictamente más rápido que otra.</span></a>
<a class="chapter-entry" href="5-notacion-theta/"><span class="chapter-entry__number">3.3.6</span><strong>Notación Θ</strong><span>Establece una cota ajustada combinando límites superior e inferior.</span></a>
<a class="chapter-entry" href="ejemplos-concretos-notaciones/"><span class="chapter-entry__number">3.4</span><strong>Ejemplos concretos</strong><span>Aplica cada notación a una misma función para comparar las demostraciones.</span></a>
<a class="chapter-entry" href="ejercicios-propuestos/"><span class="chapter-entry__number">3.6</span><strong>Ejercicios propuestos</strong><span>Propone problemas para practicar cotas, límites y relaciones asintóticas.</span></a>
</div>
</section>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-4/">Capítulo 4 →</a></nav>
