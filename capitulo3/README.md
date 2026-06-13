# Capítulo 3: Notación asintótica

La notación asintótica es un método matemático que permite analizar el comportamiento de una función cuando sus variables se aproximan a valores límite, típicamente el infinito. En análisis de algoritmos, este lenguaje permite caracterizar el crecimiento de una función de complejidad e identificar el término dominante que gobierna su tendencia.

En el Capítulo 2 estudiamos funciones como $1$, $\log_2(n)$, $n$, $n\log_2(n)$, $n^2$, $n^3$, $n^k$, $2^n$ y $n!$. En este capítulo damos el siguiente paso: aprendemos a comparar esas funciones mediante cotas, límites y familias de crecimiento.

La pregunta central es:

> ¿Cómo podemos describir formalmente el crecimiento de una función cuando $n\to\infty$?

La intención no es memorizar símbolos. La intención es aprender a leer relaciones de crecimiento: cuándo una función queda eventualmente por debajo de otra, cuándo queda por encima, cuándo la relación es estricta y cuándo ambas funciones tienen el mismo orden dominante.

---

## Cómo estudiar este capítulo con los notebooks

Este capítulo está pensado para leerse con el libro abierto y los notebooks ejecutándose al lado. Una buena forma de estudiarlo es seguir este ciclo:

1. Lee la definición de la notación.
2. Identifica la desigualdad que debe cumplirse.
3. Observa qué límite se usa para justificar la relación.
4. Abre el notebook correspondiente.
5. Ejecuta la simulación con el ejemplo base del libro.
6. Cambia $C(n)$ y $g(n)$.
7. Modifica $c$, o $c_1$ y $c_2$ en el caso de $\Theta$.
8. Observa desde qué punto aparece $n_0$.
9. Escribe con tus palabras si $C(n)$ pertenece o no pertenece a la familia seleccionada.

Los notebooks no reemplazan la demostración formal. Sirven para hacer visible la definición: muestran cómo una desigualdad empieza a cumplirse a partir de cierto punto y cómo el límite anticipa esa relación.

---

## Objetivos de aprendizaje

Al finalizar este capítulo deberías poder:

- interpretar la notación asintótica como una relación entre $C(n)$ y una función de referencia $g(n)$;
- distinguir entre cotas superiores, inferiores, estrictas y ajustadas;
- usar límites para decidir si una función pertenece a $O$, $o$, $\Omega$, $\omega$ o $\Theta$;
- explicar el papel de $c$, $c_1$, $c_2$ y $n_0$;
- reconocer cuándo una cota es válida pero poco ajustada;
- entender por qué los términos de menor orden desaparecen en el límite;
- diferenciar una relación de pertenencia asintótica de una igualdad algebraica exacta.

---

## Mapa del capítulo

| Sección | Tema | Pregunta guía |
|---|---|---|
| 3.1 | Contexto histórico | ¿De dónde viene la notación asintótica? |
| 3.2 | Comportamiento asintótico general | ¿Por qué el término dominante controla el crecimiento? |
| 3.3 | Familias de funciones | ¿Qué significa agrupar funciones por su comportamiento límite? |
| 3.4 | Notación asintótica simplificada | ¿Por qué suele escribirse $f(n)=O(g(n))$ aunque formalmente sea pertenencia? |
| 3.5 | Tipos de notación asintótica | ¿Qué diferencia hay entre $O$, $o$, $\Omega$, $\omega$ y $\Theta$? |
| 3.6 | Ejercicios | ¿Cómo se aplican las definiciones en casos concretos? |

---

## Notebooks interactivos

Usa estos notebooks en paralelo con el libro. En local, los enlaces abren los archivos del repositorio; en remoto, los enlaces de Colab abren la versión ejecutable correspondiente.

| Notación | Notebook local | Colab | Qué deberías observar |
|---|---|---|---|
| Comparación general | [Abrir local](./0_comparacion_notaciones_asintoticas.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/0_comparacion_notaciones_asintoticas.ipynb) | Cómo cambian la desigualdad, los límites, las constantes y el intervalo solución entre las cinco notaciones. |
| Big-$O$ | [Abrir local](./1_notacion_big_o.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/1_notacion_big_o.ipynb) | Cuándo $C(n)$ queda por debajo de $c\cdot g(n)$. |
| little-$o$ | [Abrir local](./2_notacion_little_o.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/2_notacion_little_o.ipynb) | Cuándo $C(n)$ crece estrictamente más lento que $g(n)$. |
| Big-$\Omega$ | [Abrir local](./3_notacion_big_omega.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/3_notacion_big_omega.ipynb) | Cuándo $C(n)$ queda por encima de $c\cdot g(n)$. |
| little-$\omega$ | [Abrir local](./4_notacion_little_omega.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/4_notacion_little_omega.ipynb) | Cuándo $C(n)$ crece estrictamente más rápido que $g(n)$. |
| $\Theta$ | [Abrir local](./5_notacion_theta.ipynb) | [Abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/5_notacion_theta.ipynb) | Cuándo $C(n)$ queda entre $c_1\cdot g(n)$ y $c_2\cdot g(n)$. |

---

## 3.1 Contexto histórico

El análisis de algoritmos moderno recurre a la notación asintótica para describir el comportamiento esperado de las funciones de complejidad. Este lenguaje formal tiene raíces en estudios matemáticos de los siglos XVIII y XIX sobre límites, series y funciones.

### 3.1.1 Análisis del comportamiento límite

Los primeros antecedentes se encuentran en el trabajo de matemáticos como Leonhard Euler y Augustin-Louis Cauchy, quienes estudiaron el comportamiento de funciones y series cerca de valores extremos. Esa mirada preparó el terreno para analizar qué ocurre cuando una variable crece sin cota.

En el análisis de algoritmos, la variable de interés suele ser el tamaño de entrada $n$. Si $C(n)$ representa el costo de un algoritmo, entonces el análisis asintótico pregunta qué ocurre cuando:

$$
n\to\infty
$$

El punto clave es que no se busca describir cada valor exacto de $C(n)$, sino su tendencia dominante.

### 3.1.2 El trabajo de Bachmann y Landau

El primer uso formal documentado de una notación destinada a acotar el crecimiento de funciones se remonta al trabajo de Paul Bachmann, quien introdujo la notación Big-$O$ en teoría de números. Posteriormente, Edmund Landau retomó y extendió este formalismo, consolidando el uso de Big-$O$ y little-$o$.

Estas notaciones permitieron separar dos ideas:

- el valor exacto de una función;
- la forma en que esa función crece cuando su argumento tiende a infinito.

### 3.1.3 El salto a la computación

La incorporación de la notación asintótica al análisis de algoritmos tuvo lugar con fuerza durante el siglo XX. Donald E. Knuth organizó y extendió el uso de estas ideas en el análisis computacional, formalizando el uso de $O$, $\Omega$ y $\Theta$ como herramientas para clasificar problemas y algoritmos.

En computación, esta abstracción resulta útil porque el tiempo medido en una máquina concreta depende del lenguaje, el hardware, el compilador, el sistema operativo y muchas otras condiciones. La forma de crecimiento, en cambio, suele ser más estable.

### 3.1.4 Consolidación y uso moderno

La notación asintótica se consolidó como una convención central en el análisis de algoritmos. Su propósito es abstraer detalles de implementación y enfocar el estudio en el crecimiento funcional.

Por eso, cuando decimos que un algoritmo tiene costo $O(n^2)$, no estamos dando un tiempo exacto de ejecución. Estamos diciendo que su crecimiento queda acotado superiormente por una función cuadrática, salvo constantes y valores iniciales pequeños.

---

## 3.2 Comportamiento asintótico general

Una función de complejidad puede expresarse como una combinación de términos cuyo crecimiento está ordenado de menor a mayor:

$$
f(n)=f_1(n)+f_2(n)+f_3(n)+\cdots+f_m(n)
$$

donde:

$$
f_1(n)\prec f_2(n)\prec \cdots \prec f_m(n)
$$

El término $f_m(n)$ representa el término dominante. Si analizamos el cociente entre la función completa y su término dominante, los términos de menor orden se vuelven despreciables:

$$
\lim_{n\to\infty}
\left(
\frac{f(n)}{f_m(n)}
\right)
=1
$$

Por lo tanto:

$$
f(n)\sim f_m(n)
\qquad
n\to\infty
$$

El símbolo $\sim$ expresa equivalencia asintótica: ambas funciones se vuelven indistinguibles en su forma dominante de crecimiento.

### 3.2.1 Caso particular: función polinómica

Consideremos una función polinómica:

$$
f(n)=a_k n^k+a_{k-1}n^{k-1}+\cdots+a_1n+a_0
$$

donde $a_k\ne 0$ y $k\in\mathbb{Z}_0^{+}$. Cuando $n$ tiende a infinito, el término de mayor grado domina el comportamiento:

$$
\lim_{n\to\infty}
\left(
\frac{f(n)}{a_k n^k}
\right)
=1
$$

Por tanto:

$$
f(n)\sim a_k n^k
\qquad
n\to\infty
$$

Como las constantes multiplicativas no modifican la familia de crecimiento, también se usa la lectura:

$$
f(n)\sim n^k
\qquad
n\to\infty
$$

### 3.2.2 Caso particular: función exponencial

Consideremos una función donde aparece un término exponencial junto con términos polinómicos:

$$
g(n)=a^n+c_k n^k+c_{k-1}n^{k-1}+\cdots+c_1n+c_0
$$

Si la base $a$ es mayor que $1$, el término exponencial domina a los términos polinómicos. En ese caso:

$$
\lim_{n\to\infty}
\left(
\frac{g(n)}{a^n}
\right)
=1
$$

Por lo tanto:

$$
g(n)\sim a^n
\qquad
n\to\infty
$$

### 3.2.3 Jerarquía funcional asintótica

Aplicando los resultados anteriores a las funciones comunes del Capítulo 2, se obtiene una jerarquía funcional útil para comparar crecimientos:

$$
1
\prec
\log_{\ell}(n)
\prec
n
\prec
n\log_{\ell}(n)
\prec
n^2
\prec
n^3
\prec
\cdots
\prec
n^k
\prec
2^n
\prec
n!
$$

Las funciones con tasas de crecimiento más lentas, como $1$, $\log(n)$ y $n$, suelen mantenerse manejables incluso para entradas grandes. En cambio, las funciones polinómicas de alto grado, exponenciales y factoriales pueden superar rápidamente cualquier umbral práctico.

---

## 3.3 Familias de funciones

### 3.3.1 Definición

Una familia de funciones es un conjunto de funciones que comparten una misma estructura general. Su forma concreta queda determinada por el valor de ciertos parámetros.

Sea $\Lambda$ un conjunto no vacío de parámetros. Una familia de funciones puede escribirse como:

$$
\mathcal{F}
=
\{f_{\lambda}:\lambda\in\Lambda\}
$$

donde $\lambda$ representa el parámetro que identifica a cada función de la familia.

Por ejemplo, las funciones lineales pueden expresarse como:

$$
\mathcal{F}
=
\{f_{(m,b)}:\mathbb{R}\to\mathbb{R}\mid f_{(m,b)}(x)=mx+b,\;(m,b)\in\mathbb{R}^2\}
$$

Distintos valores de $m$ y $b$ producen funciones distintas, pero todas comparten la estructura lineal.

### 3.3.2 Familias de funciones en el límite asintótico

En análisis asintótico, el interés recae sobre el comportamiento de una función cuando el argumento crece sin cota. Dada una función de complejidad:

$$
C:\mathbb{N}\to\mathbb{R}^{+},
\qquad
n\mapsto C(n)
$$

podemos pensar en la familia de funciones con comportamiento asintótico equivalente a $C(n)$:

$$
\mathcal{F}(C(n))
=
\{f_{\lambda}:\mathbb{N}\to\mathbb{R}^{+}\mid \lambda\in\Lambda,\; f_{\lambda}(n)\sim C(n)\}
$$

Por ejemplo, las funciones $3n+5$, $7n-2$ y $n+\log(n)$ pertenecen a la misma familia lineal, porque todas tienen crecimiento dominante lineal.

### 3.3.3 Propiedades asintóticas de $\mathcal{F}$

| Propiedad | Idea formal | Significado |
|---|---|---|
| Invarianza frente a constantes | $c\in\mathbb{R}^{+}\Rightarrow \mathcal{F}(c\cdot g(n))=\mathcal{F}(g(n))$ | Multiplicar por una constante positiva no cambia la familia asintótica. |
| Aditividad | $\mathcal{F}(f(n))+\mathcal{F}(g(n))\subseteq \mathcal{F}(f(n)+g(n))$ | La suma conserva la lectura por familias de crecimiento. |
| Multiplicatividad | $\mathcal{F}(f(n))\cdot\mathcal{F}(g(n))\subseteq \mathcal{F}(f(n)\cdot g(n))$ | El producto combina los comportamientos de crecimiento. |
| Dominancia | $\lim_{n\to\infty}\frac{g(n)}{f(n)}=0\Rightarrow \mathcal{F}(f(n)+g(n))=\mathcal{F}(f(n))$ | Si $f(n)$ domina a $g(n)$, la suma queda gobernada por $f(n)$. |

### 3.3.4 Ejemplos de clasificación en familias

| Función $f(n)$ | Familia asintótica |
|---|---|
| $f(n)=k$ | $\mathcal{F}(1)$ |
| $f(n)=3n+5$ | $\mathcal{F}(n)$ |
| $f(n)=n\log(n)+5n$ | $\mathcal{F}(n\log(n))$ |
| $f(n)=3n^2+7n+1$ | $\mathcal{F}(n^2)$ |
| $f(n)=2^n+n^3$ | $\mathcal{F}(2^n)$ |
| $f(n)=k\cdot n!+2^n$ | $\mathcal{F}(n!)$ |

---

## 3.4 Notación asintótica simplificada

En la práctica, muchas veces se reemplaza una función completa por su término dominante. Por ejemplo:

$$
n^3+2n^2+n+5
\quad\leadsto\quad
n^3
$$

Esta simplificación no dice que ambas funciones sean iguales. Dice que, para estudiar crecimiento, los términos de menor orden pierden importancia cuando $n$ se hace suficientemente grande.

La herramienta que formaliza esa idea es el cociente:

$$
\frac{C(n)}{g(n)}
$$

Según el valor al que tienda ese cociente, se decide qué tipo de relación asintótica existe entre $C(n)$ y $g(n)$.

Una precisión importante: en muchos textos se escribe:

$$
C(n)=O(g(n))
$$

como una abreviatura convencional. Sin embargo, formalmente $O(g(n))$ representa una familia de funciones. Por eso, en este capítulo usaremos la lectura:

$$
C(n)\in O(g(n))
$$

---

## 3.5 Tipos de notación asintótica

Las cinco notaciones principales describen relaciones distintas entre $C(n)$ y $g(n)$.

| Notación | Tipo de relación | Lectura |
|---|---|---|
| $O(g(n))$ | Cota superior | $C(n)$ crece al mismo ritmo o más lento que $g(n)$. |
| $o(g(n))$ | Cota superior estricta | $C(n)$ crece estrictamente más lento que $g(n)$. |
| $\Omega(g(n))$ | Cota inferior | $C(n)$ crece al mismo ritmo o más rápido que $g(n)$. |
| $\omega(g(n))$ | Cota inferior estricta | $C(n)$ crece estrictamente más rápido que $g(n)$. |
| $\Theta(g(n))$ | Cota ajustada | $C(n)$ queda acotada por abajo y por arriba por múltiplos de $g(n)$. |

---

## 3.5.1 Notación Big-O

La notación Big-$O$ describe una cota superior asintótica. Se utiliza para mostrar que $C(n)$ crece al mismo ritmo o más lento que $g(n)$. Decir que:

$$
C(n)\in O(g(n))
$$

significa que existe una constante positiva $c$ y un punto $n_0$ a partir del cual $C(n)$ nunca supera a $c\cdot g(n)$:

$$
C(n)\in O(g(n))
\iff
\exists c\in\mathbb{R}^{+},\exists n_0\in\mathbb{N}:
\forall n\ge n_0,\;
C(n)\le c\cdot g(n)
$$

La demostración por límite usa el límite superior:

$$
k=
\limsup_{n\to\infty}
\left(
\frac{C(n)}{g(n)}
\right)
$$

Si el límite superior converge a una constante finita, entonces existe una cota superior. Cuando $k$ es positivo, una elección válida para la constante debe satisfacer:

$$
c\ge k
$$

El valor $n_0$ se obtiene buscando el primer punto a partir del cual se cumple la desigualdad. Si $A$ representa ese umbral real, entonces:

$$
n_0=\lceil A\rceil
$$

donde $A$ satisface:

$$
\forall n\ge A,\qquad C(n)\le c\cdot g(n)
$$

Notebook: [abrir simulación Big-O](./1_notacion_big_o.ipynb) · [abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/1_notacion_big_o.ipynb)

---

## 3.5.2 Notación little-o

La notación little-$o$ describe una cota superior estricta. Se utiliza para mostrar que $C(n)$ crece estrictamente más lento que $g(n)$. Decir que:

$$
C(n)\in o(g(n))
$$

equivale a exigir:

$$
\lim_{n\to\infty}
\left(
\frac{C(n)}{g(n)}
\right)
=0
$$

La lectura con desigualdad es más fuerte que en Big-$O$: para cualquier constante positiva $c$, existe un punto desde el cual:

$$
C(n)\le c\cdot g(n)
\qquad
\forall n\ge n_0
$$

Es decir, no importa qué tan pequeño sea el múltiplo positivo de $g(n)$: eventualmente $C(n)$ queda por debajo.

El valor $n_0$ se calcula identificando el primer umbral real $A$ desde el cual se cumple la desigualdad:

$$
n_0=\lceil A\rceil
$$

donde:

$$
\forall n\ge A,\qquad C(n)\le c\cdot g(n)
$$

Notebook: [abrir simulación little-o](./2_notacion_little_o.ipynb) · [abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/2_notacion_little_o.ipynb)

---

## 3.5.3 Notación Big-Omega

La notación Big-$\Omega$ describe una cota inferior asintótica. Se utiliza para mostrar que $C(n)$ crece al mismo ritmo o más rápido que $g(n)$. Decir que:

$$
C(n)\in \Omega(g(n))
$$

significa que existe una constante positiva $c$ y un punto $n_0$ a partir del cual $C(n)$ queda por encima de $c\cdot g(n)$:

$$
C(n)\in \Omega(g(n))
\iff
\exists c\in\mathbb{R}^{+},\exists n_0\in\mathbb{N}:
\forall n\ge n_0,\;
C(n)\ge c\cdot g(n)
$$

La demostración por límite usa el límite inferior:

$$
k=
\liminf_{n\to\infty}
\left(
\frac{C(n)}{g(n)}
\right)
$$

Si $k$ es positivo, entonces existe una cota inferior asintótica. Cuando el cociente converge a $k$, una constante válida debe satisfacer:

$$
c\in(0,k]
$$

El valor $n_0$ se obtiene buscando el primer umbral real $A$ desde el cual se cumple:

$$
n_0=\lceil A\rceil
$$

donde:

$$
\forall n\ge A,\qquad C(n)\ge c\cdot g(n)
$$

Notebook: [abrir simulación Big-Omega](./3_notacion_big_omega.ipynb) · [abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/3_notacion_big_omega.ipynb)

---

## 3.5.4 Notación little-omega

La notación little-$\omega$ describe una cota inferior estricta. Se utiliza para mostrar que $C(n)$ crece estrictamente más rápido que $g(n)$. Decir que:

$$
C(n)\in \omega(g(n))
$$

equivale a exigir:

$$
\lim_{n\to\infty}
\left(
\frac{C(n)}{g(n)}
\right)
=\infty
$$

La lectura con desigualdad indica que, para cualquier constante positiva $c$, eventualmente:

$$
C(n)\ge c\cdot g(n)
\qquad
\forall n\ge n_0
$$

Es decir, no importa qué tan grande sea el múltiplo positivo de $g(n)$: si $C(n)\in\omega(g(n))$, terminará superándolo.

El valor $n_0$ se calcula identificando el primer umbral real $A$ desde el cual se cumple:

$$
n_0=\lceil A\rceil
$$

donde:

$$
\forall n\ge A,\qquad C(n)\ge c\cdot g(n)
$$

Notebook: [abrir simulación little-omega](./4_notacion_little_omega.ipynb) · [abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/4_notacion_little_omega.ipynb)

---

## 3.5.5 Notación Theta

La notación $\Theta$ define la familia de funciones que están acotadas simultáneamente por arriba y por abajo por múltiplos constantes de una función de referencia. Se utiliza para describir una cota ajustada.

Decir que:

$$
C(n)\in \Theta(g(n))
$$

significa que existen dos constantes positivas $c_1$ y $c_2$, y un punto $n_0$, tales que:

$$
C(n)\in \Theta(g(n))
\iff
\exists c_1,c_2\in\mathbb{R}^{+},\exists n_0\in\mathbb{N}:
\forall n\ge n_0,\;
c_1\cdot g(n)\le C(n)\le c_2\cdot g(n)
$$

También puede leerse como la intersección entre una cota inferior y una cota superior:

$$
C(n)\in \Theta(g(n))
\iff
C(n)\in \Omega(g(n))
\quad\text{y}\quad
C(n)\in O(g(n))
$$

Si el cociente converge a una constante positiva:

$$
\lim_{n\to\infty}
\left(
\frac{C(n)}{g(n)}
\right)
=k,
\qquad
k\in\mathbb{R}^{+}
$$

entonces $C(n)$ y $g(n)$ tienen el mismo orden de crecimiento dominante.

El valor $n_0$ se obtiene identificando el primer umbral real $A$ desde el cual se cumplen simultáneamente ambas desigualdades:

$$
n_0=\lceil A\rceil
$$

donde:

$$
\forall n\ge A,\qquad c_1\cdot g(n)\le C(n)\le c_2\cdot g(n)
$$

Notebook: [abrir simulación Theta](./5_notacion_theta.ipynb) · [abrir en Colab](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo3/5_notacion_theta.ipynb)

---

## 3.5.6 Resumen de propiedades

| Notación | Límite del cociente | Desigualdad eventual | Lectura |
|---|---|---|---|
| $O(g(n))$ | $\limsup\frac{C(n)}{g(n)}\text{ es finito}$ | $C(n)\le c\cdot g(n)$ | Cota superior. |
| $o(g(n))$ | $\lim\frac{C(n)}{g(n)}=0$ | $C(n)\le c\cdot g(n)$ para todo $c\in\mathbb{R}^{+}$ | Cota superior estricta. |
| $\Omega(g(n))$ | $\liminf\frac{C(n)}{g(n)}\text{ es positivo}$ | $C(n)\ge c\cdot g(n)$ | Cota inferior. |
| $\omega(g(n))$ | $\lim\frac{C(n)}{g(n)}=\infty$ | $C(n)\ge c\cdot g(n)$ para todo $c\in\mathbb{R}^{+}$ | Cota inferior estricta. |
| $\Theta(g(n))$ | $\lim\frac{C(n)}{g(n)}=k$, con $k\in\mathbb{R}^{+}$ | $c_1\cdot g(n)\le C(n)\le c_2\cdot g(n)$ | Cota ajustada. |

---

## Controles de las simulaciones

Las simulaciones del capítulo comparten una misma estructura para que puedas comparar las notaciones sin aprender una interfaz distinta en cada notebook.

| Control | Significado |
|---|---|
| $C(n)$ | Función de complejidad de interés. |
| $g(n)$ | Función de referencia contra la que se compara $C(n)$. |
| $a$ y $b$ | Intervalo visible de la gráfica. |
| $c$ | Constante usada en $O$, $o$, $\Omega$ y $\omega$. |
| $c_1$ y $c_2$ | Constantes usadas en $\Theta$. |
| Escala | Permite alternar entre escala lineal y logarítmica. |

Además, puedes mover el intervalo directamente sobre la gráfica. Esto ayuda a ver que muchas desigualdades no tienen que cumplirse desde $n=0$, sino desde algún punto $n_0$.

---

## Ejemplo base del libro

El ejemplo usado como referencia en las simulaciones es:

$$
C(n)=n^3+2n^2+n+5
$$

comparado con:

$$
g(n)=n^3
$$

El cociente es:

$$
\frac{C(n)}{g(n)}
=
1+\frac{2}{n}+\frac{1}{n^2}+\frac{5}{n^3}
$$

Por lo tanto:

$$
\lim_{n\to\infty}
\left(
\frac{C(n)}{g(n)}
\right)
=1
$$

La conclusión es:

$$
C(n)\in \Theta(n^3)
$$

y, como consecuencia:

$$
C(n)\in O(n^3)
\qquad
\text{y}
\qquad
C(n)\in \Omega(n^3)
$$

pero:

$$
C(n)\notin o(n^3)
\qquad
\text{y}
\qquad
C(n)\notin \omega(n^3)
$$

La razón es que el cociente no tiende a $0$ ni a $\infty$; tiende a una constante positiva.

---

## Material de referencia

Los ejemplos concretos del libro se conservaron como material de referencia para reutilización futura:

| Recurso | Local |
|---|---|
| Ejemplos concretos de notaciones | [Abrir](./referencias/ejemplos_concretos_notaciones.ipynb) |
| Representación genérica de la notación asintótica | [Abrir](./referencias/notacion_asintotica_representacion_generica.ipynb) |

---

## Preguntas para estudiar mientras ejecutas

1. ¿Qué función estás usando como $C(n)$?
2. ¿Qué función estás usando como referencia $g(n)$?
3. ¿El cociente $\frac{C(n)}{g(n)}$ tiende a $0$, a una constante positiva o a $\infty$?
4. ¿La desigualdad se cumple desde el inicio o solo después de cierto $n_0$?
5. ¿La cota es válida pero demasiado amplia?
6. ¿Qué cambia cuando agregas términos de menor orden?
7. ¿La escala lineal permite ver la relación o conviene usar escala logarítmica?
8. ¿La conclusión coincide con lo que esperabas por la jerarquía funcional?

---

## Errores comunes

| Error | Por qué ocurre | Cómo evitarlo |
|---|---|---|
| Leer $O(g(n))$ como igualdad exacta | $O(g(n))$ representa una familia de funciones, no una función individual. | Usa la lectura $C(n)\in O(g(n))$. |
| Olvidar el papel de $n_0$ | La desigualdad no tiene que cumplirse para valores pequeños de $n$. | Busca desde qué punto se vuelve estable. |
| Confundir Big-$O$ con $\Theta$ | Una cota superior puede ser correcta pero poco ajustada. | Verifica también si existe cota inferior. |
| Usar little-$o$ como si fuera Big-$O$ | little-$o$ exige crecimiento estrictamente más lento. | Revisa si el cociente tiende a $0$. |
| Usar little-$\omega$ como si fuera Big-$\Omega$ | little-$\omega$ exige crecimiento estrictamente más rápido. | Revisa si el cociente tiende a $\infty$. |
| Elegir $c$ sin mirar la desigualdad | El límite orienta la constante, pero $n_0$ depende del valor concreto elegido. | Cambia $c$ en la simulación y observa si existe $n_0$. |

---

## 3.6 Ejercicios propuestos

Los ejercicios del capítulo permiten practicar comparación de funciones, demostraciones por límite y cálculo de constantes asintóticas.

[Ver soluciones de los ejercicios propuestos del Capítulo 3](https://drive.google.com/file/d/175Q_ze2udbV-mJwqsI34MmwCeHKvs3qP/view)

---

## Licencia

El contenido de este capítulo se distribuye bajo la licencia Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0).

© 2026 Carlos Eduardo Orozco Garcés, César Jesús Pardo Calvache, Mauro Callejas Cuervo
