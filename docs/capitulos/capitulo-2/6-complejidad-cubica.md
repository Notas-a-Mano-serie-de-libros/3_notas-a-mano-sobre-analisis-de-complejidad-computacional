<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.6 Complejidad cúbica

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/6_complejidad_cubica.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: multiplicación clásica de matrices

El ejemplo calcula cada posición de la matriz resultado mediante tres índices: fila, columna y posición interna de acumulación.

Como los tres recorridos dependen de \(n\), el número total de operaciones crece de acuerdo con \(n^3\).


---

### Código del ejemplo

=== "Pseudocódigo"

    ```text
    función multiplicar(A, B, n)
        C ← matriz n × n inicializada en 0
        para i ← 0 hasta n - 1
            para j ← 0 hasta n - 1
                para k ← 0 hasta n - 1
                    C[i,j] ← C[i,j] + A[i,k] × B[k,j]
        retornar C
    ```

=== "Python"

    ```python
    def multiplicar_matrices(a, b):
        n = len(a)
        c = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    c[i][j] += a[i][k] * b[k][j]
        return c
    ```

=== "Java"

    ```java
    static int[][] multiplicar(int[][] a, int[][] b) {
        int n = a.length;
        int[][] c = new int[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                for (int k = 0; k < n; k++) c[i][j] += a[i][k] * b[k][j];
        return c;
    }
    ```

=== "C"

    ```c
    void multiplicar(int n, int a[n][n], int b[n][n], int c[n][n]) {
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++) {
                c[i][j] = 0;
                for (int k = 0; k < n; k++) c[i][j] += a[i][k] * b[k][j];
            }
    }
    ```

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad cúbica aparece cuando tres recorridos anidados dependen del tamaño \(n\). Este patrón es común en algoritmos que combinan tres dimensiones o tres índices.

Un ejemplo representativo es la multiplicación clásica de matrices cuadradas, donde cada posición del resultado se calcula acumulando productos a lo largo de una tercera dimensión.

Para una entrada de tamaño \(n\), una función de costo cúbico puede expresarse como:

\[
T(n) = cn^3
\]

donde \(n^3\) representa la cantidad de iteraciones producidas por tres ciclos anidados.

El crecimiento es muy pronunciado: duplicar \(n\) puede multiplicar el trabajo aproximadamente por ocho.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_cubica.png" alt="Representación gráfica de 2.1.2.6 complejidad cúbica"><figcaption>Representación gráfica de 2.1.2.6 complejidad cúbica.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../5-complejidad-cuadratica/">← 2.1.2.5 Complejidad cuadrática</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../7-complejidad-polinomial-general/">2.1.2.7 Complejidad polinomial general →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
