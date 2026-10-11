# Búsqueda exponencial

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 7</span>

La búsqueda exponencial localiza el rango donde puede estar el objetivo duplicando el índice en cada paso (1, 2, 4, 8, 16, …) hasta encontrar un elemento mayor o igual al objetivo. Luego aplica búsqueda binaria sobre ese rango acotado. Requiere que el arreglo esté ordenado.

Es especialmente eficaz cuando el objetivo está cerca del inicio del arreglo, ya que la fase de duplicación llega rápidamente al rango correcto.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/5_busqueda_exponencial.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Análisis de complejidad

### Resumen general

La búsqueda exponencial requiere un arreglo ordenado: duplica el límite de exploración y después aplica búsqueda binaria en el intervalo identificado. El costo depende de la posición del objetivo y queda acotado logarítmicamente por el tamaño del arreglo.

### Versión iterativa

En la implementación iterativa, la fase exponencial necesita pocas comparaciones para ubicar un intervalo cuyo extremo superior supera o alcanza el objetivo. La fase binaria final conserva el crecimiento logarítmico.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(1)\) | \(\Theta(1)\) | El objetivo coincide con el primer elemento o el intervalo inicial resuelve la búsqueda. |
| Caso promedio | \(\Theta(\log_2(n))\) | \(\Theta(1)\) | Con posiciones equiprobables del objetivo, se combinan varios avances exponenciales con la búsqueda binaria. |
| Peor caso | \(O(\log_2(n))\) | \(O(1)\) | El objetivo está cerca del final o está ausente y se explora un intervalo grande. |

### Versión recursiva

Si el recorrido se expresa mediante llamadas recursivas, la fase de expansión y la fase binaria pueden apilar llamadas. La cantidad total de niveles sigue siendo logarítmica porque los índices crecen por duplicación y el rango final se divide a la mitad.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(1)\) | \(\Omega(1)\) | El objetivo coincide con el primer elemento o el intervalo inicial resuelve la búsqueda. |
| Caso promedio | \(\Theta(\log_2(n))\) | \(\Theta(\log_2(n))\) | Con posiciones equiprobables del objetivo, se combinan varios avances exponenciales con la búsqueda binaria. |
| Peor caso | \(O(\log_2(n))\) | \(O(\log_2(n))\) | El objetivo está cerca del final o está ausente y se explora un intervalo grande. |

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y abra la carpeta de notebooks del capítulo con Jupyter Lab:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir el laboratorio del capítulo 7 | `jupyter lab simulaciones/capitulo7/notebooks/` |

Jupyter Lab abrirá la carpeta; elija una simulación y ejecute todas sus celdas.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->
