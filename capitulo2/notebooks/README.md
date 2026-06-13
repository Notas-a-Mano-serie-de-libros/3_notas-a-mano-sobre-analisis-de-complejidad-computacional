# Capítulo 2: Fundamentos del análisis de algoritmos

> **Libro:** páginas 59–88 · **Pregunta guía:** ¿cómo cambia el costo de un algoritmo cuando crece el tamaño de la entrada?

Este capítulo presenta las funciones de complejidad temporal y espacial. Los notebooks permiten reconocer sus formas de crecimiento y contrastar modelos teóricos con mediciones experimentales.

> [!IMPORTANT]
> **Complemento de lectura:** [consultar la síntesis del capítulo 2 en GitHub Pages](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-2/).

<a href="https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-2/"><img src="../../assets/qr/capitulo-2.png" width="132" alt="Código QR de la síntesis digital del capítulo 2"></a>

## Objetivos de aprendizaje

- Interpretar el tamaño de entrada $n$ y las funciones $T(n)$ y $S(n)$.
- Distinguir complejidad temporal y espacial.
- Reconocer crecimientos constantes, logarítmicos, polinomiales, exponenciales y factoriales.
- Comparar órdenes de crecimiento y sus límites prácticos.
- Diferenciar una medición experimental de una proyección teórica.

## Contenido de la obra

| Sección | Contenido |
| :---: | --- |
| 2.1 | Función de complejidad y propiedades básicas |
| 2.1.2 | Funciones de complejidad teóricas comunes |
| 2.1.3 | Análisis teórico temporal y espacial |
| 2.1.4 | Análisis práctico de complejidad temporal |
| 2.1.5–2.1.6 | Errores comunes y consideraciones finales |
| 2.2 | Ejercicios propuestos |

## Recursos interactivos

| Sección | Recurso | Abrir |
| :---: | --- | :---: |
| 2.1.2 | Complejidad constante | [Notebook](./1_complejidad_constante.ipynb) |
| 2.1.2 | Complejidad logarítmica | [Notebook](./2_complejidad_logaritmica.ipynb) |
| 2.1.2 | Complejidad lineal | [Notebook](./3_complejidad_lineal.ipynb) |
| 2.1.2 | Complejidad log-lineal | [Notebook](./4_complejidad_log_lineal.ipynb) |
| 2.1.2 | Complejidad cuadrática | [Notebook](./5_complejidad_cuadratica.ipynb) |
| 2.1.2 | Complejidad cúbica | [Notebook](./6_complejidad_cubica.ipynb) |
| 2.1.2 | Complejidad polinomial general | [Notebook](./7_complejidad_polinomial_general.ipynb) |
| 2.1.2 | Complejidad exponencial | [Notebook](./8_complejidad_exponencial.ipynb) |
| 2.1.2 | Complejidad factorial | [Notebook](./9_complejidad_factorial.ipynb) |
| 2.1.3 | Comparación de complejidades | [Notebook](./graficas/comparacion_complejidades_teoricas.ipynb) |
| 2.1.4 | Alta complejidad temporal | [Notebook](./graficas/analisis_alta_complejidad_temporal.ipynb) |
| 2.1.4 | Alta complejidad espacial | [Notebook](./graficas/analisis_alta_complejidad_espacial.ipynb) |
| 2.2 | Ejercicios propuestos | [PDF](./ejercicios_propuestos.pdf) |

<details>
<summary><strong>Notebooks para reproducir las gráficas</strong></summary>

Las versiones independientes están en [`graficas/`](./graficas/): [constante](./graficas/1_complejidad_constante.ipynb), [logarítmica](./graficas/2_complejidad_logaritmica.ipynb), [lineal](./graficas/3_complejidad_lineal.ipynb), [log-lineal](./graficas/4_complejidad_log_lineal.ipynb), [cuadrática](./graficas/5_complejidad_cuadratica.ipynb), [cúbica](./graficas/6_complejidad_cubica.ipynb), [polinomial](./graficas/complejidad_polinomica.ipynb), [exponencial](./graficas/7_complejidad_exponencial.ipynb) y [factorial](./graficas/8_complejidad_factorial.ipynb).

</details>

## Ruta recomendada

1. Identifica qué representa $n$ en el problema.
2. Predice la forma de $T(n)$ y $S(n)$.
3. Ejecuta el notebook de la familia correspondiente.
4. Aumenta el tamaño de entrada y compara teoría y medición.
5. Explica cuándo el crecimiento deja de ser práctico.

## Síntesis conceptual

Una función de complejidad $C(n)$ modela un recurso en función del tamaño de entrada $n$. La obra restringe su dominio a tamaños válidos, exige costos no negativos y estudia funciones monótonas no decrecientes capaces de representar el comportamiento cuando $n$ crece.

| Perspectiva | Qué se analiza |
| --- | --- |
| Complejidad temporal | Cantidad de operaciones y tiempo teórico $t=T_0\,T(n)$ |
| Complejidad espacial | Recursos de almacenamiento y consumo teórico $s=S_0\,S(n)$ |
| Análisis práctico | Mediciones temporales bajo un entorno concreto y comparación con la tendencia teórica |

Las familias estudiadas son constante, logarítmica, lineal, log-lineal, polinómica, cuadrática, cúbica, exponencial y factorial. Para exponentes fijos y tamaños suficientemente grandes, su jerarquía típica es:

```math
1 < \log n < n < n\log n < n^2 < n^3 < n^k < 2^n < n!
```

La obra advierte que no se debe subestimar el tiempo, ignorar el espacio, olvidar los efectos del entorno, asumir que una medición representa todos los casos ni privilegiar evidencia empírica aislada sobre el análisis formal.

---

[Índice general](../../README.md) · [Capítulo 3 →](../../capitulo3/notebooks/README.md)
