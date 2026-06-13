<h1 style="text-align:center;">
  <strong>Capítulo 4: Análisis de algoritmos estructurados</strong>
</h1>

<p align="justify">
Este capítulo aplica el marco formal de la notación asintótica (Capítulo 3) al análisis concreto de algoritmos estructurados, es decir, algoritmos cuyo flujo de control se expresa mediante <b>secuencias</b>, <b>condicionales</b> y <b>ciclos</b>. El objetivo es desarrollar en el lector la capacidad de estimar la complejidad de un algoritmo con solo observar su estructura, sin necesidad de ejecutarlo.
</p>

---

<h2>🧭 Contenido del capítulo</h2>

<ul>
  <li><a href="#4-1">4.1 Aspectos preliminares y clasificación</a></li>
  <li><a href="#4-2">4.2 Complejidad temporal</a></li>
  <li><a href="#4-3">4.3 Complejidad espacial</a></li>
  <li><a href="#4-4">4.4 Análisis de estructuras de control</a></li>
  <li><a href="#4-5">4.5 Composición de complejidades — Ejemplos</a></li>
  <li><a href="#4-55">4.5 Consideraciones finales</a></li>
  <li><a href="#4-6">4.6 Ejercicios propuestos</a></li>
</ul>

---

<h2 id="4-1">📜 4.1 Aspectos preliminares y clasificación</h2>

<p align="justify">
El análisis de algoritmos busca responder una pregunta fundamental: <b>¿cómo crece el costo de un algoritmo cuando aumenta el tamaño de la entrada?</b>  
Este costo puede manifestarse en tiempo de ejecución, consumo de memoria o ambos.
</p>

<p align="justify">
Un principio clave es que el análisis <b>no se basa en mediciones experimentales</b>, sino en un modelo abstracto que cuenta operaciones elementales y estudia su comportamiento cuando <i>n</i> tiende a infinito.  
De esta forma, los resultados son independientes del lenguaje de programación, del hardware y del sistema operativo.
</p>

<p align="justify">
Para lograrlo, se asume que ciertas operaciones básicas —como asignaciones, comparaciones o accesos a memoria— tienen un costo constante.  
A partir de esta base, se construyen funciones que describen el comportamiento global del algoritmo.
</p>

---

<h2 id="4-2">⏱️ 4.2 Cálculo de la complejidad temporal</h2>

<p align="justify">
La <b>complejidad temporal</b> mide cómo varía el tiempo de ejecución de un algoritmo en función del tamaño de la entrada <i>n</i>.  
Se expresa mediante una función <i>T(n)</i>, que representa el número de operaciones elementales ejecutadas.
</p>

<p align="justify">
El procedimiento general para calcular la complejidad temporal es el siguiente:
</p>

<ol>
  <li><b>Identificar las operaciones básicas</b> que se ejecutan en el algoritmo.</li>
  <li><b>Determinar cuántas veces se ejecuta cada operación</b> en función de <i>n</i>.</li>
  <li><b>Sumar los costos</b> de todas las operaciones.</li>
  <li><b>Aplicar notación asintótica</b> para conservar solo el término dominante.</li>
</ol>

<p align="justify">
Por ejemplo, una asignación o una comparación se ejecuta una sola vez y tiene costo constante:  
<b>O(1)</b>.  
En cambio, una operación dentro de un ciclo que se ejecuta <i>n</i> veces tiene costo <b>O(n)</b>.
</p>

<p align="justify">
Cuando existen ciclos anidados, el número total de iteraciones se obtiene multiplicando las iteraciones de cada ciclo, lo que conduce a complejidades cuadráticas, cúbicas o superiores.
</p>

<p align="justify">
El análisis suele enfocarse en el <b>peor caso</b>, ya que garantiza límites superiores sobre el tiempo de ejecución del algoritmo.
</p>

---

<h2 id="4-3">💾 4.3 Cálculo de la complejidad espacial</h2>

<p align="justify">
La <b>complejidad espacial</b> describe cómo crece el consumo de memoria de un algoritmo a medida que aumenta el tamaño de la entrada.  
Se representa mediante la función <i>S(n)</i>.
</p>

<p align="justify">
Para calcularla, se distinguen dos componentes:
</p>

<ul>
  <li><b>Complejidad espacial fija:</b> memoria usada por variables cuyo tamaño no depende de <i>n</i>.</li>
  <li><b>Complejidad espacial variable:</b> memoria asociada a estructuras de datos cuyo tamaño depende de la entrada.</li>
</ul>

<p align="justify">
El procedimiento de cálculo es:
</p>

<ol>
  <li>Identificar todas las variables declaradas.</li>
  <li>Determinar cuáles dependen del tamaño de la entrada.</li>
  <li>Expresar el consumo total como suma de ambos componentes.</li>
  <li>Aplicar notación asintótica para obtener el orden dominante.</li>
</ol>

<p align="justify">
Por ejemplo, declarar unas pocas variables escalares implica un consumo constante <b>O(1)</b>,  
mientras que crear un arreglo de tamaño <i>n</i> implica un consumo lineal <b>O(n)</b>,  
y una matriz <i>n × n</i> conduce a un consumo cuadrático <b>O(n²)</b>.
</p>

---

<h2 id="4-4">🧩 4.4 Análisis de estructuras de control</h2>

<p align="justify">
El análisis de algoritmos estructurados se apoya en el estudio de tres tipos de estructuras de control:
</p>

<h3>🔹 Secuencias</h3>
<p align="justify">
Las instrucciones secuenciales se ejecutan una sola vez y su complejidad es la suma de los costos individuales. En notación asintótica, una secuencia de operaciones constantes sigue siendo <b>T(n) ∈ O(1)</b>. Si una instrucción de costo O(f(n)) precede a una de costo O(g(n)), la complejidad total es O(f(n) + g(n)), que por dominancia se reduce al término mayor.
</p>

<h3>🔹 Condicionales</h3>
<p align="justify">
Las estructuras condicionales evalúan una condición y ejecutan uno de varios bloques posibles. Como el número de condiciones es fijo, la evaluación de la condición tiene costo constante. Sin embargo, los bloques ejecutados pueden introducir costos adicionales. En el peor caso, se considera el bloque de mayor costo entre todas las ramas posibles.
</p>

<h3>🔹 Ciclos</h3>

<table style="width:100%; border-collapse:collapse; margin-top:0.8em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Tipo de ciclo</th>
      <th style="padding:8px; border:1px solid #ccc;">Patrón de control</th>
      <th style="padding:8px; border:1px solid #ccc; text-align:center;">T(n)</th>
      <th style="padding:8px; border:1px solid #ccc;">Ejemplo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Incremento unitario</b></td>
      <td style="padding:8px; border:1px solid #ccc; font-family:monospace;">for i = 1 to n</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><b>O(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Imprimir elementos de un arreglo</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>División por constante</b></td>
      <td style="padding:8px; border:1px solid #ccc; font-family:monospace;">while n > 1: n = n/2</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><b>O(log n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Búsqueda binaria</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Dos ciclos anidados lineales</b></td>
      <td style="padding:8px; border:1px solid #ccc; font-family:monospace;">for i, for j = 1 to n</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><b>O(n²)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Recorrido de una matriz n × n</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Tres ciclos anidados lineales</b></td>
      <td style="padding:8px; border:1px solid #ccc; font-family:monospace;">for i, for j, for k = 1 to n</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><b>O(n³)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Multiplicación de matrices</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Ciclo con límite fijo</b></td>
      <td style="padding:8px; border:1px solid #ccc; font-family:monospace;">for i = 1 to k (k constante)</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><b>O(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Ciclo de inicialización fija</td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;"><b>Ciclo lineal con interno log</b></td>
      <td style="padding:8px; border:1px solid #ccc; font-family:monospace;">for i = 1 to n, while m > 1: m = m/2</td>
      <td style="padding:8px; border:1px solid #ccc; text-align:center;"><b>O(n·log n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;">Heap sort iterativo</td>
    </tr>
  </tbody>
</table>

---

<h2 id="4-5">🧠 4.5 Composición de complejidades</h2>

<p align="justify">
Cuando un algoritmo combina múltiples estructuras, su complejidad total se obtiene:
</p>

<ul>
  <li><b>Sumando</b> las complejidades de bloques secuenciales.</li>
  <li><b>Multiplicando</b> las complejidades de ciclos anidados.</li>
</ul>

<p align="justify">
Finalmente, la notación asintótica elimina constantes y términos de menor orden, conservando únicamente el término dominante.  
Este proceso permite comparar algoritmos y razonar sobre su escalabilidad.
</p>

---

<h2 id="4-5">📊 4.5 Composición de complejidades — Ejemplos del libro</h2>

<p align="justify">
La siguiente tabla presenta los ejemplos analizados formalmente en el capítulo. Cada ejemplo ilustra un principio específico del análisis de complejidad de algoritmos estructurados, desde operaciones constantes hasta combinaciones de estructuras anidadas con complejidad oculta.
</p>

<table style="width:100%; border-collapse:collapse; margin-top:1em;">
  <thead>
    <tr style="background-color:#f2f2f2;">
      <th style="padding:8px; border:1px solid #ccc;">Ejercicio / Notebook</th>
      <th style="padding:8px; border:1px solid #ccc;">Descripción</th>
      <th style="padding:8px; border:1px solid #ccc;">Complejidad temporal</th>
      <th style="padding:8px; border:1px solid #ccc;">Complejidad espacial</th>
      <th style="padding:8px; border:1px solid #ccc;">Explicación (según el libro)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">
        📘 <a href="./ejemplo1_(sumar_numeros).ipynb"><b>Ejemplo 1</b></a><br/>
        <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/ejemplo1_(sumar_numeros).ipynb">🔗 Colab</a>
      </td>
      <td style="padding:8px; border:1px solid #ccc;">
        Suma de dos números enteros
      </td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">
        El algoritmo no contiene ciclos ni estructuras de control dependientes del tamaño
        de la entrada. Todas las operaciones (lectura de variables, suma y retorno)
        tienen costo constante. Al no declararse estructuras dependientes de <i>n</i>,
        la complejidad espacial también es constante.
      </td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">
        📘 <a href="./ejemplo2_(imprimir_elementos_arreglo).ipynb"><b>Ejemplo 2</b></a><br/>
        <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/ejemplo2_(imprimir_elementos_arreglo).ipynb">🔗 Colab</a>
      </td>
      <td style="padding:8px; border:1px solid #ccc;">
        Impresión de los elementos de un arreglo
      </td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(n)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">
        El algoritmo implementa un ciclo con incremento unitario que se ejecuta una vez
        por cada elemento del arreglo, por lo que <i>f(n)=n</i>. El cuerpo del ciclo
        contiene únicamente operaciones constantes. No se crean estructuras adicionales,
        por lo que el consumo de memoria permanece constante.
      </td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">
        📘 <a href="./ejemplo3_(imprimir_elementos_matriz).ipynb"><b>Ejemplo 3</b></a><br/>
        <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/ejemplo3_(imprimir_elementos_matriz).ipynb">🔗 Colab</a>
      </td>
      <td style="padding:8px; border:1px solid #ccc;">
        Impresión de los elementos de una matriz
      </td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(n²)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">
        Se utilizan dos ciclos anidados con incrementos unitarios. El ciclo interno se
        ejecuta <i>n</i> veces por cada iteración del ciclo externo, resultando en
        <i>f(n)=n·n</i>. Las operaciones internas son constantes. La memoria utilizada
        corresponde únicamente a índices y variables escalares.
      </td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">
        📘 <a href="./ejemplo4_(inicializar_matriz_variable).ipynb"><b>Ejemplo 4</b></a><br/>
        <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/ejemplo4_(inicializar_matriz_variable).ipynb">🔗 Colab</a>
      </td>
      <td style="padding:8px; border:1px solid #ccc;">
        Inicialización de una matriz de tamaño variable
      </td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(n²)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(n²)</b></td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">
        La matriz se recorre completamente mediante ciclos anidados, lo que produce un
        crecimiento cuadrático del tiempo de ejecución. A diferencia del ejemplo anterior,
        aquí la estructura de datos se declara dentro del algoritmo, por lo que el consumo
        de memoria depende directamente del tamaño de la entrada.
      </td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">
        📘 <a href="./ejemplo5_(ciclos_incremento_no_lineal).ipynb"><b>Ejemplo 5</b></a><br/>
        <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/ejemplo5_(ciclos_incremento_no_lineal).ipynb">🔗 Colab</a>
      </td>
      <td style="padding:8px; border:1px solid #ccc;">
        Ciclos con incremento no estrictamente lineal
      </td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(n²)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(n²)</b></td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">
        Aunque uno de los ciclos incrementa su índice en saltos mayores a una unidad,
        el número de iteraciones sigue siendo proporcional a <i>n</i> en el límite
        asintótico. Al combinarse con un segundo ciclo lineal, la complejidad total
        resulta cuadrática. La memoria está dominada por la matriz creada.
      </td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">
        📘 <a href="./ejemplo7_(ciclo_sin_dependencia).ipynb"><b>Ejemplo 7</b></a><br/>
        <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/ejemplo7_(ciclo_sin_dependencia).ipynb">🔗 Colab</a>
      </td>
      <td style="padding:8px; border:1px solid #ccc;">
        Ciclo sin dependencia del tamaño de la entrada
      </td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>O(1)</b></td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">
        El ciclo se ejecuta un número fijo de veces, independiente del tamaño de la entrada.
        Según la notación asintótica, las constantes no afectan el orden de complejidad,
        por lo que tanto el tiempo como el espacio permanecen constantes.
      </td>
    </tr>
    <tr>
      <td style="padding:8px; border:1px solid #ccc;">
        📘 <a href="ejemplo9_(complejidad_oculta).ipynb"><b>Ejemplo 8</b></a><br/>
        <a href="https://githubtocolab.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/capitulo4/ejemplo9_(complejidad_oculta).ipynb">🔗 Colab</a>
      </td>
      <td style="padding:8px; border:1px solid #ccc;">
        Algoritmo con complejidad no evidente a simple vista
      </td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Dominada por el término mayor</b></td>
      <td style="padding:8px; border:1px solid #ccc;"><b>Variable</b></td>
      <td style="padding:8px; border:1px solid #ccc; text-align:justify;">
        El análisis requiere descomponer el algoritmo en bloques y estudiar cada estructura
        de control por separado. Al combinar ciclos, llamadas a funciones y operaciones
        internas, la complejidad total queda determinada por el término de mayor crecimiento,
        ilustrando el principio de dominancia explicado en el capítulo.
      </td>
    </tr>
  </tbody>
</table>


<h2 id="4-55">💡 4.5 Consideraciones finales</h2>

<p align="justify">
El análisis de algoritmos estructurados sienta las bases para el estudio de algoritmos más complejos, como los algoritmos recursivos (Capítulo 6) y los algoritmos de búsqueda y ordenamiento (Capítulos 7 y 8). Los principios desarrollados en este capítulo —conteo de operaciones, composición de complejidades, dominancia asintótica— son las herramientas fundamentales con las que el analista aborda cualquier problema algorítmico.
</p>

<p align="justify">
Es importante recordar que el análisis de complejidad siempre se refiere a un modelo abstracto que ignora las constantes de implementación. Dos algoritmos con la misma complejidad asintótica pueden tener rendimientos muy distintos en la práctica, especialmente para entradas pequeñas. Sin embargo, a medida que n crece, la complejidad asintótica se convierte en el factor determinante del rendimiento.
</p>

<p align="justify">
La complejidad espacial, aunque frecuentemente recibe menos atención que la temporal, es igualmente importante en sistemas con recursos limitados. El ejemplo 4 de este capítulo ilustra claramente cómo la declaración de una estructura de datos dentro del algoritmo puede cambiar su complejidad espacial de O(1) a O(n²), lo que tiene implicaciones directas en la viabilidad del algoritmo.
</p>

---

<h2 id="4-6">📚 4.6 Ejercicios propuestos</h2>

<p align="justify">
Los ejercicios del capítulo están diseñados para fortalecer la habilidad de:
</p>

<ul>
  <li>Identificar estructuras de control.</li>
  <li>Contar iteraciones de forma analítica.</li>
  <li>Calcular complejidades temporales y espaciales.</li>
  <li>Aplicar notación asintótica correctamente.</li>
</ul>

<p align="justify">
El objetivo es que el lector desarrolle la capacidad de <b>estimar la complejidad de un algoritmo con solo observar su estructura</b>, sin necesidad de ejecutarlo.
</p>

---

<h2>🧾 Licencia</h2>

<div style="border-left:4px solid #999; padding:1em; background-color:#fafafa; border-radius:6px;">
<p style="text-align:justify; color:#333;">
El contenido de este capítulo se distribuye bajo la licencia  
<b>Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)</b>.  
Se autoriza su uso con fines académicos citando la fuente original.
</p>
<p style="text-align:center; font-weight:600; margin-top:0.5em;">
© 2026 Carlos Eduardo Orozco Garcés, César Jesús Pardo Calvache, Mauro Callejas Cuervo
</p>
</div>