# Búsqueda binaria

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 7</span>

La búsqueda binaria compara el elemento central del arreglo con el objetivo. Si no coincide, descarta la mitad donde el objetivo no puede estar y repite el proceso sobre la mitad restante. Requiere que el arreglo esté ordenado.

Cada comparación reduce el espacio de búsqueda a la mitad, lo que produce una complejidad temporal logarítmica: con un millón de elementos basta con unos 20 pasos.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/2_busqueda_binaria.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Análisis de complejidad

### Resumen general

La búsqueda binaria requiere un arreglo ordenado y reduce el intervalo a la mitad. Ambas versiones realizan un número logarítmico de comparaciones; la iterativa usa espacio constante y la recursiva acumula los marcos de la pila.

### Versión iterativa

En la implementación iterativa, cada comparación calcula el índice medio y conserva solo los límites \(a\) y \(b\). Cada descarte reduce el intervalo activo a la mitad.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(1)\) | \(\Theta(1)\) | El objetivo coincide con el elemento central del intervalo inicial. |
| Caso promedio | \(\Theta(\log_2(n))\) | \(\Theta(1)\) | Con posiciones equiprobables del objetivo, se realizan varias divisiones del intervalo a la mitad. |
| Peor caso | \(O(\log_2(n))\) | \(O(1)\) | El objetivo se encuentra en uno de los niveles más profundos o está ausente y se agota el intervalo. |

### Versión recursiva

En la implementación recursiva, cada llamada recibe un intervalo cuya longitud es aproximadamente la mitad de la anterior. El número de comparaciones es el mismo orden que en la versión iterativa, pero la pila crece con la profundidad de divisiones.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(1)\) | \(\Omega(1)\) | El objetivo coincide con el elemento central del intervalo inicial. |
| Caso promedio | \(\Theta(\log_2(n))\) | \(\Theta(\log_2(n))\) | Con posiciones equiprobables del objetivo, se realizan varias divisiones del intervalo a la mitad. |
| Peor caso | \(O(\log_2(n))\) | \(O(\log_2(n))\) | El objetivo se encuentra en uno de los niveles más profundos o está ausente y se agota el intervalo. |

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
