<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.5 Ciclos con incremento no lineal

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo5_(ciclos_incremento_no_lineal).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ciclo interior avanza de dos en dos, pero continúa recorriendo una cantidad proporcional a \(n\) de posiciones por cada fila.

### Código analizado

<!-- book-code:start -->

Listado original del libro, página 158 (Java).

```java
public static void recorrerMatrizVacia(int m, int n) {
    int[][] matriz = new int[m][n];
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j+=2) {
            // Sin operaciones internas en este ciclo
        }
    }
}
```

<!-- book-code:end -->

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
