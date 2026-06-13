# Capítulo 5: Relaciones de recurrencia

> **Libro:** páginas 179–222 · **Pregunta guía:** ¿cómo obtenemos el costo de un algoritmo a partir de sus subproblemas recursivos?

Este capítulo estudia la formulación y solución de recurrencias. Los laboratorios hacen visibles las expansiones, los niveles del árbol y las condiciones de aplicación de cada método.

> [!IMPORTANT]
> **Complemento de lectura:** [consultar la síntesis del capítulo 5 en GitHub Pages](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-5/).

<a href="https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-5/"><img src="../../assets/qr/capitulo-5.png" width="132" alt="Código QR de la síntesis digital del capítulo 5"></a>

## Objetivos de aprendizaje

- Formular una recurrencia a partir de un algoritmo recursivo.
- Separar el costo recursivo del trabajo externo $f(n)$.
- Interpretar nodos, niveles, altura y costo total de un árbol de recurrencia.
- Aplicar sustitución, árboles, teoremas maestros y ecuaciones características.
- Distinguir una solución exacta de una clasificación asintótica.

## Contenido de la obra

| Sección | Contenido |
| :---: | --- |
| 5.1 | Sucesiones numéricas, tipos, convergencia y divergencia |
| 5.2 | Relaciones de recurrencia y definición formal |
| 5.3 | Relaciones lineales, no lineales, homogéneas y de coeficientes variables |
| 5.4 | Recurrencias aplicadas al análisis de complejidad |
| 5.5 | Sustitución iterativa, árbol de recurrencia, teorema maestro básico, extendido y generalizado, y ecuación característica |
| 5.6 | Consideraciones finales y ejercicios propuestos |

## Recursos interactivos

| Sección | Recurso | Abrir |
| :---: | --- | :---: |
| 5.5.3 | Árboles de recurrencia | [Notebook](./0_arboles_recursion.ipynb) |
| 5.5.2–5.5.5 | Métodos de solución | [Notebook](./1_metodos_solucion_relaciones_recurrencia.ipynb) |
| 5.6.1 | Ejercicios propuestos | [PDF](./ejercicios_propuestos.pdf) |

Los constructores configurables son material adicional: permiten modificar coeficientes, factores, costos externos y casos base más allá de los ejemplos impresos.

## Ruta recomendada

1. Identifica el caso base.
2. Determina cuántos subproblemas se generan y cómo cambia su tamaño.
3. Separa el costo externo $f(n)$.
4. Clasifica la recurrencia como reducción, división o combinación.
5. Predice la altura y el costo por nivel.
6. Selecciona un método compatible y verifica sus condiciones.
7. Contrasta la expresión obtenida con el resultado asintótico.

## Síntesis conceptual

El capítulo comienza con sucesiones numéricas y sus propiedades de convergencia o divergencia. Luego define formalmente las relaciones de recurrencia y las clasifica antes de aplicarlas al análisis algorítmico.

### Clasificaciones estudiadas

| Criterio | Formas |
| --- | --- |
| Linealidad | Lineales y no lineales |
| Término independiente | Homogéneas y no homogéneas |
| Coeficientes | Constantes o variables en función de $n$ |
| Transformación del tamaño | Reducción y división, con uno o varios términos recursivos |

Toda recurrencia debe distinguir el caso base del caso recursivo:

```math
C(n)=
\begin{cases}
c(n), & n \leq n_0, \\
C_{\mathrm{rec}}(n)+f(n), & n>n_0.
\end{cases}
```

Para una reducción simple, el tamaño disminuye en una cantidad fija $b$:

```math
C(n)=a\,C(n-b)+f(n).
```

Para una división simple, el tamaño se multiplica por un factor $b$ entre cero y uno:

```math
C(n)=a\,C(bn)+f(n), \qquad 0<b<1.
```

La obra también contempla varios términos recursivos. La forma general de reducción es:

```math
C(n)=\sum_{i=1}^{m} a_i\,C(n-b_i)+f(n).
```

La forma general de división es:

```math
C(n)=\sum_{i=1}^{m} a_i\,C(b_i n)+f(n),
\qquad 0<b_i<1.
```

Aquí, $m$ es la cantidad de términos recursivos, $a_i$ indica cuántas veces aparece cada subproblema, $b_i$ determina cómo se reduce su tamaño y $f(n)$ representa el trabajo externo. Los árboles resultantes pueden ser uniformes o desbalanceados y no todas las recurrencias encajan en un teorema maestro.

### Métodos de solución

| Método | Qué aporta | Cuándo resulta apropiado |
| --- | --- | --- |
| Sustitución iterativa | Expande la recurrencia hasta reconocer un patrón. | Para obtener intuición y una forma cerrada manejable. |
| Árbol de recurrencia | Distribuye y acumula el costo por niveles. | Cuando interesa visualizar subproblemas, altura y costo total. |
| Teorema maestro básico | Compara el trabajo recursivo con un término polinómico. | Recurrencias de división que satisfacen su forma canónica. |
| Teorema maestro extendido | Incorpora factores polinómicos y logarítmicos. | Cuando $f(n)$ incluye potencias de $n$ y logaritmos. |
| Teorema maestro generalizado | Resuelve divisiones con factores distintos mediante Akra–Bazzi. | Árboles no uniformes con varios tamaños de subproblema. |
| Ecuación característica | Produce una solución exacta homogénea y particular. | Recurrencias lineales con coeficientes constantes. |

La elección del método depende de la estructura. El caso base, el costo externo $f(n)$ y el significado computacional de la solución son partes necesarias del análisis.

---

[← Capítulo 4](../../capitulo4/notebooks/README.md) · [Índice general](../../README.md) · [Capítulo 6 →](../../capitulo6/notebooks/README.md)
