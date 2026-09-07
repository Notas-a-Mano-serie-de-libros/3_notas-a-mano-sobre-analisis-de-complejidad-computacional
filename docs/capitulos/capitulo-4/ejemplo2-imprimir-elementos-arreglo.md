<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.2 Imprimir los elementos de un arreglo

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo2_(imprimir_elementos_arreglo).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar notebook en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El algoritmo visita una vez cada posición de un arreglo de tamaño \(n\). La simulación prepara la entrada antes de medir la operación.

### Código analizado

=== "Pseudocódigo"

    ```text
    procedimiento recorrer(arreglo)
        para cada elemento en arreglo
            visitar elemento
    ```

=== "Python"

    ```python
    def imprimir_elementos(arr):
        for elemento in arr:
            _ = elemento
    ```

=== "Java"

    ```java
    static void recorrer(int[] arreglo) {
        for (int elemento : arreglo) {
            int visitado = elemento;
        }
    }
    ```

=== "C"

    ```c
    void recorrer(const int arreglo[], int n) {
        for (int i = 0; i < n; i++) {
            int visitado = arreglo[i];
        }
    }
    ```


---

### Análisis esperado

#### Complejidad temporal

\(T(n)\in O(n)\) porque el cuerpo del ciclo se ejecuta una vez por cada elemento.

#### Complejidad espacial

\(S(n)\in O(1)\) en espacio adicional: el arreglo se considera la entrada y el recorrido solo conserva la referencia actual.

### Simulaciones experimentales

Cada experimento ejecuta el mismo algoritmo para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La preparación de la entrada se realiza fuera de la medición temporal. En memoria se reporta el espacio adicional utilizado durante la operación.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_imprimir_elementos_tiempo.png" alt="Comportamiento temporal experimental de 4.4.4.2 imprimir los elementos de un arreglo"><figcaption>Comportamiento temporal experimental de 4.4.4.2 imprimir los elementos de un arreglo.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_imprimir_elementos_espacio.png" alt="Comportamiento espacial experimental de 4.4.4.2 imprimir los elementos de un arreglo"><figcaption>Comportamiento espacial experimental de 4.4.4.2 imprimir los elementos de un arreglo.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo1-sumar-numeros/">← 4.4.4.1 Sumar dos números</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo3-imprimir-elementos-matriz/">4.4.4.3 Imprimir los elementos de una matriz →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
