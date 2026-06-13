# Cómo usar los laboratorios

El sitio sirve como mapa de lectura; el código ejecutable permanece en los cuadernos del repositorio. Puedes trabajar de tres maneras.

## 1. Leer y orientar el estudio

Usa el recorrido por capítulos para ubicar conceptos, ecuaciones, comparaciones y enlaces. La búsqueda del sitio permite encontrar un término en todo el complemento digital.

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

Los capítulos 2–6 se apoyan principalmente en cuadernos Jupyter. Los capítulos 7–8 incorporan experiencias interactivas que también pueden ejecutarse con Voilà desde el entorno local.

!!! tip "Un ciclo de estudio útil"
    Lee primero el razonamiento del capítulo, formula tu predicción sobre \(T(n)\) o \(S(n)\), ejecuta el cuaderno y contrasta el resultado. La medición complementa el análisis; no lo reemplaza.

[Explorar el repositorio](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional){ .md-button .md-button--primary }
[Ir al recorrido](capitulos/index.md){ .md-button }
