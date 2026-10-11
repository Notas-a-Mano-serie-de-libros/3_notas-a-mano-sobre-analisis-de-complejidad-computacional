# Visualización de la fórmula de interpolación

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 7</span>

La interpolación lineal es una técnica para estimar el valor \(y\) que corresponde a un punto \(x\) dentro de un intervalo \([x_0, x_1]\), conociendo únicamente los valores de la función en sus extremos: \((x_0,\,y_0)\) y \((x_1,\,y_1)\).

El principio es geométrico: se traza una línea recta entre ambos puntos de referencia y se evalúa esa recta en \(x\). La fórmula que expresa esta idea es:

\[
y = y_0 + \frac{(y_1 - y_0) \cdot (x - x_0)}{x_1 - x_0}
\]

El cociente \(\dfrac{x - x_0}{x_1 - x_0}\) mide la posición relativa de \(x\) dentro del intervalo: vale \(0\) cuando \(x = x_0\) y vale \(1\) cuando \(x = x_1\). En cualquier punto intermedio, representa la fracción del recorrido horizontal ya completado.

Multiplicar esa fracción por \((y_1 - y_0)\) escala el cambio vertical total del intervalo según cuánto avanzó \(x\) desde \(x_0\). Sumar \(y_0\) al resultado desplaza el cálculo para que parta desde el primer punto de referencia.

El valor obtenido es el punto sobre la recta que une \((x_0, y_0)\) con \((x_1, y_1)\), no necesariamente el valor real de la función en \(x\). La diferencia entre ambos constituye el **error de aproximación**, y depende de la curvatura de la función y de qué tan separados se encuentren los extremos del intervalo.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/3_busqueda_interpolacion.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Simulación interactiva

La siguiente simulación permite explorar visualmente cómo se comporta la fórmula sobre diferentes funciones.

La **curva azul** es la función real \(f(x)\) evaluada sobre el dominio \([0, n]\). La **línea roja discontinua** es la recta de interpolación: la secante que une los puntos \((x_0, y_0)\) y \((x_1, y_1)\), que actúan como extremos del intervalo de estimación. El **punto rojo** sobre esa recta es el valor estimado \(y\) para el \(x\) seleccionado; el **punto verde** es el valor real \(f(x)\).

La **barra naranja** vertical entre ambos puntos representa el error de la aproximación. Cuando la función es lineal, la recta de interpolación coincide exactamente con la curva y el error es nulo. A medida que la función presenta mayor curvatura, o a medida que el intervalo \([x_0, x_1]\) se amplía, el error crece.

Los controles permiten cambiar la función \(f(x)\), ajustar el dominio total mediante \(n\) —lo que reposiciona automáticamente los extremos a \((0,\,f(0))\) y \((n,\,f(n))\)—, mover los extremos del intervalo con los deslizadores \(x_0\) y \(x_1\), y seleccionar el punto de consulta \(x\) con el deslizador central o arrastrando directamente sobre la gráfica.


---

## Búsqueda por interpolación

La búsqueda por interpolación estima la posición del objetivo usando interpolación lineal: en vez de ir siempre al centro, salta a una posición proporcional al valor buscado. Requiere que el arreglo esté ordenado.

Para distribuciones uniformes alcanza \(O(\log(\log(n)))\) en el caso promedio, lo que la hace sublogarítmica. Sin embargo, si la distribución no es uniforme el peor caso es \(O(n)\).

## Análisis de complejidad

### Resumen general

La búsqueda por interpolación requiere un arreglo ordenado y estima la posición usando los valores de sus extremos. Con datos aproximadamente uniformes, el tiempo promedio es doblemente logarítmico; una distribución adversa puede llevar a un recorrido lineal.

### Versión iterativa

En la implementación iterativa, la estimación usa los valores de los extremos para saltar a una posición proporcional al objetivo. El caso promedio doblemente logarítmico depende de una distribución aproximadamente uniforme.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(1)\) | \(\Theta(1)\) | La primera estimación coincide con el objetivo, o una comprobación inicial resuelve la búsqueda. |
| Caso promedio | \(\Theta(\log_2(\log_2(n)))\) | \(\Theta(1)\) | Los valores tienen distribución aproximadamente uniforme y las estimaciones quedan cerca de la posición del objetivo. |
| Peor caso | \(O(n)\) | \(O(1)\) | Una distribución muy desigual hace que las estimaciones avancen pocas posiciones en cada paso. |

### Versión recursiva

Si el recorrido se expresa mediante llamadas recursivas, cada llamada calcula una posición estimada y continúa sobre el subrango que aún puede contener el objetivo. La memoria adicional queda determinada por la cantidad de estimaciones encadenadas.

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(1)\) | \(\Omega(1)\) | La primera estimación coincide con el objetivo, o una comprobación inicial resuelve la búsqueda. |
| Caso promedio | \(\Theta(\log_2(\log_2(n)))\) | \(\Theta(\log_2(\log_2(n)))\) | Los valores tienen distribución aproximadamente uniforme y las estimaciones quedan cerca de la posición del objetivo. |
| Peor caso | \(O(n)\) | \(O(n)\) | Una distribución muy desigual hace que las estimaciones avancen pocas posiciones en cada paso. |

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
