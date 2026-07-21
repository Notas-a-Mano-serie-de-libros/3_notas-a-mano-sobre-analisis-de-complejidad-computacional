<h1 style="text-align:center;">
<strong>Sección: Análisis temporal experimental</strong><br/>
<strong>Medición empírica de la complejidad algorítmica</strong>
</h1>

---

## 🧩 Introducción

<p style="text-align:justify;">
Esta sección tiene como propósito analizar de manera <b>experimental</b> el comportamiento temporal de los algoritmos en función del tamaño de entrada <i>n</i>.  
Si bien la <b>complejidad temporal</b> puede determinarse teóricamente mediante la notación asintótica, los resultados empíricos permiten contrastar dicha predicción con la realidad práctica del sistema de ejecución.
</p>

<p style="text-align:justify;">
A través de una serie de <b>notebooks experimentales</b>, se ilustran los principales órdenes de crecimiento: <b>constante</b>, <b>logarítmico</b>, <b>lineal</b>, <b>cuadrático</b>, <b>cúbico</b>, <b>exponencial</b> y <b>factorial</b>.  
Cada experimento mide el tiempo real de ejecución del algoritmo y lo relaciona con el tamaño de la entrada, permitiendo observar de forma directa cómo escala su costo computacional y evidenciando las diferencias prácticas entre algoritmos eficientes y no eficientes.
</p>

---

## ⏱️ Metodología de medición experimental

<p style="text-align:justify;">
La medición experimental de la complejidad temporal consiste en <b>ejecutar el algoritmo bajo condiciones controladas</b> y registrar su tiempo de procesamiento para distintos tamaños de entrada.  
De esta manera, se obtiene una relación empírica entre <i>tiempo</i> y <i>n</i> que puede graficarse y compararse con el modelo teórico esperado.
</p>

### 🔬 Procedimiento general

<ol>
  <li><p style="text-align:justify;"><b>Definición del algoritmo:</b> se implementa una función representativa de un tipo de complejidad (por ejemplo, búsqueda lineal o recursión exponencial).</p></li>
  <li><p style="text-align:justify;"><b>Control del tamaño de entrada:</b> se genera un conjunto de entradas con valores crecientes de <i>n</i> (por ejemplo: 10³, 10⁴, 10⁵...), asegurando uniformidad en las condiciones de prueba.</p></li>
  <li><p style="text-align:justify;"><b>Medición del tiempo:</b> se registran los tiempos de inicio y fin utilizando funciones de alta precisión como <code>time.perf_counter()</code> o la librería <code>timeit</code>.</p></li>
  <li><p style="text-align:justify;"><b>Repetición y promedio:</b> cada experimento se ejecuta varias veces, y se promedian los resultados para reducir el error estadístico causado por procesos del sistema o carga del CPU.</p></li>
  <li><p style="text-align:justify;"><b>Análisis de resultados:</b> los valores promedio se grafican (n vs tiempo) y se comparan con la curva teórica correspondiente, permitiendo evaluar la correspondencia entre el modelo analítico y el comportamiento empírico.</p></li>
</ol>

<p style="text-align:justify;">
Este enfoque no solo permite verificar la validez del modelo asintótico, sino también identificar desviaciones producidas por factores externos como el sistema operativo, la política de planificación de procesos, el recolector de basura o las optimizaciones internas del intérprete o compilador.
</p>

<p style="text-align:justify;">
<b>Nota metodológica:</b> en todos los ejemplos de esta sección la medición se realiza con <code>time.perf_counter()</code>, ya que ofrece mayor resolución que <code>time.time()</code> para algoritmos rápidos o entradas pequeñas. Además, cada experimento repite varias veces la ejecución y promedia los resultados; cuando se requiera un análisis más fino, se recomienda complementar esta estrategia con <code>timeit.repeat()</code> para obtener medidas más estables y estadísticamente significativas.
</p>

---

## 📊 Resultados experimentales

<p style="text-align:justify;">
La siguiente tabla resume los experimentos desarrollados en esta sección, indicando la función implementada, el archivo correspondiente y una breve descripción del problema que ejemplifica cada orden de complejidad.
</p>

<table style="width:100%; border-collapse:collapse; text-align:left;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px;">Función</th>
      <th style="padding:8px;">Archivo asociado</th>
      <th style="padding:8px;">Descripción del experimento</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px;"><code>constante()</code></td>
      <td style="padding:8px;">1_complejidad_constante.ipynb</td>
      <td style="padding:8px; text-align:justify;">Evalúa operaciones con tiempo constante 𝒪(1), donde el número de instrucciones ejecutadas no depende de <i>n</i>. Ejemplo: acceder a un elemento en un arreglo por índice.</td>
    </tr>
    <tr>
      <td style="padding:8px;"><code>logaritmica()</code></td>
      <td style="padding:8px;">2_complejidad_logaritmica.ipynb</td>
      <td style="padding:8px; text-align:justify;">Simula algoritmos que reducen el espacio de búsqueda en cada iteración, como la búsqueda binaria, caracterizados por un crecimiento logarítmico 𝒪(log n).</td>
    </tr>
    <tr>
      <td style="padding:8px;"><code>lineal()</code></td>
      <td style="padding:8px;">3_complejidad_lineal.ipynb</td>
      <td style="padding:8px; text-align:justify;">Realiza un recorrido completo sobre una lista de longitud <i>n</i>, validando la complejidad 𝒪(n). Es representativo de algoritmos que analizan o procesan cada elemento una única vez.</td>
    </tr>
    <tr>
      <td style="padding:8px;"><code>log_lineal()</code></td>
      <td style="padding:8px;">4_complejidad_log_lineal.ipynb</td>
      <td style="padding:8px; text-align:justify;">Combina un proceso de crecimiento lineal con uno logarítmico (𝒪(n log n)), como ocurre en algoritmos de ordenamiento eficientes (MergeSort, QuickSort).</td>
    </tr>
    <tr>
      <td style="padding:8px;"><code>cuadratica()</code></td>
      <td style="padding:8px;">5_complejidad_cuadratica.ipynb</td>
      <td style="padding:8px; text-align:justify;">Ejecuta un doble bucle anidado representativo de algoritmos 𝒪(n²), como el ordenamiento burbuja o la multiplicación de matrices de tamaño reducido.</td>
    </tr>
    <tr>
      <td style="padding:8px;"><code>cubica()</code></td>
      <td style="padding:8px;">6_complejidad_cubica.ipynb</td>
      <td style="padding:8px; text-align:justify;">Modela una triple anidación de ciclos típica en operaciones de álgebra lineal, simulando algoritmos 𝒪(n³) con crecimiento rápido pero aún determinístico.</td>
    </tr>
    <tr>
      <td style="padding:8px;"><code>polinomial_general()</code></td>
      <td style="padding:8px;">7_complejidad_polinomial_general.ipynb</td>
      <td style="padding:8px; text-align:justify;">Explora la familia teórica 𝒪(nᵏ), variando el grado <i>k</i> para observar cómo las curvas polinomiales se vuelven más pronunciadas.</td>
    </tr>
    <tr>
      <td style="padding:8px;"><code>exponencial()</code></td>
      <td style="padding:8px;">8_complejidad_exponencial.ipynb</td>
      <td style="padding:8px; text-align:justify;">Evalúa el crecimiento de una función recursiva que duplica el número de llamadas (𝒪(2ⁿ)), como la implementación ingenua de Fibonacci.</td>
    </tr>
    <tr>
      <td style="padding:8px;"><code>factorial()</code></td>
      <td style="padding:8px;">9_complejidad_factorial.ipynb</td>
      <td style="padding:8px; text-align:justify;">Analiza procesos que generan todas las permutaciones posibles de un conjunto, representando el crecimiento factorial 𝒪(n!).</td>
    </tr>
  </tbody>
</table>

---

## 📈 Interpretación de los resultados

<p style="text-align:justify;">
Los resultados experimentales evidencian que los algoritmos con órdenes de complejidad bajos (𝒪(1), 𝒪(log n), 𝒪(n)) escalan de manera eficiente incluso para entradas grandes, mientras que los de orden superior (𝒪(n²), 𝒪(n³), 𝒪(2ⁿ), 𝒪(n!)) presentan un incremento exponencial del tiempo de ejecución, volviéndose impracticables para valores altos de <i>n</i>.
</p>

<p align="center">
  <img src="../../images/capitulo2/complejidad_ejecucion.png" width="90%" alt="Gráfico comparativo de crecimiento temporal">
</p>

<p style="text-align:center;"><em>Figura:</em> Crecimiento empírico del tiempo de ejecución para distintos órdenes de complejidad.</p>

---

## ⚙️ Importancia de minimizar la complejidad temporal

<ul>
  <li><p style="text-align:justify;"><b>Optimización del rendimiento:</b> un algoritmo eficiente permite procesar mayores volúmenes de datos en menos tiempo, reduciendo costos de cómputo y consumo energético.</p></li>
  <li><p style="text-align:justify;"><b>Escalabilidad:</b> sistemas con algoritmos de baja complejidad se adaptan mejor al crecimiento de usuarios o información sin degradar su desempeño.</p></li>
  <li><p style="text-align:justify;"><b>Limitaciones prácticas:</b> en contextos donde el tiempo de respuesta es crítico (por ejemplo, sistemas financieros o médicos), un algoritmo ineficiente puede comprometer la viabilidad del sistema.</p></li>
  <li><p style="text-align:justify;"><b>Impacto económico y ambiental:</b> los algoritmos con complejidad alta requieren mayor tiempo de CPU y energía, afectando tanto el costo operativo como la huella de carbono del sistema.</p></li>
</ul>

---

## 💡 Estrategias para reducir la complejidad temporal

<ol>
  <li><p style="text-align:justify;"><b>Uso de estructuras de datos adecuadas:</b> seleccionar la estructura óptima (listas, árboles, grafos, tablas hash) según el tipo de operación predominante.</p></li>
  <li><p style="text-align:justify;"><b>Evitar bucles innecesarios:</b> reducir el número de iteraciones, eliminar redundancias y emplear condiciones de salida temprana.</p></li>
  <li><p style="text-align:justify;"><b>Aplicar divide y vencerás:</b> descomponer el problema en subproblemas más pequeños para disminuir la complejidad general (por ejemplo, MergeSort o QuickSort).</p></li>
  <li><p style="text-align:justify;"><b>Memorización y programación dinámica:</b> reutilizar resultados previos en algoritmos recursivos para evitar cálculos repetitivos.</p></li>
  <li><p style="text-align:justify;"><b>Paralelismo y concurrencia:</b> distribuir la carga de trabajo entre múltiples núcleos o procesos cuando sea posible.</p></li>
</ol>

---

## 🧠 Conclusión

<p style="text-align:justify;">
El <b>análisis temporal experimental</b> constituye una herramienta esencial para validar empíricamente las predicciones teóricas de la complejidad algorítmica.  
Permite observar en la práctica cómo el aumento del tamaño de entrada <i>n</i> impacta el rendimiento y pone de manifiesto las limitaciones reales del hardware y del lenguaje de programación utilizado.
</p>

<p style="text-align:justify;">
Asimismo, proporciona una base cuantitativa para comparar implementaciones alternativas y seleccionar la más eficiente, fortaleciendo el pensamiento analítico y la toma de decisiones fundamentada en métricas objetivas.
</p>

---

## 📎 Archivos de referencia

<ul>
  <li><a href="./1_complejidad_constante.ipynb"><code>1_complejidad_constante.ipynb</code></a></li>
  <li><a href="./2_complejidad_logaritmica.ipynb"><code>2_complejidad_logaritmica.ipynb</code></a></li>
  <li><a href="./3_complejidad_lineal.ipynb"><code>3_complejidad_lineal.ipynb</code></a></li>
  <li><a href="./4_complejidad_log_lineal.ipynb"><code>4_complejidad_log_lineal.ipynb</code></a></li>
  <li><a href="./5_complejidad_cuadratica.ipynb"><code>5_complejidad_cuadratica.ipynb</code></a></li>
  <li><a href="./6_complejidad_cubica.ipynb"><code>6_complejidad_cubica.ipynb</code></a></li>
  <li><a href="./7_complejidad_polinomial_general.ipynb"><code>7_complejidad_polinomial_general.ipynb</code></a></li>
  <li><a href="./8_complejidad_exponencial.ipynb"><code>8_complejidad_exponencial.ipynb</code></a></li>
  <li><a href="./9_complejidad_factorial.ipynb"><code>9_complejidad_factorial.ipynb</code></a></li>
</ul>

---

## 🔗 Comandos LaTeX para Colab

```tex
% Complejidades experimentales - Capítulo 2
\newcommand{\colabComplejidadConstante}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/1_complejidad_constante.ipynb}
\newcommand{\colabComplejidadLogaritmica}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/2_complejidad_logaritmica.ipynb}
\newcommand{\colabComplejidadLineal}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/3_complejidad_lineal.ipynb}
\newcommand{\colabComplejidadLogLineal}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/4_complejidad_log_lineal.ipynb}
\newcommand{\colabComplejidadCuadratica}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/5_complejidad_cuadratica.ipynb}
\newcommand{\colabComplejidadCubica}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/6_complejidad_cubica.ipynb}
\newcommand{\colabComplejidadPolinomialGeneral}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/7_complejidad_polinomial_general.ipynb}
\newcommand{\colabComplejidadExponencial}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/8_complejidad_exponencial.ipynb}
\newcommand{\colabComplejidadFactorial}{https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo2/analisis_complejidad_temporal_experimental/9_complejidad_factorial.ipynb}
```

---

## 🧾 Licencia

<div style="border-left:4px solid #999; padding:1em; background-color:#fafafa; border-radius:6px;">
<p style="text-align:justify; color:#333;">
El contenido de esta sección se distribuye bajo la licencia  
<b>Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)</b>.  
Se autoriza su uso y adaptación con fines académicos siempre que se cite la fuente original.
</p>
<p style="text-align:center; font-weight:600; margin-top:0.5em;">
© 2025 Carlos Eduardo Orozco
</p>
</div>
