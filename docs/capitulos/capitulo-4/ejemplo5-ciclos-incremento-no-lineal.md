<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.5 Ciclos con incremento no lineal

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo5_(ciclos_incremento_no_lineal).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ciclo interior avanza de dos en dos, pero continúa recorriendo una cantidad proporcional a \(n\) de posiciones por cada fila.

### Código analizado

=== "Pseudocódigo"

    ```text
    procedimiento recorrerConSaltos(n)
        matriz ← nueva matriz n × n
        para i ← 0 hasta n - 1
            para j ← 0 hasta n - 1 con paso 2
                visitar matriz[i][j]
    ```

=== "Python"

    ```python
    def recorrer_matriz_vacia(n):
        matriz = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(0, n, 2):
                _ = matriz[i][j]
    ```

=== "Java"

    ```java
    static void recorrerConSaltos(int n) {
        int[][] matriz = new int[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j += 2) {
                int visitado = matriz[i][j];
            }
    }
    ```

=== "C"

    ```c
    void recorrerConSaltos(int n) {
        int (*matriz)[n] = calloc(n, sizeof *matriz);
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j += 2) {
                int visitado = matriz[i][j];
            }
        free(matriz);
    }
    ```


---

### Análisis esperado

#### Complejidad temporal

\(T(n)\in O(n^2)\): el incremento de dos modifica una constante, no el orden cuadrático.

#### Complejidad espacial

\(S(n)\in O(n^2)\) porque el algoritmo construye una matriz cuadrada.

### Simulaciones experimentales

Cada experimento ejecuta el mismo algoritmo para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La preparación de la entrada se realiza fuera de la medición temporal. En memoria se reporta el espacio adicional utilizado durante la operación.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-4/ejemplos/recorrer_matriz_vacia_tiempo.png" alt="Comportamiento temporal experimental de 4.4.4.5 ciclos con incremento no lineal"><figcaption>Comportamiento temporal experimental de 4.4.4.5 ciclos con incremento no lineal.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-4/ejemplos/recorrer_matriz_vacia_espacio.png" alt="Comportamiento espacial experimental de 4.4.4.5 ciclos con incremento no lineal"><figcaption>Comportamiento espacial experimental de 4.4.4.5 ciclos con incremento no lineal.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo4-inicializar-matriz-variable/">← 4.4.4.4 Inicializar una matriz variable</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo6/">4.4.4.6 Algoritmo con estructura deliberadamente compleja →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
