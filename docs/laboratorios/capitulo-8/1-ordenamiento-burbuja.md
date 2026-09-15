# Ordenamiento burbuja

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 8</span>

El ordenamiento burbuja compara pares de elementos adyacentes e intercambia los que están en orden incorrecto. Repite este proceso hasta que no hay más intercambios. En cada pasada, el elemento mayor no ordenado queda en su posición final.

Es el algoritmo de ordenamiento más intuitivo pero también el menos eficiente en la práctica para arreglos grandes, con complejidad cuadrática en el caso promedio y peor caso.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/1_ordenamiento_burbuja.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Análisis de complejidad

### Resumen general

El ordenamiento burbuja compara pares adyacentes. La versión básica siempre completa sus pasadas; la versión con bandera termina cuando una pasada no produce intercambios. Ambas trabajan sobre el arreglo con espacio auxiliar constante.

### Versión iterativa

La tabla corresponde a la versión con bandera. En la versión básica, los tres casos requieren \(\Theta(n^2)\) tiempo y \(\Theta(1)\) espacio: se hacen \(n \cdot (n-1)/2\) comparaciones sin parada anticipada.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(n)\) | \(\Omega(1)\) | Con bandera: el arreglo ya está ordenado y la primera pasada no realiza intercambios. |
| Caso promedio | \(\Theta(n^2)\) | \(\Theta(1)\) | Los valores están en un orden aleatorio y se requieren varias pasadas con intercambios. |
| Peor caso | \(O(n^2)\) | \(O(1)\) | El arreglo está en orden inverso y se realizan todas las pasadas necesarias. |

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
