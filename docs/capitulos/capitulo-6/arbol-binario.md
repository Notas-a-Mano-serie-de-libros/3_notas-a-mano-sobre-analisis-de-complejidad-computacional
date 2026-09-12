<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 5 · Búsqueda en árbol binario

<span class="chapter-kicker">Capítulo 6</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

#### Código

<!-- book-code:start -->

Listado original del libro, página 254 (Java).

```java
public static boolean buscar(Nodo raiz, int valor) {
    if (raiz == null)
        return false;
    if (valor == raiz.dato)
        return true;
    if (valor < raiz.dato)
        return buscar(raiz.izquierdo, valor);
    else
        return buscar(raiz.derecho, valor);
}
```

<!-- book-code:end -->

#### Análisis

El mejor caso encuentra el valor en la raíz: \(\Omega(1)\). En un árbol balanceado, una búsqueda guiada por orden alcanza una profundidad \(\Theta(\log_2(n))\); en un árbol degenerado puede recorrer \(O(n)\) nodos. La memoria de la versión recursiva depende de la altura \(h\): \(S(n)\in\Theta(h)\).

#### Simulación

El laboratorio contrasta árboles balanceados y degenerados para relacionar cantidad de nodos, altura y profundidad de la pila.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-6/ejemplos/complejidad_binario.png" alt="Secuencia visual de ejemplo 5 · búsqueda en árbol binario · paso representativo 1 de 3"><figcaption>Secuencia visual de ejemplo 5 · búsqueda en árbol binario · paso representativo 1 de 3.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/comparacion_complejidad_binario_1.png" alt="Comparación de crecimiento para ejemplo 5 · búsqueda en árbol binario"><figcaption>Comparación de crecimiento para ejemplo 5 · búsqueda en árbol binario.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/comparacion_complejidad_binario_2.png" alt="Comparación de crecimiento para ejemplo 5 · búsqueda en árbol binario"><figcaption>Comparación de crecimiento para ejemplo 5 · búsqueda en árbol binario.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../merge-sort/">← Ejemplo 4 · Ordenamiento por mezcla</a><a class="section-step__index" href="../">Capítulo 6</a><a class="section-step__next" href="../ejercicios-propuestos/">6.4.1 Ejercicios propuestos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>
