# Cómo usar los laboratorios

El sitio reúne las explicaciones y ejemplos ejecutables en Java, Python y C. Los cuadernos del repositorio amplían la experimentación con controles, animaciones y mediciones en Colab.

## Cómo se distribuye el contenido

| Soporte | Contenido principal |
| --- | --- |
| Obra | Desarrollo completo, contexto y progresión editorial. |
| GitHub Pages | Explicaciones, ecuaciones, análisis y ejemplos ejecutables en Java, Python y C. |
| Notebook | Código, controles, animaciones, tablas y resultados ejecutables. |
| Google Colab | Entorno inmediato para ejecutar el notebook. |

## Qué encontrarás en cada sección

La lectura sigue una secuencia fija: **objetivo**, **procedimiento**, **ecuaciones**, **resultado teórico**, **interpretación experimental** y, cuando corresponde, **ejercicios**. El botón de Colab aparece después de la explicación para que puedas formular primero una predicción y contrastarla luego con la ejecución.

Cada notebook incluye un enlace hacia su explicación específica en Pages. Al final de cada explicación encontrarás un botón para abrir el notebook en Colab.

## 1. Leer y orientar el estudio

Usa el recorrido por capítulos para ubicar conceptos generales y entra en cada sección para consultar el desarrollo asociado a una simulación concreta. La búsqueda del sitio permite encontrar términos dentro de todo el complemento digital.

## Ejecutar ejemplos en Pages

Abre **Ver código y editar entradas**, elige **Java**, **Python** o **C** y modifica los valores resaltados. El algoritmo permanece en solo lectura. Pulsa **Ejecutar** para ver el resultado, **Detener** para cancelar o **Reestablecer** para recuperar las entradas originales. Cada lenguaje conserva sus entradas al cambiar de selección.

La ejecución ocurre en tu navegador: Java utiliza [CheerpJ](https://cheerpj.com/), Python utiliza [Pyodide](https://pyodide.org/) y C se compila a WebAssembly. La primera carga necesita conexión a Internet. En Java y C, la función `main` invoca directamente el algoritmo con los valores editables; en Python, las líneas resaltadas cumplen la misma función.

## 2. Ejecutar en Google Colab

Los botones **Abrir en Colab** cargan cada cuaderno en el navegador. Es la ruta más corta para experimentar sin preparar un entorno local. Para conservar tus cambios, guarda una copia del cuaderno en tu propia cuenta.

## 3. Trabajar localmente

Prepare el entorno siguiendo la [guía de instalación del repositorio](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional#guía-de-instalación). Con el proyecto clonado y el entorno virtual activo, abra una terminal y vaya a la ruta principal del proyecto. Por ejemplo, para ejecutar la búsqueda binaria:

| Paso | Comando |
| --- | --- |
| Ir a la ruta principal del proyecto | `cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional` |
| Abrir la simulación de búsqueda binaria | `jupyter lab simulaciones/capitulo7/notebooks/2_busqueda_binaria.ipynb` |

El primer comando se ejecuta desde la carpeta que contiene el repositorio. Jupyter abrirá el notebook en el navegador; seleccione **Ejecutar todas las celdas** para iniciar la simulación. Cada página con una simulación incluye su comando local, y el README agrupa todos los comandos por capítulo.

Se recomienda ejecutar las simulaciones localmente para aprovechar los recursos del equipo y evitar límites de sesión. Los retrasos en entornos remotos pueden deberse a la latencia y a las restricciones de recursos de esos entornos.

!!! tip "Un ciclo de estudio útil"
    Lee primero el razonamiento del capítulo, formula tu predicción sobre \(T(n)\) o \(S(n)\), ejecuta el cuaderno y contrasta el resultado. La medición complementa el análisis; no lo reemplaza.

[Explorar el repositorio](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional){ .md-button .md-button--primary .icon-button .repository-button target="_blank" rel="noopener noreferrer" }
[Ir al recorrido](capitulos/index.md){ .md-button .icon-button .route-button }

## Coherencia de las implementaciones

Los códigos ejecutables conservan los nombres y la estructura utilizados en el libro. Las entradas que pueden modificarse se distinguen dentro de cada implementación.
