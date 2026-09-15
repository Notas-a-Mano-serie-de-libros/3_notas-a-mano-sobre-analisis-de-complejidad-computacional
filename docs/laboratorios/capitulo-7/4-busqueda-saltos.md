# Búsqueda por saltos

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 7</span>

La búsqueda por saltos avanza en bloques de tamaño \(\sqrt{n}\) hasta encontrar un elemento mayor que el objetivo o alcanzar el final del arreglo. Luego realiza una búsqueda secuencial hacia atrás dentro del bloque acotado. Requiere que el arreglo esté ordenado.

El bloque óptimo de tamaño \(\sqrt{n}\) balancea los saltos hacia adelante con la búsqueda secuencial hacia atrás, produciendo una complejidad de \(O(\sqrt{n})\).

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/4_busqueda_saltos.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Análisis de complejidad

### Resumen general

La búsqueda por saltos combina avances de bloque con un recorrido secuencial del bloque seleccionado. Con un salto de \(\lfloor\sqrt{n}\rfloor\), ambas fases tienen costo del orden de \(\sqrt{n}\).

### Versión iterativa

En la implementación iterativa, el tamaño del salto se elige como \(\lfloor\sqrt{n}\rfloor\). Así se equilibran las comparaciones de bloques y las comparaciones secuenciales del bloque final.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(1)\) | \(\Theta(1)\) | El objetivo está al inicio del primer bloque y se encuentra en la primera comparación de la fase lineal. |
| Caso promedio | \(\Theta(\sqrt{n})\) | \(\Theta(1)\) | Con posiciones equiprobables del objetivo, se recorren varios bloques y parte del bloque final. |
| Peor caso | \(O(\sqrt{n})\) | \(O(1)\) | Se recorren casi todos los bloques y casi todo el bloque seleccionado antes de encontrar el objetivo o confirmar su ausencia. |

### Versión recursiva

Si el recorrido se expresa mediante llamadas recursivas, la estructura de fases se mantiene, pero cada salto o avance lineal puede quedar como una llamada pendiente. La pila crece con la cantidad de comparaciones realizadas antes de terminar.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(1)\) | \(\Omega(1)\) | El objetivo está al inicio del primer bloque y se encuentra en la primera comparación de la fase lineal. |
| Caso promedio | \(\Theta(\sqrt{n})\) | \(\Theta(\sqrt{n})\) | Con posiciones equiprobables del objetivo, se recorren varios bloques y parte del bloque final. |
| Peor caso | \(O(\sqrt{n})\) | \(O(\sqrt{n})\) | Se recorren casi todos los bloques y casi todo el bloque seleccionado antes de encontrar el objetivo o confirmar su ausencia. |

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
