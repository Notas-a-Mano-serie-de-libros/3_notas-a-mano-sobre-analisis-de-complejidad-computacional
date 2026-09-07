<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>

# 5.5.4 Ecuación característica

<span class="chapter-kicker">Capítulo 5</span>

<div class="lab-action">
<a class="md-button md-button--primary colab-button" href="https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo5/notebooks/1_metodos_solucion_relaciones_recurrencia.ipynb" target="_blank" rel="noopener noreferrer">Ejecutar notebook en Google Colab</a>
<small class="lab-action__note">Se abrirá en una pestaña nueva.</small>
</div>

La ecuación característica resuelve recurrencias lineales de reducción con coeficientes constantes. Separa la parte homogénea y propone una solución exponencial \(T_h(n)=r^n\), con la que se obtiene un polinomio en \(r\).

### Procedimiento

1. Lleve todos los términos homogéneos a un lado.
2. Sustituya \(T_h(n)=r^n\) y construya el polinomio característico.
3. Halle sus raíces y considere su multiplicidad.
4. Si existe un término no homogéneo, proponga una solución particular compatible.
5. Use las condiciones iniciales para determinar las constantes.

Las raíces distintas, repetidas o complejas producen formas de solución diferentes. El método no se aplica directamente a coeficientes variables ni a argumentos como \(n/2\).

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../teorema-maestro/">← 5.5.3 Teorema maestro</a><a class="section-step__index" href="../">Capítulo 5</a><a class="section-step__next" href="../ejercicios-propuestos/">5.6.1 Ejercicios propuestos →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-4/">← Capítulo 4</a><a class="chapter-nav__index" href="../">Capítulo 5</a><a class="chapter-nav__next" href="../../capitulo-6/">Capítulo 6 →</a></nav>
