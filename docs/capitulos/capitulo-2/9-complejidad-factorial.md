<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.9 Complejidad factorial

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo2/notebooks/9_complejidad_factorial.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
</div>

<!-- book-code:start -->

El ejemplo del libro consiste en generar todos los reordenamientos posibles de una lista. La siguiente implementación en Python explora las elecciones de cada posición y devuelve cada permutación.

<div class="example-runner" data-example-runner><details open><summary>Ver código y editar entradas</summary><input type="hidden" data-runner-language value="python"><p>Solo la línea de entrada resaltada es editable.</p><div class="python-code-editor highlight" data-language="python" aria-label="Código Python · Generación de permutaciones"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">generar_permutaciones</span><span class="p">(</span><span class="n">lista</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="ow">not</span> <span class="n">lista</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">yield</span> <span class="p">[]</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line>    <span class="k">for</span> <span class="n">indice</span><span class="p">,</span> <span class="n">valor</span> <span class="ow">in</span> <span class="nb">enumerate</span><span class="p">(</span><span class="n">lista</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="n">restante</span> <span class="o">=</span> <span class="n">lista</span><span class="p">[:</span><span class="n">indice</span><span class="p">]</span> <span class="o">+</span> <span class="n">lista</span><span class="p">[</span><span class="n">indice</span> <span class="o">+</span> <span class="mi">1</span><span class="p">:]</span></span><span class="python-code-line" data-code-line>        <span class="k">for</span> <span class="n">permutacion</span> <span class="ow">in</span> <span class="n">generar_permutaciones</span><span class="p">(</span><span class="n">restante</span><span class="p">):</span></span><span class="python-code-line" data-code-line>            <span class="k">yield</span> <span class="p">[</span><span class="n">valor</span><span class="p">]</span> <span class="o">+</span> <span class="n">permutacion</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Lista de entrada" spellcheck="false" data-editable><span class="n">lista</span> <span class="o">=</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">3</span><span class="p">]</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="k">for</span> <span class="n">permutacion</span> <span class="ow">in</span> <span class="n">generar_permutaciones</span><span class="p">(</span><span class="n">lista</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="nb">print</span><span class="p">(</span><span class="n">permutacion</span><span class="p">)</span></span></code></pre></div><p class="runtime-credit" data-runtime-credit="python">Python se ejecuta en tu navegador con <a href="https://pyodide.org/en/stable/" target="_blank" rel="noopener">Pyodide</a>.</p><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Reestablecer</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></details></div>

<!-- book-code:end -->

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Complejidad factorial | `jupyter lab simulaciones/capitulo2/notebooks/9_complejidad_factorial.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../8-complejidad-exponencial/">← 2.1.2.8 Complejidad exponencial</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../ejercicios-propuestos/">2.2 Ejercicios propuestos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
