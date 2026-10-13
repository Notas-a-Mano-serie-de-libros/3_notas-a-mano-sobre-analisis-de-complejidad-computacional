# Verificación de accesibilidad

## Comprobaciones automáticas

`smoke_portal_e2e.py` ejecuta el portal en Chromium con anchos de 375 y 1280 píxeles y con reducción de movimiento activa. Comprueba:

- desbordamiento horizontal y zoom al 200 %;
- estructura de encabezados y fórmulas sin procesar;
- nombre accesible de enlaces, botones, campos e iframes visibles;
- acceso por teclado y foco visible inicial.

`validate_widget_contracts.py` comprueba las ayudas accesibles de los controles compartidos de `ipywidgets`. Estas pruebas son una barrera de regresión, no una certificación WCAG.

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
