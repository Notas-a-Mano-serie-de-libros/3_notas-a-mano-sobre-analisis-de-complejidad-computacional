<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>

# 3.6 Ejercicios propuestos

<span class="chapter-kicker">Capítulo 3</span>

Esta sección reúne los problemas destinados a comprobar relaciones asintóticas, seleccionar funciones de referencia y justificar cotas mediante desigualdades o límites. Los enunciados completos quedan disponibles en HTML; el PDF se conserva únicamente como versión descargable.

## Comportamiento asintótico general

Para cada función, identifique una función de referencia asintóticamente ajustada cuando \(n\to\infty\). Simplifique productos antes de elegir el término dominante.

1. \(5 \cdot n+10\)
2. \(n^2+3 \cdot n+7\)
3. \((2 \cdot n+5) \cdot (3 \cdot n+7)+n\)
4. \(4 \cdot n \cdot \log(n)+20 \cdot n\)
5. \(3 \cdot n^3+2 \cdot n^2+5\)
6. \((n^2+2 \cdot n) \cdot (3 \cdot n+1)+10 \cdot n\)
7. \((4 \cdot n^3+n^2) \cdot (n+1)+5 \cdot n\)
8. \(2^n+n^2+n \cdot \log(n)\)
9. \(n!+2 \cdot n^2\)
10. \(3(n^3+5 \cdot n)+(2 \cdot n^3-3 \cdot n)\)
11. \((n^4+n^3) \cdot (n+\log(n))+n^5\)
12. \(n!+(3 \cdot n+5) \cdot (n^2+1)+2^{2 \cdot n}\)
13. \((2 \cdot n^3+n^2) \cdot (n^2+n \cdot \log(n))+4^n\)
14. \(n^3 \cdot \log(n)+n^2 \cdot \log^2(n)+n^3 \cdot \log^2(n)\)
15. \(5 \cdot n!+n^n+2^n\)
16. \((n^3+n^{1.5}) \cdot (\sqrt n+\log^2(n)))+(2^{n/2}+n \cdot \log(n))\)
17. \(((e^n+n!) \cdot (n+\log(n)))+(n^3+\ln(n!))\)
18. \((n^{1.2}+n \cdot \log^3(n))+((n^n+n^{0.5}) \cdot (n \cdot \log(n)))\)
19. \((\ln(n!)+3^{n/2})+((n^4+n^{3.5}) \cdot (\log^2(n)+\sqrt n))\)
20. \(((n^n+e^{n/3}) \cdot (n^{0.7}+n^2 \cdot \log(n)))+((n!)^2+n^5)\)
21. \(((n^5+n^{2.5}) \cdot (\log(n)+n^{0.3}))+(4^n+n \cdot \log^2(n))\)
22. \(((\ln(n!)+n^{1.1}) \cdot (n^3+\log^3(n)))+(e^n+n^5)\)
23. \((n^n+n^{1.8} \cdot \log(n))+((n^3+3^{n/2}) \cdot (\sqrt n+n^{0.9}))\)
24. \(((n^4+n \cdot \log(n)) \cdot (2^n+n!))+(n^2\ln(n!)+n^{3.2})\)
25. \(2 \cdot n+n^n+n^{1.3}+n \cdot \log^3(n)+3^n+n^{1.5}\)

## Verificación mediante límites

Determine si cada afirmación es verdadera. No basta con indicar “sí” o “no”: plantee el cociente apropiado, evalúe su límite y relacione el resultado con la definición de la notación.

1. \(3 \cdot n^2+2 \cdot n\in O(n^2)\)
2. \(n^3+5 \cdot n^2\in O(n^2)\)
3. \(n^2+\log(n)\in\Theta(n^2)\)
4. \(4 \cdot n^3+n\in\omega(n^3)\)
5. \(2 \cdot n+1\in\Omega(\log(n))\)
6. \(n^4+2 \cdot n^3+n\in O(n^5)\)
7. \(2^n+n^3\in\Theta(2^n)\)
8. \(\sqrt n+n\in O(n)\)
9. \(\ln(n)+n\in\Theta(n^2)\)
10. \(n \cdot \log(n)+n\in O(n)\)
11. \(3^n+n^2\in O(3^n)\)
12. \(n^{1.5}+n\in\Theta(n^{1.5})\)
13. \(n^n+n^2\in\Omega(n^{n+1})\)
14. \((n^2+1)\log(n)\in O(n^3)\)
15. \(5 \cdot n^3+n^4\in\Omega(n^4)\)
16. \(n!+2^n\in\omega(n!)\)
17. \(n^5+n \cdot \log(n)\in O(n^6)\)
18. \(4^n+n^3\in\Theta(4^n)\)
19. \(2^n+\sqrt n\in\Omega(2^n)\)
20. \(\log^3(n)+\log^2(n)\in O(\log^3(n))\)

<div class="lab-action">
<a class="md-button md-button--primary pdf-button" href="../../../assets/pdfs/capitulo-3-ejercicios-propuestos.pdf" target="_blank" rel="noopener noreferrer"><span class="pdf-button__icon" aria-hidden="true">📖</span> CONSULTAR EJERCICIOS PROPUESTOS</a>
<small class="lab-action__note">Versión descargable con la numeración de la obra.</small>
</div>

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../5-notacion-theta/">← 3.5.3 Notación Θ</a><a class="section-step__index" href="../">Capítulo 3</a><a class="section-step__next" href="../practica-autocorregible/">Ejercicios complementarios →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../capitulo-2/">← Capítulo 2</a><a class="chapter-nav__index" href="../">Capítulo 3</a><a class="chapter-nav__next" href="../../capitulo-4/">Capítulo 4 →</a></nav>
