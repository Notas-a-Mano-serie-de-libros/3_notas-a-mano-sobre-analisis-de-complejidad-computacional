<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.2 Ejercicios propuestos

<span class="chapter-kicker">Capítulo 2</span>

Los ejercicios cierran el capítulo y permiten aplicar las funciones de complejidad, distinguir tiempo y espacio, y comparar órdenes de crecimiento. Los enunciados completos se presentan a continuación para que esta página pueda estudiarse sin abrir otro formato.

Utilice, cuando corresponda, las expresiones simplificadas:

\[
t=T_0\cdot T(n),\qquad s=S_0\cdot S(n).
\]

1. Una máquina consume \(0{,}001\) segundos por operación y 8 bytes de memoria por instrucción. Calcule el tiempo total y el consumo teórico para \(n=10^6\) con:

    - \(T(n)=n\), \(S(n)=n\).
    - \(T(n)=n \cdot \log_2(n)\), \(S(n)=\log_2(n)\).
    - \(T(n)=\sqrt n\), \(S(n)=\log_2^2(n)\).

2. Una operación toma en promedio \(0{,}002\) segundos y \(T(n)=n^3\). Para \(n=500\), determine el tiempo total y cuántas instrucciones caben en 1 GB si cada una consume 16 bytes.
3. Un algoritmo tiene \(T(n)=2^n\), \(S(n)=n!\), \(T_0=0{,}0005\) segundos y \(S_0=4\) bytes. Determine tiempo y espacio para \(n\in\{1,10,1000,10000\}\) y discuta cuándo dejan de ser representables o practicables.
4. Un sistema debe procesar \(10^6\) datos en menos de 10 segundos y ejecuta una instrucción cada \(0{,}001\) segundos. Determine qué familias de complejidad temporal podrían satisfacer la restricción y justifique los supuestos.
5. Compare \(T_1(n)=n \cdot \log_2(n)\), \(T_2(n)=n^2\) y \(T_3(n)=10 \cdot n^2\), con \(T_0=0{,}002\) segundos. Calcule el tiempo para \(n=10^5\) y determine cuál tarda menos para 5000 datos.
6. Diseñe una restricción de costo para procesar \(10^7\) datos en menos de 5 segundos y determine qué funciones de complejidad podrían cumplirla. Declare primero la tasa de operaciones asumida.
7. Una máquina dispone de 128 MB. Determine órdenes tentativos de complejidad espacial que permitan procesar \(10^5\) datos e indique el costo por unidad que está suponiendo.
8. Estime el tiempo para procesar \(10^6\) datos con \(T(n)=n!\) si cada instrucción toma \(10^{-5}\) segundos. Explique cómo comunicar el resultado cuando supera los límites numéricos habituales.
9. Un algoritmo con \(S(n)=n \cdot \log_2(n)\) consume 16 bytes por operación. Calcule los kilobytes decimales y kibibytes binarios consumidos para \(n=10000\).
10. Calcule el tiempo para 20 datos con \(T(n)=2^n\) y un segundo por instrucción. ¿Es útil el resultado en la práctica?
11. Un algoritmo cuadrático tarda \(0{,}01\) segundos con 1000 datos. Estime el tiempo para 100000 datos, suponiendo que la constante y el entorno se mantienen estables.
12. Se deben procesar 10000 datos en menos de un segundo en una máquina que ejecuta \(10^7\) instrucciones por segundo. Identifique los órdenes temporales que cumplen la restricción.
13. Un sistema usa \(S(n)=2^n\) y procesa 20 datos. Determine cuánta memoria requeriría para 25 datos bajo el mismo costo por unidad y elija una unidad apropiada.
14. Un sistema embebido ejecuta \(10^6\) operaciones por segundo y dispone de 1 MB. Determine qué órdenes temporales y espaciales permitirían procesar 5000 datos. Declare el consumo unitario supuesto.
15. Un algoritmo \(n \cdot \log_2(n)\) tarda 2 segundos con 1000 datos. Estime si puede procesar 10000 datos en menos de 10 segundos bajo el mismo modelo.

## Orientación para resolverlos

En cada respuesta identifique primero \(n\), la función de costo y la constante física. Conserve las unidades durante todo el cálculo y distinga una predicción del modelo de una medición real. Si el enunciado no aporta una constante necesaria, declárela explícitamente en lugar de ocultar el supuesto.

<div class="lab-action">
<a class="md-button md-button--primary pdf-button" href="../../../assets/pdfs/capitulo-2-ejercicios-propuestos.pdf" target="_blank" rel="noopener noreferrer"><span class="pdf-button__icon" aria-hidden="true">📖</span> CONSULTAR EJERCICIOS PROPUESTOS</a>
<small class="lab-action__note">Versión descargable con la numeración de la obra.</small>
</div>

Para entrenar con problemas generados de forma continua con retroalimentación inmediata, continúe a los [ejercicios complementarios](practica-autocorregible.md).

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../9-complejidad-factorial/">← 2.1.2.9 Complejidad factorial</a><a class="section-step__index" href="../">Capítulo 2</a><a href="../practica-autocorregible/">Ejercicios complementarios →</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
