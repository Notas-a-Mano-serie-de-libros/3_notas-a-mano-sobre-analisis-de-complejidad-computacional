# Consideraciones teóricas previas

<span class="chapter-kicker">Páginas 25–35</span>

Esta sección reúne la simbología y las herramientas matemáticas que la obra utiliza en los capítulos posteriores. Sirve como referencia de consulta; no pretende sustituir un texto especializado de lógica, cálculo, probabilidad o análisis matemático.

## Simbología utilizada en la obra

### Conjuntos numéricos

| Símbolo | Significado |
| --- | --- |
| \(\mathbb{N}\) | Números naturales, incluido el cero. |
| \(\mathbb{Z}\) | Números enteros. |
| \(\mathbb{R}\) | Números reales. |
| \(\mathbb{Z}^{+}\) | Enteros estrictamente positivos. |
| \(\mathbb{Z}^{+}_{0}\) | Enteros no negativos. |
| \(\mathbb{R}^{+}\) | Reales estrictamente positivos. |
| \(\mathbb{R}^{+}_{0}\) | Reales no negativos. |

La notación sigue la convención matemática utilizada por la obra a partir de ISO 80000-2:2019.

### Lógica, pertenencia e inclusión

| Símbolo | Lectura |
| --- | --- |
| \(\land\), \(\lor\) | Conjunción y disyunción. |
| \(a\in A\), \(a\notin A\) | Pertenencia y no pertenencia. |
| \(a\Rightarrow b\) | Implicación. |
| \(a\Leftrightarrow b\) | Equivalencia. |
| \(A\subset B\), \(A\subseteq B\) | Contenido propio e inclusión. |
| \(\exists\), \(\forall\) | Existe y para todo. |
| \(\mid\) o \(:\) | “Tal que”. |

Los intervalos \([a,b]\) incluyen sus extremos; los intervalos \((a,b)\) los excluyen. Las expresiones \(a\ll b\), \(a\gg b\) y \(n\to\infty\) describen comparación de magnitud y tendencia al infinito.

## Funciones

Una función asigna a cada elemento de un dominio exactamente un elemento de un codominio:

\[
f:A\to B,\qquad x\mapsto f(x)
\]

En análisis de algoritmos, una función modela los recursos consumidos según el tamaño de entrada.

La **función piso** redondea hacia el entero inferior y la **función techo** hacia el entero superior:

\[
\lfloor x\rfloor=\max\{n\in\mathbb{Z}\mid n\le x\},
\qquad
\lceil x\rceil=\min\{n\in\mathbb{Z}\mid n\ge x\}
\]

## Unidades, escala y variación

Una **unidad de medida** proporciona una referencia para interpretar una magnitud. Un **factor de escala** permite expresar la misma magnitud en unidades diferentes; por ejemplo, \(1\,[\mathrm{min}]=60\,[\mathrm{s}]\).

La **variación estocástica** describe fluctuaciones debidas a incertidumbre o factores no controlados. En una medición computacional puede proceder de procesos en segundo plano, planificación del sistema o gestión dinámica de memoria.

## Conceptos útiles para el capítulo 2

### Bytes decimales y binarios

| Sistema decimal | Cantidad | Sistema binario | Cantidad |
| --- | ---: | --- | ---: |
| KB | \(10^3\) bytes | KiB | \(2^{10}\) bytes |
| MB | \(10^6\) bytes | MiB | \(2^{20}\) bytes |
| GB | \(10^9\) bytes | GiB | \(2^{30}\) bytes |
| TB | \(10^{12}\) bytes | TiB | \(2^{40}\) bytes |
| PB | \(10^{15}\) bytes | PiB | \(2^{50}\) bytes |
| EB | \(10^{18}\) bytes | EiB | \(2^{60}\) bytes |
| ZB | \(10^{21}\) bytes | ZiB | \(2^{70}\) bytes |

La diferencia porcentual crece con la escala. Elegir el sistema equivocado puede distorsionar cálculos de almacenamiento, transferencia y consumo de memoria.

## Conceptos útiles para el capítulo 3

Cuando \(f(n)\) crece estrictamente más lento que \(g(n)\), la razón puede tender a cero:

\[
\lim_{n\to\infty}\frac{f(n)}{g(n)}=0
\]

Una función monótonamente creciente sin cota superior tiende a infinito. Para estudiar comportamientos que oscilan se utilizan el límite inferior y el límite superior:

\[
\liminf_{n\to\infty}f(n),
\qquad
\limsup_{n\to\infty}f(n)
\]

Cuando el comportamiento asintótico está bien definido, ambos coinciden con el límite total. Esta coincidencia no es una regla general para cualquier función.

## Conceptos útiles para los capítulos 4, 5 y 6

### Sumatorias

\[
\sum_{i=a}^{b}f(i)=f(a)+f(a+1)+\cdots+f(b)
\]

Propiedades y resultados utilizados con frecuencia:

\[
\sum_{i=a}^{b}(f(i)+g(i))=\sum_{i=a}^{b}f(i)+\sum_{i=a}^{b}g(i)
\]

\[
\sum_{i=1}^{n}i=\frac{n(n+1)}{2},
\qquad
\sum_{i=1}^{n}i^2=\frac{n(n+1)(2n+1)}{6}
\]

Para una serie geométrica con \(r\ne1\):

\[
\sum_{i=0}^{n}r^i=\frac{r^{n+1}-1}{r-1}
\]

### Logaritmos y potencias

\[
(a^m)^n=a^{mn},
\qquad
\log_a(n)=\frac{\log_b(n)}{\log_b(a)}
\]

\[
\log_b(mn)=\log_b(m)+\log_b(n),
\qquad
\log_b(n^k)=k\log_b(n)
\]

\[
b^{\log_b(n)}=n,
\qquad
a^{\log_b(n)}=n^{\log_b(a)}
\]

### Productorias

\[
\prod_{i=a}^{b}f(i)=f(a)\,f(a+1)\cdots f(b)
\]

## Conceptos útiles para los capítulos 7 y 8

El **valor esperado** representa el promedio ponderado de los valores posibles. Para observaciones equiprobables:

\[
\mathbb{E}[X]=\frac{1}{n}\sum_{i=1}^{n}f(i)
\]

El **error cuadrático medio** cuantifica la diferencia promedio entre valores observados \(y_i\) y predicciones \(\hat y_i\):

\[
\operatorname{MSE}=\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat y_i)^2
\]

Un MSE menor indica que el modelo se aproxima mejor a las observaciones, dentro de las condiciones del experimento.

---

[Continuar con el capítulo 1](capitulos/capitulo-1.md){ .md-button .md-button--primary }
[Consultar el glosario](glosario.md){ .md-button }
