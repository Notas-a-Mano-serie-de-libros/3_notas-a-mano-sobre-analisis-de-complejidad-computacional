<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.0 Complejidad sublineal

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/2_complejidad_logaritmica.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">La búsqueda binaria ilustra un crecimiento logarítmico.</small>
</div>

Un algoritmo tiene complejidad temporal **sublineal** cuando su costo crece más lentamente que el tamaño de la entrada. En términos asintóticos, una función \(T(n)\) es estrictamente sublineal si:

\[
T(n)\in o(n),
\]

lo que equivale a exigir:

\[
\lim_{n\to\infty}\frac{T(n)}{n}=0.
\]

Esta condición permite distinguir el crecimiento sublineal de una función simplemente acotada por \(O(n)\). Por ejemplo, una función lineal también pertenece a \(O(n)\), pero no pertenece a \(o(n)\).

## Formas habituales

| Familia | Ejemplo | Relación con \(n\) |
| --- | --- | --- |
| Constante | \(T(n)=c\) | El trabajo no aumenta con la entrada. |
| Logarítmica | \(T(n)=c\log_b(n)\) | El trabajo aumenta por niveles de reducción. |
| Raíz | \(T(n)=c\sqrt{n}\) | Se inspecciona una fracción decreciente de la entrada. |
| Casi lineal sublineal | \(T(n)=n/\log_b(n)\) | Crece cerca de \(n\), pero su cociente con \(n\) tiende a cero. |

Todas satisfacen \(T(n)/n\to 0\). Sin embargo, pertenecen a familias diferentes y pueden comportarse de manera muy distinta para un mismo tamaño de entrada.

## ¿Cómo es posible examinar menos de \(n\) elementos?

Un algoritmo sublineal no suele leer toda la entrada. Para lograrlo necesita aprovechar información adicional o aceptar una respuesta que no requiera inspección exhaustiva. La búsqueda binaria, por ejemplo, utiliza el orden previo de una colección para descartar la mitad del intervalo en cada comparación. Los algoritmos de muestreo y aproximación pueden estudiar únicamente una parte de los datos, aunque entonces sus garantías dependen del modelo empleado.

Esto impone un límite importante: si resolver correctamente un problema exige verificar cada elemento de una entrada arbitraria, ningún algoritmo determinista puede hacerlo en tiempo sublineal bajo el modelo de acceso habitual. El beneficio no surge gratuitamente; proviene de una estructura previa, un índice, una distribución conocida o una garantía más débil sobre la respuesta.

## Relación con las siguientes familias

La complejidad constante y la logarítmica son casos sublineales y se analizan por separado en las páginas siguientes. La complejidad lineal marca la frontera: cuando \(T(n)\in\Theta(n)\), el cociente \(T(n)/n\) tiende a una constante positiva en lugar de tender a cero.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../1-complejidad-constante/">2.1.2.1 Complejidad constante →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
