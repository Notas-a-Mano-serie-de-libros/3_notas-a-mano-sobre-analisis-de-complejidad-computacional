# Ordenamiento rápido

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 8</span>

El ordenamiento rápido (quicksort) elige un elemento pivote y reorganiza el arreglo para que todos los elementos menores queden a su izquierda y los mayores a su derecha. Luego ordena recursivamente cada partición.

La partición puede realizarse mediante distintos esquemas. **Hoare** usa dos índices que avanzan desde extremos opuestos e intercambia pares ubicados en el lado incorrecto. **Lomuto** recorre el subarreglo en una dirección, mantiene el límite de los elementos que deben quedar antes del pivote y coloca el pivote en su posición definitiva al finalizar la pasada. La selección del pivote también puede variar: inicio, medio, fin, aleatorio, mediana de tres y mediana de medianas. La mediana de tres toma los valores ubicados al inicio, al centro y al final del subarreglo, y usa como pivote el valor central entre esos tres. La mediana de medianas divide el subarreglo en grupos pequeños, calcula la mediana de cada grupo y luego usa la mediana de esas medianas como pivote.

En el caso promedio logra \(O(n \cdot \log(n))\) con una constante menor que el ordenamiento por mezcla, lo que lo hace el algoritmo de propósito general más rápido en la práctica. El peor caso es \(O(n^2)\) y ocurre cuando el pivote divide el arreglo de forma muy asimétrica.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo8/notebooks/6_ordenamiento_rapido.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Análisis de complejidad

### Resumen general

El ordenamiento rápido particiona alrededor de un pivote. El equilibrio de las particiones determina tanto el tiempo como la profundidad de la pila: particiones equilibradas producen crecimiento logarítmico en profundidad y particiones muy desiguales pueden generar profundidad lineal.

### Versión recursiva

| Caso | \(T(n)\) | \(S(n)\) | Cuándo ocurre |
| --- | --- | --- | --- |
| Mejor caso | \(\Omega(n \cdot \log_2(n))\) | \(\Omega(\log_2(n))\) | Las particiones dividen el arreglo en partes aproximadamente iguales en cada nivel. |
| Caso promedio | \(\Theta(n \cdot \log_2(n))\) | \(\Theta(\log_2(n))\) | Con valores aleatorios y pivotes representativos, las particiones son equilibradas en promedio. |
| Peor caso | \(O(n^2)\) | \(O(n)\) | El pivote produce repetidamente una partición vacía o muy pequeña y otra con casi todos los elementos. |

## Comparación entre Hoare y Lomuto

Ambos esquemas producen particiones válidas para quicksort, aunque recorren y modifican el arreglo de manera diferente. Hoare inicia con dos índices fuera del intervalo activo: \(i\) avanza desde la izquierda hasta encontrar un valor que pertenece al lado derecho y \(j\) retrocede desde la derecha hasta encontrar uno que pertenece al lado izquierdo. Mientras \(i<j\), ambos elementos se intercambian. Cuando los índices se cruzan, \(j\) define el límite entre las dos particiones.

Lomuto mueve primero el pivote al extremo final. El índice \(j\) examina cada elemento y el índice \(i\) conserva el límite de la región cuyos valores deben quedar antes del pivote. Cada valor que satisface la relación con el pivote se intercambia con el elemento situado en \(i\); al terminar el recorrido, el pivote se coloca en esa frontera.

La siguiente animación ejecuta ambos esquemas en paralelo sobre el mismo arreglo, con el pivote tomado de la posición media. La columna **Pasos** permite comparar la cantidad de estados visibles que requiere cada estrategia. Esta medición incluye comparaciones e intercambios mostrados por la animación y permite observar la diferencia operativa entre los recorridos.

## Comparación entre estrategias de pivote

La selección del pivote modifica la forma en que se dividen los subarreglos. Cuando el pivote queda cerca del centro de los valores, las particiones tienden a ser más equilibradas y el recorrido recursivo reduce su profundidad. Cuando el pivote queda cerca de un extremo, una partición puede concentrar casi todos los elementos y el número de pasos aumenta.

La siguiente animación permite elegir el esquema de partición y compara, sobre el mismo arreglo, las estrategias de pivote usadas por la simulación: inicio, medio, fin, aleatorio, mediana de tres y mediana de medianas. La columna **Pasos** muestra cuántos estados visibles requiere cada estrategia para completar el ordenamiento con la misma configuración de orden y partición.

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
