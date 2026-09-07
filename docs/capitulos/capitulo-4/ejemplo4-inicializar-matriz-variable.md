<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.4 Inicializar una matriz variable

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo4_(inicializar_matriz_variable).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar notebook en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

Este algoritmo recibe \(n\) y construye internamente una matriz de \(n\times n\) antes de recorrerla.

### Código analizado

=== "Pseudocódigo"

    ```text
    procedimiento crearYRecorrer(n)
        matriz ← nueva matriz n × n inicializada en 0
        para cada fila en matriz
            para cada elemento en fila
                visitar elemento
    ```

=== "Python"

    ```python
    def imprimir_matriz_creada(n):
        matriz = [[0 for _ in range(n)] for _ in range(n)]
        for fila in matriz:
            for elemento in fila:
                _ = elemento
    ```

=== "Java"

    ```java
    static void crearYRecorrer(int n) {
        int[][] matriz = new int[n][n];
        for (int[] fila : matriz) {
            for (int elemento : fila) {
                int visitado = elemento;
            }
        }
    }
    ```

=== "C"

    ```c
    void crearYRecorrer(int n) {
        int (*matriz)[n] = calloc(n, sizeof *matriz);
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++) {
                int visitado = matriz[i][j];
            }
        free(matriz);
    }
    ```


---

### Análisis esperado

#### Complejidad temporal

\(T(n)\in O(n^2)\) por la creación y el recorrido de \(n^2\) posiciones.

#### Complejidad espacial

\(S(n)\in O(n^2)\) porque la matriz se crea dentro del algoritmo.

### Simulaciones experimentales

Cada experimento ejecuta el mismo algoritmo para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La preparación de la entrada se realiza fuera de la medición temporal. En memoria se reporta el espacio adicional utilizado durante la operación.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_inicializar_matriz_tiempo.png" alt="Comportamiento temporal experimental de 4.4.4.4 inicializar una matriz variable"><figcaption>Comportamiento temporal experimental de 4.4.4.4 inicializar una matriz variable.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_inicializar_matriz_espacio.png" alt="Comportamiento espacial experimental de 4.4.4.4 inicializar una matriz variable"><figcaption>Comportamiento espacial experimental de 4.4.4.4 inicializar una matriz variable.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo3-imprimir-elementos-matriz/">← 4.4.4.3 Imprimir los elementos de una matriz</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo5-ciclos-incremento-no-lineal/">4.4.4.5 Ciclos con incremento no lineal →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
