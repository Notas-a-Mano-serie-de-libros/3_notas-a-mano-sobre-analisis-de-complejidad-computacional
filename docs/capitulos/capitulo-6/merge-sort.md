<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 4 · Ordenamiento por mezcla

<span class="chapter-kicker">Capítulo 6</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

#### Código

<!-- book-code:start -->

Listado original del libro, página 247 (Java).

```java
public void ordenar(int[] arr, int a, int b) {
    if (a >= b)
        return;
    int m = a + (b - a) / 2;
    ordenar(arr, a, m);
    ordenar(arr, m + 1, b);
    combinar(arr, a, m, b);
}
public void combinar(int[] arr, int a, int m, int b) {
    int[] izquierda = Arrays.copyOfRange(arr, a, m + 1);
    int[] derecha = Arrays.copyOfRange(arr, m + 1, b + 1);
    int i = 0, j = 0, k = a;
    while (i < izquierda.length && j < derecha.length) {
        if (izquierda[i] <= derecha[j])
            arr[k++] = izquierda[i++];
        else
            arr[k++] = derecha[j++];
    }
    while (i < izquierda.length)
        arr[k++] = izquierda[i++];
    while (j < derecha.length)
        arr[k++] = derecha[j++];
}
```

<!-- book-code:end -->

#### Análisis

La división genera dos subproblemas de tamaño \(n/2\) y la combinación recorre los \(n\) elementos. Por tanto, \(T(n)=2 \cdot T(n/2)+\Theta(n)\in\Theta(n \cdot \log_2(n))\). Los arreglos auxiliares de combinación requieren \(\Theta(n)\) memoria; la pila añade \(\Theta(\log_2(n))\), que queda dominada por el almacenamiento lineal.

#### Simulación

La vista experimental muestra las divisiones, el retorno de cada mitad y la combinación ordenada por niveles.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-6/ejemplos/arbol_recursion_mezcla.png" alt="Árbol de llamadas de ejemplo 4 · ordenamiento por mezcla"><figcaption>Árbol de llamadas de ejemplo 4 · ordenamiento por mezcla.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/arbol_recursion_mecla_2.png" alt="Árbol de llamadas de ejemplo 4 · ordenamiento por mezcla"><figcaption>Árbol de llamadas de ejemplo 4 · ordenamiento por mezcla.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../potencia/">← Ejemplo 3 · Potencia de un número entero positivo</a><a class="section-step__index" href="../">Capítulo 6</a><a class="section-step__next" href="../arbol-binario/">Ejemplo 5 · Búsqueda en árbol binario →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>
