<nav class="chapter-nav" aria-label="Navegación superior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>

# 2.3 Ejercicios complementarios

<span class="chapter-kicker">Extensión digital · Capítulo 2</span>

Esta sección complementa la lectura del capítulo con actividades interactivas diseñadas para afianzar las propiedades formales de las funciones de complejidad, el cálculo canónico de tiempo y recursos ($t = T_0 \cdot T(n)$ y $s = S_0 \cdot S(n)$), los puntos de cruce entre familias y la simulación interactiva de viabilidad física computacional. Cada intento genera nuevos parámetros y el avance se conserva localmente en su navegador.

<div class="self-check-practice" data-chapter2-practice data-storage-key="notas-a-mano:practica:capitulo-2:v1">
  <section class="self-check-practice__summary" aria-labelledby="practice-progress-title">
    <div>
      <p class="self-check-practice__eyebrow">Progreso en este navegador</p>
      <h2 id="practice-progress-title">Dominio del capítulo</h2>
    </div>
    <dl class="self-check-practice__stats">
      <div><dt>Resueltos</dt><dd data-practice-correct>0</dd></div>
      <div><dt>Intentos</dt><dd data-practice-attempts>0</dd></div>
      <div><dt>Mejor racha</dt><dd data-practice-best>0</dd></div>
    </dl>
  </section>

  <div class="self-check-practice__mastery" aria-label="Avance por habilidad">
    <div><span>Propiedades formales</span><meter min="0" max="3" value="0" data-mastery="properties">0 de 3</meter><small data-mastery-label="properties">0/3</small></div>
    <div><span>Fórmulas canónicas</span><meter min="0" max="3" value="0" data-mastery="canonical">0 de 3</meter><small data-mastery-label="canonical">0/3</small></div>
    <div><span>Puntos de cruce</span><meter min="0" max="3" value="0" data-mastery="crossover">0 de 3</meter><small data-mastery-label="crossover">0/3</small></div>
    <div><span>Viabilidad y escala</span><meter min="0" max="3" value="0" data-mastery="viability">0 de 3</meter><small data-mastery-label="viability">0/3</small></div>
  </div>

  <nav class="self-check-practice__modes" aria-label="Tipo de ejercicio">
    <button type="button" data-practice-mode="properties" aria-pressed="true"><span>1. Propiedades de C(n)</span></button>
    <button type="button" data-practice-mode="canonical" aria-pressed="false"><span>2. Cálculo canónico t y s</span></button>
    <button type="button" data-practice-mode="crossover" aria-pressed="false"><span>3. Puntos de cruce</span></button>
    <button type="button" data-practice-mode="viability" aria-pressed="false"><span>4. Viabilidad y escala</span></button>
  </nav>

  <section class="self-check-practice__exercise" aria-labelledby="practice-exercise-title">
    <div class="self-check-practice__exercise-heading">
      <div>
        <p class="self-check-practice__eyebrow" data-practice-level>Nivel 1 · Fundamentos matemáticos</p>
        <h2 id="practice-exercise-title" data-practice-title>Propiedades formales de las funciones de complejidad</h2>
      </div>
      <button class="md-button self-check-practice__secondary" type="button" data-practice-new><span class="self-check-practice__button-icon" aria-hidden="true">↻</span><span>Otro ejercicio</span></button>
    </div>
    <div data-practice-question></div>
    <div class="self-check-practice__actions">
      <button class="md-button md-button--primary" type="button" data-practice-check><span class="self-check-practice__button-icon" aria-hidden="true">✓</span><span data-practice-check-label>Comprobar respuesta</span></button>
      <button class="md-button self-check-practice__secondary" type="button" data-practice-hint><span class="self-check-practice__button-icon" aria-hidden="true">◇</span><span>Ver una pista</span></button>
    </div>
    <div class="self-check-practice__feedback" data-practice-feedback role="status" aria-live="polite" tabindex="-1"></div>
  </section>

  <footer class="self-check-practice__footer">
    <p>El progreso se guarda de manera local en este dispositivo. Cada módulo se considera afianzado tras alcanzar 3 aciertos.</p>
    <button class="self-check-practice__reset" type="button" data-practice-reset><span class="self-check-practice__button-icon" aria-hidden="true">↺</span><span>Reiniciar progreso</span></button>
  </footer>
</div>

## Recomendaciones para el cálculo

Para resolver los problemas del módulo canónico, recuerde las relaciones presentadas en el libro:

$$t = T_0 \cdot T(n) \qquad s = S_0 \cdot S(n)$$

donde $T_0$ denota el tiempo medio por operación básica y $S_0$ el costo unitario de memoria por dato.

### Múltiplos del byte: Sistema Internacional (SI) vs. Norma ISO/IEC 80000-13

En computación conviven dos convenciones para expresar cantidades de memoria: el sistema decimal (base 10, SI) utilizado habitualmente por fabricantes de almacenamiento, y el sistema binario (base 2, ISO/IEC 80000-13) que rige la arquitectura interna de direccionamiento digital:

| Magnitud | Sistema Internacional (SI) | Cantidad en bytes (SI) | Norma ISO/IEC 80000-13 | Cantidad en bytes (Binario) |
| :--- | :--- | :--- | :--- | :--- |
| **Byte** | Byte [B] | $10^0 = 1$ | Byte [B] | $2^0 = 1$ |
| **Kilo / Kibi** | Kilobyte [KB] | $10^3 = 1\,000$ | Kibibyte [KiB] | $2^{10} = 1\,024$ |
| **Mega / Mebi** | Megabyte [MB] | $10^6 = 1\,000\,000$ | Mebibyte [MiB] | $2^{20} = 1\,048\,576$ |
| **Giga / Gibi** | Gigabyte [GB] | $10^9 = 1\,000\,000\,000$ | Gibibyte [GiB] | $2^{30} = 1\,073\,741\,824$ |
| **Tera / Tebi** | Terabyte [TB] | $10^{12} = 1\,000\,000\,000\,000$ | Tebibyte [TiB] | $2^{40} = 1\,099\,511\,627\,776$ |
| **Peta / Pebi** | Petabyte [PB] | $10^{15} = 10^{15}$ | Pebibyte [PiB] | $2^{50} \approx 1.125 \times 10^{15}$ |

### Unidades de tiempo de ejecución

Para interpretar los órdenes de magnitud de $T_0$ y el tiempo total $t$, considere las siguientes equivalencias y factores de escala canónicos:

| Unidad | Símbolo | Equivalencia en segundos [s] | Factor respecto a la unidad base |
| :--- | :--- | :--- | :--- |
| **Nanosegundo** | [ns] | $10^{-9}\text{ s} = 0.000\,000\,001\text{ s}$ | $1\text{ s} = 10^9\text{ ns}$ |
| **Microsegundo** | [$\mu$s] | $10^{-6}\text{ s} = 0.000\,001\text{ s}$ | $1\text{ s} = 10^6\,\mu\text{s}$ |
| **Milisegundo** | [ms] | $10^{-3}\text{ s} = 0.001\text{ s}$ | $1\text{ s} = 10^3\text{ ms}$ |
| **Segundo** | [s] | $1\text{ s} = 10^0\text{ s}$ | Unidad base SI |
| **Minuto** | [min] | $60\text{ s}$ | $1\text{ min} = 60\text{ s}$ |
| **Hora** | [h] | $3\,600\text{ s}$ | $1\text{ h} = 60\text{ min} = 3\,600\text{ s}$ |
| **Día** | [d] | $86\,400\text{ s}$ | $1\text{ d} = 24\text{ h} = 86\,400\text{ s}$ |

<nav class="section-return section-step" aria-label="Navegación entre secciones"><a href="../ejercicios-propuestos/">← 2.2 Ejercicios propuestos</a><a class="section-step__index" href="../">Capítulo 2</a></nav>

---

<nav class="chapter-nav chapter-nav--bottom" aria-label="Navegación inferior entre capítulos"><a href="../../">← Recorrido</a><a class="chapter-nav__index" href="../">Capítulo 2</a><a class="chapter-nav__next" href="../../capitulo-3/">Capítulo 3 →</a></nav>
