# Comparación de algoritmos de búsqueda

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 7</span>

Este notebook muestra una animación general para comparar varios algoritmos de búsqueda sobre el mismo arreglo y el mismo elemento objetivo. La intención es observar, en una sola vista, cómo cambia el número de pasos y qué posiciones del arreglo revisa cada estrategia.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/0_comparacion_busquedas.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

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
    <tr><td>Búsqueda binaria</td><td>\(\Omega(1)\)</td><td>\(\Theta(\log_2(n))\)</td><td>\(O(\log_2(n))\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/2_busqueda_binaria.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda ternaria</td><td>\(\Omega(1)\)</td><td>\(\Theta(\log_2(n))\)</td><td>\(O(\log_2(n))\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/6_busqueda_ternaria.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda exponencial</td><td>\(\Omega(1)\)</td><td>\(\Theta(\log_2(n))\)</td><td>\(O(\log_2(n))\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/5_busqueda_exponencial.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda por interpolación</td><td>\(\Omega(1)\)</td><td>\(\Theta(\log_2(\log_2(n)))\)</td><td>\(O(n)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/3_busqueda_interpolacion.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda por saltos</td><td>\(\Omega(1)\)</td><td>\(\Theta(\sqrt n)\)</td><td>\(O(\sqrt n)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/4_busqueda_saltos.ipynb" title="Abrir animación">🔗</a></td></tr>
    <tr><td>Búsqueda secuencial</td><td>\(\Omega(1)\)</td><td>\(\Theta(n)\)</td><td>\(O(n)\)</td><td style="text-align:center;"><a target="_blank" rel="noopener noreferrer" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo7/notebooks/1_busqueda_secuencial.ipynb" title="Abrir animación">🔗</a></td></tr>
  </tbody>
</table>
</div>

<br>

Este resumen presenta los resultados generales. El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede consultar en los recursos complementarios que proporciona la obra.


---

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
