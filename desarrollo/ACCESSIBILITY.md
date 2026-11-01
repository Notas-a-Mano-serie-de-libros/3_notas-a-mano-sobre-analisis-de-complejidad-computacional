# Verificación de accesibilidad

## Comprobaciones automáticas

`smoke_portal_e2e.py` ejecuta una matriz representativa de todos los capítulos en Chromium con anchos de 320, 375 y 1280 píxeles y con reducción de movimiento activa. Comprueba:

- desbordamiento horizontal, reflujo a 320 píxeles y zoom al 200 % y 400 %;
- estructura de encabezados y fórmulas sin procesar;
- nombre accesible de enlaces, botones, campos e iframes visibles;
- acceso por teclado y foco visible inicial.

`validate_widget_contracts.py` comprueba las ayudas accesibles de los controles compartidos de `ipywidgets`, el foco visible, el modo de colores forzados, el estado de paneles y pestañas, los resúmenes dinámicos y las alternativas textuales de arreglos. Estas pruebas son una barrera de regresión, no una certificación WCAG.

Las simulaciones publicadas ofrecen una descripción textual desplegable de cada arreglo y un resumen dinámico independiente del color. Durante la ejecución automática se silencian los pasos intermedios y se anuncia el resultado final para no saturar la cola del lector de pantalla. En JupyterLite, la extensión asigna `aria-expanded`, `aria-controls`, `tablist`, `tab` y `tabpanel`, y habilita flechas, Inicio y Fin para navegar entre pestañas.

La integración de Axe o Pa11y debe hacerse con una dependencia fijada y su lock transitivo; no debe descargarse una versión flotante durante CI.

## Matriz manual antes de publicar

Debe registrarse resultado, navegador, sistema operativo y commit para:

1. navegación completa mediante Tab, Mayús+Tab, flechas, Enter, Espacio y Escape;
2. orden de foco dentro de cada simulación y devolución del foco al cerrar paneles;
3. VoiceOver con Safari y NVDA con Firefox o Chrome;
4. zoom del navegador al 200 % sin pérdida de controles ni contenido;
5. `prefers-reduced-motion: reduce` durante reproducción y restablecimiento;
6. contraste de los estados normal, hover, focus, activo y deshabilitado;
7. cambios repetidos de parámetros mientras una animación está activa.

Una comprobación automática satisfactoria no sustituye esta matriz, especialmente para lectores de pantalla y el orden semántico de gráficos complejos.
