# Demo de JupyterLite

Este directorio contiene la configuración de los laboratorios que se publican
dentro del complemento digital. El contenido se toma de los archivos canónicos
del repositorio durante la compilación; no se mantienen copias de los notebooks
ni de los módulos de simulación.

Para construir el demo después de generar el sitio de MkDocs:

```bash
python desarrollo/scripts/build_jupyterlite_demo.py
```

Los resultados de los capítulos 2 a 8 se escriben en sus directorios
`site/jupyterlite/capitulo-N/`. Cada sitio incluye solo los notebooks y módulos
de runtime que necesita ese capítulo. Las dependencias de Python se configuran
en las opciones de inicio del kernel Pyodide para que se carguen antes de abrir
los notebooks, sin celdas de instalación auxiliares.
