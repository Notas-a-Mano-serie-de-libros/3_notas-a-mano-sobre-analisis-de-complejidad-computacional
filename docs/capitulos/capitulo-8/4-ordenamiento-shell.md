<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# Ampliación · Ordenamiento Shell

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/4_ordenamiento_shell.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ordenamiento Shell generaliza la idea del ordenamiento por inserción. En lugar de comparar solo elementos contiguos, primero compara elementos separados por un valor h determinado. Después reduce progresivamente ese valor h hasta llegar a 1, momento en el que realiza una pasada equivalente a inserción sobre un arreglo que ya quedó parcialmente organizado.

La ventaja práctica aparece porque los elementos pueden desplazarse grandes distancias durante las primeras pasadas. Cuando h se vuelve pequeño, el arreglo suele estar mucho más cerca de su posición final y las pasadas restantes requieren menos movimientos.

### Implementación

=== "Pseudocódigo"

    ```text
    salto ← ⌊n/2⌋
    mientras salto > 0
        aplicar inserción entre elementos separados por salto
        salto ← ⌊salto/2⌋
    ```

=== "Python"

    ```python
    gap = len(a)//2
    while gap:
        for i in range(gap, len(a)):
            v, j = a[i], i
            while j >= gap and a[j-gap] > v: a[j] = a[j-gap]; j -= gap
            a[j] = v
        gap //= 2
    ```

=== "Java"

    ```java
    for(int g=a.length/2;g>0;g/=2)for(int i=g;i<a.length;i++){int v=a[i],j=i;while(j>=g&&a[j-g]>v){a[j]=a[j-g];j-=g;}a[j]=v;}
    ```

=== "C"

    ```c
    for(int g=n/2;g>0;g/=2)for(int i=g;i<n;i++){int v=a[i],j=i;while(j>=g&&a[j-g]>v){a[j]=a[j-g];j-=g;}a[j]=v;}
    ```

### Complejidad

<div style="display:flex; justify-content:center; margin:1.2em 0;">
<table style="margin: 0 auto; text-align: center;">
  <thead>
    <tr>
      <th>Secuencia de h</th>
      <th>Mejor caso</th>
      <th>Caso promedio</th>
      <th>Peor caso</th>
      <th>Espacio</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Shell: n/2, n/4, ..., 1</td><td>\(\Omega(n \log_2(n))\)</td><td>Depende de los datos</td><td>\(O(n^2)\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Hibbard: \(2^k - 1\)</td><td>\(\Omega(n \log_2(n))\)</td><td>Depende de los datos</td><td>\(O(n^{3/2})\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Sedgewick</td><td>\(\Omega(n \log_2(n))\)</td><td>Depende de los datos</td><td>Aproximadamente \(O(n^{4/3})\)</td><td>\(O(1)\)</td></tr>
    <tr><td>Pratt: \(2^i3^j\)</td><td>\(\Omega(n \log_2(n))\)</td><td>Depende de los datos</td><td>\(O(n\log_2^2(n))\)</td><td>\(O(1)\)</td></tr>
  </tbody>
</table>
</div>

Shell sort no tiene una única complejidad temporal fija, porque el número de comparaciones y movimientos depende directamente de la secuencia de h. Con la secuencia original propuesta por Shell, el peor caso sigue siendo cuadrático. Con secuencias mejor diseñadas, como Hibbard, Sedgewick o Pratt, el comportamiento mejora de forma importante.

La complejidad espacial se mantiene constante, ya que el algoritmo opera directamente sobre el arreglo original y solo necesita variables auxiliares para el valor actual de \(h\), los índices y el intercambio de valores.


---

### Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo, la vista, el orden y la secuencia de h.
3. Use `Paso siguiente` para avanzar una comparación o intercambio a la vez.
4. Use `Ejecución automática` para observar toda la ejecución.
5. Cambie el campo `h` para comparar cómo se modifica el recorrido interno del algoritmo.

### Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento Shell sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios usando la secuencia original de Shell.

- **Línea sólida** — simulación empírica sobre varios tamaños de arreglo.
- **Línea discontinua** — extrapolación analítica para observar la tendencia cuando el tamaño crece.
- **Checkbox** — superpone una referencia cuadrática normalizada para la secuencia original.

La comparación experimental debe interpretarse como una referencia para la secuencia seleccionada en la implementación. El análisis formal cambia cuando se modifica la secuencia de h, por eso el resumen anterior separa Shell, Hibbard, Sedgewick y Pratt.

#### Tabla de resultados

La tabla muestra, para cada tamaño de arreglo \(n\) evaluado:

- **Operaciones teóricas** y **Tiempo teórico**: calculados con la función de referencia usada para la curva superpuesta.
- **Operaciones obtenidas** y **Tiempo experimental**: valores medidos por la simulación.
- **Error absoluto** y **Error relativo**: diferencia entre la referencia teórica escalada y los resultados obtenidos.

### Comparación de secuencias de h

La siguiente animación ejecuta Shell sort en paralelo sobre el mismo arreglo usando las secuencias Shell, Hibbard, Sedgewick y Pratt. La columna **Pasos** permite comparar cuántas operaciones visibles necesita cada técnica para completar el ordenamiento bajo las mismas condiciones iniciales.

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../3-ordenamiento-insercion/">← 8.4 Ordenamiento por inserción</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../5-ordenamiento-mezcla/">8.5 Ordenamiento por mezcla →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
