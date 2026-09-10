<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.3 Complejidad lineal

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/3_complejidad_lineal.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: búsqueda secuencial en una lista

El ejemplo recorre la lista de izquierda a derecha hasta encontrar el objetivo o agotar la entrada. En el peor caso, el elemento no aparece y la función revisa todos los valores.

Cada elemento se evalúa una vez. Por eso el tiempo de ejecución observado tiende a crecer junto con la cantidad de datos.


---

### Código del ejemplo

=== "Pseudocódigo"

    ```text
    función buscar(A, objetivo)
        para i ← 0 hasta longitud(A) - 1
            si A[i] = objetivo entonces retornar i
        retornar -1
    ```

=== "Python"

    ```python
    def buscar_elemento(lista, objetivo):
        for indice, valor in enumerate(lista):
            if valor == objetivo:
                return indice
        return -1
    ```

=== "Java"

    ```java
    static int buscar(int[] a, int objetivo) {
        for (int i = 0; i < a.length; i++)
            if (a[i] == objetivo) return i;
        return -1;
    }
    ```

=== "C"

    ```c
    int buscar(const int a[], int n, int objetivo) {
        for (int i = 0; i < n; i++)
            if (a[i] == objetivo) return i;
        return -1;
    }
    ```

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad lineal describe algoritmos cuyo costo crece de forma proporcional al tamaño de la entrada. Si la entrada tiene más elementos, el algoritmo puede necesitar más pasos en la misma proporción.

Este comportamiento aparece cuando el procedimiento debe inspeccionar cada elemento o avanzar secuencialmente hasta encontrar una condición. La forma del trabajo no cambia, pero se repite una vez por cada dato disponible.

Para una entrada de tamaño \(n\), una función de costo lineal puede expresarse como:

\[
T(n) = cn
\]

donde \(c\) representa el costo constante de procesar un elemento y \(n\) representa la cantidad de elementos de la entrada.

La expresión indica que el costo aumenta al mismo ritmo que la entrada. Si se duplican los elementos, el número esperado de operaciones también se duplica aproximadamente.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_lineal.png" alt="Representación gráfica de 2.1.2.3 complejidad lineal"><figcaption>Representación gráfica de 2.1.2.3 complejidad lineal.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../2-complejidad-logaritmica/">← 2.1.2.2 Complejidad logarítmica</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../4-complejidad-log-lineal/">2.1.2.4 Complejidad log-lineal →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
