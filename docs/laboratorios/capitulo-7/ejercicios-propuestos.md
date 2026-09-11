# Laboratorio de ejercicios propuestos: algoritmos de búsqueda

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 7</span>

Este laboratorio desarrolla los ejercicios propuestos 1 y 2 mediante una simulación configurable. Permite escoger el algoritmo, el tipo de complejidad, el máximo \(n\), la cantidad de puntos y el caso de ejecución. Cada fila de la tabla indica si el valor fue medido o proyectado; por encima de \(10^6\) se usa una proyección teórica calibrada con las mediciones seguras.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/ejercicios_propuestos.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

## Ejercicios opcionales

Se desarrollan los ejercicios opcionales 2, 3 y 4. El ejercicio opcional 1 no se incluye, como se solicitó.

La búsqueda ternaria recursiva conserva la siguiente referencia para el selector temporal/espacial:

<table><tbody><tr><td>Caso promedio</td><td>\(\Theta(\log_3(n))\)</td><td>\(\Theta(\log_3(n))\)</td></tr><tr><td>Peor caso</td><td>\(O(\log_3(n))\)</td><td>\(O(\log_3(n))\)</td></tr></tbody></table>


---

## Opcional 2: aplicaciones comunes

- **Búsqueda secuencial:** colecciones pequeñas o sin ordenar, flujos de datos y comprobaciones donde preparar un índice costaría más que recorrer la entrada.
- **Búsqueda binaria:** catálogos ordenados, tablas de símbolos, búsqueda de límites y consultas sobre datos estáticos.
- **Búsqueda por interpolación:** índices numéricos con distribución aproximadamente uniforme, como identificadores o marcas temporales regulares.
- **Búsqueda por saltos:** estructuras ordenadas con acceso por posición; reduce saltos respecto de la búsqueda secuencial y mantiene una implementación sencilla.
- **Búsqueda exponencial:** colecciones ordenadas de tamaño desconocido o potencialmente no acotado; primero localiza un intervalo y luego aplica búsqueda binaria.
- **Búsqueda ternaria:** búsqueda sobre dominios ordenados y, en su variante de optimización, funciones unimodales. Para arreglos suele preferirse la binaria porque hace menos comparaciones por nivel.

## Opcional 3: otros algoritmos de búsqueda

### Búsqueda en tablas hash

Calcula una posición a partir de una función hash. Su tiempo esperado es \(\Theta(1)\) para insertar, consultar o eliminar, aunque las colisiones pueden llevar el peor caso a \(\Theta(n)\). Requiere \(\Theta(n)\) espacio adicional.

### Búsqueda en árboles balanceados

Árboles AVL y rojo-negro conservan altura \(\Theta(\log(n))\), por lo que búsqueda, inserción y eliminación cuestan \(\Theta(\log(n))\). El almacenamiento de nodos ocupa \(\Theta(n)\).

### Búsqueda en tries

Un trie procesa una clave carácter por carácter. Para una clave de longitud \(m\), la búsqueda cuesta \(\Theta(m)\), independiente del número total de claves, a cambio de un consumo de memoria que puede ser elevado.

### Búsqueda primero en anchura y profundidad

En grafos, BFS y DFS recorren vértices y aristas en \(\Theta(V+E)\). BFS necesita una cola y encuentra caminos mínimos en grafos no ponderados; DFS usa una pila o recursión y es útil para conectividad, ciclos y ordenamiento topológico.

## Opcional 4: búsquedas sobre matrices

Para una matriz de \(f\) filas y \(c\) columnas, una búsqueda secuencial revisa hasta \(fc\) elementos: tiempo \(\Theta(fc)\) y espacio auxiliar \(\Theta(1)\). Si se define \(n=f=c\), el costo es \(\Theta(n^2)\).

Si cada fila está ordenada, puede aplicarse búsqueda binaria en cada una: \(\Theta(f \cdot \log c)\). Si toda la matriz está ordenada como una secuencia y se admite acceso por índice, puede interpretarse la posición lineal \(p\) como \((p//c,p\bmod c)\) y buscar en \(\Theta(\log(fc))\).

Cuando filas y columnas están ordenadas de forma creciente, el recorrido desde la esquina superior derecha elimina una fila o una columna en cada comparación. Su tiempo es \(\Theta(f+c)\) y su espacio auxiliar \(\Theta(1)\). Interpolación, saltos, exponencial y ternaria requieren definir primero qué orden global garantiza la matriz; sin esa condición no pueden descartar regiones correctamente.
