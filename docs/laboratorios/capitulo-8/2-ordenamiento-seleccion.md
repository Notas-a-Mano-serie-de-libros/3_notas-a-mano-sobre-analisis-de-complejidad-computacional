# Ordenamiento por selección

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 8</span>

El ordenamiento por selección busca el elemento mínimo en el subarreglo no ordenado y lo coloca al inicio de ese subarreglo, expandiendo la parte ordenada en una posición con cada pasada. Siempre realiza el mismo número de comparaciones independientemente del orden inicial.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/2_ordenamiento_seleccion.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Análisis de complejidad

### Resumen general

El ordenamiento por selección examina el subarreglo pendiente para localizar sus extremos. Las variantes del libro mantienen un tiempo cuadrático independientemente del orden inicial y utilizan espacio auxiliar constante.

### Versión iterativa

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(n^2)\) | \(\Omega(1)\) | El arreglo ya está ordenado; aun así se examinan los subarreglos completos. |
| Caso promedio | \(\Theta(n^2)\) | \(\Theta(1)\) | Los valores están en un orden aleatorio y cada pasada busca los extremos del subarreglo pendiente. |
| Peor caso | \(O(n^2)\) | \(O(1)\) | El orden inicial es desfavorable; la búsqueda de extremos sigue requiriendo un número cuadrático de comparaciones. |

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
