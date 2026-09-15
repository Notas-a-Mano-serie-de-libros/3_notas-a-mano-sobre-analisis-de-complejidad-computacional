# Notas a mano sobre análisis de complejidad computacional

## Complemento digital de la obra

Este repositorio reúne las simulaciones interactivas de la segunda edición del libro de **Carlos Eduardo Orozco Garcés**, **César Jesús Pardo Calvache** y **Mauro Callejas Cuervo**. El libro desarrolla la teoría; [Pages](https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/) organiza los capítulos y enlaza las simulaciones de Google Colab. También puede ejecutarlas localmente con **Jupyter**, siguiendo esta guía.

<p align="center">
  <a href="https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/actions/workflows/ci.yml"><img src="https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/actions/workflows/ci.yml/badge.svg" alt="Estado de CI"></a>
  <a href="https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/actions/workflows/pages.yml"><img src="https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/actions/workflows/pages.yml/badge.svg" alt="Estado de GitHub Pages"></a>
  <a href="https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/actions/workflows/codeql.yml"><img src="https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/actions/workflows/codeql.yml/badge.svg" alt="Estado de CodeQL"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&amp;logoColor=white" alt="Python 3.10 o superior">
  <img src="https://img.shields.io/badge/Jupyter-Simulaciones-F37626?logo=jupyter&amp;logoColor=white" alt="Simulaciones en Jupyter">
  <img src="https://img.shields.io/badge/Edición-Segunda-1f4e79" alt="Segunda edición">
  <a href="LICENSE"><img src="https://img.shields.io/badge/Código-MIT-green.svg" alt="Licencia MIT para el código"></a>
</p>

<p align="center">
  <a href="https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/">
    <img src="https://raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/main/assets/qr/pages-inicio.png" width="168" alt="Código QR del complemento digital de la obra">
  </a>
  <br>
  <strong><a href="https://notas-a-mano-serie-de-libros.github.io/3_notas-a-mano-sobre-analisis-de-complejidad-computacional/">Consultar el complemento digital</a></strong>
</p>

## Inicio rápido

```bash
git clone https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional.git
cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt -c requirements-lock.txt jupyterlab jupyterlab_widgets ipykernel "tornado<6.5.9"
python -m jupyter lab simulaciones/capitulo2/notebooks/
```

En Windows PowerShell, active el entorno con `.venv\Scripts\Activate.ps1`. La guía siguiente explica cada paso y permite abrir los demás capítulos.

## Compatibilidad verificada

| Componente | Versión o entorno |
| --- | --- |
| Python | 3.10 o superior |
| JupyterLab | Versión resuelta con `requirements-lock.txt` |
| Navegadores | Chrome, Edge, Firefox y Safari actuales |
| Sistemas | Linux, macOS y Windows |

## Guía de instalación

Necesita Python 3.10 o superior y Git. Siga estos pasos en orden, completos, en una terminal — no son opcionales ni intercambiables entre sí.

### 1. Cierre cualquier Jupyter que ya esté corriendo

Si tiene JupyterLab abierto (de este proyecto o de cualquier otro), ciérrelo por completo antes de continuar: vaya a cada terminal donde lo lanzó y presione `Ctrl+C` dos veces. Un servidor viejo que queda corriendo en segundo plano ocupa el puerto por defecto (8888) y JupyterLab abre uno nuevo en otro puerto sin avisarlo con claridad, lo que lleva a que termine mirando una pestaña conectada al proceso equivocado.

### 2. Clone el proyecto

```bash
git clone https://github.com/Notas-a-Mano-serie-de-libros/3_notas-a-mano-sobre-analisis-de-complejidad-computacional.git
cd 3_notas-a-mano-sobre-analisis-de-complejidad-computacional
```

### 3. Prepare un entorno nuevo y aislado

**No instale ni ejecute este proyecto dentro del entorno `base` de Anaconda/Miniconda**, ni dentro de ningún entorno conda que ya tenga instalados otros paquetes de widgets/notebooks (`bqplot`, `voila`, `panel`, `ipyleaflet`, `ipytree`, `anywidget`, etc.). Esos paquetes instalan sus propias extensiones de JupyterLab y fijan versiones de `ipywidgets`/`jupyterlab_widgets` que compiten con las de este proyecto — es la causa más común de que los controles o las fórmulas de las animaciones se vean mal.

Si su terminal muestra `(base)` (o el nombre de cualquier otro entorno conda) al inicio de la línea de comandos, desactívelo primero:

```bash
conda deactivate
```

Luego cree y active el entorno virtual del proyecto:

```bash
python3 -m venv .venv
```

| Sistema | Comando para activar |
| --- | --- |
| Linux / macOS | `source .venv/bin/activate` |
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |

Confirme que quedó activo: el inicio de la línea de comandos debe mostrar `(.venv)`, no `(base)` ni ningún otro nombre de entorno conda.

### 4. Instale las dependencias y Jupyter

Este único comando instala, en el entorno recién creado (sin nada más que pueda entrar en conflicto), todo lo necesario — incluyendo versiones de `jupyterlab`, `ipywidgets`, `jupyterlab_widgets` y `tornado` resueltas juntas y mutuamente compatibles:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt -c requirements-lock.txt jupyterlab jupyterlab_widgets ipykernel "tornado<6.5.9"
```

Con los cuatro pasos anteriores el entorno queda listo de una vez — no hace falta repetir ni ajustar comandos después, ni ejecutar verificaciones manuales antes de abrir las animaciones.

Las versiones de las dependencias usadas por CI están registradas en `requirements-lock.txt`. Las carpetas `.ipynb_checkpoints` y `.virtual_documents` son archivos temporales de Jupyter; no forman parte de las simulaciones y se pueden borrar si aparecen. El comando `make clean-notebooks` limpia salidas y metadatos generados sin tocar el código fuente.

## Guía de ejecución de animaciones por capítulo

Desde la **raíz del proyecto**, con el entorno virtual activo, ejecute el comando del capítulo que quiera explorar. Jupyter Lab abrirá la carpeta con sus notebooks en el navegador. Elija la simulación que desee, abra su notebook y seleccione **Ejecutar todas las celdas** para mostrar los controles e iniciar la animación. Puede abrir otros notebooks del mismo capítulo desde el explorador de archivos de Jupyter Lab.

La ejecución local aprovecha los recursos del equipo y evita los límites de sesión de Colab. Los retrasos en entornos remotos pueden deberse a su latencia o a la disponibilidad de recursos.

**Capítulo 2: Fundamentos del análisis de algoritmos**

```bash
jupyter lab simulaciones/capitulo2/notebooks/
```

**Capítulo 3: Notación asintótica**

```bash
jupyter lab simulaciones/capitulo3/notebooks/
```

**Capítulo 4: Análisis de algoritmos estructurados**

```bash
jupyter lab simulaciones/capitulo4/notebooks/
```

**Capítulo 5: Relaciones de recurrencia**

```bash
jupyter lab simulaciones/capitulo5/notebooks/
```

**Capítulo 6: Análisis de algoritmos recursivos**

```bash
jupyter lab simulaciones/capitulo6/notebooks/
```

**Capítulo 7: Algoritmos de búsqueda**

```bash
jupyter lab simulaciones/capitulo7/notebooks/
```

**Capítulo 8: Algoritmos de ordenamiento**

```bash
jupyter lab simulaciones/capitulo8/notebooks/
```
