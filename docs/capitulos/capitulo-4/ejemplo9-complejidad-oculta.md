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

Listado original del libro, página 167 (Java).

```java
public BigInteger fibonacciBigInteger(int n) {
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

<!-- book-code:end -->

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
