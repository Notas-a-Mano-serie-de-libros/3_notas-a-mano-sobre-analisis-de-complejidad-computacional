<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.1 Sumar dos números

<span class="chapter-kicker">Capítulo 4</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo1_(sumar_numeros).ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

Este ejemplo analiza una secuencia de una sola operación aritmética. El tamaño de referencia \(n\) cambia, pero la cantidad de instrucciones ejecutadas permanece fija.

### Código analizado

<!-- book-code:start -->

Listado original del libro, página 150 (Java).

```java
public static int sumar(int a, int b) {
    return a + b;
}
```

<!-- book-code:end -->

### Análisis esperado

#### Complejidad temporal

\(T(n)\in O(1)\) porque la suma ejecuta una cantidad constante de operaciones para cada valor de \(n\).

#### Complejidad espacial

\(S(n)\in O(1)\) porque solo se mantienen dos operandos y el resultado.

### Simulaciones experimentales

Cada experimento ejecuta el mismo algoritmo para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La preparación de la entrada se realiza fuera de la medición temporal. En memoria se reporta el espacio adicional utilizado durante la operación.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_suma_dos_numeros_tiempo.png" alt="Comportamiento temporal experimental de 4.4.4.1 sumar dos números"><figcaption>Comportamiento temporal experimental de 4.4.4.1 sumar dos números.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-4/ejemplos/ejemplo_suma_dos_numeros_espacio.png" alt="Comportamiento espacial experimental de 4.4.4.1 sumar dos números"><figcaption>Comportamiento espacial experimental de 4.4.4.1 sumar dos números.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo2-imprimir-elementos-arreglo/">4.4.4.2 Imprimir los elementos de un arreglo →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
