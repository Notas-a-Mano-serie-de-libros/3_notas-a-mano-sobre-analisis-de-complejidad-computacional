<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# 8.9 Ejercicios propuestos

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/ejercicios_propuestos.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

Los enunciados de esta sección se conservan en el documento PDF del capítulo. Ábrelo para consultar la formulación completa, las condiciones y la numeración original.

<div class="lab-action">
<a class="md-button md-button--primary pdf-button" href="../../../assets/pdfs/capitulo-8-ejercicios-propuestos.pdf" target="_blank" rel="noopener noreferrer"><span aria-hidden="true">PDF</span> Consultar ejercicios propuestos</a>
<small class="lab-action__note">El documento se abrirá en una pestaña nueva.</small>
</div>

Este laboratorio desarrolla los ejercicios propuestos 1 y 2 mediante una simulación configurable. Permite escoger el algoritmo, el tipo de complejidad, el máximo \(n\), la cantidad de puntos y la distribución que representa el caso de ejecución. La tabla separa mediciones de proyecciones y la gráfica muestra una única curva resultante. Para \(n>10^6\) se utiliza proyección teórica; los algoritmos costosos proyectan desde un límite práctico menor.

### Ejercicios opcionales

Se desarrollan los ejercicios opcionales 2, 3 y 4. El ejercicio opcional 1 no se incluye, como se solicitó.


---

### Opcional 2: aplicaciones reales

- **Burbuja:** enseñanza, listas muy pequeñas y detección simple de entradas ya ordenadas; rara vez se usa en producción.
- **Selección:** entornos donde las escrituras son costosas, porque realiza pocas permutaciones aunque compare \(\Theta(n^2)\) veces.
- **Inserción:** arreglos pequeños, datos casi ordenados y subarreglos finales de algoritmos híbridos como Timsort e Introsort.
- **Shell Sort:** sistemas con memoria limitada que requieren ordenamiento in situ y un rendimiento práctico mejor que inserción sin usar memoria auxiliar lineal.
- **Merge Sort:** ordenamiento externo de archivos, listas enlazadas, procesamiento paralelo y escenarios que requieren estabilidad.
- **Quick Sort:** arreglos en memoria y bibliotecas de propósito general cuando interesan localidad de caché y buen tiempo promedio.
- **Radix Sort:** claves enteras, códigos, direcciones y cadenas de longitud acotada cuando sus dígitos pueden procesarse directamente.

### Opcional 3: algoritmos avanzados

#### Heap Sort

Construye un montículo máximo y extrae repetidamente su raíz. Garantiza \(\Theta(n\log(n))\) en los tres casos, usa \(\Theta(1)\) espacio auxiliar en su versión in situ y no es estable.

#### Counting Sort

Cuenta cuántas veces aparece cada clave del intervalo \([0,k]\) y reconstruye la salida. Su tiempo es \(\Theta(n+k)\) y su espacio auxiliar \(\Theta(n+k)\) en la versión estable. Es apropiado cuando \(k\) no es mucho mayor que \(n\).

#### Radix Sort

Ordena por dígitos usando un algoritmo estable en cada pasada. Con \(d\) dígitos y base \(k\), su tiempo es \(\Theta(d(n+k))\) y su espacio auxiliar usual es \(\Theta(n+k)\). No depende de comparaciones entre pares de elementos.

#### Tim Sort

Detecta subsecuencias ya ordenadas y las combina, aprovechando la estructura existente en datos reales. Su peor caso es \(\Theta(n\log(n))\), su mejor caso puede ser \(\Theta(n)\) y es estable.

### Opcional 4: impacto de la distribución inicial

- **Arreglo ordenado:** burbuja optimizada e inserción se aproximan a \(\Theta(n)\); selección permanece en \(\Theta(n^2)\). Merge Sort y Heap Sort conservan \(\Theta(n\log(n))\). Quick Sort puede degradarse a \(\Theta(n^2)\) si escoge siempre un extremo como pivote.
- **Orden inverso:** inserción y burbuja realizan el máximo número de desplazamientos o intercambios, ambos \(\Theta(n^2)\). Selección mantiene el mismo número de comparaciones. Merge Sort conserva su orden log-lineal.
- **Distribución aleatoria:** inserción, burbuja y selección presentan comportamiento cuadrático promedio; Quick Sort con pivote razonable alcanza \(\Theta(n\log(n))\) esperado.
- **Muchos duplicados:** Quick Sort mejora con partición de tres vías; una partición binaria deficiente puede quedar desbalanceada. Counting Sort y Radix Sort aprovechan claves de dominio acotado.
- **Datos casi ordenados:** inserción y Tim Sort suelen ser especialmente eficientes porque el número de inversiones o de subsecuencias naturales es pequeño.

El selector **Caso de ejecución** del laboratorio materializa estas diferencias con arreglos ordenados, aleatorios e inversos y permite contrastarlas con la función analítica de cada algoritmo.

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../7-ordenamiento-radix/">← 8.7 Ordenamiento radix</a><a class="section-step__index" href="../">Capítulo 8</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
