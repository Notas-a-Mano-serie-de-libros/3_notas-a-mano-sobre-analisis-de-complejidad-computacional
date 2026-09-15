# Ordenamiento Shell

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 8</span>

El ordenamiento Shell generaliza la idea del ordenamiento por inserción. En lugar de comparar solo elementos contiguos, primero compara elementos separados por un valor h determinado. Después reduce progresivamente ese valor h hasta llegar a 1, momento en el que realiza una pasada equivalente a inserción sobre un arreglo que ya quedó parcialmente organizado.

La ventaja práctica aparece porque los elementos pueden desplazarse grandes distancias durante las primeras pasadas. Cuando h se vuelve pequeño, el arreglo suele estar mucho más cerca de su posición final y las pasadas restantes requieren menos movimientos.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/4_ordenamiento_shell.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Análisis de complejidad

### Resumen general

Shell ordena mediante inserciones entre elementos separados por saltos decrecientes. El tiempo depende de la secuencia de saltos y del orden de los datos; el espacio auxiliar permanece constante.

### Versión iterativa

La tabla corresponde a la secuencia original de Shell: \(\lfloor n/2\rfloor\), \(\lfloor n/4\rfloor\), hasta \(1\). Otras secuencias pueden modificar las cotas temporales.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Theta(n\cdot\log_2(n))\) | \(\Theta(1)\) | El arreglo ya está ordenado y cada pasada verifica los elementos sin desplazarlos. |
| Caso promedio | Depende de la distribución de los datos | \(\Theta(1)\) | Las pasadas realizan distintos números de desplazamientos según el orden inicial; no se presupone una única cota ajustada. |
| Peor caso | \(O(n^2)\) | \(O(1)\) | Un orden desfavorable requiere numerosos desplazamientos con la secuencia original de saltos. |

## Comparación de secuencias de h

La siguiente animación ejecuta Shell sort en paralelo sobre el mismo arreglo usando las secuencias Shell, Hibbard, Sedgewick y Pratt. La columna **Pasos** permite comparar cuántas operaciones visibles necesita cada técnica para completar el ordenamiento bajo las mismas condiciones iniciales.

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
