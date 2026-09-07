<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.4.4.6 Algoritmo con estructura deliberadamente compleja

<span class="chapter-kicker">Capítulo 4</span>

Este ejemplo combina un ciclo externo, dos ciclos internos y llamadas a funciones con costos propios. Su propósito es mostrar que la apariencia del anidamiento no basta: cada cuerpo debe sustituirse por su función de costo antes de aplicar dominancia.

## Código analizado

=== "Pseudocódigo"

    ```text
    procedimiento imprimirElementos(m, n)
        para i ← 0 hasta m - 1
            imprimir i
            para j ← 0 hasta n - 1
                imprimir j
            para k ← n; k > 1; k ← ⌊k / 2⌋
                imprimir k
                foo2()
            foo1()
    ```

=== "Python"

    ```python
    def imprimir_elementos(m, n):
        for i in range(m):
            print(i)
            for j in range(n):
                print(j)
            k = n
            while k > 1:
                print(k)
                foo2()
                k //= 2
            foo1()
    ```

=== "Java"

    ```java
    static void imprimirElementos(int m, int n) {
        for (int i = 0; i < m; i++) {
            System.out.println(i);
            for (int j = 0; j < n; j++) System.out.println(j);
            for (int k = n; k > 1; k /= 2) {
                System.out.println(k);
                foo2();
            }
            foo1();
        }
    }
    ```

=== "C"

    ```c
    void imprimirElementos(int m, int n) {
        for (int i = 0; i < m; i++) {
            printf("%d\n", i);
            for (int j = 0; j < n; j++) printf("%d\n", j);
            for (int k = n; k > 1; k /= 2) {
                printf("%d\n", k);
                foo2();
            }
            foo1();
        }
    }
    ```

## Análisis esperado

El conteo debe conservar los costos de las funciones llamadas. Antes de simplificar, la forma general es \(T(n)\in O\!\left(n\,[n+\log_2(n)(1+T_{foo2}(n))+T_{foo1}(n)]\right)\). Solo después se sustituyen \(T_{foo1}\) y \(T_{foo2}\) y se aplica dominancia. La memoria suma las variables constantes y el costo lineal de `foo2`, por lo que \(S(n)\in O(n)\). La obra no propone simulación para este caso por su crecimiento deliberadamente poco habitual.

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo5-ciclos-incremento-no-lineal/">← 4.4.4.5 Ciclos con incremento no lineal</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../ejemplo7-ciclo-sin-dependencia/">4.4.4.7 Ciclo sin dependencia de la entrada →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
