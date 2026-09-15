<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# Ampliación · Ordenamiento Shell

<span class="chapter-kicker">Capítulo 8</span>

El ordenamiento Shell generaliza la idea del ordenamiento por inserción. En lugar de comparar solo elementos contiguos, primero compara elementos separados por un valor h determinado. Después reduce progresivamente ese valor h hasta llegar a 1, momento en el que realiza una pasada equivalente a inserción sobre un arreglo que ya quedó parcialmente organizado.

La ventaja práctica aparece porque los elementos pueden desplazarse grandes distancias durante las primeras pasadas. Cuando h se vuelve pequeño, el arreglo suele estar mucho más cerca de su posición final y las pasadas restantes requieren menos movimientos.

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/4_ordenamiento_shell.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
</div>

<!-- book-code:start -->

El libro no incluye un listado de implementación para este tema.

<!-- book-code:end -->

### Análisis de complejidad

#### Resumen general

Shell ordena mediante inserciones entre elementos separados por saltos decrecientes. El tiempo depende de la secuencia de saltos y del orden de los datos; el espacio auxiliar permanece constante.

#### Versión iterativa

La tabla corresponde a la secuencia original de Shell: \(\lfloor n/2\rfloor\), \(\lfloor n/4\rfloor\), hasta \(1\). Otras secuencias pueden modificar las cotas temporales.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Theta(n\cdot\log_2(n))\) | \(\Theta(1)\) | El arreglo ya está ordenado y cada pasada verifica los elementos sin desplazarlos. |
| Caso promedio | Depende de la distribución de los datos | \(\Theta(1)\) | Las pasadas realizan distintos números de desplazamientos según el orden inicial; no se presupone una única cota ajustada. |
| Peor caso | \(O(n^2)\) | \(O(1)\) | Un orden desfavorable requiere numerosos desplazamientos con la secuencia original de saltos. |

### Comparación de secuencias de h

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y abra la carpeta de notebooks del capítulo con Jupyter Lab:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir el laboratorio del capítulo 8 | `jupyter lab simulaciones/capitulo8/notebooks/` |

Jupyter Lab abrirá la carpeta; elija una simulación y ejecute todas sus celdas.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../3-ordenamiento-insercion/">← 8.4 Ordenamiento por inserción</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../5-ordenamiento-mezcla/">8.5 Ordenamiento por mezcla →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
