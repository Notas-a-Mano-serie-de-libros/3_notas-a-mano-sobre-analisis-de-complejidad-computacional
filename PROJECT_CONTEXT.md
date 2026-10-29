# Contexto Técnico del Proyecto

**Obra:** *Notas a mano sobre análisis de complejidad computacional* (2.ª edición)  
**Autores:** Carlos Eduardo Orozco Garcés, César Jesús Pardo Calvache, Mauro Callejas Cuervo  
**Rol del repositorio:** Complemento digital interactivo, plataforma de documentación web, suite de simulaciones algorítmicas ejecutables y laboratorios de complejidad computacional.  
**Fecha de reconstrucción inicial:** 2026-10-28  

---

## 1. Propósito y Alcance

Este proyecto provee la plataforma digital complementaria para el libro de texto universitario de análisis de algoritmos. Permite al estudiante y docente:
1. Leer el contenido teórico riguroso y explicaciones pedagógicas mediante un portal web estático publicado en **GitHub Pages** (construido con MkDocs Material y MathJax).
2. Experimentar de forma interactiva e inmediata con cada algoritmo y concepto analítico en tres modalidades de ejecución sincronizadas:
   - **En el navegador sin instalación:** Vía **JupyterLite** con kernel WebAssembly (**Pyodide**).
   - **En la nube con GPU/CPU:** Vía **Google Colab** a través de botones de lanzamiento directo vinculados a revisiones estables.
   - **En local:** En un entorno estándar de Python 3.11+ y JupyterLab sin conflictos de dependencias.
3. Contrastar análisis teórico de complejidad formal ($O, o, \Omega, \omega, \Theta$), árboles de recursión, laboratorio de análisis empírico y algoritmos de búsqueda y ordenamiento mediante pruebas de escritorio animadas y trazas canónicas.

---

## 2. Estado Actual del Desarrollo

- **Suite de pruebas:** 551 pruebas unitarias y de integración (`pytest`), 451 subtests, 100% pasando en tiempo récord (~8.5 s).
- **Linter y calidad de código:** `ruff check .` con 0 errores y 0 advertencias bajo configuración estricta (línea máxima 160).
- **Validaciones globales:** `make validate` pasa limpiamente (47 notebooks; 94 cargas verificadas entre local y Colab; 0 fallos).
- **Últimos hitos en Git:**
  - `e0b867d`: Corrige el control de pausa canónico.
  - `ab08ba3`: Suaviza escalas e interacción canónica.
  - `4c66215`: Mejora simulaciones de crecimiento canónico.
  - `91b6bfd`: Anima el cálculo canónico por órdenes de magnitud.
  - `f8a9168`: Ordena referencias canónicas y estabiliza JupyterLite.
  - `796421b`: Actualización del payload embebido del runtime en `0_comparacion_crecimiento` para ejecución en Colab y sincronización de URLs JupyterLite.
- **Árbol de trabajo:** Limpio (`working tree clean`), sincronizado con `origin/main`.

---

## 3. Arquitectura y Organización de Componentes

El proyecto sigue una arquitectura en capas desacopladas orientada a la inmutabilidad de los contratos y a la paridad estricta entre JupyterLite, Colab y JupyterLab local:

```
├── common/                  # Capa transversal de widgets, vistas y runtime de animación
│   ├── animation_runtime.py # Control de bucles asíncronos (play/pause/step/speed/cancel) a 30 fps
│   ├── chart_runtime.py     # Generación de gráficos analíticos y renderizado SVG/HTML
│   ├── desk_check.py        # Generación de pruebas de escritorio y trazas tabulares paso a paso
│   ├── exercise_laboratory.py # Motor interactivo para ejercicios de complejidad asistidos
│   ├── simulation_views.py  # Plantillas visuales unificadas (paneles, encabezados, controles)
│   ├── visual_roles.py      # Paleta canónica semántica (colores por rol: pivot, comparado, ordenado)
│   └── widget_controls.py   # Factoría de widgets UI estándar (steppers, botones, frames, dropdowns)
│
├── core/                    # Núcleo de lógica pura algorítmica y comparaciones temáticas
│   ├── search/              # Búsqueda secuencial, binaria, interpolación, saltos, exponencial, ternaria
│   └── sort/                # Burbuja, selección, inserción, shell, mezcla, rápido, radix
│
├── simulaciones/            # Capa de presentación para Jupyter y Colab organizada por capítulos
│   ├── capitulo2/           # Familias de crecimiento asintótico (1, log, n, n log n, n^2, n^3, 2^n, n!)
│   ├── capitulo3/           # Definiciones formales y cotas asintóticas (O, o, Omega, omega, Theta)
│   ├── capitulo4/           # Laboratorio empírico de conteo de instrucciones y ciclos
│   ├── capitulo5/           # Árboles de recursión y métodos de solución de recurrencias
│   ├── capitulo6/           # Laboratorio de análisis recursivo y Fibonacci
│   ├── capitulo7/           # Simuladores interactivos de búsqueda y comparador unificado
│   └── capitulo8/           # Simuladores interactivos de ordenamiento y comparador unificado
│       └── notebooks/       # Notebooks .ipynb canónicos del capítulo
│       └── runtime/         # Módulos Python ejecutables vinculados a los notebooks
│
├── docs/                    # Código fuente de la documentación web (Markdown + MkDocs Material)
│   └── capitulos/           # Páginas por capítulo con iframes hacia JupyterLite y enlaces a Colab
│
├── desarrollo/              # Infraestructura de ingeniería, calidad, compilación y pruebas
│   ├── scripts/             # Validadores, sincronizadores de enlaces, constructores de artefactos
│   │   ├── audit_simulation_references.py  # Verifica enlaces locales y remotos de notebooks
│   │   ├── build_jupyterlite_demo.py       # Compilación de perfiles JupyterLite y assets WASM
│   │   ├── sync_jupyterlite_urls.py        # Mantiene los hashes de revisión en docs/
│   │   ├── validate_widget_contracts.py    # Valida dimensiones, accesibilidad y tokens CSS
│   │   └── validate_colab_bootstrap.py     # Asegura que Colab use la revisión inmutable canónica
│   └── tests/               # Suite exhaustiva de pruebas automáticas con pytest
```

---

## 4. Tecnologías y Herramientas

- **Lenguaje base:** Python 3.11 y 3.12 (compatibilidad multiplataforma macOS, Linux, Windows).
- **Frontend / Widgets:** `ipywidgets` (versión 8.1.9 fijada estrictamente en `requirements-lock.txt`), `HTML`, `SVG`, `CSS` inyectado sin dependencias externas pesadas.
- **Entorno interactivo:** `JupyterLab`, `JupyterLite` 0.8.6 con `pyodide-kernel` y extensión personalizada `@notas-a-mano/jupyterlite-auto-run`.
- **Generación estática:** `MkDocs Material` con extensiones matemáticas (`pymdownx.arithmatex`, MathJax 3).
- **Ejemplos políglotas:** Compilador y ejecutor de ejemplos canónicos en `Java` (Temurin 17) y `C` (`gcc`/`clang` / WebAssembly via Node.js).
- **Testing & Calidad:** `pytest`, `pytest-subtests`, `ruff` (linter/formatter), `pip-audit`.
- **Automatización:** `Makefile`, GitHub Actions (`ci.yml`, `pages.yml`, `codeql.yml`, `deploy-worker.yml`).

---

## 5. Convenciones de Programación

1. **Futuro y Tipado:** `from __future__ import annotations` en la cabecera de todo archivo Python. Tipado explícito con sintaxis moderna (`int | float`, `dict[str, Any]`, `tuple[str, ...]`).
2. **Formato y Líneas:** Longitud máxima de línea de **160 caracteres** configurada en `pyproject.toml`. Comillas dobles en Python.
3. **Control de importaciones:** Módulos de la biblioteca estándar primero, seguidos de dependencias de terceros (`ipywidgets`), y luego módulos del proyecto (`common.*`, `core.*`). `core/sort/sort_config.py` tiene exención en `ruff` por orden intencional.
4. **Notebooks autocontenidos:** Cada celda interactiva en los `.ipynb` debe ser robusta ante reinicios del kernel. Las variables globales temporales (`SIMULATION_NAME`, `THEORETICAL_GRAPH`) se limpian en bloques `finally`.
5. **No contaminación de notebooks:** No incluir salidas grandes ni estados de ejecución en notebooks versionados (`make clean-notebooks` limpia metadatos y execution counts).

---

## 6. Sistema de Diseño e Identidad Visual

El proyecto implementa un sistema visual riguroso orientado a la legibilidad editorial y a la precisión académica:

- **Paleta de colores semántica (`common/visual_roles.py`):**
  - **Acento editorial / Terracota:** `#a94728` / `#8b4b32` (títulos, encabezados, barras de progreso, énfasis principal).
  - **Superficie y fondo:** `#ffffff` (tarjetas), `#f7f7f7` / `#fbfaf7` (fondos de control, paneles plegables).
  - **Bordes:** `#dedede` (marcos de paneles), `#cccccc` / `#767676` (bordes de campos, controles y selectores).
  - **Texto:** `#333333` (texto principal), `#666666` / `#555555` (etiquetas secundarias, notas, ejes).
  - **Roles algorítmicos:**
    - Comparación / Inspección: Ámbar (`#fff8e1` relleno, `#ffa000` borde).
    - Objetivo / Encontrado: Verde esmeralda (`#e8f5e9` relleno, `#2e7d32` borde).
    - Descartado / Fuera de rango: Gris atenuado (`#fafafa` relleno, `#e0e0e0` borde).
    - Elemento pivote / Partición: Púrpura / Azul petróleo.
- **Tipografía:**
  - Interfaz y controles: `sans-serif` (13px para etiquetas, 14px para valores).
  - Fórmulas matemáticas y notaciones: `'STIX Two Math'`, `'Cambria Math'`, `'Scheherazade New'`, `serif` (renderizado tipográfico de subíndices reales como $\log_2(n)$ y superíndices como $n^2$).
  - Tablas y trazas numéricas: `font-variant-numeric: tabular-nums` (alineación precisa de cifras).
- **Componentes y distribución:**
  - Controles rotulados compactos (`compact_labeled_control` con etiqueta izquierda fija de ~92-128px y campo acoplado).
  - Marcos de opciones agrupados (`options-frame` con borde `1px solid #767676`, fondo `#ffffff`, padding).
  - Botones de acción (`action_button_row` con altura fija de 32px, esquinas rectas `border-radius: 0`, iconos FontAwesome).
  - Animaciones a 30 fps con transiciones CSS suaves (`transform: translateY(...)`, `transition: width .12s linear`).

---

## 7. Componentes y Funcionalidades Principales

1. **Comparador interactivo de familias de crecimiento (`simulaciones/capitulo2/runtime/growth_comparison.py`):**
   - Vista dividida unificada: curvas a la izquierda y carrera de barras en tiempo real a la derecha.
   - Alternancia entre escala lineal estricta y escala logarítmica.
   - Filtro de funciones visibles organizado en cuadrícula matemática de 2 filas × 4 columnas con fórmulas enriquecidas.
2. **Definiciones y cotas asintóticas (`simulaciones/capitulo3/`):**
   - Visualización geométrica interactiva de $c \cdot g(n)$ vs $f(n)$ con deslizador del punto umbral $n_0$.
3. **Laboratorio experimental de conteo (`simulaciones/capitulo4/`):**
   - Conteo empírico de pasos y operaciones elementales en bucles simples, anidados y matrices.
4. **Árboles de recursión y laboratorio recursivo (`simulaciones/capitulo5/` y `capitulo6/`):**
   - Expansión interactiva nivel a nivel, cálculo del costo por nivel y suma de series geométricas.
5. **Simuladores de búsqueda (`core/search/` y `simulaciones/capitulo7/`):**
   - Búsqueda secuencial, binaria, saltos, interpolación, ternaria y exponencial con trazas y pruebas de escritorio.
6. **Simuladores de ordenamiento (`core/sort/` y `simulaciones/capitulo8/`):**
   - Burbuja, selección, inserción, shell (con secuencias de Shell, Hibbard, Sedgewick), mezcla, rápido y radix.

---

## 8. Decisiones Técnicas Clave y Justificaciones

1. **Bootstrap inmutable con commit SHA en Colab:**
   - *Decisión:* `RAW_BASE_URL` en `colab_bootstrap.py` y `validate_colab_bootstrap.py` apunta a un commit SHA específico (`8e4db91d4f199230f179a8b9ad49d27e93f26a6d`) en vez de a `main`.
   - *Justificación:* Evita que un commit en desarrollo rompa las simulaciones que los lectores ya tienen abiertas en Colab antes de que el release sea congelado.
2. **Payload embebido para módulos nuevos en Colab:**
   - *Decisión:* Módulos recién creados o con dependencias no reflejadas aún en el commit base viajan comprimidos en base64 (`_runtime_payload`) dentro del notebook cuando se detecta `COLAB_RELEASE_TAG`.
   - *Justificación:* Permite probar y validar inmediatamente notebooks en Colab antes de crear una nueva etiqueta o actualizar el commit congelado de producción.
3. **Sincronización de URLs con Content Hashes en JupyterLite:**
   - *Decisión:* Cada enlace de notebook en la documentación incluye `&revision=<hash>`.
   - *Justificación:* Obliga a que los Service Workers del navegador y la caché de Pyodide invaliden bundles antiguos cuando se actualiza el código del notebook o de su runtime.
4. **Ausencia de dependencias gráficas pesadas en el cliente:**
   - *Decisión:* Se usan SVGs generados dinámicamente en Python y maquetación CSS flex/grid en lugar de bibliotecas como Matplotlib interactivo o Plotly.
   - *Justificación:* Garantiza arranque instantáneo en JupyterLite (WASM), cero dependencias de canvas externo y compatibilidad perfecta en dispositivos móviles.

---

## 9. Funcionalidades Pendientes y Trabajo en Curso

- Continuar la estabilización de los controles canónicos de pausa y reinicio en simulaciones interactivas.
- Refinar los análisis pedagógicos y explicaciones contextuales de órdenes de magnitud cuando $n$ crece a valores extremos.
- Mantener la paridad de los ejemplos en Java y C con el texto definitivo del libro impreso.

---

## 10. Riesgos Técnicos y Deuda Observable

1. **Desalineación del payload base64 en notebooks de Colab:**
   - *Riesgo:* Modificar un módulo en `runtime/` y no actualizar el payload embebido en su notebook correspondiente deja a Colab ejecutando código desactualizado.
   - *Mitigación:* Correr siempre `python desarrollo/scripts/audit_simulation_references.py` y validar con mocks de entorno Colab.
2. **Incompatibilidad con JupyterLite al olvidar sincronizar URLs:**
   - *Riesgo:* Modificar notebooks sin correr `python desarrollo/scripts/sync_jupyterlite_urls.py` provoca fallos en las pruebas de CI (`test_jupyterlite_demo.py`).
   - *Mitigación:* Ejecutar `make validate` antes de cada commit.
3. **Conflicto de versiones de widgets en entornos locales con conda:**
   - *Riesgo:* Lectores que usan entornos `base` con extensiones conflictivas experimentan controles rotos.
   - *Mitigación:* Documentado extensamente en el `README.md` (aislamiento con `.venv` y fijación con `requirements-lock.txt`).

---

## 11. Protocolo para Verificar el Proyecto

Para asegurar que cualquier cambio mantiene intacta la integridad del sistema:

```bash
# 1. Comprobación rápida de linter
make lint       # ejecuta: python3 -m ruff check .

# 2. Comprobación rápida de pruebas unitarias
make test       # ejecuta: python3 -m pytest -q

# 3. Validación exhaustiva de contratos, libros, notebooks y catálogo
make validate   # ejecuta la suite de 17 validadores

# 4. Comprobación integral completa
make check      # combina lint + test + validate + audit-simulations
```

---

## 12. Reglas Obligatorias para Futuros Agentes de IA

1. **No inventar abstracciones:** Desarrollar siempre dentro de las clases, funciones auxiliares y patrones existentes en `common/`, `core/` y `desarrollo/scripts/`.
2. **Preservar la identidad visual:** Utilizar `shared_ui_styles()`, `compact_labeled_control()`, `action_button_row()` y la paleta de `visual_roles.py`.
3. **Mínima intervención:** No modificar archivos fuera del alcance estricto de la tarea. No alterar contratos visuales de otros capítulos sin autorización expresa.
4. **Verificación obligatoria antes de reportar éxito:** Ninguna tarea se considera completa sin haber ejecutado `pytest -q`, `ruff check .` y `make validate`.
5. **Mantener este archivo actualizado:** Si una decisión técnica cambia el estado de la arquitectura, reflejarlo de inmediato en `PROJECT_CONTEXT.md`.
