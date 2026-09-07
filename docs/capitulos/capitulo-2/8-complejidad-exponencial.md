<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.8 Complejidad exponencial

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/8_complejidad_exponencial.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar notebook en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: Fibonacci recursivo sin memoización

El ejemplo calcula Fibonacci mediante dos llamadas recursivas en cada paso no trivial. Muchas llamadas repiten los mismos subproblemas, lo que genera un árbol de ejecución grande.

Esta repetición explica por qué el tiempo crece de forma exponencial cuando \(n\) aumenta.


---

### Código del ejemplo

=== "Pseudocódigo"

    ```text
    función fibonacci(n)
        si n ≤ 1 entonces retornar n
        retornar fibonacci(n - 1) + fibonacci(n - 2)
    ```

=== "Python"

    ```python
    def fibonacci(n):
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    ```

=== "Java"

    ```java
    static long fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
    ```

=== "C"

    ```c
    long fibonacci(int n) {
        if (n <= 1) return n;
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
    ```

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo hasta ese máximo se divide en varios tamaños para conservar la forma experimental de la curva, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor reportado en la tabla y en la figura es el promedio de esas ejecuciones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones. Si el tamaño elegido supera el límite seguro para el entorno, la tabla marca esos puntos como **Solo teórico**.

### Detalle teórico

La complejidad exponencial aparece cuando cada llamada o decisión abre múltiples ramas nuevas. El número de subproblemas crece de forma multiplicativa.

Este tipo de crecimiento se vuelve costoso muy rápido. Incluso incrementos pequeños en \(n\) pueden producir aumentos grandes en el tiempo de ejecución.

Para una entrada de tamaño \(n\), una función de costo exponencial puede expresarse como:

\[
T(n) = c2^n
\]

donde \(2^n\) representa un árbol de decisiones que duplica aproximadamente la cantidad de trabajo por cada incremento de \(n\).

La base puede cambiar según el algoritmo, pero la característica importante es que la variable aparece en el exponente.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_exponencial.png" alt="Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 1 de 5"><figcaption>Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 1 de 5.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-2/analisis_eficiencia/complejidad_temporal/complejidad_exponencial_1.png" alt="Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 2 de 5"><figcaption>Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 2 de 5.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-2/analisis_eficiencia/complejidad_temporal/complejidad_exponencial_2.png" alt="Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 3 de 5"><figcaption>Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 3 de 5.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-2/analisis_eficiencia/complejidad_espacial/complejidad_exponencial_1.png" alt="Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 4 de 5"><figcaption>Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 4 de 5.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-2/analisis_eficiencia/complejidad_espacial/complejidad_exponencial_2.png" alt="Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 5 de 5"><figcaption>Secuencia visual de 2.1.2.8 complejidad exponencial · paso representativo 5 de 5.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../7-complejidad-polinomial-general/">← 2.1.2.7 Complejidad polinomial general</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../9-complejidad-factorial/">2.1.2.9 Complejidad factorial →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
