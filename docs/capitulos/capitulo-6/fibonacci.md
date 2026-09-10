<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 2 · Fibonacci recursivo ingenuo

<span class="chapter-kicker">Capítulo 6</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

#### Código

=== "Pseudocódigo"

    ```text
    función fibonacci(n)
        si n ≤ 1 entonces retornar n
        retornar fibonacci(n - 1) + fibonacci(n - 2)
    ```

=== "Python"

    ```python
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    ```

=== "Java"

    ```java
    static long fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
    ```

=== "C"

    ```c
    long fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
    ```

#### Análisis

Cada llamada no base genera dos subproblemas parcialmente superpuestos:

\[
T(n)=T(n-1)+T(n-2)+\Theta(1)\in\Theta(\varphi^n).
\]

El árbol contiene una cantidad exponencial de llamadas por la repetición de resultados. Sin embargo, sus dos ramas no permanecen completas a la vez: la profundidad máxima es lineal, así que \(S(n)\in\Theta(n)\).

#### Simulación

La animación hace visible la ramificación y permite reconocer llamadas repetidas, como \(F(n-2)\), que motivan técnicas posteriores como memoización.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-6/ejemplos/arbol_recurrencia_fibonacci_general.png" alt="Árbol de llamadas de ejemplo 2 · fibonacci recursivo ingenuo"><figcaption>Árbol de llamadas de ejemplo 2 · fibonacci recursivo ingenuo.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/comparacion_complejidad_exponencial.png" alt="Comparación de crecimiento para ejemplo 2 · fibonacci recursivo ingenuo"><figcaption>Comparación de crecimiento para ejemplo 2 · fibonacci recursivo ingenuo.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../factorial/">← Ejemplo 1 · Factorial recursivo</a><a class="section-step__index" href="../">Capítulo 6</a><a class="section-step__next" href="../potencia/">Ejemplo 3 · Potencia de un número entero positivo →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>
