# Copias canónicas para Pages

Las imágenes de esta carpeta que aparecen en `page_asset_sources.json` son copias importadas de las figuras utilizadas por la versión LaTeX del libro. Se guardan aquí para que el portal sea reproducible y no dependa de otro repositorio ni de una ruta local al manuscrito.

Para actualizar una figura, se copia manualmente la versión insertada en el manuscrito a esta carpeta y se ejecutan:

```text
python desarrollo/scripts/sync_page_assets.py
python desarrollo/scripts/validate_page_assets.py
```

El proceso de construcción solo lee archivos de este repositorio. No abre ni modifica el proyecto LaTeX.
