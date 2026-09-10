<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.9 Complejidad oculta

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo9_(complejidad_oculta).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El algoritmo de Fibonacci es iterativo, pero los enteros crecen con \(n\). La simulación permite observar el costo que introduce el tamaño creciente de esos valores.

### Código analizado

=== "Pseudocódigo"

    ```text
    función fibonacciGrande(n)
        si n ≤ 1 entonces retornar n
        a ← 0; b ← 1
        para i ← 2 hasta n
            (a, b) ← (b, a + b)
        retornar b
    ```

=== "Python"

    ```python
    def fib_big(n):
        if n <= 1:
            return n
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    ```

=== "Java"

    ```java
    static java.math.BigInteger fibGrande(int n) {
        if (n <= 1) return java.math.BigInteger.valueOf(n);
        var a = java.math.BigInteger.ZERO;
        var b = java.math.BigInteger.ONE;
        for (int i = 2; i <= n; i++) {
            var siguiente = a.add(b);
            a = b; b = siguiente;
        }
        return b;
    }
    ```

=== "C"

    ```c
    /* Para conservar enteros arbitrariamente grandes se usa GMP. */
    void fibGrande(unsigned n, mpz_t resultado) {
        mpz_t a, b, siguiente;
        mpz_inits(a, b, siguiente, NULL);
        mpz_set_ui(b, 1);
        for (unsigned i = 2; i <= n; i++) {
            mpz_add(siguiente, a, b);
            mpz_set(a, b); mpz_set(b, siguiente);
        }
        mpz_set(resultado, n == 0 ? a : b);
        mpz_clears(a, b, siguiente, NULL);
    }
    ```


---

### Análisis esperado

#### Complejidad temporal

El ciclo tiene \(n\) iteraciones, pero cada suma opera sobre enteros cada vez más grandes; el costo real puede superar el modelo unitario \(O(n)\).

#### Complejidad espacial

Los enteros de Fibonacci necesitan más bits a medida que aumenta \(n\), por lo que la memoria observada también crece.

### Simulaciones experimentales

Cada experimento ejecuta el mismo algoritmo para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La preparación de la entrada se realiza fuera de la medición temporal. En memoria se reporta el espacio adicional utilizado durante la operación.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo8/">← 4.4.4.8 Ciclo con límite fijo y función de costo lineal</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo10/">4.4.4.10 Algoritmo costoso por diseño →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
