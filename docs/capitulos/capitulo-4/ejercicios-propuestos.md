<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>

# 4.6 Ejercicios propuestos

<span class="chapter-kicker">Capítulo 4</span>

Calcule la complejidad temporal y espacial teórica de cada fragmento. Indique el tamaño de entrada, cuente las operaciones dominantes y analice por separado los caminos que dependan de una condición. Los enunciados completos se presentan en HTML.

## Ejercicios 1–3 · Operaciones y decisiones

1. **Asignación y retorno de enteros**

    ```java
    public int asignacion() {
        int x = 10, y = 20;
        return x + y;
    }
    ```

2. **Retorno basado en una condición compuesta**

    ```java
    public boolean validacion() {
        return true || false && true && false || true;
    }
    ```

    Considere además el efecto de la evaluación de cortocircuito.

3. **Clasificación de un número**

    ```java
    public String evaluarNumero(int n) {
        if (n > 0) return "Positivo";
        else if (n < 0) return "Negativo";
        else return "Cero";
    }
    ```

## Ejercicios 4–7 · Ciclos simples

4. **Suma de los elementos de un arreglo**

    ```java
    public int sumaElementos(int[] arreglo) {
        int suma = 0;
        for (int i = 0; i < arreglo.length; i++) {
            suma += arreglo[i];
        }
        return suma;
    }
    ```

5. **Múltiplos de un número**

    ```java
    public void imprimirMultiplosDe(int multiplo, int n) {
        if (n < multiplo) return;
        int i = multiplo;
        while (i <= n) {
            System.out.println(i);
            i += multiplo;
        }
    }
    ```

    Exprese el número de iteraciones en función de \(n\) y `multiplo`; no suponga que ambos parámetros crecen de la misma forma.

6. **División logarítmica**

    ```java
    public void divisionLogaritmica(int n) {
        int count = 0;
        while (n > 1) {
            n = n / 2;
            count++;
        }
        System.out.println("Número de divisiones: " + count);
    }
    ```

7. **Prueba de primalidad**

    ```java
    public boolean esPrimo(int n) {
        if (n <= 1) return false;
        for (int i = 2; (long) i * i <= n; i++) {
            if (n % i == 0) return false;
        }
        return true;
    }
    ```

    Compare el mejor caso —cuando se encuentra pronto un divisor— con el peor caso.

## Ejercicios 8–10 · Ciclos anidados

8. **Todas las parejas de posiciones de un arreglo**

    ```java
    public void imprimirPares(int[] arr) {
        for (int i = 0; i < arr.length; i++) {
            for (int j = i + 1; j < arr.length; j++) {
                System.out.println(arr[i] + "," + arr[j]);
            }
        }
    }
    ```

9. **Parejas de elementos iguales**

    ```java
    public void imprimirParesIguales(int[] arr) {
        for (int i = 0; i < arr.length; i++) {
            for (int j = i + 1; j < arr.length; j++) {
                if (arr[i] == arr[j]) {
                    System.out.println(arr[i] + "," + arr[j]);
                }
            }
        }
    }
    ```

    Distinga el costo de comparar del costo de imprimir y declare cuál de los dos está modelando.

10. **Multiplicación de matrices cuadradas**

    ```java
    public int[][] multiplicar(int[][] a, int[][] b) {
        int n = a.length;
        int[][] resultado = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    resultado[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        return resultado;
    }
    ```

## Ejercicios 11–15 · Costos compuestos

11. **Divisiones sucesivas**

    ```java
    public int contarDivisiones(int n) {
        int contador = 0;
        while (true) {
            if (n <= 1) break;
            n = n / 2;
            contador++;
        }
        return contador;
    }
    ```

12. **Incrementos de dos unidades**

    ```java
    public void cicloConIncrementoDoble(int n) {
        for (int i = 0; i < n; i += 2) {
            foo1();
        }
    }
    ```

    Suponga \(T_{foo1}(n)=\log_2(n)\) y \(S_{foo1}(n)=n\).

13. **Invocación anidada**

    ```java
    public boolean esPrimoAnidado(int n) {
        return esPrimo(n);
    }
    ```

    Suponga \(T_{esPrimo}(n)=\sqrt n\) y \(S_{esPrimo}(n)=1\).

14. **Ciclos y funciones con costos distintos**

    ```java
    public void dosCiclos(int n) {
        for (int i = 0; i < n; i++) {
            foo1(i);
        }
        int j = 1;
        while (j < n) {
            foo2();
            j *= 2;
        }
        foo3();
    }
    ```

    \[
    \begin{aligned}
    T_{foo1}(n)&=3 \cdot n!+5 \cdot n,& S_{foo1}(n)&=n,\\
    T_{foo2}(n)&=2 \cdot n^2+3,& S_{foo2}(n)&=1,\\
    T_{foo3}(n)&=n+5,& S_{foo3}(n)&=\log_2(n).
    \end{aligned}
    \]

    Al calcular el espacio, indique si las llamadas son secuenciales o simultáneas; sumar memoria que ya fue liberada puede sobreestimar el máximo ocupado.

15. **Funciones arbitrarias secuenciales**

    ```java
    public void foo() {
        foo1();
        foo2();
    }
    ```

    \[
    \begin{aligned}
    T_{foo1}(n)&=\sqrt n,&S_{foo1}(n)&=n,\\
    T_{foo2}(n)&=\log_2(n),&S_{foo2}(n)&=n.
    \end{aligned}
    \]

## Criterio de entrega

Para cada ejercicio escriba la función de costo antes de simplificarla, separe mejor y peor caso cuando proceda, y explique si el espacio de varias operaciones debe sumarse o calcularse como un máximo.

<div class="lab-action">
<a class="md-button md-button--primary pdf-button" href="../../../assets/pdfs/capitulo-4-ejercicios-propuestos.pdf" target="_blank" rel="noopener noreferrer"><span class="pdf-button__icon" aria-hidden="true">📖</span> CONSULTAR EJERCICIOS PROPUESTOS</a>
<small class="lab-action__note">Versión descargable con las soluciones de referencia.</small>
</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplo10/">← 4.4.4.10 Algoritmo costoso por diseño</a><a class="section-step__index" href="../">Capítulo 4</a><a class="section-step__next" href="../practica-autocorregible/">Ejercicios complementarios →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-3/">← Capítulo 3</a><a class="chapter-nav__index" href="../">Capítulo 4</a><a class="chapter-nav__next" href="../../capitulo-5/">Capítulo 5 →</a></nav>
