<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.8 Ciclo con límite fijo y función de costo lineal

<span class="chapter-kicker">Capítulo 4</span>

El número de iteraciones es constante, pero la operación ejecutada dentro del ciclo depende de la entrada.

## Código analizado

<!-- book-code:start -->

Listado original del libro, página 166 (Java).

```java
public static void cicloFijo(int n) {
    for (int i = 0; i < 1000; i++) {
        foo(n);
    }
}
```

<!-- book-code:end -->

## Análisis esperado

Si \(T_{foo}(n)=n\), entonces \(T(n)=1000 \cdot n\in O(n)\). La constante del ciclo se absorbe, pero la dependencia de `foo` no. Si \(S_{foo}(n)=n\), el espacio también queda en \(O(n)\).

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo7-ciclo-sin-dependencia/">← 4.4.4.7 Ciclo sin dependencia de la entrada</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo9-complejidad-oculta/">4.4.4.9 Complejidad oculta →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
