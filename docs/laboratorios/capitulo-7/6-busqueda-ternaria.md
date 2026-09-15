# Búsqueda ternaria

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 7</span>

La búsqueda ternaria divide el espacio de búsqueda en tres partes iguales calculando dos puntos medios. Compara el objetivo con cada punto medio para descartar un tercio del arreglo en cada iteración. Requiere que el arreglo esté ordenado.

Aunque cada iteración descarta más que la búsqueda binaria (un tercio en vez de la mitad), necesita dos comparaciones por paso, por lo que en la práctica es ligeramente menos eficiente que la búsqueda binaria. En el análisis espacial se toma como referencia la formulación recursiva, donde la pila de llamadas crece con la profundidad de las divisiones.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/6_busqueda_ternaria.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Análisis de complejidad

### Resumen general

La búsqueda ternaria requiere un arreglo ordenado, compara dos posiciones y conserva uno de los tres subintervalos. Su tiempo es logarítmico; la versión iterativa conserva espacio constante y la recursiva utiliza una pila de profundidad logarítmica.

### Versión iterativa

En la implementación iterativa, cada paso calcula \(m_1\) y \(m_2\), compara el objetivo con esos puntos y conserva solo el tercio que puede contenerlo. El espacio auxiliar se mantiene constante porque los límites se actualizan en el mismo marco de ejecución.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(1)\) | \(\Theta(1)\) | El objetivo coincide con una de las dos posiciones examinadas en el intervalo inicial. |
| Caso promedio | \(\Theta(\log_3(n))\) | \(\Theta(1)\) | Con posiciones equiprobables del objetivo, se desciende por varios subintervalos. |
| Peor caso | \(O(\log_3(n))\) | \(O(1)\) | El objetivo está en un nivel profundo o está ausente y se agotan las divisiones del intervalo. |

### Versión recursiva

En la implementación recursiva, cada partición del arreglo genera una llamada sobre un tercio del intervalo anterior. La profundidad de esa cadena de llamadas es proporcional a \(\log_3(n)\).

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(1)\) | \(\Omega(1)\) | El objetivo coincide con una de las dos posiciones examinadas en el intervalo inicial. |
| Caso promedio | \(\Theta(\log_3(n))\) | \(\Theta(\log_3(n))\) | Con posiciones equiprobables del objetivo, se desciende por varios subintervalos. |
| Peor caso | \(O(\log_3(n))\) | \(O(\log_3(n))\) | El objetivo está en un nivel profundo o está ausente y se agotan las divisiones del intervalo. |

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
