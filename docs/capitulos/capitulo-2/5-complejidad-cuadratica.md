<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.5 Complejidad cuadrática

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/5_complejidad_cuadratica.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar notebook en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: recorrer una matriz

El ejemplo recorre todas las posiciones de una matriz. Si la matriz tiene \(n\) filas y \(n\) columnas, el cuerpo interno se ejecuta \(n \times n\) veces.

La estructura de dos ciclos anidados hace que el número de accesos crezca cuadráticamente con el tamaño lateral de la matriz.


---

### Código del ejemplo

=== "Pseudocódigo"

    ```text
    función sumarMatriz(M)
        suma ← 0
        para cada fila en M
            para cada valor en fila
                suma ← suma + valor
        retornar suma
    ```

=== "Python"

    ```python
    def recorrer_matriz(matriz):
        suma = 0
        for fila in matriz:
            for valor in fila:
                suma += valor
        return suma
    ```

=== "Java"

    ```java
    static long sumarMatriz(int[][] m) {
        long suma = 0;
        for (int[] fila : m)
            for (int valor : fila) suma += valor;
        return suma;
    }
    ```

=== "C"

    ```c
    long sumarMatriz(int filas, int columnas, int m[filas][columnas]) {
        long suma = 0;
        for (int i = 0; i < filas; i++)
            for (int j = 0; j < columnas; j++) suma += m[i][j];
        return suma;
    }
    ```

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad cuadrática describe algoritmos cuyo costo crece con el cuadrado del tamaño de entrada. Suele aparecer cuando dos ciclos anidados dependen de \(n\).

En estos casos, cada elemento puede relacionarse con muchos otros elementos, o se recorre una estructura bidimensional de tamaño \(n \times n\).

Para una entrada de tamaño \(n\), una función de costo cuadrático puede expresarse como:

\[
T(n) = cn^2
\]

donde \(c\) representa el costo constante de cada operación elemental y \(n^2\) representa la cantidad de combinaciones o posiciones evaluadas.

El crecimiento es mucho más rápido que el lineal: duplicar \(n\) puede multiplicar el trabajo aproximadamente por cuatro.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_cuadratica.png" alt="Representación gráfica de 2.1.2.5 complejidad cuadrática"><figcaption>Representación gráfica de 2.1.2.5 complejidad cuadrática.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../4-complejidad-log-lineal/">← 2.1.2.4 Complejidad log-lineal</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../6-complejidad-cubica/">2.1.2.6 Complejidad cúbica →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
