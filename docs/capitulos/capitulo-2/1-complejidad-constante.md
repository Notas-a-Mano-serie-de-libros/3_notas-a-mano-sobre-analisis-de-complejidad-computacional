<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.1.2.1 Complejidad constante

<span class="chapter-kicker">Capítulo 2</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/notebooks/1_complejidad_constante.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar notebook en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

### Algoritmo simulado: acceder a una posición de un arreglo

El ejemplo implementa el acceso a una posición específica de una lista o arreglo. En la función, `lista` representa la estructura de datos, `indice` representa la posición que se desea consultar y el valor leído se devuelve directamente.

El acceso por índice tiene comportamiento constante porque la posición del elemento se calcula directamente. La ejecución requiere conocer la referencia inicial de la estructura y el desplazamiento asociado al índice. Con esa información, el entorno de ejecución puede ubicar el elemento solicitado mediante una operación directa de acceso.

La lista puede contener muchos elementos, pero el acceso a `lista[indice]` consulta una sola posición. La operación realizada para leer el elemento central de una lista de 100 posiciones tiene la misma forma que la operación realizada para leer el elemento central de una lista de 1.000.000 de posiciones: se identifica un índice válido y se recupera el dato ubicado en esa posición.

La diferencia entre listas pequeñas y grandes aparece en otras operaciones, como construir la lista, recorrerla completa, copiarla o buscar un valor desconocido. En cambio, cuando el índice ya está determinado, el acceso se concentra en una única ubicación.


---

### Código del ejemplo

=== "Pseudocódigo"

    ```text
    función acceder(arreglo, índice)
        retornar arreglo[índice]
    ```

=== "Python"

    ```python
    def acceder_posicion(lista, indice):
        return lista[indice]
    ```

=== "Java"

    ```java
    static int acceder(int[] arreglo, int indice) {
        return arreglo[indice];
    }
    ```

=== "C"

    ```c
    int acceder(const int arreglo[], int indice) {
        return arreglo[indice];
    }
    ```

### Simulación

Los dos experimentos utilizan los mismos controles:

- **Máximo \(n\):** establece el mayor tamaño de entrada que se estudiará. El intervalo entre \(10^0\) y ese máximo se divide en múltiples tamaños para conservar la curva experimental, y la tabla destaca los puntos \(10^1, 10^2, \ldots, 10^i\).
- **Ejecuciones:** indica cuántas veces se repite la operación para cada tamaño de entrada. El valor mostrado en la tabla y en la figura es el promedio de esas repeticiones.

Una medición individual puede verse afectada por interrupciones del sistema, resolución del temporizador, caché y otros factores externos. A medida que aumenta el número de ejecuciones, el promedio experimental tiende a acercarse al **valor esperado del costo observado** bajo las mismas condiciones y las fluctuaciones aleatorias pierden influencia. Esto no obliga al valor experimental a coincidir exactamente con la constante teórica, pero permite observar con mayor claridad que no existe una tendencia de crecimiento asociada a \(n\).

#### Complejidad temporal experimental

### Detalle teórico

La complejidad constante describe operaciones cuyo costo permanece estable frente a cambios en el tamaño de la entrada. El tamaño de la entrada se representa con \(n\) y suele indicar la cantidad de elementos disponibles para procesar: por ejemplo, la longitud de una lista, la cantidad de registros en una tabla o el número de posiciones de un arreglo.

Una operación de costo constante realiza una cantidad fija de acciones elementales. Esa cantidad puede ser pequeña o grande, dependiendo de la operación concreta y de la máquina que la ejecuta, pero conserva una característica esencial: al aumentar \(n\), el procedimiento ejecutado mantiene la misma estructura y la misma cantidad básica de trabajo.

Este tipo de comportamiento aparece en instrucciones puntuales como leer una variable, asignar un valor, comparar dos datos simples o acceder a una posición conocida dentro de una estructura con acceso directo.

Para una entrada de tamaño \(n\), una función de costo constante puede expresarse como:

\[
T(n) = c
\]

donde \(T(n)\) representa el costo de ejecutar la operación sobre una entrada de tamaño \(n\), y \(c\) representa una cantidad fija de trabajo. Ese valor puede interpretarse como tiempo, número de instrucciones, número de accesos a memoria o cualquier unidad de medición definida para el análisis.

La expresión \(T(n)=c\) indica que el costo se mantiene en el mismo nivel para diferentes valores de \(n\). Si \(n=10\), \(n=10.000\) o \(n=10.000.000\), el modelo teórico asigna el mismo costo a la operación estudiada.

Esto ocurre cuando el algoritmo llega directamente a la información requerida. La operación evaluada tiene una ruta de ejecución fija: recibe la entrada, identifica la posición o dato requerido, realiza la acción y termina. El número total de elementos disponibles modifica el tamaño de la estructura, pero la operación puntual sigue ocupando el mismo lugar dentro del proceso.

En una gráfica, una función constante se representa mediante una línea horizontal. La altura de esa línea corresponde al valor de \(c\). Si la línea está más arriba, la operación tarda más en términos absolutos; si está más abajo, tarda menos. En ambos casos, el rasgo importante es la ausencia de crecimiento sostenido al aumentar \(n\).

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-2/complejidad_temporal/complejidad_constante.png" alt="Representación gráfica de 2.1.2.1 complejidad constante"><figcaption>Representación gráfica de 2.1.2.1 complejidad constante.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../0-complejidad-sublineal/">← 2.1.2.0 Complejidad sublineal</a><a class="section-step__index" href="../">Capítulo 2</a><a class="section-step__next" href="../2-complejidad-logaritmica/">2.1.2.2 Complejidad logarítmica →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
