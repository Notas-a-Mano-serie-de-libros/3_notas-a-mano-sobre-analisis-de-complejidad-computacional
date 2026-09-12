<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 3 · Potencia de un número entero positivo

<span class="chapter-kicker">Capítulo 6</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

#### Código

<!-- book-code:start -->

##### Potencia por división del exponente

Implementación basada en el libro, página 243 (Java).

=== "Java"

    ```java
    public static double potencia(int a, int n) {
        if (a == 0 && n < 0)
            throw new ArithmeticException("Cero no admite exponente negativo");
        long absExponente = Math.abs((long) n);
        double base = n < 0 ? 1.0 / a : a;
        return potenciaAbsoluta(base, absExponente);
    }

    private static double potenciaAbsoluta(double a, long n) {
        if (n == 0)
            return 1;
        double mitad = potenciaAbsoluta(a, n / 2);
        mitad = mitad * mitad;
        return n % 2 == 0 ? mitad : mitad * a;
    }
    ```

=== "Pseudocódigo"

    ```text
    función potencia(a, n)
        si a == 0 y n < 0 entonces
            error ZeroDivisionError("Cero no admite exponente negativo")
        absExponente ← abs(n)
        base ← 1.0 / a if n < 0 else float(a)
        retornar potenciaAbsoluta(base, absExponente)


    función potenciaAbsoluta(a, n)
        si n == 0 entonces
            retornar 1.0
        mitad ← potenciaAbsoluta(a, n div 2)
        mitad ← mitad * mitad
        retornar mitad if n % 2 == 0 else mitad * a
    ```

=== "Python"

    ```python
    def potencia(a, n):
        if a == 0 and n < 0:
            raise ZeroDivisionError("Cero no admite exponente negativo")
        absExponente = abs(n)
        base = 1.0 / a if n < 0 else float(a)
        return potenciaAbsoluta(base, absExponente)


    def potenciaAbsoluta(a, n):
        if n == 0:
            return 1.0
        mitad = potenciaAbsoluta(a, n // 2)
        mitad = mitad * mitad
        return mitad if n % 2 == 0 else mitad * a
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    double potenciaAbsoluta(double a, int64_t n);

    double potencia(int a, int n) {
        if (a == 0 && n < 0) {
            abort();
        }
        int64_t absExponente = llabs((long long) n);
        double base = n < 0 ? 1.0 / a : (double) a;
        return potenciaAbsoluta(base, absExponente);
    }

    double potenciaAbsoluta(double a, int64_t n) {
        if (n == 0) {
            return 1;
        }
        double mitad = potenciaAbsoluta(a, n / 2);
        mitad = mitad * mitad;
        return n % 2 == 0 ? mitad : mitad * a;
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `a` | Base entera. |
| `n` | Exponente, que puede ser negativo. |
| `absExponente` | Valor absoluto del exponente. |
| `mitad` | Resultado de una llamada recursiva de la auxiliar potenciaAbsoluta. |

**Precondiciones:** Si n es negativo, a debe ser distinto de cero.

**Resultado:** Devuelve a elevado a n mediante una base recíproca cuando n es negativo.

**Explicación:** El valor absoluto del exponente se calcula en long para admitir también Integer.MIN_VALUE. El resultado se representa en double y está sujeto a su rango y redondeo.

??? example "Ejemplo paso a paso"
    Entrada: `a = 2, n = -3`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `base = 0.5, absExponente = 3` | Convierte el exponente negativo en una potencia de la base recíproca. |
    | `potenciaAbsoluta(0.5, 1) = 0.5` | Resuelve la mitad. |
    | \(0.5 \times 0.5 \times 0.5\) | Devuelve 0.125. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-0f3471be4e4e">Código Python · Potencia por división del exponente</label><div class="python-code-editor"><div class="highlight" aria-hidden="true"><pre><code><span class="k">def</span><span class="w"> </span><span class="nf">potencia</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">n</span><span class="p">):</span>
    <span class="k">if</span> <span class="n">a</span> <span class="o">==</span> <span class="mi">0</span> <span class="ow">and</span> <span class="n">n</span> <span class="o">&lt;</span> <span class="mi">0</span><span class="p">:</span>
        <span class="k">raise</span> <span class="ne">ZeroDivisionError</span><span class="p">(</span><span class="s2">"Cero no admite exponente negativo"</span><span class="p">)</span>
    <span class="n">absExponente</span> <span class="o">=</span> <span class="nb">abs</span><span class="p">(</span><span class="n">n</span><span class="p">)</span>
    <span class="n">base</span> <span class="o">=</span> <span class="mf">1.0</span> <span class="o">/</span> <span class="n">a</span> <span class="k">if</span> <span class="n">n</span> <span class="o">&lt;</span> <span class="mi">0</span> <span class="k">else</span> <span class="nb">float</span><span class="p">(</span><span class="n">a</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">potenciaAbsoluta</span><span class="p">(</span><span class="n">base</span><span class="p">,</span> <span class="n">absExponente</span><span class="p">)</span>


<span class="k">def</span><span class="w"> </span><span class="nf">potenciaAbsoluta</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">n</span><span class="p">):</span>
    <span class="k">if</span> <span class="n">n</span> <span class="o">==</span> <span class="mi">0</span><span class="p">:</span>
        <span class="k">return</span> <span class="mf">1.0</span>
    <span class="n">mitad</span> <span class="o">=</span> <span class="n">potenciaAbsoluta</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">n</span> <span class="o">//</span> <span class="mi">2</span><span class="p">)</span>
    <span class="n">mitad</span> <span class="o">=</span> <span class="n">mitad</span> <span class="o">*</span> <span class="n">mitad</span>
    <span class="k">return</span> <span class="n">mitad</span> <span class="k">if</span> <span class="n">n</span> <span class="o">%</span> <span class="mi">2</span> <span class="o">==</span> <span class="mi">0</span> <span class="k">else</span> <span class="n">mitad</span> <span class="o">*</span> <span class="n">a</span>

<span class="c1"># Entradas editables del ejemplo.</span>
<span class="n">a</span> <span class="o">=</span> <span class="mi">2</span>
<span class="n">n</span> <span class="o">=</span> <span class="o">-</span><span class="mi">3</span>

<span class="n">resultado</span> <span class="o">=</span> <span class="n">potencia</span><span class="p">(</span><span class="n">a</span><span class="p">,</span> <span class="n">n</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="s2">"Resultado:"</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span>
</code></pre></div><textarea id="runner-0f3471be4e4e" spellcheck="false" autocapitalize="off" autocomplete="off" wrap="off" rows="14">def potencia(a, n):
    if a == 0 and n &lt; 0:
        raise ZeroDivisionError(&quot;Cero no admite exponente negativo&quot;)
    absExponente = abs(n)
    base = 1.0 / a if n &lt; 0 else float(a)
    return potenciaAbsoluta(base, absExponente)


def potenciaAbsoluta(a, n):
    if n == 0:
        return 1.0
    mitad = potenciaAbsoluta(a, n // 2)
    mitad = mitad * mitad
    return mitad if n % 2 == 0 else mitad * a

# Entradas editables del ejemplo.
a = 2
n = -3

resultado = potencia(a, n)
print(&quot;Resultado:&quot;, resultado)
</textarea></div></details><div class="example-runner-actions"><button type="button" data-run><span class="button-icon" aria-hidden="true">▶</span><span>Ejecutar</span></button><button type="button" data-stop disabled><span class="button-icon" aria-hidden="true">■</span><span>Detener</span></button><button type="button" data-reset><span class="button-icon" aria-hidden="true">↻</span><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

##### Laboratorio y medición

La animación permite observar la estructura recursiva. El panel experimental ejecuta funciones Python: el tiempo y la memoria de ese panel corresponden a esas funciones y no a una ejecución del listado Java. La memoria se obtiene con tracemalloc; no mide directamente la pila de una JVM.

El experimento cuenta llamadas al dividir n entre dos; no evalúa la base ni calcula el resultado numérico de la potencia.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/runtime/recursive_examples_analysis.py).

<!-- book-code:end -->

#### Análisis

El resultado recursivo se calcula una sola vez y se reutiliza. Para analizar exponentes positivos y negativos se define \(e=|n|\), calculando el valor absoluto en long para admitir también Integer.MIN_VALUE. El subproblema divide \(e\) entre dos:

\[
T(e)=T(\lfloor e/2\rfloor)+\Theta(1)\in\Theta(\log_2(2+e)).
\]

La profundidad de llamadas sigue la misma cantidad de divisiones, de modo que \(S(e)\in\Theta(\log_2(2+e))\). Llamar dos veces a `potencia(a, absExponente / 2)` cambiaría radicalmente el árbol y desperdiciaría el resultado compartido.

#### Simulación

La animación muestra la reducción por mitades del exponente. El panel experimental amplía la comparación a factorial, Fibonacci, Merge Sort y búsqueda en árbol binario, mostrando tiempo, memoria y función teórica ajustada.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-6/ejemplos/arbol_recursion_potencia.png" alt="Árbol de llamadas de ejemplo 3 · potencia de un número entero positivo"><figcaption>Árbol de llamadas de ejemplo 3 · potencia de un número entero positivo.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/comparacion_teorema_maestro_potencia.png" alt="Comparación de crecimiento para ejemplo 3 · potencia de un número entero positivo"><figcaption>Comparación de crecimiento para ejemplo 3 · potencia de un número entero positivo.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../fibonacci/">← Ejemplo 2 · Fibonacci recursivo ingenuo</a><a class="section-step__index" href="../">Capítulo 6</a><a class="section-step__next" href="../merge-sort/">Ejemplo 4 · Ordenamiento por mezcla →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>
