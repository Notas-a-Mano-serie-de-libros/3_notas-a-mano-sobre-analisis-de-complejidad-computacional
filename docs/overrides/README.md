# Personalizaciones de tema para MkDocs Material (Overrides)

Este directorio contiene las plantillas personalizadas (`theme.custom_dir = docs/overrides`) que extienden el tema `material`:

- **`main.html`**:
  - Inyecta metadatos editoriales (autoría, edición, Open Graph).
  - Incluye la carga de MathJax con integridad SRI SHA-384.
  - Renderiza componentes visuales contextuales: panel de navegación superior, barra de progreso de lectura, lightbox accesible de figuras y llamadas de cierre de sección (`section_closings.html`).

- **`home.html`**:
  - Estructura personalizada para la portada del sitio.

- **`section_closings.html`**:
  - Mensajes de síntesis pedagógica específicos al final de cada sección temática.

- **`partials/`**:
  - Bloques modulares reutilizables por las plantillas.

> [!NOTE]
> **Compatibilidad con MkDocs 2.0**:
> MkDocs 2.0 modificará el sistema de extensiones y overrides de plantillas. Al actualizar versiones mayores de MkDocs o de `mkdocs-material`, revise los bloques `{% block %}` extendidos en `main.html` contra la especificación vigente del tema.
