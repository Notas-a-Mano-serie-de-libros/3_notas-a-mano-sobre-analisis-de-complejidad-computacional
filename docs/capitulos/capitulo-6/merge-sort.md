<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 4 · Ordenamiento por mezcla

<span class="chapter-kicker">Capítulo 6</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

#### Código

=== "Pseudocódigo"

    ```text
    función mergeSort(A)
        si longitud(A) ≤ 1 entonces retornar A
        m ← ⌊longitud(A) / 2⌋
        retornar combinar(mergeSort(A[0:m]), mergeSort(A[m:]))
    ```

=== "Python"

    ```python
    def merge_sort(a):
        if len(a) <= 1:
            return a
        m = len(a) // 2
        return combinar(merge_sort(a[:m]), merge_sort(a[m:]))
    ```

=== "Java"

    ```java
    static int[] mergeSort(int[] a) {
        if (a.length <= 1) return a;
        int m = a.length / 2;
        return combinar(
            mergeSort(java.util.Arrays.copyOfRange(a, 0, m)),
            mergeSort(java.util.Arrays.copyOfRange(a, m, a.length)));
    }
    ```

=== "C"

    ```c
    void mergeSort(int a[], int inicio, int fin) {
        if (inicio >= fin) return;
        int medio = inicio + (fin - inicio) / 2;
        mergeSort(a, inicio, medio);
        mergeSort(a, medio + 1, fin);
        combinar(a, inicio, medio, fin);
    }
    ```

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
