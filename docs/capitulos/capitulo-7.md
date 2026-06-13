<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-8/">Capítulo 8 →</a></nav>

# Capítulo 7 · Algoritmos de búsqueda

<span class="chapter-kicker">Páginas 259–316</span>

El capítulo compara estrategias para localizar elementos y muestra por qué la organización de los datos condiciona el algoritmo que conviene utilizar. El material digital conserva la estructura de la obra.

## 1. Comparación general

La comparación reúne requisitos, idea central y complejidad de cada búsqueda. No existe un algoritmo universalmente superior: ordenar previamente, disponer de acceso aleatorio o conocer la distribución de las claves cambia la decisión.

| Algoritmo | Requisito principal | Tiempo característico |
| --- | --- | --- |
| Secuencial | Ninguno | \(O(n)\) |
| Binaria | Datos ordenados | \(O(\log n)\) |
| Interpolación | Datos ordenados y bien distribuidos | promedio \(O(\log\log n)\) |
| Por saltos | Datos ordenados | \(O(\sqrt n)\) |
| Exponencial | Datos ordenados | \(O(\log n)\) |
| Ternaria | Datos ordenados | \(O(\log n)\) |

[Consultar la comparación completa](../algoritmos/busquedas.md){ .md-button .md-button--primary }

## 2. Algoritmos específicos

La obra desarrolla seis algoritmos: búsqueda secuencial, binaria, por interpolación, por saltos, exponencial y ternaria. Cada estudio incluye su funcionamiento, implementación, análisis temporal y espacial, escenarios de aplicación, ventajas y limitaciones.

## 3. Solución de los ejercicios propuestos

Los cuadernos permiten ejecutar los algoritmos, cambiar entradas y contrastar el comportamiento observado con el análisis teórico. La solución se presenta como material de estudio reproducible, no como sustituto del razonamiento previo.

[Abrir comparación en Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/0_comparacion_busquedas.ipynb){ .md-button }
[Ver soluciones del capítulo](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/tree/main/capitulo7/notebooks){ .md-button }

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-8/">Capítulo 8 →</a></nav>
