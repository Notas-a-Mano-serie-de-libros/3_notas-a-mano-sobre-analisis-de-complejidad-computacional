<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>

# 7.9 Ejercicios propuestos

<span class="chapter-kicker">Capítulo 7</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/ejercicios_propuestos.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

Los enunciados de esta sección se conservan en el documento PDF del capítulo. Ábrelo para consultar la formulación completa, las condiciones y la numeración original.

<div class="lab-action">
<a class="md-button md-button--primary pdf-button" href="../../../assets/pdfs/capitulo-7-ejercicios-propuestos.pdf" target="_blank" rel="noopener noreferrer"><span aria-hidden="true">PDF</span> Consultar ejercicios propuestos</a>
<small class="lab-action__note">El documento se abrirá en una pestaña nueva.</small>
</div>

Este laboratorio desarrolla los ejercicios propuestos 1 y 2 mediante una simulación configurable. Permite escoger el algoritmo, el tipo de complejidad, el máximo \(n\), la cantidad de puntos y el caso de ejecución. Cada fila de la tabla indica si el valor fue medido o proyectado; por encima de \(10^6\) se usa una proyección teórica calibrada con las mediciones seguras.

### Ejercicios opcionales

Se desarrollan los ejercicios opcionales 2, 3 y 4. El ejercicio opcional 1 no se incluye, como se solicitó.

La búsqueda ternaria recursiva conserva la siguiente referencia para el selector temporal/espacial:

<table><tbody><tr><td>Caso promedio</td><td>\(\Theta(\log_3(n))\)</td><td>\(\Theta(\log_3(n))\)</td></tr><tr><td>Peor caso</td><td>\(O(\log_3(n))\)</td><td>\(O(\log_3(n))\)</td></tr></tbody></table>


---

### Opcional 2: aplicaciones comunes

- **Búsqueda secuencial:** colecciones pequeñas o sin ordenar, flujos de datos y comprobaciones donde preparar un índice costaría más que recorrer la entrada.
- **Búsqueda binaria:** catálogos ordenados, tablas de símbolos, búsqueda de límites y consultas sobre datos estáticos.
- **Búsqueda por interpolación:** índices numéricos con distribución aproximadamente uniforme, como identificadores o marcas temporales regulares.
- **Búsqueda por saltos:** estructuras ordenadas con acceso por posición; reduce saltos respecto de la búsqueda secuencial y mantiene una implementación sencilla.
- **Búsqueda exponencial:** colecciones ordenadas de tamaño desconocido o potencialmente no acotado; primero localiza un intervalo y luego aplica búsqueda binaria.
- **Búsqueda ternaria:** búsqueda sobre dominios ordenados y, en su variante de optimización, funciones unimodales. Para arreglos suele preferirse la binaria porque hace menos comparaciones por nivel.

### Opcional 3: otros algoritmos de búsqueda

#### Búsqueda en tablas hash

Calcula una posición a partir de una función hash. Su tiempo esperado es \(\Theta(1)\) para insertar, consultar o eliminar, aunque las colisiones pueden llevar el peor caso a \(\Theta(n)\). Requiere \(\Theta(n)\) espacio adicional.

#### Búsqueda en árboles balanceados

Árboles AVL y rojo-negro conservan altura \(\Theta(\log(n))\), por lo que búsqueda, inserción y eliminación cuestan \(\Theta(\log(n))\). El almacenamiento de nodos ocupa \(\Theta(n)\).

#### Búsqueda en tries

Un trie procesa una clave carácter por carácter. Para una clave de longitud \(m\), la búsqueda cuesta \(\Theta(m)\), independiente del número total de claves, a cambio de un consumo de memoria que puede ser elevado.

#### Búsqueda primero en anchura y profundidad

En grafos, BFS y DFS recorren vértices y aristas en \(\Theta(V+E)\). BFS necesita una cola y encuentra caminos mínimos en grafos no ponderados; DFS usa una pila o recursión y es útil para conectividad, ciclos y ordenamiento topológico.

### Opcional 4: búsquedas sobre matrices

Para una matriz de \(f\) filas y \(c\) columnas, una búsqueda secuencial revisa hasta \(fc\) elementos: tiempo \(\Theta(fc)\) y espacio auxiliar \(\Theta(1)\). Si se define \(n=f=c\), el costo es \(\Theta(n^2)\).

Si cada fila está ordenada, puede aplicarse búsqueda binaria en cada una: \(\Theta(f \cdot \log c)\). Si toda la matriz está ordenada como una secuencia y se admite acceso por índice, puede interpretarse la posición lineal \(p\) como \((p//c,p\bmod c)\) y buscar en \(\Theta(\log(fc))\).

Cuando filas y columnas están ordenadas de forma creciente, el recorrido desde la esquina superior derecha elimina una fila o una columna en cada comparación. Su tiempo es \(\Theta(f+c)\) y su espacio auxiliar \(\Theta(1)\). Interpolación, saltos, exponencial y ternaria requieren definir primero qué orden global garantiza la matriz; sin esa condición no pueden descartar regiones correctamente.

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-busquedas/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../6-busqueda-ternaria/">← 7.7 Búsqueda ternaria</a><a class="section-step__index" href="../">Capítulo 7</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-6/">← Capítulo 6</a><a class="chapter-nav__index" href="../">Capítulo 7</a><a class="chapter-nav__next" href="../../capitulo-8/">Capítulo 8 →</a></nav>
