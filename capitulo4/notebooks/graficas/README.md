# Notebooks para generar las gráficas del capítulo 4

Esta carpeta separa los generadores de gráficas estáticas de las simulaciones
interactivas ubicadas en el directorio superior.

Cada notebook mide el algoritmo correspondiente, ajusta la función teórica y
genera las imágenes temporal y espacial. Las imágenes se guardan en
`capitulo4/images/generadas/referencias/` mediante
`capitulo4/runtime/util.py`.

El archivo `ejemplo9_(fibonacci_iterativo)_graficas.ipynb` utiliza enteros de
32 bits para conservar el comportamiento del algoritmo analizado: tiempo
lineal y espacio adicional constante.
