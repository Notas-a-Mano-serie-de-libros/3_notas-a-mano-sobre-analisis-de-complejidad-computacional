<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 1 · Factorial recursivo

<span class="chapter-kicker">Capítulo 6</span>

## Código

<!-- book-code:start -->

### Factorial recursivo

<div class="example-runner" data-example-runner><details open><summary>Ver código y editar entradas</summary><input type="hidden" data-runner-language value="java"><div class="runner-language-tabs" role="tablist" aria-label="Lenguaje del ejemplo"><button type="button" role="tab" id="java-tab-ac692c6509c2" aria-controls="java-code-ac692c6509c2" aria-selected="true" data-language-tab="java">Java</button><button type="button" role="tab" id="python-tab-ac692c6509c2" aria-controls="runner-ac692c6509c2" aria-selected="false" tabindex="-1" data-language-tab="python">Python</button><button type="button" role="tab" id="c-tab-ac692c6509c2" aria-controls="c-code-ac692c6509c2" aria-selected="false" tabindex="-1" data-language-tab="c">C</button></div><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div id="java-code-ac692c6509c2" role="tabpanel" aria-labelledby="java-tab-ac692c6509c2" class="python-code-editor highlight" data-language="java" data-java-class="ejemplos.eac692c6509c2.Main" aria-label="Código Java · Factorial recursivo"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Main</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="nf">factorial</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">n</span><span class="w"> </span><span class="o">&lt;=</span><span class="w"> </span><span class="mi">1</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="mi">1</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">else</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="n">factorial</span><span class="p">(</span><span class="n">n</span><span class="o">-</span><span class="mi">1</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line data-editable-row><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: n" spellcheck="false" data-editable data-java-input="n"><span class="mi">3</span></span><span class="p">;</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">&quot;Resultado: &quot;</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">Main</span><span class="p">.</span><span class="na">factorial</span><span class="p">(</span><span class="n">n</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-ac692c6509c2" role="tabpanel" aria-labelledby="python-tab-ac692c6509c2" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Factorial recursivo"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">factorial</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">n</span> <span class="o">&lt;=</span> <span class="mi">1</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="n">n</span> <span class="o">*</span> <span class="n">factorial</span><span class="p">(</span><span class="n">n</span> <span class="o">-</span> <span class="mi">1</span><span class="p">)</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 7" spellcheck="false" data-editable><span class="n">n</span> <span class="o">=</span> <span class="mi">3</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="n">resultado</span> <span class="o">=</span> <span class="n">factorial</span><span class="p">(</span><span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Resultado:&quot;</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span></span></code></pre></div><div id="c-code-ac692c6509c2" role="tabpanel" aria-labelledby="c-tab-ac692c6509c2" class="python-code-editor highlight" data-language="c" data-c-key="ac692c6509c2" hidden aria-label="Código C · Factorial recursivo"><pre><code><span class="python-code-line" data-code-line><span class="cp">#include</span><span class="w"> </span><span class="cpf">&lt;stdbool.h&gt;</span></span><span class="python-code-line" data-code-line><span class="cp">#include</span><span class="w"> </span><span class="cpf">&lt;stdio.h&gt;</span></span><span class="python-code-line" data-code-line><span class="cp">#include</span><span class="w"> </span><span class="cpf">&lt;stdlib.h&gt;</span></span><span class="python-code-line" data-code-line><span class="cp">#include</span><span class="w"> </span><span class="cpf">&lt;stdint.h&gt;</span></span><span class="python-code-line" data-code-line><span class="cp">#include</span><span class="w"> </span><span class="cpf">&lt;limits.h&gt;</span></span><span class="python-code-line" data-code-line><span class="cp">#include</span><span class="w"> </span><span class="cpf">&lt;math.h&gt;</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="kt">int</span><span class="w"> </span><span class="nf">factorial</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">n</span><span class="w"> </span><span class="o">&lt;=</span><span class="w"> </span><span class="mi">1</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">return</span><span class="w"> </span><span class="mi">1</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="k">else</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">return</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="nf">factorial</span><span class="p">(</span><span class="n">n</span><span class="w"> </span><span class="o">-</span><span class="w"> </span><span class="mi">1</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="kt">int</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="kt">void</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line data-editable-row><span class="w">    </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada C: n" spellcheck="false" data-editable data-c-input="n"><span class="mi">3</span></span><span class="p">;</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="w">    </span><span class="n">printf</span><span class="p">(</span><span class="s">&quot;Resultado: %d</span><span class="se">\n</span><span class="s">&quot;</span><span class="p">,</span><span class="w"> </span><span class="n">factorial</span><span class="p">(</span><span class="n">n</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="k">return</span><span class="w"> </span><span class="mi">0</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><p class="java-runtime-credit runtime-credit" data-runtime-credit="java">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>.</p><p class="runtime-credit" data-runtime-credit="python" hidden>Python se ejecuta en tu navegador con <a href="https://pyodide.org/en/stable/" target="_blank" rel="noopener">Pyodide</a>.</p><p class="runtime-credit" data-runtime-credit="c" hidden>C se ejecuta en tu navegador mediante <a href="https://webassembly.org/" target="_blank" rel="noopener">WebAssembly</a>.</p><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Reestablecer</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></details></div>

??? example "Ejemplo paso a paso"
    Entrada: `n = 3`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `factorial(3)` | Espera \(3 \times \operatorname{factorial}(2)\). |
    | `factorial(2)` | Espera \(2 \times \operatorname{factorial}(1)\). |
    | `factorial(1) = 1` | Caso base. |
    | `Retorno` | \(2 \times 1 = 2\); luego \(3 \times 2 = 6\). |

<!-- book-code:end -->

## Análisis

Cada llamada reduce \(n\) en una unidad y realiza una multiplicación adicional:

\[
T(n)=T(n-1)+\Theta(1),\qquad T(1)=\Theta(1).
\]

Después de \(n-1\) expansiones se alcanza el caso base, de modo que \(T(n)\in\Theta(n)\). Las llamadas pendientes forman una cadena de profundidad \(n\), por lo que \(S(n)\in\Theta(n)\).

### Aplicación de los procedimientos del libro

El costo depende únicamente de \(n\), de modo que los tres casos de análisis coinciden. Primero se separan los componentes de la recurrencia temporal:

\[
T_{base}(n)=\Theta(1),\qquad
T_{recursivo}(n)=T(n-1),\qquad
f(n)=\Theta(1).
\]

Al expresar el costo exacto de cada término se obtiene:

\[
T(n)=
\begin{cases}
1 & \text{si } n\leq1,\\
T(n-1)+1 & \text{si } n>1.
\end{cases}
\]

#### Sustitución iterativa

La recurrencia se expande hasta hacer visible el patrón:

\[
\begin{aligned}
T(n)&=T(n-1)+1\\
&=T(n-2)+2\\
&=T(n-3)+3\\
&=\cdots\\
&=T(n-k)+k.
\end{aligned}
\]

La recursión termina cuando \(n-k=1\), por lo que \(k=n-1\). Al sustituir:

\[
T(n)=T(1)+(n-1)=1+n-1=n\in\Theta(n).
\]

#### Árbol de recurrencia

En el nivel \(k\) hay un solo nodo y su trabajo local es constante:

\[
\#_{nodos}=1,\qquad f_k(n)=1,\qquad T_k(n)=1.
\]

La altura se obtiene de \(n-h=1\), es decir, \(h=n-1\). La suma de todos los niveles confirma el resultado:

\[
T(n)=\sum_{k=0}^{h}T_k(n)=\sum_{k=0}^{n-1}1=n\in\Theta(n).
\]

#### Ecuación característica

La recurrencia es lineal, no homogénea y de orden uno. Su ecuación característica es

\[
r-1=0,
\]

con raíz \(r_1=1\), por lo que \(T_h(n)=A_1\). Como el término independiente es constante y \(1\) ya es raíz, se propone \(T_p(n)=An\). Al sustituir en la recurrencia:

\[
An=A(n-1)+1\quad\Longrightarrow\quad A=1.
\]

Así, \(T(n)=A_1+n\). La condición inicial \(T(1)=1\) produce \(A_1=0\), y finalmente:

\[
T(n)=n\in\Theta(n).
\]

#### Complejidad espacial

Cada llamada añade un marco de tamaño constante y reduce \(n\) en una unidad:

\[
S(n)=
\begin{cases}
1 & \text{si } n\leq1,\\
S(n-1)+1 & \text{si } n>1.
\end{cases}
\]

Esta recurrencia tiene la misma forma que la temporal; por cualquiera de los procedimientos anteriores, \(S(n)\in\Theta(n)\).

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-6/ejemplos/arbol_recursion_factorial.png" alt="Árbol de llamadas de ejemplo 1 · factorial recursivo"><figcaption>Árbol de llamadas de ejemplo 1 · factorial recursivo.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/comparacion_complejidad_for.png" alt="Comparación de crecimiento para ejemplo 1 · factorial recursivo"><figcaption>Comparación de crecimiento para ejemplo 1 · factorial recursivo.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a class="section-step__index" href="../">Capítulo 6</a><a class="section-step__next" href="../fibonacci/">Ejemplo 2 · Fibonacci recursivo ingenuo →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>
