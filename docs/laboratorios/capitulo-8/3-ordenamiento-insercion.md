# Ordenamiento por inserción

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 8</span>

El ordenamiento por inserción construye el arreglo ordenado de izquierda a derecha: toma cada elemento y lo inserta en su posición correcta dentro del subarreglo ya ordenado, desplazando los elementos mayores hacia la derecha.

Es muy eficiente para arreglos casi ordenados (\(O(n)\) en el mejor caso) y es el algoritmo preferido para arreglos pequeños dentro de implementaciones híbridas como Timsort.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/3_ordenamiento_insercion.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Análisis de complejidad

### Resumen general

El ordenamiento por inserción desplaza cada elemento hasta su posición en el prefijo ordenado. El tiempo depende de cuántos desplazamientos exige el orden inicial y el espacio auxiliar es constante.

### Versión iterativa

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(n)\) | \(\Omega(1)\) | El arreglo ya está ordenado y cada elemento permanece en su posición. |
| Caso promedio | \(\Theta(n^2)\) | \(\Theta(1)\) | Con valores en orden aleatorio, cada inserción desplaza parte del prefijo ordenado. |
| Peor caso | \(O(n^2)\) | \(O(1)\) | El arreglo está en orden inverso y cada nuevo elemento desplaza todo el prefijo. |

## Variante: inserción binaria

El ordenamiento por inserción localiza, para cada elemento, la posición que debe ocupar dentro del prefijo ya ordenado. En la versión clásica esa búsqueda se hace de derecha a izquierda mediante comparaciones consecutivas. La variante de **inserción binaria** aprovecha que el prefijo `arr[0:i]` ya está ordenado y usa búsqueda binaria para encontrar la posición de inserción.

La mejora principal está en la cantidad de comparaciones usadas para decidir la posición del elemento: en lugar de revisar linealmente el prefijo, la búsqueda binaria reduce el rango activo a la mitad en cada comparación. Esto puede bajar las comparaciones de búsqueda de un comportamiento lineal por iteración a uno logarítmico por iteración.

El desplazamiento de elementos sigue siendo necesario, porque insertar dentro de un arreglo exige mover una sección hacia la derecha para abrir espacio. Por eso la complejidad temporal total permanece cuadrática en el peor caso, aunque el número de comparaciones puede disminuir de forma importante.

## Comparación entre inserción clásica e inserción binaria

La siguiente animación ejecuta ambas variantes sobre el mismo arreglo. La columna **Pasos** permite observar cómo cambia el número de operaciones visibles cuando la posición de inserción se localiza mediante búsqueda lineal o mediante búsqueda binaria.

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
