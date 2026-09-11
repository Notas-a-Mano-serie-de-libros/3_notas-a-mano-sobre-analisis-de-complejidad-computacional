<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../consideraciones-teoricas/">← Consideraciones teóricas</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-2/">Capítulo 2 →</a></nav>

# Capítulo 1 · Introducción

<span class="chapter-kicker">Páginas 49–58</span>

Que un programa funcione es apenas el primer criterio de calidad. Cuando crecen los datos, la cantidad de usuarios o las restricciones operativas, también importa cuánto tarda una solución, cuánta memoria utiliza y cómo se comporta bajo demanda. El análisis de complejidad proporciona un lenguaje formal para estudiar esas preguntas antes de depender exclusivamente de mediciones.

<section class="chapter-sections" aria-labelledby="chapter-sections-title">
<h2 id="chapter-sections-title">Secciones del capítulo</h2>
<div class="chapter-index chapter-index--sections">
<a class="chapter-entry" href="#11-conceptos-iniciales"><span class="chapter-entry__number">1.1</span><strong>Conceptos iniciales</strong><span>Diferencia algoritmo, análisis de algoritmos y complejidad computacional.</span></a>
<a class="chapter-entry" href="#12-contexto-historico"><span class="chapter-entry__number">1.2</span><strong>Contexto histórico</strong><span>Recorre los hitos que condujeron desde la automatización hasta la teoría de la complejidad.</span></a>
<a class="chapter-entry" href="#13-de-vuelta-al-contexto-actual"><span class="chapter-entry__number">1.3</span><strong>De vuelta al contexto actual</strong><span>Relaciona el análisis crítico con el desarrollo de software y la inteligencia artificial.</span></a>
</div>
</section>

## 1.1 Conceptos iniciales

| Concepto | Pregunta central | Alcance |
| --- | --- | --- |
| Algoritmo | ¿Qué secuencia finita y precisa transforma las entradas en resultados? | Describe un procedimiento para resolver una clase de problemas. |
| Análisis de algoritmos | ¿Cuánto cuesta una solución concreta ante entradas distintas? | Estudia tiempo, espacio y otros recursos de una implementación. |
| Complejidad computacional | ¿Qué dificultad posee el problema con independencia de una solución particular? | Clasifica clases de problemas mediante modelos formales. |

Un algoritmo debe terminar, expresar sus pasos sin ambigüedad y establecer la relación entre sus entradas y salidas. Analizarlo permite anticipar riesgos de rendimiento; estudiar la complejidad del problema amplía la mirada hacia los límites de las soluciones posibles.

## 1.2 Contexto histórico

El recorrido comienza con la automatización del cálculo propuesta por Charles Babbage y Ada Lovelace, continúa con los modelos abstractos de Alan Turing y Alonzo Church y llega a la formalización de la complejidad durante el siglo XX.

| Etapa | Aporte al campo |
| --- | --- |
| Siglo XIX | Aparecen instrucciones concebidas para una máquina y la idea de un procedimiento reproducible. |
| Década de 1930 | La computabilidad adquiere modelos matemáticos formales. |
| Décadas de 1960–1970 | El tiempo polinomial, P versus NP, las reducciones y la NP-completitud permiten clasificar problemas. |
| Final del siglo XX | Se consolidan la complejidad espacial, probabilística, de comunicación y parametrizada. |
| Siglo XXI | Datos masivos, nube, inteligencia artificial, criptografía poscuántica y computación cuántica amplían las preguntas de eficiencia. |

La notación asintótica se convierte en el lenguaje común para expresar órdenes de crecimiento y comparar algoritmos sin atarlos a una máquina específica.

## 1.3 De vuelta al contexto actual

La inteligencia artificial generativa puede producir código funcional con gran rapidez, pero no elimina la necesidad de comprenderlo. Una revisión responsable todavía debe preguntar:

- qué razonamiento dio lugar a la solución;
- si podría reconstruirse y explicarse sin confiar ciegamente en una herramienta;
- si cumple criterios de eficiencia, seguridad y escalabilidad;
- qué restricciones del problema y del entorno fueron asumidas.

El propósito de la obra nace de esta exigencia: desarrollar una base crítica y metódica para diseñar y evaluar soluciones mediante criterios cuantificables.

!!! note "Idea central"
    La experimentación muestra lo que ocurrió en una ejecución; el análisis formal ayuda a explicar y anticipar lo que puede ocurrir cuando cambia el tamaño del problema.

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../consideraciones-teoricas/">← Consideraciones teóricas</a><a class="chapter-nav__index" href="../">Recorrido</a><a class="chapter-nav__next" href="../capitulo-2/">Capítulo 2 →</a></nav>
