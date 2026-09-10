<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.2 Complejidad logarítmica

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/2_complejidad_logaritmica.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: búsqueda binaria en una lista ordenada

El ejemplo implementa una búsqueda binaria iterativa. En cada vuelta se calcula la posición media del rango activo y se compara el valor encontrado con el objetivo.

Si el valor central no es el buscado, la mitad que no puede contener la respuesta se descarta. La lista completa puede ser muy grande, pero el algoritmo solo conserva dos límites: `bajo` y `alto`. Esa reducción sucesiva explica el comportamiento logarítmico.


---

### Código del ejemplo

=== "Pseudocódigo"

    ```text
    función búsquedaBinaria(A, objetivo)
        bajo ← 0; alto ← longitud(A) - 1
        mientras bajo ≤ alto
            medio ← ⌊(bajo + alto) / 2⌋
            si A[medio] = objetivo entonces retornar medio
            si A[medio] < objetivo entonces bajo ← medio + 1
            en otro caso alto ← medio - 1
        retornar -1
    ```

=== "Python"

    ```python
    def busqueda_binaria(lista, objetivo):
        bajo, alto = 0, len(lista) - 1
        while bajo <= alto:
            medio = (bajo + alto) // 2
            if lista[medio] == objetivo:
                return medio
            if lista[medio] < objetivo:
                bajo = medio + 1
            else:
                alto = medio - 1
        return -1
    ```

=== "Java"

    ```java
    static int busquedaBinaria(int[] a, int objetivo) {
        int bajo = 0, alto = a.length - 1;
        while (bajo <= alto) {
            int medio = bajo + (alto - bajo) / 2;
            if (a[medio] == objetivo) return medio;
            if (a[medio] < objetivo) bajo = medio + 1;
            else alto = medio - 1;
        }
        return -1;
    }
    ```

=== "C"

    ```c
    int busquedaBinaria(const int a[], int n, int objetivo) {
        int bajo = 0, alto = n - 1;
        while (bajo <= alto) {
            int medio = bajo + (alto - bajo) / 2;
            if (a[medio] == objetivo) return medio;
            if (a[medio] < objetivo) bajo = medio + 1;
            else alto = medio - 1;
        }
        return -1;
    }
    ```

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad logarítmica describe algoritmos cuyo costo crece muy lentamente frente al tamaño de la entrada. En lugar de revisar todos los elementos, el algoritmo reduce el espacio de búsqueda en una fracción significativa en cada paso.

Este comportamiento aparece cuando cada decisión descarta una parte grande del problema. Por ejemplo, en una lista ordenada, la búsqueda binaria compara contra el elemento central y conserva únicamente la mitad donde todavía puede estar el valor buscado.

Por esa razón, aumentar mucho el tamaño de la entrada no produce un aumento proporcional en el número de pasos: duplicar n normalmente añade solo una decisión adicional.

Para una entrada de tamaño \(n\), una función de costo logarítmico puede expresarse como:

\[
T(n) = c \log_2(n)
\]

donde \(T(n)\) representa el costo de ejecución, \(c\) representa el costo constante de cada comparación o decisión, y \(\log_2(n)\) representa la cantidad aproximada de veces que la entrada puede dividirse entre dos.

La base del logaritmo no cambia la familia de crecimiento. En general, una función logarítmica puede expresarse como \(\log_\ell(n)\), donde \(\ell\) es la base del logaritmo. Si se desea expresar ese logaritmo usando otra base \(b\), se aplica el cambio de base:

\[
\log_\ell(n) = \frac{\log_b(n)}{\log_b(\ell)}
\]

El término \(\frac{1}{\log_b(\ell)}\) es una constante multiplicativa. Por eso, \(\log_2(n)\), \(\log_{10}(n)\) y \(\log_e(n)\) crecen con la misma forma general: cambian de escala vertical, pero pertenecen a la misma familia logarítmica.

La expresión muestra que el costo crece por niveles de división. Si \(n\) pasa de \(1.000\) a \(1.000.000\), el crecimiento no sigue la diferencia entre esos tamaños, sino la cantidad de divisiones necesarias para reducir el rango hasta encontrar o descartar el elemento.

Una característica especialmente importante de esta familia es que crece extremadamente lento. Incluso cuando el tamaño de entrada alcanza valores enormes, el número de pasos logarítmicos permanece manejable. Por ejemplo, si \(n=10^{100}\), entonces:

\[
\log_2(10^{100}) = 100\log_2(10) \approx 332.19
\]

Esto significa que una entrada con cien órdenes de magnitud puede reducirse, en un modelo logarítmico base dos, a poco más de trescientas decisiones teóricas. Encontrar soluciones de orden constante suele ser una tarea bastante complicada, porque exige que el costo no dependa del tamaño de la entrada. Cuando eso no es posible, la siguiente mejor opción práctica suelen ser las soluciones logarítmicas: todavía dependen de \(n\), pero lo hacen de una manera muy lenta.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_logaritmica.png" alt="Representación gráfica de 2.1.2.2 complejidad logarítmica"><figcaption>Representación gráfica de 2.1.2.2 complejidad logarítmica.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../1-complejidad-constante/">← 2.1.2.1 Complejidad constante</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../3-complejidad-lineal/">2.1.2.3 Complejidad lineal →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
