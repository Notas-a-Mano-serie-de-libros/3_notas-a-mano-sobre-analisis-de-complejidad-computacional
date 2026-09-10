<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>

# 8.7 Ordenamiento radix

<span class="chapter-kicker">Capítulo 8</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/7_ordenamiento_radix.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

El ordenamiento radix organiza enteros no negativos procesando sus dígitos de menor a mayor peso. En cada pasada distribuye los elementos en buckets según el dígito actual y luego reconstruye el arreglo conservando el orden relativo dentro de cada bucket.

La versión implementada aquí usa radix LSD en base 10. Su comportamiento depende de la cantidad de elementos `n`, de la cantidad de dígitos `d` del valor máximo y de la base `k` utilizada para los buckets.

### Implementación

=== "Pseudocódigo"

    ```text
    exp ← 1
    mientras máximo(A)/exp > 0
        ordenar establemente por el dígito exp
        exp ← 10·exp
    ```

=== "Python"

    ```python
    exp, maximum = 1, max(a, default=0)
    while maximum // exp:
        counting_digit(a, exp)
        exp *= 10
    ```

=== "Java"

    ```java
    int max=java.util.Arrays.stream(a).max().orElse(0);for(int exp=1;max/exp>0;exp*=10)countingDigit(a,exp);
    ```

=== "C"

    ```c
    int max=maximo(a,n);for(int exp=1;max/exp>0;exp*=10)countingDigit(a,n,exp);
    ```

### Complejidad

<div style="display:flex; justify-content:center; margin:1.2em 0;">
<table style="margin: 0 auto; text-align: center;">
  <thead>
    <tr>
      <th>Escenario</th>
      <th><i>T</i>(<i>n</i>)</th>
      <th><i>S</i>(<i>n</i>)</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Mejor caso</td><td>\(\Omega(d(n+k))\)</td><td>\(\Omega(n+k)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(\Theta(d(n+k))\)</td><td>\(\Theta(n+k)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(d(n+k))\)</td><td>\(O(n+k)\)</td></tr>
  </tbody>
</table>
</div>

En esta animación la base es fija, `k = 10`, por lo que el crecimiento se observa principalmente a través del número de elementos y la cantidad de dígitos procesados.


---

### Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento radix sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios de enteros no negativos.

- **Línea sólida** — simulación empírica.
- **Línea discontinua** — extrapolación analítica.
- **Checkbox** — superpone la función teórica asociada a \(d(n+k)\).

La gráfica usa el mismo formato de los análisis experimentales del capítulo 2 para mantener consistencia visual con el resto de la obra.

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../6-ordenamiento-rapido/">← 8.6 Ordenamiento rápido</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../ejercicios-propuestos/">8.9 Ejercicios propuestos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
