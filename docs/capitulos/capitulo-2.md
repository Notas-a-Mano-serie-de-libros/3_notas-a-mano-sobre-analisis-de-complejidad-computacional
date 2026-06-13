<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Inicio</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-3/">Capítulo 3 →</a></nav>

# Capítulo 2 · Fundamentos del análisis de algoritmos

**Páginas 59–88.** El capítulo define las funciones de complejidad y conecta el análisis teórico de tiempo y espacio con el comportamiento observado en una ejecución real.

## Estructura conceptual

| Sección | Desarrollo |
| :---: | --- |
| 2.1.1 | Dominio natural, no negatividad, crecimiento monótono y representación asintótica. |
| 2.1.2 | Funciones constante, logarítmica, lineal, log-lineal, polinómica, cuadrática, cúbica, exponencial y factorial. |
| 2.1.3 | Cálculo teórico del tiempo y los recursos de almacenamiento. |
| 2.1.4 | Medición práctica de complejidad temporal para las familias estudiadas. |
| 2.1.5 | Errores comunes al interpretar teoría, hardware y experimentos. |
| 2.2 | Ejercicios de estimación con restricciones de tiempo y memoria. |

Una función \(C(n)\) expresa el costo en función del tamaño de entrada. La obra utiliza los modelos \(t=T_0T(n)\) y \(s=S_0S(n)\) para relacionar el orden teórico con unidades físicas.

## Laboratorios

Los nueve notebooks principales permiten modificar el tamaño de entrada y observar cada familia. El comparador reúne las curvas y los análisis de alta complejidad muestran cuándo tiempo o memoria dejan de ser viables.

[Ver todos los recursos](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/tree/main/capitulo2/notebooks){ .md-button .md-button--primary }
[Abrir comparación en Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/graficas/comparacion_complejidades_teoricas.ipynb){ .md-button }

!!! warning "Lectura correcta"
    Una medición depende del hardware, el sistema operativo y la carga del entorno. Sirve para contrastar el modelo, no para reemplazar el análisis formal.

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Inicio</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-3/">Capítulo 3 →</a></nav>
