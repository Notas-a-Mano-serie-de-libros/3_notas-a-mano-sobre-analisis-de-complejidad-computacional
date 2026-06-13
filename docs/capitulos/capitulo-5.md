<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-6/">Capítulo 6 →</a></nav>

# Capítulo 5 · Relaciones de recurrencia

**Páginas 179–222.** El capítulo introduce las recurrencias como representaciones del costo de problemas recursivos y compara métodos para resolverlas.

## Formas estudiadas

Las recurrencias se clasifican como lineales o no lineales, homogéneas o no homogéneas, y con coeficientes constantes o variables. En el análisis algorítmico aparecen dos transformaciones principales:

=== "Reducción"

    El tamaño disminuye en una cantidad fija:

    \[
    C(n)=\sum_{i=1}^{m}a_iC(n-b_i)+f(n)
    \]

=== "División"

    El tamaño se multiplica por factores entre cero y uno:

    \[
    C(n)=\sum_{i=1}^{m}a_iC(b_i n)+f(n),\qquad 0<b_i<1
    \]

En ambos casos, \(m\) representa términos recursivos distintos, \(a_i\) su multiplicidad, \(b_i\) la transformación del tamaño y \(f(n)\) el trabajo externo.

## Métodos de solución

| Método | Aporte principal |
| --- | --- |
| Sustitución iterativa | Expande hasta reconocer un patrón. |
| Árbol de recurrencia | Distribuye el costo por niveles. |
| Teorema maestro básico | Resuelve su forma canónica de división. |
| Teorema maestro extendido | Incorpora factores polinómicos y logarítmicos. |
| Teorema maestro generalizado | Usa Akra–Bazzi para factores de división distintos. |
| Ecuación característica | Obtiene soluciones exactas para recurrencias lineales de coeficientes constantes. |

[Abrir árbol de recurrencia](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo5/notebooks/0_arboles_recursion.ipynb){ .md-button .md-button--primary }
[Explorar métodos](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo5/notebooks/1_metodos_solucion_relaciones_recurrencia.ipynb){ .md-button }

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-6/">Capítulo 6 →</a></nav>
