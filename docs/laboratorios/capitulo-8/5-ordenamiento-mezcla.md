# Ordenamiento por mezcla

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 8</span>

El ordenamiento por mezcla (merge sort) divide el arreglo a la mitad de forma recursiva hasta obtener subarreglos de un solo elemento, que por definición están ordenados. Luego combina (mezcla) los subarreglos en orden creciente hasta reconstruir el arreglo completo.

Garantiza \(O(n \cdot \log(n))\) en todos los casos, lo que lo hace predecible y eficiente, aunque requiere \(O(n)\) de memoria auxiliar para la fase de mezcla.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/5_ordenamiento_mezcla.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Análisis de complejidad

### Resumen general

El ordenamiento por mezcla divide el arreglo y combina los subarreglos ordenados. La estructura de división y mezcla garantiza tiempo \(\Theta(n \cdot \log_2(n))\) en los tres casos; los arreglos temporales dominan el espacio auxiliar.

### Versión recursiva

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(n \cdot \log_2(n))\) | \(\Omega(n)\) | El arreglo ya está ordenado; la implementación igualmente divide y mezcla todos los niveles. |
| Caso promedio | \(\Theta(n \cdot \log_2(n))\) | \(\Theta(n)\) | Los valores están en orden aleatorio y se ejecuta la misma estructura de divisiones y mezclas. |
| Peor caso | \(O(n \cdot \log_2(n))\) | \(O(n)\) | Los elementos obligan a recorrer extensamente ambas mitades durante las mezclas; el orden de crecimiento sigue siendo el mismo. |

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
