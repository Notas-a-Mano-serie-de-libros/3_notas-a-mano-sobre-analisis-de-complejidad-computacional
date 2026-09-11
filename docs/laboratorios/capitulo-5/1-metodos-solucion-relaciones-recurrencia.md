# Métodos para analizar relaciones de recurrencia

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 5</span>

Una relación de recurrencia puede resolverse mediante diferentes métodos. La elección depende principalmente de la forma en que disminuye el tamaño del problema y de la estructura de sus términos recursivos.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo5/notebooks/1_metodos_solucion_relaciones_recurrencia.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" }

---

| Método | Descripción | Uso recomendado |
|---|---|---|
| **Sustitución iterativa** | Expande la relación reemplazando sucesivamente cada término recursivo por su propia definición. Las primeras expansiones permiten reconocer cómo cambian el coeficiente, el argumento de \(C(n)\) y el costo acumulado, hasta obtener una expresión general después de \(k\) sustituciones. | Relaciones de **reducción** y de **división** cuando las expansiones producen un patrón analítico. En esta simulación se limita a \(m=1\) porque el procedimiento desarrolla un único término recursivo en cada sustitución. |
| **Árbol de recurrencia** | Representa gráficamente las llamadas recursivas. Para cada nivel determina el costo de cada nodo \(f_i(n)\), el número de nodos y su producto \(C_k(n)\); después suma el costo de todos los niveles. | Relaciones de **reducción** y de **división** con árbol uniforme. Se limita a \(m=1\) para que todos los hijos sigan la misma transformación y exista un único costo \(f_i(n)\) por nivel. |
| **Teorema maestro** | Determina el crecimiento asintótico comparando \(f(n)\) con el costo crítico de las llamadas recursivas. La versión básica trata costos polinómicos, la extendida incorpora factores logarítmicos y la generalizada admite diferentes tamaños de subproblema. | Exclusivamente relaciones de **división**. Las versiones básica y extendida exigen la forma \(a \cdot C(n/b)+f(n)\) y por ello fijan \(m=1\). La versión generalizada habilita \(m>1\) porque admite varios términos \(a_iC(b_i n)\). |
| **Ecuación característica** | Separa la parte homogénea, propone \(C_h(n)=r^n\) y construye un polinomio cuyas raíces determinan la solución. Si existe \(f(n)\), añade una solución particular. | Relaciones de **reducción lineales**, con coeficientes constantes y desplazamientos enteros. Permite \(m>1\) porque cada término puede representar un retardo distinto y contribuir al polinomio característico. |

En la siguiente simulación puedes construir \(C(n)\), elegir un método compatible con el tipo de relación y observar su procedimiento de solución.
