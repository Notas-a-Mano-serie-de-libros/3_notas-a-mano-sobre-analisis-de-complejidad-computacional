# Análisis de eficiencia

Esta carpeta reúne los notebooks que llevan las funciones de crecimiento a escalas extremas. Su propósito es complementar el [Capítulo 2](../README.md), no volver a explicar toda la teoría: aquí la pregunta central es cuándo el tiempo o la memoria dejan de ser razonables.

## Uso recomendado

1. Ejecuta primero el análisis temporal.
2. Ejecuta después el análisis espacial.
3. Observa los cambios de unidad en las tablas y gráficas: segundos, años, bytes o escalas mayores.
4. Usa estos notebooks como cierre después de estudiar las simulaciones experimentales.

## Notebooks

| Análisis | Local | Colab | Qué observar |
|---|---|---|---|
| Temporal | [Abrir local](./complejidad_temporal/analisis_alta_complejidad.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_eficiencia/complejidad_temporal/analisis_alta_complejidad.ipynb) | Cuándo \(2^n\) y \(n!\) superan escalas temporales útiles. |
| Espacial | [Abrir local](./complejidad_espacial/analisis_alta_complejidad.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_eficiencia/complejidad_espacial/analisis_alta_complejidad.ipynb) | Cuándo \(2^n\) y \(n!\) exceden capacidades de almacenamiento. |

## Figuras de referencia

| Figura | Archivo | Lectura |
|---|---|---|
| Crecimiento temporal exponencial | [Ver imagen](../../images/capitulo2/analisis_eficiencia/complejidad_temporal/complejidad_exponencial_1.png) | Comparación entre \(2^n\) y escalas de tiempo grandes. |
| Crecimiento temporal factorial | [Ver imagen](../../images/capitulo2/analisis_eficiencia/complejidad_temporal/complejidad_factorial_1.png) | Incremento de \(n!\) frente a límites temporales prácticos. |
| Crecimiento espacial exponencial | [Ver imagen](../../images/capitulo2/analisis_eficiencia/complejidad_espacial/complejidad_exponencial_1.png) | Memoria requerida por \(2^n\). |
| Crecimiento espacial factorial | [Ver imagen](../../images/capitulo2/analisis_eficiencia/complejidad_espacial/complejidad_factorial_1.png) | Memoria requerida por \(n!\). |

## Relación con las simulaciones experimentales

Antes de usar estos notebooks conviene pasar por el [laboratorio interactivo de complejidad experimental](../analisis_complejidad_temporal_experimental/README.md). Allí se ve el crecimiento desde entradas pequeñas y controladas; aquí se extiende la mirada hacia límites de viabilidad.

## Preguntas de estudio

- ¿Qué cambia primero: el tiempo disponible o la memoria disponible?
- ¿En qué punto deja de tener sentido ejecutar y conviene razonar solo con el modelo?
- ¿Qué información aporta el cambio de unidades frente al valor numérico bruto?

## Licencia

Este material se distribuye bajo la licencia Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).

© 2025 Carlos Eduardo Orozco
