<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../../obra/">La obra →</a></nav>

# Capítulo 8 · Algoritmos de ordenamiento

<span class="chapter-kicker">Páginas 317–370</span>

El capítulo estudia cómo distintas estrategias reorganizan una colección y qué costos introducen. La comparación considera tiempo, memoria, estabilidad y condiciones de uso; el material digital sigue las tres partes de la obra.

## 1. Comparación general

| Algoritmo | Mejor caso | Caso promedio | Peor caso | Espacio auxiliar |
| --- | --- | --- | --- | --- |
| Burbuja, versión base | \(O(n^2)\) | \(O(n^2)\) | \(O(n^2)\) | \(O(1)\) |
| Selección | \(O(n^2)\) | \(O(n^2)\) | \(O(n^2)\) | \(O(1)\) |
| Inserción | \(O(n)\) | \(O(n^2)\) | \(O(n^2)\) | \(O(1)\) |
| Mezcla | \(O(n\log n)\) | \(O(n\log n)\) | \(O(n\log n)\) | \(O(n)\) |
| Rápido | \(O(n\log n)\) | \(O(n\log n)\) | \(O(n^2)\) | depende de la partición |
| Radix | \(\Theta(d(n+b))\) | \(\Theta(d(n+b))\) | \(\Theta(d(n+b))\) | \(\Theta(n+b)\) |

!!! info "Burbuja optimizada"
    Una variante que detiene el proceso cuando no hay intercambios alcanza \(O(n)\) en el mejor caso. La tabla separa esta mejora del algoritmo base explicado en la comparación principal.

[Consultar la comparación completa](../algoritmos/ordenamientos.md){ .md-button .md-button--primary }

## 2. Algoritmos específicos

La obra desarrolla burbuja, selección, inserción, mezcla, rápido y radix. Para cada uno se revisan el procedimiento, el código, la complejidad temporal y espacial, las ventajas, las limitaciones y los casos en que su uso resulta razonable.

El repositorio incluye además un laboratorio sobre **Shell sort** como ampliación práctica; no se presenta como un séptimo algoritmo del contenido central del libro.

## 3. Solución de los ejercicios propuestos

Los cuadernos reproducen las ejecuciones y las soluciones de los ejercicios. Pueden abrirse en Colab o ejecutarse localmente con Jupyter y Voilà.

[Abrir comparación en Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/0_comparacion_ordenamientos.ipynb){ .md-button }
[Ver soluciones del capítulo](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/tree/main/capitulo8/notebooks){ .md-button }

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../../obra/">La obra →</a></nav>
