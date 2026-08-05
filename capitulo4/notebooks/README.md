# Capítulo 4: Análisis de algoritmos estructurados

Este capítulo aplica las funciones de complejidad y la notación asintótica al análisis de algoritmos construidos mediante secuencias, condicionales y ciclos. El objetivo es reconocer cómo la estructura del código determina el crecimiento del tiempo de ejecución y del consumo adicional de memoria.

La pregunta central es:

> ¿Cómo podemos determinar la complejidad de un algoritmo a partir de sus estructuras de control?

El análisis formal y el análisis experimental cumplen funciones distintas. El primero permite deducir el orden de crecimiento sin depender de una máquina concreta. El segundo aporta evidencia observable sobre esa tendencia y ayuda a distinguirla del ruido propio de las mediciones.

---

## Cómo estudiar este capítulo con los notebooks

Cada notebook conecta el análisis del libro con una simulación ejecutable. Una ruta de trabajo recomendada es:

1. Lee el ejemplo y determina qué representa el tamaño de entrada $n$.
2. Identifica las instrucciones cuyo número de ejecuciones depende de $n$.
3. Obtén las funciones $T(n)$ y $S(n)$.
4. Reduce cada función a su término dominante.
5. Predice la forma de las curvas temporal y espacial.
6. Abre el notebook y ejecuta ambas simulaciones.
7. Cambia el máximo valor de $n$ y el número de ejecuciones.
8. Compara las mediciones con la curva teórica ajustada.
9. Explica cualquier fluctuación sin confundirla con un cambio de complejidad.

Los notebooks no sustituyen el análisis formal. Permiten contrastar sus conclusiones con mediciones reales.

---

## Objetivos de aprendizaje

Al finalizar este capítulo deberías poder:

- identificar el tamaño de entrada de un algoritmo;
- distinguir entre complejidad temporal y complejidad espacial adicional;
- calcular el costo de secuencias, condicionales y ciclos;
- analizar ciclos anidados y ciclos con incrementos distintos de uno;
- componer los costos de varios bloques;
- reconocer cuándo una constante no depende de $n$;
- identificar costos ocultos por el tamaño de los datos procesados;
- contrastar una función teórica con resultados experimentales;
- interpretar correctamente las fluctuaciones de tiempo y memoria.

---

## Mapa del capítulo

| Sección | Tema | Pregunta guía |
|---|---|---|
| 4.1 | Aspectos preliminares | ¿Qué representa el costo de un algoritmo? |
| 4.2 | Complejidad temporal | ¿Cuántas operaciones se ejecutan cuando aumenta $n$? |
| 4.3 | Complejidad espacial | ¿Cuánta memoria adicional requiere el algoritmo? |
| 4.4 | Estructuras de control | ¿Cómo se analizan secuencias, condicionales y ciclos? |
| 4.5 | Composición de complejidades | ¿Cómo se combinan los costos de varios bloques? |
| 4.6 | Ejercicios propuestos | ¿Cómo se aplican estos criterios a nuevos algoritmos? |

---

## Notebooks experimentales

Los enlaces locales abren los archivos del repositorio. Los enlaces de Colab abren las versiones ejecutables en línea.

| Ejemplo | Algoritmo | Tiempo | Espacio adicional | Local | Colab |
|---:|---|:---:|:---:|:---:|:---:|
| 1 | Sumar dos números | $O(1)$ | $O(1)$ | [Abrir](./ejemplo1_(sumar_numeros).ipynb) | [Ejecutar](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo1_(sumar_numeros).ipynb) |
| 2 | Recorrer los elementos de un arreglo | $O(n)$ | $O(1)$ | [Abrir](./ejemplo2_(imprimir_elementos_arreglo).ipynb) | [Ejecutar](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo2_(imprimir_elementos_arreglo).ipynb) |
| 3 | Recorrer los elementos de una matriz | $O(n^2)$ | $O(1)$ | [Abrir](./ejemplo3_(imprimir_elementos_matriz).ipynb) | [Ejecutar](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo3_(imprimir_elementos_matriz).ipynb) |
| 4 | Crear y recorrer una matriz variable | $O(n^2)$ | $O(n^2)$ | [Abrir](./ejemplo4_(inicializar_matriz_variable).ipynb) | [Ejecutar](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo4_(inicializar_matriz_variable).ipynb) |
| 5 | Recorrer una matriz con incremento no unitario | $O(n^2)$ | $O(n^2)$ | [Abrir](./ejemplo5_(ciclos_incremento_no_lineal).ipynb) | [Ejecutar](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo5_(ciclos_incremento_no_lineal).ipynb) |
| 7 | Ejecutar un ciclo con límite fijo | $O(1)$ | $O(1)$ | [Abrir](./ejemplo7_(ciclo_sin_dependencia).ipynb) | [Ejecutar](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo7_(ciclo_sin_dependencia).ipynb) |
| 9 | Calcular Fibonacci iterativo | $O(n)$ | $O(1)$ | [Abrir](./ejemplo9_(fibonacci_iterativo).ipynb) | [Ejecutar](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo9_(fibonacci_iterativo).ipynb) |
| 10 | Calcular Fibonacci iterativo con enteros de precisión arbitraria | $O(n^2)$ | $O(n)$ | [Abrir](./ejemplo10_(complejidad_oculta).ipynb) | [Ejecutar](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo10_(complejidad_oculta).ipynb) |

La numeración conserva la correspondencia con los ejemplos del libro; por eso la secuencia no es consecutiva.

---

## Qué muestran las simulaciones

Cada notebook contiene dos laboratorios:

- **complejidad temporal experimental**, representada mediante $T(n)$;
- **complejidad espacial experimental**, representada mediante $S(n)$.

Las simulaciones permiten modificar:

- el máximo valor de $n$;
- el número de ejecuciones utilizadas en cada medición;
- la ejecución de valores adicionales dentro de un límite seguro.

Después de ejecutar, la tabla muestra los puntos correspondientes a potencias de diez y la gráfica compara:

- la medición experimental;
- la curva teórica ajustada a las mediciones.

La constante de ajuste se calcula sobre la región final de los datos. De esta manera, la comparación da más importancia a la zona donde debería dominar el comportamiento asintótico.

### Cómo interpretar los resultados

Una medición experimental no tiene que coincidir exactamente con la curva teórica. El tiempo puede variar por:

- procesos ejecutados en segundo plano;
- planificación del procesador;
- caché;
- recolección de basura;
- calentamiento del intérprete;
- resolución del reloj.

El consumo de memoria también incluye costos internos del intérprete y de las estructuras de Python. Por eso conviene observar la tendencia general y no una diferencia aislada.

Los puntos que superan los límites seguros no se ejecutan. La tabla los identifica y la gráfica conserva únicamente los resultados calculados de manera segura.

---

## 4.1 Aspectos preliminares

El análisis de algoritmos estudia cómo cambia un costo cuando aumenta el tamaño de la entrada. Si $n$ representa ese tamaño, utilizaremos:

$$
T(n)
$$

para describir el costo temporal y:

$$
S(n)
$$

para describir el consumo de memoria adicional.

Estas funciones no representan necesariamente segundos o bytes exactos. En el análisis formal pueden expresar cantidades de operaciones o unidades abstractas de memoria. La notación asintótica identifica después la forma dominante de crecimiento.

---

## 4.2 Complejidad temporal

Para calcular la complejidad temporal:

1. identifica las operaciones básicas;
2. determina cuántas veces se ejecuta cada operación;
3. expresa el costo total como una función de $n$;
4. conserva el término dominante.

Una secuencia fija de operaciones tiene costo constante:

$$
T(n)\in O(1)
$$

Un ciclo que recorre los $n$ elementos de una entrada tiene costo lineal:

$$
T(n)\in O(n)
$$

Dos ciclos anidados que recorren una matriz cuadrada producen:

$$
T(n)\in O(n^2)
$$

---

## 4.3 Complejidad espacial

La complejidad espacial adicional mide la memoria creada por el algoritmo sin contar la entrada recibida.

Un algoritmo que solo declara una cantidad fija de variables escalares utiliza:

$$
S(n)\in O(1)
$$

Crear un arreglo de tamaño $n$ requiere:

$$
S(n)\in O(n)
$$

Crear una matriz de $n\times n$ requiere:

$$
S(n)\in O(n^2)
$$

Esta distinción explica por qué recorrer una matriz recibida como argumento puede tener espacio adicional constante, mientras que crear esa misma matriz dentro de la función requiere espacio cuadrático.

---

## 4.4 Análisis de estructuras de control

### Secuencias

Los costos de bloques consecutivos se suman:

$$
T(n)=T_1(n)+T_2(n)+\cdots+T_k(n)
$$

La notación asintótica conserva el término de mayor crecimiento.

### Condicionales

En el peor caso se considera la rama de mayor costo:

$$
T(n)\in O\left(\max\{T_1(n),T_2(n),\ldots,T_k(n)\}\right)
$$

### Ciclos

| Estructura | Cantidad aproximada de iteraciones | Complejidad |
|---|---:|:---:|
| Límite fijo | $k$, con $k$ constante | $O(1)$ |
| Incremento unitario hasta $n$ | $n$ | $O(n)$ |
| Incremento de tamaño $k$ | $n/k$ | $O(n)$ |
| Multiplicación o división por una constante | $\log(n)$ | $O(\log n)$ |
| Dos ciclos lineales anidados | $n\cdot n$ | $O(n^2)$ |
| Ciclo lineal con ciclo logarítmico | $n\log(n)$ | $O(n\log n)$ |

El incremento constante de un índice modifica el coeficiente, pero no el orden asintótico. Por ejemplo:

$$
\frac{n}{2}\in O(n)
$$

---

## 4.5 Composición de complejidades

Para combinar estructuras:

- suma los costos de los bloques secuenciales;
- toma la rama de mayor costo en un condicional de peor caso;
- multiplica las cantidades de iteraciones de ciclos anidados;
- conserva el término dominante de la función resultante.

Por ejemplo:

$$
T(n)=an^2+bn+c
$$

se reduce a:

$$
T(n)\in O(n^2)
$$

El notebook de Fibonacci añade una consideración importante: una operación escrita como una sola instrucción no siempre tiene costo constante. Los enteros calculados crecen en cantidad de bits, por lo que las sumas se vuelven progresivamente más costosas. Bajo el modelo de complejidad en bits, el algoritmo iterativo utilizado en el capítulo presenta tiempo $O(n^2)$ y espacio $O(n)$.

---

## Ruta recomendada de experimentación

| Orden | Notebook | Qué deberías observar |
|---:|---|---|
| 1 | Sumar dos números | Las curvas permanecen aproximadamente constantes aunque cambie $n$. |
| 2 | Recorrer un arreglo | El tiempo crece de forma lineal y el espacio adicional permanece estable. |
| 3 | Recorrer una matriz | El tiempo refleja el efecto de dos ciclos anidados. |
| 4 | Crear una matriz | Tiempo y memoria crecen con el número de elementos creados. |
| 5 | Incremento no unitario | Recorrer una de cada dos columnas conserva el orden cuadrático. |
| 6 | Ciclo con límite fijo | Un ciclo grande sigue siendo constante si su límite no depende de $n$. |
| 7 | Fibonacci iterativo | El tamaño creciente de los enteros introduce un costo que no resulta evidente al contar únicamente iteraciones. |

---

## Preguntas para estudiar mientras ejecutas

- ¿Qué representa $n$ en cada ejemplo?
- ¿La función recibe la estructura o la crea internamente?
- ¿Qué parte del código determina $T(n)$?
- ¿Qué parte del código determina $S(n)$?
- ¿Duplicar $n$ produce el cambio esperado?
- ¿Las fluctuaciones modifican la tendencia o solo añaden ruido?
- ¿La curva teórica representa el orden correcto aunque no atraviese todos los puntos?
- ¿Qué ocurre al aumentar el número de ejecuciones?
- ¿Por qué un incremento de dos en dos sigue siendo lineal?
- ¿Qué operaciones aparentemente constantes dependen del tamaño de sus operandos?

---

## Errores comunes

### Confundir la entrada con memoria adicional

Recibir un arreglo de tamaño $n$ no implica automáticamente espacio adicional $O(n)$. El análisis espacial del algoritmo cuenta la memoria que crea durante su ejecución.

### Multiplicar bloques secuenciales

Los bloques consecutivos se suman. La multiplicación aparece cuando una estructura se ejecuta dentro de otra.

### Considerar que un ciclo siempre depende de $n$

Un ciclo con límite fijo conserva costo $O(1)$ aunque ejecute miles de iteraciones.

### Interpretar cada fluctuación como un cambio de complejidad

La complejidad describe una tendencia de crecimiento. Una medición aislada puede variar sin cambiar el orden asintótico.

### Suponer que toda instrucción tiene costo constante

El costo de una operación puede depender del tamaño de los datos que procesa, como ocurre con enteros de precisión arbitraria.

---

## Gráficas de referencia

Los notebooks utilizados para generar las imágenes estáticas del capítulo se encuentran en [`graficas/`](./graficas/). Estas versiones sirven como base reproducible para las figuras del libro y están separadas de los laboratorios experimentales.

Consulta la [guía de los notebooks de gráficas](./graficas/README.md) para conocer sus archivos y la forma de ejecutarlos.

---

## 4.6 Ejercicios propuestos

Los ejercicios propuestos permiten practicar:

- identificación del tamaño de entrada;
- conteo de operaciones;
- cálculo de complejidad temporal;
- cálculo de espacio adicional;
- composición de estructuras de control;
- aplicación de notación asintótica.

[Abrir los ejercicios propuestos en el visor en línea](https://docs.google.com/gview?embedded=true&url=https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main/capitulo4/ejercicios_propuestos.pdf)

[Descargar el PDF desde el repositorio](./ejercicios_propuestos.pdf)

---

## Comandos LaTeX

```latex
\newcommand{\colabSumarNumeros}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo1_(sumar_numeros).ipynb}
\newcommand{\colabImprimirElementosArreglo}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo2_(imprimir_elementos_arreglo).ipynb}
\newcommand{\colabImprimirElementosMatriz}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo3_(imprimir_elementos_matriz).ipynb}
\newcommand{\colabInicializarMatrizVariable}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo4_(inicializar_matriz_variable).ipynb}
\newcommand{\colabCiclosIncrementoNoLineal}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo5_(ciclos_incremento_no_lineal).ipynb}
\newcommand{\colabCicloSinDependencia}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo7_(ciclo_sin_dependencia).ipynb}
\newcommand{\colabFibonacciIterativo}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo9_(fibonacci_iterativo).ipynb}
\newcommand{\colabComplejidadOculta}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/notebooks/ejemplo10_(complejidad_oculta).ipynb}
\newcommand{\visorEjerciciosCapituloCuatro}{https://docs.google.com/gview?embedded=true\&url=https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main/capitulo4/ejercicios_propuestos.pdf}
```

---

## Estructura de archivos

```text
capitulo4/
├── README.md
├── colab_bootstrap.py
├── experiment_ui.py
├── experimental_analysis.py
├── ejemplo1_(sumar_numeros).ipynb
├── ejemplo2_(imprimir_elementos_arreglo).ipynb
├── ejemplo3_(imprimir_elementos_matriz).ipynb
├── ejemplo4_(inicializar_matriz_variable).ipynb
├── ejemplo5_(ciclos_incremento_no_lineal).ipynb
├── ejemplo7_(ciclo_sin_dependencia).ipynb
├── ejemplo9_(fibonacci_iterativo).ipynb
├── ejemplo10_(complejidad_oculta).ipynb
├── ejercicios_propuestos.pdf
└── graficas/
```

---

## Licencia

El contenido de este capítulo se distribuye bajo la licencia **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. Se autoriza su uso con fines académicos citando la fuente original.
