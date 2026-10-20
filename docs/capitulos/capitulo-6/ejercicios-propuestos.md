<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>

# 6.4.1 Ejercicios propuestos

<span class="chapter-kicker">Capítulo 6</span>

Para cada algoritmo determine: (i) el tamaño de entrada; (ii) el caso base; (iii) la relación de recurrencia temporal; (iv) su solución asintótica; y (v) el espacio auxiliar de la pila. Los enunciados completos y el código están disponibles en esta página.

## 1. Búsqueda binaria recursiva

```java
public int buscar(int[] arr, int izq, int der, int x) {
    if (izq > der) {
        return -1;
    }
    int medio = izq + (der - izq) / 2;
    if (arr[medio] == x) {
        return medio;
    } else if (arr[medio] > x) {
        return buscar(arr, izq, medio - 1, x);
    }
    return buscar(arr, medio + 1, der, x);
}
```

## 2. Máximo común divisor mediante Euclides

```java
public int mcd(int a, int b) {
    if (b == 0) {
        return a;
    }
    return mcd(b, a % b);
}
```

## 3. Coeficiente binomial

```java
public int combinar(int n, int k) {
    if (k == 0 || k == n) {
        return 1;
    }
    return combinar(n - 1, k - 1) + combinar(n - 1, k);
}
```

## 4. Suma de un arreglo

```java
public int sumaArreglo(int[] arr, int n) {
    if (n == 0) {
        return 0;
    }
    return arr[n - 1] + sumaArreglo(arr, n - 1);
}
```

## 5. Torres de Hanói

```java
public void hanoi(int n, char origen, char aux, char destino) {
    if (n <= 0) {
        return;
    }
    hanoi(n - 1, origen, destino, aux);
    // Mover el disco n de origen a destino.
    hanoi(n - 1, aux, origen, destino);
}
```

## 6. Inversión de una cadena

```java
public String invertir(String str) {
    if (str.isEmpty()) {
        return str;
    }
    return invertir(str.substring(1)) + str.charAt(0);
}
```

Al analizar este ejercicio, declare si la operación `substring` copia caracteres o crea una vista en la versión concreta de Java. El costo de esa operación cambia el resultado temporal y espacial.

## 7. Suma de dígitos

```java
public int sumaDigitos(int n) {
    if (n == 0) {
        return 0;
    }
    return (n % 10) + sumaDigitos(n / 10);
}
```

## Preguntas transversales

1. ¿Qué ejercicios generan una sola llamada por nivel y cuáles generan dos?
2. ¿En cuáles la profundidad depende de \(n\), de \(\log(n)\) o de dos parámetros?
3. ¿Qué complejidades cambiarían si se incorporara memoización?
4. ¿Qué diferencia existe entre el tamaño numérico de un entero y su cantidad de dígitos?

<div class="lab-action">
<a class="md-button md-button--primary pdf-button" href="../../../assets/pdfs/capitulo-6-ejercicios-propuestos.pdf" target="_blank" rel="noopener noreferrer"><span class="pdf-button__icon" aria-hidden="true">📖</span> CONSULTAR EJERCICIOS PROPUESTOS</a>
<small class="lab-action__note">Versión descargable con las soluciones de referencia.</small>
</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../arbol-binario/">← Ejemplo 5 · Búsqueda en árbol binario</a><a class="section-step__index" href="../">Capítulo 6</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-5/">← Capítulo 5</a><a class="chapter-nav__index" href="../">Capítulo 6</a><a class="chapter-nav__next" href="../../capitulo-7/">Capítulo 7 →</a></nav>
