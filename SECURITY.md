# Seguridad y recursos ejecutables

## Fronteras de confianza

El portal ejecuta código propio en Web Workers e iframes. Los archivos remotos permitidos son dependencias declaradas y versionadas:

| Recurso | Uso | Política |
| --- | --- | --- |
| MathJax 3.2.2 | Fórmulas del portal y las simulaciones | Versión exacta y SRI tanto en la plantilla como en los documentos `srcdoc`. |
| Pyodide v314.0.6 | Ejemplos Python en Web Worker | Versión exacta; el worker no recibe credenciales ni almacenamiento del sitio. |
| CheerpJ | Ejemplos Java aislados en iframe | Solo carga al ejecutar Java; no se considera código del repositorio. |
| Cloudflare Turnstile | Protección del formulario de comentarios | La API pública `v0` solo carga cuando el formulario está disponible; no participa en la lectura ni en las simulaciones. |
| `raw.githubusercontent.com/Notas-a-Mano-serie-de-libros/.../main` | Bootstrap y módulos de los notebooks abiertos en Colab | Se ejecuta como código confiable del mantenedor. Cada cambio en `main` cambia lo que ejecutará Colab y debe pasar revisión, CI, CodeQL y escaneo de secretos. |
| JupyterLite/Pyodide kernel | Notebooks en el navegador | Se genera desde dependencias fijadas y se publica dentro del artefacto de Pages. |

No se admite código remoto con ramas o URL distintas de la lista permitida. Turnstile conserva su endpoint público `v0` porque Cloudflare no publica esa API con una versión de archivo inmutable; por eso se limita a un formulario no esencial. `validate_web_dependencies.py` hace cumplir las URL conocidas. El empaquetado local de MathJax es viable y reduciría esta frontera de red; el de Pyodide debe evaluarse junto con el presupuesto de tamaño antes de duplicar lo que JupyterLite ya distribuye.

## Controles de publicación

- CI ejecuta pruebas, Ruff, `pip-audit` y un escaneo de formatos conocidos de secretos.
- CodeQL analiza cada `push` y `pull_request`. Antes de desplegar, debe comprobarse que el análisis del mismo commit esté aprobado mediante la protección de rama de GitHub.
- Las acciones se referencian por SHA y el job de construcción de Pages solo posee `contents: read`.
- `pages: write` e `id-token: write` pertenecen exclusivamente al job de despliegue.

Los hallazgos deben reportarse de forma privada al mantenedor; no se deben incluir credenciales ni pruebas de explotación en incidencias públicas.

## Código remoto de Colab

Los notebooks prefieren archivos locales en JupyterLite y en una clonación. En Colab descargan el bootstrap y sus módulos desde la rama `main` de este mismo repositorio y luego los ejecutan. Esa descarga no es contenido pasivo: tiene los mismos privilegios que una celda del notebook. Por ello, la protección de `main` debe exigir revisión y todos los checks del commit. Para ejecuciones científicas archivables se debe sustituir `main` por el SHA del commit publicado en las URL del notebook o conservar una copia completa del repositorio.
