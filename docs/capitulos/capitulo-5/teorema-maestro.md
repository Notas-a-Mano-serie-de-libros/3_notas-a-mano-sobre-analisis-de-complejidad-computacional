<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>

# 5.5.3 Teorema maestro

<span class="chapter-kicker">Capítulo 5</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo5/notebooks/1_metodos_solucion_relaciones_recurrencia.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El teorema maestro clasifica recurrencias de división de la forma \(T(n)=aT(n/b)+f(n)\). La comparación central es entre el trabajo externo \(f(n)\) y el costo crítico \(n^{\log_b(a)}\).

### Procedimiento

1. Identifique \(a\), \(b\) y \(f(n)\); si la recurrencia no tiene la forma exigida, no aplique el teorema.
2. Calcule \(n^{\log_b(a)}\).
3. Compare órdenes de crecimiento y determine el caso aplicable.
4. En el caso que exige regularidad, compruebe explícitamente la condición correspondiente.
5. Escriba la cota ajustada y explique qué parte del árbol domina.

La versión básica cubre costos polinómicos; extensiones permiten factores logarítmicos. Las relaciones de reducción \(T(n-1)\) y las divisiones desiguales requieren otro método o una generalización.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../arbol-recurrencia/">← 5.5.2 Árbol de recurrencia</a><a class="section-step__index" href="../">Capítulo 5</a><a class="section-step__next" href="../ecuacion-caracteristica/">5.5.4 Ecuación característica →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>
