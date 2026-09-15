<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>

# 3.5 Tipos de notación asintótica

<span class="chapter-kicker">Capítulo 3</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo3/notebooks/0_comparacion_notaciones_asintoticas.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar simulación en Google Colab</a>
</div>

Las notaciones asintóticas formalizan distintas relaciones de crecimiento entre una función de interés \(C(n)\) y una función de referencia \(g(n)\). A continuación se presentan sus definiciones formales y sus representaciones gráficas:

- **Notación \(O\):** cota superior asintótica, con las variantes [Big-O](1-notacion-big-o.md) y [little-o](2-notacion-little-o.md).

    \[
    C(n)\in
    \begin{cases}
    O(g(n))\iff \exists c\in\mathbb{R}^{+}: C(n)\leq c\cdot g(n)\quad \forall n\ge n_0,\;n_0\in\mathbb{R}^{+} \\
    o(g(n))\iff \forall c\in\mathbb{R}^{+}: C(n)<c\cdot g(n)\quad \forall n\ge n_0,\;n_0\in\mathbb{R}^{+}
    \end{cases}
    \]

    <figure><img src="../../../assets/images/capitulo-3/comparacion_o_generica.png" alt="Gráfica genérica de la notación O"><figcaption>Notación \(O\) (representación genérica).</figcaption></figure>

- **Notación \(\Omega\):** cota inferior asintótica, con las variantes [Big-Omega](3-notacion-big-omega.md) y [little-omega](4-notacion-little-omega.md).

    \[
    C(n)\in
    \begin{cases}
    \Omega(g(n))\iff \exists c\in\mathbb{R}^{+}: C(n)\geq c\cdot g(n)\quad \forall n\ge n_0,\;n_0\in\mathbb{R}^{+} \\
    \omega(g(n))\iff \forall c\in\mathbb{R}^{+}: C(n)>c\cdot g(n)\quad \forall n\ge n_0,\;n_0\in\mathbb{R}^{+}
    \end{cases}
    \]

    <figure><img src="../../../assets/images/capitulo-3/comparacion_omega_generica.png" alt="Gráfica genérica de la notación Omega"><figcaption>Notación \(\Omega\) (representación genérica).</figcaption></figure>

- [**Notación \(\Theta\)**](5-notacion-theta.md): cota asintótica ajustada.

    \[
    C(n)\in\Theta(g(n))\iff
    \begin{cases}
    \exists (c_1,c_2)\in(\mathbb{R}^{+})^2: c_1\cdot g(n)\leq C(n)\leq c_2\cdot g(n) \\
    \forall n\ge n_0,\;n_0\in\mathbb{R}^{+}
    \end{cases}
    \]

    <figure><img src="../../../assets/images/capitulo-3/comparacion_theta_generica.png" alt="Gráfica genérica de la notación Theta"><figcaption>Notación \(\Theta\) (representación genérica).</figcaption></figure>

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Comparación interactiva de notaciones asintóticas | `jupyter lab simulaciones/capitulo3/notebooks/0_comparacion_notaciones_asintoticas.ipynb` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejemplos-concretos-notaciones/">← 3.4 Notación asintótica simplificada</a><a class="section-step__index" href="../">Capítulo 3</a><a class="section-step__next" href="../1-notacion-big-o/">3.5.1.1 Notación Big-O →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>
