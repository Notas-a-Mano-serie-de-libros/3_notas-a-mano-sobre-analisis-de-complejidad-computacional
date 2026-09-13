<div align="center">

# Notas a mano sobre análisis de complejidad computacional

### Teoría, experimentos y simulaciones interactivas de algoritmos

[![CI](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/actions/workflows/ci.yml/badge.svg)](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/actions/workflows/ci.yml)
[![GitHub Pages](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/actions/workflows/pages.yml/badge.svg)](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/actions/workflows/pages.yml)
[![CodeQL](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/actions/workflows/codeql.yml/badge.svg)](https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/actions/workflows/codeql.yml)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Licencia CC BY-NC 4.0](https://img.shields.io/badge/Licencia-CC%20BY--NC%204.0-EF9421?logo=creativecommons&logoColor=white)](./LICENSE.MD)

Material interactivo de la **segunda edición (2026)** del libro de Carlos Eduardo Orozco Garcés, César Jesús Pardo Calvache y Mauro Callejas Cuervo.

[Visitar el sitio de la obra](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/) · [Explorar los capítulos](#ruta-de-aprendizaje) · [Empezar en local](#ejecución-local) · [Ver el libro](https://a.co/d/02EZLscG)

</div>

---

## Complemento digital de la obra

El **libro** contiene el desarrollo teórico completo. El **sitio de la obra** organiza la lectura por capítulos y conecta cada tema con sus comparaciones y laboratorios. El **repositorio** conserva el código fuente y los notebooks; **Google Colab** permite ejecutarlos sin instalación.

<p align="center">
  <a href="https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/">
    <img src="./assets/qr/pages-inicio.png" width="168" alt="Código QR del complemento digital de la obra">
  </a>
  <br>
  <strong><a href="https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/">Leer el complemento digital</a></strong>
</p>

La ruta recomendada es: **leer el capítulo en la obra → consultar su síntesis en Pages → ejecutar el laboratorio enlazado → volver al análisis con los resultados observados**.

## Acerca del proyecto

La obra desarrolla un recorrido que parte de los conceptos iniciales y el contexto histórico de la complejidad computacional, establece sus fundamentos matemáticos, aplica el análisis a algoritmos estructurados y recursivos, y culmina con búsquedas, ordenamientos y una reflexión final sobre el diseño eficiente de soluciones.

El sitio desarrolla el recorrido completo de los **capítulos 1–9**. Los capítulos 1 y 9 aportan la apertura y el cierre editorial; los capítulos 2–8 enlazan notebooks para comparar funciones de crecimiento, experimentar con notación asintótica, resolver recurrencias y observar algoritmos de búsqueda y ordenamiento paso a paso. Las consideraciones teóricas, la bibliografía y la fe de erratas complementan esta ruta.

El contenido conserva el orden y la numeración de la obra impresa. Cada ampliación se identifica como material adicional para diferenciarla de los ejemplos publicados.

## Empieza aquí

```bash
# Ver todos los recursos disponibles
python3 abrir.py --lista

# Abrir una simulación local
python3 abrir.py 7/secuencial

# Abrir un recurso directamente en Google Colab
python3 abrir.py --colab 3/theta
```

> [!TIP]
> Si solo quieres explorar el material, usa la opción `--colab`: no requiere preparar un entorno local.

## Ruta de aprendizaje

| Capítulo | Tema | Leer en Pages | Recursos técnicos |
| :---: | --- | :---: | :---: |
| **1** | Introducción al análisis y la complejidad | [Síntesis](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-1/) | Lectura |
| **2** | Fundamentos y funciones de complejidad | [Síntesis](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-2/) | [Notebooks](./capitulo2/notebooks/README.md) |
| **3** | Notación asintótica | [Síntesis](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-3/) | [Notebooks](./capitulo3/notebooks/README.md) |
| **4** | Análisis de algoritmos estructurados | [Síntesis](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-4/) | [Notebooks](./capitulo4/notebooks/README.md) |
| **5** | Relaciones de recurrencia | [Síntesis](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-5/) | [Notebooks](./capitulo5/notebooks/README.md) |
| **6** | Análisis de algoritmos recursivos | [Síntesis](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-6/) | [Notebooks](./capitulo6/notebooks/README.md) |
| **7** | Algoritmos de búsqueda clásicos | [Síntesis](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-7/) | [Notebooks](./capitulo7/notebooks/README.md) |
| **8** | Algoritmos de ordenamiento clásicos | [Síntesis](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-8/) | [Notebooks](./capitulo8/notebooks/README.md) |
| **9** | Reflexiones finales | [Síntesis](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/capitulos/capitulo-9/) | Lectura |

## Qué encontrarás

| Recurso | Propósito |
| --- | --- |
| **Notebooks interactivos** | Experimentar con parámetros y observar cómo cambia el comportamiento de un algoritmo. |
| **Simulaciones paso a paso** | Visualizar estados, comparaciones, descartes, llamadas recursivas y operaciones. |
| **Comparadores** | Contrastar familias de complejidad y algoritmos bajo las mismas condiciones. |
| **Ejercicios** | Aplicar los conceptos y comprobar resultados mediante experimentación. |
| **Gráficas reproducibles** | Relacionar el análisis teórico con mediciones y representaciones visuales. |

## Ejecución local

### 1. Preparar el entorno

```bash
git clone https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional.git
cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt jupyterlab voila
```

En Windows, activa el entorno con:

```powershell
.venv\Scripts\activate
```

### 2. Abrir una experiencia

```bash
python3 abrir.py --lista
python3 abrir.py 2/comparacion
python3 abrir.py 7/binaria
python3 abrir.py 8/mezcla
```

Los capítulos 2–6 se abren con Jupyter. Las simulaciones de los capítulos 7–8 usan Voilà para mostrar la interfaz sin exponer el código del notebook.

## Organización del repositorio

```text
.
├── capitulo2/ ... capitulo8/   # Notebooks y recursos por capítulo
├── common/                     # Componentes visuales compartidos
├── core/                       # Motores de búsqueda y ordenamiento
├── scripts/                    # Validadores y automatización
├── tests/                      # Pruebas automatizadas
├── abrir.py                    # Lanzador unificado de notebooks
└── Makefile                    # Comandos de desarrollo
```

<details>
<summary><strong>Alcance y fidelidad respecto de la obra</strong></summary>

Los README conservan los títulos, la numeración y la secuencia conceptual de la segunda edición. Los notebooks acompañan secciones concretas del libro o amplían su estudio mediante comparaciones, mediciones y laboratorios de ejercicios.

Estos recursos no sustituyen las definiciones, demostraciones, implementaciones ni análisis desarrollados en la obra. Las ampliaciones se señalan en el capítulo correspondiente y las simulaciones distinguen los resultados medidos de las estimaciones o proyecciones teóricas.

</details>

<details>
<summary><strong>Desarrollo y control de calidad</strong></summary>

Instala las dependencias y los hooks del repositorio:

```bash
make install
```

Ejecuta las comprobaciones locales:

```bash
make clean-notebooks
make clean-graphics
make check
```

La integración continua valida rutas, enlaces de Colab, contratos visuales, pruebas, rendimiento y dependencias.

</details>

<details>
<summary><strong>Serie Notas a mano para ingenieros</strong></summary>

1. [Notas a mano sobre fundamentos en lógica y programación estructurada](https://a.co/d/aobD6ct)
2. [Notas a mano sobre análisis orientado a objetos y patrones de diseño](https://a.co/d/9rEY0dC)
3. **Notas a mano sobre análisis de complejidad computacional**

</details>

## Autores

| Autor | Perfiles académicos |
| --- | --- |
| **Carlos Eduardo Orozco Garcés** | [LinkedIn](https://www.linkedin.com/in/corozco9408) · [ORCID](https://orcid.org/0000-0003-3279-4784) · [ResearchGate](https://www.researchgate.net/profile/Carlos-Orozco-41) |
| **César Jesús Pardo Calvache** | [ORCID](https://orcid.org/0000-0002-0750-5928) · [ResearchGate](https://www.researchgate.net/profile/Cesar-Pardo-Calvache) |
| **Mauro Callejas Cuervo** | [ResearchGate](https://www.researchgate.net/profile/Mauro-Callejas-Cuervo) |

## Licencia

El material se distribuye con fines académicos bajo la licencia [Creative Commons Attribution-NonCommercial 4.0 International](./LICENSE.MD). Se permite compartirlo y adaptarlo con atribución, siempre que no se utilice con fines comerciales.

<div align="center">

© 2026 Carlos Eduardo Orozco Garcés, César Jesús Pardo Calvache y Mauro Callejas Cuervo

</div>

### Coherencia de los códigos publicados con el libro

Los listados de Pages se conservan en `scripts/data/book_code.json`, con su página de origen y la huella SHA-256 del PDF de referencia. Se publican en Java con los nombres y firmas principales del libro, incluidas sus variantes y las correcciones solicitadas. Los ejemplos de complejidad del capítulo 2 remiten a listados de los capítulos donde se desarrollan esos algoritmos. Shell y la sección de complejidad factorial no tienen un listado correspondiente en el libro.

`python scripts/sync_book_code.py` actualiza los bloques de implementación sin reconstruir las páginas. `python scripts/sync_book_code.py --check` comprueba su igualdad con el catálogo. La regeneración de capítulos aplica esta sincronización al finalizar, y la validación editorial también la verifica.

El catálogo también conserva títulos de variantes, parámetros, precondiciones, trazas y notas de medición. El catálogo incorpora las correcciones de funcionamiento solicitadas por el autor, incluida la declaración de la matriz. Los códigos actualizados y sus explicaciones se presentan en cada sección de los capítulos. `make book-review` requiere un JDK y reproduce las comprobaciones de Java sobre los 72 listados inventariados, con el contexto de prueba documentado.

Los ejemplos de Pages permiten elegir Java o Python y editar únicamente las entradas. Java ejecuta el `main` del programa compilado con CheerpJ; Python utiliza Pyodide. Para regenerar el archivo JAR al modificar los listados, ejecuta `python scripts/build_java_examples.py` con JDK 17 instalado; `make docs-build` lo incluye. La integración utiliza el CDN oficial de CheerpJ y conserva su crédito en cada ejemplo. Para probar Java localmente, utiliza un servidor con solicitudes Range, por ejemplo `npx http-server site -p 8765 -c-1`; el servidor básico de Python no admite esas solicitudes.
