<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 1 · Factorial recursivo

<span class="chapter-kicker">Capítulo 6</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

#### Código

=== "Pseudocódigo"

    ```text
    función factorial(n)
        si n ≤ 1 entonces retornar 1
        retornar n × factorial(n - 1)
    ```

=== "Python"

    ```python
    def factorial(n):
        if n <= 1:
            return 1
        return n * factorial(n - 1)
    ```

=== "Java"

    ```java
    static long factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }
    ```

=== "C"

    ```c
    long factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }
    ```

#### Análisis

Cada llamada reduce \(n\) en una unidad y realiza una multiplicación adicional:

\[
T(n)=T(n-1)+\Theta(1),\qquad T(1)=\Theta(1).
\]

Después de \(n-1\) expansiones se alcanza el caso base, de modo que \(T(n)\in\Theta(n)\). Las llamadas pendientes forman una cadena de profundidad \(n\), por lo que \(S(n)\in\Theta(n)\).

#### Simulación

El recorrido muestra cómo se apilan los valores \(n,n-1,\ldots,1\) y cómo los productos se resuelven durante el retorno.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-6/ejemplos/arbol_recursion_factorial.png" alt="Árbol de llamadas de ejemplo 1 · factorial recursivo"><figcaption>Árbol de llamadas de ejemplo 1 · factorial recursivo.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/comparacion_complejidad_for.png" alt="Comparación de crecimiento para ejemplo 1 · factorial recursivo"><figcaption>Comparación de crecimiento para ejemplo 1 · factorial recursivo.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a class="section-step__index" href="../">Capítulo 6</a><a class="section-step__next" href="../fibonacci/">Ejemplo 2 · Fibonacci recursivo ingenuo →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>
