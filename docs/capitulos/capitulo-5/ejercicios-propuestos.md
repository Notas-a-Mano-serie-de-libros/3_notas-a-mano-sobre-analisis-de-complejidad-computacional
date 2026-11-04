<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>

# 5.6.1 Ejercicios propuestos

<span class="chapter-kicker">Capítulo 5</span>

Los ejercicios consolidan las técnicas del capítulo. Resuelva cada recurrencia por al menos un método y, cuando las condiciones lo permitan, compruebe el resultado mediante otro. Los enunciados completos están disponibles en esta página.

1. **Relación lineal básica**

    \[
    C(n)=\begin{cases}1&n=1,\\C(n-1)+1&n>1.\end{cases}
    \]

2. **Suma de los primeros números naturales**

    \[
    C(n)=\begin{cases}1&n=1,\\C(n-1)+n&n>1.\end{cases}
    \]

3. **Relación cuadrática simple**

    \[
    C(n)=\begin{cases}1&n=1,\\C(n-1)+n^2&n>1.\end{cases}
    \]

4. **Costo constante en cada paso**, con \(c>0\)

    \[
    C(n)=\begin{cases}c&n=1,\\C(n-1)+c&n>1.\end{cases}
    \]

5. **División binaria básica**

    \[
    C(n)=\begin{cases}1&n=1,\\2C(n/2)+1&n>1.\end{cases}
    \]

6. **Reducción con crecimiento logarítmico**

    \[
    C(n)=\begin{cases}1&n=1,\\C(n-1)+\log(n)&n>1.\end{cases}
    \]

7. **Relación lineal con factor constante**

    \[
    C(n)=\begin{cases}1&n=1,\\2C(n-1)+1&n>1.\end{cases}
    \]

8. **División con crecimiento lineal por nivel**

    \[
    C(n)=\begin{cases}1&n=1,\\2C(n/2)+n&n>1.\end{cases}
    \]

9. **División tripartita**

    \[
    C(n)=\begin{cases}1&n=1,\\3C(n/3)+n&n>1.\end{cases}
    \]

10. **Divisiones múltiples con costo cuadrático**

    \[
    C(n)=\begin{cases}1&n=1,\\4C(n/2)+n^2&n>1.\end{cases}
    \]

11. **Relación factorial**

    \[
    C(n)=\begin{cases}1&n=1,\\n \cdot C(n-1)&n>1.\end{cases}
    \]

12. **Suma de dos términos anteriores**

    \[
    C(n)=\begin{cases}1&n=1,\\2&n=2,\\C(n-1)+C(n-2)+n&n>2.\end{cases}
    \]

13. **División con término cúbico**

    \[
    C(n)=\begin{cases}1&n=1,\\2C(n/2)+n^3&n>1.\end{cases}
    \]

14. **División con costo exponencial**

    \[
    C(n)=\begin{cases}1&n=1,\\2C(n/2)+2^n&n>1.\end{cases}
    \]

15. **Relación factorial con suma acumulada**

    \[
    C(n)=\begin{cases}1&n=1,\\n \cdot C(n-1)+\displaystyle\sum_{k=1}^{n}k&n>1.\end{cases}
    \]

## Guía de comprobación

Para cada solución indique el caso base, el método empleado, la expresión intermedia y la familia asintótica. Cuando use el teorema maestro, compruebe primero que la recurrencia tiene la forma requerida; no lo aplique a relaciones como \(C(n-1)\) o a ramas de tamaños distintos.

<div class="lab-action">
<a class="md-button md-button--primary pdf-button" href="../../../assets/pdfs/capitulo-5-ejercicios-propuestos.pdf" target="_blank" rel="noopener noreferrer"><span class="pdf-button__icon" aria-hidden="true">📖</span> CONSULTAR EJERCICIOS PROPUESTOS</a>
<small class="lab-action__note">Versión descargable con las soluciones de referencia.</small>
</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ecuacion-caracteristica/">← 5.5.5 Ecuación característica</a><a class="section-step__index" href="../">Capítulo 5</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>
