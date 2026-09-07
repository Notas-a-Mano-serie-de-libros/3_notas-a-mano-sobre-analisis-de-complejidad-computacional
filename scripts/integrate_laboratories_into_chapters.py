"""Integra el desarrollo de los laboratorios en la lectura continua del capítulo."""

from __future__ import annotations

import re
import shutil
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

LABS: dict[int, list[tuple[str, str]]] = {
    2: [
        ("2.1.2.1 Complejidad constante", "1-complejidad-constante"),
        ("2.1.2.2 Complejidad logarítmica", "2-complejidad-logaritmica"),
        ("2.1.2.3 Complejidad lineal", "3-complejidad-lineal"),
        ("2.1.2.4 Complejidad log-lineal", "4-complejidad-log-lineal"),
        ("2.1.2.5 Complejidad cuadrática", "5-complejidad-cuadratica"),
        ("2.1.2.6 Complejidad cúbica", "6-complejidad-cubica"),
        ("2.1.2.7 Complejidad polinomial general", "7-complejidad-polinomial-general"),
        ("2.1.2.8 Complejidad exponencial", "8-complejidad-exponencial"),
        ("2.1.2.9 Complejidad factorial", "9-complejidad-factorial"),
    ],
    3: [
        ("3.2 Comparación de las notaciones", "0-comparacion-notaciones-asintoticas"),
        ("3.5.1 Notación O", "1-notacion-big-o"),
        ("3.5.2 Notación o", "2-notacion-little-o"),
        ("3.5.3 Notación Ω", "3-notacion-big-omega"),
        ("3.5.4 Notación ω", "4-notacion-little-omega"),
        ("3.5.5 Notación Θ", "5-notacion-theta"),
        ("3.6 Ejemplos concretos", "ejemplos-concretos-notaciones"),
        ("Representación general", "notacion-asintotica-representacion-generica"),
    ],
    4: [
        ("4.4.4.1 Sumar dos números", "ejemplo1-sumar-numeros"),
        ("4.4.4.2 Imprimir los elementos de un arreglo", "ejemplo2-imprimir-elementos-arreglo"),
        ("4.4.4.3 Imprimir los elementos de una matriz", "ejemplo3-imprimir-elementos-matriz"),
        ("4.4.4.4 Inicializar una matriz variable", "ejemplo4-inicializar-matriz-variable"),
        ("4.4.4.5 Ciclos con incremento no lineal", "ejemplo5-ciclos-incremento-no-lineal"),
        ("4.4.4.7 Ciclo sin dependencia de la entrada", "ejemplo7-ciclo-sin-dependencia"),
        ("4.4.4.9 Complejidad oculta", "ejemplo9-complejidad-oculta"),
    ],
    5: [
        ("5.4 Formas de las relaciones de recurrencia", "0-arboles-recursion"),
        ("5.5 Métodos de solución", "1-metodos-solucion-relaciones-recurrencia"),
    ],
    6: [("6.2–6.3 Análisis de algoritmos recursivos", "0-laboratorio-analisis-recursivo")],
    7: [
        ("7.1 Comparación general", "0-comparacion-busquedas"),
        ("7.2 Búsqueda secuencial", "1-busqueda-secuencial"),
        ("7.3 Búsqueda binaria", "2-busqueda-binaria"),
        ("7.4 Búsqueda por interpolación", "3-busqueda-interpolacion"),
        ("7.5 Búsqueda por saltos", "4-busqueda-saltos"),
        ("7.6 Búsqueda exponencial", "5-busqueda-exponencial"),
        ("7.7 Búsqueda ternaria", "6-busqueda-ternaria"),
        ("7.9 Ejercicios propuestos", "ejercicios-propuestos"),
    ],
    8: [
        ("8.1 Comparación general", "0-comparacion-ordenamientos"),
        ("8.2 Ordenamiento burbuja", "1-ordenamiento-burbuja"),
        ("8.3 Ordenamiento por selección", "2-ordenamiento-seleccion"),
        ("8.4 Ordenamiento por inserción", "3-ordenamiento-insercion"),
        ("Ampliación · Ordenamiento Shell", "4-ordenamiento-shell"),
        ("8.5 Ordenamiento por mezcla", "5-ordenamiento-mezcla"),
        ("8.6 Ordenamiento rápido", "6-ordenamiento-rapido"),
        ("8.7 Ordenamiento radix", "7-ordenamiento-radix"),
        ("8.9 Ejercicios propuestos", "ejercicios-propuestos"),
    ],
}

# Figuras que forman parte de las explicaciones y deben quedar disponibles en
# GitHub Pages. Las rutas conservan su estructura para evitar colisiones entre
# archivos con nombres parecidos y para que sea fácil rastrear su origen.
PAGE_FIGURES: dict[tuple[int, str], tuple[str, ...]] = {
    (2, "1-complejidad-constante"): ("complejidad_temporal/complejidad_constante.png",),
    (2, "2-complejidad-logaritmica"): ("complejidad_temporal/complejidad_logaritmica.png",),
    (2, "3-complejidad-lineal"): ("complejidad_temporal/complejidad_lineal.png",),
    (2, "4-complejidad-log-lineal"): ("complejidad_temporal/complejidad_log_lineal.png",),
    (2, "5-complejidad-cuadratica"): ("complejidad_temporal/complejidad_cuadratica.png",),
    (2, "6-complejidad-cubica"): ("complejidad_temporal/complejidad_cubica.png",),
    (2, "7-complejidad-polinomial-general"): (
        "complejidad_temporal/complejidad_teorica_polinomica1.png",
        "complejidad_temporal/complejidad_teorica_polinomica2.png",
    ),
    (2, "8-complejidad-exponencial"): (
        "complejidad_temporal/complejidad_exponencial.png",
        "analisis_eficiencia/complejidad_temporal/complejidad_exponencial_1.png",
        "analisis_eficiencia/complejidad_temporal/complejidad_exponencial_2.png",
        "analisis_eficiencia/complejidad_espacial/complejidad_exponencial_1.png",
        "analisis_eficiencia/complejidad_espacial/complejidad_exponencial_2.png",
    ),
    (2, "9-complejidad-factorial"): (
        "complejidad_temporal/complejidad_factorial.png",
        "analisis_eficiencia/complejidad_temporal/complejidad_factorial_1.png",
        "analisis_eficiencia/complejidad_temporal/complejidad_factorial_2.png",
        "analisis_eficiencia/complejidad_espacial/complejidad_factorial_1.png",
        "analisis_eficiencia/complejidad_espacial/complejidad_factorial_2.png",
    ),
    (3, "1-notacion-big-o"): ("comparacion_big_O.png", "comparacion_big_O_2.png"),
    (3, "2-notacion-little-o"): ("comparacion_little_o.png", "comparacion_little_o2.png"),
    (3, "3-notacion-big-omega"): ("comparacion_big_omega.png", "comparacion_big_omega_2.png"),
    (3, "4-notacion-little-omega"): ("comparacion_little_omega.png", "comparacion_little_omega_2.png"),
    (3, "5-notacion-theta"): ("comparacion_big_theta.png", "comparacion_big_theta_2.png"),
    (3, "notacion-asintotica-representacion-generica"): (
        "comparacion_o_generica.png",
        "comparacion_omega_generica.png",
        "comparacion_theta_generica.png",
    ),
    (4, "ejemplo1-sumar-numeros"): (
        "ejemplos/ejemplo_suma_dos_numeros_tiempo.png",
        "ejemplos/ejemplo_suma_dos_numeros_espacio.png",
    ),
    (4, "ejemplo2-imprimir-elementos-arreglo"): (
        "ejemplos/ejemplo_imprimir_elementos_tiempo.png",
        "ejemplos/ejemplo_imprimir_elementos_espacio.png",
    ),
    (4, "ejemplo3-imprimir-elementos-matriz"): (
        "ejemplos/ejemplo_imprimir_matriz_tiempo.png",
        "ejemplos/ejemplo_imprimir_matriz_espacio.png",
    ),
    (4, "ejemplo4-inicializar-matriz-variable"): (
        "ejemplos/ejemplo_inicializar_matriz_tiempo.png",
        "ejemplos/ejemplo_inicializar_matriz_espacio.png",
    ),
    (4, "ejemplo5-ciclos-incremento-no-lineal"): (
        "ejemplos/recorrer_matriz_vacia_tiempo.png",
        "ejemplos/recorrer_matriz_vacia_espacio.png",
    ),
    (4, "ejemplo7-ciclo-sin-dependencia"): (
        "ejemplos/ciclo_sin_dependencia_tiempo.png",
        "ejemplos/ciclo_sin_dependencia_espacio.png",
    ),
    (6, "factorial"): (
        "ejemplos/arbol_recursion_factorial.png",
        "ejemplos/comparacion_complejidad_for.png",
    ),
    (6, "fibonacci"): (
        "ejemplos/arbol_recurrencia_fibonacci_general.png",
        "ejemplos/comparacion_complejidad_exponencial.png",
    ),
    (6, "potencia"): (
        "ejemplos/arbol_recursion_potencia.png",
        "ejemplos/comparacion_teorema_maestro_potencia.png",
    ),
    (6, "merge-sort"): (
        "ejemplos/arbol_recursion_mezcla.png",
        "ejemplos/arbol_recursion_mecla_2.png",
    ),
    (6, "arbol-binario"): (
        "ejemplos/complejidad_binario.png",
        "ejemplos/comparacion_complejidad_binario_1.png",
        "ejemplos/comparacion_complejidad_binario_2.png",
    ),
    (7, "1-busqueda-secuencial"): (
        "busqueda_lineal/busqueda_lineal_ejemplo.png",
        "busqueda_lineal/busqueda_lineal_ejemplo_mejor_caso.png",
        "busqueda_lineal/busqueda_lineal_ejemplo_caso_promedio.png",
        "busqueda_lineal/busqueda_lineal_ejemplo_peor_caso_2.png",
    ),
    (7, "2-busqueda-binaria"): (
        "busqueda_binaria/busqueda_binaria_ejemplo_1.png",
        "busqueda_binaria/busqueda_binaria_ejemplo_2.png",
        "busqueda_binaria/busqueda_binaria_ejemplo_3.png",
        "busqueda_binaria/busqueda_binaria_ejemplo_caso_promedio_2.png",
    ),
    (7, "3-busqueda-interpolacion"): (
        "busqueda_interpolacion/busqueda_interpolacion.png",
        "busqueda_interpolacion/interpolacion_promedio.png",
        "busqueda_interpolacion/interpolacion_ajuste.png",
        "busqueda_interpolacion/busqueda_interpolacion_peor_caso_asimetrico.png",
    ),
    (7, "4-busqueda-saltos"): (
        "busqueda_salto/busqueda_salto_1.png",
        "busqueda_salto/busqueda_salto_3.png",
        "busqueda_salto/busqueda_salto_6.png",
        "busqueda_salto/busqueda_salto_promedio_caso_4.png",
    ),
    (7, "5-busqueda-exponencial"): (
        "busqueda_exponencial/busqueda_exponencial_ejemplo_1.png",
        "busqueda_exponencial/busqueda_exponencial_ejemplo_3.png",
        "busqueda_exponencial/busqueda_exponencial_ejemplo_6.png",
        "busqueda_exponencial/busqueda_exponencial_caso_promedio.png",
    ),
    (7, "6-busqueda-ternaria"): (
        "busqueda_ternaria/busqueda_ternaria_ejemplo_1.png",
        "busqueda_ternaria/busqueda_ternaria_ejemplo_2.png",
        "busqueda_ternaria/busqueda_ternaria_ejemplo_4.png",
        "busqueda_ternaria/busqueda_ternaria_caso_promedio_3.png",
    ),
    (8, "1-ordenamiento-burbuja"): tuple(
        f"ordenamiento_burbuja/ordenamiento_burbuja_{step}.png" for step in (1, 4, 7, 11)
    ),
    (8, "2-ordenamiento-seleccion"): tuple(
        f"ordenamiento_seleccion/ordenamiento_seleccion_{step}.png" for step in (1, 4, 7, 11)
    ),
    (8, "3-ordenamiento-insercion"): tuple(
        f"ordenamiento_insercion/ordenamiento_insercion_{step}.png" for step in (1, 4, 7, 11)
    ),
    (8, "5-ordenamiento-mezcla"): tuple(
        f"ordenamiento_mezcla/ordenamiento_mezcla_{step}.png" for step in (1, 7, 13, 20)
    ),
    (8, "6-ordenamiento-rapido"): tuple(
        f"ordenamiento_rapido/ordenamiento_rapido_{step}.png" for step in (1, 4, 7, 11)
    ),
}

INTRO = {  # Las cadenas son raw para conservar los delimitadores de MathJax.
    2: r"""## 2.1 Funciones de complejidad

Una función de complejidad relaciona el tamaño de entrada \(n\) con los recursos consumidos. El tiempo se representa mediante \(T(n)\) y el espacio mediante \(S(n)\). Estas funciones modelan crecimiento: no son segundos o bytes universales, pues la ejecución concreta depende de la máquina, el lenguaje y la implementación.

### 2.1.1 Propiedades básicas

El dominio contiene tamaños de entrada válidos y el costo es no negativo. La monotonía permite estudiar cómo cambia el consumo al aumentar \(n\). En el análisis se identifican la operación básica, la frecuencia con que se ejecuta y la memoria que permanece activa; después se separa el término dominante de constantes y términos menores.

### 2.1.2 Familias de crecimiento

Las familias corresponden a estructuras de ejecución distintas. \(O(1)\) no depende de \(n\); \(O(\log_2(n))\) reduce el problema por factores; \(O(n)\) recorre la entrada; \(O(n\log_2(n))\) combina niveles logarítmicos con trabajo lineal; y \(O(n^k)\) suele aparecer en recorridos anidados. Los crecimientos \(O(2^n)\) y \(O(n!)\) enumeran combinaciones o permutaciones y dejan de ser prácticos rápidamente.

Esta página establece el marco teórico. Cada sección hija realiza el análisis experimental de una familia: identifica un algoritmo representativo, presenta sus implementaciones, formula tiempo y espacio y enlaza la simulación con la que se contrasta la curva.
""",
    3: r"""## 3.1 Contexto y propósito

La notación asintótica compara tasas de crecimiento cuando \(n\) tiende a infinito. Su utilidad consiste en abstraer constantes de implementación sin perder la relación formal entre una función de costo \(C(n)\) y una función de referencia \(g(n)\). Las cotas pueden ser superiores, inferiores, ajustadas o estrictas; por eso los cinco símbolos no son intercambiables.
""",
    4: r"""## 4.1–4.4 Del algoritmo estructurado a su función de costo

El análisis comienza definiendo qué representa \(n\), qué escenario se estudia y qué operaciones dependen de la entrada. Las secuencias suman costos, los condicionales seleccionan recorridos y los ciclos multiplican el costo de su cuerpo por la cantidad real de iteraciones. En ciclos anidados debe establecerse si los límites son independientes o dependen unos de otros. Tiempo y espacio se derivan por separado y solo después se simplifican asintóticamente.

### Procedimiento para calcular la complejidad temporal

1. Defina el tamaño de entrada y el escenario: mejor, promedio o peor caso.
2. Elija una operación básica cuyo número de ejecuciones dependa de la entrada.
3. Sume los costos de las secuencias y construya una función para cada rama condicional.
4. Determine las iteraciones reales de cada ciclo; en ciclos anidados, escriba las sumas antes de inferir el orden.
5. Sustituya el costo de las funciones llamadas y simplifique únicamente al final mediante dominancia.

### Procedimiento para calcular la complejidad espacial

1. Separe la memoria de entrada de la memoria auxiliar creada por el algoritmo.
2. Cuente variables, estructuras dinámicas y copias temporales activas simultáneamente.
3. Relacione cada dimensión de las estructuras con el tamaño de entrada.
4. Exprese \(S(n)\) y conserve su término dominante. El espacio no se obtiene copiando la complejidad temporal.

## 4.4.4 Ejemplos desarrollados

Las páginas siguientes aplican este procedimiento a los diez ejemplos de la obra, en el orden código, análisis temporal, análisis espacial y simulación cuando existe un laboratorio asociado.
""",
    5: """## 5.1–5.3 Sucesiones y recurrencias

Una recurrencia define un término mediante valores anteriores. Puede ser lineal o no lineal, homogénea o no homogénea, y usar coeficientes constantes o variables. En análisis de algoritmos, la relación debe reflejar cuántas llamadas se generan, cómo cambia el tamaño del subproblema y cuánto trabajo se hace fuera de ellas. Clasificarla antes de resolverla evita aplicar un teorema fuera de sus condiciones.
""",
    6: r"""## 6.1 Estructura de una solución recursiva

Toda función recursiva necesita un caso base y una transformación que acerque cada llamada a ese caso. El seguimiento distingue tres momentos: apilamiento de llamadas, resolución del caso base y retorno de resultados. El tiempo cuenta todo el trabajo ejecutado; el espacio cuenta la máxima cantidad de marcos activos simultáneamente, no el total histórico de llamadas.

### Procedimiento para calcular el tiempo

1. Identifique el caso base y su costo.
2. Cuente las llamadas de un caso no base y el tamaño recibido por cada una.
3. Calcule el trabajo local realizado fuera de las llamadas.
4. Escriba \(T(n)\), resuélvala con un método compatible y compruebe el resultado.

### Procedimiento para calcular el espacio

1. Determine la memoria local de un marco de llamada.
2. Calcule la profundidad máxima de llamadas activas, no la cantidad total de nodos del árbol.
3. Añada estructuras auxiliares que sobrevivan mientras se resuelven los subproblemas.
4. Exprese la altura en función de \(n\) y simplifique \(S(n)\).

Las secciones siguientes aplican el procedimiento a factorial, Fibonacci, potencia, Merge Sort y búsqueda en árbol binario, siempre en el orden código, análisis y simulación.
""",
    7: """## Cómo leer este capítulo

Los algoritmos de búsqueda se comparan a partir de sus precondiciones, la forma en que descartan candidatos, sus casos mejor, promedio y peor, y la memoria adicional que requieren. Cada sección desarrolla el procedimiento y su análisis antes de ofrecer la simulación correspondiente.
""",
    8: """## Cómo leer este capítulo

Un ordenamiento no se elige únicamente por su tiempo asintótico. También importan estabilidad, memoria auxiliar, comportamiento ante datos casi ordenados, número de movimientos y restricciones sobre las claves. Cada sección presenta el mecanismo, sus invariantes, sus costos por escenario y el experimento ejecutable.
""",
}

ASYMPTOTIC_EXAMPLES = r"""En todos los ejemplos se analiza la misma función:

\[
C(n)=n^3+2n^2+n+5.
\]

El propósito es mostrar que la función de referencia cambia según la relación que se quiere demostrar. No basta con observar que ambas curvas parecen próximas: deben exhibirse constantes y un umbral, o calcular el límite correspondiente.

### Ejemplo 1 · Cota superior \(O(n^3)\)

Se toma \(g(n)=n^3\). Para \(n\geq 1\), se cumplen \(n^2\leq n^3\), \(n\leq n^3\) y \(1\leq n^3\). Por tanto:

\[
C(n)\leq n^3+2n^3+n^3+5n^3=9n^3.
\]

Al elegir \(c=9\) y \(n_0=1\), queda demostrada la desigualdad \(C(n)\leq c\,g(n)\) para todo \(n\geq n_0\). En consecuencia, \(C(n)\in O(n^3)\). El valor de \(c\) no tiene que ser mínimo: cualquier constante válida prueba la cota.

### Ejemplo 2 · Cota superior estricta \(o(n^4)\)

Ahora se compara con \(g(n)=n^4\). La relación es estricta porque:

\[
\lim_{n\to\infty}\frac{C(n)}{n^4}
=\lim_{n\to\infty}\left(\frac1n+\frac2{n^2}+\frac1{n^3}+\frac5{n^4}\right)=0.
\]

El límite cero significa que, para cualquier constante \(c>0\), existe un umbral \(n_0\) a partir del cual \(C(n)<c n^4\). Por eso \(C(n)\in o(n^4)\). Esta afirmación es más fuerte que decir solamente \(C(n)\in O(n^4)\).

### Ejemplo 3 · Cota inferior \(\Omega(n^3)\)

Como todos los términos adicionales son no negativos para \(n\geq1\):

\[
C(n)=n^3+2n^2+n+5\geq n^3.
\]

Con \(c=1\) y \(n_0=1\) se satisface \(C(n)\geq c\,g(n)\). Así, \(C(n)\in\Omega(n^3)\). Esta cota garantiza que el crecimiento de \(C\) no puede quedar asintóticamente por debajo del cúbico.

### Ejemplo 4 · Cota inferior estricta \(\omega(n^2)\)

Al usar \(g(n)=n^2\), el cociente es:

\[
\frac{C(n)}{n^2}=n+2+\frac1n+\frac5{n^2}.
\]

Como este cociente tiende a infinito, para cualquier \(c>0\) se puede encontrar un \(n_0\) tal que \(C(n)>c n^2\) cuando \(n\geq n_0\). En consecuencia, \(C(n)\in\omega(n^2)\).

### Ejemplo 5 · Cota ajustada \(\Theta(n^3)\)

Las pruebas de los ejemplos 1 y 3 pueden combinarse:

\[
n^3\leq C(n)\leq9n^3,\qquad n\geq1.
\]

Con \(c_1=1\), \(c_2=9\) y \(n_0=1\), la función queda encerrada entre dos múltiplos positivos de \(n^3\). Por ello, \(C(n)\in\Theta(n^3)\). Esta es la clasificación ajustada: \(n^3\) es simultáneamente cota superior e inferior del mismo orden.

### Qué debe observarse en la simulación

Las vistas lineal y logarítmica cambian la apariencia de las curvas, pero no la relación formal. El laboratorio permite observar el umbral \(n_0\), modificar las constantes y comprobar en qué región se mantiene cada desigualdad. Una gráfica ilustra la prueba; no la reemplaza."""

RECURSIVE_EXAMPLES = r"""La metodología se aplica por separado a cada algoritmo. En todos los casos se identifica el caso base, la reducción del argumento, el trabajo local y la profundidad máxima de la pila.

### Ejemplo 1 · Factorial recursivo

#### Código

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

#### Análisis

Cada llamada reduce \(n\) en una unidad y realiza una multiplicación adicional:

\[
T(n)=T(n-1)+\Theta(1),\qquad T(1)=\Theta(1).
\]

Después de \(n-1\) expansiones se alcanza el caso base, de modo que \(T(n)\in\Theta(n)\). Las llamadas pendientes forman una cadena de profundidad \(n\), por lo que \(S(n)\in\Theta(n)\).

#### Simulación

El recorrido muestra cómo se apilan los valores \(n,n-1,\ldots,1\) y cómo los productos se resuelven durante el retorno.

### Ejemplo 2 · Fibonacci recursivo ingenuo

#### Código

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

#### Análisis

Cada llamada no base genera dos subproblemas parcialmente superpuestos:

\[
T(n)=T(n-1)+T(n-2)+\Theta(1)\in\Theta(\varphi^n).
\]

El árbol contiene una cantidad exponencial de llamadas por la repetición de resultados. Sin embargo, sus dos ramas no permanecen completas a la vez: la profundidad máxima es lineal, así que \(S(n)\in\Theta(n)\).

#### Simulación

La animación hace visible la ramificación y permite reconocer llamadas repetidas, como \(F(n-2)\), que motivan técnicas posteriores como memoización.

### Ejemplo 3 · Potencia recursiva simple

#### Código

```python
def potencia(x, n):
    if n == 0:
        return 1
    return x * potencia(x, n - 1)
```

#### Análisis

La recurrencia \(T(n)=T(n-1)+\Theta(1)\) tiene \(n\) niveles. Tanto el tiempo como la pila crecen linealmente: \(T(n),S(n)\in\Theta(n)\).

#### Simulación

El laboratorio permite seguir la cadena descendente del exponente y el producto acumulado durante los retornos.

### Ejemplo 4 · Exponenciación rápida

#### Código

```python
def potencia_rapida(x, n):
    if n == 0:
        return 1
    mitad = potencia_rapida(x, n // 2)
    if n % 2:
        return mitad * mitad * x
    return mitad * mitad
```

#### Análisis

El resultado recursivo se calcula una sola vez y se reutiliza. Como el exponente se divide entre dos:

\[
T(n)=T(\lfloor n/2\rfloor)+\Theta(1)\in\Theta(\log_2(n)).
\]

La profundidad de llamadas sigue la misma cantidad de divisiones, de modo que \(S(n)\in\Theta(\log_2(n))\). Llamar dos veces a `potencia_rapida(x, n // 2)` cambiaría radicalmente el árbol y desperdiciaría el resultado compartido.

#### Simulación

La animación contrasta la reducción lineal de la potencia simple con la reducción por mitades. El panel experimental amplía la comparación a factorial, Fibonacci, Merge Sort y búsqueda en árbol binario, mostrando tiempo, memoria y función teórica ajustada."""

CHAPTER6_ADDITIONAL = r"""

### Ejemplo 4 · Ordenamiento por mezcla

#### Código

```python
def merge_sort(a):
    if len(a) <= 1:
        return a
    m = len(a) // 2
    return combinar(merge_sort(a[:m]), merge_sort(a[m:]))
```

#### Análisis

La división genera dos subproblemas de tamaño \(n/2\) y la combinación recorre los \(n\) elementos. Por tanto, \(T(n)=2T(n/2)+\Theta(n)\in\Theta(n\log_2(n))\). Los arreglos auxiliares de combinación requieren \(\Theta(n)\) memoria; la pila añade \(\Theta(\log_2(n))\), que queda dominada por el almacenamiento lineal.

#### Simulación

La vista experimental muestra las divisiones, el retorno de cada mitad y la combinación ordenada por niveles.

### Ejemplo 5 · Búsqueda en árbol binario

#### Código

```python
def buscar(raiz, valor):
    if raiz is None:
        return False
    if raiz.valor == valor:
        return True
    return buscar(raiz.izquierdo, valor) or buscar(raiz.derecho, valor)
```

#### Análisis

El mejor caso encuentra el valor en la raíz: \(\Omega(1)\). En un árbol balanceado, una búsqueda guiada por orden alcanza una profundidad \(\Theta(\log_2(n))\); en un árbol degenerado puede recorrer \(O(n)\) nodos. La memoria de la versión recursiva depende de la altura \(h\): \(S(n)\in\Theta(h)\).

#### Simulación

El laboratorio contrasta árboles balanceados y degenerados para relacionar cantidad de nodos, altura y profundidad de la pila."""

CHAPTER4_CODE = {
    "ejemplo1-sumar-numeros": {
        "Pseudocódigo": "función sumar(a, b)\n    retornar a + b",
        "Python": "def sumar(a, b):\n    return a + b",
        "Java": "static double sumar(double a, double b) {\n    return a + b;\n}",
        "C": "double sumar(double a, double b) {\n    return a + b;\n}",
    },
    "ejemplo2-imprimir-elementos-arreglo": {
        "Pseudocódigo": "procedimiento recorrer(arreglo)\n    para cada elemento en arreglo\n        visitar elemento",
        "Python": "def imprimir_elementos(arr):\n    for elemento in arr:\n        _ = elemento",
        "Java": "static void recorrer(int[] arreglo) {\n    for (int elemento : arreglo) {\n        int visitado = elemento;\n    }\n}",
        "C": "void recorrer(const int arreglo[], int n) {\n    for (int i = 0; i < n; i++) {\n        int visitado = arreglo[i];\n    }\n}",
    },
    "ejemplo3-imprimir-elementos-matriz": {
        "Pseudocódigo": "procedimiento recorrerMatriz(matriz)\n    para cada fila en matriz\n        para cada elemento en fila\n            visitar elemento",
        "Python": "def imprimir_matriz(matriz):\n    for fila in matriz:\n        for elemento in fila:\n            _ = elemento",
        "Java": "static void recorrerMatriz(int[][] matriz) {\n    for (int[] fila : matriz) {\n        for (int elemento : fila) {\n            int visitado = elemento;\n        }\n    }\n}",
        "C": "void recorrerMatriz(int filas, int columnas, int matriz[filas][columnas]) {\n    for (int i = 0; i < filas; i++) {\n        for (int j = 0; j < columnas; j++) {\n            int visitado = matriz[i][j];\n        }\n    }\n}",
    },
    "ejemplo4-inicializar-matriz-variable": {
        "Pseudocódigo": "procedimiento crearYRecorrer(n)\n    matriz ← nueva matriz n × n inicializada en 0\n    para cada fila en matriz\n        para cada elemento en fila\n            visitar elemento",
        "Python": "def imprimir_matriz_creada(n):\n    matriz = [[0 for _ in range(n)] for _ in range(n)]\n    for fila in matriz:\n        for elemento in fila:\n            _ = elemento",
        "Java": "static void crearYRecorrer(int n) {\n    int[][] matriz = new int[n][n];\n    for (int[] fila : matriz) {\n        for (int elemento : fila) {\n            int visitado = elemento;\n        }\n    }\n}",
        "C": "void crearYRecorrer(int n) {\n    int (*matriz)[n] = calloc(n, sizeof *matriz);\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) {\n            int visitado = matriz[i][j];\n        }\n    free(matriz);\n}",
    },
    "ejemplo5-ciclos-incremento-no-lineal": {
        "Pseudocódigo": "procedimiento recorrerConSaltos(n)\n    matriz ← nueva matriz n × n\n    para i ← 0 hasta n - 1\n        para j ← 0 hasta n - 1 con paso 2\n            visitar matriz[i][j]",
        "Python": "def recorrer_matriz_vacia(n):\n    matriz = [[0 for _ in range(n)] for _ in range(n)]\n    for i in range(n):\n        for j in range(0, n, 2):\n            _ = matriz[i][j]",
        "Java": "static void recorrerConSaltos(int n) {\n    int[][] matriz = new int[n][n];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j += 2) {\n            int visitado = matriz[i][j];\n        }\n}",
        "C": "void recorrerConSaltos(int n) {\n    int (*matriz)[n] = calloc(n, sizeof *matriz);\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j += 2) {\n            int visitado = matriz[i][j];\n        }\n    free(matriz);\n}",
    },
    "ejemplo7-ciclo-sin-dependencia": {
        "Pseudocódigo": "procedimiento iterar()\n    para i ← 0 hasta 9 999\n        visitar i",
        "Python": "def iterar():\n    for i in range(10_000):\n        _ = i",
        "Java": "static void iterar() {\n    for (int i = 0; i < 10_000; i++) {\n        int visitado = i;\n    }\n}",
        "C": "void iterar(void) {\n    for (int i = 0; i < 10000; i++) {\n        int visitado = i;\n    }\n}",
    },
    "ejemplo9-complejidad-oculta": {
        "Pseudocódigo": "función fibonacciGrande(n)\n    si n ≤ 1 entonces retornar n\n    a ← 0; b ← 1\n    para i ← 2 hasta n\n        (a, b) ← (b, a + b)\n    retornar b",
        "Python": "def fib_big(n):\n    if n <= 1:\n        return n\n    a, b = 0, 1\n    for _ in range(2, n + 1):\n        a, b = b, a + b\n    return b",
        "Java": "static java.math.BigInteger fibGrande(int n) {\n    if (n <= 1) return java.math.BigInteger.valueOf(n);\n    var a = java.math.BigInteger.ZERO;\n    var b = java.math.BigInteger.ONE;\n    for (int i = 2; i <= n; i++) {\n        var siguiente = a.add(b);\n        a = b; b = siguiente;\n    }\n    return b;\n}",
        "C": "/* Para conservar enteros arbitrariamente grandes se usa GMP. */\nvoid fibGrande(unsigned n, mpz_t resultado) {\n    mpz_t a, b, siguiente;\n    mpz_inits(a, b, siguiente, NULL);\n    mpz_set_ui(b, 1);\n    for (unsigned i = 2; i <= n; i++) {\n        mpz_add(siguiente, a, b);\n        mpz_set(a, b); mpz_set(b, siguiente);\n    }\n    mpz_set(resultado, n == 0 ? a : b);\n    mpz_clears(a, b, siguiente, NULL);\n}",
    },
}

CHAPTER4_MISSING = {
    "ejemplo6": {
        "title": "4.4.4.6 Algoritmo con estructura deliberadamente compleja",
        "intro": "Este ejemplo combina un ciclo externo, dos ciclos internos y llamadas a funciones con costos propios. Su propósito es mostrar que la apariencia del anidamiento no basta: cada cuerpo debe sustituirse por su función de costo antes de aplicar dominancia.",
        "code": {
            "Pseudocódigo": "procedimiento imprimirElementos(m, n)\n    para i ← 0 hasta m - 1\n        imprimir i\n        para j ← 0 hasta n - 1\n            imprimir j\n        para k ← n; k > 1; k ← ⌊k / 2⌋\n            imprimir k\n            foo2()\n        foo1()",
            "Python": "def imprimir_elementos(m, n):\n    for i in range(m):\n        print(i)\n        for j in range(n):\n            print(j)\n        k = n\n        while k > 1:\n            print(k)\n            foo2()\n            k //= 2\n        foo1()",
            "Java": "static void imprimirElementos(int m, int n) {\n    for (int i = 0; i < m; i++) {\n        System.out.println(i);\n        for (int j = 0; j < n; j++) System.out.println(j);\n        for (int k = n; k > 1; k /= 2) {\n            System.out.println(k);\n            foo2();\n        }\n        foo1();\n    }\n}",
            "C": "void imprimirElementos(int m, int n) {\n    for (int i = 0; i < m; i++) {\n        printf(\"%d\\n\", i);\n        for (int j = 0; j < n; j++) printf(\"%d\\n\", j);\n        for (int k = n; k > 1; k /= 2) {\n            printf(\"%d\\n\", k);\n            foo2();\n        }\n        foo1();\n    }\n}",
        },
        "analysis": r"El conteo debe conservar los costos de las funciones llamadas. Antes de simplificar, la forma general es \(T(n)\in O\!\left(n\,[n+\log_2(n)(1+T_{foo2}(n))+T_{foo1}(n)]\right)\). Solo después se sustituyen \(T_{foo1}\) y \(T_{foo2}\) y se aplica dominancia. La memoria suma las variables constantes y el costo lineal de `foo2`, por lo que \(S(n)\in O(n)\). La obra no propone simulación para este caso por su crecimiento deliberadamente poco habitual.",
    },
    "ejemplo8": {
        "title": "4.4.4.8 Ciclo con límite fijo y función de costo lineal",
        "intro": "El número de iteraciones es constante, pero la operación ejecutada dentro del ciclo depende de la entrada.",
        "code": {
            "Pseudocódigo": "procedimiento cicloFijo(n)\n    repetir 1 000 veces\n        foo(n)",
            "Python": "def ciclo_fijo(n):\n    for _ in range(1_000):\n        foo(n)",
            "Java": "static void cicloFijo(int n) {\n    for (int i = 0; i < 1_000; i++) foo(n);\n}",
            "C": "void cicloFijo(int n) {\n    for (int i = 0; i < 1000; i++) foo(n);\n}",
        },
        "analysis": r"Si \(T_{foo}(n)=n\), entonces \(T(n)=1000n\in O(n)\). La constante del ciclo se absorbe, pero la dependencia de `foo` no. Si \(S_{foo}(n)=n\), el espacio también queda en \(O(n)\).",
    },
    "ejemplo10": {
        "title": "4.4.4.10 Algoritmo costoso por diseño",
        "intro": "Este ejemplo estudia cómo el orden de evaluación de condiciones modifica los casos observados cuando las funciones tienen costos distintos.",
        "code": {
            "Pseudocódigo": "si h(n) entonces\n    resolver caso frecuente\nsi no, si g(n) entonces\n    resolver segundo caso\nsi no\n    r(n)",
            "Python": "def resolver(n):\n    if h(n):\n        return caso_frecuente(n)\n    if g(n):\n        return segundo_caso(n)\n    return r(n)",
            "Java": "static Resultado resolver(int n) {\n    if (h(n)) return casoFrecuente(n);\n    if (g(n)) return segundoCaso(n);\n    return r(n);\n}",
            "C": "Resultado resolver(int n) {\n    if (h(n)) return casoFrecuente(n);\n    if (g(n)) return segundoCaso(n);\n    return r(n);\n}",
        },
        "analysis": r"Si \(h(n)\in\Theta(\log_2(n))\) es el caso más frecuente, evaluarla antes que \(g(n)\in\Theta(n)\) reduce el caso promedio a \(\Theta(\log_2(n))\). El peor caso continúa incluyendo \(r(n)\in\Theta(2^n)\); reordenar condiciones mejora la ruta habitual, pero no elimina el cuello de botella exponencial.",
    },
}

CHAPTER2_CODE = {
    "1-complejidad-constante": {
        "Pseudocódigo": "función acceder(arreglo, índice)\n    retornar arreglo[índice]",
        "Python": "def acceder_posicion(lista, indice):\n    return lista[indice]",
        "Java": "static int acceder(int[] arreglo, int indice) {\n    return arreglo[indice];\n}",
        "C": "int acceder(const int arreglo[], int indice) {\n    return arreglo[indice];\n}",
    },
    "2-complejidad-logaritmica": {
        "Pseudocódigo": "función búsquedaBinaria(A, objetivo)\n    bajo ← 0; alto ← longitud(A) - 1\n    mientras bajo ≤ alto\n        medio ← ⌊(bajo + alto) / 2⌋\n        si A[medio] = objetivo entonces retornar medio\n        si A[medio] < objetivo entonces bajo ← medio + 1\n        en otro caso alto ← medio - 1\n    retornar -1",
        "Python": "def busqueda_binaria(lista, objetivo):\n    bajo, alto = 0, len(lista) - 1\n    while bajo <= alto:\n        medio = (bajo + alto) // 2\n        if lista[medio] == objetivo:\n            return medio\n        if lista[medio] < objetivo:\n            bajo = medio + 1\n        else:\n            alto = medio - 1\n    return -1",
        "Java": "static int busquedaBinaria(int[] a, int objetivo) {\n    int bajo = 0, alto = a.length - 1;\n    while (bajo <= alto) {\n        int medio = bajo + (alto - bajo) / 2;\n        if (a[medio] == objetivo) return medio;\n        if (a[medio] < objetivo) bajo = medio + 1;\n        else alto = medio - 1;\n    }\n    return -1;\n}",
        "C": "int busquedaBinaria(const int a[], int n, int objetivo) {\n    int bajo = 0, alto = n - 1;\n    while (bajo <= alto) {\n        int medio = bajo + (alto - bajo) / 2;\n        if (a[medio] == objetivo) return medio;\n        if (a[medio] < objetivo) bajo = medio + 1;\n        else alto = medio - 1;\n    }\n    return -1;\n}",
    },
    "3-complejidad-lineal": {
        "Pseudocódigo": "función buscar(A, objetivo)\n    para i ← 0 hasta longitud(A) - 1\n        si A[i] = objetivo entonces retornar i\n    retornar -1",
        "Python": "def buscar_elemento(lista, objetivo):\n    for indice, valor in enumerate(lista):\n        if valor == objetivo:\n            return indice\n    return -1",
        "Java": "static int buscar(int[] a, int objetivo) {\n    for (int i = 0; i < a.length; i++)\n        if (a[i] == objetivo) return i;\n    return -1;\n}",
        "C": "int buscar(const int a[], int n, int objetivo) {\n    for (int i = 0; i < n; i++)\n        if (a[i] == objetivo) return i;\n    return -1;\n}",
    },
    "4-complejidad-log-lineal": {
        "Pseudocódigo": "función ordenar(A)\n    retornar mezclaOrdenada(A)",
        "Python": "def ordenar_lista(lista):\n    return sorted(lista)",
        "Java": "static void ordenar(int[] a) {\n    java.util.Arrays.sort(a);\n}",
        "C": "int comparar(const void *x, const void *y) {\n    return (*(const int *)x > *(const int *)y) -\n           (*(const int *)x < *(const int *)y);\n}\n\nvoid ordenar(int a[], int n) {\n    qsort(a, n, sizeof(int), comparar);\n}",
    },
    "5-complejidad-cuadratica": {
        "Pseudocódigo": "función sumarMatriz(M)\n    suma ← 0\n    para cada fila en M\n        para cada valor en fila\n            suma ← suma + valor\n    retornar suma",
        "Python": "def recorrer_matriz(matriz):\n    suma = 0\n    for fila in matriz:\n        for valor in fila:\n            suma += valor\n    return suma",
        "Java": "static long sumarMatriz(int[][] m) {\n    long suma = 0;\n    for (int[] fila : m)\n        for (int valor : fila) suma += valor;\n    return suma;\n}",
        "C": "long sumarMatriz(int filas, int columnas, int m[filas][columnas]) {\n    long suma = 0;\n    for (int i = 0; i < filas; i++)\n        for (int j = 0; j < columnas; j++) suma += m[i][j];\n    return suma;\n}",
    },
    "6-complejidad-cubica": {
        "Pseudocódigo": "función multiplicar(A, B, n)\n    C ← matriz n × n inicializada en 0\n    para i ← 0 hasta n - 1\n        para j ← 0 hasta n - 1\n            para k ← 0 hasta n - 1\n                C[i,j] ← C[i,j] + A[i,k] × B[k,j]\n    retornar C",
        "Python": "def multiplicar_matrices(a, b):\n    n = len(a)\n    c = [[0] * n for _ in range(n)]\n    for i in range(n):\n        for j in range(n):\n            for k in range(n):\n                c[i][j] += a[i][k] * b[k][j]\n    return c",
        "Java": "static int[][] multiplicar(int[][] a, int[][] b) {\n    int n = a.length;\n    int[][] c = new int[n][n];\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++)\n            for (int k = 0; k < n; k++) c[i][j] += a[i][k] * b[k][j];\n    return c;\n}",
        "C": "void multiplicar(int n, int a[n][n], int b[n][n], int c[n][n]) {\n    for (int i = 0; i < n; i++)\n        for (int j = 0; j < n; j++) {\n            c[i][j] = 0;\n            for (int k = 0; k < n; k++) c[i][j] += a[i][k] * b[k][j];\n        }\n}",
    },
    "8-complejidad-exponencial": {
        "Pseudocódigo": "función fibonacci(n)\n    si n ≤ 1 entonces retornar n\n    retornar fibonacci(n - 1) + fibonacci(n - 2)",
        "Python": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n - 1) + fibonacci(n - 2)",
        "Java": "static long fibonacci(int n) {\n    if (n <= 1) return n;\n    return fibonacci(n - 1) + fibonacci(n - 2);\n}",
        "C": "long fibonacci(int n) {\n    if (n <= 1) return n;\n    return fibonacci(n - 1) + fibonacci(n - 2);\n}",
    },
    "9-complejidad-factorial": {
        "Pseudocódigo": "función contarPermutaciones(A)\n    si longitud(A) ≤ 1 entonces retornar 1\n    total ← 0\n    para i ← 0 hasta longitud(A) - 1\n        total ← total + contarPermutaciones(A sin A[i])\n    retornar total",
        "Python": "def contar_permutaciones(lista):\n    if len(lista) <= 1:\n        return 1\n    total = 0\n    for indice in range(len(lista)):\n        restante = lista[:indice] + lista[indice + 1:]\n        total += contar_permutaciones(restante)\n    return total",
        "Java": "static long contarPermutaciones(java.util.List<Integer> a) {\n    if (a.size() <= 1) return 1;\n    long total = 0;\n    for (int i = 0; i < a.size(); i++) {\n        var restante = new java.util.ArrayList<>(a);\n        restante.remove(i);\n        total += contarPermutaciones(restante);\n    }\n    return total;\n}",
        "C": "long contarPermutaciones(int n) {\n    if (n <= 1) return 1;\n    long total = 0;\n    for (int i = 0; i < n; i++)\n        total += contarPermutaciones(n - 1);\n    return total;\n}",
    },
}

CHAPTER6_CODE = {
    "factorial": {
        "Pseudocódigo": "función factorial(n)\n    si n ≤ 1 entonces retornar 1\n    retornar n × factorial(n - 1)",
        "Python": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
        "Java": "static long factorial(int n) {\n    if (n <= 1) return 1;\n    return n * factorial(n - 1);\n}",
        "C": "long factorial(int n) {\n    if (n <= 1) return 1;\n    return n * factorial(n - 1);\n}",
    },
    "fibonacci": {
        "Pseudocódigo": "función fibonacci(n)\n    si n ≤ 1 entonces retornar n\n    retornar fibonacci(n - 1) + fibonacci(n - 2)",
        "Python": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n - 1) + fibonacci(n - 2)",
        "Java": "static long fibonacci(int n) {\n    if (n <= 1) return n;\n    return fibonacci(n - 1) + fibonacci(n - 2);\n}",
        "C": "long fibonacci(int n) {\n    if (n <= 1) return n;\n    return fibonacci(n - 1) + fibonacci(n - 2);\n}",
    },
    "potencia": {
        "Pseudocódigo": "función potencia(x, n)\n    si n = 0 entonces retornar 1\n    retornar x × potencia(x, n - 1)",
        "Python": "def potencia(x, n):\n    if n == 0:\n        return 1\n    return x * potencia(x, n - 1)",
        "Java": "static double potencia(double x, int n) {\n    if (n == 0) return 1;\n    return x * potencia(x, n - 1);\n}",
        "C": "double potencia(double x, int n) {\n    if (n == 0) return 1;\n    return x * potencia(x, n - 1);\n}",
    },
    "potencia_rapida": {
        "Pseudocódigo": "función potenciaRápida(x, n)\n    si n = 0 entonces retornar 1\n    mitad ← potenciaRápida(x, ⌊n / 2⌋)\n    si n es impar entonces retornar mitad × mitad × x\n    retornar mitad × mitad",
        "Python": "def potencia_rapida(x, n):\n    if n == 0:\n        return 1\n    mitad = potencia_rapida(x, n // 2)\n    if n % 2:\n        return mitad * mitad * x\n    return mitad * mitad",
        "Java": "static double potenciaRapida(double x, int n) {\n    if (n == 0) return 1;\n    double mitad = potenciaRapida(x, n / 2);\n    return n % 2 == 1 ? mitad * mitad * x : mitad * mitad;\n}",
        "C": "double potenciaRapida(double x, int n) {\n    if (n == 0) return 1;\n    double mitad = potenciaRapida(x, n / 2);\n    return n % 2 ? mitad * mitad * x : mitad * mitad;\n}",
    },
    "merge": {
        "Pseudocódigo": "función mergeSort(A)\n    si longitud(A) ≤ 1 entonces retornar A\n    m ← ⌊longitud(A) / 2⌋\n    retornar combinar(mergeSort(A[0:m]), mergeSort(A[m:]))",
        "Python": "def merge_sort(a):\n    if len(a) <= 1:\n        return a\n    m = len(a) // 2\n    return combinar(merge_sort(a[:m]), merge_sort(a[m:]))",
        "Java": "static int[] mergeSort(int[] a) {\n    if (a.length <= 1) return a;\n    int m = a.length / 2;\n    return combinar(\n        mergeSort(java.util.Arrays.copyOfRange(a, 0, m)),\n        mergeSort(java.util.Arrays.copyOfRange(a, m, a.length)));\n}",
        "C": "void mergeSort(int a[], int inicio, int fin) {\n    if (inicio >= fin) return;\n    int medio = inicio + (fin - inicio) / 2;\n    mergeSort(a, inicio, medio);\n    mergeSort(a, medio + 1, fin);\n    combinar(a, inicio, medio, fin);\n}",
    },
    "arbol": {
        "Pseudocódigo": "función buscar(raíz, valor)\n    si raíz = nulo entonces retornar falso\n    si raíz.valor = valor entonces retornar verdadero\n    retornar buscar(raíz.izquierdo, valor) o buscar(raíz.derecho, valor)",
        "Python": "def buscar(raiz, valor):\n    if raiz is None:\n        return False\n    if raiz.valor == valor:\n        return True\n    return buscar(raiz.izquierdo, valor) or buscar(raiz.derecho, valor)",
        "Java": "static boolean buscar(Nodo raiz, int valor) {\n    if (raiz == null) return false;\n    if (raiz.valor == valor) return true;\n    return buscar(raiz.izquierdo, valor) || buscar(raiz.derecho, valor);\n}",
        "C": "bool buscar(const Nodo *raiz, int valor) {\n    if (raiz == NULL) return false;\n    if (raiz->valor == valor) return true;\n    return buscar(raiz->izquierdo, valor) ||\n           buscar(raiz->derecho, valor);\n}",
    },
}

# Los capítulos algorítmicos también deben ser legibles sin abrir Colab.  Estas
# implementaciones son deliberadamente compactas: el texto explica el algoritmo
# y el selector permite comparar su traducción, no cuatro explicaciones repetidas.
CHAPTER7_CODE = {
    "1-busqueda-secuencial": ("para i ← 0 hasta longitud(A)-1\n    si A[i] = x entonces retornar i\nretornar -1", "for i, v in enumerate(a):\n    if v == x: return i\nreturn -1", "for (int i=0;i<a.length;i++) if (a[i]==x) return i;\nreturn -1;", "for (int i=0;i<n;i++) if (a[i]==x) return i;\nreturn -1;"),
    "2-busqueda-binaria": ("izq ← 0; der ← longitud(A)-1\nmientras izq ≤ der\n    m ← ⌊(izq+der)/2⌋\n    si A[m] = x retornar m\n    si A[m] < x: izq ← m+1; si no: der ← m-1\nretornar -1", "lo, hi = 0, len(a)-1\nwhile lo <= hi:\n    m = (lo+hi)//2\n    if a[m] == x: return m\n    if a[m] < x: lo = m+1\n    else: hi = m-1\nreturn -1", "int lo=0, hi=a.length-1;\nwhile(lo<=hi){ int m=lo+(hi-lo)/2; if(a[m]==x)return m; if(a[m]<x)lo=m+1; else hi=m-1; }\nreturn -1;", "int lo=0, hi=n-1;\nwhile(lo<=hi){ int m=lo+(hi-lo)/2; if(a[m]==x)return m; if(a[m]<x)lo=m+1; else hi=m-1; }\nreturn -1;"),
    "3-busqueda-interpolacion": ("mientras bajo ≤ alto y x está entre A[bajo] y A[alto]\n    p ← bajo + (x-A[bajo])(alto-bajo)/(A[alto]-A[bajo])\n    comparar A[p] y acotar el intervalo\nretornar -1", "lo, hi = 0, len(a)-1\nwhile lo <= hi and a[lo] <= x <= a[hi]:\n    if a[hi] == a[lo]: return lo if a[lo] == x else -1\n    p = lo + (x-a[lo])*(hi-lo)//(a[hi]-a[lo])\n    if a[p] == x: return p\n    if a[p] < x: lo = p+1\n    else: hi = p-1\nreturn -1", "int lo=0,hi=a.length-1;\nwhile(lo<=hi && x>=a[lo] && x<=a[hi]){ if(a[hi]==a[lo]) return a[lo]==x?lo:-1; int p=lo+(x-a[lo])*(hi-lo)/(a[hi]-a[lo]); if(a[p]==x)return p; if(a[p]<x)lo=p+1; else hi=p-1; } return -1;", "int lo=0,hi=n-1;\nwhile(lo<=hi && x>=a[lo] && x<=a[hi]){ if(a[hi]==a[lo]) return a[lo]==x?lo:-1; int p=lo+(x-a[lo])*(hi-lo)/(a[hi]-a[lo]); if(a[p]==x)return p; if(a[p]<x)lo=p+1; else hi=p-1; } return -1;"),
    "4-busqueda-saltos": ("paso ← ⌊√longitud(A)⌋\nsaltar bloques hasta superar x\nbuscar secuencialmente en el bloque candidato", "from math import isqrt\nstep = max(1, isqrt(len(a)))\nprev = 0\nwhile prev < len(a) and a[min(prev+step, len(a))-1] < x: prev += step\nfor i in range(prev, min(prev+step, len(a))):\n    if a[i] == x: return i\nreturn -1", "int step=(int)Math.sqrt(a.length), prev=0;\nwhile(prev<a.length && a[Math.min(prev+step,a.length)-1]<x) prev+=step;\nfor(int i=prev;i<Math.min(prev+step,a.length);i++) if(a[i]==x)return i; return -1;", "int step=(int)sqrt(n), prev=0;\nwhile(prev<n && a[(prev+step<n?prev+step:n)-1]<x) prev+=step;\nfor(int i=prev;i<n && i<prev+step;i++) if(a[i]==x)return i; return -1;"),
    "5-busqueda-exponencial": ("si A[0] = x retornar 0\ni ← 1\nmientras i < longitud(A) y A[i] ≤ x: i ← 2i\naplicar búsqueda binaria en [i/2, min(i,n-1)]", "if a and a[0] == x: return 0\ni = 1\nwhile i < len(a) and a[i] <= x: i *= 2\nreturn binaria(a, x, i//2, min(i, len(a)-1))", "if(a.length>0&&a[0]==x)return 0; int i=1;\nwhile(i<a.length&&a[i]<=x)i*=2;\nreturn binaria(a,x,i/2,Math.min(i,a.length-1));", "if(n>0&&a[0]==x)return 0; int i=1;\nwhile(i<n&&a[i]<=x)i*=2;\nreturn binaria(a,x,i/2,i<n?i:n-1);"),
    "6-busqueda-ternaria": ("mientras izq ≤ der\n    m1 ← izq+(der-izq)/3; m2 ← der-(der-izq)/3\n    comparar x con A[m1] y A[m2]\n    conservar uno de los tres intervalos\nretornar -1", "lo, hi = 0, len(a)-1\nwhile lo <= hi:\n    third = (hi-lo)//3; m1, m2 = lo+third, hi-third\n    if a[m1] == x: return m1\n    if a[m2] == x: return m2\n    if x < a[m1]: hi = m1-1\n    elif x > a[m2]: lo = m2+1\n    else: lo, hi = m1+1, m2-1\nreturn -1", "int lo=0,hi=a.length-1; while(lo<=hi){int t=(hi-lo)/3,m1=lo+t,m2=hi-t;if(a[m1]==x)return m1;if(a[m2]==x)return m2;if(x<a[m1])hi=m1-1;else if(x>a[m2])lo=m2+1;else{lo=m1+1;hi=m2-1;}}return -1;", "int lo=0,hi=n-1; while(lo<=hi){int t=(hi-lo)/3,m1=lo+t,m2=hi-t;if(a[m1]==x)return m1;if(a[m2]==x)return m2;if(x<a[m1])hi=m1-1;else if(x>a[m2])lo=m2+1;else{lo=m1+1;hi=m2-1;}}return -1;"),
}

CHAPTER8_CODE = {
    "1-ordenamiento-burbuja": ("para fin ← n-1 hasta 1\n    para i ← 0 hasta fin-1\n        si A[i] > A[i+1] intercambiar", "for end in range(len(a)-1, 0, -1):\n    for i in range(end):\n        if a[i] > a[i+1]: a[i], a[i+1] = a[i+1], a[i]", "for(int e=a.length-1;e>0;e--) for(int i=0;i<e;i++) if(a[i]>a[i+1]){int t=a[i];a[i]=a[i+1];a[i+1]=t;}", "for(int e=n-1;e>0;e--) for(int i=0;i<e;i++) if(a[i]>a[i+1]){int t=a[i];a[i]=a[i+1];a[i+1]=t;}"),
    "2-ordenamiento-seleccion": ("para i ← 0 hasta n-2\n    mínimo ← i\n    buscar el menor en A[i+1:n]\n    intercambiar A[i] y A[mínimo]", "for i in range(len(a)-1):\n    m = min(range(i, len(a)), key=a.__getitem__)\n    a[i], a[m] = a[m], a[i]", "for(int i=0;i<a.length-1;i++){int m=i;for(int j=i+1;j<a.length;j++)if(a[j]<a[m])m=j;int t=a[i];a[i]=a[m];a[m]=t;}", "for(int i=0;i<n-1;i++){int m=i;for(int j=i+1;j<n;j++)if(a[j]<a[m])m=j;int t=a[i];a[i]=a[m];a[m]=t;}"),
    "3-ordenamiento-insercion": ("para i ← 1 hasta n-1\n    clave ← A[i]; j ← i-1\n    desplazar valores mayores que clave\n    insertar clave en j+1", "for i in range(1, len(a)):\n    key, j = a[i], i-1\n    while j >= 0 and a[j] > key: a[j+1], j = a[j], j-1\n    a[j+1] = key", "for(int i=1;i<a.length;i++){int k=a[i],j=i-1;while(j>=0&&a[j]>k){a[j+1]=a[j--];}a[j+1]=k;}", "for(int i=1;i<n;i++){int k=a[i],j=i-1;while(j>=0&&a[j]>k){a[j+1]=a[j--];}a[j+1]=k;}"),
    "4-ordenamiento-shell": ("salto ← ⌊n/2⌋\nmientras salto > 0\n    aplicar inserción entre elementos separados por salto\n    salto ← ⌊salto/2⌋", "gap = len(a)//2\nwhile gap:\n    for i in range(gap, len(a)):\n        v, j = a[i], i\n        while j >= gap and a[j-gap] > v: a[j] = a[j-gap]; j -= gap\n        a[j] = v\n    gap //= 2", "for(int g=a.length/2;g>0;g/=2)for(int i=g;i<a.length;i++){int v=a[i],j=i;while(j>=g&&a[j-g]>v){a[j]=a[j-g];j-=g;}a[j]=v;}", "for(int g=n/2;g>0;g/=2)for(int i=g;i<n;i++){int v=a[i],j=i;while(j>=g&&a[j-g]>v){a[j]=a[j-g];j-=g;}a[j]=v;}"),
    "5-ordenamiento-mezcla": ("si longitud(A) ≤ 1 retornar A\ndividir A en dos mitades\nordenar recursivamente cada mitad\ncombinar ambas mitades ordenadas", "def merge_sort(a):\n    if len(a) <= 1: return a\n    m = len(a)//2\n    return merge(merge_sort(a[:m]), merge_sort(a[m:]))", "static int[] mergeSort(int[] a){if(a.length<=1)return a;int m=a.length/2;return merge(mergeSort(java.util.Arrays.copyOfRange(a,0,m)),mergeSort(java.util.Arrays.copyOfRange(a,m,a.length)));}", "void mergeSort(int a[],int lo,int hi){if(lo>=hi)return;int m=lo+(hi-lo)/2;mergeSort(a,lo,m);mergeSort(a,m+1,hi);merge(a,lo,m,hi);}"),
    "6-ordenamiento-rapido": ("si bajo < alto\n    p ← particionar(A,bajo,alto)\n    quicksort(A,bajo,p-1)\n    quicksort(A,p+1,alto)", "def quicksort(a, lo, hi):\n    if lo < hi:\n        p = partition(a, lo, hi)\n        quicksort(a, lo, p-1); quicksort(a, p+1, hi)", "static void quicksort(int[]a,int lo,int hi){if(lo<hi){int p=partition(a,lo,hi);quicksort(a,lo,p-1);quicksort(a,p+1,hi);}}", "void quicksort(int a[],int lo,int hi){if(lo<hi){int p=partition(a,lo,hi);quicksort(a,lo,p-1);quicksort(a,p+1,hi);}}"),
    "7-ordenamiento-radix": ("exp ← 1\nmientras máximo(A)/exp > 0\n    ordenar establemente por el dígito exp\n    exp ← 10·exp", "exp, maximum = 1, max(a, default=0)\nwhile maximum // exp:\n    counting_digit(a, exp)\n    exp *= 10", "int max=java.util.Arrays.stream(a).max().orElse(0);for(int exp=1;max/exp>0;exp*=10)countingDigit(a,exp);", "int max=maximo(a,n);for(int exp=1;max/exp>0;exp*=10)countingDigit(a,n,exp);"),
}


def compact_code(snippets: tuple[str, str, str, str]) -> dict[str, str]:
    return dict(zip(("Pseudocódigo", "Python", "Java", "C"), snippets))


def code_tabs(snippets: dict[str, str]) -> str:
    language = {"Pseudocódigo": "text", "Python": "python", "Java": "java", "C": "c"}
    blocks = []
    for label, code in snippets.items():
        indented = "\n".join(f"    {line}" if line else "" for line in code.splitlines())
        blocks.append(f'=== "{label}"\n\n    ```{language[label]}\n{indented}\n    ```')
    return "\n\n".join(blocks)


def lab_button(url: str) -> str:
    return (
        '<div class="lab-action">\n'
        f'<a class="md-button md-button--primary colab-button" href="{url}" '
        'target="_blank" rel="noopener noreferrer">Ejecutar notebook en Google Colab</a>\n'
        '<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>\n'
        "</div>"
    )


FIGURES_START = "<!-- figures-from-explanation:start -->"
FIGURES_END = "<!-- figures-from-explanation:end -->"


def _figure_caption(label: str, relative_path: str, position: int, total: int) -> str:
    """Construye un pie breve y legible a partir del recurso original."""
    stem = Path(relative_path).stem
    if stem.endswith("_tiempo"):
        return f"Comportamiento temporal experimental de {label.lower()}."
    if stem.endswith("_espacio"):
        return f"Comportamiento espacial experimental de {label.lower()}."
    if "mejor_caso" in stem:
        return f"Visualización del mejor caso de {label.lower()}."
    if "peor_caso" in stem:
        return f"Visualización del peor caso de {label.lower()}."
    if "promedio" in stem:
        return f"Visualización del caso promedio de {label.lower()}."
    if "comparacion" in stem:
        return f"Comparación de crecimiento para {label.lower()}."
    if "arbol" in stem:
        return f"Árbol de llamadas de {label.lower()}."
    if total > 1:
        return f"Secuencia visual de {label.lower()} · paso representativo {position} de {total}."
    return f"Representación gráfica de {label.lower()}."


def publish_figure_gallery(chapter: int, slug: str, label: str) -> str:
    """Copia las figuras al árbol de Pages y retorna la galería HTML."""
    relative_paths = PAGE_FIGURES.get((chapter, slug), ())
    if not relative_paths:
        return ""

    source_root = ROOT / f"capitulo{chapter}" / "images" / "recursos"
    destination_root = DOCS / "assets" / "images" / f"capitulo-{chapter}"
    figures = []
    for position, relative_path in enumerate(relative_paths, start=1):
        source = source_root / relative_path
        if not source.is_file():
            raise FileNotFoundError(f"No existe la figura declarada para Pages: {source}")
        destination = destination_root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        caption = _figure_caption(label, relative_path, position, len(relative_paths))
        image_url = f"../../../assets/images/capitulo-{chapter}/{relative_path}"
        figures.append(
            f'<figure><img src="{image_url}" alt="{caption[:-1]}">'
            f"<figcaption>{caption}</figcaption></figure>"
        )
    return "\n".join((FIGURES_START, '<div class="chapter-figures">', *figures, "</div>", FIGURES_END))


def relocate_colab_action(content: str) -> str:
    """Ubica el llamado a Colab inmediatamente después del título y el kicker."""
    pattern = re.compile(
        r'\n*<div class="lab-action">(?:(?!</div>).)*?colab-button(?:(?!</div>).)*?</div>\n*',
        flags=re.DOTALL,
    )
    blocks = pattern.findall(content)
    if not blocks:
        return content
    content = pattern.sub("\n\n", content)
    block = blocks[0].strip()
    kicker = re.search(r'^<span class="chapter-kicker">.+$', content, flags=re.MULTILINE)
    if not kicker:
        raise ValueError("No se encontró el chapter-kicker para ubicar el botón de Colab")
    return content[: kicker.end()] + "\n\n" + block + content[kicker.end():]


def sync_published_sections() -> None:
    """Sincroniza posición de botones y figuras en todas las páginas hijas."""
    labels: dict[tuple[int, str], str] = {}
    for chapter in LABS:
        for label, slug, _body, _url in section_specs(chapter):
            labels[(chapter, slug)] = label

    for path in sorted((DOCS / "capitulos").glob("capitulo-*/*.md")):
        match = re.fullmatch(r"capitulo-(\d+)", path.parent.name)
        if not match:
            continue
        chapter = int(match.group(1))
        slug = path.stem
        content = relocate_colab_action(path.read_text(encoding="utf-8"))

        gallery_pattern = re.compile(
            rf"\n*{re.escape(FIGURES_START)}.*?{re.escape(FIGURES_END)}\n*",
            flags=re.DOTALL,
        )
        content = gallery_pattern.sub("\n\n", content)
        label = labels.get((chapter, slug))
        gallery = publish_figure_gallery(chapter, slug, label or slug.replace("-", " "))
        if gallery:
            expected_names = [Path(item).name for item in PAGE_FIGURES[(chapter, slug)]]
            # Las páginas 2 y 3 incluyen algunas figuras colocadas manualmente en
            # puntos semánticos precisos. Si ya están todas, no se duplican.
            if not all(name in content for name in expected_names):
                insertion = re.search(
                    r'^(?:<div class="related-links">|<nav class="section-return )',
                    content,
                    flags=re.MULTILINE,
                )
                index = insertion.start() if insertion else len(content.rstrip())
                content = content[:index].rstrip() + "\n\n" + gallery + "\n\n" + content[index:].lstrip()
        path.write_text(content.rstrip() + "\n", encoding="utf-8")


def section_id(slug: str) -> str:
    plain = unicodedata.normalize("NFKD", slug).encode("ascii", "ignore").decode()
    return "seccion-" + re.sub(r"[^a-z0-9]+", "-", plain.lower()).strip("-")


def chapter_outline(chapter: int) -> str:
    links = [
        f'<li><a href="#{section_id(slug)}">{heading}</a></li>'
        for heading, slug in LABS[chapter]
    ]
    return (
        '<nav class="chapter-outline" id="contenido-del-capitulo" aria-label="Contenido del capítulo">\n'
        '<strong>En este capítulo</strong>\n<ol>\n'
        + "\n".join(links)
        + "\n</ol>\n</nav>"
    )


def normalize_table_math(body: str) -> str:
    """Convierte fórmulas de celdas HTML a LaTeX antes de que llegue MathJax."""
    translations = str.maketrans({"²": "^2", "³": "^3", "√": r"\sqrt "})

    def convert(match: re.Match[str]) -> str:
        value = match.group(1).strip()
        if r"\(" in value or not re.match(r"^(?:O|o|Ω|ω|Θ)\s*\(", value):
            return match.group(0)
        formula, suffix = value, ""
        if " con " in value:
            formula, suffix = value.split(" con ", 1)
            suffix = " con " + suffix
        latex = formula.translate(translations)
        latex = latex.replace("Ω", r"\Omega").replace("ω", r"\omega").replace("Θ", r"\Theta")
        latex = re.sub(r"log\(log\(n\)\)", r"\\log_2(\\log_2(n))", latex)
        latex = re.sub(r"log\(n\)", r"\\log_2(n)", latex)
        latex = re.sub(r"\bn d\b", "nd", latex)
        return f"<td>\\({latex}\\){suffix}</td>"

    return re.sub(r"<td>(.*?)</td>", convert, body, flags=re.DOTALL)


def missing_chapter4_example(key: str) -> str:
    example = CHAPTER4_MISSING[key]
    return "\n\n".join(
        (
            f"## {example['title']}",
            example["intro"],
            "### Código analizado\n\n" + code_tabs(example["code"]),
            "### Análisis esperado\n\n" + example["analysis"],
        )
    )


def extract_lab(chapter: int, slug: str) -> tuple[str, str]:
    source = (DOCS / "laboratorios" / f"capitulo-{chapter}" / f"{slug}.md").read_text(encoding="utf-8")
    match = re.search(
        r"^\[Abrir en Google Colab\]\((https://colab\.research\.google\.com/.+)\)\{",
        source,
        flags=re.MULTILINE,
    )
    if not match:
        raise ValueError(f"No se encontró el enlace de Colab en capítulo {chapter}: {slug}")
    url = match.group(1)
    lines = source.splitlines()
    body = "\n".join(lines[3:]).strip()
    body = re.sub(
        r"\n*---\n+## Ejecutar el laboratorio\n+.*?\n+\[Abrir en Google Colab\].*?\n+---\n*",
        "\n\n",
        body,
        flags=re.DOTALL,
    )
    body = re.sub(r"^(#{2,5}) ", lambda m: "#" + m.group(1) + " ", body, flags=re.MULTILINE)
    body = body.replace("Este notebook", "Esta sección")
    body = body.replace("este notebook", "el laboratorio")
    body = body.replace("GitHubColab", "Google Colab")
    body = body.replace(
        "Este resumen presenta los resultados generales para las dos formas de implementación. "
        "El detalle de los procesos, criterios y cálculos que llevan a estas complejidades se puede "
        "consultar en los recursos complementarios que proporciona la obra.\n",
        "",
    )
    if chapter == 3 and slug == "ejemplos-concretos-notaciones":
        body = ASYMPTOTIC_EXAMPLES
    elif chapter == 6 and slug == "0-laboratorio-analisis-recursivo":
        body = re.sub(
            r"### Ejemplo 3 · Potencia recursiva simple.*?(?=### Ejemplo 4 · Exponenciación rápida)",
            "",
            RECURSIVE_EXAMPLES,
            flags=re.DOTALL,
        )
        body = body.replace("### Ejemplo 4 · Exponenciación rápida", "### Ejemplo 3 · Potencia de un número entero positivo")
        body = body.replace("La animación contrasta la reducción lineal de la potencia simple con la reducción por mitades.", "La animación muestra la reducción por mitades del exponente.")
        body += CHAPTER6_ADDITIONAL
        examples = iter(("factorial", "fibonacci", "potencia_rapida", "merge", "arbol"))
        body = re.sub(
            r"```python\n.*?\n```",
            lambda _match: code_tabs(CHAPTER6_CODE[next(examples)]),
            body,
            flags=re.DOTALL,
        )
    elif chapter == 4:
        body = body.replace(
            "### Código analizado\n",
            f"### Código analizado\n\n{code_tabs(CHAPTER4_CODE[slug])}\n",
            1,
        )
    elif chapter == 2 and slug in CHAPTER2_CODE:
        body = body.replace(
            "### Simulación\n",
            f"### Código del ejemplo\n\n{code_tabs(CHAPTER2_CODE[slug])}\n\n### Simulación\n",
            1,
        )
    elif chapter == 7 and slug in CHAPTER7_CODE:
        marker = "### Complejidad"
        body = body.replace(marker, "### Implementación\n\n" + code_tabs(compact_code(CHAPTER7_CODE[slug])) + "\n\n" + marker, 1)
    elif chapter == 8 and slug in CHAPTER8_CODE:
        marker = "### Complejidad"
        body = body.replace(marker, "### Implementación\n\n" + code_tabs(compact_code(CHAPTER8_CODE[slug])) + "\n\n" + marker, 1)
    body = normalize_table_math(body)
    body = body.strip()
    return body, url


def navigation(chapter: int) -> tuple[str, str]:
    prev = "../../" if chapter == 2 else f"../capitulo-{chapter - 1}/"
    prev_label = "Inicio" if chapter == 2 else f"Capítulo {chapter - 1}"
    nxt = "../../obra/" if chapter == 8 else f"../capitulo-{chapter + 1}/"
    next_label = "La obra" if chapter == 8 else f"Capítulo {chapter + 1}"
    links = (
        f'<a href="{prev}">← {prev_label}</a><a class="chapter-nav__index" href="../">Recorrido</a>'
        f'<a class="chapter-nav__next" href="{nxt}">{next_label} →</a>'
    )
    return (
        f'<nav class="chapter-nav" aria-label="Navegación superior entre capítulos">{links}</nav>',
        f'<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos">{links}</nav>',
    )


def section_navigation(chapter: int, sections: list[tuple[str, str]], index: int) -> str:
    previous = ""
    following = ""
    if index:
        label, slug = sections[index - 1]
        previous = f'<a href="../{slug}/">← {label}</a>'
    if index + 1 < len(sections):
        label, slug = sections[index + 1]
        following = f'<a class="section-step__next" href="../{slug}/">{label} →</a>'
    return (
        '<nav class="section-return section-step" aria-label="Navegación entre secciones">'
        f'{previous}<a class="section-step__index" href="../">Capítulo {chapter}</a>{following}</nav>'
    )


def nested_chapter_navigation(chapter: int) -> tuple[str, str]:
    prev = "../../" if chapter == 2 else f"../../capitulo-{chapter - 1}/"
    prev_label = "Recorrido" if chapter == 2 else f"Capítulo {chapter - 1}"
    nxt = "../../" if chapter == 8 else f"../../capitulo-{chapter + 1}/"
    next_label = "Recorrido" if chapter == 8 else f"Capítulo {chapter + 1}"
    links = (
        f'<a href="{prev}">← {prev_label}</a><a class="chapter-nav__index" href="../">Capítulo {chapter}</a>'
        f'<a class="chapter-nav__next" href="{nxt}">{next_label} →</a>'
    )
    return (
        f'<nav class="chapter-nav" aria-label="Navegación superior entre capítulos">{links}</nav>',
        f'<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos">{links}</nav>',
    )


METHODS = {
    "sustitucion-iterativa": (
        "5.5.1 Sustitución iterativa",
        r"""La sustitución iterativa expande la recurrencia hasta reconocer un patrón. Primero se reemplaza el término recursivo por su definición; después se repite la operación \(k\) veces, se identifica cuándo el argumento alcanza el caso base y se suma el trabajo acumulado.

### Procedimiento

1. Escriba la recurrencia y su condición inicial.
2. Expanda dos o tres niveles sin simplificar prematuramente.
3. Exprese coeficientes, argumento y suma después de \(k\) sustituciones.
4. Resuelva \(k\) a partir del caso base.
5. Sustituya ese valor y simplifique la suma mediante dominancia.

Es apropiado para relaciones de reducción y división con un patrón analítico reconocible. La expansión no es una demostración completa hasta justificar el patrón general y verificar la condición inicial.""",
    ),
    "arbol-recurrencia": (
        "5.5.2 Árbol de recurrencia",
        r"""El árbol de recurrencia representa cada llamada como un nodo y cada subproblema como una rama. La complejidad se obtiene sumando el costo de todos los niveles, no siguiendo únicamente una rama.

### Procedimiento

1. Determine número y tamaño de los hijos de cada llamada.
2. Calcule el costo individual de un nodo en el nivel \(i\).
3. Multiplique ese costo por la cantidad de nodos del nivel.
4. Determine la altura mediante el caso base.
5. Sume costos internos y hojas, y contraste el término dominante.

El método es especialmente claro para árboles uniformes. En relaciones mixtas las ramas pueden tener alturas diferentes y deben contabilizarse por separado.""",
    ),
    "teorema-maestro": (
        "5.5.3 Teorema maestro",
        r"""El teorema maestro clasifica recurrencias de división de la forma \(T(n)=aT(n/b)+f(n)\). La comparación central es entre el trabajo externo \(f(n)\) y el costo crítico \(n^{\log_b(a)}\).

### Procedimiento

1. Identifique \(a\), \(b\) y \(f(n)\); si la recurrencia no tiene la forma exigida, no aplique el teorema.
2. Calcule \(n^{\log_b(a)}\).
3. Compare órdenes de crecimiento y determine el caso aplicable.
4. En el caso que exige regularidad, compruebe explícitamente la condición correspondiente.
5. Escriba la cota ajustada y explique qué parte del árbol domina.

La versión básica cubre costos polinómicos; extensiones permiten factores logarítmicos. Las relaciones de reducción \(T(n-1)\) y las divisiones desiguales requieren otro método o una generalización.""",
    ),
    "ecuacion-caracteristica": (
        "5.5.4 Ecuación característica",
        r"""La ecuación característica resuelve recurrencias lineales de reducción con coeficientes constantes. Separa la parte homogénea y propone una solución exponencial \(T_h(n)=r^n\), con la que se obtiene un polinomio en \(r\).

### Procedimiento

1. Lleve todos los términos homogéneos a un lado.
2. Sustituya \(T_h(n)=r^n\) y construya el polinomio característico.
3. Halle sus raíces y considere su multiplicidad.
4. Si existe un término no homogéneo, proponga una solución particular compatible.
5. Use las condiciones iniciales para determinar las constantes.

Las raíces distintas, repetidas o complejas producen formas de solución diferentes. El método no se aplica directamente a coeficientes variables ni a argumentos como \(n/2\).""",
    ),
}

EXERCISE_TITLES = {
    2: "2.2 Ejercicios propuestos",
    3: "3.6 Ejercicios propuestos",
    4: "4.6 Ejercicios propuestos",
    5: "5.6.1 Ejercicios propuestos",
    6: "6.4.1 Ejercicios propuestos",
    7: "7.9 Ejercicios propuestos",
    8: "8.9 Ejercicios propuestos",
}


def exercise_pdf(chapter: int) -> str:
    return (
        "Los enunciados de esta sección se conservan en el documento PDF del capítulo. "
        "Ábrelo para consultar la formulación completa, las condiciones y la numeración original.\n\n"
        '<div class="lab-action">\n'
        f'<a class="md-button md-button--primary pdf-button" href="../../../assets/pdfs/'
        f'capitulo-{chapter}-ejercicios-propuestos.pdf" target="_blank" rel="noopener noreferrer">'
        '<span aria-hidden="true">PDF</span> Consultar ejercicios propuestos</a>\n'
        '<small class="lab-action__note">El documento se abrirá en una pestaña nueva.</small>\n'
        "</div>"
    )


def section_specs(chapter: int) -> list[tuple[str, str, str, str | None]]:
    """Retorna título, slug, contenido y URL de simulación para cada página hija."""
    specs: list[tuple[str, str, str, str | None]] = []
    if chapter == 4:
        missing_after = {
            "ejemplo5-ciclos-incremento-no-lineal": "ejemplo6",
            "ejemplo7-ciclo-sin-dependencia": "ejemplo8",
            "ejemplo9-complejidad-oculta": "ejemplo10",
        }
        for heading, slug in LABS[chapter]:
            body, url = extract_lab(chapter, slug)
            specs.append((heading, slug, body, url))
            if slug in missing_after:
                key = missing_after[slug]
                example = CHAPTER4_MISSING[key]
                specs.append((example["title"], key, "\n\n".join((example["intro"], "## Código analizado\n\n" + code_tabs(example["code"]), "## Análisis esperado\n\n" + example["analysis"])), None))
        specs.append((EXERCISE_TITLES[chapter], "ejercicios-propuestos", exercise_pdf(chapter), None))
        return specs
    if chapter == 5:
        body, url = extract_lab(5, "0-arboles-recursion")
        specs.append(("5.4 Formas de las relaciones de recurrencia", "formas-de-recurrencia", body, url))
        _, method_url = extract_lab(5, "1-metodos-solucion-relaciones-recurrencia")
        specs.extend((title, slug, body, method_url) for slug, (title, body) in METHODS.items())
        specs.append((EXERCISE_TITLES[chapter], "ejercicios-propuestos", exercise_pdf(chapter), None))
        return specs
    if chapter == 6:
        body, url = extract_lab(6, "0-laboratorio-analisis-recursivo")
        matches = list(re.finditer(r"^### (Ejemplo \d+ · .+)$", body, flags=re.MULTILINE))
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
            title = match.group(1)
            slug = ("factorial", "fibonacci", "potencia", "merge-sort", "arbol-binario")[index]
            specs.append((title, slug, body[match.end():end].strip(), url))
        specs.append((EXERCISE_TITLES[chapter], "ejercicios-propuestos", exercise_pdf(chapter), None))
        return specs
    for heading, slug in LABS[chapter]:
        body, url = extract_lab(chapter, slug)
        if slug == "ejercicios-propuestos":
            body = exercise_pdf(chapter) + "\n\n" + body
        specs.append((heading, slug, body, url))
    return specs


def build_sectioned_chapter(chapter: int) -> None:
    current_path = DOCS / "capitulos" / f"capitulo-{chapter}.md"
    current = current_path.read_text(encoding="utf-8")
    title = re.search(r"^# .+$", current, flags=re.MULTILINE).group(0)
    kicker = re.search(r'^<span class="chapter-kicker">.+$', current, flags=re.MULTILINE).group(0)
    specs = section_specs(chapter)
    directory = DOCS / "capitulos" / f"capitulo-{chapter}"
    directory.mkdir(exist_ok=True)

    cards = [
        '<nav class="chapter-outline chapter-outline--pages" aria-label="Secciones del capítulo">',
        "<strong>Secciones del capítulo</strong>",
        '<ol class="chapter-section-list">',
    ]
    for label, slug, _body, _url in specs:
        cards.append(f'<li><a href="{slug}/"><span>{label}</span><small>Leer sección →</small></a></li>')
    cards.extend(("</ol>", "</nav>"))
    top, bottom = navigation(chapter)
    current_path.write_text("\n\n".join((top, title, kicker, INTRO[chapter].strip(), "\n".join(cards), "---", bottom)) + "\n", encoding="utf-8")

    section_pairs = [(label, slug) for label, slug, _body, _url in specs]
    nested_top, nested_bottom = nested_chapter_navigation(chapter)
    for index, (label, slug, body, url) in enumerate(specs):
        button = lab_button(url) if url else ""
        if chapter in (7, 8) and not slug.startswith("0-comparacion-"):
            comparison_slug = "0-comparacion-busquedas" if chapter == 7 else "0-comparacion-ordenamientos"
            body = body.rstrip() + (
                f'\n\n<div class="related-links"><strong>Para comparar</strong> '
                f'<a href="../{comparison_slug}/">ver la comparación general de todos los algoritmos</a>.</div>'
            )
        if slug.startswith("0-comparacion-"):
            marker = re.search(r"^### Algoritmos incluidos\s*$", body, flags=re.MULTILINE)
            if marker:
                body = body[:marker.start()].rstrip() + "\n\n" + button + "\n\n" + body[marker.start():]
                button = ""
        content = (nested_top, f"# {label}", f'<span class="chapter-kicker">Capítulo {chapter}</span>', body, button, section_navigation(chapter, section_pairs, index), "---", nested_bottom)
        (directory / f"{slug}.md").write_text("\n\n".join(part for part in content if part) + "\n", encoding="utf-8")
def build_chapter(chapter: int) -> None:
    current = (DOCS / "capitulos" / f"capitulo-{chapter}.md").read_text(encoding="utf-8")
    title = re.search(r"^# .+$", current, flags=re.MULTILINE).group(0)
    kicker = re.search(r"^<span class=\"chapter-kicker\">.+$", current, flags=re.MULTILINE).group(0)
    top, bottom = navigation(chapter)
    parts = [top, title, kicker, INTRO[chapter].strip(), chapter_outline(chapter)]
    for index, (heading, slug) in enumerate(LABS[chapter]):
        body, url = extract_lab(chapter, slug)
        button = lab_button(url)
        is_comparison = chapter in (7, 8) and slug.startswith("0-comparacion-")
        if is_comparison:
            table_heading = re.search(r"^### Algoritmos incluidos\s*$", body, flags=re.MULTILINE)
            if not table_heading:
                raise ValueError(f"La comparación {chapter}/{slug} no contiene la tabla esperada")
            body = body[: table_heading.start()].rstrip() + "\n\n" + button + "\n\n" + body[table_heading.start():]
        previous_link = ""
        next_link = ""
        if index:
            prev_heading, prev_slug = LABS[chapter][index - 1]
            previous_link = f'<a href="#{section_id(prev_slug)}">← {prev_heading}</a>'
        if index + 1 < len(LABS[chapter]):
            next_heading, next_slug = LABS[chapter][index + 1]
            next_link = f'<a class="section-step__next" href="#{section_id(next_slug)}">{next_heading} →</a>'
        section_navigation = (
            '<nav class="section-return section-step" aria-label="Navegación entre secciones">'
            f'{previous_link}<a class="section-step__index" href="#contenido-del-capitulo">Contenido</a>{next_link}</nav>'
        )
        parts.extend(
            [
                f'## {heading} {{ #{section_id(slug)} }}',
                body,
                "" if is_comparison else button,
                section_navigation,
            ]
        )
        if chapter == 4 and slug == "ejemplo5-ciclos-incremento-no-lineal":
            parts.append(missing_chapter4_example("ejemplo6"))
        elif chapter == 4 and slug == "ejemplo7-ciclo-sin-dependencia":
            parts.append(missing_chapter4_example("ejemplo8"))
        elif chapter == 4 and slug == "ejemplo9-complejidad-oculta":
            parts.append(missing_chapter4_example("ejemplo10"))
    parts.extend(["---", bottom])
    (DOCS / "capitulos" / f"capitulo-{chapter}.md").write_text("\n\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    for chapter_number in LABS:
        # Los capítulos 2 y 3 contienen una edición manual ampliada con figuras y
        # secciones teóricas que no deben reconstruirse desde las fichas antiguas.
        if chapter_number in {2, 3}:
            continue
        build_chapter(chapter_number)
        build_sectioned_chapter(chapter_number)
    sync_published_sections()
    print("Capítulos, botones de Colab y figuras de las explicaciones sincronizados.")
