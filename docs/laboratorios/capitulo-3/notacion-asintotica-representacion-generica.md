# Comportamiento asintótico general

<span class="chapter-kicker">Capítulo 3</span>

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo3/notebooks/notacion_asintotica_representacion_generica.ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

La obra parte de una función compuesta por términos ordenados de menor a mayor crecimiento:

\[
f(n)=\sum_{i=1}^{m}f_i(n),
\qquad
f_1(n)\prec f_2(n)\prec\cdots\prec f_m(n)
\]

Al dividir por el término dominante y llevar la razón al límite se obtiene:

\[
\lim_{n\to\infty}\frac{f(n)}{f_m(n)}
=1+\sum_{i=1}^{m-1}\lim_{n\to\infty}\frac{f_i(n)}{f_m(n)}=1
\]

Por tanto, \(f(n)\sim f_m(n)\): para entradas suficientemente grandes, su comportamiento está determinado por el término de mayor crecimiento. En un polinomio domina el término de mayor grado; en una suma que contiene un término exponencial y términos polinómicos, domina el exponencial.

Este razonamiento produce la jerarquía funcional asintótica:

\[
1\prec\log_\ell(n)\prec n\prec n \cdot \log_\ell(n)\prec n^2\prec n^3
\prec\cdots\prec n^k\prec2^n\prec n!
\]

La jerarquía compara tendencias teóricas y no sustituye el costo exacto de una implementación.

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Notacion Asintotica Representacion Generica | `jupyter lab simulaciones/capitulo3/notebooks/notacion_asintotica_representacion_generica.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->
