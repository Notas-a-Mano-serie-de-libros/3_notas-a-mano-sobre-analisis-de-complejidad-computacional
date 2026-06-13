# Capítulo 5: Relaciones de recurrencia y análisis de complejidad

Este capítulo estudia cómo describir y resolver el costo de los algoritmos recursivos. Una relación de recurrencia expresa $C(n)$ mediante el costo de uno o varios subproblemas más pequeños y el trabajo adicional $f(n)$ realizado fuera de las llamadas recursivas.

La pregunta central es:

> ¿Cómo podemos obtener la función de complejidad de un algoritmo a partir de la forma en que genera y reduce sus subproblemas?

El capítulo conecta la formulación matemática con dos notebooks interactivos. El primero permite construir y recorrer árboles de recurrencia. El segundo permite elegir un método de solución compatible, seguir su desarrollo y comparar la expresión exacta con el resultado asintótico.

---

## Cómo estudiar este capítulo con los notebooks

Una ruta de trabajo recomendada es:

1. Identifica el caso base del algoritmo.
2. Determina cuántos subproblemas genera cada llamada.
3. Establece cómo cambia el tamaño de cada subproblema.
4. Separa el costo recursivo del costo externo $f(n)$.
5. Clasifica la relación como reducción, división o combinación de términos con factores distintos.
6. Predice la forma y la altura del árbol.
7. Abre el notebook de árboles y contrasta tu predicción.
8. Selecciona un método compatible en el notebook de solución.
9. Sigue el desarrollo hasta la condición inicial y verifica el resultado asintótico.

Los notebooks no sustituyen la derivación matemática. Su propósito es hacer visibles las expansiones, los niveles del árbol, las condiciones de aplicación y los pasos que conducen al resultado.

---

## Objetivos de aprendizaje

Al finalizar este capítulo deberías poder:

- formular una relación de recurrencia a partir de un algoritmo recursivo;
- distinguir entre relaciones de reducción y de división;
- interpretar el papel de $a_i$, $b_i$, $f(n)$ y el caso base;
- construir y analizar un árbol de recurrencia;
- calcular el número de nodos y el costo de cada nivel;
- aplicar sustitución iterativa cuando la expansión produce un patrón manejable;
- elegir entre el teorema maestro básico, extendido y generalizado;
- reconocer cuándo el teorema maestro no aplica;
- construir la ecuación característica de una relación lineal de reducción;
- diferenciar una solución exacta de una clasificación asintótica.

---

## Mapa del capítulo

| Sección | Tema | Pregunta guía |
|---|---|---|
| 5.1 | Relaciones de recurrencia | ¿Cómo se define una sucesión o un costo mediante valores anteriores? |
| 5.2 | Clasificación | ¿Qué propiedades determinan el método de solución? |
| 5.3 | Recurrencias en algoritmos | ¿Cómo se representan las llamadas y el trabajo externo? |
| 5.4 | Métodos de solución | ¿Qué método es compatible con cada estructura? |
| 5.5 | Comparación de métodos | ¿Qué resultado produce cada método y cuáles son sus límites? |
| 5.6 | Ejercicios propuestos | ¿Cómo se aplican los métodos a nuevas relaciones? |

---

## Notebooks interactivos

Los enlaces locales abren los archivos del repositorio. Los enlaces de Colab abren sus versiones ejecutables en línea.

| Notebook | Propósito | Local | Colab |
|---|---|:---:|:---:|
| Árboles de recurrencia | Construir una relación, recorrer sus niveles y observar el costo de los nodos. | [Abrir](./0_arboles_recursion.ipynb) | [Ejecutar](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo5/0_arboles_recursion.ipynb) |
| Métodos de solución | Aplicar sustitución iterativa, árbol de recurrencia, teorema maestro o ecuación característica. | [Abrir](./1_metodos_solucion_relaciones_recurrencia.ipynb) | [Ejecutar](https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo5/1_metodos_solucion_relaciones_recurrencia.ipynb) |

### Controles principales

Las simulaciones permiten modificar:

- el tipo de relación;
- el costo externo $f(n)$;
- el caso base;
- la cantidad $m$ de términos recursivos;
- los coeficientes $a_i$;
- los desplazamientos o factores $b_i$;
- la profundidad visible $h$;
- los parámetros $k$, $p$ y $\ell$ de las funciones configurables;
- el método y, cuando corresponde, la versión del teorema maestro.

El catálogo de costos externos incluye:

$$
0,\quad 1,\quad \log_2(n),\quad n,\quad n\log_2(n),\quad
n^2,\quad n^3,\quad n^k,\quad n^k\log_\ell^p(n),\quad 2^n,\quad n!
$$

Cuando se selecciona $n^k$, aparece el parámetro $k$. Para $n^k\log_\ell^p(n)$ aparecen, debajo de $b_i$, los parámetros $k$, $p$ y $\ell$. La base elegida se conserva en las expresiones y en los resultados mostrados por la simulación.

---

## 5.1 Relaciones de recurrencia

Una relación de recurrencia define un término mediante uno o varios términos anteriores:

$$
a_n=f(a_{n-1},a_{n-2},\ldots,a_{n-k})
$$

Para determinar una solución se necesitan condiciones iniciales. Por ejemplo:

- factorial: $a_n=n\,a_{n-1}$, con $a_0=1$;
- Fibonacci: $a_n=a_{n-1}+a_{n-2}$, con valores iniciales establecidos.

En análisis de algoritmos, $C(n)$ representa el costo de resolver una entrada de tamaño $n$. La relación separa dos contribuciones:

- el costo de las llamadas recursivas;
- el trabajo adicional $f(n)$ ejecutado fuera de ellas.

---

## 5.2 Clasificación de las relaciones

### Lineales y no lineales

Una relación es lineal cuando cada término recurrente aparece elevado a la primera potencia y no se multiplica por otro término recurrente. Si aparecen productos o potencias de esos términos, la relación es no lineal.

### Homogéneas y no homogéneas

Una relación lineal homogénea contiene únicamente términos de la sucesión. Una relación no homogénea añade una función independiente:

$$
C(n)=a_1C(n-1)+a_2C(n-2)+\cdots+a_kC(n-k)+f(n)
$$

La solución no homogénea suele escribirse como:

$$
C(n)=C_h(n)+C_p(n)
$$

donde $C_h(n)$ es la solución homogénea y $C_p(n)$ una solución particular.

### Coeficientes constantes y variables

Cuando los coeficientes $a_i$ no dependen de $n$, la relación tiene coeficientes constantes. Si alguno cambia con el tamaño de entrada, se requieren técnicas adicionales que quedan fuera del catálogo principal de la simulación.

---

## 5.3 Recurrencias en el análisis de algoritmos

La estructura de una recurrencia depende de la transformación aplicada al tamaño de entrada.

| Tipo | Forma | Interpretación | Ejemplo típico |
|---|---|---|---|
| Reducción | $C(n)=\sum_{i=1}^{m}a_iC(n-b_i)+f(n)$ | Cada llamada resta una cantidad fija al tamaño. | Fibonacci y recurrencias lineales |
| División | $C(n)=aC(n/b)+f(n)$ | Cada llamada divide el tamaño por un factor constante. | Búsqueda binaria y merge sort |
| División con factores distintos | $C(n)=\sum_{i=1}^{m}a_iC(b_i n)+f(n)$, con $0<b_i<1$ | Los términos generan subproblemas de tamaños diferentes. | Divide y vencerás no uniforme |

Los parámetros representan:

- $m$: cantidad de términos recursivos diferentes;
- $a_i$: cantidad o ponderación de llamadas asociadas al término $i$;
- $b_i$: desplazamiento en una reducción o fracción del tamaño en una división;
- $f(n)$: costo adicional realizado fuera de las llamadas;
- $h$: profundidad del árbol que se desea observar.

Para $f(n)$ se exige la forma compatible con el método elegido. En el teorema maestro básico y extendido, el costo debe tener crecimiento polinómico o polinómico-logarítmico. Las funciones $2^n$ y $n!$ no pertenecen a esas formas.

---

## 5.4 Métodos de solución

### 5.4.1 Sustitución iterativa

La sustitución iterativa expande repetidamente el término recursivo hasta reconocer un patrón. Para una relación con un único término:

$$
C(n)=2C(n/2)+n,\qquad C(1)=1
$$

las primeras expansiones conducen a:

$$
C(n)=2^kC\left(\frac{n}{2^k}\right)+kn
$$

El caso base se alcanza cuando $n/2^k=1$, por lo que $k=\log_2(n)$. Entonces:

$$
C(n)=n+n\log_2(n)\in\Theta(n\log_2(n))
$$

En la simulación, este método se limita a $m=1$ porque desarrolla una sola transformación recursiva en cada sustitución.

### 5.4.2 Árbol de recurrencia

El árbol representa cada llamada mediante un nodo y cada llamada generada mediante una rama. El análisis sigue cuatro cantidades:

1. el argumento de los nodos en el nivel $k$;
2. el costo individual $f_k(n)$;
3. el número de nodos del nivel;
4. la suma de los costos desde la raíz hasta las hojas.

En una relación uniforme con $a$ hijos por nodo, el nivel $k$ contiene $a^k$ nodos. Para una división por $b$, la altura satisface normalmente $h=\log_b(n)$.

El notebook permite avanzar nivel por nivel, seleccionar filas de la tabla y relacionar cada costo con los nodos correspondientes. El método de solución usa $m=1$ para conservar un único argumento y un costo común por nivel.

### 5.4.3 Teorema maestro

El teorema maestro obtiene una clasificación asintótica para relaciones de división. La simulación ofrece tres versiones.

#### Versión básica

Aplica a relaciones de la forma:

$$
C(n)=aC(n/b)+\Theta(n^k)
$$

| Comparación | Interpretación | Resultado |
|---|---|---|
| $a>b^k$ | Domina la recursión. | $\Theta(n^{\log_b(a)})$ |
| $a=b^k$ | Ambos costos tienen el mismo orden. | $\Theta(n^k\log_b(n))$ |
| $a<b^k$ | Domina el costo externo. | $\Theta(n^k)$, bajo la condición de regularidad correspondiente |

#### Versión extendida

Admite costos de la forma:

$$
f(n)\in\Theta\left(n^k\log_\ell^p(n)\right)
$$

El resultado depende de la comparación entre $a$ y $b^k$ y del exponente $p$. La simulación conserva la base $\ell$ seleccionada al presentar el costo y su resultado.

#### Versión generalizada: Akra–Bazzi

Admite varios tamaños de subproblema:

$$
C(n)=\sum_{i=1}^{m}a_iC(b_i n)+f(n),
\qquad 0<b_i<1
$$

Primero se determina el valor $q$ que satisface:

$$
\sum_{i=1}^{m}a_i b_i^q=1
$$

Después se utiliza:

$$
C(n)\in\Theta\left(
n^q\left(1+\int_1^n\frac{f(u)}{u^{q+1}}\,du\right)
\right)
$$

Aquí se usa $q$ para distinguir el exponente de Akra–Bazzi del parámetro $p$ de $\log_\ell^p(n)$.

#### Funciones no admitidas

El selector del teorema maestro excluye:

- $f(n)=0$;
- $f(n)=2^n$;
- $f(n)=n!$.

Las dos últimas crecen más rápido que cualquier cota superior polinómica y no tienen la forma requerida por las versiones implementadas. Cuando se utilizan otros métodos, permanecen disponibles para explorar el árbol o las expansiones compatibles.

### 5.4.4 Ecuación característica

La ecuación característica se utiliza en relaciones lineales de reducción con coeficientes constantes:

$$
C(n)=\sum_{i=1}^{m}a_iC(n-b_i)+f(n)
$$

El procedimiento separa la parte homogénea, propone $C_h(n)=r^n$ y construye un polinomio cuyas raíces determinan la forma de $C_h(n)$. Si $f(n)\neq 0$, se añade una solución particular compatible con la función externa y se emplean los casos base para calcular las constantes.

La simulación admite varios retardos enteros $b_i$ y verifica la solución obtenida mediante el residuo de la relación.

---

## 5.5 Cómo elegir el método

| Método | Relación compatible | Cantidad de términos | Resultado principal |
|---|---|:---:|---|
| Sustitución iterativa | Reducción o división con patrón analítico | $m=1$ | Expansión y, cuando existe, expresión cerrada |
| Árbol de recurrencia | Reducción o división uniforme | $m=1$ | Costo por nivel, suma total y orden asintótico |
| Maestro básico | División con costo polinómico | $m=1$ | Orden asintótico |
| Maestro extendido | División con costo polinómico-logarítmico | $m=1$ | Orden asintótico |
| Akra–Bazzi | División con factores $b_i$ distintos | $m\geq1$ | Orden asintótico mediante una integral |
| Ecuación característica | Reducción lineal con retardos enteros | $m\geq1$ | Solución homogénea, particular y completa |

La selección de un método debe hacerse a partir de la estructura de la relación, no del resultado que se espera obtener. Si las condiciones del método no se cumplen, la simulación lo indica y evita configuraciones incompatibles.

---

## Errores comunes

### Confundir $C(n/b)$ con $C(bn)$

Ambas expresiones pueden representar la misma fracción cuando $b$ se redefine, pero sus condiciones son distintas. En $C(n/b)$ se requiere $b>1$; en $C(b_i n)$ se requiere $0<b_i<1$.

### Interpretar $a_i$ como el tamaño del subproblema

$a_i$ determina la cantidad o ponderación de llamadas. El cambio del argumento está determinado por $b_i$.

### Olvidar el caso base

La relación por sí sola no determina una solución única. Las condiciones iniciales fijan las constantes y el punto donde termina la expansión.

### Aplicar el teorema maestro a cualquier $f(n)$

Las funciones exponenciales y factoriales no satisfacen la forma polinómica o polinómica-logarítmica requerida por las versiones estudiadas.

### Confundir solución exacta con orden asintótico

Una expresión cerrada conserva constantes y términos de menor orden. Una expresión $\Theta$ describe únicamente el crecimiento dominante.

### Suponer que la base del logaritmo cambia la familia asintótica

Las bases constantes mayores que uno difieren por un factor constante. Por ello pertenecen a la misma familia $\Theta$, aunque la simulación conserve $\ell$ para mantener coherencia con la función seleccionada.

---

## 5.6 Ejercicios propuestos

Los ejercicios permiten practicar:

- formulación de recurrencias a partir de algoritmos;
- expansión por sustitución;
- construcción de árboles;
- aplicación de las tres versiones del teorema maestro;
- resolución mediante ecuaciones características;
- verificación de expresiones exactas y asintóticas.

[Abrir los ejercicios propuestos en el visor en línea](https://docs.google.com/gview?embedded=true&url=https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main/capitulo5/ejercicios_propuestos.pdf)

[Descargar el PDF desde el repositorio](./ejercicios_propuestos.pdf)

---

## Comandos LaTeX

```latex
\newcommand{\colabArbolesRecursion}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo5/0_arboles_recursion.ipynb}
\newcommand{\colabMetodosSolucionRecurrencias}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo5/1_metodos_solucion_relaciones_recurrencia.ipynb}
\newcommand{\visorEjerciciosCapituloCinco}{https://docs.google.com/gview?embedded=true\&url=https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main/capitulo5/ejercicios_propuestos.pdf}
```

---

## Estructura de archivos

```text
capitulo5/
├── README.md
├── colab_bootstrap.py
├── recursion_tree_animation.py
├── recurrence_solution_methods.py
├── 0_arboles_recursion.ipynb
├── 1_metodos_solucion_relaciones_recurrencia.ipynb
└── ejercicios_propuestos.pdf
```

---

## Licencia

El contenido de este capítulo se distribuye bajo la licencia **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. Se autoriza su uso con fines académicos citando la fuente original.
