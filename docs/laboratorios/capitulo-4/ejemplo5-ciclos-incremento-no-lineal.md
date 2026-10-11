# Ejemplo 5: Ciclos con incremento no lineal

<span class="chapter-kicker">Explicación del laboratorio · Capítulo 4</span>

El ciclo interior avanza de dos en dos, pero continúa recorriendo una cantidad proporcional a \(n\) de posiciones por cada fila.

---

## Ejecutar el laboratorio

La página reúne la explicación y el análisis. El notebook conserva la implementación, los controles y las salidas experimentales.

[Abrir en Google Colab](https://colab.research.google.com/github/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/blob/main/simulaciones/capitulo4/notebooks/ejemplo5_(ciclos_incremento_no_lineal).ipynb){ .md-button .md-button--primary target="_blank" rel="noopener noreferrer" .colab-button }

---

## Código analizado


---

## Análisis esperado

### Complejidad temporal

\(T(n)\in O(n^2)\): el incremento de dos modifica una constante, no el orden cuadrático.

### Complejidad espacial

\(S(n)\in O(n^2)\) porque el algoritmo construye una matriz cuadrada.

## Simulaciones experimentales

Cada experimento ejecuta el mismo algoritmo para distintos valores de \(n\).

- **Máximo \(n\):** determina el mayor tamaño de entrada. El sistema incluye valores intermedios y potencias de diez.
- **Ejecuciones:** controla cuántas veces se repite la operación para cada valor de \(n\). La gráfica y la tabla muestran el promedio.

La preparación de la entrada se realiza fuera de la medición temporal. En memoria se reporta el espacio adicional utilizado durante la operación.

<!-- local-execution:start -->
<details class="local-execution" markdown="1">
<summary>Recomendación de ejecución local</summary>

Con el proyecto clonado, abra una terminal, sitúese en la ruta principal y active el entorno según la [guía de instalación](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación) y ejecute el notebook con Jupyter:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir Ciclos con incremento no lineal | `jupyter lab 'simulaciones/capitulo4/notebooks/ejemplo5_(ciclos_incremento_no_lineal).ipynb'` |

Jupyter abrirá la simulación; ejecute todas sus celdas para iniciarla.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de los entornos remotos.
</details>
<!-- local-execution:end -->
