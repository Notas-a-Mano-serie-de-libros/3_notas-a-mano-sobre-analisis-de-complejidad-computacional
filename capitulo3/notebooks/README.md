# Capítulo 3: Notación asintótica

> **Libro:** páginas 89–132 · **Pregunta guía:** ¿cómo describimos formalmente el crecimiento de una función cuando $n\to\infty$?

Este capítulo introduce las notaciones que permiten comparar funciones de complejidad mediante cotas superiores, inferiores, ajustadas y estrictas.

> [!IMPORTANT]
> **Complemento de lectura:** [consultar la síntesis del capítulo 3 en GitHub Pages](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-3/).

<a href="https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-3/"><img src="../../assets/qr/capitulo-3.png" width="132" alt="Código QR de la síntesis digital del capítulo 3"></a>

## Objetivos de aprendizaje

- Interpretar $O$, $\Omega$ y $\Theta$ como familias de funciones.
- Distinguir cotas superiores, inferiores y ajustadas.
- Comprender las relaciones estrictas $o$ y $\omega$.
- Determinar constantes y un punto $n_0$ que satisfagan cada definición.
- Justificar relaciones asintóticas mediante límites y desigualdades.

## Contenido de la obra

| Sección | Contenido |
| :---: | --- |
| 3.1 | Contexto histórico de la notación asintótica |
| 3.2 | Comportamiento asintótico general y jerarquía funcional |
| 3.3 | Familias de funciones y sus propiedades asintóticas |
| 3.4 | Notación asintótica simplificada |
| 3.5 | Notaciones $O$, $o$, $\Omega$, $\omega$ y $\Theta$; propiedades y estudio de complejidad |
| 3.6 | Ejercicios generales y verificaciones mediante límites |

## Recursos interactivos

| Sección | Recurso | Abrir |
| :---: | --- | :---: |
| 3.2 | Representación asintótica general | [Notebook](./notacion_asintotica_representacion_generica.ipynb) |
| 3.5.1 | Notación $O$ | [Notebook](./1_notacion_big_o.ipynb) |
| 3.5.2 | Notación $\Omega$ | [Notebook](./3_notacion_big_omega.ipynb) |
| 3.5.3 | Notación $\Theta$ | [Notebook](./5_notacion_theta.ipynb) |
| Adicional | Comparación de las cinco notaciones | [Notebook](./0_comparacion_notaciones_asintoticas.ipynb) |
| 3.5.1.2 | Notación $o$ | [Notebook](./2_notacion_little_o.ipynb) |
| 3.5.2.2 | Notación $\omega$ | [Notebook](./4_notacion_little_omega.ipynb) |
| 3.5.5 | Estudio de complejidad con ejemplos concretos | [Notebook](./ejemplos_concretos_notaciones.ipynb) |
| 3.6 | Ejercicios propuestos | [PDF](./ejercicios_propuestos.pdf) |

## Ruta recomendada

1. Identifica las funciones $C(n)$ y $g(n)$.
2. Escribe la desigualdad exigida por la notación.
3. Propón las constantes y el punto $n_0$.
4. Comprueba la relación en el notebook correspondiente.
5. Contrasta el resultado con el criterio del límite.

## Síntesis conceptual

El capítulo construye la notación asintótica en tres niveles: primero estudia el comportamiento límite de funciones polinómicas y exponenciales; luego define familias de funciones y sus relaciones; finalmente presenta una notación simplificada y las cinco familias usadas en complejidad.

| Notación | Lectura |
| :---: | --- |
| $O(g(n))$ | Cota superior asintótica |
| $\Omega(g(n))$ | Cota inferior asintótica |
| $\Theta(g(n))$ | Cota ajustada asintótica |
| $o(g(n))$ | Crecimiento estrictamente menor |
| $\omega(g(n))$ | Crecimiento estrictamente mayor |

Las relaciones se justifican mediante desigualdades, constantes, un umbral $n_0$ y criterios de límite. El capítulo también estudia reflexividad, antirreflexividad estricta, simetría, simetría transpuesta, transitividad, anidamiento y ausencia de tricotomía.

La notación adquiere significado computacional cuando se vincula con casos de análisis. Si dos entradas del mismo tamaño pueden producir costos diferentes, deben distinguirse mejor, peor y caso promedio; si el costo es uniforme, una cota ajustada $\Theta$ describe el comportamiento.

---

[← Capítulo 2](../../capitulo2/notebooks/README.md) · [Índice general](../../README.md) · [Capítulo 4 →](../../capitulo4/notebooks/README.md)
