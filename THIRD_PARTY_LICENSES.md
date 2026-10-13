# Dependencias y licencias de terceros

Este inventario cubre los componentes que el portal distribuye o carga en tiempo de ejecución. No reemplaza los avisos incluidos en cada distribución.

| Componente | Versión usada | Licencia / condición | Acción de publicación |
| --- | --- | --- | --- |
| MathJax | 3.2.2 | Apache-2.0 | Conservar avisos si se empaqueta localmente. |
| Pyodide | v314.0.6 en el ejecutor; versión resuelta por JupyterLite para notebooks | MPL-2.0 y licencias de paquetes incluidos | Conservar avisos del artefacto generado. |
| JupyterLite | 0.8.6 | BSD-3-Clause | Conservar copyright y licencia en redistribuciones. |
| jupyterlite-pyodide-kernel | 0.8.6 | BSD-3-Clause | Conservar copyright y licencia. |
| ipywidgets | 8.1.9 | BSD-3-Clause | Conservar copyright y licencia. |
| MkDocs Material | 9.7.7 | MIT | Conservar copyright y licencia. |
| CheerpJ | servicio externo | Licencia comunitaria o comercial según el uso | Confirmar con Leaning Technologies que la publicación institucional concreta es elegible antes de producción. |

La comprobación de licencias debe repetirse cuando cambie una versión. En especial, CheerpJ no debe declararse “libre” solo porque pueda cargarse sin credenciales: sus condiciones distinguen entre uso comunitario, evaluación y otros usos organizacionales.
