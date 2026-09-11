# Guía comparativa de ordenamientos

Esta guía acompaña el capítulo 8. Además del crecimiento temporal, conviene considerar la memoria auxiliar, la estabilidad y la forma inicial de los datos.

## Burbuja

Intercambia pares adyacentes fuera de orden. La versión base es cuadrática; con detección de ausencia de intercambios, el mejor caso es \(O(n)\). Es estable y trabaja *in-place*.

[Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/1_ordenamiento_burbuja.ipynb){ target="_blank" rel="noopener noreferrer" }

## Selección

Selecciona repetidamente el mínimo restante. Realiza \(O(n^2)\) comparaciones en todos los casos, usa \(O(1)\) espacio auxiliar y reduce el número de intercambios.

[Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/2_ordenamiento_seleccion.ipynb){ target="_blank" rel="noopener noreferrer" }

## Inserción

Inserta cada elemento en la zona ya ordenada. Es lineal cuando la entrada ya está ordenada y cuadrático en promedio y en el peor caso; resulta natural para colecciones pequeñas o casi ordenadas.

[Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/3_ordenamiento_insercion.ipynb){ target="_blank" rel="noopener noreferrer" }

## Mezcla

Divide la colección, ordena recursivamente las partes y las combina. Mantiene \(O(n \cdot \log(n))\) en todos los casos y requiere \(O(n)\) memoria auxiliar en su implementación habitual.

[Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/5_ordenamiento_mezcla.ipynb){ target="_blank" rel="noopener noreferrer" }

## Rápido

Particiona alrededor de un pivote. Su promedio es \(O(n \cdot \log(n))\), pero particiones muy desequilibradas producen \(O(n^2)\); la selección del pivote es decisiva.

[Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/6_ordenamiento_rapido.ipynb){ target="_blank" rel="noopener noreferrer" }

## Radix

Ordena por dígitos o posiciones sin comparar directamente todos los pares. Su costo se expresa como \(\Theta(d \cdot (n+b))\), donde \(d\) es el número de dígitos y \(b\) la base empleada.

[Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/7_ordenamiento_radix.ipynb){ target="_blank" rel="noopener noreferrer" }

## Ampliación: Shell sort

El repositorio añade una práctica sobre Shell sort. Se ofrece como extensión experimental del capítulo, no como parte del conjunto central de seis algoritmos desarrollado en la obra.

[Abrir ampliación](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/4_ordenamiento_shell.ipynb){ target="_blank" rel="noopener noreferrer" }

## Práctica integrada

[Comparar todos los algoritmos](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/0_comparacion_ordenamientos.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }
[Resolver los ejercicios](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo8/notebooks/ejercicios_propuestos.ipynb){ .md-button  target="_blank" rel="noopener noreferrer" }