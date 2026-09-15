# Ordenamiento radix

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 8</span>

El ordenamiento radix organiza enteros no negativos procesando sus dígitos de menor a mayor peso. En cada pasada distribuye los elementos en buckets según el dígito actual y luego reconstruye el arreglo conservando el orden relativo dentro de cada bucket.

La versión implementada aquí usa radix LSD en base 10. Su comportamiento depende de la cantidad de elementos `n`, de la cantidad de dígitos `d` del valor máximo y de la base `k` utilizada para los buckets.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/7_ordenamiento_radix.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Análisis de complejidad

### Resumen general

El ordenamiento radix procesa los dígitos de enteros no negativos. Con \(d\) dígitos y base \(k\), cada pasada recorre el arreglo y los conteos: el costo es \(\Theta(d \cdot (n+k))\), independientemente del orden inicial.

### Versión iterativa

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(d \cdot (n+k))\) | \(\Omega(n+k)\) | Para un número fijo de dígitos, incluso un arreglo ya ordenado requiere todas las pasadas. |
| Caso promedio | \(\Theta(d \cdot (n+k))\) | \(\Theta(n+k)\) | Los enteros no negativos están en orden aleatorio y se procesan todos sus dígitos. |
| Peor caso | \(O(d \cdot (n+k))\) | \(O(n+k)\) | Con el mismo número de dígitos, un orden desfavorable no evita ni agrega pasadas: se procesan igualmente todos los elementos. |

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
