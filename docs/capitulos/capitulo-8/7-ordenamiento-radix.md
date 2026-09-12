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

<!-- book-code:start -->

Listado original del libro, página 363 (Java).

```java
public void ordenar(int[] arr) {
    // Obtiene el elemento más grande del arreglo
    int max = Arrays.stream(arr).max().getAsInt();
    // Obtiene la cantidad de dígitos (iteraciones)
    int d = (int) Math.floor(Math.log10(max)) + 1;
    for (int i = 1; i <= d; i++)
        ordenarPorDigito(arr, i);
}
public void ordenarPorDigito(int[] arr, int i) {
    int n = arr.length;
    int exp = (int) Math.pow(10, i - 1);
    // Arreglo que representa los buckets (b=10)
    int[] conteo = new int[10];
    // Arreglo parcialmente ordenado
    int[] salida = new int[n];
    // Paso 1: Cuenta elementos por bucket
    for (int valor : arr)
        conteo[(valor / exp) % 10]++;
    // Paso 2: Calcula la suma acumulada
    for (int j = 1; j < 10; j++)
        conteo[j] += conteo[j - 1];
    // Paso 3: Inserta los elementos en la nueva posición
    for (int j = n - 1; j >= 0; j--) {
        int d = (arr[j] / exp) % 10;
        salida[conteo[d] - 1] = arr[j];
        conteo[d]--;
    }
    // Actualiza el arreglo original con el nuevo orden
    System.arraycopy(salida, 0, arr, 0, n);
}
```

<!-- book-code:end -->

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
    <tr><td>Mejor caso</td><td>\(\Omega(d \cdot (n+k))\)</td><td>\(\Omega(n+k)\)</td></tr>
    <tr><td>Caso promedio</td><td>\(\Theta(d \cdot (n+k))\)</td><td>\(\Theta(n+k)\)</td></tr>
    <tr><td>Peor caso</td><td>\(O(d \cdot (n+k))\)</td><td>\(O(n+k)\)</td></tr>
  </tbody>
</table>
</div>

En esta animación la base es fija, `k = 10`, por lo que el crecimiento se observa principalmente a través del número de elementos y la cantidad de dígitos procesados.


---

### Eficiencia por tamaño de arreglo

La siguiente celda simula el ordenamiento radix sobre arreglos de tamaño creciente y mide el **número de operaciones** sobre arreglos aleatorios de enteros no negativos.

- **Línea sólida** — simulación empírica.
- **Línea discontinua** — extrapolación analítica.
- **Checkbox** — superpone la función teórica asociada a \(d \cdot (n+k)\).

La gráfica usa el mismo formato de los análisis experimentales del capítulo 2 para mantener consistencia visual con el resto de la obra.

<div class="related-links"><strong>Para comparar</strong> <a href="../0-comparacion-ordenamientos/">ver la comparación general de todos los algoritmos</a>.</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../6-ordenamiento-rapido/">← 8.6 Ordenamiento rápido</a><a class="section-step__index" href="../">Capítulo 8</a><a class="section-step__next" href="../ejercicios-propuestos/">8.9 Ejercicios propuestos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-7/">← Capítulo 7</a><a class="chapter-nav__index" href="../">Capítulo 8</a><a class="chapter-nav__next" href="../../">Recorrido →</a></nav>
