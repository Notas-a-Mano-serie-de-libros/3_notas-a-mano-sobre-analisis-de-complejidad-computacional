# Laboratorio interactivo: complejidad experimental

Esta carpeta contiene los notebooks ejecutables de la sección experimental del Capítulo 2. La idea no es repetir la teoría del capítulo, sino usar cada notebook como una práctica corta para observar cómo una función de crecimiento se refleja en mediciones de tiempo, consumo de recursos o valores teóricos.

Para estudiar el contexto completo, vuelve a la [guía principal del Capítulo 2](../README.md).

## Cómo usar este laboratorio

1. Abre el notebook correspondiente, en local o en Colab.
2. Ejecuta primero la explicación y la gráfica teórica.
3. Revisa el código fuente del experimento antes de correr la simulación.
4. Ajusta los controles interactivos: máximo \(n\), número de ejecuciones o \(k\), según el notebook.
5. Ejecuta la simulación y compara la tabla con la figura final.

Cuando el notebook muestre una advertencia, úsala como señal de escala: no significa que el experimento esté mal, sino que la función elegida puede exigir demasiado tiempo o memoria.

## Qué se observa en las tablas

| Columna | Lectura recomendada |
|---|---|
| Cantidad de datos \(n\) | Tamaños de entrada evaluados hasta el máximo seleccionado. |
| Tiempo teórico [s] | Valor esperado según la función de crecimiento temporal. |
| Tiempo experimental [s] | Promedio medido durante las ejecuciones del experimento. |
| Recurso teórico [bytes] | Memoria estimada según la función espacial usada. |
| Recurso experimental [bytes] | Consumo observado durante la ejecución. |
| Operaciones | Valor teórico adimensional, usado en notebooks sin experimento empírico. |
| Estado | Indica si una fila está pendiente, en ejecución o completada. |

## Notebooks

| Tema | Local | Colab | Enfoque |
|---|---|---|---|
| Constante | [Abrir local](./1_complejidad_constante.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/1_complejidad_constante.ipynb) | Acceso directo y costo estable. |
| Logarítmica | [Abrir local](./2_complejidad_logaritmica.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/2_complejidad_logaritmica.ipynb) | Reducción progresiva del problema. |
| Lineal | [Abrir local](./3_complejidad_lineal.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/3_complejidad_lineal.ipynb) | Recorrido proporcional a \(n\). |
| Log-lineal | [Abrir local](./4_complejidad_log_lineal.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/4_complejidad_log_lineal.ipynb) | Crecimiento combinado \(n \log(n)\). |
| Cuadrática | [Abrir local](./5_complejidad_cuadratica.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/5_complejidad_cuadratica.ipynb) | Doble interacción entre elementos. |
| Cúbica | [Abrir local](./6_complejidad_cubica.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/6_complejidad_cubica.ipynb) | Triple interacción entre elementos. |
| Polinomial general | [Abrir local](./7_complejidad_polinomial_general.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/7_complejidad_polinomial_general.ipynb) | Familia \(n^k\) sin medición experimental. |
| Exponencial | [Abrir local](./8_complejidad_exponencial.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/8_complejidad_exponencial.ipynb) | Duplicación del trabajo al crecer \(n\). |
| Factorial | [Abrir local](./9_complejidad_factorial.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/9_complejidad_factorial.ipynb) | Permutaciones y explosión combinatoria. |

## Ruta de estudio sugerida

- Empieza con constante, logarítmica y lineal para comparar crecimientos suaves.
- Sigue con log-lineal, cuadrática, cúbica y polinomial general para observar cómo cambia la pendiente.
- Termina con exponencial y factorial, donde las advertencias de ejecución se vuelven parte del aprendizaje.

## Archivos de soporte

| Archivo | Propósito |
|---|---|
| [colab_bootstrap.py](./colab_bootstrap.py) | Prepara imports locales/remotos para que los notebooks funcionen dentro y fuera de Colab. |
| [complexity_animations.py](./complexity_animations.py) | Implementa la lógica compartida de las animaciones experimentales. |
| [constant_animation.py](./constant_animation.py) | Mantiene la simulación constante y su compatibilidad con notebooks anteriores. |
| [polynomial_animation.py](./polynomial_animation.py) | Implementa la simulación teórica de \(n^k\). |
| [theoretical_graphs.py](./theoretical_graphs.py) | Genera las gráficas teóricas usadas antes de las simulaciones. |

## Comandos LaTeX para Colab

```tex
% Complejidades experimentales - Capítulo 2
\newcommand{\colabComplejidadConstante}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/1_complejidad_constante.ipynb}
\newcommand{\colabComplejidadLogaritmica}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/2_complejidad_logaritmica.ipynb}
\newcommand{\colabComplejidadLineal}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/3_complejidad_lineal.ipynb}
\newcommand{\colabComplejidadLogLineal}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/4_complejidad_log_lineal.ipynb}
\newcommand{\colabComplejidadCuadratica}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/5_complejidad_cuadratica.ipynb}
\newcommand{\colabComplejidadCubica}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/6_complejidad_cubica.ipynb}
\newcommand{\colabComplejidadPolinomialGeneral}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/7_complejidad_polinomial_general.ipynb}
\newcommand{\colabComplejidadExponencial}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/8_complejidad_exponencial.ipynb}
\newcommand{\colabComplejidadFactorial}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/9_complejidad_factorial.ipynb}
```

## Licencia

Este material se distribuye bajo la licencia Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).

© 2025 Carlos Eduardo Orozco
