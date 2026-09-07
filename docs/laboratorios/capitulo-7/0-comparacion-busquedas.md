# Comparación de algoritmos de búsqueda

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 7</span>

Este notebook muestra una animación general para comparar varios algoritmos de búsqueda sobre el mismo arreglo y el mismo elemento objetivo. La intención es observar, en una sola vista, cómo cambia el número de pasos y qué posiciones del arreglo revisa cada estrategia.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/0_comparacion_busquedas.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

## Algoritmos incluidos

<div style="text-align: center;">
<table style="margin: 0 auto; text-align: center;">
  <thead>
    <tr>
      <th>Algoritmo</th>
      <th>Mejor caso</th>
      <th>Caso promedio</th>
      <th>Peor caso</th>
      <th>Animación</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>Búsqueda binaria</td><td>\(\Omega(1)\)</td><td>\(\Theta(\log_2(n))\)</td><td>\(O(\log_2(n))\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/2_busqueda_binaria.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda ternaria</td><td>\(\Omega(1)\)</td><td>\(\Theta(\log_2(n))\)</td><td>\(O(\log_2(n))\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/6_busqueda_ternaria.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda exponencial</td><td>\(\Omega(1)\)</td><td>\(\Theta(\log_2(n))\)</td><td>\(O(\log_2(n))\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/5_busqueda_exponencial.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda por interpolación</td><td>\(\Omega(1)\)</td><td>\(\Theta(\log_2(\log_2(n)))\)</td><td>\(O(n)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/3_busqueda_interpolacion.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda por saltos</td><td>\(\Omega(1)\)</td><td>\(\Theta(\sqrt n)\)</td><td>\(O(\sqrt n)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/4_busqueda_saltos.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda secuencial</td><td>\(\Omega(1)\)</td><td>\(\Theta(n)\)</td><td>\(O(n)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/1_busqueda_secuencial.ipynb" title="Abrir animación">🔗</a></td></tr>
  </tbody>
</table>
</div>

<br>

Este resumen presenta los resultados generales. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.


---

## Uso

1. Ejecute la celda de simulación.
2. Defina el tamaño del arreglo.
3. Seleccione si el elemento objetivo debe existir o estar fuera del arreglo.
4. Use el botón `Buscar` para ejecutar todos los algoritmos activos sobre el mismo arreglo.
5. Revise la columna `Pasos` para comparar cuántas acciones necesitó cada algoritmo.

## Recomendación de ejecución local

GitHubColab permite abrir y ejecutar la simulación rápidamente desde el navegador, aunque tiene límites de sesión, rendimiento, persistencia de archivos, estabilidad de widgets interactivos y tiempo disponible de ejecución. Para trabajar con mayor estabilidad, modificar el código, guardar resultados o repetir experimentos largos, se recomienda descargar el proyecto y ejecutarlo en local desde el repositorio.

## Eficiencia por tamaño de arreglo

La siguiente celda simula cada algoritmo sobre arreglos de tamaño creciente y mide el **número de operaciones** que cada uno necesita para encontrar el objetivo (siempre presente en el arreglo). El análisis se enfoca exclusivamente en el conteo de operaciones del algoritmo, no en tiempos de ejecución reales.

- **Línea sólida** — simulación empírica (n ≤ 5 000, 50 ensayos por tamaño)
- **Línea punteada** — extrapolación analítica hasta n = 10 000 000
- **Checkbox** — superpone las funciones teóricas normalizadas para comparar la forma de cada curva con los datos experimentales
- **Algoritmos activos** — permite mostrar u ocultar algoritmos individuales para facilitar la comparación

El gráfico usa escala logarítmica en ambos ejes, lo que hace visibles las diferencias entre O(log(log(n))), O(log(n)), O(√n) y O(n).

> **Tiempo de ejecución:** la celda puede demorar varios minutos porque ejecuta 6 algoritmos sobre 50 tamaños distintos con 50 ensayos cada uno. En Colab el tiempo es mayor debido a las limitaciones del entorno. Para obtener resultados más rápidos y una ejecución más estable, se recomienda correr esta celda en local.
