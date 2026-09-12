<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.10 Algoritmo costoso por diseño

<span class="chapter-kicker">Capítulo 4</span>

Este ejemplo estudia cómo el orden de evaluación de condiciones modifica los casos observados cuando las funciones tienen costos distintos.

## Código analizado

<!-- book-code:start -->

#### Evaluación de condiciones y ruta alternativa: orden original

Implementación basada en el libro, página 170 (Java).

=== "Java"

    ```java
    if (g(n)) {
        // Se cumple g(n)
    } else if (h(n)) {
        // Se cumple h(n)
    } else {
        r(n);
    }
    ```

=== "Pseudocódigo"

    ```text
    si g(n) entonces
        sin operaciones  # Se cumple g(n)
    si no, si h(n) entonces
        sin operaciones  # Se cumple h(n)
    si no
        r(n)
    ```

=== "Python"

    ```python
    if g(n):
        pass  # Se cumple g(n)
    elif h(n):
        pass  # Se cumple h(n)
    else:
        r(n)
    ```

=== "C"

    ```c
    if (g(n)) {
        // Se cumple g(n)
    } else if (h(n)) {
        // Se cumple h(n)
    } else {
        r(n);
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Tamaño de la entrada. |
| `g, h` | Predicados con costos diferentes. |
| `r, s` | Operaciones de la ruta alternativa. |
| `var` | Resultado booleano disponible en la variante de la página 173. |

**Precondiciones:** Predicados y auxiliares definidos; considerar sus costos y posibles efectos laterales.

**Resultado:** Ejecuta la primera rama cuya condición se cumple. Es un fragmento de control, no un método completo.

??? example "Ejemplo paso a paso"
    Entrada: `h(n) = true, g(n) = false`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `g(n) = false` | No toma la primera rama. |
    | `h(n) = true` | Selecciona la segunda rama. |
    | `r(n)` | No se ejecuta. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-e6aa5726127a">Código Python · Evaluación de condiciones y ruta alternativa: orden original</label><div class="python-code-editor"><div class="highlight" aria-hidden="true"><pre><code><span class="n">n</span> <span class="o">=</span> <span class="mi">3</span>
<span class="n">var</span> <span class="o">=</span> <span class="kc">False</span>

<span class="c1"># Valores de los predicados para esta prueba de escritorio.</span>
<span class="k">def</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">return</span> <span class="kc">False</span>


<span class="k">def</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">return</span> <span class="kc">True</span>


<span class="k">def</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa r(n)"</span><span class="p">)</span>


<span class="k">def</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa s(n)"</span><span class="p">)</span>

<span class="k">if</span> <span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">pass</span>  <span class="c1"># Se cumple g(n)</span>
<span class="k">elif</span> <span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">pass</span>  <span class="c1"># Se cumple h(n)</span>
<span class="k">else</span><span class="p">:</span>
    <span class="n">r</span><span class="p">(</span><span class="n">n</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">"Evaluación de condiciones completada"</span><span class="p">)</span>
</code></pre></div><textarea id="runner-e6aa5726127a" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" rows="14">n = 3
var = False

# Valores de los predicados para esta prueba de escritorio.
def g(n):
    return False


def h(n):
    return True


def r(n):
    print(&quot;Se ejecuta la alternativa r(n)&quot;)


def s(n):
    print(&quot;Se ejecuta la alternativa s(n)&quot;)

if g(n):
    pass  # Se cumple g(n)
elif h(n):
    pass  # Se cumple h(n)
else:
    r(n)
print(&quot;Evaluación de condiciones completada&quot;)</textarea></div></details><div class="example-runner-actions"><button type="button" data-run><span class="button-icon" aria-hidden="true">▶</span><span>Ejecutar</span></button><button type="button" data-stop disabled><span class="button-icon" aria-hidden="true">■</span><span>Detener</span></button><button type="button" data-reset><span class="button-icon" aria-hidden="true">↻</span><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Evaluación de condiciones y ruta alternativa: condiciones reordenadas

Implementación basada en el libro, página 170 (Java).

=== "Java"

    ```java
    if (h(n)) {
        // Se cumple h(n)
    } else if (g(n)) {
        // Se cumple g(n)
    } else {
        r(n);
    }
    ```

=== "Pseudocódigo"

    ```text
    si h(n) entonces
        sin operaciones  # Se cumple h(n)
    si no, si g(n) entonces
        sin operaciones  # Se cumple g(n)
    si no
        r(n)
    ```

=== "Python"

    ```python
    if h(n):
        pass  # Se cumple h(n)
    elif g(n):
        pass  # Se cumple g(n)
    else:
        r(n)
    ```

=== "C"

    ```c
    if (h(n)) {
        // Se cumple h(n)
    } else if (g(n)) {
        // Se cumple g(n)
    } else {
        r(n);
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Tamaño de la entrada. |
| `g, h` | Predicados con costos diferentes. |
| `r, s` | Operaciones de la ruta alternativa. |
| `var` | Resultado booleano disponible en la variante de la página 173. |

**Precondiciones:** Predicados y auxiliares definidos; considerar sus costos y posibles efectos laterales.

**Resultado:** Ejecuta la primera rama cuya condición se cumple. Es un fragmento de control, no un método completo.

??? example "Ejemplo paso a paso"
    Entrada: `h(n) = true, g(n) = false`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `h(n) = true` | Selecciona la primera rama. |
    | `g(n), r(n)` | No se evalúan ni ejecutan en esta ruta. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-7dadf59bf6e8">Código Python · Evaluación de condiciones y ruta alternativa: condiciones reordenadas</label><div class="python-code-editor"><div class="highlight" aria-hidden="true"><pre><code><span class="n">n</span> <span class="o">=</span> <span class="mi">3</span>
<span class="n">var</span> <span class="o">=</span> <span class="kc">False</span>

<span class="c1"># Valores de los predicados para esta prueba de escritorio.</span>
<span class="k">def</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">return</span> <span class="kc">False</span>


<span class="k">def</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">return</span> <span class="kc">True</span>


<span class="k">def</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa r(n)"</span><span class="p">)</span>


<span class="k">def</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa s(n)"</span><span class="p">)</span>

<span class="k">if</span> <span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">pass</span>  <span class="c1"># Se cumple h(n)</span>
<span class="k">elif</span> <span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">pass</span>  <span class="c1"># Se cumple g(n)</span>
<span class="k">else</span><span class="p">:</span>
    <span class="n">r</span><span class="p">(</span><span class="n">n</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">"Evaluación de condiciones completada"</span><span class="p">)</span>
</code></pre></div><textarea id="runner-7dadf59bf6e8" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" rows="14">n = 3
var = False

# Valores de los predicados para esta prueba de escritorio.
def g(n):
    return False


def h(n):
    return True


def r(n):
    print(&quot;Se ejecuta la alternativa r(n)&quot;)


def s(n):
    print(&quot;Se ejecuta la alternativa s(n)&quot;)

if h(n):
    pass  # Se cumple h(n)
elif g(n):
    pass  # Se cumple g(n)
else:
    r(n)
print(&quot;Evaluación de condiciones completada&quot;)</textarea></div></details><div class="example-runner-actions"><button type="button" data-run><span class="button-icon" aria-hidden="true">▶</span><span>Ejecutar</span></button><button type="button" data-stop disabled><span class="button-icon" aria-hidden="true">■</span><span>Detener</span></button><button type="button" data-reset><span class="button-icon" aria-hidden="true">↻</span><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Evaluación de condiciones y ruta alternativa

Implementación basada en el libro, página 171 (Java).

=== "Java"

    ```java
    if (h(n)) {
        // Se cumple h(n)
    } else if (g(n)) {
        // Se cumple g(n)
    } else {
        s(n); // O(1)
    }
    ```

=== "Pseudocódigo"

    ```text
    si h(n) entonces
        sin operaciones  # Se cumple h(n)
    si no, si g(n) entonces
        sin operaciones  # Se cumple g(n)
    si no
        s(n)
    ```

=== "Python"

    ```python
    if h(n):
        pass  # Se cumple h(n)
    elif g(n):
        pass  # Se cumple g(n)
    else:
        s(n)
    ```

=== "C"

    ```c
    if (h(n)) {
        // Se cumple h(n)
    } else if (g(n)) {
        // Se cumple g(n)
    } else {
        s(n); // O(1)
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Tamaño de la entrada. |
| `g, h` | Predicados con costos diferentes. |
| `r, s` | Operaciones de la ruta alternativa. |
| `var` | Resultado booleano disponible en la variante de la página 173. |

**Precondiciones:** Predicados y auxiliares definidos; considerar sus costos y posibles efectos laterales.

**Resultado:** Ejecuta la primera rama cuya condición se cumple. Es un fragmento de control, no un método completo.

??? example "Ejemplo paso a paso"
    Entrada: `h(n) = true, g(n) = false`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `h(n) = true` | Selecciona la primera rama. |
    | `g(n), s(n)` | No se evalúan ni ejecutan en esta ruta. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-14c69ffc07a3">Código Python · Evaluación de condiciones y ruta alternativa</label><div class="python-code-editor"><div class="highlight" aria-hidden="true"><pre><code><span class="n">n</span> <span class="o">=</span> <span class="mi">3</span>
<span class="n">var</span> <span class="o">=</span> <span class="kc">False</span>

<span class="c1"># Valores de los predicados para esta prueba de escritorio.</span>
<span class="k">def</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">return</span> <span class="kc">False</span>


<span class="k">def</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">return</span> <span class="kc">True</span>


<span class="k">def</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa r(n)"</span><span class="p">)</span>


<span class="k">def</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa s(n)"</span><span class="p">)</span>

<span class="k">if</span> <span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">pass</span>  <span class="c1"># Se cumple h(n)</span>
<span class="k">elif</span> <span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">pass</span>  <span class="c1"># Se cumple g(n)</span>
<span class="k">else</span><span class="p">:</span>
    <span class="n">s</span><span class="p">(</span><span class="n">n</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">"Evaluación de condiciones completada"</span><span class="p">)</span>
</code></pre></div><textarea id="runner-14c69ffc07a3" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" rows="14">n = 3
var = False

# Valores de los predicados para esta prueba de escritorio.
def g(n):
    return False


def h(n):
    return True


def r(n):
    print(&quot;Se ejecuta la alternativa r(n)&quot;)


def s(n):
    print(&quot;Se ejecuta la alternativa s(n)&quot;)

if h(n):
    pass  # Se cumple h(n)
elif g(n):
    pass  # Se cumple g(n)
else:
    s(n)
print(&quot;Evaluación de condiciones completada&quot;)</textarea></div></details><div class="example-runner-actions"><button type="button" data-run><span class="button-icon" aria-hidden="true">▶</span><span>Ejecutar</span></button><button type="button" data-stop disabled><span class="button-icon" aria-hidden="true">■</span><span>Detener</span></button><button type="button" data-reset><span class="button-icon" aria-hidden="true">↻</span><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Evaluación de condiciones y ruta alternativa

Implementación basada en el libro, página 172 (Java).

=== "Java"

    ```java
    if (!h(n) && !g(n)) {
        s(n);
    } else if (h(n)) {
        // Se cumple h(n)
    } else if (g(n)) {
        // Se cumple g(n)
    }
    ```

=== "Pseudocódigo"

    ```text
    si no h(n) y no g(n) entonces
        s(n)
    si no, si h(n) entonces
        sin operaciones  # Se cumple h(n)
    si no, si g(n) entonces
        sin operaciones  # Se cumple g(n)
    ```

=== "Python"

    ```python
    if not h(n) and not g(n):
        s(n)
    elif h(n):
        pass  # Se cumple h(n)
    elif g(n):
        pass  # Se cumple g(n)
    ```

=== "C"

    ```c
    if (!h(n) && !g(n)) {
        s(n);
    } else if (h(n)) {
        // Se cumple h(n)
    } else if (g(n)) {
        // Se cumple g(n)
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Tamaño de la entrada. |
| `g, h` | Predicados con costos diferentes. |
| `r, s` | Operaciones de la ruta alternativa. |
| `var` | Resultado booleano disponible en la variante de la página 173. |

**Precondiciones:** Predicados y auxiliares definidos; considerar sus costos y posibles efectos laterales.

**Resultado:** Ejecuta la primera rama cuya condición se cumple. Es un fragmento de control, no un método completo.

??? example "Ejemplo paso a paso"
    Entrada: `h(n) = true, g(n) = false`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `!h(n) = false` | La primera condición no se cumple; && evita evaluar !g(n). |
    | `h(n) = true` | Vuelve a evaluar h(n) y toma su rama. |
    | `s(n)` | No se ejecuta. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-3ce31ecc35dd">Código Python · Evaluación de condiciones y ruta alternativa</label><div class="python-code-editor"><div class="highlight" aria-hidden="true"><pre><code><span class="n">n</span> <span class="o">=</span> <span class="mi">3</span>
<span class="n">var</span> <span class="o">=</span> <span class="kc">False</span>

<span class="c1"># Valores de los predicados para esta prueba de escritorio.</span>
<span class="k">def</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">return</span> <span class="kc">False</span>


<span class="k">def</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">return</span> <span class="kc">True</span>


<span class="k">def</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa r(n)"</span><span class="p">)</span>


<span class="k">def</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa s(n)"</span><span class="p">)</span>

<span class="k">if</span> <span class="ow">not</span> <span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">)</span> <span class="ow">and</span> <span class="ow">not</span> <span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="n">s</span><span class="p">(</span><span class="n">n</span><span class="p">)</span>
<span class="k">elif</span> <span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">pass</span>  <span class="c1"># Se cumple h(n)</span>
<span class="k">elif</span> <span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">pass</span>  <span class="c1"># Se cumple g(n)</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">"Evaluación de condiciones completada"</span><span class="p">)</span>
</code></pre></div><textarea id="runner-3ce31ecc35dd" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" rows="14">n = 3
var = False

# Valores de los predicados para esta prueba de escritorio.
def g(n):
    return False


def h(n):
    return True


def r(n):
    print(&quot;Se ejecuta la alternativa r(n)&quot;)


def s(n):
    print(&quot;Se ejecuta la alternativa s(n)&quot;)

if not h(n) and not g(n):
    s(n)
elif h(n):
    pass  # Se cumple h(n)
elif g(n):
    pass  # Se cumple g(n)
print(&quot;Evaluación de condiciones completada&quot;)</textarea></div></details><div class="example-runner-actions"><button type="button" data-run><span class="button-icon" aria-hidden="true">▶</span><span>Ejecutar</span></button><button type="button" data-stop disabled><span class="button-icon" aria-hidden="true">■</span><span>Detener</span></button><button type="button" data-reset><span class="button-icon" aria-hidden="true">↻</span><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Evaluación de condiciones y ruta alternativa

Implementación basada en el libro, página 173 (Java).

=== "Java"

    ```java
    if (var) {
        s(n);
    } else if (h(n)) {
        // Se cumple h(n)
    } else if (g(n)) {
        // Se cumple g(n)
    }
    ```

=== "Pseudocódigo"

    ```text
    si var entonces
        s(n)
    si no, si h(n) entonces
        sin operaciones  # Se cumple h(n)
    si no, si g(n) entonces
        sin operaciones  # Se cumple g(n)
    ```

=== "Python"

    ```python
    if var:
        s(n)
    elif h(n):
        pass  # Se cumple h(n)
    elif g(n):
        pass  # Se cumple g(n)
    ```

=== "C"

    ```c
    if (var) {
        s(n);
    } else if (h(n)) {
        // Se cumple h(n)
    } else if (g(n)) {
        // Se cumple g(n)
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Tamaño de la entrada. |
| `g, h` | Predicados con costos diferentes. |
| `r, s` | Operaciones de la ruta alternativa. |
| `var` | Resultado booleano disponible en la variante de la página 173. |

**Precondiciones:** Predicados y auxiliares definidos; considerar sus costos y posibles efectos laterales.

**Resultado:** Ejecuta la primera rama cuya condición se cumple. Es un fragmento de control, no un método completo.

??? example "Ejemplo paso a paso"
    Entrada: `var = false, h(n) = true, g(n) = false`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `var = false` | No ejecuta s(n). |
    | `h(n) = true` | Selecciona la rama de h(n). |
    | `g(n)` | No se evalúa en esta ruta. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-d5912a571cd2">Código Python · Evaluación de condiciones y ruta alternativa</label><div class="python-code-editor"><div class="highlight" aria-hidden="true"><pre><code><span class="n">n</span> <span class="o">=</span> <span class="mi">3</span>
<span class="n">var</span> <span class="o">=</span> <span class="kc">False</span>

<span class="c1"># Valores de los predicados para esta prueba de escritorio.</span>
<span class="k">def</span><span class="w"> </span><span class="nf">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">return</span> <span class="kc">False</span>


<span class="k">def</span><span class="w"> </span><span class="nf">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">return</span> <span class="kc">True</span>


<span class="k">def</span><span class="w"> </span><span class="nf">r</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa r(n)"</span><span class="p">)</span>


<span class="k">def</span><span class="w"> </span><span class="nf">s</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="nb">print</span><span class="p">(</span><span class="s2">"Se ejecuta la alternativa s(n)"</span><span class="p">)</span>

<span class="k">if</span> <span class="n">var</span><span class="p">:</span>
    <span class="n">s</span><span class="p">(</span><span class="n">n</span><span class="p">)</span>
<span class="k">elif</span> <span class="n">h</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">pass</span>  <span class="c1"># Se cumple h(n)</span>
<span class="k">elif</span> <span class="n">g</span><span class="p">(</span><span class="n">n</span><span class="p">):</span>
    <span class="k">pass</span>  <span class="c1"># Se cumple g(n)</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">"Evaluación de condiciones completada"</span><span class="p">)</span>
</code></pre></div><textarea id="runner-d5912a571cd2" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" rows="14">n = 3
var = False

# Valores de los predicados para esta prueba de escritorio.
def g(n):
    return False


def h(n):
    return True


def r(n):
    print(&quot;Se ejecuta la alternativa r(n)&quot;)


def s(n):
    print(&quot;Se ejecuta la alternativa s(n)&quot;)

if var:
    s(n)
elif h(n):
    pass  # Se cumple h(n)
elif g(n):
    pass  # Se cumple g(n)
print(&quot;Evaluación de condiciones completada&quot;)</textarea></div></details><div class="example-runner-actions"><button type="button" data-run><span class="button-icon" aria-hidden="true">▶</span><span>Ejecutar</span></button><button type="button" data-stop disabled><span class="button-icon" aria-hidden="true">■</span><span>Detener</span></button><button type="button" data-reset><span class="button-icon" aria-hidden="true">↻</span><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

Los experimentos ejecutan adaptaciones Python. El tiempo excluye la preparación y se promedia por ejecución. La memoria representa el incremento de pico observado por tracemalloc durante la operación, sin incluir la entrada preparada; no es el tamaño de la memoria de una máquina Java.

Estas variantes se analizan simbólicamente; no tienen simulación enlazada.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/runtime/experimental_analysis.py).

<!-- book-code:end -->

## Análisis esperado

Si \(h(n)\in\Theta(\log_2(n))\) es el caso más frecuente, evaluarla antes que \(g(n)\in\Theta(n)\) reduce el caso promedio a \(\Theta(\log_2(n))\). El peor caso continúa incluyendo \(r(n)\in\Theta(2^n)\); reordenar condiciones mejora la ruta habitual, pero no elimina el cuello de botella exponencial.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo9-complejidad-oculta/">← 4.4.4.9 Complejidad oculta</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejercicios-propuestos/">4.6 Ejercicios propuestos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
