<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.7 Ciclo sin dependencia de la entrada

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo7_(ciclo_sin_dependencia).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ciclo ejecuta siempre \(10\,000\) iteraciones. Esa cantidad es fija y no cambia con el valor de \(n\).

### Código analizado

<!-- book-code:start -->

Listado original del libro, página 164 (Java).

```java
public static void iterar() {
    for (int i = 0; i < 10000000; i++) {
        System.out.println(i);
    }
}
```

<!-- book-code:end -->

### Análisis esperado

#### Complejidad temporal

\(T(n)\in O(1)\) respecto a \(n\), aunque la constante de trabajo sea grande.

#### Complejidad espacial

\(S(n)\in O(1)\) porque el ciclo utiliza una cantidad fija de variables.

### Simulaciones experimentales

Cada experimento ejecuta el mismo algoritmo para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La preparación de la entrada se realiza fuera de la medición temporal. En memoria se reporta el espacio adicional utilizado durante la operación.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ciclo_sin_dependencia_tiempo.png" alt="Comportamiento temporal experimental de 4.4.4.7 ciclo sin dependencia de la entrada"><figcaption>Comportamiento temporal experimental de 4.4.4.7 ciclo sin dependencia de la entrada.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ciclo_sin_dependencia_espacio.png" alt="Comportamiento espacial experimental de 4.4.4.7 ciclo sin dependencia de la entrada"><figcaption>Comportamiento espacial experimental de 4.4.4.7 ciclo sin dependencia de la entrada.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo6/">← 4.4.4.6 Algoritmo con estructura deliberadamente compleja</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo8/">4.4.4.8 Ciclo con límite fijo y función de costo lineal →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
