<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.10 Algoritmo costoso por diseño

<span class="chapter-kicker">Capítulo 4</span>

Este ejemplo estudia cómo el orden de evaluación de condiciones modifica los casos observados cuando las funciones tienen costos distintos.

## Código analizado

<!-- book-code:start -->

Listado original del libro, página 170 (Java).

```java
if (g(n)) {
    // Se cumple g(n)
} else if (h(n)) {
    // Se cumple h(n)
} else {
    r(n);
}
```

Listado original del libro, página 170 (Java).

```java
if (h(n)) {
    // Se cumple h(n)
} else if (g(n)) {
    // Se cumple g(n)
} else {
    r(n);
}
```

Listado original del libro, página 171 (Java).

```java
if (h(n)) {
    // Se cumple h(n)
} else if (g(n)) {
    // Se cumple g(n)
} else {
    s(n); // O(1)
}
```

Listado original del libro, página 172 (Java).

```java
if (!h(n) && !g(n)) {
    s(n);
} else if (h(n)) {
    // Se cumple h(n)
} else if (g(n)) {
    // Se cumple g(n)
}
```

Listado original del libro, página 173 (Java).

```java
if (var) {
    s(n);
} else if (h(n)) {
    // Se cumple h(n)
} else if (g(n)) {
    // Se cumple g(n)
}
```

<!-- book-code:end -->

## Análisis esperado

Si \(h(n)\in\Theta(\log_2(n))\) es el caso más frecuente, evaluarla antes que \(g(n)\in\Theta(n)\) reduce el caso promedio a \(\Theta(\log_2(n))\). El peor caso continúa incluyendo \(r(n)\in\Theta(2^n)\); reordenar condiciones mejora la ruta habitual, pero no elimina el cuello de botella exponencial.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo9-complejidad-oculta/">← 4.4.4.9 Complejidad oculta</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejercicios-propuestos/">4.6 Ejercicios propuestos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
