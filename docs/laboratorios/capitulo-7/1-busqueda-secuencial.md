# Búsqueda secuencial

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 7</span>

La búsqueda secuencial (o lineal) recorre el arreglo posición por posición, comparando cada elemento con el objetivo. No requiere que el arreglo esté ordenado; basta con acceder a los elementos en cualquier orden. Si el arreglo está ordenado, la búsqueda puede detenerse anticipadamente al encontrar un elemento mayor que el objetivo, aunque esto no mejora el peor caso.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/1_busqueda_secuencial.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Análisis de complejidad

### Resumen general

La búsqueda secuencial revisa los elementos en orden. El tiempo depende de la posición del objetivo; el espacio auxiliar es constante en la versión iterativa y crece con las llamadas pendientes en la recursiva.

### Versión iterativa

En la implementación iterativa, el algoritmo mantiene únicamente el índice de avance y algunas variables auxiliares constantes. El número de comparaciones depende de la posición del objetivo dentro del arreglo.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(1)\) | \(\Theta(1)\) | El objetivo está en la primera posición. |
| Caso promedio | \(\Theta(n)\) | \(\Theta(1)\) | El objetivo está presente y sus posiciones posibles son equiprobables; se revisa aproximadamente la mitad del arreglo. |
| Peor caso | \(O(n)\) | \(O(1)\) | El objetivo está en la última posición o está ausente; se recorre todo el arreglo. |

### Versión recursiva

Si el recorrido se expresa mediante llamadas recursivas, cada llamada representa la comparación de una posición. La cantidad de comparaciones se conserva, pero cada llamada queda registrada temporalmente en la pila de ejecución hasta que se alcanza el caso base.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(1)\) | \(\Omega(1)\) | El objetivo está en la primera posición. |
| Caso promedio | \(\Theta(n)\) | \(\Theta(n)\) | El objetivo está presente y sus posiciones posibles son equiprobables; se revisa aproximadamente la mitad del arreglo. |
| Peor caso | \(O(n)\) | \(O(n)\) | El objetivo está en la última posición o está ausente; se recorre todo el arreglo. |

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
