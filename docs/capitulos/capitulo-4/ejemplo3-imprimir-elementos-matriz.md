<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.3 Imprimir los elementos de una matriz

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo3_(imprimir_elementos_matriz).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar notebook en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El algoritmo recorre una matriz cuadrada de \(n\times n\). La matriz se prepara antes de medir para separar el costo del recorrido.

### Código analizado

=== "Pseudocódigo"

    ```text
    procedimiento recorrerMatriz(matriz)
        para cada fila en matriz
            para cada elemento en fila
                visitar elemento
    ```

=== "Python"

    ```python
    def imprimir_matriz(matriz):
        for fila in matriz:
            for elemento in fila:
                _ = elemento
    ```

=== "Java"

    ```java
    static void recorrerMatriz(int[][] matriz) {
        for (int[] fila : matriz) {
            for (int elemento : fila) {
                int visitado = elemento;
            }
        }
    }
    ```

=== "C"

    ```c
    void recorrerMatriz(int filas, int columnas, int matriz[filas][columnas]) {
        for (int i = 0; i < filas; i++) {
            for (int j = 0; j < columnas; j++) {
                int visitado = matriz[i][j];
            }
        }
    }
    ```


---

### Análisis esperado

#### Complejidad temporal

\(T(n)\in O(n^2)\) porque se visitan las \(n^2\) posiciones de la matriz.

#### Complejidad espacial

\(S(n)\in O(1)\) en espacio adicional porque la matriz pertenece a la entrada.

### Simulaciones experimentales

Cada experimento ejecuta el mismo algoritmo para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La preparación de la entrada se realiza fuera de la medición temporal. En memoria se reporta el espacio adicional utilizado durante la operación.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_imprimir_matriz_tiempo.png" alt="Comportamiento temporal experimental de 4.4.4.3 imprimir los elementos de una matriz"><figcaption>Comportamiento temporal experimental de 4.4.4.3 imprimir los elementos de una matriz.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_imprimir_matriz_espacio.png" alt="Comportamiento espacial experimental de 4.4.4.3 imprimir los elementos de una matriz"><figcaption>Comportamiento espacial experimental de 4.4.4.3 imprimir los elementos de una matriz.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo2-imprimir-elementos-arreglo/">← 4.4.4.2 Imprimir los elementos de un arreglo</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo4-inicializar-matriz-variable/">4.4.4.4 Inicializar una matriz variable →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
