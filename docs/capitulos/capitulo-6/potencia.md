<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 3 · Potencia de un número entero positivo

<span class="chapter-kicker">Capítulo 6</span>

## Código

<!-- book-code:start -->

### Potencia por división del exponente

<div class="example-runner" data-example-runner><details open><summary>Ver código y editar entradas</summary><input type="hidden" data-runner-language value="java"><div class="runner-language-tabs" role="tablist" aria-label="Lenguaje del ejemplo"><button type="button" role="tab" id="java-tab-bd618cda1a83" aria-controls="java-code-bd618cda1a83" aria-selected="true" data-language-tab="java">Java</button><button type="button" role="tab" id="python-tab-bd618cda1a83" aria-controls="runner-bd618cda1a83" aria-selected="false" tabindex="-1" data-language-tab="python">Python</button><button type="button" role="tab" id="c-tab-bd618cda1a83" aria-controls="c-code-bd618cda1a83" aria-selected="false" tabindex="-1" data-language-tab="c">C</button></div><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div id="java-code-bd618cda1a83" role="tabpanel" aria-labelledby="java-tab-bd618cda1a83" class="python-code-editor highlight" data-language="java" data-java-class="ejemplos.ebd618cda1a83.Main" aria-label="Código Java · Potencia por división del exponente"><pre><code><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.util.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="kn">import</span><span class="w"> </span><span class="nn">java.math.*</span><span class="p">;</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="kd">public</span><span class="w"> </span><span class="kd">class</span> <span class="nc">Main</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">double</span><span class="w"> </span><span class="nf">potencia</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">n</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="mi">0</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="k">return</span><span class="w"> </span><span class="mi">1</span><span class="p">;</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">absExponente</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">Math</span><span class="p">.</span><span class="na">abs</span><span class="p">(</span><span class="n">n</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="kt">double</span><span class="w"> </span><span class="n">mitad</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">potencia</span><span class="p">(</span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">absExponente</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="mi">2</span><span class="p">);</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">absExponente</span><span class="w"> </span><span class="o">%</span><span class="w"> </span><span class="mi">2</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="mi">0</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="n">mitad</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">mitad</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="n">mitad</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">else</span></span><span class="python-code-line" data-code-line><span class="w">            </span><span class="n">mitad</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">mitad</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="n">mitad</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="n">a</span><span class="p">;</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">return</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="mi">0</span><span class="w"> </span><span class="o">?</span><span class="w"> </span><span class="mf">1.0</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="n">mitad</span><span class="w"> </span><span class="p">:</span><span class="w"> </span><span class="n">mitad</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kd">public</span><span class="w"> </span><span class="kd">static</span><span class="w"> </span><span class="kt">void</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="n">String</span><span class="o">[]</span><span class="w"> </span><span class="n">args</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line data-editable-row><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: a" spellcheck="false" data-editable data-java-input="a"><span class="mi">2</span></span><span class="p">;</span></span><span class="python-code-line" data-code-line data-editable-row><span class="w">        </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada Java: n" spellcheck="false" data-editable data-java-input="n"><span class="o">-</span><span class="mi">3</span></span><span class="p">;</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">System</span><span class="p">.</span><span class="na">out</span><span class="p">.</span><span class="na">println</span><span class="p">(</span><span class="s">&quot;Resultado: &quot;</span><span class="w"> </span><span class="o">+</span><span class="w"> </span><span class="n">Main</span><span class="p">.</span><span class="na">potencia</span><span class="p">(</span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">n</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="p">}</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><div id="runner-bd618cda1a83" role="tabpanel" aria-labelledby="python-tab-bd618cda1a83" class="python-code-editor highlight" data-language="python" hidden aria-label="Código Python · Potencia por división del exponente"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">potencia</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">n</span> <span class="o">==</span> <span class="mi">0</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span> <span class="mf">1.0</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line>    <span class="n">absExponente</span> <span class="o">=</span> <span class="nb">abs</span><span class="p">(</span><span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="n">mitad</span> <span class="o">=</span> <span class="n">potencia</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">absExponente</span> <span class="o">//</span> <span class="mi">2</span><span class="p">)</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">absExponente</span> <span class="o">%</span> <span class="mi">2</span> <span class="o">==</span> <span class="mi">0</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="n">mitad</span> <span class="o">=</span> <span class="n">mitad</span> <span class="o">*</span> <span class="n">mitad</span></span><span class="python-code-line" data-code-line>    <span class="k">else</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="n">mitad</span> <span class="o">=</span> <span class="n">mitad</span> <span class="o">*</span> <span class="n">mitad</span> <span class="o">*</span> <span class="n">a</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="mf">1.0</span> <span class="o">/</span> <span class="n">mitad</span> <span class="k">if</span> <span class="n">n</span> <span class="o">&lt;</span> <span class="mi">0</span> <span class="k">else</span> <span class="n">mitad</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 16" spellcheck="false" data-editable><span class="n">a</span> <span class="o">=</span> <span class="mi">2</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 17" spellcheck="false" data-editable><span class="n">n</span> <span class="o">=</span> <span class="o">-</span><span class="mi">3</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="n">resultado</span> <span class="o">=</span> <span class="n">potencia</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">&quot;Resultado:&quot;</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span></span></code></pre></div><div id="c-code-bd618cda1a83" role="tabpanel" aria-labelledby="c-tab-bd618cda1a83" class="python-code-editor highlight" data-language="c" data-c-key="bd618cda1a83" hidden aria-label="Código C · Potencia por división del exponente"><pre><code><span class="python-code-line" data-code-line><span class="cp">#include</span><span class="w"> </span><span class="cpf">&lt;stdbool.h&gt;</span></span><span class="python-code-line" data-code-line><span class="cp">#include</span><span class="w"> </span><span class="cpf">&lt;stdio.h&gt;</span></span><span class="python-code-line" data-code-line><span class="cp">#include</span><span class="w"> </span><span class="cpf">&lt;stdlib.h&gt;</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="kt">double</span><span class="w"> </span><span class="nf">potencia</span><span class="p">(</span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">n</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="mi">0</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="k">return</span><span class="w"> </span><span class="mi">1</span><span class="p">;</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kt">int</span><span class="w"> </span><span class="n">absExponente</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">abs</span><span class="p">(</span><span class="n">n</span><span class="p">);</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="kt">double</span><span class="w"> </span><span class="n">mitad</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">potencia</span><span class="p">(</span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">absExponente</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="mi">2</span><span class="p">);</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="w">    </span><span class="k">if</span><span class="w"> </span><span class="p">(</span><span class="n">absExponente</span><span class="w"> </span><span class="o">%</span><span class="w"> </span><span class="mi">2</span><span class="w"> </span><span class="o">==</span><span class="w"> </span><span class="mi">0</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">mitad</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">mitad</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="n">mitad</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="k">else</span></span><span class="python-code-line" data-code-line><span class="w">        </span><span class="n">mitad</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span class="n">mitad</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="n">mitad</span><span class="w"> </span><span class="o">*</span><span class="w"> </span><span class="n">a</span><span class="p">;</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="w">    </span><span class="k">return</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">&lt;</span><span class="w"> </span><span class="mi">0</span><span class="w"> </span><span class="o">?</span><span class="w"> </span><span class="mf">1.0</span><span class="w"> </span><span class="o">/</span><span class="w"> </span><span class="n">mitad</span><span class="w"> </span><span class="o">:</span><span class="w"> </span><span class="n">mitad</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="kt">int</span><span class="w"> </span><span class="nf">main</span><span class="p">(</span><span class="kt">void</span><span class="p">)</span><span class="w"> </span><span class="p">{</span></span><span class="python-code-line" data-code-line data-editable-row><span class="w">    </span><span class="kt">int</span><span class="w"> </span><span class="n">a</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada C: a" spellcheck="false" data-editable data-c-input="a"><span class="mi">2</span></span><span class="p">;</span></span><span class="python-code-line" data-code-line data-editable-row><span class="w">    </span><span class="kt">int</span><span class="w"> </span><span class="n">n</span><span class="w"> </span><span class="o">=</span><span class="w"> </span><span contenteditable="plaintext-only" role="textbox" aria-label="Entrada C: n" spellcheck="false" data-editable data-c-input="n"><span class="mi">-3</span></span><span class="p">;</span></span><span class="python-code-line" data-code-line> </span><span class="python-code-line" data-code-line><span class="w">    </span><span class="n">printf</span><span class="p">(</span><span class="s">&quot;Resultado: %.17g</span><span class="se">\n</span><span class="s">&quot;</span><span class="p">,</span><span class="w"> </span><span class="n">potencia</span><span class="p">(</span><span class="n">a</span><span class="p">,</span><span class="w"> </span><span class="n">n</span><span class="p">));</span></span><span class="python-code-line" data-code-line><span class="w">    </span><span class="k">return</span><span class="w"> </span><span class="mi">0</span><span class="p">;</span></span><span class="python-code-line" data-code-line><span class="p">}</span></span></code></pre></div><p class="java-runtime-credit runtime-credit" data-runtime-credit="java">Java se ejecuta en tu navegador con <a href="https://cheerpj.com/" target="_blank" rel="noopener">CheerpJ</a>.</p><p class="runtime-credit" data-runtime-credit="python" hidden>Python se ejecuta en tu navegador con <a href="https://pyodide.org/en/stable/" target="_blank" rel="noopener">Pyodide</a>.</p><p class="runtime-credit" data-runtime-credit="c" hidden>C se ejecuta en tu navegador mediante <a href="https://webassembly.org/" target="_blank" rel="noopener">WebAssembly</a>.</p><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Reestablecer</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></details></div>

**Explicación:** Divide el valor absoluto del exponente entre dos, calcula la mitad recursivamente y combina el resultado según su paridad. Cuando n es negativo, retorna el recíproco.

??? example "Ejemplo paso a paso"
    Entrada: `a = 2, n = -3`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `base = 0.5, absExponente = 3` | Convierte el exponente negativo en una potencia de la base recíproca. |
    | `potenciaAbsoluta(0.5, 1) = 0.5` | Resuelve la mitad. |
    | \(0.5 \times 0.5 \times 0.5\) | Devuelve 0.125. |

<!-- book-code:end -->

## Análisis

El resultado recursivo se calcula una sola vez y se reutiliza. Para analizar exponentes positivos y negativos se define \(e=|n|\), calculando el valor absoluto en long para admitir también Integer.MIN_VALUE. El subproblema divide \(e\) entre dos:

\[
T(e)=T(\lfloor e/2\rfloor)+\Theta(1)\in\Theta(\log_2(2+e)).
\]

La profundidad de llamadas sigue la misma cantidad de divisiones, de modo que \(S(e)\in\Theta(\log_2(2+e))\). Llamar dos veces a `potencia(a, absExponente / 2)` cambiaría radicalmente el árbol y desperdiciaría el resultado compartido.

### Aplicación de los procedimientos del libro

Sea \(e=|n|\). El caso base cuesta una unidad, hay una sola llamada con la mitad del exponente y el resto de las operaciones es constante:

\[
T(e)=
\begin{cases}
1 & \text{si } e=0,\\
T(\lfloor e/2\rfloor)+1 & \text{si } e>0.
\end{cases}
\]

Para mostrar el desarrollo del libro se omiten temporalmente los pisos; estos no cambian el orden asintótico.

#### Sustitución iterativa

\[
\begin{aligned}
T(e)&=T(e/2)+1\\
&=T(e/4)+2\\
&=T(e/8)+3\\
&=\cdots\\
&=T(e/2^k)+k.
\end{aligned}
\]

El caso base se alcanza cuando \(e/2^k=1\), de donde \(k=\log_2(e)\). Al sustituir:

\[
T(e)=T(1)+\log_2(e)=1+\log_2(e)\in\Theta(\log_2(e)).
\]

Para incluir también \(e=0\), la página expresa el mismo orden como \(\Theta(\log_2(2+e))\).

#### Árbol de recurrencia

El árbol tiene un nodo por nivel y cada nodo realiza trabajo constante:

\[
\#_{nodos}=1,qquad f_k(e)=1,qquad T_k(e)=1.
\]

La profundidad máxima satisface \(e/2^h=1\), por lo que \(h=\log_2(e)\). Sumando todos los niveles:

\[
T(e)=\sum_{k=0}^{h}T_k(e)
=\sum_{k=0}^{\log_2(e)}1
=1+\log_2(e)
\in\Theta(\log_2(e)).
\]

#### Teorema maestro básico

La recurrencia tiene la forma \(T(e)=a\cdot T(e/b)+f(e)\), con

\[
a=1,qquad b=2,qquad f(e)=1,qquad \log_b(a)=\log_2(1)=0.
\]

Como

\[
f(e)=1=e^0=e^{\log_b(a)},
\]

se cumple el caso 2 del teorema maestro:

\[
T(e)\in\Theta\!\left(e^{\log_b(a)}\cdot\log_2(e)\right)
=\Theta(\log_2(e)).
\]

#### Complejidad espacial

La pila sigue una sola rama y cada marco almacena una cantidad constante de datos:

\[
S(e)=
\begin{cases}
1 & \text{si } e=0,\\
S(\lfloor e/2\rfloor)+1 & \text{si } e>0.
\end{cases}
\]

Su forma coincide con la recurrencia temporal; por ello, \(S(e)\in\Theta(\log_2(2+e))\).

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-6/ejemplos/arbol_recursion_potencia.png" alt="Árbol de llamadas de ejemplo 3 · potencia de un número entero positivo"><figcaption>Árbol de llamadas de ejemplo 3 · potencia de un número entero positivo.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/comparacion_teorema_maestro_potencia.png" alt="Comparación de crecimiento para ejemplo 3 · potencia de un número entero positivo"><figcaption>Comparación de crecimiento para ejemplo 3 · potencia de un número entero positivo.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../fibonacci/">← Ejemplo 2 · Fibonacci recursivo ingenuo</a><a class="section-step__index" href="../">Capítulo 6</a><a class="section-step__next" href="../merge-sort/">Ejemplo 4 · Ordenamiento por mezcla →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>
