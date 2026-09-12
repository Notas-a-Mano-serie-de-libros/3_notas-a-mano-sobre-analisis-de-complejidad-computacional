<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 3 · Potencia de un número entero positivo

<span class="chapter-kicker">Capítulo 6</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

#### Código

<!-- book-code:start -->

Listado original del libro, página 243 (Java).

```java
public static double potencia(int a, int n) {
    if (n == 0)
        return 1;
    int absExponente = Math.abs(n);
    double mitad = potencia(a, absExponente / 2);
    if (absExponente % 2 == 0)
        mitad = mitad * mitad;
    else
        mitad = mitad * mitad * a;
    return n < 0 ? 1.0 / mitad : mitad;
}
```

<!-- book-code:end -->

#### Análisis

El resultado recursivo se calcula una sola vez y se reutiliza. Como el exponente se divide entre dos:

\[
T(n)=T(\lfloor n/2\rfloor)+\Theta(1)\in\Theta(\log_2(n)).
\]

La profundidad de llamadas sigue la misma cantidad de divisiones, de modo que \(S(n)\in\Theta(\log_2(n))\). Llamar dos veces a `potencia(a, absExponente / 2)` cambiaría radicalmente el árbol y desperdiciaría el resultado compartido.

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
