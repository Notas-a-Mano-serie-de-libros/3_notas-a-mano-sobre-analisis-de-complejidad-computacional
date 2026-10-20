<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>

# 5.5.3 Árbol de recurrencia

<span class="chapter-kicker">Capítulo 5</span>

Un **árbol de recurrencia** representa cada llamada como un nodo y cada subproblema como una rama. La complejidad se obtiene calculando el costo de un nivel y sumando las contribuciones de todos los niveles hasta alcanzar el caso base.

## Procedimiento

1. Determine el número y el tamaño de los hijos de cada llamada.
2. Calcule el costo individual de un nodo en el nivel \(i\).
3. Multiplique ese costo por la cantidad de nodos del nivel.
4. Determine la altura mediante el caso base.
5. Sume los costos de los nodos internos y de las hojas, e identifique el término dominante.

Use este método para visualizar y sumar los costos de árboles uniformes. En relaciones mixtas, contabilice por separado las ramas que alcanzan el caso base a diferentes alturas.

## Ejemplo desarrollado

Considere la misma recurrencia estudiada mediante sustitución:

\[
C(n)=
\begin{cases}
1 & \text{si } n=1,\\
2 \cdot C(n/2)+n & \text{si } n>1.
\end{cases}
\]

En el nivel cero existe un problema de tamaño \(n\), cuyo trabajo externo es \(n\). En el nivel uno aparecen dos problemas de tamaño \(n/2\); en el nivel dos, cuatro problemas de tamaño \(n/4\).

| Nivel \(i\) | Cantidad de nodos | Tamaño por nodo | Costo del nivel |
| ---: | ---: | ---: | ---: |
| \(0\) | \(1\) | \(n\) | \(n\) |
| \(1\) | \(2\) | \(n/2\) | \(2(n/2)=n\) |
| \(2\) | \(4\) | \(n/4\) | \(4(n/4)=n\) |
| \(i\) | \(2^i\) | \(n/2^i\) | \(2^i(n/2^i)=n\) |

El último nivel se alcanza cuando el tamaño de cada subproblema es uno:

\[
\frac{n}{2^h}=1
\quad\Longrightarrow\quad
h=\log_2(n).
\]

Cada nivel cuesta \(n\) y existen \(1+\log_2(n)\) niveles si se cuentan desde cero. Por tanto:

\[
\begin{aligned}
C(n)
&=\sum_{i=0}^{\log_2(n)}n\\
&=n\left(1+\log_2(n)\right)\\
&\in\mathcal{F}\!\left(n \cdot \log_2(n)\right).
\end{aligned}
\]

La tabla cumple la función del dibujo: hace explícitas la cantidad de nodos, el tamaño de cada subproblema y la contribución completa de cada nivel. Además, puede leerse y navegarse sin depender exclusivamente de una figura.

## Cómo interpretar el resultado

El método muestra **dónde se acumula el trabajo**. En este ejemplo todos los niveles internos aportan el mismo orden. En otras recurrencias, el costo puede concentrarse en la raíz, repartirse uniformemente o crecer hacia las hojas. Esa distribución permite anticipar qué término dominará la suma.

## Errores frecuentes

- Sumar el costo de un solo nodo en lugar del costo de todo el nivel.
- Olvidar el costo de las hojas.
- Confundir la cantidad de niveles con la cantidad de nodos.
- Suponer que todas las ramas tienen la misma altura en una recurrencia no uniforme.
- Inferir mejor, peor o promedio sin conocer el significado algorítmico de \(C(n)\).

## Compruebe su comprensión

1. Construya la tabla de niveles para \(C(n)=C(n/2)+1\).
2. ¿Cuál es el costo del nivel \(i\) en \(C(n)=4 \cdot C(n/2)+n^2\)?
3. Explique qué parte del procedimiento deja de ser uniforme en \(C(n)=C(n/2)+C(n/3)+n\).

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../sustitucion-iterativa/">← 5.5.2 Sustitución iterativa</a><a class="section-step__index" href="../">Capítulo 5</a><a class="section-step__next" href="../teorema-maestro/">5.5.4 Teorema maestro →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>
