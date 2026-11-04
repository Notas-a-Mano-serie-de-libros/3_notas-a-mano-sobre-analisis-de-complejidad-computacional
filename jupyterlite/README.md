# Demo de JupyterLite

Este directorio contiene la configuración de los laboratorios que se publican
dentro del complemento digital. El contenido se toma de los archivos canónicos
del repositorio durante la compilación; no se mantienen copias de los notebooks
ni de los módulos de simulación.

Para construir el demo después de generar el sitio de MkDocs:

```bash
python desarrollo/scripts/build_jupyterlite_demo.py
```

El catálogo centralizado agrupa los capítulos que comparten dependencias en
cuatro sitios: `graficas` (capítulos 2, 4, 6 y 8),
`graficas-cientificas` (capítulo 3), `algebra-simbolica` (capítulo 5) y
`analisis-completo` (capítulo 7). Así se comparten los bundles de JupyterLab sin
forzar a todos los capítulos a cargar el conjunto máximo de paquetes. Las
páginas se sincronizan con estos perfiles mediante:

```bash
python desarrollo/scripts/sync_jupyterlite_urls.py
```

Las dependencias de Python se configuran en las opciones de inicio del kernel
Pyodide para que se carguen antes de abrir los notebooks, sin celdas de
instalación auxiliares. El kernel predeterminado se inicia automáticamente al
abrir una simulación, sin pedir que se seleccione en cada ejecución. Una
extensión ligera ejecuta las celdas al quedar listo el kernel; no modifica ni
añade celdas a los notebooks. La extensión se compila durante la generación del
sitio con Node.js. Los accesos a Colab y pantalla completa quedan debajo del
iframe para que la simulación aparezca primero. Después de compilar, el
validador del artefacto revisa
las rutas, la configuración del kernel, la presencia de paquetes, las celdas de
solo lectura y el presupuesto total de tamaño:

```bash
python desarrollo/scripts/validate_jupyterlite_artifact.py
```

Esta comprobación valida el sitio compilado, pero no abre un navegador ni
ejecuta un kernel Pyodide real.
