<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# Ejemplo 5 · Búsqueda en árbol binario

<span class="chapter-kicker">Capítulo 6</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/notebooks/0_laboratorio_analisis_recursivo.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

#### Código

<!-- book-code:start -->

##### Búsqueda en un árbol binario de búsqueda

Implementación corregida basada en el libro, página 254 (Java).

=== "Java"

    ```java
    public static boolean buscar(Nodo raiz, int valor) {
        if (raiz == null)
            return false;
        if (valor == raiz.dato)
            return true;
        if (valor < raiz.dato)
            return buscar(raiz.izquierdo, valor);
        else
            return buscar(raiz.derecho, valor);
    }
    ```

=== "Pseudocódigo"

    ```text
    función buscar(raiz, valor)
        si raiz is nulo entonces
            retornar falso
        si valor == raiz.dato entonces
            retornar verdadero
        si valor < raiz.dato entonces
            retornar buscar(raiz.izquierdo, valor)
        retornar buscar(raiz.derecho, valor)
    ```

=== "Python"

    ```python
    def buscar(raiz, valor):
        if raiz is None:
            return False
        if valor == raiz.dato:
            return True
        if valor < raiz.dato:
            return buscar(raiz.izquierdo, valor)
        return buscar(raiz.derecho, valor)
    ```

=== "C"

    ```c
    #include <stdbool.h>
    #include <stdint.h>
    #include <limits.h>
    #include <stdio.h>
    #include <stdlib.h>
    #include <math.h>

    typedef struct Nodo {
        int dato;
        struct Nodo *izquierdo;
        struct Nodo *derecho;
    } Nodo;

    bool buscar(const Nodo *raiz, int valor) {
        if (raiz == NULL) {
            return false;
        }
        if (valor == raiz->dato) {
            return true;
        }
        if (valor < raiz->dato) {
            return buscar(raiz->izquierdo, valor);
        } else {
            return buscar(raiz->derecho, valor);
        }
    }
    ```

Java presenta la implementación de referencia; las otras pestañas traducen esta misma variante. En pseudocódigo, `rango(inicio, fin, paso)` excluye `fin`. Python usa enteros de precisión arbitraria; donde Java limita el resultado a `int`, se conserva esa comprobación. En C se usa `int` de 32 bits y `int64_t` para los cálculos ampliados; los errores de dominio o desbordamiento se señalan con `abort()`.

| Parámetro o variable | Significado |
| --- | --- |
| `raiz` | Nodo inicial o null. |
| `valor` | Entero buscado. |
| `dato, izquierdo, derecho` | Campos de Nodo. |

**Precondiciones:** Árbol acíclico que respeta el orden de un árbol binario de búsqueda; clase Nodo definida.

**Resultado:** Devuelve true si encuentra valor; false si llega a null.

??? example "Ejemplo paso a paso"
    Entrada: `Raíz 5, hijo izquierdo 3; valor = 3`.

    | Estado | Acción o resultado |
    | --- | --- |
    | `raiz.dato = 5` | 3 < 5: continúa por izquierdo. |
    | `raiz.dato = 3` | Coincide con valor; devuelve true. |

<div class="example-runner" data-example-runner><p><strong>Ejecutar este ejemplo</strong> · Python</p><p>Modifica las entradas o el código y consulta el resultado aquí. La primera ejecución carga Python en el navegador.</p><details><summary>Editar código y entradas</summary><label for="runner-eabf1fdbb839">Código Python · Búsqueda en un árbol binario de búsqueda</label><textarea id="runner-eabf1fdbb839" spellcheck="false" wrap="off" rows="14">def buscar(raiz, valor):
    if raiz is None:
        return False
    if valor == raiz.dato:
        return True
    if valor &lt; raiz.dato:
        return buscar(raiz.izquierdo, valor)
    return buscar(raiz.derecho, valor)

# Entradas editables del ejemplo.
from types import SimpleNamespace

raiz = SimpleNamespace(dato=5, izquierdo=SimpleNamespace(
    dato=3, izquierdo=None, derecho=None), derecho=None)
valor = 3

resultado = buscar(raiz, valor)
print(&quot;Resultado:&quot;, resultado)
</textarea></details><div class="example-runner-actions"><button type="button" data-run>Ejecutar</button><button type="button" data-stop disabled>Detener</button><button type="button" data-reset>Restablecer ejemplo</button></div><p data-status role="status">Listo para ejecutar.</p><pre data-output aria-label="Resultado de la ejecución" tabindex="0">El resultado aparecerá aquí.</pre></div>

##### Laboratorio y medición

La animación permite observar la estructura recursiva. El panel experimental ejecuta funciones Python: el tiempo y la memoria de ese panel corresponden a esas funciones y no a una ejecución del listado Java. La memoria se obtiene con tracemalloc; no mide directamente la pila de una JVM.

El panel experimental modela un camino balanceado mediante n // 2; no construye nodos ni mide una búsqueda sobre un árbol real.

[Consultar la adaptación y sus mediciones](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo6/runtime/recursive_examples_analysis.py).

<!-- book-code:end -->

#### Análisis

El mejor caso encuentra el valor en la raíz: \(\Omega(1)\). En un árbol balanceado, una búsqueda guiada por orden alcanza una profundidad \(\Theta(\log_2(n))\); en un árbol degenerado puede recorrer \(O(n)\) nodos. La memoria de la versión recursiva depende de la altura \(h\): \(S(n)\in\Theta(h)\).

#### Simulación

El laboratorio contrasta árboles balanceados y degenerados para relacionar cantidad de nodos, altura y profundidad de la pila.

<!-- figures-from-explanation:start -->
<div class="chapter-figures">
<figure><img src="../../../assets/images/capitulo-6/ejemplos/complejidad_binario.png" alt="Secuencia visual de ejemplo 5 · búsqueda en árbol binario · paso representativo 1 de 3"><figcaption>Secuencia visual de ejemplo 5 · búsqueda en árbol binario · paso representativo 1 de 3.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/comparacion_complejidad_binario_1.png" alt="Comparación de crecimiento para ejemplo 5 · búsqueda en árbol binario"><figcaption>Comparación de crecimiento para ejemplo 5 · búsqueda en árbol binario.</figcaption></figure>
<figure><img src="../../../assets/images/capitulo-6/ejemplos/comparacion_complejidad_binario_2.png" alt="Comparación de crecimiento para ejemplo 5 · búsqueda en árbol binario"><figcaption>Comparación de crecimiento para ejemplo 5 · búsqueda en árbol binario.</figcaption></figure>
</div>
<!-- figures-from-explanation:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../merge-sort/">← Ejemplo 4 · Ordenamiento por mezcla</a><a class="section-step__index" href="../">Capítulo 6</a><a class="section-step__next" href="../ejercicios-propuestos/">6.4.1 Ejercicios propuestos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>
