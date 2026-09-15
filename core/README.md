# Núcleo de simulaciones

`core` contiene la lógica de dominio que no pertenece a los notebooks.

- `search`: algoritmos, estados, métricas y renderizadores de búsqueda.
- `sort`: algoritmos, trazas, métricas y renderizadores de ordenamiento.

Los capítulos conservan únicamente notebooks y adaptadores de ejecución. Las
vistas de los motores se componen mediante `common.simulation_views`; los
controles de bajo nivel permanecen en `common.widget_controls`.

No se deben volver a crear carpetas `domain` dentro de los capítulos. Una
nueva familia de simulaciones debe añadirse como paquete de `core` y declarar
sus secciones y acciones con el contrato común de vistas.
