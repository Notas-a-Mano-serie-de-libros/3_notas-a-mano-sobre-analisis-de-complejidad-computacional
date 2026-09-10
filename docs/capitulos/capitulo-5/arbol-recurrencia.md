<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>

# 5.5.2 Árbol de recurrencia

<span class="chapter-kicker">Capítulo 5</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo5/notebooks/1_metodos_solucion_relaciones_recurrencia.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El árbol de recurrencia representa cada llamada como un nodo y cada subproblema como una rama. La complejidad se obtiene sumando el costo de todos los niveles, no siguiendo únicamente una rama.

### Procedimiento

1. Determine número y tamaño de los hijos de cada llamada.
2. Calcule el costo individual de un nodo en el nivel \(i\).
3. Multiplique ese costo por la cantidad de nodos del nivel.
4. Determine la altura mediante el caso base.
5. Sume costos internos y hojas, y contraste el término dominante.

El método es especialmente claro para árboles uniformes. En relaciones mixtas las ramas pueden tener alturas diferentes y deben contabilizarse por separado.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../sustitucion-iterativa/">← 5.5.1 Sustitución iterativa</a><a class="section-step__index" href="../">Capítulo 5</a><a class="section-step__next" href="../teorema-maestro/">5.5.3 Teorema maestro →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>
