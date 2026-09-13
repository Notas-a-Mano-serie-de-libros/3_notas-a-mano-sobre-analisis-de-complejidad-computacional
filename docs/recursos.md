# Cómo usar los laboratorios

El sitio reúne las explicaciones y ejemplos ejecutables en Java y Python. Los cuadernos del repositorio amplían la experimentación con controles, animaciones y mediciones en Colab.

## Cómo se distribuye el contenido

| Soporte | Contenido principal |
| --- | --- |
| Obra | Desarrollo completo, contexto y progresión editorial. |
| GitHub Pages | Explicaciones, ecuaciones, análisis y ejemplos ejecutables en Java y Python. |
| Notebook | Código, controles, animaciones, tablas y resultados ejecutables. |
| Google Colab | Entorno inmediato para ejecutar el notebook. |

## Qué encontrarás en cada sección

La lectura sigue una secuencia fija: **objetivo**, **procedimiento**, **ecuaciones**, **resultado teórico**, **interpretación experimental** y, cuando corresponde, **ejercicios**. El botón de Colab aparece después de la explicación para que puedas formular primero una predicción y contrastarla luego con la ejecución.

Cada notebook incluye un enlace hacia su explicación específica en Pages. Al final de cada explicación encontrarás un botón para abrir el notebook en Colab.

## 1. Leer y orientar el estudio

Usa el recorrido por capítulos para ubicar conceptos generales y entra en cada sección para consultar el desarrollo asociado a una simulación concreta. La búsqueda del sitio permite encontrar términos dentro de todo el complemento digital.

## Ejecutar ejemplos en Pages

Abre **Ver código y editar entradas**, elige **Java** o **Python** y modifica los valores resaltados. El algoritmo permanece en solo lectura. Pulsa **Ejecutar** para ver el resultado, **Detener** para cancelar o **Restablecer ejemplo** para recuperar las entradas originales. Cada lenguaje conserva sus entradas al cambiar de selección.

La ejecución ocurre en tu navegador: Java utiliza [CheerpJ](https://cheerpj.com/) y Python utiliza [Pyodide](https://pyodide.org/). La primera carga necesita conexión a Internet. En Java, el `main` invoca la función presentada; `Entradas` lee los valores editables usando los argumentos del programa. Los ejemplos conceptuales con funciones `foo` requieren una definición propia del problema y muestran esa limitación al ejecutarse.

## 2. Ejecutar en Google Colab

Los botones **Abrir en Colab** cargan cada cuaderno en el navegador. Es la ruta más corta para experimentar sin preparar un entorno local. Para conservar tus cambios, guarda una copia del cuaderno en tu propia cuenta.

## 3. Trabajar localmente

```bash
git clone https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional.git
cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python3 abrir.py --lista
```

Después puedes abrir un recurso concreto, por ejemplo:

```bash
python3 abrir.py 7/binaria
```

Los capítulos 2–8 se apoyan en cuadernos Jupyter. Colab es la ruta recomendada para ejecutar las animaciones desde Pages; la ejecución local queda disponible para quien quiera modificar el código.

!!! tip "Un ciclo de estudio útil"
    Lee primero el razonamiento del capítulo, formula tu predicción sobre \(T(n)\) o \(S(n)\), ejecuta el cuaderno y contrasta el resultado. La medición complementa el análisis; no lo reemplaza.

[Explorar el repositorio](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional){ .md-button .md-button--primary }
[Ir al recorrido](capitulos/index.md){ .md-button }

## Coherencia de las implementaciones

Cada código de Pages identifica su versión, parámetros, precondiciones y resultado. Los ejemplos paso a paso utilizan los nombres del listado. Las notas «Laboratorio y medición» explican la adaptación que ejecuta Colab. Consulta la [correspondencia por implementación](correspondencia.md#implementaciones-y-ejemplos).
