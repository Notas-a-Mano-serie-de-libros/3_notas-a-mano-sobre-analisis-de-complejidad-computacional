# Gráficas de referencia del capítulo 4

Los notebooks utilizados para medir, ajustar y generar las gráficas estáticas
se encuentran en `capitulo4/notebooks/graficas/`, separados de las simulaciones
interactivas.

Los notebooks visibles en `capitulo4/notebooks/` presentan cada ejemplo con el
formato experimental del capítulo 2: ejecutan el algoritmo para distintos
valores de \(n\), separan las mediciones temporales y espaciales y muestran sus
resultados mediante una gráfica y una tabla.

El módulo `capitulo4/runtime/util.py` aplica el formato matemático STIX a títulos,
ejes y leyendas, y guarda las imágenes resultantes en `capitulo4/images/generadas/referencias`.
