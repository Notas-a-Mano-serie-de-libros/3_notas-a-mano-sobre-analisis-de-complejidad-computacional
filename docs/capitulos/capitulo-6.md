<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-7/">Capítulo 7 →</a></nav>

# Capítulo 6 · Análisis de algoritmos recursivos

<span class="chapter-kicker">Páginas 223–258</span>

Este capítulo traslada las herramientas de recurrencia al análisis de programas recursivos. El objetivo no es reconocer una fórmula de memoria, sino reconstruir el costo a partir del código y distinguir el tiempo de ejecución del espacio ocupado por la pila.

## Método de análisis

1. Identificar el caso base y el caso recursivo.
2. Establecer cómo cambia el tamaño de la entrada en cada llamada.
3. Formular la relación de recurrencia que representa el tiempo o el espacio.
4. Resolverla y expresar el resultado con el orden asintótico correspondiente.

En términos generales, el costo temporal reúne el trabajo local de cada llamada y el costo de las llamadas recursivas:

\[
T(n)=\sum T(n_i)+f(n)
\]

El costo espacial exige observar, además, la profundidad máxima de la pila:

\[
S(n)=S(\text{llamada activa})+\text{memoria local}
\]

## Casos estudiados

El recorrido incluye factorial, Fibonacci, potencia, ordenamiento por mezcla y operaciones sobre árboles binarios de búsqueda. Estos ejemplos permiten contrastar recursión lineal, ramificada y por división del problema.

!!! note "La diferencia que importa"
    Dos algoritmos pueden resolver el mismo problema mediante recursión y, aun así, generar árboles de llamadas radicalmente distintos. Fibonacci ingenuo repite subproblemas; *merge sort* divide la entrada y combina resultados con una estructura regular.

## Laboratorios

[Abrir laboratorio del capítulo](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb){ .md-button .md-button--primary }
[Ver archivos del capítulo](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/tree/main/capitulo6/notebooks){ .md-button }

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-7/">Capítulo 7 →</a></nav>
