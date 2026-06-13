# Guía comparativa de búsquedas

Esta guía concentra los seis métodos estudiados en el capítulo 7. Las complejidades describen el comportamiento asintótico; la elección práctica también depende del orden, la distribución y el soporte de acceso de los datos.

## Secuencial

Recorre los elementos hasta encontrar el objetivo o agotar la colección. Funciona sin orden previo y cuesta \(O(1)\) en el mejor caso y \(O(n)\) en el promedio y el peor.

[Cuaderno](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/1_busqueda_secuencial.ipynb) · [Abrir en Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/1_busqueda_secuencial.ipynb)

## Binaria

Descarta la mitad del intervalo en cada paso. Requiere datos ordenados y ofrece \(O(\log n)\) en el promedio y el peor caso.

[Cuaderno](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/2_busqueda_binaria.ipynb) · [Abrir en Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/2_busqueda_binaria.ipynb)

## Interpolación

Estima la posición del objetivo según su valor. Sobre claves ordenadas y aproximadamente uniformes puede lograr un promedio de \(O(\log\log n)\); una distribución desfavorable lo lleva a \(O(n)\).

[Cuaderno](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/3_busqueda_interpolacion.ipynb) · [Abrir en Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/3_busqueda_interpolacion.ipynb)

## Por saltos

Avanza por bloques y realiza una búsqueda lineal dentro del bloque candidato. Con saltos de tamaño cercano a \(\sqrt n\), su costo es \(O(\sqrt n)\).

[Cuaderno](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/4_busqueda_saltos.ipynb) · [Abrir en Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/4_busqueda_saltos.ipynb)

## Exponencial

Duplica el límite de búsqueda hasta acotar el objetivo y luego aplica búsqueda binaria. Es útil cuando se desconoce el tamaño efectivo del rango y conserva \(O(\log n)\).

[Cuaderno](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/5_busqueda_exponencial.ipynb) · [Abrir en Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/5_busqueda_exponencial.ipynb)

## Ternaria

Divide el intervalo ordenado en tres regiones. Reduce el problema de forma logarítmica, aunque no implica automáticamente una mejora práctica frente a la búsqueda binaria.

[Cuaderno](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/6_busqueda_ternaria.ipynb) · [Abrir en Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/6_busqueda_ternaria.ipynb)

## Práctica integrada

[Comparar todos los algoritmos](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/0_comparacion_busquedas.ipynb){ .md-button .md-button--primary }
[Resolver los ejercicios](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo7/notebooks/ejercicios_propuestos.ipynb){ .md-button }
