<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.9 Complejidad oculta

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo9_(complejidad_oculta).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El algoritmo de Fibonacci es iterativo, pero los enteros crecen con \(n\). La simulación permite observar el costo que introduce el tamaño creciente de esos valores.

### Código analizado

<!-- book-code:start -->

#### Fibonacci con enteros de precisión arbitraria

Implementación basada en el libro, página 167 (Java).

=== "Java"

    ```java
    public BigInteger fibonacciBigInteger(int n) {
        if (n < 0)
            throw new IllegalArgumentException("n debe ser no negativo");
        if (n <= 1)
            return BigInteger.valueOf(n);
        BigInteger a = BigInteger.ZERO;
        BigInteger b = BigInteger.ONE;
        for (int i = 2; i <= n; i++) {
            BigInteger c = a.add(b);
            a = b;
            b = c;
        }
        return b;
    }
    ```

=== "Pseudocódigo"

    ```text
    función fibonacciBigInteger(n)
        si n < 0 entonces
            error ValueError("n debe ser no negativo")
        si n <= 1 entonces
            retornar n
        a ← 0
        b ← 1
        para i en rango(2, n + 1)
            c ← a + b
            a ← b
            b ← c
        retornar b
    ```

=== "Python"

    ```python
    def fibonacciBigInteger(n):
        if n < 0:
            raise ValueError("n debe ser no negativo")
        if n <= 1:
            return n
        a = 0
        b = 1
        for i in range(2, n + 1):
            c = a + b
            a = b
            b = c
        return b
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    #include <gmp.h>

    // resultado debe inicializarse con mpz_init antes de llamar.
    void fibonacciBigInteger(int n, mpz_t resultado) {
        if (n < 0) {
            abort();
        }
        if (n <= 1) {
            mpz_set_ui(resultado, n);
            return;
        }
        mpz_t a, b, c;
        mpz_inits(a, b, c, NULL);
        mpz_set_ui(a, 0);
        mpz_set_ui(b, 1);
        for (int64_t i = 2; i <= n; i++) {
            mpz_add(c, a, b);
            mpz_set(a, b);
            mpz_set(b, c);
        }
        mpz_set(resultado, b);
        mpz_clears(a, b, c, NULL);
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

La versión C requiere GMP (`gmp.h` y enlace con `-lgmp`) para conservar la precisión arbitraria de `BigInteger`. El llamador inicializa y libera el resultado con `mpz_init` y `mpz_clear`.

| Parámetro o variable | Significado |
| --- | --- |
| `n` | Índice de Fibonacci. |
| `a, b` | Dos valores consecutivos. |
| `c` | Suma temporal para el siguiente valor. |

**Precondiciones:** n no negativo. Importar java.math.BigInteger.

**Resultado:** Devuelve F(n) sin el límite numérico de int.

??? example "Ejemplo paso a paso"
    Entrada: `n = 4`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `a = 0, b = 1` | Estado inicial. |
    | `i = 2; c = 1` | Actualiza a = 1, b = 1. |
    | `i = 3; c = 2` | Actualiza a = 1, b = 2. |
    | `i = 4; c = 3` | Actualiza a = 2, b = 3; devuelve 3. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas del ejemplo y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Ver código y editar entradas</summary><p>Solo las líneas de entrada resaltadas son editables. La implementación y la llamada al algoritmo son de solo lectura.</p><div id="runner-99de70187345" class="python-code-editor highlight" aria-label="Código Python · Fibonacci con enteros de precisión arbitraria"><pre><code><span class="python-code-line" data-code-line><span class="k">def</span><span class="w"> </span><span class="nf">fibonacciBigInteger</span><span class="p">(</span><span class="n">n</span><span class="p">):</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">n</span> <span class="o">&lt;</span> <span class="mi">0</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">raise</span> <span class="ne">ValueError</span><span class="p">(</span><span class="s2">"n debe ser no negativo"</span><span class="p">)</span></span><span class="python-code-line" data-code-line>    <span class="k">if</span> <span class="n">n</span> <span class="o">&lt;=</span> <span class="mi">1</span><span class="p">:</span></span><span class="python-code-line" data-code-line>        <span class="k">return</span> <span class="n">n</span></span><span class="python-code-line" data-code-line>    <span class="n">a</span> <span class="o">=</span> <span class="mi">0</span></span><span class="python-code-line" data-code-line>    <span class="n">b</span> <span class="o">=</span> <span class="mi">1</span></span><span class="python-code-line" data-code-line>    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">2</span><span class="p">,</span> <span class="n">n</span> <span class="o">+</span> <span class="mi">1</span><span class="p">):</span></span><span class="python-code-line" data-code-line>        <span class="n">c</span> <span class="o">=</span> <span class="n">a</span> <span class="o">+</span> <span class="n">b</span></span><span class="python-code-line" data-code-line>        <span class="n">a</span> <span class="o">=</span> <span class="n">b</span></span><span class="python-code-line" data-code-line>        <span class="n">b</span> <span class="o">=</span> <span class="n">c</span></span><span class="python-code-line" data-code-line>    <span class="k">return</span> <span class="n">b</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="c1"># Entradas editables del ejemplo.</span></span><span class="python-code-line" data-code-line contenteditable="plaintext-only" role="textbox" aria-label="Entrada editable, línea 15" spellcheck="false" data-editable><span class="n">n</span> <span class="o">=</span> <span class="mi">4</span></span><span class="python-code-line" data-code-line></span><span class="python-code-line" data-code-line><span class="n">resultado</span> <span class="o">=</span> <span class="n">fibonacciBigInteger</span><span class="p">(</span><span class="n">n</span><span class="p">)</span></span><span class="python-code-line" data-code-line><span class="nb">print</span><span class="p">(</span><span class="s2">"Resultado:"</span><span class="p">,</span> <span class="n">resultado</span><span class="p">)</span></span></code></pre></div></details><div class="example-runner-actions"><button type="button" data-run><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5v14l11-7z"/></svg><span>Ejecutar</span></button><button type="button" data-stop disabled><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6h12v12H6z"/></svg><span>Detener</span></button><button type="button" data-reset><svg class="button-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M17.65 6.35A7.95 7.95 0 0 0 12 4a8 8 0 1 0 7.75 10h-2.1A6 6 0 1 1 12 6c1.66 0 3.14.69 4.22 1.78L13 11h7V4z"/></svg><span>Restablecer ejemplo</span></button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

#### Laboratorio y medición

Los experimentos ejecutan adaptaciones Python. El tiempo excluye la preparación y se promedia por ejecución. La memoria representa el incremento de pico observado por tracemalloc durante la operación, sin incluir la entrada preparada; no es el tamaño de la memoria de una máquina Java.

El experimento usa enteros de precisión arbitraria de Python. Las sumas crecen con la cantidad de bits, como las de BigInteger.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/runtime/experimental_analysis.py).

<!-- book-code:end -->

### Análisis esperado

#### Complejidad temporal

El ciclo tiene \(\Theta(n)\) iteraciones. En un modelo que cobra cada suma como una operación, el tiempo es \(\Theta(n)\). Sin embargo, \(F(i)\) necesita \(\Theta(i)\) bits; con suma lineal en los bits, el costo acumulado es \(\sum_{i=2}^{n}\Theta(i)\in\Theta(n^2)\).

#### Complejidad espacial

Se conservan una cantidad constante de referencias, pero los valores a, b y c requieren \(\Theta(n)\) bits en el pico. Por tanto, el espacio para los valores numéricos es \(\Theta(n)\) bits; no es constante por el hecho de usar pocas variables.

### Simulaciones experimentales

Cada experimento ejecuta la adaptación Python descrita en «Laboratorio y medición» para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La entrada preparada se excluye de la medición. Las reservas realizadas dentro de la operación sí se incluyen; la memoria observada corresponde al incremento de pico de Python.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo8/">← 4.4.4.8 Ciclo con límite fijo y función de costo lineal</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo10/">4.4.4.10 Algoritmo costoso por diseño →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
